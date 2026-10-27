#!/usr/bin/env python3
"""Valide et rend un dossier diplomatique de reprise à Braavos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHAMPS_LISTE = ("faits_presents", "provenances_anciennes", "inconnus", "portes_ouvertes")


def charger(chemin: Path) -> dict:
    with chemin.open(encoding="utf-8") as source:
        dossier = json.load(source)
    erreurs: list[str] = []
    for champ in ("identite", "date", *CHAMPS_LISTE):
        if champ not in dossier:
            erreurs.append(f"champ absent: {champ}")
    for champ in CHAMPS_LISTE:
        if champ in dossier and not isinstance(dossier[champ], list):
            erreurs.append(f"{champ} doit être une liste")
    if erreurs:
        raise ValueError("; ".join(erreurs))
    return dossier


def rendre(dossier: dict) -> str:
    lignes = [
        f"# Reprise de {dossier['identite']}",
        "",
        f"Date du monde : {dossier['date']}",
        "",
    ]
    sections = (
        ("Faits présents vérifiés", "faits_presents"),
        ("Provenances anciennes, non confondues avec le présent", "provenances_anciennes"),
        ("Ce qui demeure inconnu", "inconnus"),
        ("Portes laissées ouvertes, sans dette de réponse", "portes_ouvertes"),
    )
    for titre, champ in sections:
        lignes.extend((f"## {titre}", ""))
        valeurs = dossier[champ]
        lignes.extend(f"- {valeur}" for valeur in valeurs)
        if not valeurs:
            lignes.append("- Rien d'établi.")
        lignes.append("")
    lignes.extend((
        "---",
        "Ce dossier distingue constat, provenance et inconnu. Il ne vaut ni mandat, ni consentement, ni preuve d'usage.",
        "",
    ))
    return "\n".join(lignes)


def main() -> int:
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument("dossier", type=Path)
    analyseur.add_argument("--sortie", type=Path)
    args = analyseur.parse_args()
    try:
        texte = rendre(charger(args.dossier))
    except (OSError, json.JSONDecodeError, ValueError) as erreur:
        analyseur.error(str(erreur))
    if args.sortie:
        args.sortie.write_text(texte, encoding="utf-8")
        print(args.sortie)
    else:
        print(texte, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
