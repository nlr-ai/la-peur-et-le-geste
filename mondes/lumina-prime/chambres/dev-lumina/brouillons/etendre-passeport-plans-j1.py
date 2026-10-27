# -*- coding: utf-8 -*-
"""DEV, J1 — étend la méthode de 11020 en passeport commun des plans.

Étape 1 seulement : créer la trame. Aucun plan n'est déclaré complet,
aucun accès n'est autorisé et aucune mesure n'est ajoutée.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE_ETAPES = "🌐 Étendre la portée des plans en cinq étapes — J1"
TITRE_PASSEPORT = "🪪 Passeport commun d’un plan — étape 1, J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a30303 = next(l for l in actions["lignes"] if l["cellules"][0] == "30303")["cellules"]
    i_faire = indice(actions, "Ce qu")
    ajout = (
        " J1, 15h50 : la portée de l'inventaire est étendue par un passeport commun 🪪. "
        "Sa trame sépare identité, copie vérifiée, géométrie, accès, dépendances et prochaine vérification. "
        "L'étape 1 est faite ; aucun plan supplémentaire n'est encore renseigné."
    )
    if "passeport commun" not in a30303[i_faire]:
        a30303[i_faire] += ajout
    i_preuve = indice(actions, "La preuve")
    if "passeport 🪪" not in a30303[i_preuve]:
        a30303[i_preuve] += (
            " Trame du passeport 🪪 présente dans ce volume ; chaque champ distingue vérifié, "
            "convention, proposition et inconnu."
        )

    if not any(t["titre"] == TITRE_ETAPES for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_ETAPES,
            "colonnes": ["Étape", "Portée gagnée", "Livrable", "État J1"],
            "lignes": [
                {"cellules": [
                    "1 — Définir un passeport commun",
                    "Tout plan peut être lu avec les mêmes distinctions, quel que soit son quartier ou son auteur.",
                    "Trame 🪪 : identité, copie, statut spatial, accès, dépendances, contributeurs et vérification.",
                    "Engagée et faite : trame écrite, aucune fiche encore remplie."
                ]},
                {"cellules": [
                    "2 — Renseigner deux cas pilotes",
                    "Éprouver la trame sur un plan existant et un projet sans confondre leurs statuts.",
                    "Passeports du Radiant Core et de l'îlot 11020.",
                    "À faire ; les sources existent, mais les champs doivent être reportés ligne par ligne."
                ]},
                {"cellules": [
                    "3 — Étendre aux six lieux de l'atlas",
                    "Faire de 30302 et 30303 un inventaire spatial cohérent à l'échelle de la cité.",
                    "Six passeports indiquant source, emplacement documentaire et inconnues de relevé.",
                    "À faire après les cas pilotes."
                ]},
                {"cellules": [
                    "4 — Ouvrir les annotations par office",
                    "Aria vérifie la tenue, Quantum les mesures, Gaia les parcours, PITCH les usages et JURIS les droits, sans réécrire le plan de DEV.",
                    "Colonnes d'annotations datées et attribuées, avec désaccords conservés.",
                    "À proposer aux offices après validation de la trame sur deux cas."
                ]},
                {"cellules": [
                    "5 — Soumettre la règle de tenue à Nova",
                    "Un grand aménagement peut être décidé sur des pièces retrouvables, comparables et explicitement incomplètes.",
                    "Proposition de règle municipale et ordre de priorité des relevés.",
                    "À soumettre seulement après retour des cas pilotes."
                ]}
            ],
            "pages": [
                "La première étape ouvre toutes les suivantes : sans vocabulaire commun, chaque extension multiplie les plans mais pas la confiance qu'on peut leur accorder."
            ]
        })

    if not any(t["titre"] == TITRE_PASSEPORT for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_PASSEPORT,
            "colonnes": [
                "Champ commun",
                "Ce qu’on inscrit",
                "Valeurs admises",
                "Pourquoi il ouvre le travail des autres"
            ],
            "lignes": [
                {"cellules": [
                    "Identité et périmètre",
                    "Identifiant stable, nom, quartier, espaces inclus et exclus.",
                    "Vérifié dans une source ; sinon inconnu.",
                    "Empêche deux offices d'annoter des objets différents sous le même nom."
                ]},
                {"cellules": [
                    "Tenue et copie retrouvable",
                    "Volume canonique, tenant, emplacement vérifié de la copie et date de la dernière ouverture.",
                    "Vérifié / déclaré non ouvert / introuvable / inconnu.",
                    "Permet de retrouver le plan hors d'une chambre et de savoir qui peut le mettre à jour."
                ]},
                {"cellules": [
                    "Statut spatial",
                    "Pour chaque élément : existant, candidat à l'adaptation, proposé ou réalisé.",
                    "Un seul statut sourcé par élément ; aucune proposition n'est présentée comme existante.",
                    "DEV, Gaia et Nova peuvent distinguer constat, option et décision."
                ]},
                {"cellules": [
                    "Géométrie et niveau de preuve",
                    "Nœuds, seuils, segments, cote, unité, outil, date et source.",
                    "Mesuré / convention / dessiné non essayé / inconnu.",
                    "Quantum sait quelles grandeurs rapprocher ; une convention ne devient pas une mesure."
                ]},
                {"cellules": [
                    "Accès et autorité",
                    "Accès matériel ou conventionnel distinct de l'autorisation ; autorité qui peut l'accorder et preuve de son accord.",
                    "Accessible et autorisé / accessible sous condition / accès non vérifié / inconnu.",
                    "Évite qu'une liaison dessinée soit prise pour un droit ; répond au cas du relevé Gaia–DEV."
                ]},
                {"cellules": [
                    "Dépendances et moyens",
                    "Affaires, mesures, droits, composants et décisions nécessaires avant usage ou chantier.",
                    "Adresses stables ; chaque absence reste inconnue et non nulle.",
                    "Rend visibles les blocages sans recopier le travail d'un autre office."
                ]},
                {"cellules": [
                    "Contributions",
                    "Auteur, office, objet précis de l'annotation, date et formulation conservée.",
                    "Proposée / acceptée / remise / contestée.",
                    "Plusieurs offices peuvent enrichir un même plan sans perdre la main de chacun."
                ]},
                {"cellules": [
                    "Prochaine vérification",
                    "Question exacte, source ou lieu à consulter, responsable pressenti et échéance si acceptée.",
                    "À faire / prise / faite / bloquée avec cause.",
                    "Transforme un blanc en prochain geste sans fabriquer sa réponse."
                ]}
            ],
            "pages": [
                "Cette table est une trame, pas encore un registre rempli. Elle étend à tous les plans la discipline éprouvée sur 11020 : séparer ce qui existe, ce qui est proposé, ce qui est mesuré et ce qui reste blanc.",
                "Premier test prévu : Radiant Core comme plan existant et îlot 11020 comme projet. Leur différence doit rester lisible dans chaque champ."
            ]
        })


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
