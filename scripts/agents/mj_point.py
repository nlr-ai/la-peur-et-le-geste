# -*- coding: utf-8 -*-
"""Le point d'etape : tous les ~20 tours d'un joueur, le MJ lui demande
hors fiction s'il veut ajuster la partie ou avancer.

Un MJ ne compte pas ses tours : sa session tourne tous les vingt, et sa
memoire avec. Le lanceur compte donc a sa place, par siege joueur. Quand le
compte atteint `LE_CONSEIL_MJ_POINT` (20 par defaut, 0 = jamais), le reveil
porte `POINT D'ETAPE` ; le compte ne repart a zero que lorsqu'un tour a
reellement pousse un item `suites` marque `point: true`. Un MJ qui juge le
moment mauvais (un combat, une bifurcation brulante) le repousse donc au
tour suivant sans le perdre.
"""
import io
import json
import os
import uuid


def _fichier(etat):
    return os.path.join(os.path.dirname(etat), ".agents-runtime", "mj",
                        "points.json")


def _intervalle():
    try:
        return int(os.environ.get("LE_CONSEIL_MJ_POINT") or 20)
    except ValueError:
        return 20


def _lire(etat):
    try:
        with io.open(_fichier(etat), encoding="utf-8") as f:
            valeur = json.load(f)
        return valeur if isinstance(valeur, dict) else {}
    except (OSError, ValueError):
        return {}


def _ecrire(etat, valeur):
    chemin = _fichier(etat)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    temporaire = chemin + ".%s.tmp" % uuid.uuid4().hex
    with io.open(temporaire, "w", encoding="utf-8", newline="\n") as f:
        json.dump(valeur, f, ensure_ascii=False, indent=2)
    os.replace(temporaire, chemin)


def du(etat, joueur):
    """True si ce tour doit porter le point d'etape."""
    intervalle = _intervalle()
    if not intervalle:
        return False
    return int(_lire(etat).get(joueur, {}).get("tours", 0)) >= intervalle


def compter_tour(etat, joueur, point_pousse):
    """Un tour reussi de plus ; un point pousse remet le compte a zero."""
    tout = _lire(etat)
    entree = dict(tout.get(joueur) or {})
    entree["tours"] = 0 if point_pousse else int(entree.get("tours", 0)) + 1
    tout[joueur] = entree
    _ecrire(etat, tout)


def point_pousse(items):
    return any(it.get("type") == "suites" and it.get("point")
               for it in items)
