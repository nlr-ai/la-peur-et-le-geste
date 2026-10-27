# -*- coding: utf-8 -*-
"""Régence : statut des sièges et lecture des passations historiques.

Un siège vacant n'est plus activé automatiquement. La matière conservée ici
sert aux dépêches explicites et à la remise des archives déjà écrites.
"""
from __future__ import print_function

import os

from temps.expose import occupation
from etat.expose import tables


import os as _os, sys as _sys  # le chemin des freres : scripts/ et scripts/noyau/
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "scripts" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
for _p in (_d, _os.path.join(_d, "noyau")):
    if _p not in _sys.path:
        _sys.path.insert(0, _p)

import racines

# LES DEUX RACINES, ET POURQUOI LES DEUX RESTENT ICI.
# `ETAT` suit le monde courant : c'est la donnee. `RACINE` ne le suit pas —
# `regence_passation` l'importe pour rendre un chemin LISIBLE (`os.path.relpath`)
# et c'est la racine du DEPOT qu'il lui faut, celle qu'elle a toujours valu.
# Le nom doit rester expose : il traverse un import circulaire (cette porte
# charge `regence_passation`, qui relit ces deux noms-ci), donc le supprimer ne
# rend pas une erreur de nom a la ligne fautive mais un « partially initialized
# module » a l'autre bout du cercle, et la garde d'occupation tombe.
RACINE = racines.DEPOT
ETAT = racines.etat()


def lire_json(chemin, defaut):
    return tables.lire(chemin, defaut)


def lire_table(nom, defaut):
    return lire_json(os.path.join(ETAT, nom + ".json"), defaut)


def sieges():
    roster = lire_table("joueurs", [])
    if isinstance(roster, dict):
        roster = roster.get("joueurs") or roster.get("sieges") or []
    return [s for s in roster
            if isinstance(s, dict) and s.get("personnage_id")]


def sieges_vacants():
    return occupation.vacants()


def sieges_occupes():
    return occupation.occupes()


def est_en_regence(pid):
    return bool(pid) and pid in sieges_vacants()


def nom_de(pid):
    for siege in sieges():
        if siege["personnage_id"] == pid:
            return siege.get("nom") or pid
    for personnage in lire_table("personnages", []) or []:
        if isinstance(personnage, dict) and personnage.get("id") == pid:
            return personnage.get("nom") or pid
    return pid


def date_du_monde():
    return (lire_table("monde", {}) or {}).get("date") or {}


def horloge_de(pid):
    return (lire_table("horloges", {}) or {}).get(pid) or date_du_monde()


def dire_date(date):
    if not date:
        return "date inconnue"
    return "an %s, %se lune, %se jour" % (
        date.get("annee"), date.get("lune"), date.get("jour"))


from temps.regence_passation import (  # noqa: E402,F401
    clause_croyance, clause_declencheur, clause_posee, tete_de,
    poser_clause, registre_de, lire_registre, compte_rendu,
    remettre, etat_des_regences, main)
