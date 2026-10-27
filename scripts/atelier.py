# -*- coding: utf-8 -*-
"""Atelier de developpement : equipe, dossier, essayer, resultat."""
import os
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
for chemin in (SCRIPTS, os.path.join(SCRIPTS, "noyau")):
    if chemin not in sys.path:
        sys.path.insert(0, chemin)

from agents.expose import atelier_main

if __name__ == "__main__":
    raise SystemExit(atelier_main())
