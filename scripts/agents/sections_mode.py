# -*- coding: utf-8 -*-
"""Les sections d'un manuel qui ne servent qu'avec un mode du joueur.

Une ligne `<!-- modes: run -->` (ou `<!-- modes: run, jump -->`) juste avant
un titre markdown marque la section qu'il ouvre : elle court jusqu'au titre
suivant de niveau egal ou superieur. Au reveil, on ne garde que les sections
dont un mode est actif ce tour-ci. Le fichier reste entier pour qui le lit a
la main : un commentaire HTML ne se voit pas.
"""
import re

_MARQUE = re.compile(r"^<!--\s*modes:\s*([a-z_,\s]+?)\s*-->\s*$")
_TITRE = re.compile(r"^(#{1,6})\s")


def filtrer(texte, modes):
    actifs = set(modes or [])
    lignes = texte.split("\n")
    sortie, i = [], 0
    while i < len(lignes):
        m = _MARQUE.match(lignes[i])
        titre = _TITRE.match(lignes[i + 1]) if m and i + 1 < len(lignes) else None
        if not titre:
            sortie.append(lignes[i])
            i += 1
            continue
        voulus = {x.strip() for x in m.group(1).split(",") if x.strip()}
        niveau = len(titre.group(1))
        fin = i + 2
        while fin < len(lignes):
            t = _TITRE.match(lignes[fin])
            if t and len(t.group(1)) <= niveau:
                break
            fin += 1
        if fin < len(lignes) and _MARQUE.match(lignes[fin - 1]):
            fin -= 1  # la marque du titre suivant lui appartient
        if voulus & actifs:
            sortie.extend(lignes[i + 1:fin])
        i = fin
    return "\n".join(sortie)
