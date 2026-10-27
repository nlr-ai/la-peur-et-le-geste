# -*- coding: utf-8 -*-
"""JETONS — ce que les agents ont consomme, lu dans `.agents-runtime/compute`.

    python scripts/analyse/jetons.py                 # les 7 derniers jours
    python scripts/analyse/jetons.py --jours 1 --par role

Ne compte que les appels enregistres depuis l'ajout du champ `jetons` (4 oct.
2026) ; les plus anciens n'ont que leur duree et sont dits a part. Le cout en
dollars n'est donne que si le fournisseur l'a rendu lui-meme (Claude) : on
n'invente pas un tarif.
"""
import os as _os, sys as _sys  # le chemin des freres : scripts/ et scripts/noyau/
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "scripts" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
for _p in (_d, _os.path.join(_d, "noyau")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

import argparse
import collections
import time

from agents import compute

CHAMPS = ("entree", "cache_lue", "cache_ecrite", "sortie", "raisonnement")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--jours", type=float, default=7)
    p.add_argument("--par", choices=("provider", "role", "modele"),
                   default="provider")
    a = p.parse_args()
    depuis = time.time() - a.jours * 86400
    evs = [e for e in compute.lire_evenements() if e["fin_mur_s"] >= depuis]
    comptes = [e for e in evs if e.get("jetons")]
    groupes = collections.defaultdict(lambda: collections.Counter())
    for e in comptes:
        g = groupes[str(e.get(a.par) or "?")]
        g["appels"] += 1
        g["secondes"] += e.get("duree_secondes") or 0
        for c in CHAMPS + ("cout_usd",):
            g[c] += e["jetons"].get(c) or 0
    print("%d appels sur %g jour(s), dont %d avec jetons."
          % (len(evs), a.jours, len(comptes)))
    if not comptes:
        return
    print("%-28s %6s %8s %10s %11s %9s %9s %9s"
          % (a.par, "appels", "s/appel", "entree", "cache lue", "sortie",
             "raison.", "$"))
    for nom, g in sorted(groupes.items(), key=lambda x: -x[1]["appels"]):
        print("%-28s %6d %8.0f %10d %11d %9d %9d %9s"
              % (nom[:28], g["appels"], g["secondes"] / g["appels"],
                 g["entree"], g["cache_lue"], g["sortie"], g["raisonnement"],
                 ("%.2f" % g["cout_usd"]) if g["cout_usd"] else "-"))


if __name__ == "__main__":
    main()
