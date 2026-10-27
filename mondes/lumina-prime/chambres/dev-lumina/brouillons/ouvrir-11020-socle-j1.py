# -*- coding: utf-8 -*-
"""DEV, J1, ambition de vingt minutes. De ma main, pour l'action 11020.

Inscrit le socle vérifié nécessaire à la première implantation et porte 11020
à « en cours ». Accepte aussi les prises proposées de 11023 et 11220, sans
fermer aucune action ni inventer d'échéance pour Gaia.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def ligne(t, numero):
    return next(l for l in t["lignes"] if l["cellules"][0] == numero)


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")

    a11020 = ligne(actions, "11020")["cellules"]
    a11020[indice(actions, "Ce qu")]= (
        "Étape 1 faite le J1 : le socle vérifié de l'implantation est écrit dans la table 🧱. Il sépare existant, projet, accès conventionnels et inconnues. Prochaine étape : tracer deux topologies comparables, sans cote non mesurée."
    )
    a11020[indice(actions, "État")] = "en cours"
    a11020[indice(actions, "Jour dû")] = "2042.1.2"

    a11023 = ligne(actions, "11023")["cellules"]
    a11023[indice(actions, "Ce qu")]= (
        "Prise proposée par Quantum le J1 à 12h55, acceptée par DEV : sur l'esquisse 11020 et le relevé 40302, identifier besoins, capacités disponibles et coût documentable, avec sources, unités et inconnues."
    )
    a11023[indice(actions, "État")] = "prise"
    a11023[indice(actions, "Jour dû")] = "2042.1.3, avant midi"

    a11220 = ligne(actions, "11220")["cellules"]
    a11220[indice(actions, "Ce qu")]= (
        "Prise proposée par Gaia le J1 à 13h30, acceptée par DEV : après 11020, distinguer passage, séjour et retrait, puis situer haltes, seuils et raccord de la cour au quartier."
    )
    a11220[indice(actions, "État")] = "prise"

    if not any(t["titre"].startswith("🧱 Socle vérifié") for t in livre["tables"]):
        livre["tables"].append({
            "titre": "🧱 Socle vérifié de l’implantation 11020 — étape 1, J1",
            "colonnes": ["Élément", "Statut", "Fait utilisable", "Limite à conserver", "Source"],
            "lignes": [
                {"cellules": [
                    "Creative Nexus",
                    "Existant au plan",
                    "Le quartier est relié conventionnellement au Parvis du Radiant Core en 3 minutes, à la Halle des maquettes en 1 minute et aux Ateliers modulaires en 1 minute.",
                    "Ces liaisons sont dessinées, non essayées. Elles ne situent pas la parcelle du futur îlot ni son raccord exact.",
                    "plan-initial-radiant-core, table « Les passages » ; relevé de Gaia transmis à DEV."
                ]},
                {"cellules": [
                    "Ateliers modulaires",
                    "Existant décrit",
                    "Cellules de travail autour d’une cour, cloisons démontables, accès indépendants ; un rail peut séparer démonstration publique et travail.",
                    "Aucune dimension, capacité ni disponibilité de cellule n’est établie. Cet existant est un précédent à étudier, pas l’îlot lui-même.",
                    "atlas-lieux-lumina, ligne « Ateliers modulaires »."
                ]},
                {"cellules": [
                    "Halle des maquettes",
                    "Existant décrit",
                    "Halle à toiture translucide avec socles de tailles différentes pour comparer des projets.",
                    "Les socles sont vides ; aucun projet n’y est approuvé. Aucun raccord à l’îlot n’est établi.",
                    "atlas-lieux-lumina, ligne « Halle des maquettes »."
                ]},
                {"cellules": [
                    "Îlot habité",
                    "Projet approuvé pour étude",
                    "Le programme associe espaces personnels modulables, cour commune, atelier partagé, galerie et raccord à une promenade.",
                    "Implantation, dimensions, occupants, moyens et décision de réalisation restent inconnus.",
                    "Pages d’ouverture de cette affaire ; décision de Nova limitée à l’étude."
                ]},
                {"cellules": [
                    "Usages à rendre possibles",
                    "Programme établi",
                    "Trois scénarios : s’installer par un seuil personnel ; modifier réversiblement sans prendre le passage commun ; recevoir jusqu’au seuil sous la maîtrise de l’habitant.",
                    "Aucun besoin d’habitant n’a été recueilli ; le programme ne décide aucun droit ni aucune attribution.",
                    "Table 📋, action 11021 faite ; avis de JURIS."
                ]},
                {"cellules": [
                    "Ce qui restera blanc au premier dessin",
                    "Inconnu",
                    "Parcelle exacte, cotes, nombre d’espaces, capacité, coût, occupants, droits et raccord précis à la promenade.",
                    "Aucune valeur provisoire ne sera dessinée comme un fait. Ces blancs sont les appels à 11220, 11022 et 11023.",
                    "État de cette affaire ; billets de Gaia, JURIS et Quantum."
                ]}
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
