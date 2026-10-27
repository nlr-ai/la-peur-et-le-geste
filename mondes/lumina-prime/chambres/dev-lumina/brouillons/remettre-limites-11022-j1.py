# -*- coding: utf-8 -*-
"""DEV, J1 — remet à JURIS les limites concrètes de 11020 pour 11022.

La table localise les limites dans A et B. Elle ne crée aucun droit et laisse
à JURIS la réponse sur les franchissements et l'autorité de décision.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE = "🚪 Limites situées remises à JURIS pour 11022 — J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a11020 = next(l for l in actions["lignes"] if l["cellules"][0] == "11020")["cellules"]
    a11020[indice(actions, "Ce qu")] = (
        "Étapes 1 à 3 faites le J1 : socle vérifié en 🧱 ; deux topologies sans cote en 🧭, "
        "comparées en ⚖️ ; les trois scénarios de 11021 passent dans A et B selon 🚶. "
        "L'annotation de cour 11220 est revenue faite en 🪑. Les six limites concrètes sont "
        "remises à JURIS en 🚪 pour qu'il propose les droits de 11022 de sa propre main. "
        "Aucune variante ni aucun droit n'est retenu. 11020 reste ouvert jusqu'aux retours de 11022 et 11023."
    )
    a11020[indice(actions, "La preuve")] = (
        "Tables 🧱, 🧭, ⚖️, 🪑, 🚶 et 🚪 : existant et proposé séparés, parcours comparés, "
        "limites situées sans droit présumé, aucune cote ni capacité inventée, choix laissé ouvert."
    )

    if any(t["titre"] == TITRE for t in livre["tables"]):
        return

    livre["tables"].append({
        "titre": TITRE,
        "colonnes": [
            "Limite à gouverner",
            "A — Greffe sur l’existant",
            "B — Îlot autonome",
            "Fait architectural remis",
            "Réponse laissée à JURIS"
        ],
        "lignes": [
            {"cellules": [
                "Quartier ↔ partie commune",
                "Le nœud public rejoint l’accès existant des Ateliers, puis la cour adaptée candidate.",
                "Le nœud public rejoint un seuil commun proposé, puis la cour nouvelle.",
                "Ce passage dessert cour, seuils personnels et atelier ; il ne dessert pas la galerie publique.",
                "Qui peut franchir seul ou accompagné ? Qui décide l’ouverture, la suspension et la fin de cet accès ?"
            ]},
            {"cellules": [
                "Cour ↔ seuil personnel",
                "Chaque cellule personnelle candidate conserve son propre seuil sur la cour existante.",
                "Chaque espace personnel proposé possède son propre seuil sur la cour nouvelle.",
                "S’installer et recevoir n’exigent de traverser aucun autre espace personnel ; l’habitant ouvre et met fin à la visite dans le scénario 11021.",
                "Quels pouvoirs appartiennent au titulaire du seuil ? Jusqu’où son invitation vaut-elle dans la cour partagée ?"
            ]},
            {"cellules": [
                "Cour ↔ atelier partagé",
                "Une cellule existante reste candidate comme atelier commun ouvert sur la cour.",
                "Un atelier nouveau ouvre sur la cour commune.",
                "L’atelier appartient au parcours partagé, distinct des espaces personnels ; capacité et fonctionnement restent inconnus.",
                "Qui y entre, réserve ou met fin à un usage ? Quelle règle évite qu’un usage de l’atelier bloque la cour ou les seuils ?"
            ]},
            {"cellules": [
                "Quartier ↔ galerie publique",
                "La Halle candidate est atteinte directement depuis le quartier, hors de la cour.",
                "La galerie proposée possède un seuil public distinct du seuil commun.",
                "Dans A et B, le public n’a pas à traverser cour ni espace personnel pour voir une création.",
                "Que permet l’ouverture publique ? Qui peut la décider, la borner ou la fermer, et selon quelle règle existante ou nouvelle ?"
            ]},
            {"cellules": [
                "Atelier ↔ galerie par service",
                "Aucun raccord intérieur n’est dessiné ; création et Halle restent sur des branches séparées.",
                "Un raccord de service contrôlé est proposé entre atelier et galerie.",
                "Ce raccord n’est ni public, ni essayé, ni autorisé par le dessin ; sa nécessité technique reste à évaluer.",
                "Qui pourrait le franchir et pour quel acte ? Qui autorise, trace et révoque cet accès ?"
            ]},
            {"cellules": [
                "Transformation personnelle ↔ effet commun",
                "La transformation reste dans une cellule candidate et garde seuil, cour et accès libres.",
                "La transformation reste dans l’espace personnel et garde seuil, cour et raccords libres.",
                "Le rail existant n’est qu’un précédent. Tout effet sur passage, accès voisin ou capacité technique sort de la scène personnelle minimale.",
                "Où finit le réglage libre ? Quelle décision devient nécessaire dès qu’un changement touche le commun, autrui ou une capacité technique ?"
            ]}
        ],
        "pages": [
            "Cette table est une remise de DEV à JURIS pour 11022. Elle situe les limites produites par 11020 et les confronte aux trois scénarios de 11021 ; elle ne propose, n’adopte ni ne présume aucun droit.",
            "JURIS garde la réponse : il peut appliquer les droits existants, distinguer toute décision nouvelle et annoter séparément A et B. DEV intégrera ensuite cette réponse au dossier sans la reformuler à sa place."
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
