# -*- coding: utf-8 -*-
"""DEV, J1 — cinq voies contre l'obstacle de site de 11020, audit essayé.

Le test relit les documents disponibles. Il ne vaut ni visite, ni mesure,
ni affectation, ni décision de variante.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE_VOIES = "🛠️ Cinq voies pour obtenir un site recevable — 11020, J1"
TITRE_TEST = "🧪 Épreuve immédiate : audit documentaire du site — 11020, J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a11020 = next(l for l in actions["lignes"] if l["cellules"][0] == "11020")["cellules"]
    marque = (
        " Cinq voies de dépassement sont comparées en 🛠️. L'audit documentaire, seul essai "
        "immédiat sans décision ni déplacement, est fait en 🧪 : aucun document ne prouve un site "
        "recevable. Le prochain fait nécessaire est donc un constat de site, puis une affectation de Nova."
    )
    i_faire = indice(actions, "Ce qu")
    if "Cinq voies de dépassement" not in a11020[i_faire]:
        a11020[i_faire] += marque
    i_preuve = indice(actions, "La preuve")
    if "🛠️ et 🧪" not in a11020[i_preuve]:
        a11020[i_preuve] += (
            " Tables 🛠️ et 🧪 : cinq voies comparées, audit sourcé et résultat négatif conservé "
            "sans convertir l'absence de preuve en indisponibilité."
        )

    if not any(t["titre"] == TITRE_VOIES for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_VOIES,
            "colonnes": ["Voie", "Ce qu'elle pourrait établir", "Peut être essayée maintenant ?", "Limite"],
            "lignes": [
                {"cellules": [
                    "1 — Relevé sur place des Ateliers et de la Halle",
                    "Emprise, seuils, géométrie, éléments transformables et état visible de A.",
                    "Non depuis l'atelier des plans : il faut se rendre au Creative Nexus et relever avec une unité et une date.",
                    "Ne décide ni disponibilité ni affectation ; ne donne pas à lui seul un site pour B."
                ]},
                {"cellules": [
                    "2 — Décision de Nova sur les emprises candidates",
                    "Disponibilité et affectation de l'existant pour A ; emprise candidate pour B.",
                    "Une demande peut être préparée maintenant, mais la réponse appartient à Nova.",
                    "Une affectation sans relevé ne donne aucune cote ni garantie technique."
                ]},
                {"cellules": [
                    "3 — Audit croisé des documents existants",
                    "Découvrir une pièce déjà tenue qui établirait site, disponibilité ou géométrie.",
                    "Oui : atlas, plan initial, affaire des plans, projets de quartiers et affaire 11020 sont lisibles maintenant.",
                    "Un document schématique ou une piste ne devient ni mesure ni décision."
                ]},
                {"cellules": [
                    "4 — Maquette réversible des deux emprises",
                    "Éprouver l'ordre des espaces et rendre les écarts visibles à Nova.",
                    "Une maquette non cotée peut être dessinée, mais les topologies A/B remplissent déjà cette fonction.",
                    "Répéter la forme ne prouve ni site, ni disponibilité, ni passage réel."
                ]},
                {"cellules": [
                    "5 — Attendre 40302 et le résultat 11023",
                    "Capacités et marges techniques mesurées dans les unités disponibles.",
                    "Non immédiatement : 40302 est dû au J2 et tenu par Quantum.",
                    "Les capacités de la cité ne situent pas une parcelle et ne rendent pas l'existant disponible."
                ]}
            ],
            "pages": [
                "Voie choisie pour l'épreuve immédiate : 3. Elle est la seule qui puisse produire maintenant un fait sur le site sans inventer une visite, une mesure ou une décision d'autrui."
            ]
        })

    if not any(t["titre"] == TITRE_TEST for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_TEST,
            "colonnes": ["Source relue", "Ce qu'elle établit", "Ce qu'elle n'établit pas", "Verdict pour le site"],
            "lignes": [
                {"cellules": [
                    "Atlas des six lieux",
                    "Ateliers : cellules autour d'une cour, cloisons démontables, accès indépendants. Halle : toiture translucide et socles de tailles différentes.",
                    "Aucune emprise cotée, disponibilité de cellule, affectation à l'îlot ni parcelle nouvelle.",
                    "Existence et qualités spatiales seulement ; A reste candidate et B non située."
                ]},
                {"cellules": [
                    "Plan initial du Radiant Core et des quartiers",
                    "Le nœud du Creative Nexus dessert conventionnellement Ateliers et Halle sur deux branches distinctes.",
                    "Les accès conventionnels ne donnent ni parcelle, ni longueur mesurée, ni disponibilité.",
                    "Topologie confirmée, site non établi."
                ]},
                {"cellules": [
                    "Affaire Les plans de Lumina Prime",
                    "Les tracés sont schématiques ; les coordonnées ne sont pas des mètres ; aucune surface ni distance n'est mesurée.",
                    "La carte de la ville n'est pas localisée et la coupe du Belvédère n'est pas transcrite.",
                    "Aucune cote recevable pour 11020."
                ]},
                {"cellules": [
                    "Trois projets pour les quartiers",
                    "Une piste d'atelier témoin, de galerie et de zone de travail séparée existe.",
                    "Ces pistes ne sont ni décisions de Nova, ni demandes, ni réalisations.",
                    "Programme utile, aucune emprise."
                ]},
                {"cellules": [
                    "Affaire Habiter le Creative Nexus",
                    "Les variantes, scénarios, seuils, droits proposés et le bon de relevé sont écrits.",
                    "Elle marque explicitement parcelle, géométrie, disponibilité, cotes et raccords comme inconnus.",
                    "L'audit ne trouve aucun site recevable dans les documents tenus."
                ]}
            ],
            "pages": [
                "Résultat de l'épreuve : la voie documentaire ne dépasse pas l'obstacle. Elle établit en revanche qu'aucun choix ne peut être justifié par une pièce déjà tenue.",
                "Conséquence : passer à la combinaison 1 puis 2 — constat daté au Creative Nexus, ensuite décision de Nova sur les emprises candidates. Absence de preuve ne signifie pas indisponibilité : le statut reste inconnu."
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
