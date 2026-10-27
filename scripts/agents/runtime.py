# -*- coding: utf-8 -*-
"""RUNTIME — une seule porte vers les CLI d'agents Claude et Codex.

Le jeu connait des sessions logiques (un homme, un jour ; l'unique MJ ;
un narrateur d'activation). Le fournisseur, lui, a son propre identifiant de
thread. Ce module garde cette traduction et rend toujours le vieux contrat
Claude ``{result, usage, ...}`` aux appelants.

Le choix global se fait avec ``python scripts/fournisseur.py`` ou, pour une
commande seulement, ``LE_CONSEIL_FOURNISSEUR=claude|codex``.
"""
import contextlib
import ctypes
import datetime as dt
import hashlib
import io
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import uuid


RACINE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
DOSSIER_RUNTIME = os.path.join(RACINE, ".agents-runtime")
CONFIG = os.path.join(DOSSIER_RUNTIME, "config.json")
SESSIONS = os.path.join(DOSSIER_RUNTIME, "sessions.json")
REQUETES = os.path.join(DOSSIER_RUNTIME, "requests")
ACTIVITES = os.path.join(DOSSIER_RUNTIME, "active")
MAX_SESSIONS_ACTIVES = 15
RESERVATION_ENV = "LE_CONSEIL_RESERVATION_SESSION"

FOURNISSEURS = {"claude": "claude", "codex": "codex", "chatgpt": "codex", "gemini": "gemini"}
MODELE_CODEX = "gpt-5.3-codex-spark"
EFFORT_CODEX = "low"


def _lire_json(chemin, defaut):
    if not os.path.exists(chemin):
        return defaut
    with io.open(chemin, encoding="utf-8") as f:
        return json.load(f)


def _ecrire_json(chemin, valeur):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    temporaire = chemin + ".%s.tmp" % uuid.uuid4().hex
    with io.open(temporaire, "w", encoding="utf-8", newline="\n") as f:
        json.dump(valeur, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(temporaire, chemin)


def configuration():
    d = _lire_json(CONFIG, {})
    brut = (os.environ.get("LE_CONSEIL_FOURNISSEUR") or
            os.environ.get("LE_CONSEIL_AGENT_PROVIDER") or
            d.get("fournisseur") or d.get("provider") or "claude")
    nom = FOURNISSEURS.get(str(brut).casefold())
    if not nom:
        raise RuntimeError("fournisseur d'agent inconnu : %s" % brut)
    return {
        "fournisseur": nom,
        "executable_codex": (os.environ.get("LE_CONSEIL_CODEX_EXECUTABLE") or
                             d.get("executable_codex") or "codex"),
        "modele_codex": (os.environ.get("LE_CONSEIL_CODEX_MODELE") or
                          os.environ.get("LE_CONSEIL_CODEX_MODEL") or
                          d.get("modele_codex") or MODELE_CODEX),
        "effort_codex": (os.environ.get("LE_CONSEIL_CODEX_EFFORT") or
                          d.get("effort_codex") or EFFORT_CODEX),
        "service_tier_codex": (
            os.environ.get("LE_CONSEIL_CODEX_SERVICE_TIER") or
            d.get("service_tier_codex")),
        "modele_claude": (os.environ.get("LE_CONSEIL_CLAUDE_MODELE") or
                           os.environ.get("LE_CONSEIL_CLAUDE_MODEL") or
                           d.get("modele_claude")),
        "modele_gemini": (os.environ.get("LE_CONSEIL_GEMINI_MODELE") or
                           os.environ.get("LE_CONSEIL_GEMINI_MODEL") or
                           d.get("modele_gemini")),
    }


def fournisseur():
    return configuration()["fournisseur"]


def choisir(nom, modele=None, effort=None, fast=None):
    """Pose le choix local global. L'environnement reste prioritaire."""
    canonique = FOURNISSEURS.get(str(nom).casefold())
    if not canonique:
        raise ValueError("choisir claude, codex ou chatgpt")
    d = _lire_json(CONFIG, {})
    d["fournisseur"] = canonique
    if canonique == "codex":
        if modele:
            d["modele_codex"] = modele
        if effort:
            d["effort_codex"] = effort
        if fast is not None:
            d["service_tier_codex"] = "fast" if fast else None
    elif canonique == "gemini" and modele:
        d["modele_gemini"] = modele
    elif modele:
        d["modele_claude"] = modele
    _ecrire_json(CONFIG, d)
    return configuration()


def _modele(provider, demande):
    cfg = configuration()
    if provider == "codex":
        # Les CLI historiques donnent souvent `opus` ou `sonnet`. Ce ne sont
        # pas des choix Codex : la bascule globale doit suffire a elle seule.
        if demande and (str(demande).startswith("gpt-") or
                        "codex" in str(demande).casefold()):
            return str(demande)
        return cfg["modele_codex"]
    if provider == "gemini":
        return str(demande) if demande else cfg.get("modele_gemini")
    if demande and not (str(demande).startswith("gpt-") or
                        "codex" in str(demande).casefold()):
        return str(demande)
    return cfg.get("modele_claude")


def _effort(provider, demande):
    if provider == "codex":
        return str(demande or configuration()["effort_codex"])
    return str(demande) if demande else None


def _service_tier(provider):
    if provider == "codex":
        return configuration().get("service_tier_codex")
    return None


def _identite_processus(pid):
    """Identité de naissance d'un PID, pour ne pas compter un PID réutilisé."""
    try:
        pid = int(pid)
        if os.name == "nt":
            kernel = ctypes.windll.kernel32
            handle = kernel.OpenProcess(0x1000, False, pid)
            if not handle:
                return None
            try:
                exit_code = ctypes.c_ulong()
                if (not kernel.GetExitCodeProcess(handle, ctypes.byref(exit_code))
                        or exit_code.value != 259):  # STILL_ACTIVE
                    return None
                creation = ctypes.c_ulonglong()
                sortie = [ctypes.c_ulonglong() for _ in range(3)]
                ok = kernel.GetProcessTimes(
                    handle, ctypes.byref(creation), ctypes.byref(sortie[0]),
                    ctypes.byref(sortie[1]), ctypes.byref(sortie[2]))
                return "win:%d" % creation.value if ok else None
            finally:
                kernel.CloseHandle(handle)
        stat = "/proc/%d/stat" % pid
        if os.path.exists(stat):
            with io.open(stat, encoding="utf-8") as f:
                # Le nom entre parenthèses peut contenir des espaces ; les
                # champs qui suivent commencent après la dernière parenthèse.
                suite = f.read().rsplit(")", 1)[1].split()
            return "proc:%s" % suite[19]  # champ 22 : starttime
        os.kill(pid, 0)
        return "pid:%d" % pid
    except (OSError, ValueError, IndexError, TypeError):  # voyant disparu -> pid None (10.9)
        return None


@contextlib.contextmanager
def _verrou_activites():
    os.makedirs(ACTIVITES, exist_ok=True)
    chemin = os.path.join(ACTIVITES, ".admission.lock")
    limite = time.time() + 10
    while True:
        try:
            fd = os.open(chemin, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(chemin) > 30:
                    os.remove(chemin)
                    continue
            except OSError:
                continue
            if time.time() >= limite:
                raise RuntimeError("garde des wake-up calls occupée depuis 10 s")
            time.sleep(.02)
    try:
        yield
    finally:
        try:
            os.remove(chemin)
        except OSError:
            pass


def _marqueurs_vivants():
    """Nettoie les morts et rend les slots actifs/réservés. Verrou requis."""
    maintenant = time.time()
    vivants = []
    for nom in os.listdir(ACTIVITES):
        if not nom.endswith(".json"):
            continue
        chemin = os.path.join(ACTIVITES, nom)
        try:
            d = _lire_json(chemin, {})
        except (OSError, ValueError):
            d = {}
        pid = d.get("pid")
        if pid is None and d.get("reserve"):
            vivant = maintenant - float(d.get("t") or 0) <= 60
        else:
            identite = _identite_processus(pid)
            attendue = d.get("processus")
            # Compatibilité de déploiement : un ancien voyant sans identité ne
            # survit que cinq minutes. Les nouveaux résistent aux sessions très
            # longues et aux PID recyclés.
            vivant = bool(identite and (
                identite == attendue if attendue else
                maintenant - float(d.get("t") or 0) <= 300))
        if vivant:
            vivants.append((chemin, d))
        else:
            try:
                os.remove(chemin)
            except OSError:
                pass
    return vivants


def _essayer_reserver(role, session_id, pid=None):
    """Prend atomiquement un des quinze slots, ou rend None."""
    with _verrou_activites():
        vivants = _marqueurs_vivants()
        monde = os.environ.get("CONSEIL_MONDE", "")
        plateau = os.environ.get("LE_CONSEIL_MODE") == "plateau"
        if any(d.get("homme") == str(role)
               and d.get("monde", monde) == monde
               and (plateau or d.get("mode") == "plateau")
               for _, d in vivants):
            return None
        if len(vivants) >= MAX_SESSIONS_ACTIVES:
            return None
        nom = "%s.json" % uuid.uuid4().hex
        chemin = os.path.join(ACTIVITES, nom)
        marqueur = {
            "monde": monde, "mode": os.environ.get("LE_CONSEIL_MODE", ""),
            "homme": str(role), "session": str(session_id),
            "pid": int(pid) if pid is not None else None,
            "processus": (_identite_processus(pid)
                            if pid is not None else None),
            "reserve": pid is None, "t": time.time(),
        }
        _ecrire_json(chemin, marqueur)
        return chemin


def activites_vivantes():
    """Relevé en lecture seule ; exclut réservations, morts et PID recyclés."""
    actifs = []
    if not os.path.isdir(ACTIVITES):
        return actifs
    for nom in os.listdir(ACTIVITES):
        if not nom.endswith(".json"):
            continue
        try:
            d = _lire_json(os.path.join(ACTIVITES, nom), {})
            identite = _identite_processus(d.get("pid"))
            if identite and identite == d.get("processus") and not d.get("reserve"):
                actifs.append({k: d.get(k) for k in
                               ("homme", "session", "racine", "monde", "pour", "t")})
        except (OSError, ValueError, TypeError, AttributeError):
            continue
    return actifs


def _attendre_slot(role, session_id, pid=None):
    debut, annonce = time.monotonic(), False
    while True:
        chemin = _essayer_reserver(role, session_id, pid=pid)
        if chemin:
            return chemin
        if not annonce and time.monotonic() - debut >= 1:
            sys.stderr.write(
                "GARDE WAKE-UP : 15 sessions actives ; %s attend un slot.\n"
                % role)
            sys.stderr.flush()
            annonce = True
        time.sleep(.25)


def _adopter_reservation(nom, role, session_id):
    if not re.match(r"^[a-f0-9]{32}\.json$", nom or ""):
        return None
    chemin = os.path.join(ACTIVITES, nom)
    with _verrou_activites():
        if not os.path.exists(chemin):
            return None
        d = _lire_json(chemin, {})
        d.update({"homme": str(role), "session": str(session_id),
                  "pid": os.getpid(),
                  "processus": _identite_processus(os.getpid()),
                  "reserve": False, "t": time.time()})
        _ecrire_json(chemin, d)
    return chemin


def _liberer_slot(chemin):
    try:
        os.remove(chemin)
    except OSError:
        pass


@contextlib.contextmanager
def _activite(role, session_id, env=None):
    """Prend un slot global puis expose la session réellement en calcul."""
    os.makedirs(ACTIVITES, exist_ok=True)
    reservation = os.environ.get(RESERVATION_ENV)
    chemin = (_adopter_reservation(reservation, role, session_id)
              if reservation else None)
    if not chemin:
        chemin = _attendre_slot(role, session_id, pid=os.getpid())
    try:
        if env:
            d = _lire_json(chemin, {})
            d.update({"racine": os.path.normcase(os.path.abspath(
                env.get("CONSEIL_RACINE") or RACINE)),
                "pour": env.get("LE_CONSEIL_AUDIENCE", "").split(",")})
            _ecrire_json(chemin, d)
        yield
    finally:
        _liberer_slot(chemin)


def _session_codex(logique):
    return _entree_session(logique).get("codex_thread_id")


def _entree_session(logique):
    return dict(_lire_json(SESSIONS, {}).get(str(logique)) or {})


def _poser_session_codex(logique, thread_id, modele, transcript=None,
                         manuel_sha256=None, interrompu=False):
    d = _lire_json(SESSIONS, {})
    entree = dict(d.get(str(logique)) or {})
    entree.update({
        "interrompu": interrompu,
        "codex_thread_id": thread_id,
        "modele": modele,
        "dernier_transcript": transcript,
        "mis_a_jour": dt.datetime.now().astimezone().isoformat(),
    })
    if manuel_sha256:
        entree["manuel_sha256_codex"] = manuel_sha256
    d[str(logique)] = entree
    _ecrire_json(SESSIONS, d)


def _poser_empreinte_manuel(logique, fournisseur, empreinte):
    d = _lire_json(SESSIONS, {})
    entree = dict(d.get(str(logique)) or {})
    entree["manuel_sha256_%s" % fournisseur] = empreinte
    entree["mis_a_jour"] = dt.datetime.now().astimezone().isoformat()
    d[str(logique)] = entree
    _ecrire_json(SESSIONS, d)


def _prompt_codex(manuel, cwd):
    chemin = os.path.join(cwd, "AGENTS.md")
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(u"# Manuel de ce réveil\n\n")
        f.write(manuel.strip() + u"\n\n")
        f.write(u"# Cadre technique\n\n"
                u"Tu es lancé sans interface depuis ce dossier neutre. "
                u"Respecte les chemins et les portes nommés dans le manuel. "
                u"Ta réponse finale est remise telle quelle au jeu.\n")
    return chemin


def _empreinte_manuel(manuel):
    return hashlib.sha256(manuel.encode("utf-8")).hexdigest()


def _retirer_prompt_codex(cwd):
    chemin = os.path.join(cwd, "AGENTS.md")
    try:
        os.remove(chemin)
    except FileNotFoundError:
        pass


def _preparer_prompt_codex(manuel, cwd, thread_id, entree):
    """Pose le gros manuel pour UN appel seulement s'il est neuf ou change.

    Le fichier est retire apres l'appel reussi : une reprise Codex garde son
    contexte de session et ne doit pas recharger 180 ko d'AGENTS.md a chaque
    reveil. L'empreinte rend les futures modifications injectables une fois.
    """
    empreinte = _empreinte_manuel(manuel)
    injecter = (not thread_id or
                entree.get("manuel_sha256_codex") != empreinte)
    if injecter:
        _prompt_codex(manuel, cwd)
    else:
        # Nettoie aussi les anciens fichiers persistants de l'ere ou le manuel
        # etait reecrit avant chaque resume.
        _retirer_prompt_codex(cwd)
    return empreinte, injecter


def _prompt_claude(manuel, cwd):
    # Un nom par appel : deux reveils paralleles dans le meme pas-de-tir
    # (deux scenes du MJ) ne s'ecrasent pas leur systeme l'un l'autre.
    chemin = os.path.join(cwd, "system-prompt-%s.md" % uuid.uuid4().hex)
    for tentative in range(8):
        try:
            with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
                f.write(manuel)
            break
        except OSError:
            if tentative == 7:
                raise
            time.sleep(min(0.5, 0.05 * (2 ** tentative)))
    return chemin


def _retirer_prompt_claude(chemin):
    try:
        os.remove(chemin)
    except (FileNotFoundError, TypeError):
        pass


def _preparer_prompt_claude(manuel, cwd, reprendre, entree):
    """Le systeme accompagne CHAQUE appel, reprise comprise.

    Claude ne range pas le prompt systeme dans la session : une reprise sans
    `--system-prompt-file` retombait sur le systeme par defaut de Claude Code,
    et le manuel disparaissait des le deuxieme reveil. Le cache de prompt rend
    ce renvoi presque gratuit ; il n'entre jamais dans l'historique."""
    return _empreinte_manuel(manuel), _prompt_claude(manuel, cwd), True


def _creation_sans_fenetre(detache=False):
    if os.name == "nt":
        return {"creationflags": 0x08000000 | (0x00000200 if detache else 0)}
    return {"start_new_session": True} if detache else {}


def _executer_flux(commande, message, cwd, env, timeout, on_event=None,
                   on_stderr=None, heartbeat=None, on_heartbeat=None,
                   transcript=None):
    processus = subprocess.Popen(
        commande, cwd=cwd, env=env, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace", bufsize=1,
        **_creation_sans_fenetre())
    processus.stdin.write(message)
    processus.stdin.close()
    messages = queue.Queue()

    def lire_flux(nom, flux):
        try:
            for ligne in iter(flux.readline, ""):
                messages.put((nom, ligne.rstrip("\r\n")))
        finally:
            flux.close()
            messages.put((nom, None))

    lecteurs = []
    for nom, flux in (("stdout", processus.stdout),
                      ("stderr", processus.stderr)):
        lecteur = threading.Thread(target=lire_flux, args=(nom, flux), daemon=True,
                                   name="agent-%s" % nom)
        lecteur.start()
        lecteurs.append(lecteur)

    # `timeout=None` : LA SESSION N'EXPIRE PAS. Un plafond ne se justifie que
    # s'il protege de quelque chose de nomme, et celui-ci ne protegeait de
    # rien : le processus rend la main quand il a fini. Ce qu'il faisait, en
    # revanche, se mesure — hann-bourbe, le 31.8, a travaille 20 appels
    # d'outils, fait son P.10, pose sa question a son arbitre, et le couperet
    # l'a tue au milieu : journee entiere perdue, zero octet ecrit, et le
    # traceback remonte dans sa propre pensee. Un plafond qui coupe un homme
    # au travail ne sauve rien ; il detruit ce qui etait presque fait.
    debut = time.monotonic()
    prochain = debut + (heartbeat or (timeout or 0) + 1)
    fin = (debut + timeout) if timeout else None
    ouverts, lignes, erreurs, evenements = 2, [], [], []
    operations = set()
    ticket_mj = env.get("LE_CONSEIL_MJ_TICKET")
    while ouverts or processus.poll() is None:
        maintenant = time.monotonic()
        if ticket_mj and not operations and messages.empty() and processus.poll() is None:
            from agents import file_mj
            if file_mj.plus_recent(ticket_mj):
                # Ne touche qu'au CLI du narrateur, jamais aux PNJ détachés.
                processus.terminate()
                try:
                    processus.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    processus.kill()
                    processus.wait(timeout=5)
                for lecteur in lecteurs:
                    lecteur.join(timeout=1)
                _sauver_transcript(transcript, message, evenements)
                raise file_mj.Interrompu(evenements)
        if fin is not None and maintenant >= fin:
            processus.kill()
            processus.wait(timeout=5)
            raise subprocess.TimeoutExpired(commande, timeout)
        bornes = [1.0, max(0.05, prochain - maintenant)]
        if fin is not None:
            bornes.append(max(0.05, fin - maintenant))
        attente = min(bornes)
        try:
            origine, ligne = messages.get(timeout=attente)
        except queue.Empty:
            origine, ligne = None, None
        if origine is not None:
            if ligne is None:
                ouverts -= 1
            elif origine == "stderr":
                erreurs.append(ligne)
                if on_stderr:
                    on_stderr(ligne)
            elif ligne:
                lignes.append(ligne)
                try:
                    ev = json.loads(ligne)
                except ValueError:
                    ev = None
                if ev is not None:
                    evenements.append(ev)
                    item = ev.get("item") or {}
                    if item.get("type") in ("command_execution", "mcp_tool_call", "file_change"):
                        if ev.get("type") == "item.started":
                            operations.add(item.get("id"))
                        elif ev.get("type") == "item.completed":
                            operations.discard(item.get("id"))
                    if on_event:
                        on_event(ev)
        maintenant = time.monotonic()
        if heartbeat and maintenant >= prochain:
            if on_heartbeat:
                on_heartbeat(round(maintenant - debut, 1))
            prochain = maintenant + heartbeat
    code = processus.wait()
    _sauver_transcript(transcript, message, evenements)
    return code, lignes, erreurs, evenements, time.monotonic() - debut


def _sauver_transcript(transcript, message, evenements):
    if transcript:
        with io.open(transcript, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"type": "le_conseil.user",
                                "message": message}, ensure_ascii=False) + "\n")
            for ev in evenements:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def _normaliser_codex(evenements, modele, duree, logique, transcript):
    thread_id, resultat, usage = None, u"", {}
    gestes = []
    erreur = None
    for ev in evenements:
        typ = ev.get("type")
        if typ == "thread.started":
            thread_id = ev.get("thread_id")
        elif typ == "turn.completed":
            usage = ev.get("usage") or usage
        elif typ in ("turn.failed", "error"):
            erreur = ev.get("error") or ev.get("message") or erreur
        elif typ == "item.completed":
            item = ev.get("item") or {}
            if item.get("type") == "agent_message":
                resultat = item.get("text") or resultat
            elif item.get("type") in ("command_execution", "mcp_tool_call",
                                      "file_change"):
                cible = (item.get("command") or item.get("name") or
                         item.get("path") or item.get("id") or "")
                gestes.append(u"%s %s" % (item.get("type"), str(cible)[:160]))
    if erreur:
        raise RuntimeError(str(erreur)[:500])
    return {
        "type": "result", "subtype": "success", "result": resultat,
        "session_id": thread_id or logique, "logical_session_id": logique,
        "provider": "codex", "model": modele, "usage": usage,
        "duration_ms": int(duree * 1000), "duration_api_ms": 0,
        "total_cost_usd": 0.0, "num_turns": 1,
        "transcript_path": transcript, "gestes": gestes,
    }


def _commande_codex(cwd, modele, effort, add_dirs, transcript_sortie,
                    thread_id=None, service_tier=None, recherche_web=False, restreint=False):
    commande = [
        configuration()["executable_codex"], "exec", "--ignore-user-config", "--ignore-rules",
        "--disable", "plugins", "--disable", "apps",
        "--disable", "memories", "--disable", "multi_agent",
        "--json", "--color", "never", "--skip-git-repo-check",
        "--cd", cwd,
        # Le manuel MJ assemble notamment le CLAUDE.md racine et depasse la
        # limite documentaire par defaut de Codex. Le bootstrap doit arriver
        # entier, meme s'il n'arrive desormais qu'une fois.
        "-c", "project_doc_max_bytes=524288",
        "--model", modele,
        "-c", 'model_reasoning_effort=%s' % json.dumps(effort),
        "--output-last-message", transcript_sortie,
    ]
    if recherche_web:
        commande += ["-c", 'web_search="live"']
    if service_tier:
        commande += ["-c", "service_tier=%s" % json.dumps(service_tier)]
    # Les appels d'agents travaillent directement dans le depot monte. La
    # distinction historique MJ sans sandbox / homme restreint n'avait pas
    # produit d'isolation utile : elle est retiree du contrat du runtime.
    if restreint:
        commande.remove("--ignore-rules")
        commande += ["--sandbox", "workspace-write", "-c", 'approval_policy="never"']
    else:
        commande += ["--dangerously-bypass-approvals-and-sandbox"]
    for chemin in add_dirs:
        commande += ["--add-dir", chemin]
    if thread_id:
        commande += ["resume", thread_id, "-"]
    else:
        commande += ["-"]
    return commande


def _appel_codex(manuel, message, logique, modele, effort, timeout, cwd,
                  add_dirs, reprendre, env, on_event, on_stderr, heartbeat,
                  on_heartbeat, service_tier=None, recherche_web=False):
    entree = _entree_session(logique)
    thread_id = entree.get("codex_thread_id")
    if reprendre is True and not thread_id:
        raise RuntimeError("aucun thread Codex pour reprendre %s" % logique)
    if reprendre is False:
        thread_id = None
        entree = {}
    manuel_sha256, prompt_injecte = _preparer_prompt_codex(
        manuel, cwd, thread_id, entree)
    final = os.path.join(cwd, ".dernier-message-%s.txt" % uuid.uuid4().hex)
    transcript = os.path.join(cwd, ".codex-%s.jsonl" % uuid.uuid4().hex)
    commande = _commande_codex(cwd, modele, effort, add_dirs, final,
                               thread_id, service_tier=service_tier, recherche_web=recherche_web,
                               restreint=env.get("CONSEIL_MONDE") == "argent-intelligent")
    from agents import file_mj
    try:
        code, _lignes, erreurs, evenements, duree = _executer_flux(
            commande, message, cwd, env, timeout, on_event, on_stderr,
            heartbeat, on_heartbeat, transcript)
    except file_mj.Interrompu as interruption:
        vrai = next((e.get("thread_id") for e in interruption.evenements
                     if e.get("type") == "thread.started"), thread_id)
        if vrai:
            _poser_session_codex(logique, vrai, modele, transcript,
                                 manuel_sha256=manuel_sha256, interrompu=True)
        raise
    rep = _normaliser_codex(evenements, modele, duree, logique, transcript)
    if not rep["result"] and os.path.exists(final):
        rep["result"] = io.open(final, encoding="utf-8",
                                errors="replace").read().strip()
    if code != 0:
        raise RuntimeError(("\n".join(erreurs) or
                            "codex a quitte avec le code %d" % code)[-800:])
    vrai = rep.get("session_id")
    if not vrai:
        raise RuntimeError("Codex n'a rendu aucun thread_id")
    _poser_session_codex(logique, vrai, modele, transcript,
                         manuel_sha256=manuel_sha256)
    if prompt_injecte:
        _retirer_prompt_codex(cwd)
    return rep


def _commande_claude(prompt_systeme, modele, effort, add_dirs, tools,
                      settings, sid, reprendre, stream):
    # Meme invariant que Codex : aucune session n'est materiellement privee
    # d'ecriture. Un juge peut avoir pour CONSIGNE de ne rien modifier ; ce
    # n'est pas au runtime de lui casser les mains. L'ordre preserve les
    # outils demandes, puis ajoute seulement ceux qui manquent.
    outils = list(tools or [])
    for outil in ("Read", "Grep", "Glob", "Bash", "Write", "Edit"):
        if outil not in outils:
            outils.append(outil)
    commande = ["claude", "-p"]
    if prompt_systeme:
        commande += ["--system-prompt-file", prompt_systeme]
    for chemin in add_dirs:
        commande += ["--add-dir", chemin]
    commande += ["--dangerously-skip-permissions"]
    commande += ["--tools", ",".join(outils)]
    if "Bash" in outils:
        commande += ["--allowedTools", "Bash(python:*)"]
    commande += ["--output-format", "stream-json" if stream else "json"]
    if stream:
        commande += ["--verbose"]
    if settings:
        commande += ["--settings", settings]
    if modele:
        commande += ["--model", modele]
    if effort:
        commande += ["--effort", effort]
    commande += ["--resume" if reprendre else "--session-id", sid]
    return commande


def _appel_claude(manuel, message, logique, modele, effort, timeout, cwd,
                   add_dirs, tools, settings, reprendre, env, on_event,
                   on_stderr, heartbeat, on_heartbeat):
    stream = bool(on_event or on_stderr or heartbeat)
    entree = _entree_session(logique)
    essais = [reprendre] if reprendre is not None else (
        [True, False] if entree.get("manuel_sha256_claude") else [False, True])
    dernier = u""
    for reprise in essais:
        manuel_sha256, prompt, _ = _preparer_prompt_claude(
            manuel, cwd, reprise, entree)
        commande = _commande_claude(prompt, modele, effort, add_dirs, tools,
                                    settings, logique, reprise, stream)
        try:
            if stream:
                code, lignes, erreurs, evs, _duree = _executer_flux(
                    commande, message, cwd, env, timeout, on_event, on_stderr,
                    heartbeat, on_heartbeat)
                resultat = next((ev for ev in reversed(evs)
                                  if ev.get("type") == "result"), None)
                sortie = "\n".join(lignes)
            else:
                r = subprocess.run(commande, cwd=cwd, env=env,
                                   input=message.encode("utf-8"),
                                   capture_output=True, timeout=timeout,
                                   **_creation_sans_fenetre())
                code = r.returncode
                sortie = r.stdout.decode("utf-8", "replace")
                erreurs = [r.stderr.decode("utf-8", "replace")]
                try:
                    resultat = json.loads(sortie)
                except ValueError:
                    resultat = None
        finally:
            _retirer_prompt_claude(prompt)
        dernier = sortie + "\n" + "\n".join(erreurs)
        if reprendre is None and ("already in use" in dernier or "No conversation found" in dernier):
            continue
        if code != 0:
            raise RuntimeError(("\n".join(erreurs) or
                                sortie or
                                "claude a quitte avec le code %d" % code)[-800:])
        if not resultat:
            raise RuntimeError("le flux Claude s'est ferme sans resultat")
        resultat.setdefault("provider", "claude")
        resultat.setdefault("logical_session_id", logique)
        resultat.setdefault("session_id", logique)
        resultat.setdefault("model", modele or "defaut")
        _poser_empreinte_manuel(logique, "claude", manuel_sha256)
        return resultat
    raise RuntimeError("ni creation ni reprise Claude n'ont abouti : %s" %
                       dernier[-400:])


def appeler(role, manuel, message, session_id, modele=None, effort=None,
            timeout=180, cwd=None, add_dirs=None, tools=None, reprendre=None,
            settings=None, env=None, on_event=None, on_stderr=None,
            heartbeat=None, on_heartbeat=None, compte_pour=None,
            work_identity=None):
    """Appelle le fournisseur global et rend le contrat de reponse commun."""
    provider = fournisseur()
    modele = _modele(provider, modele)
    effort = _effort(provider, effort)
    service_tier = _service_tier(provider)
    cwd = os.path.abspath(cwd or RACINE)
    os.makedirs(cwd, exist_ok=True)
    add_dirs = [os.path.abspath(x) for x in (add_dirs or [])]
    environnement = dict(os.environ)
    environnement.update(env or {})
    environnement["LE_CONSEIL_QUI"] = str(role)
    # habitant.md §4 : les sessions sont de la memoire, pas une section
    # critique. Deux reprises du meme id peuvent vivre en parallele ; leur
    # entrelacement est le registre d'audiences du MJ. Seules les portes de
    # l'etat serialisent ce qui devient vrai.
    with _activite(role, session_id, environnement):
        debut_compute = time.time()
        succes, erreur_compute = False, None
        resultat = None
        try:
            if provider == "codex":
                resultat = _appel_codex(
                    manuel, message, session_id, modele, effort, timeout, cwd,
                    add_dirs, reprendre, environnement, on_event, on_stderr,
                    heartbeat, on_heartbeat, service_tier=service_tier,
                    recherche_web=bool(tools and "WebSearch" in tools))
            elif provider == "gemini":
                from agents import runtime_gemini
                resultat = runtime_gemini.appeler(
                    manuel, message, session_id, modele, effort, timeout, cwd,
                    add_dirs, tools, settings, reprendre, environnement)
            else:
                resultat = _appel_claude(
                    manuel, message, session_id, modele, effort, timeout, cwd,
                    add_dirs, tools, settings, reprendre, environnement,
                    on_event, on_stderr, heartbeat, on_heartbeat)
            succes = True
            return resultat
        except BaseException as e:
            erreur_compute = "%s: %s" % (type(e).__name__, str(e))
            raise
        finally:
            # Cette porte est plus basse que CALL/CAST : elle voit aussi les
            # expirations et les erreurs qui ne produiront jamais de rapport.
            try:
                from agents import compute
                evenement_compute = compute.enregistrer(
                    role, compte_pour, session_id, provider, debut_compute,
                    time.time(), succes, erreur_compute,
                    work_identity=work_identity, resultat=resultat)
                if work_identity and not succes:
                    from agents import work_identity as registre_travail
                    registre_travail.terminer_attempt(
                        work_identity, evenement_compute["id"], "failed",
                        term=False)
                if work_identity and succes:
                    resultat.setdefault("continuous_work_identity", {
                        cle: evenement_compute[cle] for cle in (
                            "work_id", "attempt_id", "attempt_number",
                            "effect_key")})
                    resultat.setdefault("compute_event_id",
                                        evenement_compute["id"])
            except Exception:
                pass  # la mesure ne doit jamais tuer le travail mesure
            # Un agent dispose du dépôt et peut écrire un livre directement,
            # sans passer par bibliotheque.Session. À la fin de CHAQUE call —
            # succès, erreur ou expiration — on compare donc le disque à
            # l'empreinte. `constate` reste honnête : une écriture concurrente
            # peut être prise dans la même passe, on n'invente pas son auteur.
            try:
                from agents import reconcilier
                reconcilier.passer(True, outil="runtime:%s" % provider)
            except Exception:
                pass  # l'histoire ne doit jamais tuer la journée d'un homme


def lancer_cast(log, trace=None, **appel):
    """Lance la meme porte en detache ; le worker sait creer OU reprendre."""
    # Le slot est pris AVANT le worker : au seizième wake-up, l'appelant attend
    # au lieu de créer une grappe de processus détachés eux-mêmes en attente.
    reservation = _attendre_slot(
        appel.get("role"), appel.get("session_id"), pid=None)
    os.makedirs(REQUETES, exist_ok=True)
    requete = os.path.join(REQUETES, "%s.json" % uuid.uuid4().hex)
    provider = fournisseur()
    try:
        environnement = dict(os.environ)
        environnement[RESERVATION_ENV] = os.path.basename(reservation)
        # L'environnement voyage DANS la requete : un worker lance hors de
        # l'arbre du lanceur (agents/detache.py) n'en herite pas.
        _ecrire_json(requete, {"appel": appel, "trace": trace,
                               "fournisseur": provider,
                               "environnement": environnement})
        worker = os.path.join(RACINE, "scripts", "agents", "runtime_worker.py")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        from agents.detache import lancer_hors_arbre
        lancer_hors_arbre([sys.executable, worker, requete, log], RACINE,
                          log, environnement)
    except BaseException:
        _liberer_slot(reservation)
        try:
            os.remove(requete)
        except OSError:
            pass
        raise
    return {"cast": True, "log": log, "session": appel["session_id"],
            "provider": provider}
