# -*- coding: utf-8 -*-
"""JOUEUR PNJ — un modele tient un siege comme un humain au clavier, dans n'importe quel monde.

    python scripts/joueur_pnj.py --monde vampire-counts --qui teodor --tours 10
    python scripts/joueur_pnj.py --qui rhaenyra --tours 5          # partie racine (etat/)
    python scripts/joueur_pnj.py --monde charmed --qui phoebe --voir   # montre le prompt, n'envoie rien

Il ne lit le monde que par le serveur, avec le jeton du siege : GET /scene
(le fil filtre pour lui) et GET /entites (les noms). Il n'ouvre aucun fichier
d'etat hors joueurs.json (pour le jeton) — le brouillard est celui du joueur.
Il repond par POST /action, exactement comme la page.

Le modele joue SANS OUTILS : un fil entre, une action sort, en JSON.

Ce qu'il faut au siege — UN fichier, sa tete : <monde>/chambres/<qui>/joueur.md
(modele : mondes/vampire-counts/chambres/teodor/joueur.md). Elle peut porter :
  - un en-tete `---\\nconnus: a, b, c\\n---` : les gens qu'il connait de sa vie
    (sinon : le champ `pnj` de son siege). Les autres n'entrent dans sa liste
    que quand le fil les lui a montres — /entites sert tout le monde ;
  - `{INCLURE:prompts/pnj.md#Titre de debut..Titre de fin}` : recopie la section
    d'un fichier du monde, du titre de debut (inclus) au titre de fin (exclu) ;
    `{INCLURE:chambres/x/ma-memoire/....txt}` : recopie le fichier entier.
La tete ne porte que le personnage : la maniere de jouer — le grain (des
affaires, pas des gestes), les regles, le JSON rendu — est commune et lui est
ajoutee depuis scripts/agents/prompts/joueur-pnj.md.

Le port vient de .claude/launch.json (la configuration qui sert ce monde),
sinon --port. Un seul joueur PNJ par siege a la fois (verrou). Le journal de
chaque decision, et de chaque echec, va dans <monde>/chambres/<qui>/joueur-pnj.md.
"""
import argparse
import io
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERROUS = os.path.join(RACINE, ".agents-runtime", "joueur-pnj")
# Commun a tous les sieges de tous les mondes : le grain (des affaires, pas des
# gestes), les regles du joueur, le format rendu. La tete ne porte que le personnage.
COMMUN = os.path.join(RACINE, "scripts", "agents", "prompts", "joueur-pnj.md")
# Redit a chaque tour, au plus pres de la decision : le fil du meneur est une
# prose tres physique, et un modele rapide l'imite si on ne le lui redit pas.
RAPPEL = ("\n\nNiveau STRATÉGIQUE : une décision, un ordre, une question qui tranche, "
          "une lettre, un homme qu'on envoie. Aucun geste, aucun trajet, aucune "
          "manipulation d'objet, aucune contenance — le meneur s'en charge. "
          "En « dire », `texte` ne contient QUE les mots prononcés.")

SCHEMA = {"type": "object", "additionalProperties": False,
          "required": ["pourquoi", "mode", "texte", "a_qui"],
          "properties": {"pourquoi": {"type": "string"},
                         "mode": {"type": "string", "enum": ["dire", "agir"]},
                         "texte": {"type": "string"},
                         "a_qui": {"type": "string"}}}

# Ce qui ne vaut pas reponse du monde : ses propres lignes, et le battement
# du MJ (statut), qui dit seulement que le monde travaille encore.
DE_LUI = {"vous", "reecrit", "statut"}


def d_un_autre_siege(item, qui):
    """La ligne `vous` d'un AUTRE joueur debout dans la meme piece : pour ce
    siege-ci, c'est une replique comme une autre, pas sa propre parole."""
    j = item.get("joueur_id")
    return item.get("type") == "vous" and bool(qui) and bool(j) and j != qui


def de_lui(item, qui=None):
    return item.get("type") == "vous" and not d_un_autre_siege(item, qui)


def reponse_du_monde(item, qui=None):
    # Un avis du commentateur ne résout pas une action et ne débloque pas un tour.
    if d_un_autre_siege(item, qui):
        return True
    return item.get("type") not in DE_LUI and item.get("qui") != "sport-critic"



# ---------------------------------------------------------------- le monde

def base_monde(monde):
    return os.path.join(RACINE, "mondes", monde) if monde else RACINE


def port_monde(monde):
    """La configuration de launch.json qui sert ce monde ; « jeu » pour la racine."""
    try:
        confs = json.load(io.open(os.path.join(RACINE, ".claude", "launch.json"), encoding="utf-8"))["configurations"]
    except (OSError, ValueError, KeyError):
        return None
    for c in confs:
        args = c.get("runtimeArgs") or []
        if monde:
            if "--monde" in args and args[args.index("--monde") + 1:][:1] == [monde]:
                return c.get("port")
        elif c.get("name") == "jeu":
            return c.get("port")
    return None


def siege(base, qui, virtuel=False):
    for j in json.load(io.open(os.path.join(base, "etat", "joueurs.json"), encoding="utf-8")):
        if j.get("personnage_id") == qui:
            return j
    if virtuel:
        with io.open(os.path.join(base, "etat", "personnages.json"), encoding="utf-8") as f:
            if any(p.get("id") == qui for p in json.load(f)):
                return {"personnage_id": qui, "jeton": "homme:" + qui, "pnj": []}
    raise SystemExit("aucun siege « %s » dans %s" % (qui, os.path.join(base, "etat", "joueurs.json")))


def tete(base, qui, journee=False):
    """(texte systeme, connus declares ou None)."""
    chemin = os.path.join(base, "chambres", qui, "joueur.md")
    if not os.path.exists(chemin):
        raise SystemExit("pas de tete de joueur : %s\n(modele : mondes/vampire-counts/chambres/teodor/joueur.md)" % chemin)
    with io.open(chemin, encoding="utf-8") as fichier:
        s = fichier.read()
    connus = None
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", s, re.DOTALL)
    if m:
        s = s[m.end():]
        for ligne in m.group(1).splitlines():
            if ligne.strip().startswith("connus:"):
                connus = {x.strip() for x in ligne.split(":", 1)[1].split(",") if x.strip()}

    def inclure(mm):
        fichier, debut, fin = mm.group(1), mm.group(2).strip(), mm.group(3).strip()
        t = io.open(os.path.join(base, fichier), encoding="utf-8").read()
        lignes = t.splitlines()
        titre = lambda l, x: l.lstrip("#").strip().startswith(x) and l.startswith("#")
        i = next(k for k, l in enumerate(lignes) if titre(l, debut))
        niveau = len(lignes[i]) - len(lignes[i].lstrip("#"))
        j = next((k for k, l in enumerate(lignes[i + 1:], i + 1) if titre(l, fin)), len(lignes))
        # on descend la section d'un niveau : elle s'insere sous un titre de la tete
        return "\n".join(("#" + l) if l.startswith("#" * niveau) else l for l in lignes[i:j]).strip()

    s = re.sub(r"\{INCLURE:([^#}]+)#([^.}]+)\.\.([^}]+)\}", inclure, s)
    # {INCLURE:chemin} sans titres : le fichier entier (une memoire, une maniere)
    s = re.sub(r"\{INCLURE:([^#}]+)\}",
               lambda mm: io.open(os.path.join(base, mm.group(1).strip()), encoding="utf-8").read().strip(), s)
    prompt = os.path.join(os.path.dirname(COMMUN), "joueur-pnj-journee.md") if journee else COMMUN
    with io.open(prompt, encoding="utf-8") as fichier:
        return s + "\n\n" + fichier.read(), connus


# ---------------------------------------------------------------- le serveur

def get(base, chemin, essais=24):
    """Tolere un serveur qui redemarre : jusqu'a deux minutes de reprises."""
    for k in range(essais):
        try:
            with urllib.request.urlopen(base + chemin, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except OSError:
            if k == essais - 1:
                raise
            time.sleep(5)


def post(base, chemin, corps):
    req = urllib.request.Request(base + chemin, data=json.dumps(corps).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def noms(base, jeton):
    e = get(base, "/entites?jeton=" + jeton).get("entites", [])
    return {x["id"]: (x.get("noms") or [x["id"]])[0] for x in e if x.get("type") == "personnage"}


def vus_dans(items):
    v = set()
    for it in items:
        for k in ("locuteur_id", "acteur_id"):
            if it.get(k):
                v.add(it[k])
        for p in (it.get("presents") or []) + (it.get("entrent") or []):
            v.add(p if isinstance(p, str) else p.get("id"))
    return v


def rendre(items, nom, qui=None):
    """Le fil en texte lisible, tel qu'un joueur le lit a l'ecran."""
    out = []
    for it in items:
        t = it.get("type")
        quand = it.get("moment") or it.get("heure") or ""
        if t == "effacer":
            out.append("\n— nouvelle scène —")
        elif t == "salle":
            pres = ", ".join(nom.get(p if isinstance(p, str) else p.get("id"), str(p)) for p in it.get("presents") or [])
            out.append("[Lieu : %s%s. Présents : %s]" % (it.get("lieu", "?"), (", " + quand) if quand else "", pres))
        elif t == "recit":
            out.append(it.get("texte", ""))
        elif t == "pensee":
            out.append("(Vos pensées) " + it.get("texte", ""))
        elif t == "replique":
            l = it.get("locuteur_id")
            out.append("%s [%s] : « %s »" % (nom.get(l, l), l, it.get("texte", "")))
            if it.get("demande"):
                out.append("   (il vous demande : %s)" % it["demande"].get("quoi", ""))
        elif t == "geste":
            a = it.get("acteur_id")
            out.append("%s [%s] — %s" % (nom.get(a, a), a, it.get("texte", "")))
        elif t == "vous" and d_un_autre_siege(it, qui):
            j = it["joueur_id"]
            if it.get("mode") in ("dire", "parler"):
                out.append("%s [%s] : « %s »" % (nom.get(j, j), j, it.get("texte", "")))
            else:
                out.append("%s [%s] — %s" % (nom.get(j, j), j, it.get("texte", "")))
        elif t == "vous":
            verbe = "Vous dites" if it.get("mode") in ("dire", "parler") else "Vous faites"
            out.append("%s : %s" % (verbe, it.get("texte", "")))
        elif t in ("breve", "evenement", "ecrit", "marque"):
            out.append("[%s] %s" % (t, it.get("texte") or it.get("titre") or ""))
        elif t == "objectif" and it.get("action") == "ajouter":
            out.append("[Dessein : %s — %s]" % (it.get("titre", ""), it.get("description", "")))
        elif t == "suites":
            out.append("[Ce qui s'offre : %s]" % " / ".join(o.get("texte", str(o)) if isinstance(o, dict) else str(o) for o in it.get("options") or []))
        elif t == "reponse":
            out.append("[réponse hors fiction] " + it.get("texte", ""))
        for e in it.get("entrent") or []:
            out.append("(%s entre)" % (e.get("nom") if isinstance(e, dict) else e))
        for s_ in it.get("sortent") or []:
            out.append("(%s sort)" % nom.get(s_, s_))
    return "\n".join(x for x in out if x)


def attendre_reponse(base, jeton, depuis, calme, maxi, boite=None, qui=None):
    """Attend un item nouveau qui n'est pas de lui, puis `calme` s de silence.

    /scene ne sert qu'une FENETRE des derniers items (80) : un indice compte
    depuis le debut ne bouge plus une fois le fil plein, et le joueur
    attendait pour toujours une reponse deja arrivee. On repere donc la
    reponse APRES SA DERNIERE ACTION (`vous`), et le mouvement par la
    signature de la fenetre, pas par sa longueur. `depuis` ne sert plus
    qu'au tout premier tour, quand il n'a encore rien joue."""
    t0 = time.time()
    vu_reponse, derniere_sig, derniere_bouge = False, None, time.time()
    while time.time() - t0 < maxi:
        items = get(base, "/scene?jeton=" + jeton).get("items", [])
        sig = (len(items), json.dumps(items[-1], sort_keys=True) if items else "")
        if sig != derniere_sig:
            derniere_sig, derniere_bouge = sig, time.time()
        siens = [k for k, i in enumerate(items) if de_lui(i, qui)]
        apres = items[siens[-1] + 1:] if siens else items[depuis:]
        if any(reponse_du_monde(i, qui) for i in apres):
            vu_reponse = True
        if vu_reponse and time.time() - derniere_bouge >= calme:
            return items
        if boite and os.path.exists(boite) and os.path.getsize(boite):
            return items  # interrompu (scripts/interrompre.py) : on joue tout de suite
        time.sleep(5)
    return None


# ---------------------------------------------------------------- le modele

def valider(a):
    if a.get("mode") not in ("dire", "agir") or not (a.get("texte") or "").strip():
        raise RuntimeError("action invalide : " + json.dumps(a, ensure_ascii=False)[:400])
    a.setdefault("a_qui", "")
    a.setdefault("pourquoi", "")
    return a


def appeler_claude(sys_txt, msg, modele, timeout=300):
    vide = tempfile.mkdtemp(prefix="joueur-pnj-")
    f = os.path.join(vide, "systeme.md")
    io.open(f, "w", encoding="utf-8").write(sys_txt)
    cmd = ["claude", "-p", "--tools", "", "--no-session-persistence", "--output-format", "json",
           "--json-schema", json.dumps(SCHEMA), "--system-prompt-file", f, "--model", modele]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    kw = {"creationflags": 0x08000000} if os.name == "nt" else {}
    r = subprocess.run(cmd, input=msg.encode("utf-8"), capture_output=True, timeout=timeout, cwd=vide, env=env, **kw)
    sortie = r.stdout.decode("utf-8", "replace")
    try:
        res = json.loads(sortie)
    except ValueError:
        raise RuntimeError("reponse illisible (code %d) : %s %s" % (r.returncode, sortie[:300], r.stderr.decode("utf-8", "replace")[-300:]))
    if res.get("is_error"):
        raise RuntimeError("claude : %s" % res.get("result"))
    a = res.get("structured_output")
    if a is None:
        a = json.loads(res.get("result") or "{}")
    return valider(a), "claude/%s" % modele


def appeler_moteur(qui, sys_txt, msg, timeout=300, recherche=False, preuve_dir=None):
    """Par le fournisseur du moteur (.agents-runtime/config.json), dans un dossier
    vide et neuf a chaque tour : aucun acces au depot, aucune memoire de session."""
    for p in (os.path.join(RACINE, "scripts"), os.path.join(RACINE, "scripts", "noyau")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import agents.expose  # noqa: F401 — la facade d'abord (import circulaire sinon)
    from agents import runtime
    vide = tempfile.mkdtemp(prefix="joueur-pnj-")
    consigne = ("\n\nREPONDS UNIQUEMENT par un objet JSON sur une ligne, sans texte autour, "
                "avec les cles pourquoi, mode (dire|agir), texte, a_qui. "
                "N'ouvre aucun fichier : tout ce que tu sais est ici.")
    if recherche:
        consigne = ("\n\nRecherche sur le Web autorisée et nécessaire avant toute assertion nouvelle. "
                    "Utilise la recherche et ouvre les sources primaires. Ne lis pas l'état privé du jeu. "
                    "Distingue ce qui a réellement été consulté, les résumés et les textes inaccessibles. "
                    "Inclus dans texte les URL/DOI, résultats précis et limites utiles à ton coup. "
                    "Une recherche infructueuse reste une incertitude. Ne fabrique aucune citation. "
                    "Dans le JSON final ajoute recherche : {question, requetes:[...], sources:[{url, acces, passage, resultat, limite}], limites_recherche}. "
                    "Ces champs déclarent tes recherches ; ils ne prouvent pas une consultation. "
                    "Si aucun outil de recherche n'est accessible, dis-le : n'utilise pas ta mémoire comme lecture. "
                    "Dans texte résume la recherche et cite les pièces pertinentes pour que le MJ puisse contrôler. "
                    "Après tes recherches, rends UNIQUEMENT un JSON final avec pourquoi, mode, texte, a_qui, recherche.")
    res = runtime.appeler("%s-joueur" % qui, sys_txt, msg + consigne, str(uuid.uuid4()),
                          timeout=600 if recherche else timeout, cwd=vide, reprendre=False,
                          tools=["WebSearch", "WebFetch"] if recherche else None)
    if recherche and preuve_dir:
        os.makedirs(preuve_dir, exist_ok=True)
        with io.open(os.path.join(preuve_dir, "%s.json" % uuid.uuid4().hex), "w", encoding="utf-8") as f:
            json.dump({"transcript_path": res.get("transcript_path"), "research_log_path": res.get("research_log_path"), "gestes": res.get("gestes"),
                       "result": res.get("result"), "provider": res.get("provider"), "model": res.get("model")}, f, ensure_ascii=False, indent=2)
    brut = res.get("result") or ""
    m = re.search(r"\{.*\}", brut, re.DOTALL)
    if not m:
        raise RuntimeError("pas de JSON dans la reponse : " + brut[:400])
    return valider(json.loads(m.group(0))), "%s/%s" % (res.get("provider"), res.get("model"))


# ---------------------------------------------------------------- le verrou

def vivant(pid):
    if os.name == "nt":
        import ctypes
        h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
        ctypes.windll.kernel32.CloseHandle(h)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def lire_boite(boite):
    """Les messages deposes par scripts/interrompre.py, consommes une fois."""
    if not os.path.exists(boite):
        return []
    tmp = boite + ".%d.lu" % os.getpid()
    try:
        os.replace(boite, tmp)
    except OSError:
        return []
    msgs = []
    for ligne in io.open(tmp, encoding="utf-8"):
        try:
            msgs.append(json.loads(ligne))
        except ValueError:
            pass
    os.remove(tmp)
    return msgs


def prendre_verrou(monde, qui):
    """Deux joueurs PNJ sur le meme siege feraient parler le personnage deux fois."""
    os.makedirs(VERROUS, exist_ok=True)
    f = os.path.join(VERROUS, "%s--%s.lock" % (monde or "racine", qui))
    try:
        pid = int(io.open(f, encoding="utf-8").read().strip() or 0)
    except (OSError, ValueError):
        pid = 0
    if pid and pid != os.getpid() and vivant(pid):
        raise SystemExit("un joueur PNJ tient deja %s (pid %d). Arrete-le d'abord." % (qui, pid))
    io.open(f, "w", encoding="utf-8").write(str(os.getpid()))
    return f


# ---------------------------------------------------------------- la partie

def rappel_journee(tour, total):
    texte = "\n\nJOURNÉE HORS SCÈNE — message %d/%d. Privilégie mode=agir. " % (tour, total)
    texte += ("Expose tes actions et priorités pour le reste de cette journée, avec tes replis conditionnels. "
              if tour == 1 else "Réagis au résultat reçu et ajuste le reste de la même journée ; ne recommence pas le programme. ")
    texte += ("Dernier message disponible : regroupe la suite, sans inventer les résultats."
              if tour == total else "Le second message ajustera après le retour du MJ.")
    return texte


def main():
    ap = argparse.ArgumentParser(description="Un modele joue un siege comme un humain au clavier.")
    ap.add_argument("--monde", default="", help="id sous mondes/ ; vide = la partie racine")
    ap.add_argument("--qui", help="personnage_id du siege (defaut : depart.siege du manifeste)")
    ap.add_argument("--tours", type=int, default=None)
    ap.add_argument("--journee", action="store_true", help="une journée hors scène, en 1 ou 2 messages, priorité à agir")
    ap.add_argument("--messages", type=int, choices=(1, 2), default=None, help="budget du mode --journee (défaut : 2)")
    ap.add_argument("--fournisseur", choices=["moteur", "claude"], default="moteur",
                    help="moteur = celui de .agents-runtime/config.json ; claude = claude -p")
    ap.add_argument("--modele", default="sonnet", help="pour --fournisseur claude")
    ap.add_argument("--port", type=int, help="defaut : lu dans .claude/launch.json")
    ap.add_argument("--calme", type=int, default=10, help="secondes de silence avant de jouer")
    ap.add_argument("--attente-max", type=int, default=1200, help="secondes max d'attente d'une reponse")
    ap.add_argument("--voir", action="store_true", help="un tour : montre le prompt, n'envoie rien")
    ap.add_argument("--recherche", action="store_true", help="Recherche Web pour les ateliers scientifiques et monétaires autorisés")
    a = ap.parse_args()
    if a.messages is not None and not a.journee:
        ap.error("--messages exige --journee")
    if a.journee and a.tours is not None:
        ap.error("--journee utilise --messages 1 ou 2, pas --tours")
    a.tours = (a.messages or 2) if a.journee else (10 if a.tours is None else a.tours)
    if a.tours < 1:
        ap.error("--tours doit être positif")
    if a.recherche and (a.monde not in {"frontieres-du-vivant", "argent-intelligent"} or a.fournisseur != "moteur"):
        ap.error("--recherche exige un monde autorisé (frontieres-du-vivant, argent-intelligent) et --fournisseur moteur")

    base_m = base_monde(a.monde)
    if not os.path.isdir(base_m):
        raise SystemExit("monde introuvable : %s" % base_m)
    qui = a.qui
    if not qui:
        try:
            qui = json.load(io.open(os.path.join(base_m, "manifeste.json"), encoding="utf-8"))["depart"]["siege"]
        except (OSError, ValueError, KeyError):
            raise SystemExit("precise --qui (pas de depart.siege dans le manifeste)")
    port = a.port or port_monde(a.monde)
    if not port:
        raise SystemExit("port inconnu pour ce monde : passe --port")
    base = "http://localhost:%d" % port
    s = siege(base_m, qui, virtuel=a.journee)
    jeton = s["jeton"]
    try:  # serveur eteint : on le dit tout de suite, pas apres deux minutes de reprises
        get(base, "/scene?jeton=" + jeton, essais=1)
    except OSError:
        raise SystemExit("le serveur ne repond pas sur %s — lance-le d'abord" % base)
    sys_txt, connus_tete = tete(base_m, qui, journee=a.journee)
    connus_vie = (connus_tete if connus_tete is not None else set(s.get("pnj") or [])) | {qui}
    journal_f = os.path.join(base_m, "chambres", qui, "joueur-pnj.md")

    def journal(texte):
        with io.open(journal_f, "a", encoding="utf-8") as f:
            f.write(texte + "\n")

    if not a.voir:
        verrou = prendre_verrou(a.monde, qui)
        qui_joue = "claude/" + a.modele if a.fournisseur == "claude" else "moteur"
        journal("\n# Partie du joueur PNJ — %s — %d tours, %s\n" % (time.strftime("%Y-%m-%d %H:%M"), a.tours, qui_joue))
    boite = os.path.join(VERROUS, "%s--%s.interruptions.jsonl" % (a.monde or "racine", qui))
    try:
        depuis = 0
        items = get(base, "/scene?jeton=" + jeton).get("items", [])
        # A LA REPRISE : si la derniere chose du fil est une action du siege, le
        # monde ne lui a pas encore repondu — on attend avant de rejouer.
        attente_initiale = False
        derniers_vous = [k for k, i in enumerate(items) if de_lui(i, qui)]
        if derniers_vous and not any(reponse_du_monde(i, qui) for i in items[derniers_vous[-1] + 1:]):
            attente_initiale = True
            depuis = derniers_vous[-1] + 1
            items = []
        for tour in range(1, a.tours + 1):
            if tour > 1 or attente_initiale or (not items and not a.journee):
                items = attendre_reponse(base, jeton, depuis, a.calme, a.attente_max,
                                         None if a.voir else boite, qui)
                if items is None:
                    journal("\n**Tour %d : le monde n'a pas répondu en %d s. Arrêt.**" % (tour, a.attente_max))
                    print("pas de reponse, arret", flush=True)
                    return 1
            recus = [] if a.voir else lire_boite(boite)
            interruption = "".join(
                "\n\nMESSAGE HORS FICTION, de %s, pour toi qui joues %s — personne dans le "
                "monde ne l'a entendu ; tiens-en compte dès cette action :\n« %s »"
                % (m.get("de", "la direction de jeu"), qui, m.get("texte", "")) for m in recus)
            for m in recus:
                journal("\n> **Interruption** (%s) : %s" % (m.get("de", ""), m.get("texte", "")))
            nom = noms(base, jeton)
            connus = (connus_vie | vus_dans(items)) & set(nom)
            gens = ", ".join("%s (%s)" % (nom[k], k) for k in sorted(connus) if k != qui)
            msg = ("Voici le fil de la partie jusqu'à maintenant, tel que %s le vit :\n\n" % nom.get(qui, qui)
                   + rendre(items[-80:], nom, qui)
                   + "\n\nGens dont tu connais le nom (id entre parenthèses) : " + gens
                   + interruption
                   + "\n\nC'est à toi. Tour %d sur %d. Une action de %s." % (tour, a.tours, nom.get(qui, qui))
                   + (rappel_journee(tour, a.tours) if a.journee else RAPPEL))
            if a.voir:
                print(sys_txt if a.journee else sys_txt[:1500], "\n...\n", msg[-3000:])
                return 0
            # UN 429 N'EST PAS UNE PANNE. Neuf sieges lances ensemble ont
            # saute le debit du fournisseur, et sept sont morts au premier tour
            # sur une limite qui serait retombee en une minute. On attend et
            # on reprend, en decale ; toute autre erreur arrete comme avant.
            for essai in range(6):
                try:
                    if a.fournisseur == "claude":
                        action, modele = appeler_claude(sys_txt, msg, a.modele)
                    else:
                        action, modele = appeler_moteur(qui, sys_txt, msg, recherche=a.recherche,
                                                         preuve_dir=os.path.join(base_m, "chambres", qui, "recherches"))
                    break
                except Exception as e:  # noqa: BLE001 — tout echec du modele se consigne
                    debit = "429" in str(e) or "Too Many Requests" in str(e)
                    if not debit or essai == 5:
                        journal("\n**Tour %d : échec du modèle — %s. Arrêt.**" % (tour, str(e)[:500]))
                        print("echec du modele : %s" % e, flush=True)
                        return 1
                    pause = 30 * (essai + 1) + random.randint(0, 20)
                    print("debit depasse, reprise dans %d s" % pause, flush=True)
                    time.sleep(pause)
            corps = {"type": "libre", "mode": action["mode"], "texte": action["texte"].strip()}
            if a.journee:
                corps["pilote_mode"] = "pnjpj-journee"
            if action["mode"] == "dire" and action.get("a_qui") in connus:
                corps["destinataire_id"] = action["a_qui"]
            depuis = len(items)
            rep = post(base, "/action?jeton=" + jeton, corps)
            journal("\n## Tour %d\n\n- **%s** : %s%s\n- *pourquoi* : %s\n- ref `%s` · %s"
                    % (tour, action["mode"], corps["texte"],
                       (" → `%s`" % corps["destinataire_id"]) if "destinataire_id" in corps else "",
                       action.get("pourquoi", ""), rep.get("ref"), modele))
            print("tour %d : %s — %s" % (tour, action["mode"], corps["texte"]), flush=True)
        retour_final = attendre_reponse(base, jeton, depuis, a.calme, a.attente_max, qui=qui)
        if a.journee and retour_final is None:
            journal("\n**Budget envoyé ; arbitrage final non reçu. Journée non confirmée.**")
            print("arbitrage final non reçu, journée non confirmée", flush=True)
            return 1
        journal("\n**Fin des %d tours.**" % a.tours)
        print("fin", flush=True)
        return 0
    except Exception as e:  # noqa: BLE001
        if not a.voir:
            journal("\n**Arrêt sur erreur — %s**" % str(e)[:500])
        raise
    finally:
        if not a.voir:
            try:
                os.remove(verrou)
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
