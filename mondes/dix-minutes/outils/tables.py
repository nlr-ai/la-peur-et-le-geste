# -*- coding: utf-8 -*-
"""TABLES — la main du maitre de maison, dans le salon de Dix minutes.

    python mondes/dix-minutes/outils/tables.py --etat
    python mondes/dix-minutes/outils/tables.py --placer 1 marc-aurele:ipi wu-zetian:zhang-min ...
    python mondes/dix-minutes/outils/tables.py --decor table-1 "Une phrase de decor."
    python mondes/dix-minutes/outils/tables.py --cloche table-1        # ou --cloche tout
    python mondes/dix-minutes/outils/tables.py --carnets
    python mondes/dix-minutes/outils/tables.py --guetter               # sous Monitor

Il n'ecrit au fil que par scripts/append_flux.py, toujours --pour <un siege> :
chaque invite recoit SA table et son decor, et la presence suit les items
`salle` (deux invites dans la meme salle s'entendent, et eux seuls). La ronde
en cours vit dans salon/rondes.json, hors de etat/ : ce n'est pas de l'etat du
monde, c'est le carnet de bal du MJ.

Il ne fait jamais parler un invite. Il compte leurs repliques, il ne les lit pas.
"""
import argparse
import glob
import io
import json
import os
import shutil
import subprocess
import sys
import time

MONDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPOT = os.path.dirname(os.path.dirname(MONDE))
ETAT = os.path.join(MONDE, "etat")
SALON = os.path.join(MONDE, "salon")
RONDES = os.path.join(SALON, "rondes.json")
REGISTRE = os.path.join(SALON, "registre.md")
LUS = os.path.join(MONDE, ".agents-runtime", "inbox-lue")

REPLIQUES = 10   # une replique vaut une minute : dix, et la clochette sonne

TABLES = {
    "table-1": "La table du tilleul",
    "table-2": "La table de la cheminée",
    "table-3": "La table des cartes",
    "table-4": "La table du jardin d'hiver",
}


def lire(p, defaut):
    try:
        with io.open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defaut


def ecrire(p, d):
    with io.open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def noms():
    return {p["id"]: p["nom"] for p in lire(os.path.join(ETAT, "personnages.json"), [])}


def invites():
    return [j["personnage_id"] for j in lire(os.path.join(ETAT, "joueurs.json"), [])
            if j.get("occupe")]


def registre(texte):
    with io.open(REGISTRE, "a", encoding="utf-8") as f:
        f.write(texte.rstrip("\n") + "\n")


def pousser(pour, *items):
    env = dict(os.environ, CONSEIL_MONDE="dix-minutes")
    cmd = [sys.executable, os.path.join(DEPOT, "scripts", "append_flux.py"), "--pour", pour]
    cmd += [json.dumps(i, ensure_ascii=False) for i in items]
    r = subprocess.run(cmd, cwd=DEPOT, env=env, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit("append_flux a refusé (%s) :\n%s" % (pour, r.stderr or r.stdout))
    if r.stderr.strip():
        sys.stderr.write(r.stderr)


def flux():
    p = os.path.join(ETAT, "flux.jsonl")
    if not os.path.exists(p):
        return []
    out = []
    with io.open(p, encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            if l:
                try:
                    out.append(json.loads(l))
                except ValueError:
                    out.append({})
    return out


def repliques(table, items):
    """Les paroles des deux invites depuis qu'on les a assis."""
    t = lire(RONDES, {}).get("tables", {}).get(table)
    if not t:
        return 0
    return sum(1 for i in items[t["depuis"]:]
               if i.get("type") == "vous" and i.get("joueur_id") in t["paire"]
               and i.get("mode", "dire") in ("dire", "parler"))


# ------------------------------------------------------------------ les gestes

def placer(ronde, paires):
    N = noms()
    tous = set(invites())
    assis, tables = [], {}
    if len(paires) > len(TABLES):
        raise SystemExit("quatre tables, pas davantage")
    for p in paires:
        a, _, b = p.partition(":")
        for x in (a, b):
            if x not in tous:
                raise SystemExit("invité inconnu : %r" % x)
            if x in assis:
                raise SystemExit("%s est assis deux fois" % x)
        assis += [a, b]
    depuis = len(flux())
    for k, p in enumerate(paires):
        a, _, b = p.partition(":")
        table = "table-%d" % (k + 1)
        tables[table] = {"paire": [a, b], "depuis": depuis}
        for moi, autre in ((a, b), (b, a)):
            pousser(moi,
                    {"type": "salle", "lieu": "%s, Le salon" % TABLES[table], "salle": table,
                     "presents": [moi, autre], "moment": "ronde %d" % ronde},
                    {"type": "recit", "texte": "La clochette d'argent tinte. Ronde %d. Un huissier vous conduit "
                     "à %s. En face de vous s'assoit %s. Vous avez dix minutes."
                     % (ronde, TABLES[table].lower(), N.get(autre, autre))})
    attente = sorted(tous - set(assis))
    for x in attente:
        pousser(x,
                {"type": "salle", "lieu": "Le vestibule, Le salon", "salle": "vestibule",
                 "presents": [x], "moment": "ronde %d" % ronde},
                {"type": "recit", "texte": "La clochette tinte, et cette fois personne ne vient vous chercher. "
                 "Ronde %d : vous attendez seul au vestibule. Par les portes entrouvertes, on entend des voix "
                 "sans distinguer les mots. Vous pouvez écrire une demande au maître de maison (agir), ou "
                 "simplement attendre." % ronde})
    ecrire(RONDES, {"ronde": ronde, "tables": tables, "attente": attente, "cloches": []})
    lignes = ["", "## Ronde %d" % ronde]
    for table, t in tables.items():
        a, b = t["paire"]
        lignes.append("- %s : %s × %s — pourquoi : *(à écrire)*" % (TABLES[table], N.get(a, a), N.get(b, b)))
    if attente:
        lignes.append("- Au vestibule : %s" % ", ".join(N.get(x, x) for x in attente))
    registre("\n".join(lignes))
    print("ronde %d placée : %s ; au vestibule : %s" % (ronde, ", ".join(paires), ", ".join(attente) or "personne"))


def decor(table, texte):
    t = lire(RONDES, {}).get("tables", {}).get(table)
    if not t:
        raise SystemExit("personne n'est assis à %s" % table)
    for x in t["paire"]:
        pousser(x, {"type": "recit", "texte": texte})
    print("décor posé à %s" % table)


def cloche(qui):
    R = lire(RONDES, {})
    N = noms()
    cibles = list(R.get("tables", {})) if qui == "tout" else [qui]
    items = flux()
    for table in cibles:
        t = R.get("tables", {}).get(table)
        if not t:
            raise SystemExit("personne n'est assis à %s" % table)
        if table in R.get("cloches", []):
            print("%s : déjà sonnée" % table)
            continue
        n = repliques(table, items)
        for x in t["paire"]:
            pousser(x,
                    {"type": "recit", "texte": "La clochette tinte : les dix minutes sont écoulées."},
                    {"type": "salle", "lieu": "L'alcôve de %s, Le salon" % N.get(x, x), "salle": "alcove-" + x,
                     "presents": [x]},
                    {"type": "recit", "texte": "Un huissier vous mène à votre alcôve et tire le rideau. Sur "
                     "l'écritoire, votre carnet. Écrivez (agir) ce que vous emportez de cette conversation, "
                     "une note de 0 à 10 et pourquoi, et, si vous le voulez, à qui vous aimeriez parler ensuite."})
        R.setdefault("cloches", []).append(table)
        a, b = t["paire"]
        registre("  - %s close après %d répliques." % (TABLES[table], n))
        print("%s sonnée (%d répliques)" % (table, n))
    ecrire(RONDES, R)


def rappel():
    """L'invite qui a parle APRES la clochette attend, dans son alcove, une
    reponse qui ne viendra pas : sa derniere ligne est la sienne. Une ligne de
    decor le rend a son carnet (ronde 1 : deux carnets perdus ainsi)."""
    R = lire(RONDES, {})
    items = flux()
    for table in R.get("cloches", []):
        for x in R["tables"][table]["paire"]:
            siens = [i for i in items if x in (i.get("pour") or []) or i.get("pour") == x]
            if not siens:
                continue
            dernier = siens[-1]
            ecrit = any(i.get("type") == "vous" and i.get("joueur_id") == x and i.get("mode") == "agir"
                        for i in items[R["tables"][table]["depuis"]:])
            if not ecrit and dernier.get("type") == "vous" and dernier.get("joueur_id") == x:
                pousser(x, {"type": "recit", "texte": "Votre phrase est restée sans écho : la clochette avait "
                            "sonné et vous êtes seul dans l'alcôve. Sur l'écritoire, le carnet attend."})
                print("rappel à %s" % x)


def carnets():
    """Relève les actions `agir` (carnets, demandes) ; range les paroles restées dans l'inbox.

    Une parole `dire` reste dans l'inbox quand aucun habitant non joueur ne
    l'entend : c'est le cas de toutes les paroles d'ici, que le partenaire a
    deja recues par le fil. On les range sans les lire."""
    N = noms()
    R = lire(RONDES, {})
    lus = 0
    for p in sorted(glob.glob(os.path.join(ETAT, "inbox", "*", "action-*.json"))):
        qui = os.path.basename(os.path.dirname(p))
        a = lire(p, {})
        dest = os.path.join(LUS, qui)
        os.makedirs(dest, exist_ok=True)
        if a.get("mode") == "agir":
            texte = (a.get("texte") or "").strip()
            print("— %s :\n%s\n" % (N.get(qui, qui), texte))
            registre("  - **Carnet de %s** (ronde %s) : %s" % (N.get(qui, qui), R.get("ronde", "?"),
                                                              texte.replace("\n", " ")))
            lus += 1
        shutil.move(p, os.path.join(dest, os.path.basename(p)))
    print("%d carnet(s) ou demande(s) relevé(s)." % lus)


def etat():
    R = lire(RONDES, {})
    N = noms()
    items = flux()
    print("Ronde %s" % R.get("ronde", "—"))
    for table, t in R.get("tables", {}).items():
        n = repliques(table, items)
        f = "sonnée" if table in R.get("cloches", []) else ("À SONNER" if n >= REPLIQUES else "en cours")
        print("  %s : %s × %s — %d répliques — %s" % (table, N.get(t["paire"][0]), N.get(t["paire"][1]), n, f))
    if R.get("attente"):
        print("  vestibule : %s" % ", ".join(N.get(x, x) for x in R["attente"]))
    attente = [p for p in glob.glob(os.path.join(ETAT, "inbox", "*", "action-*.json"))
               if lire(p, {}).get("mode") == "agir"]
    print("  carnets ou demandes en attente : %d" % len(attente))


def guetter(pas):
    """Une ligne par chose qui demande la main du MJ ; le silence sinon."""
    dits = set()
    while True:
        R = lire(RONDES, {})
        items = flux()
        for table in R.get("tables", {}):
            cle = (R.get("ronde"), table)
            if table not in R.get("cloches", []) and cle not in dits and repliques(table, items) >= REPLIQUES:
                dits.add(cle)
                print("ronde %s : %s a atteint %d répliques — sonner" % (R.get("ronde"), table, REPLIQUES), flush=True)
        for p in glob.glob(os.path.join(ETAT, "inbox", "*", "action-*.json")):
            if p not in dits and lire(p, {}).get("mode") == "agir":
                dits.add(p)
                print("carnet ou demande de %s" % os.path.basename(os.path.dirname(p)), flush=True)
        time.sleep(pas)


def main():
    ap = argparse.ArgumentParser(description="La main du maître de maison.")
    ap.add_argument("--etat", action="store_true")
    ap.add_argument("--placer", nargs="+", metavar=("RONDE", "A:B"))
    ap.add_argument("--decor", nargs=2, metavar=("TABLE", "TEXTE"))
    ap.add_argument("--cloche", metavar="TABLE|tout")
    ap.add_argument("--carnets", action="store_true")
    ap.add_argument("--rappel", action="store_true")
    ap.add_argument("--guetter", action="store_true")
    ap.add_argument("--pas", type=int, default=5)
    a = ap.parse_args()
    if a.placer:
        placer(int(a.placer[0]), a.placer[1:])
    elif a.decor:
        decor(*a.decor)
    elif a.cloche:
        cloche(a.cloche)
    elif a.carnets:
        carnets()
    elif a.rappel:
        rappel()
    elif a.guetter:
        guetter(a.pas)
    else:
        etat()


if __name__ == "__main__":
    main()
