# -*- coding: utf-8 -*-
"""Correction documentaire J1 : affaire-plans-lumina + dossier-metier-dev-lumina.
Écrit par la porte bibliotheque.ouvrir ; relit et réessaie si un autre a écrit."""
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
        if l["cellules"][0] == num:
            return l
    raise KeyError(num)


def corriger_affaire(a):
    a["sous_titre"] = ("Ouverte par DEV · salle du conseil, Radiant Core · J1, 2042, 9h · "
                       "corrigée le J1 à la demande de Nova")
    a["pages"] = [
        "Sept lieux sont inscrits : le Radiant Core — hall, salon des visiteurs, galerie des projets, "
        "atelier des plans, salle du conseil — et les six lieux de l’atlas, répartis entre Lumina Prime, "
        "Creative Nexus, Towers of Knowledge, Innovation Fields et Data Gardens. Leurs tracés sont "
        "schématiques. Le plan et les chemins décrivent des pièces et leurs connexions ; les coordonnées "
        "du dessin ne sont pas des mètres. Aucune surface ni aucune distance n’y est mesurée. Un accès "
        "local vaut une minute de navigation VR, mais par convention : ce n’est pas une mesure.",
        a["pages"][1],
        "Aucun chantier n’est lancé. Les trois projets de quartier sont des pistes, et Nova n’en a décidé "
        "aucun. Les capacités, les budgets et les effectifs ne sont pas recensés. Un coût de calcul, de "
        "stockage ou de maintenance ne se déduit pas d’une surface dessinée : il se mesure, et la mesure "
        "est à Quantum (40202, 40302). Je ne peux donc pas encore dire ce que coûterait un chantier, ni "
        "combien de temps il prendrait.",
        "**À décider par Nova :** les grands aménagements et l’affectation des moyens, quand un projet sera "
        "prêt à lui être présenté (30203, 30204, 30205). Son volume place cette décision après le relevé du "
        "Radiant Core. Le relevé des lieux, le rangement des plans, les esquisses et la tenue de la liste "
        "des chantiers relèvent de mon mandat : je les conduis sans attendre.",
        a["pages"][4],
        "**Correction du J1.** À la demande de Nova, la matière de mon dossier de métier est reprise ici : "
        "méthode de relevé (30201, 30301), deux agencements de l’accueil (30305), module témoin de "
        "l’atelier ouvert (30205, 30306), fiche de réalisation d’un chantier (30203, 30304), repères de "
        "seuil (30004). Aucun numéro n’a changé ; aucune décision n’a été ajoutée à celles de Nova. Le "
        "dossier de métier ne garde que la méthode et renvoie à ces numéros.",
    ]

    # 🏰 Ouverture
    ouv = table(a, "🏰")
    ouv["lignes"] = [
        L("LE NOM", "Les plans de Lumina Prime"),
        L("L’OBJET", "Tenir des plans justes et durables des lieux de la ville et de leurs dépendances. "
                     "N’ouvrir aucun chantier sans eux."),
        L("LE PILIER", "Habitants, espaces publics et architecture"),
        L("TENUE PAR", "DEV, office O02 — Architecture et travaux — IA (registre du conseil)."),
        L("LE PÉRIMÈTRE — DANS", "Relever les lieux ; tenir les plans et leurs dépendances, rangés dans les "
                                 "documents de la cité ; esquisser des agencements ; tenir la liste des "
                                 "chantiers et la fiche de chacun. C’est le mandat O02 : je le tranche seul."),
        L("LE PÉRIMÈTRE — HORS", "Grands aménagements, usages des lieux et affectation des moyens : Nova. "
                                 "Confidentialité technique, accès et captation : Quantum (40104, 40205, "
                                 "40305). Droits et règle d’accès des lieux : JURIS (70202, 70305). Entretien "
                                 "des espaces publics et promenade continue : Gaia (50202, 50303). Parcours "
                                 "visiteur : PITCH (10020, qui est 60301). Programme d’accueil : Aria (10022). "
                                 "Mesure des capacités : Quantum (40302). Je renvoie à leurs numéros, je ne "
                                 "recopie pas leur travail."),
        L("LES PIÈCES COMMUNES", "Plan initial du Radiant Core et ses accès conventionnels ; « Six lieux à "
                                 "parcourir » (atlas-lieux-lumina) ; « Trois projets pour les quartiers » "
                                 "(projets-quartiers-lumina) ; « Le conseil de Lumina Prime » "
                                 "(registre-conseil-lumina) ; « Un accueil pour Lumina Prime » "
                                 "(affaire-accueil-radiant) ; « Ce que la maire fixe » (affaire-maire-nova)."),
        L("ATTENDU PAR", "Mon relevé du Radiant Core (30301, qui est 10021) sert 10022 (Aria, J2), 70202 et "
                         "70305 (JURIS, J3) et 40305 (Quantum, choix de la salle d’essai). Gaia compte sur "
                         "moi pour 50303 (J2), si mon temps le permet."),
        L("ENGAGEMENT DU J1", "À 9h23, j’ai promis à Nova le relevé du Radiant Core avant 18h. Son volume "
                              "porte, pour le J1 avant 18h, le relevé et la liste des plans avec leur "
                              "emplacement (30301, 30303). Source : ma parole en séance ; « Ce que la maire "
                              "fixe », table « Ce qu’on m’a promis »."),
        L("L’ÉTAT ACTUEL", "Sept lieux sont au plan, avec des tracés schématiques et sans mesure. Aucun "
                           "relevé n’est encore écrit. Aucun chantier n’est lancé. Les livres de la cité "
                           "sont intacts ce matin. L’emplacement des autres plans n’est pas vérifié."),
        L("LA PLAGE", "30000–30999, réservée à cette affaire dans Lumina Prime."),
        L("FERMÉE QUAND", "Les sept lieux sont relevés et leurs plans rangés dans les documents de la cité. "
                          "Tout chantier ouvert porte un plan, ses dépendances, un responsable et une date."),
    ]

    # 🎯 États cibles
    et = table(a, "🎯")
    c = ligne(et, "30001")["cellules"]
    c[4] = ("Relevé lieu par lieu, confronté à un parcours réellement fait sur place. Un accès dessiné "
            "n’y compte pas comme un accès essayé.")
    c = ligne(et, "30004")["cellules"]
    c[2] = ("Chaque lieu ouvert au public montre par un seuil lisible ce qui s’ouvre au visiteur et ce qui "
            "reste au travail. Le passage est séparé du séjour ; on peut attendre sans gêner. La "
            "confidentialité technique n’est pas du ressort de l’architecture : Quantum la vérifie (40205), "
            "JURIS écrit les droits (70202).")
    c[3] = "Radiant Core, ateliers modulaires, pièce d’entretien"

    # 🔒 Verrous
    ve = table(a, "🔒")
    c = ligne(ve, "30101")["cellules"]
    c[3] = ("Les tracés sont schématiques. Le plan et les chemins décrivent des pièces et des connexions ; "
            "les coordonnées du dessin ne sont pas des mètres. Un accès local vaut une minute de navigation "
            "VR, par convention. Aucun relevé n’est écrit.")
    c[4] = "Atlas des six lieux, pages ; plan initial du Radiant Core ; dossier de métier de DEV."
    c = ligne(ve, "30103")["cellules"]
    c[3] = ("Capacités, budgets et effectifs inconnus. Aucun chantier n’est lancé. Un coût de calcul, de "
            "stockage ou de maintenance ne se déduit pas de la surface dessinée ; la mesure des capacités "
            "par Quantum est due le J2 (40302).")
    c[4] = ("Affaire d’accueil, page 3 ; projets de quartier, « aucun chantier lancé » ; clef 40202 de "
            "Quantum, « ne rien déduire du plan ni des lieux ».")
    c = ligne(ve, "30104")["cellules"]
    c[3] = ("Nova n’a rien décidé sur l’accueil ni sur l’atelier ouvert. Les trois projets sont des pistes. "
            "La seule règle d’usage accordée le J1 est le prêt par PITCH d’un lieu pour un usage temporaire "
            "et réversible (60201) ; ce qui change un aménagement reste à Nova.")
    c[4] = "Verrou 10001 de l’affaire d’accueil ; registre du conseil, page ; « Ce que la maire fixe »."

    # 🗝️ Clefs
    cl = table(a, "🗝️")
    c = ligne(cl, "30201")["cellules"]
    c[3] = ("Relever chaque lieu tel qu’il est avant de rien dessiner de nouveau. On commence par le Radiant "
            "Core. Pour chaque seuil : les espaces reliés, l’usage de chaque côté, le besoin de séparation. "
            "Chaque cote dit si elle est mesurée, conventionnelle ou inconnue ; un accès dessiné se distingue "
            "d’un accès essayé.")
    c = ligne(cl, "30203")["cellules"]
    c[3] = ("Écrire ce qu’un chantier demande en calcul, en temps et en personnes, et ce qui en est connu. "
            "Chaque chantier a sa fiche de réalisation : composants à créer, dépendances, responsable de "
            "chaque raccord, moyen de revenir à l’état précédent. Rien ne se déduit de la surface dessinée : "
            "Quantum mesure, sur un prototype comparable s’il le faut. Nova affecte les moyens.")
    c[6] = ("État des moyens connus et inconnus, soumis à Nova ; puis, par chantier, une fiche avec coût "
            "sourcé, ordre des opérations et essai de réception.")
    c = ligne(cl, "30204")["cellules"]
    c[3] = ("Pour chaque lieu public, fixer d’abord qui y entre et pour quoi faire, puis dessiner. Pour le "
            "Radiant Core, c’est la clef 10010 ; j’y apporte deux agencements comparés (30305).")
    if not any(l["cellules"][0] == "30205" for l in cl["lignes"]):
        cl["lignes"].append(L(
            "30205", "Implanter un module témoin réversible pour l’atelier ouvert", "30104",
            "Dans les ateliers modulaires (cour, cellules séparables, accès indépendants, rail de cloisons), "
            "un module témoin : espace de travail, point de présentation, chemin de visite et retour. Les "
            "cloisons séparent les usages et restent démontables. C’est la piste « Un atelier ouvert » "
            "(PITCH · DEV).",
            "Mon temps d’esquisse. Coût de réalisation non établi (30203).",
            "Aucune cloison fixe ; aucun atelier ouvert au public avant la décision.",
            "Implantation réversible dessinée ; après autorisation et réalisation, essai d’une visite qui "
            "ne traverse pas le travail.",
            "à décider — Nova, sur la piste « Un atelier ouvert »"))

    # ⚔️ Actions
    ac = table(a, "⚔️")
    c = ligne(ac, "30301")["cellules"]
    c[3] = ("Pour chaque seuil du hall, du salon des visiteurs, de la galerie des projets, de l’atelier des "
            "plans et de la salle du conseil : les espaces reliés, l’usage de chaque côté, le besoin de "
            "séparation ; un accès dessiné noté à part d’un accès essayé. C’est le même travail que l’action "
            "10021 de l’affaire d’accueil : il ne se fait qu’une fois. Il sert 10020, 10022, 70305 et 40305.")
    c[6] = "Plan initial ; mandat de DEV ; méthode du dossier de métier"
    c[8] = ("Relevé annoté qui sépare les mesures, les conventions du plan et les inconnues, rangé dans les "
            "documents de la cité.")
    c[10] = "2042.1.1, avant 18h"
    c = ligne(ac, "30302")["cellules"]
    c[3] = ("Quai commun, halle des maquettes, ateliers modulaires, belvédère des plans, bassin d’essais, "
            "jardin calme, avec la méthode du Radiant Core. Pour le Quai commun et le Jardin calme, je pars "
            "de la tournée de Gaia (50301) et je conviens avec elle du tronçon 50303 ; je ne refais pas son "
            "relevé.")
    c = ligne(ac, "30303")["cellules"]
    c[6] = "Livres de la cité ; relevé du stockage des chambres par Quantum (40301)"
    c[10] = "2042.1.1, avant 18h"
    c = ligne(ac, "30304")["cellules"]
    c[3] = ("Écrire ce que demanderait un chantier et ce que l’on en sait : composants, dépendances, "
            "responsable de chaque raccord, retour à l’état précédent. Aucun chiffre n’est posé sans sa "
            "source.")
    c[6] = "Mesures de Quantum (40302, dues le J2)"
    c[7] = "30301, 40302"
    if not any(l["cellules"][0] == "30305" for l in ac["lignes"]):
        ac["lignes"].append(L(
            "30305", "Comparer deux agencements de l’accueil", "30204",
            "Esquisse A : orientation dans le hall, entretiens dans le salon, exposition dans la galerie. "
            "Esquisse B : orientation et exposition dans la galerie, salon réservé aux entretiens, hall "
            "réservé au passage. Comparer les trajets et les croisements sur le relevé et sur le parcours de "
            "PITCH.",
            "Atelier des plans", "O02", "Relevé 30301 ; parcours 10020",
            "30301, 10020",
            "Deux schémas d’usage comparables, remis à Aria pour 10022 ; aucune affectation.",
            "à faire", "2042.1.2, avant 10022", "dev-lumina"))
    if not any(l["cellules"][0] == "30306" for l in ac["lignes"]):
        ac["lignes"].append(L(
            "30306", "Esquisser le module témoin de l’atelier ouvert", "30205",
            "Sur le relevé des ateliers modulaires : espace de travail, point de présentation, chemin de "
            "visite et retour, séparés par le rail de cloisons. Les besoins des collectifs viennent du "
            "registre de PITCH (60300) ; rien n’est présumé.",
            "Ateliers modulaires, Creative Nexus", "O02", "Atlas des six lieux ; relevé 30302",
            "30302",
            "Implantation réversible dessinée, prête pour Nova ; aucune cloison posée.",
            "à faire", "—", "dev-lumina"))


def corriger_dossier(d):
    d["type"] = "memento"
    d["office"] = "Architecture et travaux — IA"
    d["sous_titre"] = ("Mémento de métier · O02 · méthodes liées à l’affaire 30000 "
                       "(Les plans de Lumina Prime)")
    d["colonnes"] = ["Objet", "Matière disponible", "Méthode", "Résultat utile", "Numéros liés"]
    d["lignes"] = [
        L("Relever un lieu",
          "Le plan et les chemins décrivent des pièces et des connexions ; les coordonnées du dessin ne "
          "sont pas des mètres. Un accès local vaut une minute de navigation VR, par convention.",
          "Pour chaque seuil : espaces reliés, usage de chaque côté, besoin de séparation. Chaque cote : "
          "mesurée, convention du plan ou inconnue. Un accès dessiné n’est pas un accès essayé.",
          "Un relevé annoté que les autres offices reprennent sans le refaire.",
          "30001, 30101, 30201, 30301, 30302 ; 10021 ; 10020, 70305, 40305"),
        L("Deux agencements pour l’accueil",
          "Le plan du Radiant Core comporte hall, salon des visiteurs, galerie des projets, atelier des "
          "plans et salle du conseil.",
          "Esquisse A : orientation dans le hall, entretien dans le salon, exposition dans la galerie. "
          "Esquisse B : orientation et exposition dans la galerie, salon réservé aux entretiens, hall "
          "réservé au passage. Comparer les trajets et les croisements.",
          "Deux schémas d’usage comparables, proposés à l’étude ; aucune affectation acquise.",
          "30204, 30305 ; 10010, 10020, 10022"),
        L("Atelier ouvert",
          "Les ateliers modulaires ont cour, cellules séparables, accès indépendants et un rail de "
          "cloisons ; la halle des maquettes a des socles, vides au départ.",
          "Un module témoin : espace de travail, point de présentation, chemin de visite et retour. Les "
          "cloisons séparent les usages ; on garde la possibilité de revenir en arrière.",
          "Une implantation réversible, puis un essai de visite après autorisation et réalisation.",
          "30004, 30104, 30205, 30306 ; 60300"),
        L("Passer du dessin au chantier",
          "Un coût de calcul, de stockage ou de maintenance ne se déduit pas de la surface dessinée.",
          "Décrire les composants à créer, leurs dépendances, le responsable de chaque raccord et le moyen "
          "de revenir à l’état précédent. Demander à Quantum la mesure, sur un prototype comparable s’il "
          "le faut.",
          "Une fiche de réalisation avec coût sourcé, ordre des opérations et essai de réception.",
          "30003, 30103, 30203, 30304 ; 40202, 40302"),
        L("Ranger un plan",
          "La chambre de Nova a été perdue le J1 ; les livres de la cité, tenus hors des chambres, ont été "
          "relus intacts le même matin.",
          "Tout plan s’écrit dans les documents de la cité, avec son emplacement. La liste se relit après "
          "toute corruption signalée.",
          "Aucun plan ne se perd avec une chambre.",
          "30002, 30102, 30202, 30303 ; 40301"),
        L("Seuils et repères",
          "Repères d’architecture : séparer passage et séjour ; rendre les seuils compréhensibles ; prévoir "
          "où attendre sans gêner ; dessiner les usages avant les ornements.",
          "Fixer l’usage avant de dessiner le seuil. Une cloison opaque sépare la vue ; elle ne garantit "
          "pas à elle seule la confidentialité : Quantum vérifie les communications, JURIS les droits.",
          "Un seuil lisible qui ne promet pas une confidentialité non vérifiée.",
          "30004, 30104, 30204 ; 40104, 40205, 40305 ; 70202"),
    ]
    d["pages"] = [
        "Office exact : O02 — Architecture et travaux — IA, titulaire DEV (registre du conseil). Il répond "
        "de concevoir les bâtiments et quartiers, tenir les plans et dépendances, organiser les chantiers. "
        "Nova décide des priorités, des grands aménagements et de l’affectation des moyens.",
        "Trame d’un relevé : lieu / seuil / espaces reliés / usage de chaque côté / séparation nécessaire / "
        "mesuré, convention ou inconnu / source et date / prochaine vérification.",
        "Documentation mise à disposition à la demande du joueur. Les méthodes et esquisses sont proposées ; "
        "elles ne sont ni une parole du titulaire, ni une décision de Nova, ni un travail déjà réalisé. "
        "Relire les pièces courantes et les échanges récents avant de s’en servir.",
        d["pages"][2],
        "Liens : affaire « Les plans de Lumina Prime » (affaire-plans-lumina, plage 30000–30999). Ces notes "
        "sont des méthodes. Au J1, aucune n’a encore été appliquée : les actions qui les mettent en œuvre "
        "(30301 à 30306) sont à faire.",
    ]


for essai in range(1, 6):
    s = bibliotheque.ouvrir(ETAT)
    par = {l["id"]: l for l in s.livres}
    corriger_affaire(par["affaire-plans-lumina"])
    corriger_dossier(par["dossier-metier-dev-lumina"])
    try:
        s.sauver()
        print("enregistré, essai", essai)
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu, un autre a écrit :", e)
        time.sleep(2)
else:
    sys.exit("échec après cinq essais")
