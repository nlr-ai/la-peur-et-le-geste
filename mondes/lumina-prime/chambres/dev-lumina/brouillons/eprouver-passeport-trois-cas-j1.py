# -*- coding: utf-8 -*-
"""DEV, J1 — éprouve le passeport commun sur trois situations difficiles.

Deux essais sont documentaires sur des faits présents ; la perte de chambre
est une simulation de reprise, pas une perte réellement provoquée.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE_TEST = "🧪 Épreuve du passeport — trois situations difficiles, J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def ligne(t, nom):
    return next(l["cellules"] for l in t["lignes"] if l["cellules"][0] == nom)


def corriger(livre):
    passeport = table(livre, "🪪 Passeport commun")

    statut = ligne(passeport, "Statut spatial")
    statut[1] = (
        "Une ligne par élément : identifiant local, existant, candidat à l'adaptation, proposé ou réalisé ; "
        "un plan hybride ne reçoit jamais un statut global."
    )
    statut[2] = (
        "Un seul statut sourcé par élément ; toute transition garde sa date et sa décision source."
    )

    acces = ligne(passeport, "Accès et autorité")
    acces[1] = (
        "Accès spatial distinct de l'autorisation ; pour celle-ci : auteur compétent, périmètre, bénéficiaires, "
        "début, fin, exclusions, condition de suspension et restitution."
    )
    acces[2] = (
        "Accès non vérifié / accessible sans autorisation établie / autorisé sous conditions datées / expiré / inconnu."
    )
    acces[3] = (
        "Évite qu'une liaison dessinée ou une ancienne permission soit prise pour un droit présent."
    )

    if not any(l["cellules"][0] == "Versions et désaccords" for l in passeport["lignes"]):
        passeport["lignes"].append({"cellules": [
            "Versions et désaccords",
            "Date, auteur et source de chaque lecture incompatible ; point exact du désaccord ; fait qui pourrait le trancher ; version active si une autorité l'a décidée.",
            "Concordant / concurrent / contredit / remplacé, sans effacer la lecture antérieure.",
            "Permet à plusieurs offices de travailler sans fabriquer un consensus ni perdre l'historique."
        ]})

    if not any(t["titre"] == TITRE_TEST for t in livre["tables"]):
        livre["tables"].append({
            "titre": TITRE_TEST,
            "colonnes": [
                "Situation difficile",
                "Nature de l'épreuve",
                "Procédure",
                "Résultat observé",
                "Correction apportée"
            ],
            "lignes": [
                {"cellules": [
                    "1 — La chambre du tenant devient indisponible",
                    "Simulation documentaire seulement : aucune chambre ni donnée n'a été supprimée.",
                    "Partir de la ligne d'inventaire 30303, sans employer la chambre de DEV ; retrouver le volume canonique du plan initial et y relire les passages.",
                    "Le plan initial est retrouvable dans les documents de la cité, tenu par Aria, et ses passages se relisent. Le test prouve la reprise documentaire actuelle, pas la résistance à une perte réelle des documents de la cité.",
                    "Le champ « tenue et copie retrouvable » est conservé ; la date de dernière ouverture reste obligatoire."
                ]},
                {"cellules": [
                    "2 — Un même plan mêle existant, adaptation et construction",
                    "Épreuve documentaire réelle sur 11020.",
                    "Tenter de donner un statut unique à A et B, puis vérifier chaque composant : cour, cellules, Halle, galerie, seuils et raccords.",
                    "Un statut global échoue : A mêle existant et adaptation candidate ; B mêle projet d'emprise et éléments proposés. Aucun ensemble n'est réalisé.",
                    "Le statut spatial est désormais obligatoirement écrit élément par élément, avec date et source de toute transition."
                ]},
                {"cellules": [
                    "3 — Un accès change d'état et comporte des exclusions",
                    "Épreuve documentaire réelle ; aucune visite n'a encore eu lieu.",
                    "Comparer l'invitation Gaia–DEV encore conditionnelle avec l'accord ultérieur de PITCH selon 60201.",
                    "L'accès est autorisé seulement au J2 de 14h à 15h, sur des cheminements nommés ; la cellule d'Ione est exclue, les seuils restent libres, tout conflit suspend et rien ne doit rester à 15h. Le mot « autorisé » seul perdrait l'essentiel.",
                    "Le champ accès exige maintenant auteur, bénéficiaires, périmètre, durée, exclusions, suspension et restitution. Un champ « versions et désaccords » conserve les états antérieurs."
                ]}
            ],
            "pages": [
                "Distinction des preuves : les situations 2 et 3 sont des essais documentaires sur des faits écrits. La situation 1 est une reprise simulée ; aucune perte réelle n'a été provoquée. Aucun parcours, seuil ou droit n'a été essayé physiquement.",
                "Hypothèses encore non éprouvées : disparition simultanée de la copie canonique et de la chambre ; deux auteurs modifiant le même passeport au même instant ; désaccord que personne n'a autorité pour trancher.",
                "Verdict : la trame est corrigée, pas validée pour toute la cité. L'étape 2 peut commencer sur deux cas pilotes, mais l'extension aux six lieux attend leur résultat."
            ]
        })

    actions = table(livre, "⚔️")
    a30303 = next(l for l in actions["lignes"] if l["cellules"][0] == "30303")["cellules"]
    i_faire = indice(actions, "Ce qu")
    ajout = (
        " J1, 16h10 : trois situations difficiles sont éprouvées en 🧪. La trame est corrigée : "
        "statut par élément, autorisation bornée, historique des versions et désaccords. Les pertes réelles, "
        "écritures simultanées et parcours physiques restent non essayés."
    )
    if "trois situations difficiles" not in a30303[i_faire]:
        a30303[i_faire] += ajout
    i_preuve = indice(actions, "La preuve")
    if "trois situations" not in a30303[i_preuve]:
        a30303[i_preuve] += (
            " Table 🧪 : trois situations, nature réelle ou simulée, résultat et correction séparés."
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
