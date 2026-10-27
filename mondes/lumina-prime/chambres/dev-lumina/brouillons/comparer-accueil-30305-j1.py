# -*- coding: utf-8 -*-
"""DEV, J1, après le retour de PITCH sur 60301.

De ma main, pour 30305. Je compare deux programmes d'usage sur les passages
transcrits. Je ne dessine ni seuil ni cloison et je n'affecte aucune pièce :
le programme reste à Nova, porté par Aria en 10022.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, numero):
    for l in t["lignes"]:
        if l["cellules"][0].strip("* ") == numero:
            return l
    raise KeyError(numero)


def col(t, fragment):
    for i, nom in enumerate(t["colonnes"]):
        if fragment in nom:
            return i
    raise KeyError(fragment)


def corriger(livre):
    actions = table(livre, "⚔️")
    action = ligne(actions, "30305")["cellules"]
    action[col(actions, "Ce qu'on fait")] = (
        "Fait le J1 après le retour de PITCH sur 60301. Les esquisses A et B "
        "sont comparées comme programmes d'usage dans la table 🧩, sur les "
        "passages dessinés du plan initial. Toutes deux font apparaître les "
        "mêmes besoins à soumettre à Nova : une voie publique vers la galerie "
        "qui ne traverse ni le salon ni la salle du conseil, et une attente "
        "hors du passage. Aucun seuil, cloison ni usage n'est affecté."
    )
    action[col(actions, "La preuve")] = (
        "Table 🧩 de ce volume ; parcours 60301 et retour de PITCH ; comparaison remise à Aria pour 10022."
    )
    action[col(actions, "État")] = "faite"
    action[col(actions, "Avec quoi")] = "Relevé 30301 ; parcours 60301 fait ; plan initial transcrit en 30307."

    titre = "🧩 Deux agencements d'usage de l'accueil — comparaison 30305, J1"
    comparaison = {
        "titre": titre,
        "colonnes": [
            "Point comparé",
            "Esquisse A — hall oriente, salon reçoit, galerie expose",
            "Esquisse B — hall traverse, galerie oriente et expose, salon reçoit",
            "Conclusion pour 10022",
            "Source",
        ],
        "lignes": [
            {"cellules": [
                "Arrivée et orientation",
                "L'orientation commence dans le hall ; le salon est atteint directement en une minute conventionnelle.",
                "L'orientation serait dans la galerie, mais le plan ne donne depuis le hall que le salon ou la salle du conseil pour l'atteindre.",
                "A fonctionne sur le dessin actuel pour orienter. B exige d'abord une voie publique indépendante vers la galerie.",
                "30301 ; 30307 ; 60301, dessinés non essayés.",
            ]},
            {"cellules": [
                "Entretien au salon et exposition à la galerie",
                "Les usages sont dans deux pièces, mais le public de la galerie traverse le salon ou la salle du conseil : l'exposition indépendante ne tient pas.",
                "Le salon reste distinct, mais tout arrivant vers la galerie traverse encore le salon ou la salle du conseil : la séparation annoncée ne tient pas.",
                "Pour rendre possibles les usages simultanés dans A ou B : voie publique vers la galerie sans traverser le salon ni le conseil. C'est un besoin d'aménagement, pas une décision prise.",
                "Retour de PITCH sur 60301 ; passages du plan initial.",
            ]},
            {"cellules": [
                "Attendre un rendez-vous",
                "Le hall reçoit et oriente, mais aucune place d'attente hors de ses trajets n'est établie.",
                "Le hall est réservé au passage ; aucune autre place d'attente hors trajet n'est établie.",
                "Les deux esquisses exigent que Nova arrête un usage d'attente hors passage. Sa place ne sera dessinée qu'après ce choix.",
                "60301 ; table ❓ de ce volume.",
            ]},
            {"cellules": [
                "Ce qui est décidé ici",
                "Proposition comparable, aucune affectation.",
                "Proposition comparable, aucune affectation.",
                "Aria peut porter les usages et les simultanéités à Nova en 10022. Après décision de 10010, DEV dessinera les seuils et la place d'attente ; un grand aménagement revient à Nova.",
                "30204 ; 30381 ; mandat O02.",
            ]},
        ],
    }
    for i, t in enumerate(livre["tables"]):
        if t["titre"].startswith("🧩 Deux agencements"):
            livre["tables"][i] = comparaison
            break
    else:
        livre["tables"].append(comparaison)


for essai in range(5):
    session = bibliotheque.ouvrir(ETAT)
    livres = {livre["id"]: livre for livre in session.livres}
    corriger(livres["affaire-plans-lumina"])
    try:
        session.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as exc:
        print("relu :", exc)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
