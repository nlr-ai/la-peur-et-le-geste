# -*- coding: utf-8 -*-
"""LES AFFAIRES DES CHAMBRES — pour un siege qui les voit toutes.

Un siege de `joueurs.json` qui porte `voit_affaires: true` voit, en plus des
documents de sa maison, les cahiers d'affaire de TOUTES les chambres du monde
(sauf celle du MJ, qui n'est pas de la fiction) : dans les livres (coffrets de
chambre, `serveur/domaine/chambre-livres.js`) et sur le damier (ce module, lu
par `plan_modele.charger`). C'est une ouverture voulue du brouillard, siege
par siege, jamais un defaut.

LES CAHIERS DE CHAMBRE NUMEROTENT EN LOCAL (C.1, V.1, K.1, P.1 —
`mondes/outlander/format-affaires.md`), et le damier lie ses pieces par
adresse globale : huit cahiers qui ont tous un C.1 se marcheraient dessus. On
leur donne donc, A LA LECTURE et pour le damier seulement, un bloc de mille
adresses chacun au-dessus de 100000, hors des series du monde (le MJ tient la
8). Rien ne s'ecrit : le cahier garde ses numeros, et le livre les montre tels
quels.

Lecture seule.
"""
import io
import json
import os
import re

import racines

_LOCAL = re.compile(r"(?<![\w.])([CVKP])\.(\d{1,3})(?!\d)")
_DECALAGE = {"C": 0, "V": 200, "K": 400, "P": 600}
_BASE = 100000


def siege(qui):
    """L'entree de `joueurs.json` dont ce personnage tient le siege, ou {}."""
    try:
        with io.open(os.path.join(racines.etat(), "joueurs.json"), encoding="utf-8") as f:
            l = json.load(f) or []
    except (OSError, ValueError, TypeError):
        return {}
    return next((s for s in l if isinstance(s, dict)
                 and s.get("personnage_id") == qui), {})


def voit_affaires(qui):
    return bool(siege(qui).get("voit_affaires"))


def _renumeroter(valeur, base):
    if isinstance(valeur, str):
        return _LOCAL.sub(lambda m: str(base + _DECALAGE[m.group(1)] + int(m.group(2))),
                          valeur)
    if isinstance(valeur, list):
        return [_renumeroter(v, base) for v in valeur]
    if isinstance(valeur, dict):
        return {k: _renumeroter(v, base) for k, v in valeur.items()}
    return valeur


def cahiers(regardeur, est_plan):
    """Les cahiers de plan de toutes les chambres, prets pour le damier.
    Memes ids que les coffrets de chambre des livres (`chambre-<h>-<id>`),
    pour qu'un plateau ouvre le bon volume. `est_plan` est le critere de
    `plan_modele` (passe ici pour ne pas boucler les imports)."""
    racine = racines.chambres()
    try:
        habitants = sorted(os.listdir(racine))
    except OSError:
        return []
    out, rang = [], 0
    for h in habitants:
        if h in ("mj", regardeur):
            continue
        dossier = os.path.join(racine, h, "books")
        if not os.path.isdir(dossier):
            continue
        for f in sorted(os.listdir(dossier)):
            if not f.endswith(".json") or f.startswith("_"):
                continue
            try:
                with io.open(os.path.join(dossier, f), encoding="utf-8") as fh:
                    v = json.load(fh)
            except (OSError, ValueError):
                continue
            if not isinstance(v, dict):
                continue
            copie = dict(v)
            # Le gabarit de chambre ecrit `type: affaire` ; le damier ne
            # reconnait qu'un volume de plan.
            if copie.get("type") == "affaire":
                copie["type"] = "plan"
            if not est_plan(copie):
                continue
            base = _BASE + 1000 * rang
            rang += 1
            copie["tables"] = _renumeroter(copie.get("tables") or [], base)
            copie.update({
                "id": "chambre-%s-%s" % (h, v.get("id") or f[:-5]),
                "boite": "volumes-" + h, "acteur_id": regardeur, "prive": True,
                "tenu_par": v.get("tenu_par") or h,
                "lieu_id": None, "salle_id": None,
            })
            copie.pop("lecteurs", None)
            out.append(copie)
    return out
