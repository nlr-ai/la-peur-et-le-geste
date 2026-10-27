# -*- coding: utf-8 -*-
"""RUNTIME GEMINI — l'appel `agy`, sorti de runtime.py.

`agy` n'a pas d'option de prompt systeme, mais il lit l'AGENTS.md de son
dossier de lancement A CHAQUE APPEL, reprise comprise, et il ne le range pas
dans l'historique (mesure du 4.10 : un AGENTS.md change entre deux tours d'une
meme conversation est obei au second). C'est donc la qu'on pose le manuel,
au lieu de le coller en tete du message.

Il lit AUSSI l'AGENTS.md de chaque `--add-dir` : avec le depot monte, chaque
MJ et chaque PNJ recevait en plus le miroir de CLAUDE.md racine (90 ko de
manuel du MJ de Peyredragon), quel que soit le monde. Et il n'a pas besoin de
ces dossiers pour lire, ecrire ou lancer une commande dans le depot une fois
les permissions levees : on ne les lui passe plus.

LA REPRISE (7.10). `agy` n'a pas de --resume : il reprend par
`--conversation <id>`, mais avec SON identifiant (`conversation_id`, rendu
dans le JSON de sortie), jamais avec le notre — un id qu'il ne connait pas
donne « conversation not found » et une conversation NEUVE, sans erreur.
Jusqu'ici on lui passait notre id logique, et seulement apres un premier
essai sans id qui reussissait toujours : aucun MJ Gemini n'a jamais repris sa
session, chaque tour relisait tout. On tient donc la table id logique ->
conversation agy dans .agents-runtime/gemini-conversations.json.
"""
import io
import json
import os
import re
import subprocess
import uuid

from agents import runtime as _rt


def _dans_le_depot(cwd):
    racine = os.path.normcase(os.path.abspath(_rt.RACINE))
    ici = os.path.normcase(os.path.abspath(cwd))
    return ici == racine or ici.startswith(racine + os.sep)


def _poser_agents_md(manuel, cwd):
    """Pose le manuel en AGENTS.md du pas-de-tir ; False si le pas-de-tir
    est dans le depot, dont on n'ecrase jamais l'AGENTS.md."""
    if _dans_le_depot(cwd):
        return False
    chemin = os.path.join(cwd, "AGENTS.md")
    temporaire = chemin + ".%s.tmp" % uuid.uuid4().hex
    with io.open(temporaire, "w", encoding="utf-8", newline="\n") as f:
        f.write(manuel)
    os.replace(temporaire, chemin)
    return True


_TABLE = os.path.join(_rt.DOSSIER_RUNTIME, "gemini-conversations.json")


def _table():
    try:
        with io.open(_TABLE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def conversation_de(logique):
    """L'id agy de la conversation tenue sous cet id logique, ou None."""
    return _table().get(str(logique))


def retenir(logique, conversation):
    """Relit la table juste avant d'ecrire : deux sessions paralleles ne
    s'effacent pas leurs entrees."""
    if not conversation:
        return
    t = _table()
    if t.get(str(logique)) == conversation:
        return
    t[str(logique)] = conversation
    os.makedirs(os.path.dirname(_TABLE), exist_ok=True)
    temporaire = _TABLE + ".%s.tmp" % uuid.uuid4().hex
    with io.open(temporaire, "w", encoding="utf-8", newline="\n") as f:
        json.dump(t, f, ensure_ascii=False, indent=2)
    os.replace(temporaire, _TABLE)


def commande(modele, sid, reprendre, restreint=False):
    nom_binaire = (r"C:\Users\reyno\AppData\Local\agy\bin\agy.exe"
                   if os.name == "nt" else "agy")
    cmd = [nom_binaire, "--output-format", "json"]
    if restreint:
        # Restriction native du terminal, sans approbation automatique.
        # Ce drapeau ne constitue pas une liste blanche des outils Web.
        cmd += ["--sandbox"]
    else:
        cmd += ["--dangerously-skip-permissions"]
    if modele:
        cmd += ["--model", modele]
    if reprendre:
        cmd += ["--conversation", sid]
    return cmd


def appeler(manuel, message, logique, modele, effort, timeout, cwd,
            add_dirs, tools, settings, reprendre, env):
    # reprendre=False : conversation neuve, voulue. Sinon (True ou None) on
    # reprend la conversation agy retenue pour cet id logique, s'il y en a une.
    connue = None if reprendre is False else conversation_de(logique)
    essais = [connue] if connue else [None]
    dernier = ""
    for conversation in essais:
        pose = _poser_agents_md(manuel, cwd)
        texte_entree = message if pose else (manuel + "\n\n" + message)
        cmd = commande(modele, conversation, bool(conversation),
                       restreint=env.get("CONSEIL_MONDE") == "argent-intelligent")
        audit = bool(tools and "WebSearch" in tools)
        audit_id = uuid.uuid4().hex
        log_path = os.path.join(cwd, "gemini-recherche-%s.log" % audit_id)
        output_path = os.path.join(cwd, "gemini-recherche-%s.json" % audit_id)
        if audit:
            cmd += ["--log-file", log_path]
        r = subprocess.run(cmd, cwd=cwd,
                           env=env, input=texte_entree.encode("utf-8"),
                           capture_output=True, timeout=timeout,
                           **_rt._creation_sans_fenetre())
        code = r.returncode
        sortie = r.stdout.decode("utf-8", "replace")
        erreurs = [r.stderr.decode("utf-8", "replace")]
        if audit:
            with io.open(output_path, "w", encoding="utf-8") as f:
                f.write(sortie)

        resultat = None
        try:
            resultat = json.loads(sortie)
        except ValueError:
            m = re.search(r"\{.*\}", sortie, re.DOTALL)
            if m:
                try:
                    resultat = json.loads(m.group(0))
                except ValueError:
                    resultat = None

        dernier = sortie + "\n" + "\n".join(erreurs)
        if code != 0:
            raise RuntimeError(("\n".join(erreurs) + "\n" + sortie or
                                "gemini a quitte avec le code %d" % code)[-800:])
        if not resultat:
            raise RuntimeError("le flux Gemini s'est ferme sans resultat")

        # Une conversation perdue (« not found ») est repartie neuve : on
        # retient la nouvelle, la prochaine reprise tombera juste.
        retenir(logique, resultat.get("conversation_id"))
        resultat.setdefault("provider", "gemini")
        resultat.setdefault("logical_session_id", logique)
        resultat.setdefault("session_id", logique)
        resultat.setdefault("model", modele or "defaut")
        if audit:
            # Le résultat et le journal brut permettent un audit ; leur présence
            # seule ne prouve pas qu'un article a été consulté.
            resultat["transcript_path"] = output_path
            resultat["research_log_path"] = log_path if os.path.isfile(log_path) else None
        if "response" in resultat and "result" not in resultat:
            resultat["result"] = resultat.pop("response")
        _rt._poser_empreinte_manuel(logique, "gemini",
                                    _rt._empreinte_manuel(manuel))
        return resultat
    raise RuntimeError("l'appel Gemini n'a pas abouti : %s"
                       % dernier[-400:])
