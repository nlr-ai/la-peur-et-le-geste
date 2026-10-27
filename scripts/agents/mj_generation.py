# -*- coding: utf-8 -*-
"""La rotation des sessions du MJ.

Une session sans fin coutait de plus en plus cher a chaque pas : mesure du
3.10 sur Codex, 110 a 190 k jetons de contexte par appel d'outil, des
millions par tour, pour un manuel de 25 k. L'historique ne servait presque
plus : ce qui fait foi vit dans `etat/` et dans le flux, que le reveil pointe.

Tous les `LE_CONSEIL_MJ_TOURS` tours reussis (20 par defaut, 0 = jamais),
une session cede la place a la suivante : meme base, generation + 1, donc un
autre identifiant. La generation 0 garde l'identifiant historique a l'octet
pres. Le premier reveil d'une generation neuve le sait et le dit au MJ.
"""
import io
import json
import os
import uuid


def _fichier(etat):
    return os.path.join(os.path.dirname(etat), ".agents-runtime", "mj",
                        "generations.json")


def _tours_max():
    try:
        return int(os.environ.get("LE_CONSEIL_MJ_TOURS") or 20)
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


def suffixe(etat, base):
    """'' pour la generation 0, sinon '#<n>' a coller a la base."""
    g = int(_lire(etat).get(base, {}).get("generation", 0))
    return "#%d" % g if g else ""


def neuve(etat, base):
    return bool(_lire(etat).get(base, {}).get("neuve"))


def compter_tour(etat, base):
    """Un tour reussi de plus ; rend True si la prochaine session est neuve.
    Appele sous le ticket de la session (file_mj) : un seul ecrivain par base."""
    tout = _lire(etat)
    entree = dict(tout.get(base) or {})
    entree["tours"] = int(entree.get("tours", 0)) + 1
    entree["neuve"] = False
    maximum = _tours_max()
    if maximum and entree["tours"] >= maximum:
        entree["generation"] = int(entree.get("generation", 0)) + 1
        entree["tours"] = 0
        entree["neuve"] = True
    tout[base] = entree
    _ecrire(etat, tout)
    return entree["neuve"]
