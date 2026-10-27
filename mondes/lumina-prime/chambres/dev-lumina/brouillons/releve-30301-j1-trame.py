# -*- coding: utf-8 -*-
"""DEV, réveil du contexte 30301 (relever le Radiant Core), J1, après le billet de PITCH
d'après 10h12. De ma main, pour l'action 30301 : remettre la table 📐 au format de la trame
de mon mémento (seuil / espaces reliés / usage de chaque côté / séparation / mesuré-convention-
inconnu / source et date / prochaine vérification) et poser la règle de seuil par usage.
Ne touche PAS aux lignes 30307, 30105 ni à la table 🗺️ : un autre réveil de moi (30307) les tient.
Ne touche qu'à affaire-plans-lumina ; aucun numéro ne change.
Écrit par la porte bibliotheque.ouvrir, racine absolue du monde ; relit et réessaie."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def L(*c):
    return {"cellules": list(c)}


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, num):
    for l in t["lignes"]:
        if l["cellules"][0].strip("* ") == num:
            return l
    raise KeyError(num)


def col(t, debut):
    for i, c in enumerate(t["colonnes"]):
        if debut in c:
            return i
    raise KeyError(debut)


RELEVE = {
    "titre": "📐 Relevé du Radiant Core — 30301, selon la trame du mémento (J1, connexions inconnues)",
    "colonnes": [
        "Pièce ou seuil",
        "Espaces reliés",
        "Usage de chaque côté",
        "Séparation nécessaire",
        "Mesuré · convention · inconnu",
        "Source et date",
        "Prochaine vérification",
    ],
    "lignes": [
        L("Hall",
          "Inconnus. Aucun volume de la cité ne porte ses connexions (30105).",
          "Côté accueil : les trois cas d’essai de PITCH y entrent (60301). Usage non arrêté (10001, 10010). Dans l’esquisse B, passage seul (30305).",
          "Séparer le passage du séjour (30004). Tout seuil vers l’atelier ou la salle du conseil suit la règle accueil ↔ travail (table suivante).",
          "Mesuré : rien. Convention : pièce au plan ; les coordonnées du dessin ne sont pas des mètres. Inconnu : connexions, surface.",
          "Mémento DEV ; 60301 (PITCH) ; J1.",
          "Transcription du plan (30307), puis parcours essayé sur place (30001)."),
        L("Salon des visiteurs",
          "Inconnus. On ne sait pas s’il touche la galerie ni par où on y entre.",
          "Côté accueil : lieu des entretiens dans les deux esquisses (30305). Aucune affectation (10001).",
          "Séjour hors du passage. S’il partage un seuil avec la galerie, ce seuil sépare au moins la vue. Le son n’est pas de l’architecture : aucune confidentialité promise (40104, 40205).",
          "Mesuré : rien. Convention : pièce au plan. Inconnu : connexions, surface, ce que le système garantit du son.",
          "Mémento DEV ; 30305 ; 40104 ; J1.",
          "30307 pour le seuil ; essai de Quantum (40305) pour le son."),
        L("Galerie des projets",
          "Inconnus.",
          "Côté accueil : PITCH y conduit les cas 1 et 3 (60301). Exposition dans les deux esquisses (30305). Usage non arrêté.",
          "Si elle reçoit du public pendant un entretien au salon, son seuil avec le salon ne doit pas être un passage (question 2 de PITCH).",
          "Mesuré : rien. Convention : pièce au plan. Inconnu : connexions, capacité (non mesurée, 40302).",
          "Mémento DEV ; 60301 ; J1.",
          "30307 ; capacité : mesure de Quantum (40302, J2)."),
        L("Atelier des plans",
          "Inconnus.",
          "Côté travail : j’y tiens mes heures. Le parcours visiteur ne doit pas le traverser (60301).",
          "Tout seuil vers le hall, le salon ou la galerie suit la règle accueil ↔ travail.",
          "Mesuré : rien. Convention : pièce au plan. Inconnu : connexions.",
          "Mémento DEV ; 60301 ; J1.",
          "30307."),
        L("Salle du conseil",
          "Inconnus.",
          "Côté travail : le conseil y siège (J1, 9h03). Hors du parcours visiteur (60301). Règle d’accès : Nova (70202).",
          "Tout seuil vers le hall, le salon ou la galerie suit la règle accueil ↔ travail.",
          "Mesuré : rien. Convention : pièce au plan. Inconnu : connexions.",
          "Mémento DEV ; 60301 ; affaire de JURIS, 70202 ; J1.",
          "30307."),
        L("Accès depuis le Quai commun",
          "Le Quai commun et au moins une pièce du Radiant Core, laquelle est inconnue.",
          "Côté public : promenade du quai (atlas). Côté Radiant Core : inconnu tant qu’on ignore la pièce desservie.",
          "Un ruban lumineux dans le sol distingue déjà la promenade des accès (atlas).",
          "Mesuré : rien. Convention : un accès local vaut une minute de navigation VR (atlas, page 1). Inconnu : nombre et place des accès, pièce desservie.",
          "Atlas, ligne « Quai commun » et page 1 ; J1.",
          "Accès locaux M202 (30307) ; relevé du Quai commun avec Gaia (30302, 50301)."),
    ],
}

REGLE = {
    "titre": "🚪 Règle de seuil par usage — 30301, à appliquer à chaque connexion dès sa transcription",
    "colonnes": [
        "Seuil entre",
        "Pièces du Radiant Core concernées",
        "Ce que le seuil doit faire",
        "Ce qu’il ne promet pas",
        "Source",
    ],
    "lignes": [
        L("Accueil ↔ accueil",
          "Hall, salon des visiteurs, galerie des projets (côté accueil selon 60301 ; usage non arrêté, 10010).",
          "Séparer le passage du séjour. Laisser une place où attendre hors du trajet (question 3 de PITCH). Si le salon ne s’atteint qu’à travers la galerie, l’esquisse B (galerie d’exposition) croise l’entretien : je le noterai dans la comparaison 30305.",
          "Aucune confidentialité (40104, 40205). Aucun usage : Nova (10010).",
          "30004 ; mémento DEV, « Seuils et repères » ; 30305."),
        L("Accueil ↔ travail",
          "Hall, salon ou galerie, d’un côté ; atelier des plans ou salle du conseil, de l’autre.",
          "Se lire comme une limite : le visiteur voit ce qui s’ouvre à lui et ce qui reste au travail. Le parcours visiteur ne le franchit pas. Si une pièce d’accueil ne s’atteint qu’à travers une pièce de travail, le parcours 10020 ne tient pas : je le signale à PITCH et à Aria (10022), et la décision d’aménagement revient à Nova.",
          "Aucun droit d’accès : JURIS (70202, 70305). Aucune confidentialité technique : Quantum (40205).",
          "30004 ; 60301 ; mémento DEV."),
        L("Travail ↔ travail",
          "Atelier des plans et salle du conseil.",
          "Aucune séparation d’architecture exigée entre deux pièces de travail.",
          "Rien sur la règle d’accès de la salle du conseil : Nova (70202).",
          "60301 ; mémento DEV."),
        L("Dehors ↔ Radiant Core",
          "Quai commun et la pièce, encore inconnue, où mène chaque accès.",
          "Le ruban lumineux distingue déjà la promenade des accès. L’accès mène de préférence au côté accueil ; s’il mène à une pièce de travail, la règle accueil ↔ travail s’applique à ce seuil.",
          "Aucune mesure : un accès vaut une minute de navigation VR, par convention.",
          "Atlas, « Quai commun » et page 1 ; 30004."),
    ],
}


def corriger(a):
    # 1) la table 📐 remplacée en place (même position), au format de la trame
    idx = next(i for i, t in enumerate(a["tables"]) if t["titre"].startswith("📐"))
    a["tables"][idx] = RELEVE
    # 2) la règle de seuil, juste après, si elle n'y est pas déjà
    if not any(t["titre"].startswith("🚪") for t in a["tables"]):
        a["tables"].insert(idx + 1, REGLE)
    # 3) la ligne 30301
    act = table(a, "⚔️")
    l = ligne(act, "30301")["cellules"]
    l[col(act, "Ce qu'on fait")] = (
        "Pour chaque seuil du hall, du salon des visiteurs, de la galerie des projets, de l’atelier des plans "
        "et de la salle du conseil : les espaces reliés, l’usage de chaque côté, le besoin de séparation ; un "
        "accès dessiné noté à part d’un accès essayé. C’est le même travail que l’action 10021 de l’affaire "
        "d’accueil : il ne se fait qu’une fois. Il sert 10020, 10022, 70305 et 40305. J1 : la table 📐 suit la "
        "trame du mémento, pièce par pièce, et sépare ce qui est mesuré (rien), ce qui est convention du plan "
        "et ce qui est inconnu. La table 🚪 dit ce que chaque seuil devra faire selon l’usage de chaque côté ; "
        "elle s’applique à chaque connexion dès sa transcription. Les connexions attendent 30307.")
    l[col(act, "Avec quoi")] = ("Plan initial (M201) et accès locaux (M202) quand 30307 les aura transcrits ; "
                                "mandat de DEV ; trame du mémento (M212) ; atlas (M203) ; parcours 60301")
    # 4) l'état actuel
    ouv = table(a, "🏰")
    for r in ouv["lignes"]:
        if r["cellules"][0] == "L’ÉTAT ACTUEL":
            r["cellules"][1] = (
                "Sept lieux sont au plan, avec des tracés schématiques et sans mesure. Le relevé du Radiant Core "
                "est écrit pour tout ce que les livres établissent, selon la trame (table 📐), avec la règle de "
                "seuil par usage (table 🚪). Ses connexions ne sont portées par aucun volume de la cité (30105) : "
                "elles sont marquées inconnues. La liste des plans est commencée (table 🗺️). Aucun chantier "
                "n’est lancé. Aucune action n’est faite.")


for essai in range(5):
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    corriger(par_id["affaire-plans-lumina"])
    try:
        s.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu :", e)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
