raise SystemExit("PÉRIMÉ (J1) : script déjà servi ; il réécrirait des cellules depuis une lecture ancienne. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""J1, hall des arrivées — 60300 (registre ouvert) et 60301 (parcours visiteur), dans l'affaire 60000."""
import json

F = r"C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/affaire-habitants-collectifs.json"


def L(*c):
    return {"cellules": list(c)}


a = json.load(open(F, encoding="utf-8"))
a["tables"] = [t for t in a["tables"] if not (t["titre"].startswith("📒") or t["titre"].startswith("🚶"))]

registre = {
    "titre": "📒 Registre des arrivants et des collectifs (60300)",
    "colonnes": ["📅 Date et heure", "👥 Personne ou collectif rencontré", "💬 Intention exprimée",
                 "🏠 Espace adapté", "🚪 Accès à vérifier", "🤲 Besoin d’accompagnement",
                 "↩️ Retour convenu", "👁️ Source"],
    "lignes": [],
}

parcours = {
    "titre": "🚶 Parcours visiteur — trois cas d’essai (60301 = 10020)",
    "colonnes": ["🧪 Cas d’essai", "🚪 Arrivée", "ℹ️ Information utile", "🧭 Orientation",
                 "⏳ Attente", "🎯 Destination et sortie", "📐 Besoin d’espace, pour DEV",
                 "❓ Inconnu"],
    "lignes": [
        L("Une première visite",
          "Par un accès au Radiant Core. Depuis le Quai commun, le ruban lumineux du sol distingue la promenade de ces accès (atlas). Les autres accès restent à relever (10021).",
          "Où l’on est, ce qui est ouvert aujourd’hui, à qui s’adresser.",
          "Au hall, quelqu’un répond et oriente vers une activité ouverte ou un lieu de l’atlas. PITCH, tant qu’aucun autre accueil n’est désigné.",
          "Aucune, ou brève, hors du passage.",
          "La galerie des projets (esquisse A) ou un lieu de l’atlas. Sortie par le hall, sans traverser l’atelier des plans ni la salle du conseil.",
          "Un point de réponse visible dès l’entrée. Un endroit où lire ce qui est ouvert sans arrêter le passage.",
          "Aucune activité ouverte n’est inscrite au J1. Ce que le hall dessert exactement relève du relevé de DEV (10021 = 30301)."),
        L("Un rendez-vous municipal",
          "Au hall, attendu par un office nommé.",
          "Avec qui, à quelle heure, où attendre.",
          "Annoncé à l’office concerné. Le visiteur ne cherche pas lui-même la salle.",
          "À l’écart du passage, sans entendre l’entretien précédent.",
          "L’entretien se tient au salon des visiteurs, dans les deux esquisses de DEV. Retour par le hall. Le visiteur ne traverse ni la galerie ni un lieu de travail.",
          "Un seuil lisible entre le hall et le salon. Le salon est-il atteint depuis le hall sans traverser la galerie ?",
          "La confidentialité réelle d’un entretien : une cloison opaque sépare la vue, sans rien garantir (40104, 40205 ; droits, JURIS)."),
        L("La présentation d’un projet par un collectif",
          "Au hall, avec une demande de lieu.",
          "Où l’on peut montrer, qui décide, dans quel délai. Un prêt temporaire et réversible se décide à l’office O05 (60201) ; le durable ou l’exclusif revient à Nova.",
          "La demande est inscrite au registre 📒. Le lieu est choisi selon l’échelle : la galerie des projets, ou la Halle des maquettes (Creative Nexus) pour un modèle spatial.",
          "Pendant l’examen de la demande. Le délai de réponse de la cité n’est pas fixé (20202).",
          "La galerie ou le lieu prêté, montré avant toute promesse (60203). Sortie par le hall.",
          "Une galerie accessible depuis le hall sans traverser le travail. Un endroit où poser une maquette. La galerie peut-elle recevoir un public pendant qu’un entretien se tient au salon ?",
          "La capacité de la galerie et de la Halle (non mesurée). Le délai de réponse promis par Nova."),
        L("Ce que les trois cas croisent",
          "Les trois entrent par le hall.",
          "Le cas 1 et le cas 3 ont besoin de la même information : ce qui est ouvert, et à qui s’adresser.",
          "Esquisse A : tout se joue au hall, qui porte à la fois le passage et l’orientation. Esquisse B : l’orientation passe à la galerie, et le hall ne sert qu’au passage.",
          "Seul le cas 2 attend à heure fixe. C’est aussi le seul qui demande l’écart.",
          "Le cas 2 va au salon, les cas 1 et 3 à la galerie. La séparation tient si le hall dessert les deux sans qu’on traverse l’un pour l’autre.",
          "À comparer par DEV sur le relevé (30305) : les trajets hall → salon et hall → galerie, et leurs croisements, dans A comme dans B.",
          "Aucune fréquentation n’est connue : ces cas sont des essais, pas des visiteurs présents."),
    ],
}

# Les tables structurelles d'abord, puis le parcours, puis le registre.
a["tables"] = a["tables"] + [parcours, registre]

for t in a["tables"]:
    if t["titre"].startswith("⚔️"):
        for l in t["lignes"]:
            c = l["cellules"]
            if c[0] == "**60300**":
                c[8] = "Table 📒 ouverte dans cette affaire le J1 au hall des arrivées, vide à l’ouverture : aucune personne ni aucune demande à inscrire."
                c[9] = "**faite**"
            elif c[0] == "**60301**":
                c[8] = "Table 🚶 écrite dans cette affaire le J1, trois cas d’essai sans fréquentation inventée, remise à Aria pour 10022 par billet ; besoins d’espace signalés à DEV pour 10021 = 30301 et 30305."
                c[9] = "**faite**"
    if t["titre"].startswith("🏰"):
        for l in t["lignes"]:
            c = l["cellules"]
            if "L’ÉTAT ACTUEL" in c[0]:
                c[1] = ("Au J1 : le registre des arrivants est ouvert et vide (60300, faite). Le parcours visiteur est écrit et remis à Aria (60301, faite). "
                        "Aucun habitant, visiteur, collectif ou demande n’est encore inscrit. La règle de prêt est accordée par Nova (9h25) ; je l’écris le J2 (60302).")

for t in a["tables"]:
    n = len(t["colonnes"])
    for l in t["lignes"]:
        assert len(l["cellules"]) == n, (t["titre"], l["cellules"][0])

json.dump(a, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("écrit :", [(t["titre"], len(t["lignes"])) for t in a["tables"]])
