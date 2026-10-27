# -*- coding: utf-8 -*-
"""DEV, J1 — inscrit la livraison v0.1 de la tranche 2D dans 30303."""
import hashlib
import pathlib
import re
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
PLANS = pathlib.Path(RACINE) / "mondes/lumina-prime/plans"
SVG = PLANS / "tranche-2d-hall-salon-galerie-dev-j1.svg"
DONNEES = PLANS / "tranche-2d-hall-salon-galerie-dev-j1.json"
TITRE = "🗺️ Tranche 2D hall–salon–galerie — livraison DEV v0.1, J1 17h10"


def empreinte(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment.lower() in nom.lower())


def corriger(livre):
    sha_svg = empreinte(SVG)
    sha_json = empreinte(DONNEES)
    if not any(t["titre"] == TITRE for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE,
            "colonnes": ["Élément livré", "Lecture publique", "Lecture municipale", "Statut et source"],
            "lignes": [
                {"cellules": [
                    "Topologie commune",
                    "Parvis → Hall → Salon → Galerie ; Salle du conseil gardée comme raccord de bord depuis Hall et Galerie.",
                    "Cinq passages, chacun à 1 minute conventionnelle, dessiné et non essayé. Aucun passage direct Hall–Galerie n'est porté par le plan.",
                    "Livré par DEV depuis plan-initial-radiant-core et 30307."
                ]},
                {"cellules": [
                    "Tâche 1 — rejoindre un entretien",
                    "Chemin trouvé au dessin : Hall → Salon.",
                    "Praticabilité, permission, usage décidé et contact opérationnel restent inconnus.",
                    "Base 60301 ; détail 60308 non remis."
                ]},
                {"cellules": [
                    "Tâche 2 — attendre hors passage",
                    "Impossibilité nommée : aucun espace d'attente hors passage n'est établi.",
                    "Le Jardin intérieur touche le Hall, mais son usage d'attente n'est pas décidé.",
                    "30305 et table ❓ ; décision d'usage réservée à Nova."
                ]},
                {"cellules": [
                    "Tâche 3 — atteindre une présentation sans traverser le travail",
                    "Impossibilité nommée sur le plan actuel.",
                    "Par le Salon, le trajet traverse l'entretien ; par le Conseil, il traverse le travail. La voie indépendante est un besoin non dessiné.",
                    "30307 et 30305 ; aucun aménagement décidé."
                ]},
                {"cellules": [
                    "Couches concurrentes",
                    "Aucun statut de permission, de praticabilité ou de service n'est affiché comme acquis.",
                    "Emplacements réservés et attribués : PITCH 60308, Gaia 50303, JURIS 70305 · 70202, Quantum 40302, Aria 20564.",
                    "Toutes non remises au seuil de cette version ; leur absence vaut « inconnu », pas conformité."
                ]},
                {"cellules": [
                    "Blancs et décisions",
                    "Usage des pièces, attente, contact et voie publique Hall–Galerie restent visibles comme blancs.",
                    "Droits, décideurs, mesures, validité, publication municipale, moyens et chantier ne sont pas décidés.",
                    "Nova garde usages nouveaux, grand aménagement, moyens, publication et chantier."
                ]},
                {"cellules": [
                    "Réception",
                    "Un lecteur sans explication de DEV doit trouver Hall–Salon et nommer les deux impossibilités.",
                    "Il doit aussi distinguer dessiné, essayé, permis et inconnu, puis retrouver chaque source.",
                    "À éprouver par Aria sous 20564 ; aucune réussite présumée."
                ]}
            ],
            "pages": [
                "Adresse graphique : mondes/lumina-prime/plans/tranche-2d-hall-salon-galerie-dev-j1.svg — SHA-256 " + sha_svg + ".",
                "Adresse des données : mondes/lumina-prime/plans/tranche-2d-hall-salon-galerie-dev-j1.json — SHA-256 " + sha_json + ".",
                "Version 0.1 : structure indépendante de DEV. Elle peut recevoir les contributions séparées sans modifier la topologie. Aucun prompt actif, plan actif, usage, droit, moyen, position, horloge ou chantier n'est modifié."
            ]
        })

    livraison = table(livre, "🗺️ Tranche 2D hall–salon–galerie — livraison")
    couches = next(l["cellules"] for l in livraison["lignes"] if l["cellules"][0] == "Couches concurrentes")
    couches[1] = (
        "La permission est affichée « inconnue » selon la remise de JURIS ; aucun statut de praticabilité "
        "ou de service n'est affiché comme acquis."
    )
    couches[2] = (
        "JURIS 70305 · 70202 remis : Nova décide par 10010 sur 10022, recours concret par 70303. "
        "Gaia 50303 remis sur Quai–Data Gardens : critères des six gestes disponibles, mais aucun constat "
        "matériel de cette tranche. Aria 20564 : fiche ouverte, lecture extérieure non consignée."
    )
    couches[3] = (
        "Raccords relus après livraison. PITCH 60308 et Quantum 40302 restent non remis ; "
        "praticabilité du hall–salon–galerie et données techniques restent inconnues."
    )
    reception = next(l["cellules"] for l in livraison["lignes"] if l["cellules"][0] == "Réception")
    reception[3] = (
        "Fiche écrite par Aria sous 20564 ; action encore en cours jusqu'à une lecture extérieure consignée."
    )
    livraison["pages"] = [
        "Adresse graphique : mondes/lumina-prime/plans/tranche-2d-hall-salon-galerie-dev-j1.svg — SHA-256 " + sha_svg + ".",
        "Adresse des données : mondes/lumina-prime/plans/tranche-2d-hall-salon-galerie-dev-j1.json — SHA-256 " + sha_json + ".",
        "Version 0.1 : structure indépendante de DEV. Raccords relus après écriture : couche de JURIS intégrée par référence ; feuille Gaia conservée dans son périmètre Quai–Data Gardens ; fiche Aria ouverte. PITCH et Quantum restent non remis. Aucun prompt actif, plan actif, usage, droit, moyen, position, horloge ou chantier n'est modifié."
    ]

    contrat = table(livre, "🧭 Tranche 2D")
    premiere = contrat["lignes"][0]["cellules"]
    if "Version 0.1 livrée" not in premiere[3]:
        premiere[3] += (
            " Version 0.1 livrée le J1 à 17h10 dans plans/tranche-2d-hall-salon-galerie-dev-j1.svg "
            "et .json ; réception indépendante et couches des autres offices non présumées."
        )

    actions = table(livre, "⚔️")
    a30303 = next(l for l in actions["lignes"] if l["cellules"][0] == "30303")["cellules"]
    i_faire = indice(actions, "Ce qu")
    if "Version 0.1 de la tranche 2D" not in a30303[i_faire]:
        a30303[i_faire] += (
            " J1, 17h10 : version 0.1 de la tranche 2D hall–salon–galerie réalisée en SVG et JSON. "
            "Elle livre la topologie et éprouve les trois tâches de 60301 : un chemin trouvé et deux "
            "impossibilités nommées. Les contributions 60308, 50303, 70305 · 70202, 40302 et la réception "
            "20564 restent non remises et visibles comme inconnues."
        )
    a30303[i_faire] = a30303[i_faire].replace(
        "Les contributions 60308, 50303, 70305 · 70202, 40302 et la réception 20564 restent non remises et visibles comme inconnues.",
        "Après relecture concurrente, JURIS a remis 70305 · 70202, Gaia a remis 50303 dans son périmètre Quai–Data Gardens et Aria a ouvert 20564 ; PITCH 60308 et Quantum 40302 restent non remis. La praticabilité de cette tranche demeure inconnue."
    )
    i_preuve = indice(actions, "preuve")
    if "livraison DEV v0.1" not in a30303[i_preuve]:
        a30303[i_preuve] += (
            " Table 🗺️ livraison DEV v0.1 ; SVG SHA-256 " + sha_svg +
            " ; JSON SHA-256 " + sha_json + "."
        )
    a30303[i_preuve] = re.sub(
        r"Table 🗺️ livraison DEV v0\.1 ; SVG SHA-256 [0-9a-f]+ ; JSON SHA-256 [0-9a-f]+\.",
        "Table 🗺️ livraison DEV v0.1 ; SVG SHA-256 " + sha_svg +
        " ; JSON SHA-256 " + sha_json + ".",
        a30303[i_preuve]
    )
    # L'inventaire, la réception et les couches restent ouverts : ne pas fermer 30303.


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
