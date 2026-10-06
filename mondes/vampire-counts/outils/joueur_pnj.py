# -*- coding: utf-8 -*-
"""JOUEUR PNJ — un modele tient le siege de Teodor comme un humain au clavier.

    python mondes/vampire-counts/outils/joueur_pnj.py --tours 10
    python mondes/vampire-counts/outils/joueur_pnj.py --voir        # un tour, montre le prompt, n'envoie rien

Il ne lit le monde que par le serveur, avec le jeton du siege : GET /scene
(le fil filtre pour Teodor) et GET /entites (les noms). Il n'ouvre aucun
fichier d'etat — le brouillard est celui du joueur. Il repond par POST /action,
exactement comme la page : le routeur et le MJ automatique font le reste.

Le modele joue SANS OUTILS (comme scripts/partie_ia.py) : un fil entre, une
action sort, en JSON contraint. Sa tete est chambres/teodor/joueur.md, plus le
savoir commun d'un infant tire de prompts/pnj.md.

Un tour : attendre que le monde ait repondu a la derniere action (au moins un
item nouveau qui n'est pas de Teodor) puis qu'il se soit tu `--calme` secondes ;
alors seulement jouer. Le journal de chaque decision va dans
mondes/vampire-counts/joueur-pnj.md.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
MONDE = os.path.dirname(ICI)
TETE = os.path.join(MONDE, "chambres", "teodor", "joueur.md")
PNJ_MD = os.path.join(MONDE, "prompts", "pnj.md")
JOURNAL = os.path.join(MONDE, "joueur-pnj.md")
JOUEURS = os.path.join(MONDE, "etat", "joueurs.json")   # seulement pour le jeton

SCHEMA = {"type": "object", "additionalProperties": False,
          "required": ["pourquoi", "mode", "texte", "a_qui"],
          "properties": {"pourquoi": {"type": "string"},
                         "mode": {"type": "string", "enum": ["dire", "agir"]},
                         "texte": {"type": "string"},
                         "a_qui": {"type": "string"}}}

DE_TEODOR = {"vous", "reecrit"}

# Ceux que Teodor connait par sa vie (joueur.md) ; les autres n'entrent dans sa
# liste que quand le fil les lui a montres. /entites sert TOUT le monde : la
# liste brute fuirait le brouillard.
CONNUS = {"anselm", "stanca", "radu", "sever", "ilka", "konstantin", "radomir",
          "hedwig", "margit", "teodor"}


def vus_dans(items):
    v = set()
    for it in items:
        for k in ("locuteur_id", "acteur_id"):
            if it.get(k):
                v.add(it[k])
        for p in (it.get("presents") or []) + (it.get("entrent") or []):
            v.add(p if isinstance(p, str) else p.get("id"))
    return v


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


def savoir_commun():
    s = io.open(PNJ_MD, encoding="utf-8").read()
    debut = s.index("## Les vérités du monde")
    fin = s.index("## Préparer ton implantation")
    return s[debut:fin].replace("## ", "### ").strip()


def systeme():
    return io.open(TETE, encoding="utf-8").read().replace("{SAVOIR_COMMUN}", savoir_commun())


def noms(base, jeton):
    e = get(base, "/entites?jeton=" + jeton).get("entites", [])
    return {x["id"]: (x.get("noms") or [x["id"]])[0] for x in e if x.get("type") == "personnage"}


def rendre(items, nom):
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


def appeler(sys_txt, msg, modele, timeout=300):
    vide = os.path.join(tempfile.gettempdir(), "joueur-pnj-vide")
    os.makedirs(vide, exist_ok=True)
    f = os.path.join(vide, "systeme-%d.md" % os.getpid())
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
    return a, res.get("total_cost_usd")


def appeler_moteur(sys_txt, msg, timeout=300):
    """Par le fournisseur du moteur (.agents-runtime/config.json), dans un dossier
    vide et neuf a chaque tour : aucun acces au depot, aucune memoire de session."""
    import re
    import uuid
    depot = os.path.dirname(os.path.dirname(MONDE))
    for p in (os.path.join(depot, "scripts"), os.path.join(depot, "scripts", "noyau")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import agents.expose  # noqa: F401 — la facade d'abord (import circulaire sinon)
    from agents import runtime
    vide = tempfile.mkdtemp(prefix="joueur-pnj-")
    consigne = ("\n\nREPONDS UNIQUEMENT par un objet JSON sur une ligne, sans texte autour, "
                "avec les cles pourquoi, mode (dire|agir), texte, a_qui. "
                "N'ouvre aucun fichier : tout ce que tu sais est ici.")
    res = runtime.appeler("teodor-joueur", sys_txt, msg + consigne, str(uuid.uuid4()),
                          timeout=timeout, cwd=vide, reprendre=False)
    brut = res.get("result") or ""
    m = re.search(r"\{.*\}", brut, re.DOTALL)
    if not m:
        raise RuntimeError("pas de JSON dans la reponse : " + brut[:400])
    a = json.loads(m.group(0))
    if a.get("mode") not in ("dire", "agir") or not a.get("texte"):
        raise RuntimeError("action invalide : " + m.group(0)[:400])
    a.setdefault("a_qui", "")
    a.setdefault("pourquoi", "")
    return a, "%s/%s" % (res.get("provider"), res.get("model"))


def journal(texte):
    with io.open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(texte + "\n")


def attendre_reponse(base, jeton, depuis, calme, maxi):
    """Attend un item nouveau qui n'est pas de Teodor, puis `calme` s de silence."""
    t0 = time.time()
    vu_reponse, dernier_total, derniere_bouge = False, None, time.time()
    while time.time() - t0 < maxi:
        items = get(base, "/scene?jeton=" + jeton).get("items", [])
        if dernier_total != len(items):
            dernier_total, derniere_bouge = len(items), time.time()
        if any(i.get("type") not in DE_TEODOR for i in items[depuis:]):
            vu_reponse = True
        if vu_reponse and time.time() - derniere_bouge >= calme:
            return items
        time.sleep(5)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tours", type=int, default=10)
    ap.add_argument("--modele", default="sonnet", help="pour --fournisseur claude")
    ap.add_argument("--fournisseur", choices=["moteur", "claude"], default="moteur",
                    help="moteur = celui de .agents-runtime/config.json (gemini) ; claude = claude -p")
    ap.add_argument("--port", type=int, default=3201)
    ap.add_argument("--calme", type=int, default=75, help="secondes de silence avant de jouer")
    ap.add_argument("--attente-max", type=int, default=1200, help="secondes max d'attente d'une reponse")
    ap.add_argument("--voir", action="store_true")
    a = ap.parse_args()

    base = "http://localhost:%d" % a.port
    jeton = next(j["jeton"] for j in json.load(io.open(JOUEURS, encoding="utf-8")) if j["personnage_id"] == "teodor")
    sys_txt = systeme()
    if not a.voir:
        journal("\n# Partie du joueur PNJ — %s — %d tours, %s\n" % (time.strftime("%Y-%m-%d %H:%M"), a.tours, a.fournisseur if a.fournisseur == "moteur" else a.modele))

    depuis = 0
    items = get(base, "/scene?jeton=" + jeton).get("items", [])
    # A LA REPRISE : si la derniere chose du fil est une action de Teodor, le
    # monde ne lui a pas encore repondu — on attend avant de rejouer.
    derniers_vous = [k for k, i in enumerate(items) if i.get("type") == "vous"]
    if derniers_vous and not any(i.get("type") not in DE_TEODOR for i in items[derniers_vous[-1] + 1:]):
        depuis = derniers_vous[-1] + 1
        items = []
    for tour in range(1, a.tours + 1):
        if tour > 1 or not items:
            items = attendre_reponse(base, jeton, depuis, a.calme, a.attente_max)
            if items is None:
                journal("\n**Tour %d : le monde n'a pas répondu en %d s. Arrêt.**" % (tour, a.attente_max))
                print("pas de reponse, arret", flush=True)
                return 1
        nom = noms(base, jeton)
        connus = (CONNUS | vus_dans(items)) & set(nom)
        presents = ", ".join("%s (%s)" % (nom[k], k) for k in sorted(connus))
        msg = ("Voici le fil de la partie jusqu'à maintenant, tel que Teodor le vit :\n\n"
               + rendre(items[-80:], nom)
               + "\n\nGens dont tu connais le nom (id entre parenthèses) : " + presents
               + "\n\nC'est à toi. Tour %d sur %d. Une action de Teodor." % (tour, a.tours))
        if a.voir:
            print(sys_txt[:1500], "\n...\n", msg[-3000:])
            return 0
        if a.fournisseur == "claude":
            action, cout = appeler(sys_txt, msg, a.modele)
        else:
            action, cout = appeler_moteur(sys_txt, msg)
        corps = {"type": "libre", "mode": action["mode"], "texte": action["texte"].strip()}
        if action["mode"] == "dire" and action.get("a_qui") in connus:
            corps["destinataire_id"] = action["a_qui"]
        depuis = len(items)
        rep = post(base, "/action?jeton=" + jeton, corps)
        journal("\n## Tour %d\n\n- **%s** : %s%s\n- *pourquoi* : %s\n- ref `%s` · %s"
                % (tour, action["mode"], corps["texte"],
                   (" → `%s`" % corps["destinataire_id"]) if "destinataire_id" in corps else "",
                   action.get("pourquoi", ""), rep.get("ref"), cout))
        print("tour %d : %s — %s" % (tour, action["mode"], corps["texte"]), flush=True)
    items = attendre_reponse(base, jeton, depuis, a.calme, a.attente_max)
    journal("\n**Fin des %d tours.**" % a.tours)
    print("fin", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
