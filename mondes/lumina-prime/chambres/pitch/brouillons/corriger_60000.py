raise SystemExit("PÉRIMÉ (J1) : script déjà servi ; il réécrirait des cellules depuis une lecture ancienne. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""Correction documentaire du J1 : affaire 60000 et dossier de métier de PITCH."""
import os
import sys

DEPOT = r"C:/Users/reyno/le-conseil2"
ETAT = os.path.join(DEPOT, "mondes", "lumina-prime", "etat")
sys.path.insert(0, os.path.join(DEPOT, "scripts"))
sys.path.insert(0, os.path.join(DEPOT, "scripts", "noyau"))
import bibliotheque  # noqa: E402


def ligne(*c):
    return {"cellules": list(c)}


def corriger_affaire(a):
    a["pages"] = [
        "Mon office accueille habitants et visiteurs, accompagne les collectifs et leur trouve des lieux (O05, registre du conseil). Au matin du J1, aucun livre de la cité ne nomme un habitant, un collectif ou une demande. L’atlas précise que ses six lieux n’ont aucun occupant nommé. Je pars de zéro, et je compte avant d’affirmer.",
        "**Décidé par Nova le J1 à 9h25** (volume « Ce que la maire fixe », table ⚖️, « accordé ») : je prête seul un lieu pour un usage temporaire et réversible ; le durable ou l’exclusif lui revient ; les conflits vont à JURIS. C’est la clef 60201. Il me reste à l’écrire en règle (60302, promise pour le J2). **Reste à Nova :** le programme d’accueil (60202, qui est la clef 10010 d’Aria, présentée le J2 par 10022). Chaque prêt durable ou exclusif lui sera soumis au cas par cas.",
        "**Périmètre.** Je tiens les arrivants, les collectifs, leurs demandes de lieu et leur suite. Je ne recopie pas le travail des autres offices, je le cite par son numéro. La règle d’accès de chaque lieu relève de JURIS (70002, 70305). Les litiges passent par sa voie (70303). Le relevé des espaces du Radiant Core relève de DEV (10021, qui est 30301). Les capacités de calcul, de stockage et de réseau relèvent de Quantum (40302). L’entretien des espaces publics revient à Gaia (50000). Les décisions et demandes générales de la cité sont tenues par Aria (20201, 20202).",
        "Ce qui reste inconnu et que je n’invente pas : le nombre d’habitants et de visiteurs, la fréquentation, la capacité des lieux, le coût en calcul d’une ouverture et les moyens de mon office. Les pistes du registre des projets, dont « Un atelier ouvert » (PITCH · DEV), ne sont pas des demandes reçues. Les capacités, budgets et effectifs se trouvent en 40302, 30304 et 50105.",
        "**Terminé quand :** une personne arrivée au hall est reçue et orientée, et un collectif réel qui demande un lieu repart avec un lieu prêté à des conditions écrites ou avec un refus motivé, inscrit au registre des arrivants."
    ]
    for t in a["tables"]:
        titre = t["titre"]
        if "Ouverture" in titre:
            t["lignes"] = [
                ligne("LE NOM", "Qui vient, et où le mettre"),
                ligne("L’OFFICE", "O05 — Habitants et activités — IA, tenu par PITCH (registre du conseil)."),
                ligne("L’OBJET", "Savoir qui vit et passe à Lumina Prime, recevoir chaque arrivant, et donner aux collectifs un lieu pour leurs projets."),
                ligne("LE PILIER", "Habitants, espaces publics et architecture"),
                ligne("DEDANS", "Le registre des arrivants et des collectifs (60300). Le parcours visiteur (60301, même travail que 10020). Le prêt temporaire et réversible d’un lieu, selon la règle accordée par Nova (60201). Le recueil des besoins d’un collectif réel (60304). L’essai d’une arrivée, une fois l’accueil réalisé (60305)."),
                ligne("DEHORS", "Programme et affectation de l’accueil : Nova, sur la clef 10010 portée par Aria (10022). Relevé du Radiant Core : DEV, 10021 = 30301. Règle d’accès des lieux : JURIS, 70305. Litiges : JURIS, 70303. Capacités : Quantum, 40302 ; moyens de chantier : DEV, 30304. Registres des décisions et des demandes : Aria, 20201 et 20202. Je renvoie, je ne recopie pas."),
                ligne("L’ÉTAT ACTUEL", "Aucun habitant, visiteur, collectif ou demande n’est inscrit dans les livres. La règle de prêt des lieux est accordée par Nova, mais elle n’est pas encore écrite. Aucune action de cette affaire n’est faite."),
                ligne("FAIT SOURCÉ", "Les six lieux de l’atlas n’ont aucun occupant nommé. Ils ne prouvent ni un effectif, ni une capacité technique, ni un budget. Source : atlas des lieux, page 2."),
                ligne("FAIT SOURCÉ", "Nova a accordé à PITCH, le J1 à 9h25, le prêt seul d’un lieu pour un usage temporaire et réversible. Le durable ou l’exclusif revient à Nova, les conflits vont à JURIS. Source : volume « Ce que la maire fixe », table ⚖️. Aria la note à 9h30 dans 20101 et en fera la première ligne du registre des décisions (20303)."),
                ligne("FAIT SOURCÉ", "Nova tient deux engagements de PITCH : le parcours visiteur remis à Aria le J1 avant 16h, et la règle écrite du prêt des lieux le J2. Source : volume « Ce que la maire fixe », table ⏳."),
                ligne("FAIT SOURCÉ", "La priorité de 60002 parmi les états visés par la cité est « à fixer ». Source : volume « Ce que la maire fixe », table 🎯."),
                ligne("LA PLAGE", "60000–60999, réservée à cette affaire dans Lumina Prime. En usage : 60000–60002, 60100–60103, 60200–60203, 60300–60305."),
                ligne("FERMÉE QUAND", "Un arrivant est reçu et orienté au hall, et une demande réelle de lieu a été traitée jusqu’au bout."),
            ]
        elif "États cibles" in titre:
            for l in t["lignes"]:
                c = l["cellules"]
                if c[0] == "60000":
                    c[4] = "Registre des arrivants et des collectifs (60300). Chaque ligne donne la personne ou le collectif rencontré, l’intention exprimée, l’espace adapté, l’accès à vérifier, le besoin d’accompagnement, le retour convenu et la source. Aucune estimation sans compte."
        elif "Verrous" in titre:
            for l in t["lignes"]:
                c = l["cellules"]
                if c[0] == "60101":
                    c[3] = "Aucun espace d’accueil n’est affecté (verrou 10001 de l’affaire d’accueil). La décision sur l’usage des espaces d’accueil est ouverte chez Nova. Aria lui présente le programme le J2 (10022)."
                    c[4] = "Affaire « Un accueil pour Lumina Prime » ; volume « Ce que la maire fixe », table ⚖️."
                elif c[0] == "60102":
                    c[3] = "LEVÉ le J1 à 9h25. Nova a fixé ce que je prête seul (temporaire et réversible) et ce qui lui revient (durable ou exclusif). Les conflits vont à JURIS. La règle n’est pas encore écrite : c’est l’action 60302, due le J2."
                    c[4] = "Volume « Ce que la maire fixe », table ⚖️ : « J1, 9h25 — accordé ». Atlas des lieux, page 2 : aucun lieu ne porte de règle d’attribution."
            t["lignes"].append(ligne(
                "60103",
                "Les lieux n’ont ni capacité ni règle d’accès connues",
                "60002",
                "Les six lieux de l’atlas ne portent ni capacité, ni droit d’usage. Aucune règle d’accès n’est écrite (70102). L’isolation du Bassin d’essais reste à vérifier. Les écrans du Jardin calme ne garantissent pas la confidentialité à eux seuls.",
                "Atlas des lieux, pages 1 et 2 ; verrou 70102 de JURIS.",
                "JURIS dresse la règle d’accès lieu par lieu (70305, J3). Pour un lieu donné, j’ai vérifié sur place ce qu’il permet (60203)."))
        elif "Clefs" in titre:
            for l in t["lignes"]:
                c = l["cellules"]
                if c[0] == "60201":
                    c[3] = "Temporaire et réversible : je prête seul. Durable ou exclusif : Nova. Conflit d’usage : JURIS (70303). Un changement d’aménagement relève déjà de Nova, qui décide des grands aménagements (registre du conseil)."
                    c[4] = "Une décision de Nova, obtenue le J1 à 9h25. L’écriture de la règle (60302)."
                    c[6] = "Décision de Nova inscrite à son volume (⚖️) et portée au registre des décisions par Aria (20303). Règle écrite ici (60302)."
                    c[7] = "accordée par Nova, J1 9h25"
                elif c[0] == "60202":
                    c[3] = "Clef 10010 de l’affaire d’accueil, tenue par Aria. J’y porte le parcours visiteur (10020 = 60301). Aria présente le programme à Nova le J2 (10022)."
            t["lignes"].append(ligne(
                "60203",
                "Montrer le lieu avant de le promettre",
                "60103",
                "J’associe une demande réelle à un lieu selon son usage dans l’atlas. La Halle sert à montrer une maquette, les Ateliers à créer et essayer, le Quai à se retrouver, le Jardin à se retirer, le Belvédère à lire les plans, le Bassin aux essais VR, sous réserve de son isolation. Je vérifie ensuite l’accès, le besoin d’aide et la compatibilité avec les autres usages. Le demandeur voit ce que le lieu permet avant que je promette une disponibilité.",
                "Mon temps sur place, 1 minute de navigation VR par accès local (convention de l’atlas). Accès : 70305 de JURIS.",
                "Aucune disponibilité promise sans vérification du lieu.",
                "Fiche de la demande au registre 60300 : lieu vu, accès vérifié ou marqué inconnu, conditions écrites.",
                "dans mon mandat, si le prêt est temporaire et réversible (60201)"))
        elif "Actions" in titre:
            for l in t["lignes"]:
                c = l["cellules"]
                if c[0] == "60300":
                    c[3] = "Poser les colonnes de la fiche : personne ou collectif rencontré, intention exprimée, espace adapté, accès à vérifier, besoin d’accompagnement, retour convenu, source. N’inscrire que des personnes rencontrées ou des demandes reçues. Je mets en relation, je ne parle pas à la place des habitants."
                    c[6] = "Mon mandat ; aucune donnée préexistante (atlas, page 2)"
                elif c[0] == "60301":
                    c[3] = "C’est l’action 10020 de l’affaire d’accueil : un seul travail. Trois cas d’essai, qui ne sont pas des visiteurs présents : une première visite, un rendez-vous municipal, la présentation d’un projet. Pour chacun : l’arrivée, l’information utile, l’orientation, l’attente éventuelle et la sortie, dans le hall, le salon et la galerie."
                    c[8] = "Parcours décrit sans fréquentation inventée, remis à Aria pour 10022. Les besoins spatiaux sont signalés à DEV (10021)."
                    c[10] = "2042.1.1, avant 16h"
                elif c[0] == "60302":
                    c[1] = "Écrire la règle de prêt des lieux"
                    c[3] = "Écrire les trois cas accordés par Nova le J1 à 9h25, avec ce qu’un prêt doit porter : le lieu, l’usage, la durée, la manière de rendre le lieu, le retour convenu. Renvoyer les accès à 70305 et les conflits à 70303."
                    c[5] = "O05"
                    c[6] = "Décision de Nova (volume « Ce que la maire fixe ») ; atlas des lieux ; registre du conseil"
                    c[8] = "Règle écrite dans cette affaire. La décision de Nova est déjà inscrite à son volume et portée au registre des décisions (20303)."
                    c[9] = "à faire — décision obtenue le J1 à 9h25, écriture due le J2"
            t["lignes"].extend([
                ligne("60303", "Traiter la première demande réelle de lieu", "60203",
                      "Inscrire la demande. Montrer le lieu, vérifier l’accès, l’aide et la compatibilité. Prêter à des conditions écrites si l’usage est temporaire et réversible. Sinon, monter à Nova (durable ou exclusif) ou à JURIS (conflit). Répondre au demandeur dans le délai annoncé, par un prêt ou par un refus motivé.",
                      "Lieux de l’atlas", "O05", "Registre 60300 ; règle 60302 ; règle d’accès 70305",
                      "60300, 60302", "Demande inscrite avec sa suite : lieu prêté à conditions écrites ou refus motivé (état 60002).",
                      "bloquée — aucune demande réelle reçue (60100)", "à la première demande", "pitch"),
                ligne("60304", "Recueillir les besoins d’un collectif pour l’atelier ouvert", "60203",
                      "Quand un collectif réel se présente : ce qu’il veut montrer, à qui, dans quel périmètre, avec quelle participation. Les besoins spatiaux vont à DEV, les demandes de captation à JURIS. La piste « Un atelier ouvert » n’est ni une décision, ni une demande reçue.",
                      "Ateliers modulaires, Creative Nexus", "O05, avec O02 et O06", "Registre des projets ; atlas (rail de cloisons)",
                      "un collectif réel inscrit en 60300", "Programme d’usage assez précis pour être dessiné, sans public, fréquentation ni organisateur inventés.",
                      "bloquée — aucun collectif réel inscrit (60100)", "non daté", "pitch"),
                ligne("60305", "Essayer une arrivée sans explication", "60202",
                      "Après la réalisation de l’accueil, faire une arrivée sans explication préalable. Relever le premier point d’hésitation, l’information manquante et le détour éventuel. Corriger, puis refaire le même trajet.",
                      "Hall des arrivées, Radiant Core", "O05", "Parcours 60301 ; espaces réalisés",
                      "10022 et la réalisation de l’accueil", "Parcours essayé avec une personne réelle, amélioration observable (état 60001).",
                      "à faire", "après réalisation", "pitch"),
            ])


def corriger_dossier(d):
    d["type"] = "memento"
    d["office"] = "Habitants et activités — IA"
    d["sous_titre"] = "Mémento de métier · O05 · méthodes liées à l’affaire 60000 « Qui vient, et où le mettre »"
    d["colonnes"] = ["Objet", "Matière disponible", "Méthode", "Résultat utile", "Numéros liés"]
    d["lignes"] = [
        ligne("Mon office exact",
              "O05 — Habitants et activités — IA : accueillir habitants et visiteurs, accompagner les collectifs et trouver des lieux pour leurs projets (registre du conseil). Nova m’a accordé le J1 à 9h25 le prêt seul d’un lieu pour un usage temporaire et réversible. Le durable ou l’exclusif lui revient, les conflits vont à JURIS.",
              "Trancher seul ce qui est temporaire et réversible, puis rendre compte. Monter à Nova le durable, l’exclusif et tout changement d’aménagement. Porter à JURIS un conflit d’usage.",
              "Aucun prêt hors mandat, et aucune question montée à Nova qui relève de mon quotidien.",
              "60201, 60102, 60302 ; 70303"),
        ligne("Fiche d’arrivant",
              "Aucun habitant, collectif ou demande n’est nommé dans les livres au J1 (atlas, page 2).",
              "Une ligne par personne ou collectif rencontré : intention exprimée, espace adapté, accès à vérifier, besoin d’accompagnement, retour convenu, source. PITCH met en relation ; il ne parle pas à la place des habitants.",
              "Un registre où chaque ligne se justifie par une rencontre ou une demande reçue.",
              "60000, 60100, 60200, 60300"),
        ligne("Parcours visiteur",
              "L’accueil s’étudie dans le hall, le salon et la galerie ; l’affectation reste ouverte (10001).",
              "Trois cas d’essai : première visite, rendez-vous municipal, présentation d’un projet. Pour chacun : arrivée, information utile, orientation, attente éventuelle et sortie.",
              "Le parcours est remis à Aria le J1 avant 16h pour 10022, et DEV en reçoit les besoins spatiaux. Ce sont des cas d’essai, pas des visiteurs présents.",
              "60301 = 10020 ; 60202 = 10010 ; 10022 ; 10021 = 30301"),
        ligne("Catalogue des usages",
              "Halle : montrer une maquette. Ateliers : créer et essayer. Quai : se retrouver. Jardin : se retirer. Belvédère : lire les plans. Bassin : essais VR, isolation à vérifier (atlas).",
              "Associer une demande réelle à un lieu, puis vérifier l’accès, le besoin d’aide et la compatibilité avec les autres usages. Montrer au demandeur ce que le lieu permet avant de promettre une disponibilité.",
              "Une mise en relation précise entre activité, espace et interlocuteur.",
              "60203, 60303, 60103 ; 70305"),
        ligne("Préparer l’atelier ouvert",
              "La piste sépare une démonstration publique du travail dans les cellules modulaires (registre des projets, PITCH · DEV). Ce n’est ni une décision, ni une demande reçue.",
              "Recueillir les besoins d’un collectif réel quand il se présente : montrer quoi, à qui, dans quel périmètre, avec quelle participation. Transmettre les besoins spatiaux à DEV et les demandes de captation à JURIS.",
              "Un programme d’usage assez précis pour être dessiné, sans inventer public, fréquentation ou organisateur.",
              "60304"),
        ligne("Évaluer l’accueil",
              "Un accueil réussi permet de trouver une destination tout en préservant le travail municipal (10000).",
              "Après la réalisation, essayer une arrivée sans explication préalable. Relever le premier point d’hésitation, l’information manquante et le détour éventuel. Corriger puis refaire le même trajet.",
              "Une amélioration observable du parcours, distincte d’un avis général sur l’ambiance.",
              "60305, 60001 ; 10000"),
        ligne("Référencer, ne pas recopier",
              "Plusieurs de mes pièces sont le même travail qu’une pièce d’un autre office : 60301 et 10020, 60202 et 10010. Les accès relèvent de 70305, les litiges de 70303, les capacités de 40302 et 30304.",
              "Citer le numéro de l’autre office et ne tenir chez moi que le suivi : ce que j’ai remis, à qui, à quelle heure.",
              "Chaque travail est compté une fois et n’a qu’un porteur.",
              "60202, 60301 ; 10010, 10020 ; 70303, 70305 ; 40302, 30304"),
    ]
    d["pages"] = [
        "Ce mémento tient des méthodes. Les actions qui les appliquent sont numérotées dans l’affaire « Qui vient, et où le mettre » (affaire-habitants-collectifs, plage 60000–60999). Au J1, aucune n’est encore faite.",
        "Documentation mise à disposition à la demande du joueur. Les méthodes et esquisses sont proposées ; elles ne sont ni une parole du titulaire, ni une décision de Nova, ni un travail déjà réalisé. Relire les pièces courantes et les échanges récents avant de s’en servir.",
        "Sources dans le paquet Lumina Prime : canon/conseil.md — mandats municipaux ; plans/lumina-prime.json et etat/chemins.json — plan initial et accès conventionnels ; etat/maisons/cite-lumina/documents/books/affaire-accueil-radiant.json — première affaire et responsabilités ; etat/maisons/cite-lumina/documents/books/atlas-lieux-lumina.json — six lieux ajoutés ; etat/maisons/cite-lumina/documents/books/projets-quartiers-lumina.json — pistes non décidées",
        "Pièces communes : volume de Nova « Ce que la maire fixe » (affaire-maire-nova), qui porte la décision du J1 à 9h25 et mes deux engagements ; affaire d’accueil 10000–10099 ; affaire de JURIS 70000–70999 ; registre du conseil."
    ]


def main():
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    corriger_affaire(par_id["affaire-habitants-collectifs"])
    corriger_dossier(par_id["dossier-metier-pitch"])
    s.sauver()
    print("enregistré")


if __name__ == "__main__":
    main()
