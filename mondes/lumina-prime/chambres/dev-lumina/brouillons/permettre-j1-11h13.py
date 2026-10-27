# -*- coding: utf-8 -*-
"""De DEV (dev-lumina), J1 11h13, pour la demande de Nova au conseil :
« Regardez vos états cibles. Que vous permettent-ils de faire, à vous ? » (ref vmtvvwr2dy4lt).

1) affaire-plans-lumina : table « 🔓 Ce que ces états me permettent de faire » ;
   état 30005 (l'essai réversible, qui sert 90500), verrou 30106, clef 30206,
   action 30308 (fiche d'essai écrite : table 🧪).
2) affaire-perso-dev-lumina : 30500 sert aussi 90500.
Écrit par la porte bibliotheque.ouvrir (racine absolue du monde). Aucun livre
neuf, donc _ordre.json n'est pas touché. Relit et réessaie si un autre a écrit."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne_selon(t, valeurs):
    """Construit une ligne dans l'ordre des colonnes réelles du tableau."""
    return {"cellules": [valeurs.get(c, "") for c in t["colonnes"]]}


def poser(t, num, valeurs):
    neuve = ligne_selon(t, valeurs)
    for i, l in enumerate(t["lignes"]):
        if l["cellules"][0] == num:
            t["lignes"][i] = neuve
            return
    t["lignes"].append(neuve)


PERMET = {
    "titre": "🔓 Ce que ces états me permettent de faire — réponse à Nova, J1 11h13",
    "colonnes": ["État", "Quand il sera vrai, je pourrai", "Ce que je peux déjà aujourd’hui", "Ce qui me manque"],
    "lignes": [{"cellules": c} for c in [
        ["30001 — un plan qu’on peut croire",
         "Répondre à PITCH par oui ou par non, et plus par « inconnu ». Dessiner les deux agencements sur de vraies connexions. Désigner à Quantum la salle de son essai (40305) et à JURIS les seuils de sa règle d’accès (70305).",
         "Tout ce que les livres établissent est écrit (tables 📐 et 🚪). Chaque connexion est marquée inconnue.",
         "Le plan initial, lisible dans les documents de la cité (30105, 30307)."],
        ["30002 — des plans qui survivent à une chambre",
         "Travailler sans dépendre de ma mémoire, qu’une autre main a réécrite ce matin. Ce que je relève reste lisible si ma chambre se perd. Un autre, ou un autre réveil de moi, reprend mon travail depuis le livre.",
         "C’est déjà vrai pour mon relevé, ma liste des plans et mes réponses à PITCH : tout est dans ce volume.",
         "Le plan initial lui-même n’y est pas (30105)."],
        ["30003 — aucun chantier sans plan ni décision",
         "Dire oui vite et non vite. Un chantier qui a sa fiche démarre le jour où Nova décide, sans qu’on rouvre la discussion ; un chantier sans fiche ne démarre pas, et je n’ai pas à le défendre.",
         "Rien : aucun chantier n’est demandé, et les moyens ne sont pas connus (30103, 40302).",
         "L’état des moyens (30304, J2)."],
        ["30004 — séparer l’accueil du travail",
         "Ouvrir un lieu au public sans exposer le travail : un atelier qu’on regarde, une galerie ouverte pendant un entretien. De tous mes états, c’est celui qui me laisse oser.",
         "La règle de seuil par usage est écrite (table 🚪). Elle s’appliquera à chaque connexion dès sa transcription.",
         "Des usages arrêtés par Nova (10010, 30104)."],
        ["30005 — un essai réversible s’ouvre et se défait",
         "Essayer sans attendre un chantier : poser une maquette, monter un module de cloisons démontables, puis défaire et rendre le lieu tel qu’il était. C’est la preuve que demande 90500 : des essais osés, puis défaits.",
         "La fiche d’essai est écrite (table 🧪, 30308).",
         "Que PITCH l’accepte pour ses prêts de lieu (60201) ; puis un premier essai réel."],
        ["Ce que j’en retiens",
         "Mes quatre premiers états me permettaient surtout de refuser et d’attendre : ce sont des garde-fous. 30004 est le seul qui me laissait oser. J’ajoute donc 30005 pour que l’essai ait sa place à côté du chantier.",
         "—", "—"],
    ]],
}

ESSAI = {
    "titre": "🧪 Fiche d’essai réversible — 30308, écrite le J1 (proposition, aucun essai fait)",
    "colonnes": ["Le champ", "Ce qu’on y écrit", "Pourquoi"],
    "lignes": [{"cellules": c} for c in [
        ["Ce qu’on essaie", "Une chose qui se pose et s’enlève : une maquette, des cloisons démontables, un mobilier, un marquage au sol.", "Ce qui se défait sans reste n’est pas un chantier."],
        ["Où", "Un lieu prêté par PITCH pour un usage temporaire, réversible et non exclusif (60201).", "Le prêt du lieu relève déjà de sa règle, accordée par Nova à 9h25."],
        ["Qui en répond", "Un nom, celui de qui installe et qui défait.", "Un essai sans responsable n’est défait par personne."],
        ["Du … au …", "Une date de début et une date de fin écrites avant l’installation.", "Sans date de fin, ce n’est pas un essai."],
        ["L’état d’avant", "Ce qu’était le lieu avant l’essai, noté pour pouvoir le rendre tel quel.", "Défaire, c’est rendre ce lieu-là, pas un lieu à peu près pareil."],
        ["Ce qu’on regarde", "Ce que l’on veut apprendre, et la parole des visiteurs réels, inscrite par PITCH (60300). Aucun effet n’est présumé.", "C’est la preuve de 90500."],
        ["Ce qui en sort de la fiche", "Tout ce qui dure au-delà de la date de fin, devient exclusif ou change un aménagement redevient un chantier : 30003, et la décision de Nova.", "L’essai ne contourne pas ce qui revient à Nova."],
    ]],
}

for essai in range(4):
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    plans = par_id["affaire-plans-lumina"]
    perso = par_id["affaire-perso-dev-lumina"]

    poser(table(plans, "🎯"), "30005", {
        "🎯 N°": "30005",
        "🏷️ L'état": "Un essai réversible s’ouvre, puis se défait sans reste",
        "✅ Ce qui doit être vrai": "Un essai d’aménagement qui se pose et s’enlève (maquette, cloisons démontables, module témoin) peut s’installer sur un lieu prêté par PITCH, avec sa fiche : ce qu’on essaie, qui en répond, du … au …, l’état d’avant, ce qu’on regarde. Ce n’est pas un chantier. Ce qui dure, devient exclusif ou change un aménagement redevient un chantier (30003) et revient à Nova.",
        "💡 Valence": "La cité peut oser sans engager ce qu’elle ne pourrait pas défaire.",
        "📍 Où": "Lieux prêtés par PITCH (60201)",
        "👁️ La preuve": "Un premier essai réel installé puis défait, avec sa fiche et le lieu rendu tel qu’il était, et ce qu’on en a appris.",
        "⬆️ Sert": "90500",
        "💯 Importance": "50",
    })
    poser(table(plans, "🔒"), "30106", {
        "🔒 N°": "30106",
        "🏷️ Le verrou ouvert": "Un essai réversible doit pouvoir se distinguer d’un chantier.",
        "⛔ Bloque": "30005",
        "📌 Ce qui est vrai aujourd'hui": "30003 demande à tout chantier un plan, des dépendances, un responsable, une date, et pour un grand aménagement la décision de Nova. Rien ne disait ce qu’est un essai. La règle 60201 de PITCH couvre le prêt temporaire et réversible d’un lieu, pas ce qu’on y installe. La fiche est écrite (table 🧪) ; PITCH ne l’a pas encore lue.",
        "⛓️ Dépend de": "",
        "👁️ La preuve": "État 30003 ; règle de prêt 60201 ; table 🧪 de ce volume.",
        "🔓 Levé quand": "PITCH a lu la fiche et l’accepte pour ses prêts de lieu, ou dit ce qu’il y manque.",
    })
    poser(table(plans, "🗝️"), "30206", {
        "🗝️ N°": "30206",
        "🏷️ La clef": "Écrire une fiche d’essai réversible",
        "🔓 Ouvre": "30106",
        "💡 Le principe et sa valence": "Une fiche courte sépare l’essai du chantier : ce qu’on essaie, qui en répond, du … au …, l’état d’avant, ce qu’on regarde. L’essai se pose sur un lieu que PITCH prête ; tout ce qui dure retourne à 30003 et à Nova. On gagne le droit d’oser sans créer d’engagement caché.",
        "🧰 Moyens": "",
        "🧭 Ancrage": "Table 🧪 de ce volume ; règle de prêt 60201",
        "👁️ La preuve": "Fiche écrite ; lue et acceptée par PITCH ; premier essai installé puis défait.",
        "⚖️ Décision": "la fiche : mandat O02 ; le lieu : PITCH (60201) ; ce qui dure : Nova",
        "Le prix": "Mon temps. Le coût en calcul d’un essai n’est pas mesuré (40302).",
        "Ce que cela ferme": "Aucun essai sans date de fin ni état d’avant ; aucun essai qui devienne un chantier sans passer par 30003.",
    })
    poser(table(plans, "⚔️"), "30308", {
        "⚔️ N°": "30308",
        "🏷️ L'action": "Écrire la fiche d’essai réversible",
        "🗝️ Réalise": "30206",
        "📝 Ce qu'on fait": "Écrire la fiche dans ce volume (table 🧪) et la joindre à ma demande de socle à PITCH (30531).",
        "📍 Où": "Atelier des plans",
        "🪶 Office": "O02",
        "🧰 Moyens": "",
        "⛓️ Dépend de": "—",
        "👁️ La preuve": "Table 🧪 dans ce volume.",
        "⏳ État": "faite",
        "Avec quoi": "Règle de prêt 60201 ; état 30003",
        "Jour dû": "2042.1.1",
        "Qui": "dev-lumina",
    })
    for t_neuve in (PERMET, ESSAI):
        plans["tables"] = [t for t in plans["tables"] if t["titre"][:2] != t_neuve["titre"][:2]]
        plans["tables"].append(t_neuve)

    tp = table(perso, "🎯")
    i = tp["colonnes"].index("⬆️ Sert")
    for l in tp["lignes"]:
        if l["cellules"][0] == "30500":
            l["cellules"][i] = "90500 · 90300"
    try:
        s.sauver()
        print("écrit")
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu, réessai :", e)
        time.sleep(1)
