# -*- coding: utf-8 -*-
"""GUICHET MJ — le mode « session-claude-guetteur ».

Au lieu de lancer ``claude -p`` ou ``codex exec`` à chaque réveil, le MJ peut
être une session Claude VIVANTE (desktop, terminal interactif) qui guette un
guichet de fichiers. Le lanceur (``mj._appeler_mj``) dépose le message du
réveil et ATTEND le rendu ; tout le reste de la chaîne — file_mj, contrôles de
réplique et de Jump, retrait de l'inbox après poussée constatée — est
inchangé. Seul le MJ passe par là : les hommes dépêchés gardent leur
fournisseur (``scripts/fournisseur.py``).

    python scripts/fournisseur.py --mj session-claude-guetteur   # armer
    python scripts/fournisseur.py --mj defaut                    # désarmer

Côté session MJ :

    python scripts/guichet_mj.py --guetter          # une ligne par billet (Monitor)
    python scripts/guichet_mj.py --lire <id>        # le billet entier + l'env
    python scripts/guichet_mj.py --rendre <id> "ce que j'ai fait"
    python scripts/guichet_mj.py --etat             # billets en souffrance

Le guichet vit sous ``.agents-runtime/mj/guichet/`` du monde joué.
"""
import hashlib
import io
import json
import os
import sys
import time
import uuid

from agents import runtime

MODE = "session-claude-guetteur"
ALIAS = {"session-claude-guetteur": MODE, "session": MODE, "guetteur": MODE,
         "defaut": None, "aucun": None, "": None}
ATTENTE_POLL = 0.5


def mode_mj():
    """Le mode du MJ : env ``LE_CONSEIL_MJ_FOURNISSEUR`` puis config."""
    brut = os.environ.get("LE_CONSEIL_MJ_FOURNISSEUR")
    if brut is None:
        brut = runtime._lire_json(runtime.CONFIG, {}).get("fournisseur_mj") or ""
    cle = str(brut).casefold()
    if cle not in ALIAS:
        raise RuntimeError("mode MJ inconnu : %s" % brut)
    return ALIAS[cle]


def choisir_mode(nom):
    cle = str(nom or "").casefold()
    if cle not in ALIAS:
        raise ValueError("choisir session-claude-guetteur ou defaut")
    d = runtime._lire_json(runtime.CONFIG, {})
    if ALIAS[cle]:
        d["fournisseur_mj"] = ALIAS[cle]
    else:
        d.pop("fournisseur_mj", None)
    runtime._ecrire_json(runtime.CONFIG, d)
    return ALIAS[cle]


def dossier(monde=None):
    if monde is None:
        import racines
        monde = os.path.dirname(racines.etat())
    return os.path.join(monde, ".agents-runtime", "mj", "guichet")


def _chemin(d, ident, suffixe=".json"):
    return os.path.join(d, ident + suffixe)


def _taille(chemin):
    try:
        return os.path.getsize(chemin)
    except OSError:
        return 0


def en_souffrance(d):
    if not os.path.isdir(d):
        return []
    noms = sorted(n for n in os.listdir(d)
                  if n.endswith(".json") and not n.endswith(".rendu.json")
                  and n[0].isdigit())
    return [n[:-5] for n in noms
            if not os.path.exists(_chemin(d, n[:-5], ".rendu.json"))]


def guetteur_vivant(d):
    v = runtime._lire_json(os.path.join(d, "vivant.json"), {})
    return bool(v) and time.time() - float(v.get("a") or 0) < 30


def appeler(manuel, message, session_id, env, flux, timeout=None, monde=None):
    """Dépose un billet et attend le rendu de la session. Rend le contrat
    ``{result, gestes, provider, ...}`` des autres fournisseurs."""
    d = dossier(monde)
    os.makedirs(d, exist_ok=True)
    empreinte = hashlib.sha256(manuel.encode("utf-8")).hexdigest()
    chemin_manuel = os.path.join(d, "manuel.md")
    if runtime._lire_json(os.path.join(d, "manuel.json"), {}).get("sha256") != empreinte:
        with io.open(chemin_manuel, "w", encoding="utf-8", newline="\n") as f:
            f.write(manuel)
        runtime._ecrire_json(os.path.join(d, "manuel.json"), {"sha256": empreinte})
    ident = "%020d-%s" % (time.time_ns(), uuid.uuid4().hex[:8])
    debut_flux = _taille(flux)
    runtime._ecrire_json(_chemin(d, ident), {
        "id": ident, "cree": time.time(), "session": session_id,
        "manuel_sha256": empreinte, "pid": os.getpid(),
        "env": {k: v for k, v in (env or {}).items() if k.startswith(
            ("LE_CONSEIL_", "CONSEIL_"))},
        "message": message,
    })
    if not guetteur_vivant(d):
        sys.stderr.write("(guichet MJ : aucune session ne guette ; le billet "
                         "%s attend)\n" % ident)
    limite = time.time() + timeout if timeout else None
    rendu_chemin = _chemin(d, ident, ".rendu.json")
    try:
        while not os.path.exists(rendu_chemin):
            if limite and time.time() > limite:
                raise TimeoutError("guichet MJ : pas de rendu pour %s" % ident)
            time.sleep(ATTENTE_POLL)
        time.sleep(0.1)  # laisser l'écriture atomique se poser
        rendu = runtime._lire_json(rendu_chemin, {})
    except BaseException:
        # Un lanceur qui meurt retire son billet : la session ne doit pas
        # jouer un tour dont personne n'attend plus le verdict.
        for c in (_chemin(d, ident),):
            try:
                os.remove(c)
            except OSError:
                pass
        raise
    gestes = list(rendu.get("gestes") or [])
    if _taille(flux) > debut_flux and "append_flux.py" not in gestes:
        gestes.append("append_flux.py")  # constaté sur le disque, pas déclaré
    return {"result": rendu.get("result") or "", "gestes": gestes,
            "provider": MODE, "session_id": session_id,
            "logical_session_id": session_id, "billet": ident}


# --- côté session -----------------------------------------------------------

def _resume(billet):
    env = billet.get("env") or {}
    tete = (billet.get("message") or "").strip().splitlines()[:1]
    return "BILLET %s refs=%s scene=%s | %s" % (
        billet.get("id"), env.get("LE_CONSEIL_REF") or "-",
        env.get("LE_CONSEIL_SCENE") or "-", (tete[0] if tete else "")[:160])


def guetter(d, une_fois=False):
    os.makedirs(d, exist_ok=True)
    vus = set()
    while True:
        runtime._ecrire_json(os.path.join(d, "vivant.json"),
                             {"pid": os.getpid(), "a": time.time()})
        for ident in en_souffrance(d):
            if ident in vus:
                continue
            vus.add(ident)
            billet = runtime._lire_json(_chemin(d, ident), {})
            print(_resume(billet), flush=True)
            if une_fois:
                return
        time.sleep(1)


def lire(d, ident):
    billet = runtime._lire_json(_chemin(d, ident), {})
    if not billet:
        raise SystemExit("billet %s introuvable" % ident)
    lu = runtime._lire_json(os.path.join(d, "manuel.lu.json"), {})
    sortie = []
    if lu.get("sha256") != billet.get("manuel_sha256"):
        sortie.append("MANUEL DU MJ CHANGE (ou jamais lu) — relis : %s\n"
                      % os.path.join(d, "manuel.md"))
        runtime._ecrire_json(os.path.join(d, "manuel.lu.json"),
                             {"sha256": billet.get("manuel_sha256")})
    env = dict(billet.get("env") or {})
    env.setdefault("LE_CONSEIL_QUI", "mj")
    sortie.append("PREFIXE TES COMMANDES (bash) : " + " ".join(
        "%s=%s" % (k, json.dumps(str(v))) for k, v in sorted(env.items())
        if k != "LE_CONSEIL_MJ_TICKET"))
    sortie.append("REND LA MAIN : python scripts/guichet_mj.py --rendre %s "
                  "[--gestes parloir.py,depecher.py] \"<verdict>\"\n" % ident)
    sortie.append(billet.get("message") or "")
    return "\n".join(sortie)


def rendre(d, ident, texte, gestes=None):
    if not os.path.exists(_chemin(d, ident)):
        raise SystemExit("billet %s introuvable (lanceur mort ?)" % ident)
    runtime._ecrire_json(_chemin(d, ident, ".rendu.json"), {
        "result": texte, "gestes": list(gestes or []), "a": time.time()})


def nettoyer(d, age=86400):
    """Retire les paires billet/rendu dont le lanceur a lu le verdict."""
    if not os.path.isdir(d):
        return
    for n in os.listdir(d):
        if n.endswith(".rendu.json"):
            c = os.path.join(d, n)
            if time.time() - os.path.getmtime(c) > age:
                for x in (c, c.replace(".rendu.json", ".json")):
                    try:
                        os.remove(x)
                    except OSError:
                        pass


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--guetter", action="store_true")
    g.add_argument("--lire", metavar="ID")
    g.add_argument("--rendre", metavar="ID")
    g.add_argument("--etat", action="store_true")
    ap.add_argument("--une-fois", action="store_true",
                    help="avec --guetter : sortir au premier billet")
    ap.add_argument("--gestes", default="",
                    help="avec --rendre : scripts lancés (parloir.py,depecher.py)")
    ap.add_argument("texte", nargs="*")
    a = ap.parse_args(argv)
    d = dossier()
    if a.guetter:
        nettoyer(d)
        guetter(d, a.une_fois)
    elif a.lire:
        print(lire(d, a.lire))
    elif a.rendre:
        rendre(d, a.rendre, " ".join(a.texte),
               [x for x in a.gestes.split(",") if x])
        print("rendu %s" % a.rendre)
    else:
        print(json.dumps({"mode_mj": mode_mj(), "guetteur_vivant": guetteur_vivant(d),
                          "en_souffrance": en_souffrance(d)},
                         ensure_ascii=False, indent=2))
