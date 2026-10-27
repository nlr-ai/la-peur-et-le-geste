# -*- coding: utf-8 -*-
"""SIEGE — un invite tenu par une session Claude, au lieu de joueur_pnj.py.

    python mondes/dix-minutes/outils/siege.py --qui ipi --tete       # sa fiche et les regles, une fois
    python mondes/dix-minutes/outils/siege.py --qui ipi --attendre   # bloque jusqu'a ce que le monde reponde, puis rend le fil
    python mondes/dix-minutes/outils/siege.py --qui ipi --dire "..."  # ses mots, et rien d'autre
    python mondes/dix-minutes/outils/siege.py --qui ipi --agir "..."  # carnet ou demande au maitre de maison

Meme brouillard que joueur_pnj.py, dont il reprend les gestes : le fil vient
de GET /scene avec le jeton du siege, la parole part par POST /action. La
session qui tient le siege n'ouvre rien d'autre du monde.
"""
import argparse
import io
import os
import sys

MONDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPOT = os.path.dirname(os.path.dirname(MONDE))
sys.path.insert(0, os.path.join(DEPOT, "scripts"))
import joueur_pnj as jp  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qui", required=True)
    ap.add_argument("--tete", action="store_true")
    ap.add_argument("--attendre", action="store_true")
    ap.add_argument("--dire")
    ap.add_argument("--agir")
    ap.add_argument("--a-qui", default="")
    ap.add_argument("--calme", type=int, default=8)
    ap.add_argument("--max", type=int, default=1500, help="secondes d'attente au plus")
    a = ap.parse_args()
    base = "http://localhost:%d" % (jp.port_monde("dix-minutes") or 3211)
    jeton = jp.siege(MONDE, a.qui)["jeton"]

    if a.tete:
        texte, _ = jp.tete(MONDE, a.qui)
        print(texte)
        return
    if a.dire or a.agir:
        corps = {"type": "libre", "mode": "dire" if a.dire else "agir", "texte": (a.dire or a.agir).strip()}
        if a.dire and a.a_qui:
            corps["destinataire_id"] = a.a_qui
        rep = jp.post(base, "/action?jeton=" + jeton, corps)
        print("envoyé (%s)" % rep.get("ref"))
        return

    items = jp.get(base, "/scene?jeton=" + jeton).get("items", [])
    if a.attendre:
        siens = [k for k, i in enumerate(items) if jp.de_lui(i, a.qui)]
        attendu = siens and not any(jp.reponse_du_monde(i, a.qui) for i in items[siens[-1] + 1:])
        if attendu:
            items = jp.attendre_reponse(base, jeton, siens[-1] + 1, a.calme, a.max, qui=a.qui)
            if items is None:
                print("[Rien n'est venu en %d s. Relance --attendre.]" % a.max)
                return
    nom = jp.noms(base, jeton)
    print(jp.rendre(items[-60:], nom, a.qui))
    print("\n— C'est à toi.")


if __name__ == "__main__":
    main()
