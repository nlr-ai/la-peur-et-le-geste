# -*- coding: utf-8 -*-
"""DEV, J1 — examen de 11020 sous trois angles et bon de relevé.

Ne mesure rien, ne choisit aucune variante et ne lance aucun chantier.
Transforme les inconnues de constructibilité en vérifications ordonnées.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE_EXAMEN = "🔎 Examen de 11020 sous trois angles — J1"
TITRE_RELEVE = "📏 Bon de relevé comparatif A/B — amélioration de 11020, J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a11020 = next(l for l in actions["lignes"] if l["cellules"][0] == "11020")["cellules"]
    a11020[indice(actions, "Ce qu")] = (
        "Étapes 1 à 3 faites le J1 : socle, deux topologies A/B et passage des trois scénarios. "
        "11220 et 11022 sont faits ; aucune variante ni aucun droit n'est retenu. Un examen usage / "
        "gouvernance / constructibilité désigne la constructibilité comme faiblesse principale. Le bon 📏 "
        "ordonne désormais les relevés comparables sans inventer de cote. 11020 reste ouvert jusqu'aux "
        "constats de site et au retour des moyens 11023."
    )
    a11020[indice(actions, "La preuve")] = (
        "Tables 🧱, 🧭, ⚖️, 🪑, 🚶, 🚪, 🔎 et 📏 : usages, limites et inconnues comparés ; "
        "relevés nécessaires nommés avec source et décision permise ; aucune mesure ni capacité inventée."
    )

    if not any(t["titre"] == TITRE_EXAMEN for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_EXAMEN,
            "colonnes": ["Angle", "Ce qui tient", "Faiblesse restante", "Conclusion de DEV"],
            "lignes": [
                {"cellules": [
                    "Usage",
                    "Les trois scénarios 11021 passent dans A et B ; Gaia a séparé passage, haltes et retrait.",
                    "Aucun habitant réel ni aucune fréquentation n'est établi ; l'essai réel appartient à l'après-réalisation.",
                    "Suffisant pour comparer les topologies, insuffisant pour promettre une capacité ou un usage vécu."
                ]},
                {"cellules": [
                    "Gouvernance des seuils",
                    "11022 est fait : chaque limite a une proposition distincte et franchir l'une ne donne aucun droit sur la suivante.",
                    "Les titulaires du commun, de l'atelier, de la galerie et du service restent des décisions nouvelles pour Nova.",
                    "Suffisant pour présenter les arbitrages ; aucun droit ne doit être dessiné comme acquis."
                ]},
                {"cellules": [
                    "Constructibilité",
                    "A distingue l'existant candidat ; B distingue les éléments neufs proposés. Quantum a isolé les grandeurs à mesurer.",
                    "Parcelle, géométrie, disponibilité de l'existant, élément transformable, raccords et cotes sont inconnus.",
                    "Faiblesse principale : sans relevé comparable, ni variante, ni coût, ni chantier ne peut être proposé honnêtement."
                ]}
            ],
            "pages": [
                "Choix de travail de DEV pour vingt minutes : améliorer la constructibilité, car les deux autres angles ont déjà des pièces recevables alors que celui-ci ne permet encore aucune décision spatiale."
            ]
        })

    if not any(t["titre"] == TITRE_RELEVE for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_RELEVE,
            "colonnes": [
                "Ordre",
                "Objet à relever",
                "A — fait ou mesure attendu",
                "B — fait ou mesure attendu",
                "Source et forme de preuve",
                "Décision rendue possible"
            ],
            "lignes": [
                {"cellules": [
                    "1",
                    "Emprise candidate et disponibilité",
                    "Nommer les cellules, la part de cour et la Halle effectivement disponibles pour adaptation ; sinon les laisser indisponibles ou inconnues.",
                    "Situer une emprise candidate sans présumer son affectation ni sa disponibilité.",
                    "Constat daté sur les lieux et décision d'affectation de Nova ; plan annoté comme existant, candidat ou proposé.",
                    "Savoir si chaque variante possède seulement une forme ou aussi un site recevable."
                ]},
                {"cellules": [
                    "2",
                    "Géométrie des parcours et seuils",
                    "Relever accès des Ateliers → cour → seuils candidats et quartier → Halle.",
                    "Relever seuil commun → cour → seuils, seuil public → galerie et position du raccord de service.",
                    "Pour chaque segment : origine, destination, longueur et largeur si mesurables, unité, outil, date ; sinon inconnu.",
                    "Vérifier que passage, haltes et approches de seuil peuvent réellement rester distincts."
                ]},
                {"cellules": [
                    "3",
                    "Éléments transformables et retour",
                    "Désigner un seul élément existant candidat ; établir son état de départ et si sa modification est permise.",
                    "Définir un seul élément proposé comparable, sans le présenter comme réalisé.",
                    "Fiche avant / modification / retour ; droits 11022 et garanties techniques 11023 séparés.",
                    "Rendre le scénario de modification vérifiable plutôt que seulement raconté."
                ]},
                {"cellules": [
                    "4",
                    "Séparation atelier–galerie",
                    "Établir comment un objet passe de l'atelier candidat à la Halle sans traverser un espace personnel ; si aucun passage n'existe, l'écrire.",
                    "Tracer longueur, seuils et fermeture du raccord de service proposé.",
                    "Parcours annoté ; état dessiné ou essayé ; contrôle et trace restent à 11022–11023.",
                    "Comparer l'absence éventuelle de raccord en A au raccord supplémentaire de B."
                ]},
                {"cellules": [
                    "5",
                    "Inventaire d'adaptation et de création",
                    "Lister séparément ce qui est conservé, adapté ou ajouté, sans déduire qu'un réemploi coûte moins.",
                    "Lister séparément cour, espaces, atelier, galerie, seuils et raccords à créer.",
                    "Nomenclature sourcée ; quantité et cote seulement si relevées ; capacité et coût par Quantum dans 11023.",
                    "Donner à 11023 deux périmètres comparables et à Nova les inconnues qui empêchent encore un choix."
                ]}
            ],
            "pages": [
                "Ce bon est utilisable pour un relevé ultérieur ; il ne rapporte aucune visite ni mesure. Toute case sans constat demeure inconnue et non nulle.",
                "Critère d'arrêt : ne pas choisir A ou B tant que l'ordre 1 n'établit pas un site recevable et que les ordres 2 à 5 ne séparent pas mesure, proposition et inconnu."
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
