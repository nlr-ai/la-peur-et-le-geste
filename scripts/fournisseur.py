# -*- coding: utf-8 -*-
"""Choisir le fournisseur global des reveils Claude/Codex.

Usage :
    python scripts/fournisseur.py
    python scripts/fournisseur.py codex --modele gpt-5.3-codex-spark --effort low --fast
    python scripts/fournisseur.py claude
    python scripts/fournisseur.py --mj session-claude-guetteur   # MJ tenu par une session vivante
    python scripts/fournisseur.py --mj defaut                    # MJ rendu au fournisseur global
"""
import argparse
import json
import os
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from agents import runtime  # noqa: E402
from agents import guichet_mj  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fournisseur", nargs="?", choices=("claude", "codex", "chatgpt", "gemini"))
    ap.add_argument("--modele")
    ap.add_argument("--effort")
    vitesse = ap.add_mutually_exclusive_group()
    vitesse.add_argument("--fast", action="store_true",
                         help="service tier fast pour tous les appels Codex")
    vitesse.add_argument("--standard", action="store_true",
                         help="retirer le service tier fast")
    ap.add_argument("--mj", metavar="MODE",
                    help="session-claude-guetteur : le MJ passe par le guichet"
                         " d'une session vivante ; defaut : comme les autres")
    a = ap.parse_args()
    if a.mj is not None:
        guichet_mj.choisir_mode(a.mj)
    fast = True if a.fast else False if a.standard else None
    d = (runtime.choisir(a.fournisseur, a.modele, a.effort, fast=fast)
         if a.fournisseur else runtime.configuration())
    d = dict(d, mode_mj=guichet_mj.mode_mj() or d["fournisseur"])
    print(json.dumps(d, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
