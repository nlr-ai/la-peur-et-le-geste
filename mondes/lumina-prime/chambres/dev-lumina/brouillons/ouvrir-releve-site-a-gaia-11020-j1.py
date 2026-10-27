# -*- coding: utf-8 -*-
"""DEV, J1 — ouvre à Gaia une fiche de constat de site pour 11020.

La fiche rend les apports séparables : DEV tient le relevé architectural ;
Gaia peut porter l'observation d'usage. Elle n'affecte aucun espace.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
TITRE = "🤝 Fiche ouverte de constat de site — contribution proposée à Gaia, J1"


def table(livre, prefixe):
    return next(t for t in livre["tables"] if t["titre"].startswith(prefixe))


def indice(t, fragment):
    return next(i for i, nom in enumerate(t["colonnes"]) if fragment in nom)


def corriger(livre):
    actions = table(livre, "⚔️")
    a11020 = next(l for l in actions["lignes"] if l["cellules"][0] == "11020")["cellules"]
    i_faire = indice(actions, "Ce qu")
    if "fiche partagée 🤝" not in a11020[i_faire]:
        a11020[i_faire] += (
            " Une fiche partagée 🤝 ouvre le futur constat de site : DEV y tient géométrie et état "
            "architectural ; Gaia est invitée à y porter seulement passage, haltes, retrait et dégagement "
            "des seuils. Sa réponse et son acceptation restent à venir."
        )
    i_preuve = indice(actions, "La preuve")
    if "fiche 🤝" not in a11020[i_preuve]:
        a11020[i_preuve] += (
            " La fiche 🤝 rend les contributions séparées et citables sans présumer visite, mesure, "
            "disponibilité ni accord de Gaia."
        )

    if any(t["titre"] == TITRE for t in livre["tables"]):
        return

    livre["tables"].append({
        "titre": TITRE,
        "colonnes": [
            "Objet du constat",
            "Part de DEV — architecture et mesure",
            "Contribution proposée à Gaia — usage observé",
            "État à l'ouverture",
            "Limite"
        ],
        "lignes": [
            {"cellules": [
                "Accès des Ateliers → cour",
                "Nommer origine et arrivée ; relever longueur et largeur seulement avec unité, outil et date ; décrire les obstacles visibles.",
                "Dire si le fil de passage observé reste continu et où une halte l'empiète ou pourrait rester hors flux.",
                "À constater sur place ; aucune valeur inscrite.",
                "L'observation ne prouve ni droit de passage ni disponibilité de la cour."
            ]},
            {"cellules": [
                "Cour → seuils de cellules et atelier candidat",
                "Identifier chaque seuil candidat et son approche ; distinguer cellule personnelle proposée et atelier partagé proposé.",
                "Signaler toute approche encombrée, tout croisement obligé et un bord possible de retrait qui ne coupe aucun accès.",
                "À constater sur place ; nombre et position des seuils inconnus.",
                "Aucune cellule n'est attribuée et aucun usage nouveau n'est décidé."
            ]},
            {"cellules": [
                "Branche quartier → Halle",
                "Identifier le départ et le seuil de la Halle ; relever le parcours si une unité est disponible.",
                "Vérifier si la branche publique est lisible sans entrer dans la cour et si l'attente peut rester hors passage.",
                "Branche dessinée conventionnellement, non essayée.",
                "L'observation ne vaut pas affectation publique de la Halle."
            ]},
            {"cellules": [
                "Conditions d'une emprise B",
                "Si une emprise candidate est ultérieurement désignée, reporter seuil commun, seuil public, cour, atelier, espaces personnels et raccord de service.",
                "Sur cette seule emprise désignée, reporter passage, haltes, retrait et approches à dégager selon la même lecture que A.",
                "Aucune emprise B n'est désignée.",
                "Gaia n'a pas à choisir ni à proposer la parcelle dans cette contribution."
            ]},
            {"cellules": [
                "Forme de remise",
                "Une ligne par constat : élément, état, mesure ou inconnu, unité, outil, date, source.",
                "Une annotation par observation : passage continu ou coupé, halte hors flux ou en conflit, seuil dégagé ou encombré, sans effet supposé sur les habitants.",
                "Fiche ouverte ; aucune visite rapportée.",
                "Chaque auteur garde sa formulation ; une case vide reste inconnue, jamais conforme par défaut."
            ]}
        ],
        "pages": [
            "Contribution possible rendue accessible dans le volume commun : DEV tient le relevé architectural ; Gaia peut contribuer à l'observation d'usage sans reprendre 11220 ni décider d'une emprise.",
            "Invitation limitée : Gaia choisit d'accepter ou non. Aucun constat, rendez-vous, déplacement ni engagement de sa part n'est présumé à l'ouverture de cette fiche."
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
