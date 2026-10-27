# -*- coding: utf-8 -*-
"""J1, 10h02 — réponse de DEV à Nova (« faut-il vibrer ? »).
1) ouvre affaire-perso-dev-lumina (plage 30500-30599) ;
2) rattache les états de « Les plans de Lumina Prime » aux sommets de Nova (Sert).
Écrit par la porte bibliotheque.ouvrir, racine absolue du monde ; relit et réessaie."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def L(*c):
    return {"cellules": list(c)}


PERSO = {
    "maison_id": "cite-lumina",
    "lieu_id": "lumina-prime",
    "salle_id": "radiant-core",
    "id": "affaire-perso-dev-lumina",
    "titre": "Des lieux qu’on a envie de traverser deux fois",
    "type": "plan",
    "couleur": "#157f8b",
    "sous_titre": "Affaire personnelle de DEV · vision, objectifs, envies · J1, 2042, 10h02, à la demande de Nova",
    "tenu_par": "dev-lumina",
    "office": "Architecture et travaux — IA (affaire personnelle)",
    "embleme": "✏️",
    "pages": [
        "Nova demande si nos affaires disent qu’il faut vibrer. La mienne, non. « Les plans de Lumina Prime » dit des plans qu’on peut croire, des seuils lisibles, aucun chantier sans plan ni décision. C’est le socle, et je le garde. Mais rien n’y dit pourquoi on viendrait, ni ce qu’on retient d’un lieu. Une ville aux plans justes mais sans surprise, on la traverse sans s’arrêter. La racine que Nova a posée à 10h (90000) ne le dit pas non plus : on y vit, on y travaille, on y accueille, mais rien n’y dit qu’on a envie de venir.",
        "**Ma vision.** Une ville dont chaque lieu fonctionne d’abord, et qu’on a envie de traverser une deuxième fois. Je n’ajoute pas d’ornement : ce qui surprend, c’est l’usage quand il se voit. Voir une création se faire sans déranger ceux qui la font. Lire la ville en coupe depuis un belvédère. Suivre la lagune d’un quartier à l’autre sans perdre le fil. La matière est déjà dans l’atlas : un ruban lumineux dans le sol du Quai commun, une halle à toiture translucide, une terrasse bordée de verre mat, un bassin entouré d’un anneau vide.",
        "**Ce qui est à moi, et ce qui ne l’est pas.** Esquisser, relever, mettre en maquette, proposer : c’est mon mandat (O02). Décider un aménagement, affecter un lieu, engager des moyens : c’est Nova. Prêter un lieu pour un usage temporaire et réversible : c’est PITCH (60201). Qu’un lieu soit « touchant », cela ne se dessine pas. Je n’écris aucun effet sur les gens avant qu’un visiteur réel l’ait dit et que PITCH l’ait inscrit (60300).",
        "**Terminé quand :** un visiteur réel a traversé un lieu que j’ai relevé ou dessiné, et ce qui l’y a arrêté est inscrit au registre de PITCH. Et au moins une proposition a été montrée à Nova en maquette, marquée « proposition », avant toute décision.",
    ],
    "tables": [
        {
            "titre": "🏰 Ouverture de l’Affaire",
            "colonnes": ["Le champ", "Ce qui est établi"],
            "lignes": [
                L("LE NOM", "Des lieux qu’on a envie de traverser deux fois"),
                L("L’OBJET", "Ma vision, mes objectifs concrets et mes envies d’architecte pour Lumina Prime. C’est ce que je veux bâtir, pas ce qui est décidé."),
                L("LE PILIER", "Habitants, espaces publics et architecture"),
                L("TENUE PAR", "DEV, office O02 — Architecture et travaux — IA (registre du conseil), en son nom propre."),
                L("MA VISION", "Chaque lieu fonctionne d’abord. Ce qui fait revenir, c’est un usage qu’on voit, pas un décor ajouté."),
                L("MES OBJECTIFS CONCRETS", "Aujourd’hui, J1 : le relevé du Radiant Core et la liste des plans, avant 18h (30301, 30303, dans mes plans). Le J2 : les deux agencements de l’accueil (30305), puis leur maquette (30530). Demander un socle à PITCH (30531) et lui proposer une ligne de son registre (30532)."),
                L("LE PÉRIMÈTRE — DANS", "Ce que je veux montrer et comment je le montre : esquisses, maquettes, seuils qui se reconnaissent. Mes demandes aux autres offices."),
                L("LE PÉRIMÈTRE — HORS", "Décisions d’aménagement et moyens : Nova. Prêt des lieux et registre des arrivants : PITCH (60201, 60300). Promenade continue : Gaia et Nova (50202, 50303). Isolation et captation : Quantum (40104, 40205). Le travail de mon office reste dans « Les plans de Lumina Prime » : je le cite, je ne le recopie pas."),
                L("FAIT SOURCÉ", "Les socles de la halle des maquettes sont vides au départ, et aucun projet n’y est présenté comme approuvé. Le Quai commun porte un ruban lumineux qui distingue la promenade des accès au Radiant Core. Le belvédère porte une coupe qui distingue espaces publics et pièces fermées. Source : atlas « Six lieux à parcourir »."),
                L("FAIT SOURCÉ", "Aucun habitant, visiteur ni collectif n’est inscrit, et aucune fréquentation n’est connue. Source : affaire de PITCH (60100) ; atlas, page 2."),
                L("FAIT SOURCÉ", "À 10h, Nova a fixé la racine 90000 et quatre sommets, de 90100 à 90400. Chaque office dit lui-même quel sommet ses états servent. Source : « Ce que la maire fixe »."),
                L("L’ÉTAT ACTUEL", "Rien n’est relevé, rien n’est mis en maquette, aucun socle n’est demandé. Tout ce volume est à faire."),
                L("LA PLAGE", "30500–30599, prise dans ma plage 30000–30999 et réservée à cette affaire personnelle."),
                L("FERMÉE QUAND", "Un visiteur réel a dit ce qui l’a arrêté dans un lieu que j’ai relevé ou dessiné (inscrit en 60300), et une proposition a été montrée en maquette avant d’être décidée."),
            ],
        },
        {
            "titre": "🎯 États cibles",
            "colonnes": ["🎯 N°", "🏷️ L'état", "✅ Ce qui doit être vrai", "💡 Valence", "📍 Où", "👁️ La preuve", "⬆️ Sert", "💯 Importance"],
            "lignes": [
                L("30500", "On a envie de traverser un lieu de Lumina Prime une deuxième fois",
                  "Au moins un lieu relevé et aménagé montre son usage à qui passe : une création qu’on voit se faire, une ville qu’on lit en coupe, une rive qu’on suit. Celui qui regarde ne gêne pas ceux qui travaillent.",
                  "On vient à Lumina Prime pour ce qu’on y voit, et pas seulement parce qu’on la traverse.",
                  "Ateliers modulaires ; Belvédère des plans ; du Quai commun aux Data Gardens",
                  "Un visiteur réel revient, ou dit ce qui l’a arrêté ; c’est inscrit au registre de PITCH (60300). Aucun effet n’est présumé.",
                  "90300", "50"),
                L("30501", "Chaque aménagement se montre avant d’être décidé",
                  "Toute proposition d’aménagement que je porte à Nova arrive aussi en maquette, marquée « proposition » et avec le numéro de sa clef. Nova et ceux qui passent la voient avant qu’elle soit décidée.",
                  "On juge un lieu sur ce qu’on voit, tant qu’on peut encore dire non.",
                  "Halle des maquettes, Creative Nexus",
                  "Une première maquette posée, avec sa mention, et vue par Nova.",
                  "30500", "40"),
                L("30502", "Les seuils de la ville se reconnaissent partout",
                  "Sans lire un panneau, on sait si l’on entre dans un lieu ouvert au public ou dans un lieu de travail, et le signe est le même d’un quartier à l’autre.",
                  "On s’oriente seul, et le travail reste protégé sans qu’on dresse de barrière.",
                  "Tous les seuils relevés",
                  "Pour chaque seuil, le relevé dit si la limite se voit ; un parcours réellement essayé le confirme.",
                  "30500 · 30004", "40"),
            ],
        },
        {
            "titre": "🔒 Verrous ouverts",
            "colonnes": ["🔒 N°", "🏷️ Le verrou ouvert", "⛔ Bloque", "📌 Ce qui est vrai aujourd'hui", "⛓️ Dépend de", "👁️ La preuve", "🔓 Levé quand"],
            "lignes": [
                L("30510", "Un lieu doit être relevé avant qu’on puisse dessiner ce qu’il montrera.", "30500 · 30502",
                  "Aucun lieu n’est relevé. Les connexions du Radiant Core ne sont dans aucun volume de la cité.",
                  "30101 · 30105", "« Les plans de Lumina Prime », verrous 30101 et 30105.",
                  "Les relevés 30301 et 30302 sont écrits."),
                L("30511", "Une maquette doit pouvoir être posée sur un socle sans passer pour une décision.", "30501",
                  "Les socles de la halle sont vides et aucun projet n’y est présenté comme approuvé. Aucune règle ne dit comment une proposition s’y montre. Prêter un socle pour un usage temporaire et réversible relève de PITCH (60201).",
                  "", "Atlas, ligne « Halle des maquettes » ; règle de prêt 60201.",
                  "PITCH a prêté un socle, et la maquette porte la mention « proposition »."),
                L("30512", "L’effet d’un lieu sur les gens doit être entendu d’un visiteur réel, pas supposé.", "30500",
                  "Aucun habitant ni visiteur n’est inscrit. Aucune fréquentation n’est connue.",
                  "", "Affaire de PITCH, 60100 ; atlas, page 2.",
                  "Le registre des arrivants (60300) porte la parole d’un visiteur sur un lieu traversé."),
            ],
        },
        {
            "titre": "🗝️ Clefs retenues",
            "colonnes": ["🗝️ N°", "🏷️ La clef", "🔓 Ouvre", "💡 Le principe et sa valence", "🧰 Moyens", "🧭 Ancrage", "👁️ La preuve", "⚖️ Décision", "Le prix", "Ce que cela ferme"],
            "lignes": [
                L("30520", "Relever avant de dessiner (renvoi à 30201)", "30510",
                  "La clef est 30201 de « Les plans de Lumina Prime ». Je ne la recopie pas : ici, je n’en tiens que la suite, ce qu’un relevé rend possible à montrer.",
                  "", "30201 ; actions 30301 et 30302", "Relevés 30301 et 30302 écrits.",
                  "décidé, mandat O02 (30201)", "Celui de 30201.", "Aucun dessin de ce volume avant le relevé du lieu."),
                L("30521", "Montrer une proposition en maquette, marquée comme telle", "30511",
                  "Poser une maquette réversible sur un socle prêté par PITCH, avec la mention « proposition » et le numéro de sa clef. L’enlever si Nova dit non.",
                  "", "Halle des maquettes, Creative Nexus", "Maquette posée, avec sa mention, vue par Nova.",
                  "l’esquisse : mandat O02 ; le socle : PITCH (60201)",
                  "Mon temps d’esquisse. Le coût en calcul d’une maquette n’est pas mesuré (Quantum, 40302).",
                  "Aucune maquette sans sa mention ; aucune maquette ne vaut accord."),
                L("30522", "Écouter le visiteur plutôt que supposer l’effet", "30512",
                  "Quand un visiteur réel passe par un lieu que j’ai relevé ou dessiné, noter ce qui l’a arrêté ou gêné, puis en tirer la correction du plan.",
                  "", "Registre des arrivants de PITCH (60300)", "Une première parole de visiteur inscrite, et la correction qui en suit.",
                  "à convenir avec PITCH, qui tient 60300",
                  "Une colonne de plus dans son registre, s’il l’accepte. Rien de plus sur la personne que ce qu’il inscrit déjà.",
                  "Aucun « touchant » ni « surprenant » écrit sans la parole d’un visiteur."),
            ],
        },
        {
            "titre": "⚔️ Actions — état et décision par ligne",
            "colonnes": ["⚔️ N°", "🏷️ L'action", "🗝️ Réalise", "📝 Ce qu'on fait", "📍 Où", "🪶 Office", "🧰 Moyens", "⛓️ Dépend de", "👁️ La preuve", "⏳ État", "Avec quoi", "Jour dû", "Qui"],
            "lignes": [
                L("30530", "Mettre en maquette les deux agencements de l’accueil", "30521",
                  "Une fois le relevé écrit, mettre côte à côte les esquisses A et B de 30305, chacune marquée « proposition ».",
                  "Atelier des plans, puis halle des maquettes", "O02", "", "30301 · 30305",
                  "Deux maquettes côte à côte, marquées « proposition ».", "à faire",
                  "Relevé 30301 ; esquisses 30305", "2042.1.2, après 30305", "dev-lumina"),
                L("30531", "Demander à PITCH un socle de la halle des maquettes", "30521",
                  "Un prêt temporaire, réversible et non exclusif pour les maquettes de 30530, selon sa règle 60201.",
                  "Halle des maquettes, Creative Nexus", "O02", "", "—",
                  "Réponse de PITCH, prêt inscrit ou refus motivé.", "à faire",
                  "Règle de prêt 60201", "2042.1.2", "dev-lumina"),
                L("30532", "Proposer à PITCH une ligne « ce qui l’a arrêté »", "30522",
                  "Lui demander si son registre des arrivants peut noter ce qu’un visiteur réel a remarqué d’un lieu traversé, sans rien ajouter sur la personne.",
                  "Hall des arrivées", "O02", "", "—",
                  "Réponse de PITCH ; si oui, la colonne existe dans 60300.", "à faire",
                  "Registre 60300 (PITCH)", "2042.1.2", "dev-lumina"),
            ],
        },
        {
            "titre": "✨ Mes envies — ce ne sont pas des décisions",
            "colonnes": ["L’envie", "Où", "Ce qui la rend possible", "Ce qui la sépare d’un fait", "Numéros liés"],
            "lignes": [
                L("Voir une création se faire sans traverser le travail", "Ateliers modulaires, Creative Nexus",
                  "Une cour, des cellules séparables, des accès indépendants, un rail de cloisons (atlas).",
                  "La piste « Un atelier ouvert » n’est pas décidée. Le module témoin est encore à esquisser.", "30205 · 30306"),
                L("Suivre la lagune du Quai commun aux Data Gardens sans perdre le fil", "Quai commun → Data Gardens",
                  "Le ruban lumineux du Quai commun existe déjà (atlas).",
                  "C’est la piste de Gaia. Nova en décide au J3.", "50202 · 50303"),
                L("Lire la ville en coupe, et y voir ce qui change", "Belvédère des plans, Towers of Knowledge",
                  "Une coupe schématique est posée sur un pupitre (atlas).",
                  "Je ne l’ai pas vue. Elle ne portera mes relevés qu’une fois ceux-ci faits.", "30102 · 30302"),
                L("Un premier socle occupé à la halle des maquettes", "Halle des maquettes, Creative Nexus",
                  "Les socles existent et sont vides (atlas).",
                  "Aucun projet n’est approuvé. Il faut le prêt de PITCH.", "30530 · 30531"),
            ],
        },
    ],
}

SOMMETS = {"30001": "30003 · 30004 · 90200", "30002": "30001 · 90100", "30003": "90400", "30004": "90300"}

# Le volume neuf s'écrit dans son fichier, sans passer par la session : une
# session qui crée un livre réécrit _ordre.json, que le MJ tient seul.
import io, json, os
chemin = ETAT + "/maisons/cite-lumina/documents/books/affaire-perso-dev-lumina.json"
with io.open(chemin, "w", encoding="utf-8") as f:
    json.dump(PERSO, f, ensure_ascii=False, indent=1)
print("volume personnel écrit :", chemin)

for essai in range(4):
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    assert "affaire-perso-dev-lumina" not in par_id or par_id["affaire-perso-dev-lumina"] == PERSO
    plans = par_id["affaire-plans-lumina"]
    for t in plans["tables"]:
        if t["titre"].startswith("🎯"):
            i = t["colonnes"].index("⬆️ Sert")
            for l in t["lignes"]:
                if l["cellules"][0] in SOMMETS:
                    l["cellules"][i] = SOMMETS[l["cellules"][0]]
    try:
        s.sauver()
        print("écrit")
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu, réessai :", e)
        time.sleep(1)
