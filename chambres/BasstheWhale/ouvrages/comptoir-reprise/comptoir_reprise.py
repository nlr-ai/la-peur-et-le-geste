#!/usr/bin/env python3
"""Contrôle une fiche de reprise sans transformer une intention en engagement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHAMPS = (
    "date",
    "personne",
    "apport",
    "offre",
    "besoin",
    "premier_geste",
    "reserve",
    "source",
)


def verifier(chemin: Path) -> int:
    try:
        fiche = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALIDE — lecture impossible : {exc}")
        return 2

    absents = [champ for champ in CHAMPS if not str(fiche.get(champ, "")).strip()]
    if absents:
        print("INCOMPLETE — " + ", ".join(absents))
        return 1

    print(f"CONFORME — {fiche['personne']} — premier geste : {fiche['premier_geste']}")
    print(f"RÉSERVE — {fiche['reserve']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fiche", type=Path, help="fiche JSON à contrôler")
    args = parser.parse_args()
    return verifier(args.fiche)


if __name__ == "__main__":
    raise SystemExit(main())
