# -*- coding: utf-8 -*-
"""DEV, J1, remise de l'étape 3 de 11020 à l'étude 11023.

Éprouve les trois scénarios de 11021 dans A et B avec une scène minimale
commune. La scène est un protocole de comparaison, pas une capacité cible.
Ne choisit aucune variante, ne cote rien et ne ferme pas 11020.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a11020 = next(l for l in actions["lignes"] if l["cellules"][0] == "11020")["cellules"]
    a11020[indice(actions, "Ce qu")] = (
        "Étapes 1 à 3 faites le J1 : socle vérifié en 🧱 ; deux topologies sans cote en 🧭, "
        "comparées en ⚖️ ; les trois scénarios de 11021 passent dans A et B selon la table 🚶. "
        "Une scène minimale commune est remise à 11023 comme protocole, non comme capacité cible. "
        "Aucune variante n'est retenue. Prochaine étape : annotations de droits, de cour et de moyens."
    )
    a11020[indice(actions, "La preuve")] = (
        "Tables 🧱, 🧭, ⚖️ et 🚶 : existant et proposé séparés, parcours des trois scénarios "
        "comparés, aucune cote ni capacité inventée, choix laissé ouvert."
    )

    if any(t["titre"].startswith("🚶 Épreuve des scénarios 11021") for t in livre["tables"]):
        return

    livre["tables"].append({
        "titre": "🚶 Épreuve des scénarios 11021 dans les topologies 11020 — remise à 11023, J1",
        "colonnes": [
            "Lecture commune",
            "A — Greffe sur l’existant",
            "B — Îlot autonome à deux seuils",
            "Ce que 11023 peut mesurer et ce qui reste inconnu"
        ],
        "lignes": [
            {"cellules": [
                "Périmètre de la scène de référence",
                "Une cellule existante candidate, son seuil sur la cour des Ateliers, la cour partagée, "
                "l’accès des Ateliers et la Halle candidate comme galerie publique séparée.",
                "Un espace personnel proposé, son seuil sur la cour nouvelle, le seuil commun de l’îlot, "
                "l’atelier partagé proposé et la galerie publique à seuil distinct.",
                "Comparer les mêmes gestes sur les seuls éléments nommés. Dimensions, nombre total "
                "d’espaces, disponibilité de l’existant et raccords exacts restent inconnus."
            ]},
            {"cellules": [
                "S’installer",
                "Depuis le nœud public : accès des Ateliers, cour, seuil propre de la cellule candidate ; "
                "aucune autre cellule personnelle n’est traversée.",
                "Depuis le nœud public : seuil commun, cour nouvelle, seuil propre de l’espace proposé ; "
                "aucun autre espace personnel n’est traversé.",
                "Mesurer, si accessible, délai de réponse, rendu, calcul et réseau du parcours. "
                "Lisibilité, praticabilité et droits de franchissement restent à essayer ou proposer."
            ]},
            {"cellules": [
                "Modifier puis revenir",
                "Dans une cellule candidate, retirer un seul élément transformable désigné, vérifier que "
                "seuil et cour restent libres, puis remettre cet élément. Les cloisons démontables sont un précédent, pas une autorisation.",
                "Dans un espace personnel proposé, retirer un seul élément transformable désigné, vérifier "
                "que seuil et cour restent libres, puis le remettre. La nature de cet élément reste à choisir.",
                "Mesurer stockage et mémoire avant, pendant et après, ainsi que le retour si un essai est autorisé. "
                "La scène fixe une opération comparable ; elle ne fixe ni dimension ni fréquence d’usage."
            ]},
            {"cellules": [
                "Recevoir jusqu’au seuil",
                "Une personne invitée suit l’accès des Ateliers puis la cour jusqu’au seuil de la cellule ; "
                "elle ne traverse ni autre cellule ni Halle. Elle repart par le même parcours partagé.",
                "Une personne invitée franchit le seuil commun puis suit la cour jusqu’au seuil personnel ; "
                "elle ne traverse ni autre espace personnel ni galerie. Elle repart par le même parcours partagé.",
                "La scène comprend un habitant et une personne invitée uniquement pour éprouver le parcours ; "
                "ce n’est pas une simultanéité cible. Trafic, délai et traces ne se mesurent que si le système les expose."
            ]},
            {"cellules": [
                "Séparation public, partagé et personnel",
                "Galerie publique candidate dans la Halle, hors de la cour ; cour partagée ; cellules personnelles candidates sur la cour.",
                "Galerie à seuil public distinct ; cour derrière le seuil commun ; espaces personnels sur la cour ; raccord de service atelier–galerie contrôlé.",
                "Le dessin sépare les parcours mais ne garantit aucun droit ni confidentialité. 11022 doit dire qui franchit, invite et consulte une trace."
            ]},
            {"cellules": [
                "Règle de résultat pour 11023",
                "Nommer séparément ce que coûte l’adaptation des éléments existants candidats et laisser leur disponibilité inconnue.",
                "Nommer séparément ce que coûte la création des éléments et raccords proposés.",
                "Pour chaque grandeur : besoin, capacité disponible, marge, unité, condition, date et source. "
                "Sans mesure : inconnu. Sans tarif ou budget : coût financier inconnu. Aucun total au-delà de la scène minimale."
            ]}
        ],
        "pages": [
            "Cette scène minimale rend A et B comparables pour 11023. Elle ne décrit ni un habitant réel, "
            "ni un nombre d’occupants à soutenir, ni une fréquence : ces valeurs restent inconnues.",
            "La remise n’achève pas 11020 : les annotations de 11022, 11220 et 11023 doivent encore revenir "
            "avant l’assemblage et le choix soumis à Nova."
        ]
    })


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
