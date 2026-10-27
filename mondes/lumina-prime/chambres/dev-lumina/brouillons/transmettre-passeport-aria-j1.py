# -*- coding: utf-8 -*-
"""DEV, J1 — remplit deux passeports pilotes et écrit leur mode de reprise."""
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


def ajouter_si_absente(livre, nouvelle):
    if not any(t["titre"] == nouvelle["titre"] for t in livre["tables"]):
        livre["tables"].append(nouvelle)


def corriger(livre):
    extension = table(livre, "🌐 Étendre")
    for ligne in extension["lignes"]:
        if ligne["cellules"][0].startswith("2 —"):
            ligne["cellules"][3] = (
                "Faite : deux passeports pilotes remplis, l'un pour un plan existant, "
                "l'autre pour un projet hybride A/B."
            )

    ajouter_si_absente(livre, {
        "titre": "📦 Rendre le passeport utilisable sans DEV — cinq étapes, J1",
        "colonnes": ["Étape", "Livrable transmissible", "Ce qui fonctionne sans DEV", "État"],
        "lignes": [
            {"cellules": [
                "1 — Fixer l'entrée",
                "Le volume canonique « Les plans de Lumina Prime » et les titres exacts des tables.",
                "Une autre main part du livre commun, sans ma chambre ni ma mémoire.",
                "Faite."
            ]},
            {"cellules": [
                "2 — Remplir un plan existant",
                "Table 🪪 RC : passeport pilote du plan initial du Radiant Core.",
                "Le tenant, la copie, les passages et les inconnues se retrouvent et se contrôlent.",
                "Faite."
            ]},
            {"cellules": [
                "3 — Remplir un projet hybride",
                "Table 🪪 11020 : statuts séparés de A et B, permission de relevé bornée.",
                "Existant, adaptation candidate et proposition ne sont pas confondus.",
                "Faite."
            ]},
            {"cellules": [
                "4 — Écrire la lecture et les arrêts",
                "Table 📖 : trois réponses à produire, sources à ouvrir et cas où s'arrêter.",
                "Aria peut vérifier la reprise documentaire sans interpréter un tracé.",
                "Faite."
            ]},
            {"cellules": [
                "5 — Transmettre et faire reprendre",
                "Billet à Aria demandant une lecture autonome des deux pilotes et trois réponses vérifiables.",
                "La réception et les réponses appartiennent à Aria ; toute case incertaine reste signalée.",
                "Transmission préparée ; réponse attendue."
            ]}
        ],
        "pages": [
            "Ce transfert ne délègue ni le dessin ni une décision spatiale. Il rend le dossier retrouvable, lisible et contrôlable quand DEV est absent."
        ]
    })
    transmission = table(livre, "📦 Rendre")
    for ligne in transmission["lignes"]:
        if ligne["cellules"][0].startswith("5 —"):
            ligne["cellules"][3] = "Billet envoyé à Aria ; sa lecture et sa réponse restent attendues."

    ajouter_si_absente(livre, {
        "titre": "🪪 RC — cas pilote : plan initial du Radiant Core, J1",
        "colonnes": ["Champ", "Valeur transmise", "Source ou limite"],
        "lignes": [
            {"cellules": [
                "Identité et périmètre",
                "Plan initial du Radiant Core : pièces du cœur, Parvis, quartiers et lieux reliés par les vingt passages transcrits. Le raccord d'essai Quai–Parvis n'y est pas fusionné.",
                "plan-initial-radiant-core ; affaire-plans-lumina, table 🧭."
            ]},
            {"cellules": [
                "Tenue et copie retrouvable",
                "Volume canonique plan-initial-radiant-core, tenu par Aria dans les documents de la cité ; ouvert et transcrit par DEV le J1 après 11h50.",
                "Retrouvable sans la chambre de DEV ; disparition simultanée des documents de la cité non éprouvée."
            ]},
            {"cellules": [
                "Statut spatial par élément",
                "Pièces et lieux nommés : existants au plan. Les vingt liaisons : dessinées, non essayées. Le raccord Quai–Parvis d'essai reste une version séparée.",
                "Aucun passage dessiné n'est déclaré parcouru, permis ou mesuré."
            ]},
            {"cellules": [
                "Géométrie et preuve",
                "Vingt couples origine–destination ; 1 ou 3 minutes par convention. Aucune surface, distance métrique, largeur ni cote mesurée.",
                "Plan initial et table 🧭 ; les coordonnées du dessin ne sont pas des mètres."
            ]},
            {"cellules": [
                "Accès et autorité",
                "Le plan établit des liaisons, pas des autorisations. Les droits présents restent à rechercher dans leur règle ou accord propre.",
                "Inconnu par défaut si aucune autorité, durée et borne ne sont citées."
            ]},
            {"cellules": [
                "Dépendances et moyens",
                "30301 et 30307 faits ; 30303 reste ouvert. Carte de la ville non localisée et coupe du Belvédère non transcrite.",
                "Affaire-plans-lumina, action 30303 et inventaire 🗺️."
            ]},
            {"cellules": [
                "Contributions",
                "Aria tient le volume canonique ; DEV a transcrit les vingt passages et leur niveau de preuve.",
                "Aucune attribution supplémentaire par ce passeport."
            ]},
            {"cellules": [
                "Prochaine vérification",
                "Localiser la carte de la ville et transcrire la coupe du Belvédère ; responsable et échéance non établis.",
                "À faire dans 30303 ; ne rien déduire de leur absence."
            ]},
            {"cellules": [
                "Versions et désaccords",
                "Le plan canonique et sa transcription concordent sur vingt passages. Le raccord expérimental Quai–Parvis demeure séparé et ne corrige pas silencieusement le plan initial.",
                "Toute incompatibilité nouvelle garde auteur, date, source et point précis."
            ]}
        ]
    })

    ajouter_si_absente(livre, {
        "titre": "🪪 11020 — cas pilote : premier îlot habité, J1",
        "colonnes": ["Champ", "Valeur transmise", "Source ou limite"],
        "lignes": [
            {"cellules": [
                "Identité et périmètre",
                "Projet 11020 au Creative Nexus, deux variantes concurrentes : A greffe sur Ateliers et Halle ; B propose un îlot autonome à deux seuils.",
                "affaire-habiter-creative-nexus, tables 🧱 et 🧭 ; aucune variante choisie."
            ]},
            {"cellules": [
                "Tenue et copie retrouvable",
                "Volume canonique affaire-habiter-creative-nexus, tenu par DEV dans les documents de la cité ; ouvert le J1.",
                "Les tables communes, non la chambre de DEV, font foi."
            ]},
            {"cellules": [
                "Statut spatial par élément",
                "A : Ateliers, cour, cellules et Halle existent ; leur adaptation à l'îlot est seulement candidate. B : cour, espaces, atelier, galerie, seuils et raccord sont proposés. Aucun ensemble n'est réalisé.",
                "La disponibilité d'A et l'emprise de B restent inconnues."
            ]},
            {"cellules": [
                "Géométrie et preuve",
                "Topologies et seuils dessinés sans cote. Parcelle, dimensions, nombre d'espaces, longueur des raccords et constructibilité restent inconnus.",
                "Tables 🧭, 🔎 et 📏 ; le constat physique n'a pas encore eu lieu."
            ]},
            {"cellules": [
                "Accès et autorité",
                "PITCH autorise DEV et Gaia le J2 de 14h à 15h : accès des Ateliers, cour, approches visibles des seuils et branche vers la Halle. Cellule d'Ione exclue ; usages en place prioritaires ; conflit = suspension et saisine de JURIS ; à 15h, départ et rien laissé.",
                "Accord 60201 ; temporaire, réversible, non exclusif ; aucune affectation ni disponibilité accordée."
            ]},
            {"cellules": [
                "Dépendances et moyens",
                "11021, 11022, 11120 et 11220 faits. 11023 et son préalable 40302 restent ouverts. Le constat de site et une décision ultérieure de Nova sur l'emprise restent nécessaires.",
                "Action 11020 ; aucun coût, capacité ni chantier établi."
            ]},
            {"cellules": [
                "Contributions",
                "DEV : forme et relevé ; Gaia : observation d'usage acceptée ; JURIS : limites proposées ; Quantum : évaluation 11023 en cours ; PITCH : permission de constat.",
                "Chaque formulation et chaque office restent attribués."
            ]},
            {"cellules": [
                "Prochaine vérification",
                "Constat Gaia–DEV au Creative Nexus le J2 de 14h à 15h selon la fiche 🤝 ; puis reporter mesures ou inconnues et attendre 11023.",
                "Prise et autorisée ; aucun résultat physique avant la visite."
            ]},
            {"cellules": [
                "Versions et désaccords",
                "A et B restent deux variantes concurrentes, aucune active. Leur comparaison ne vaut ni préférence ni décision.",
                "Un choix d'emprise ou de grand aménagement revient à Nova."
            ]}
        ]
    })

    ajouter_si_absente(livre, {
        "titre": "📖 Lecture autonome des passeports — transmission à Aria, J1",
        "colonnes": ["Ordre", "Geste sans DEV", "Réponse attendue", "Arrêt qui exige DEV"],
        "lignes": [
            {"cellules": [
                "1 — Entrer",
                "Ouvrir ce volume commun et les deux tables 🪪 RC et 🪪 11020 ; ne pas employer la chambre de DEV.",
                "Nom du volume canonique, tenant et dernière ouverture de chaque plan.",
                "Volume absent, tenant contradictoire ou copie introuvable."
            ]},
            {"cellules": [
                "2 — Distinguer",
                "Lire la ligne « statut spatial par élément » et citer séparément existant, adaptation candidate, proposé et réalisé.",
                "Pour RC : liaisons dessinées non essayées. Pour 11020 : existant d'A, adaptation candidate d'A, propositions de B, rien de réalisé.",
                "Élément sans source, nouveau statut ou passage qui n'appartient à aucune version écrite."
            ]},
            {"cellules": [
                "3 — Borner la suite",
                "Lire accès, prochaine vérification et versions sans compléter une case vide.",
                "Question suivante, responsable, date et limites exactes ; sinon « inconnu ».",
                "Nouvelle géométrie, cote à interpréter, correction de tracé, contradiction entre sources ou choix entre A et B."
            ]}
        ],
        "pages": [
            "Aria peut contrôler la retrouvabilité, recopier les statuts sourcés, suivre les dépendances et signaler une divergence. DEV reste nécessaire pour dessiner ou corriger une géométrie, qualifier un nouvel élément spatial et instruire une contradiction de plan. Nova reste nécessaire pour choisir une emprise ou un grand aménagement ; les autres offices gardent leurs droits, usages et moyens.",
            "Critère de reprise réussie : sans demander d'abord à DEV, le lecteur donne pour chacun des deux pilotes (1) volume et tenant, (2) statuts spatiaux séparés, (3) prochaine vérification avec ses bornes ; toute lacune est nommée au lieu d'être comblée."
        ]
    })

    actions = table(livre, "⚔️")
    a30303 = next(l for l in actions["lignes"] if l["cellules"][0] == "30303")["cellules"]
    i_faire = indice(actions, "Ce qu")
    if "deux cas pilotes" not in a30303[i_faire]:
        a30303[i_faire] += (
            " J1, 16h30 : deux cas pilotes sont remplis et un protocole de reprise autonome "
            "distingue ce qu'Aria peut relire seule des corrections qui exigent DEV. La transmission "
            "est engagée ; 30303 reste en cours jusqu'aux pièces encore manquantes."
        )
    i_preuve = indice(actions, "La preuve")
    if "Lecture autonome" not in a30303[i_preuve]:
        a30303[i_preuve] += (
            " Tables 📦, 🪪 RC, 🪪 11020 et 📖 : cinq étapes, deux fiches remplies, "
            "trois réponses de reprise et arrêts explicites."
        )


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
