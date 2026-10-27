# -*- coding: utf-8 -*-
"""DEV, J1, deuxième élan de vingt minutes. De ma main, pour 11020.

Ajoute deux topologies comparables, sans cote ni géométrie, et leur tableau de
comparaison. Ne choisit aucune variante et ne ferme pas 11020.
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
    a11020[indice(actions, "Ce qu")]= (
        "Étapes 1 et 2 faites le J1 : le socle vérifié est écrit en 🧱 ; deux topologies sans cote sont écrites en 🧭 et comparées en ⚖️. A greffe l'îlot sur les Ateliers et la Halle existants ; B propose un îlot autonome avec seuil commun et seuil public distincts. Aucune variante n'est retenue. Prochaine étape : éprouver les trois scénarios de 11021 dans les deux cartes."
    )
    a11020[indice(actions, "La preuve")] = (
        "Tables 🧱, 🧭 et ⚖️ : existant et proposé séparés, nœuds et seuils nommés, aucune cote non mesurée, choix laissé ouvert."
    )

    if not any(t["titre"].startswith("🧭 Deux topologies") for t in livre["tables"]):
        livre["tables"].append({
            "titre": "🧭 Deux topologies comparables pour 11020 — étape 2, J1",
            "colonnes": ["Nœud ou raccord", "A — Greffe sur l’existant", "B — Îlot autonome à deux seuils", "Statut et inconnue"],
            "lignes": [
                {"cellules": [
                    "Raccord au Creative Nexus",
                    "Le nœud public du quartier dessert séparément les Ateliers modulaires et la Halle des maquettes, comme au plan initial.",
                    "Le nœud public du quartier dessert deux seuils proposés distincts : seuil commun de l’îlot et seuil public de la galerie.",
                    "Le quartier, les Ateliers et la Halle existent ; emplacement et longueur de tout nouveau raccord restent inconnus."
                ]},
                {"cellules": [
                    "Cour commune",
                    "La cour existante des Ateliers devient candidate à l’adaptation : elle distribue les cellules personnelles candidates et l’atelier partagé.",
                    "Une cour nouvelle distribue les espaces personnels et l’atelier partagé depuis le seuil commun.",
                    "Aucun usage nouveau de la cour existante n’est décidé ; la cour B est entièrement proposée. Gaia doit distinguer passage, séjour et retrait (11220)."
                ]},
                {"cellules": [
                    "Espaces personnels",
                    "Des cellules existantes autour de la cour sont candidates à l’adaptation ; chacune conserve un seuil propre donnant sur la cour, sans traverser une autre cellule.",
                    "Des espaces nouveaux bordent la cour proposée ; chacun n’a qu’un seuil personnel sur le parcours partagé.",
                    "Nombre, dimensions, occupants et transformations admises sont inconnus. Aucun espace n’est attribué."
                ]},
                {"cellules": [
                    "Atelier partagé",
                    "Au moins une cellule existante reste candidate comme atelier partagé, ouverte sur la cour ; le rail de cloisons est un précédent de séparation à étudier.",
                    "Un atelier nouveau ouvre sur la cour et possède un raccord de service contrôlé vers la galerie, sans traverser un espace personnel.",
                    "Capacité et garanties techniques inconnues ; Quantum les évalue après l’esquisse (11023)."
                ]},
                {"cellules": [
                    "Galerie",
                    "La Halle des maquettes reste candidate comme galerie publique, atteinte depuis le nœud public du quartier sans passer par la cour ni les cellules.",
                    "Une galerie nouvelle possède son propre seuil public depuis le quartier ; elle ne donne pas sur les espaces personnels.",
                    "L’adaptation de la Halle comme galerie de l’îlot n’est pas décidée ; la galerie B est une construction proposée."
                ]},
                {"cellules": [
                    "Limites à gouverner",
                    "Quartier ↔ cour adaptée ; cour ↔ seuils personnels ; cour ↔ atelier ; quartier ↔ Halle.",
                    "Quartier ↔ cour ; cour ↔ seuils personnels ; cour ↔ atelier ; quartier ↔ galerie ; atelier ↔ galerie par raccord de service.",
                    "JURIS doit dire qui franchit chaque limite et qui en décide (11022). Tous les raccords nouveaux sont proposés, non essayés."
                ]},
                {"cellules": [
                    "Retour et sortie",
                    "Chaque espace revient à la cour ; la sortie rejoint le nœud public par l’accès des Ateliers. La galerie sort directement vers le quartier.",
                    "Chaque espace revient à la cour puis au seuil commun ; la galerie sort directement par son seuil public.",
                    "Lisibilité et praticabilité ne sont pas éprouvées. L’étape 3 y fera passer les trois scénarios de 11021."
                ]}
            ]
        })

    if not any(t["titre"].startswith("⚖️ Comparaison des topologies") for t in livre["tables"]):
        livre["tables"].append({
            "titre": "⚖️ Comparaison des topologies 11020 — aucun choix arrêté",
            "colonnes": ["Critère", "A — Greffe", "B — Autonome", "Ce qui départagera"],
            "lignes": [
                {"cellules": [
                    "Part d’existant",
                    "Réemploie potentiellement cour, cellules, accès indépendants, rail et Halle.",
                    "Tous les espaces et raccords de l’îlot sont proposés.",
                    "Relevé de l’existant, disponibilité réelle, mesures et décision d’usage."
                ]},
                {"cellules": [
                    "Séparation public / personnel",
                    "La galerie reste hors de la cour ; le public n’entre pas dans le parcours des seuils personnels.",
                    "Deux seuils du quartier séparent la galerie publique de la cour commune.",
                    "Passage des scénarios 11021 ; droits 11022 ; annotation de Gaia 11220."
                ]},
                {"cellules": [
                    "Transformation",
                    "Risque de changer des cellules et une cour aujourd’hui vouées au travail.",
                    "Risque de construire davantage et de créer de nouveaux raccords.",
                    "Capacités et coûts 11023 ; arbitrage de Nova après le dossier 11024."
                ]},
                {"cellules": [
                    "Position de DEV",
                    "Variante à éprouver, non préférée à ce stade.",
                    "Variante à éprouver, non préférée à ce stade.",
                    "Aucun choix avant les étapes 3 et 4."
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
