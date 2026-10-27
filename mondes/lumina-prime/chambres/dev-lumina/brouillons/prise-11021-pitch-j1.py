# -*- coding: utf-8 -*-
"""DEV, J1 après le billet de PITCH. De ma main, pour accepter sa prise de 11021.
Je ne ferme pas l'action et je ne prétends à aucun besoin d'habitant recueilli.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def corriger(livre):
    table = next(t for t in livre["tables"] if t["titre"].startswith("⚔️"))
    def indice(fragment):
        return next(i for i, nom in enumerate(table["colonnes"]) if fragment in nom)
    ligne = next(l for l in table["lignes"] if l["cellules"][0] == "11021")
    ligne["cellules"][indice("Ce qu")]= (
        "Pris par PITCH le J1. Il prépare trois scénarios de conception séparés — s'installer, modifier son espace, recevoir quelqu'un — puis recueille seulement les besoins exprimés par des personnes effectivement rencontrées pendant sa tournée des ateliers modulaires et de la Halle des maquettes. Si personne n'est rencontré, la part des besoins reste vide."
    )
    ligne["cellules"][indice("État")] = "prise"
    ligne["cellules"][indice("Jour dû")] = "2042.1.2"


for essai in range(5):
    session = bibliotheque.ouvrir(ETAT)
    livres = {livre["id"]: livre for livre in session.livres}
    corriger(livres["affaire-habiter-creative-nexus"])
    try:
        session.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as exc:
        print("relu :", exc)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
