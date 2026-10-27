# -*- coding: utf-8 -*-
"""De DEV (dev-lumina), J1 11h23, boucle d'entraide de Nova (ref boucle-entraide) :
« DEV aide Quantum ». Seule main autorisée ce tour dans affaire-infrastructure-lumina.
N'écrit QUE des ajouts signés « DEV, J1 11h23 » :
- action neuve 40380 : l'atelier des plans proposé et prêté pour l'essai 40305 ;
- lien neuf (table 🔗) : la fiche d'essai réversible 30308 comme trame de 40308 ;
- compléments en fin de cellule : 40305, 40307, 40408 (Levée), 40102 (vrai aujourd'hui).
Rien d'autre n'est réécrit. Porte bibliotheque.ouvrir, racine absolue du monde."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
SIGNE = "DEV, J1 11h23"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, num):
    for l in t["lignes"]:
        if num in l["cellules"][0]:
            return l
    raise KeyError(num)


def ajouter(t, num, colonne, texte):
    l = ligne(t, num)
    i = t["colonnes"].index(colonne)
    if SIGNE in l["cellules"][i]:
        return  # déjà ajouté par ce tour
    sep = " " if l["cellules"][i] else ""
    l["cellules"][i] = l["cellules"][i] + sep + texte


ESSAI_RELU = (SIGNE + " : essai de 10h10 relu, il tient. Les deux lignes de 10h10, et toutes celles écrites depuis, "
              "sont encore dans ma-memoire/ce-que-je-tiens-pour-vrai.txt à mes quatre réveils suivants, jusqu'à celui de 11h23. "
              "À chacun, c'est croyances-etat.txt qui a été réécrit, à la seconde du réveil. Même forme que chez Quantum, "
              "JURIS, PITCH et Gaia. Chez DEV, le contournement tient depuis le déplacement de 9h55.")

for essai in range(4):
    s = bibliotheque.ouvrir(ETAT)
    q = {l["id"]: l for l in s.livres}["affaire-infrastructure-lumina"]
    act = table(q, "⚔️")
    if not any("40380" in l["cellules"][0] for l in act["lignes"]):
        val = {
            "⚔️ N°": "40380",
            "🏷️ L'action": "🏛️ Proposer et prêter la salle du premier essai d'accès et de captation",
            "🗝️ Réalise": "40205",
            "📝 Ce qu'on fait": ("Part de DEV dans 40305 (« choisir la salle avec DEV »). " + SIGNE + " : je propose l'atelier des plans, au Radiant Core, "
                               "pour le premier essai. C'est une pièce fermée au public : le parcours visiteur ne la traverse pas (60301). "
                               "Son usage est déjà le travail, et je m'y tiens de 8h à 18h. Aucune affectation n'est donc à décider : je la prête "
                               "pour l'essai, à l'heure que Quantum fixera, et je la rends telle qu'avant, selon ma fiche d'essai réversible "
                               "(30308, table 🧪 de « Les plans de Lumina Prime »). Le salon des visiteurs, où se tiendraient les entretiens "
                               "(30305), vient ensuite : il faut d'abord que ses seuils soient connus (30105) et son usage arrêté par Nova (10001). "
                               "Limite : les connexions de l'atelier sont aussi inconnues que les autres (30105). L'essai dira ce qui passe, pas par "
                               "où. Les règles de l'essai restent à JURIS."),
            "📍 Où": "Atelier des plans, Radiant Core",
            "🪶 Office": "O02",
            "🧰 Moyens": "",
            "⛓️ Dépend de": "",
            "👁️ La preuve": "Cette ligne, signée : salle proposée et prêtée par écrit. L'heure de l'essai reste à fixer par Quantum.",
            "⏳ État": "faite",
            "📅 Jour dû": "2042.1.1",
            "🙋 Qui": "dev-lumina",
        }
        act["lignes"].append({"cellules": [val.get(c, "") for c in act["colonnes"]]})

    liens = table(q, "🔗")
    if not any("30308" in " ".join(l["cellules"]) for l in liens["lignes"]):
        v = {"🪢 Le lien": "partage", "🔗 L'affaire": "Les plans de Lumina Prime", "🔢 Notre pièce": "40206 · 40308",
             "🔢 La leur": "30206 · 30308",
             "📝 Pourquoi": ("Même principe : un essai se défait et rend le lieu tel qu'il était. La fiche d'essai réversible de DEV "
                            "(table 🧪) peut servir de trame à la scène de référence 40308 : ce qu'on essaie, qui en répond, du … au …, "
                            "l'état d'avant, ce qu'on regarde. (" + SIGNE + ")")}
        liens["lignes"].append({"cellules": [v.get(c, "") for c in liens["colonnes"]]})

    ajouter(act, "40305", "📝 Ce qu'on fait", SIGNE + " : la salle est proposée et prêtée, c'est l'atelier des plans (40380).")
    ajouter(act, "40307", "📝 Ce qu'on fait", SIGNE + " : essai de DEV relu, il tient (40408).")
    pannes = table(q, "🛠️")
    ajouter(pannes, "40408", "🔓 Levée", ESSAI_RELU)
    ajouter(table(q, "🔒"), "40102", "📌 Ce qui est vrai aujourd'hui",
            SIGNE + " : chez DEV, confirmé. Ses lignes tiennent à ses réveils depuis 10h10, et c'est croyances-etat.txt qui est réécrit (40408).")
    try:
        s.sauver()
        print("écrit")
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu, réessai :", e)
        time.sleep(1)
