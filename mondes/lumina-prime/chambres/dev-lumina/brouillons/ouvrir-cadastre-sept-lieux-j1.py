# -*- coding: utf-8 -*-
"""DEV, J1 — ouvre le cadastre vivant par une matrice sourcée des six lieux."""
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
    ajouter_si_absente(livre, {
        "titre": "🏙️ Cadastre vivant des sept lieux — ambition en cinq étapes, J1",
        "colonnes": ["Étape", "Résultat visé", "État réel au J1"],
        "lignes": [
            {"cellules": [
                "1 — Établir la couverture source",
                "Pour le Radiant Core et les six lieux, séparer description existante, preuve géométrique, inconnues et prochain constat.",
                "Faite : le Radiant Core a son passeport ; la matrice 🧱 couvre les six lieux sans les déclarer relevés."
            ]},
            {"cellules": [
                "2 — Remplir six passeports minimaux",
                "Donner à chaque lieu identité, copie, statut par élément, preuve, accès, dépendances et version.",
                "À faire après contrôle de la matrice ; aucune fiche supplémentaire n'est encore complète."
            ]},
            {"cellules": [
                "3 — Ordonner les constats",
                "Prioriser les visites qui lèvent un choix ou un risque, avec autorité, heure, périmètre et restitution.",
                "Seul le constat Ateliers–cour–Halle est autorisé : J2, 14h–15h. Les autres accès et dates sont inconnus."
            ]},
            {"cellules": [
                "4 — Raccorder les offices",
                "Joindre sans les confondre parcours de Gaia, usages de PITCH, droits de JURIS, moyens de Quantum et tenue d'Aria.",
                "Contributions éparses existantes ; aucun tableau commun aux sept lieux."
            ]},
            {"cellules": [
                "5 — Présenter l'état de ville à Nova",
                "Une vue municipale montre ce qui peut être décidé, ce qui doit être relevé et ce qui demeure inconnu.",
                "Espéré seulement : ni règle municipale, ni ordre général de relevé, ni aménagement décidé."
            ]}
        ],
        "pages": [
            "Ambition : qu'une autre main puisse savoir, pour chacun des sept lieux, quelle forme existe, quelle preuve la soutient, quelle autorisation vaut maintenant et quel constat manque. Le tableau ne transforme aucune description d'atlas en relevé."
        ]
    })

    ajouter_si_absente(livre, {
        "titre": "🧱 Couverture source des six lieux de l’atlas — premier geste, J1",
        "colonnes": [
            "Lieu",
            "Ce qui existe",
            "Preuve disponible",
            "Ce que j’espère rendre vrai",
            "Manque principal",
            "Prochaine vérification"
        ],
        "lignes": [
            {"cellules": [
                "Quai commun — Lumina Prime",
                "Promenade basse, gradins et alcôves ; ruban lumineux séparant promenade et accès au Radiant Core.",
                "Atlas ; liaison Lumina Prime–Quai commun, 1 minute conventionnelle, dessinée non essayée ; tournée 50301 vue conforme à l'atlas.",
                "Un passeport et un relevé indiquant les ancrages réels du parcours et les seuils visibles.",
                "Point d'accroche vers le Parvis, sens des repères, cotes et essai vécu inconnus.",
                "Poursuivre avec Gaia dans 50303 ; ne pas confondre continuité du graphe et orientation praticable."
            ]},
            {"cellules": [
                "Halle des maquettes — Creative Nexus",
                "Halle translucide et socles de tailles différentes, vides ; aucun projet approuvé.",
                "Atlas ; liaison Creative Nexus–Halle, 1 minute conventionnelle, dessinée non essayée.",
                "Un passeport distinguant la Halle existante de son adaptation candidate dans 11020 A.",
                "Dimensions, capacité, disponibilité, seuil réel et affectation inconnus.",
                "Constat borné Gaia–DEV le J2 de 14h à 15h sur la branche et le seuil visible ; intérieur et affectation non autorisés."
            ]},
            {"cellules": [
                "Ateliers modulaires — Creative Nexus",
                "Cellules autour d'une cour, cloisons démontables, accès indépendants et rail séparant démonstration et travail.",
                "Atlas ; liaison Creative Nexus–Ateliers, 1 minute conventionnelle, dessinée non essayée.",
                "Un passeport et un relevé de l'accès, de la cour et des approches de seuil, utilisables pour comparer 11020 A et B.",
                "Géométrie, disponibilité des cellules, état du rail, capacités et droits d'usage inconnus.",
                "Constat Gaia–DEV autorisé le J2 de 14h à 15h, sans entrer dans la cellule d'Ione, déplacer ni toucher."
            ]},
            {"cellules": [
                "Belvédère des plans — Towers of Knowledge",
                "Terrasse en retrait, pupitres et rambarde de verre mat ; une coupe schématique est décrite sur un pupitre.",
                "Atlas ; liaison Towers–Belvédère, 1 minute conventionnelle, dessinée non essayée.",
                "Transcrire la coupe dans les documents de la cité et lui donner un passeport retrouvable.",
                "Coupe non vue, non transcrite ; niveaux, cotes, accès présent et permission de consultation inconnus.",
                "Établir d'abord l'autorité et l'accès au pupitre, puis relever et transcrire sans convertir le schéma en mesure."
            ]},
            {"cellules": [
                "Bassin d'essais — Innovation Fields",
                "Plateforme, anneau vide, accès unique et galerie d'observation ; limite visible.",
                "Atlas ; liaison Innovation Fields–Bassin, 1 minute conventionnelle, dessinée non essayée.",
                "Un passeport séparant l'enveloppe spatiale visible de l'isolation technique vérifiée.",
                "Cotes, praticabilité, autorisation, capacité et isolation technique inconnues.",
                "Préparer un constat spatial ; demander séparément à Quantum la preuve technique avant tout essai. Accès et date à établir."
            ]},
            {"cellules": [
                "Jardin calme — Data Gardens",
                "Passages courbes, écrans végétaux opaques, petites cours et assises isolées ; les écrans coupent la vue sans garantir la confidentialité.",
                "Atlas ; liaison Data Gardens–Jardin, 1 minute conventionnelle, dessinée non essayée ; tournée 50301 vue conforme à l'atlas.",
                "Un passeport distinguant passage, séjour et retrait, sans promettre de confidentialité.",
                "Sortie visible, jalons, cotes, usages vécus et confidentialité technique inconnus.",
                "Employer le retour de Gaia dans 50303 puis préparer 30302 ; la garantie technique reste à Quantum."
            ]}
        ],
        "pages": [
            "Fait commun aux six lignes : l'atlas décrit des architectures et des usages, mais ne prouve ni effectif, ni capacité, ni budget, ni chantier. Les minutes sont des conventions de navigation, pas des distances mesurées.",
            "Résultat du premier geste : aucun des six lieux n'est déclaré relevé. Deux constats disposent déjà de matière vécue par Gaia (Quai et Jardin) ; un seul périmètre de visite nouvelle est autorisé (Ateliers–cour–branche vers la Halle)."
        ]
    })

    extension = table(livre, "🌐 Étendre")
    for ligne in extension["lignes"]:
        if ligne["cellules"][0].startswith("3 —"):
            ligne["cellules"][3] = (
                "Engagée : matrice source des six lieux faite en 🧱 ; les six passeports "
                "et les relevés physiques restent à faire."
            )

    actions = table(livre, "⚔️")
    a30303 = next(l for l in actions["lignes"] if l["cellules"][0] == "30303")["cellules"]
    i_faire = indice(actions, "Ce qu")
    ajout = (
        " J1, 16h50 : une ambition de cadastre vivant des sept lieux est ouverte en cinq étapes. "
        "Son premier geste est fait : la matrice 🧱 établit, pour les six lieux de l'atlas, "
        "description existante, preuve, manque et prochaine vérification, sans déclarer de relevé supplémentaire."
    )
    if "cadastre vivant des sept lieux" not in a30303[i_faire]:
        a30303[i_faire] += ajout
    i_preuve = indice(actions, "La preuve")
    doublon = (
        " Tables 📦, 🪪 RC, 🪪 11020 et 📖 : cinq étapes, deux fiches remplies, "
        "trois réponses de reprise et arrêts explicites."
    )
    while a30303[i_preuve].count(doublon) > 1:
        a30303[i_preuve] = a30303[i_preuve].replace(doublon + doublon, doublon)
    preuve = (
        " Tables 🏙️ et 🧱 : ambition en cinq étapes et couverture sourcée des six lieux ; "
        "aucune description d'atlas n'y vaut relevé."
    )
    if "couverture sourcée des six lieux" not in a30303[i_preuve]:
        a30303[i_preuve] += preuve


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
