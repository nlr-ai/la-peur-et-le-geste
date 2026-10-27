# -*- coding: utf-8 -*-
"""DEV, J1, après remise du programme par PITCH.

La preuve de 11021 existe déjà dans le volume et dans actes.json. Je ne
fabrique pas une seconde preuve : je porte seulement l'action à son état fait.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def clore(livre):
    table = next(t for t in livre["tables"] if t["titre"].startswith("⚔️"))
    i_etat = next(i for i, nom in enumerate(table["colonnes"]) if "État" in nom)
    ligne = next(l for l in table["lignes"] if l["cellules"][0] == "11021")
    ligne["cellules"][i_etat] = "faite"


for essai in range(5):
    session = bibliotheque.ouvrir(ETAT)
    livres = {livre["id"]: livre for livre in session.livres}
    clore(livres["affaire-habiter-creative-nexus"])
    try:
        session.sauver()
        print("11021 portée à faite, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as exc:
        print("relu :", exc)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
