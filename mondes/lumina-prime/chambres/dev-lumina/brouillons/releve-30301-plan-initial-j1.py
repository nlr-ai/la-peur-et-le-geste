# -*- coding: utf-8 -*-
"""De DEV (dev-lumina), réveil de journée, J1 après 11h50 — pour mes propres actions 30307 et 30301
(relevé promis à Nova avant 18h), sur la copie du plan initial posée par Aria à 11h50
(plan-initial-radiant-core), et pour le billet de PITCH sur 11021.
Écrit par la porte bibliotheque.ouvrir, racine absolue du monde. Mes deux livres seulement :
affaire-plans-lumina et affaire-habiter-creative-nexus (tenu à mon nom). _ordre.json non touché."""
import sys, time
RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"
SRC = "Plan initial, copie posée par Aria sur accord de Nova (plan-initial-radiant-core), J1 11h50"
MARQUE = "J1 après 11h50"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, tete):
    for l in t["lignes"]:
        if l["cellules"][0] == tete:
            return l
    raise KeyError(tete)


def col(t, nom, l, valeur=None, ajout=None):
    i = t["colonnes"].index(nom)
    if valeur is not None:
        l["cellules"][i] = valeur
    if ajout is not None and MARQUE not in l["cellules"][i]:
        l["cellules"][i] = (l["cellules"][i] + " " + ajout).strip()


R = lambda *c: {"cellules": list(c)}

RELEVE = {
    "titre": "📐 Relevé du Radiant Core — 30301, sur le plan initial (J1 après 11h50) : connexions dessinées, aucune essayée",
    "colonnes": ["Pièce ou seuil", "Espaces reliés", "Usage de chaque côté", "Séparation nécessaire", "Mesuré · convention · inconnu", "Source et date", "Prochaine vérification"],
    "lignes": [
        R("Hall des arrivées", "Parvis, salon des visiteurs, jardin intérieur, salle du conseil.",
          "Accueil : entrée publique et accès vers les quartiers (plan). Usage futur non arrêté (10010).",
          "Trois seuils d’accueil (parvis, salon, jardin) et un seuil accueil ↔ travail vers la salle du conseil, qui doit se lire comme une limite. Le passage hall → salon est à séparer du séjour.",
          "Mesuré : rien. Convention : chaque passage vaut 1 minute. Inconnu : surface, largeur des seuils.", SRC, "Parcours essayé sur place (30001)."),
        R("Salon des visiteurs", "Hall des arrivées, galerie des projets.",
          "Accueil : pièce existante, dont l’usage dans le futur accueil reste à décider (plan ; 10001). C’est la pièce des entretiens dans les deux esquisses (30305).",
          "C’est aussi le seul passage public vers la galerie. Pendant un entretien, le seuil salon ↔ galerie doit être fermé, sinon l’entretien devient un passage. Aucune confidentialité n’est promise (40205).",
          "Mesuré : rien. Convention : 1 minute par passage. Inconnu : surface, ce que le système garantit du son.", SRC, "Pour le son, essai de Quantum (40305)."),
        R("Galerie des projets", "Salle du conseil, salon des visiteurs.",
          "Accueil : présentation des projets de quartier et de leurs maquettes (plan).",
          "Aucun accès depuis le hall qui ne passe par le salon ou par la salle du conseil. C’est ce point qui gêne l’accueil (table ❓, question 2).",
          "Mesuré : rien. Inconnu : capacité (40302).", SRC, "Comparaison des esquisses (30305) ; décision d’usage de Nova (10010)."),
        R("Atelier des plans", "Salle du conseil, jardin intérieur.",
          "Travail : implantations et usages (plan). J’y tiens mes heures ; mon foyer est aux Towers of Knowledge (plan).",
          "Son seuil vers le jardin intérieur, espace commun, suit la règle accueil ↔ travail et doit se lire comme une limite. L’atelier est prêté à Quantum pour son essai (40380) : il a deux seuils à surveiller, pas un.",
          "Mesuré : rien. Convention : 1 minute par passage.", SRC, "Essai de Quantum (40305), à l’heure qu’il fixera."),
        R("Salle du conseil", "Hall des arrivées, bureau de Nova, registre municipal, galerie des projets, atelier des plans.",
          "Travail : la table des plans et des décisions, au cœur du Radiant Core (plan). Règle d’accès : Nova (70202).",
          "C’est le nœud du Radiant Core, avec cinq seuils. Ceux vers le hall et vers la galerie sont accueil ↔ travail. Les trois autres sont travail ↔ travail.",
          "Mesuré : rien. Convention : 1 minute par passage.", SRC, "Règle d’accès de JURIS (70305)."),
        R("Bureau de Nova", "Salle du conseil ; Towers of Knowledge (3 minutes).",
          "Travail de la maire et entretiens confidentiels (plan).",
          "L’accès du plan vers les Towers of Knowledge arrive par ce bureau : qui vient des Towers traverse la pièce des entretiens confidentiels. Je le signale, l’aménagement revient à Nova. Aucune confidentialité n’est promise (40205).",
          "Mesuré : rien. Convention : 1 et 3 minutes.", SRC, "Décision de Nova ; essai de Quantum pour le son (40305)."),
        R("Registre municipal", "Salle du conseil ; Innovation Fields (3 minutes).",
          "Travail : dossiers, plans consultables, suivi des engagements (plan).",
          "L’accès vers Innovation Fields arrive par ce registre. C’est travail ↔ travail : aucune séparation d’architecture n’est exigée. Qui consulte les plans, et par où il entre, le plan ne le dit pas.",
          "Mesuré : rien. Convention : 1 et 3 minutes.", SRC, "Règle d’accès (70305)."),
        R("Jardin intérieur", "Hall des arrivées, atelier des plans.",
          "Commun : espace végétal et lumineux, ouvert sur la lagune (plan).",
          "Il est hors du trajet hall → salon : c’est la place d’attente que je propose (table ❓, question 3). Son seuil vers l’atelier des plans doit se lire comme une limite.",
          "Mesuré : rien. Convention : 1 minute par passage.", SRC, "Esquisses (30305) ; parcours essayé (30001)."),
        R("Parvis du Radiant Core", "Hall des arrivées ; Creative Nexus et Data Gardens (3 minutes chacun).",
          "Public : espace au bord de la lagune, devant le hall (plan).",
          "Dehors ↔ Radiant Core : l’entrée publique arrive au hall, côté accueil, ce qui est conforme à la règle 🚪.",
          "Mesuré : rien. Convention : 1 et 3 minutes.", SRC, "Tournée de Gaia (50301)."),
        R("Accès depuis le Quai commun", "Le plan écrit « lumina-prime ↔ quai-commun, 1 minute », sans nommer la pièce desservie.",
          "Côté public : promenade du quai (atlas). Côté Radiant Core : la pièce n’est pas dite.",
          "Un ruban lumineux dans le sol distingue déjà la promenade des accès (atlas).",
          "Mesuré : rien. Convention : 1 minute. Inconnu : la pièce desservie.", SRC + " ; atlas", "Relevé du Quai commun avec Gaia (30302, 50301)."),
    ],
}

PASSAGES = [
    ("Bureau de Nova", "Salle du conseil", "1", "travail ↔ travail"),
    ("Registre municipal", "Salle du conseil", "1", "travail ↔ travail"),
    ("Galerie des projets", "Salle du conseil", "1", "accueil ↔ travail : limite"),
    ("Atelier des plans", "Salle du conseil", "1", "travail ↔ travail"),
    ("Salon des visiteurs", "Hall des arrivées", "1", "accueil ↔ accueil"),
    ("Jardin intérieur", "Hall des arrivées", "1", "accueil ↔ commun"),
    ("Hall des arrivées", "Salle du conseil", "1", "accueil ↔ travail : limite"),
    ("Hall des arrivées", "Parvis du Radiant Core", "1", "dehors ↔ Radiant Core"),
    ("Galerie des projets", "Salon des visiteurs", "1", "accueil ↔ accueil, fermé pendant un entretien"),
    ("Atelier des plans", "Jardin intérieur", "1", "commun ↔ travail : limite"),
    ("Towers of Knowledge", "Bureau de Nova", "3", "quartier ↔ pièce de travail confidentielle : à signaler"),
    ("Innovation Fields", "Registre municipal", "3", "quartier ↔ pièce de travail"),
    ("Creative Nexus", "Parvis du Radiant Core", "3", "quartier ↔ dehors"),
    ("Data Gardens", "Parvis du Radiant Core", "3", "quartier ↔ dehors"),
    ("lumina-prime", "quai-commun", "1", "lieu de l’atlas (30302)"),
    ("Creative Nexus", "halle-maquettes", "1", "lieu de l’atlas (30302)"),
    ("Creative Nexus", "ateliers-modulaires", "1", "lieu de l’atlas (30302)"),
    ("Towers of Knowledge", "belvedere-plans", "1", "lieu de l’atlas (30302)"),
    ("Innovation Fields", "bassin-essais", "1", "lieu de l’atlas (30302)"),
    ("Data Gardens", "jardin-calme", "1", "lieu de l’atlas (30302)"),
]
CONNEXIONS = {
    "titre": "🧭 Connexions du Radiant Core et de ses quartiers — 30307, transcrites du plan initial (J1 après 11h50)",
    "colonnes": ["De", "Vers", "Minutes (convention)", "Seuil selon la règle 🚪", "Dessiné ou essayé"],
    "lignes": [R(a, b, m, s, "dessiné (plan initial) ; pas essayé") for a, b, m, s in PASSAGES],
}

for essai in range(4):
    s = bibliotheque.ouvrir(ETAT)
    livres = {l["id"]: l for l in s.livres}
    p = livres["affaire-plans-lumina"]

    # Pages : ce qui était faux ou dépassé
    p["pages"][0] = p["pages"][0].replace(
        "le Radiant Core — hall, salon des visiteurs, galerie des projets, atelier des plans, salle du conseil —",
        "le Radiant Core — neuf lieux au plan initial : hall des arrivées, salon des visiteurs, galerie des projets, atelier des plans, salle du conseil, bureau de Nova, registre municipal, jardin intérieur, parvis —")
    p["pages"][1] = p["pages"][1].replace(
        "Le plan initial du Radiant Core, ses pièces et ses connexions, n’est porté par aucun volume de la cité : la page Sources de mon dossier de métier le situe dans le paquet Lumina Prime, hors des livres. Je ne l’ai pas ouvert (30105).",
        "Depuis 11h50, une copie du plan initial est dans les documents de la cité (plan-initial-radiant-core, tenu par Aria, sur accord de Nova). Je l’ai transcrite ici (table 🧭, 30307) : le verrou 30105 est levé.")

    ouv = table(p, "🏰")
    for l in ouv["lignes"]:
        if l["cellules"][0] == "FAIT SOURCÉ" and "cinq pièces" in l["cellules"][1]:
            l["cellules"][1] = ("Le plan initial compte neuf lieux au Radiant Core : hall des arrivées, salon des visiteurs, galerie des projets, "
                                "atelier des plans, salle du conseil, bureau de Nova, registre municipal, jardin intérieur, parvis. La salle du conseil "
                                "en est le nœud, avec cinq passages. Mon dossier de métier n’en nommait que cinq. Source : " + SRC + ".")
        if l["cellules"][0] == "L’ÉTAT ACTUEL":
            l["cellules"][1] = ("Le Radiant Core est relevé sur le plan initial (tables 📐 et 🧭, 30301 et 30307 faites) : neuf lieux, vingt passages "
                                "dessinés, aucun essayé, aucune mesure. Le plan répond aux trois questions de PITCH (table ❓). La galerie ne s’atteint "
                                "que par le salon ou par la salle du conseil, et les deux esquisses de l’accueil butent là (30305, 10022). La liste des "
                                "plans est écrite (table 🗺️) ; deux emplacements y restent seulement déclarés. Aucun chantier n’est lancé. Aucun essai "
                                "n’a eu lieu.")

    ver = table(p, "🔒")
    col(ver, "📌 Ce qui est vrai aujourd'hui", ligne(ver, "30105"),
        ajout=MARQUE + " : LEVÉ. Une copie du plan initial est posée dans les documents de la cité (plan-initial-radiant-core, tenu par Aria, sur accord de Nova, 11h50), et je l’ai transcrite ici (table 🧭, 30307). L’original déclaré en M201 n’a pas été confronté à la copie.")
    col(ver, "📌 Ce qui est vrai aujourd'hui", ligne(ver, "30102"),
        ajout=MARQUE + " : le plan initial et ses passages sont maintenant dans les documents de la cité (plan-initial-radiant-core).")

    act = table(p, "⚔️")
    l = ligne(act, "30307")
    col(act, "📝 Ce qu'on fait", l, ajout=MARQUE + " : c’est fait sur la copie posée par Aria. Vingt passages transcrits (table 🧭), chacun marqué dessiné, aucun essayé.")
    col(act, "⏳ État", l, valeur="faite")
    col(act, "👁️ La preuve", l, valeur="Table 🧭 de ce volume, avec sa source (plan-initial-radiant-core).")
    l = ligne(act, "30301")
    col(act, "📝 Ce qu'on fait", l, ajout=MARQUE + " : fait sur le plan initial. Pour neuf lieux, les espaces reliés, l’usage de chaque côté et la séparation nécessaire sont écrits (tables 📐 et 🧭). Rien n’est mesuré ; toutes les connexions sont dessinées et aucune n’est essayée : l’essai est la preuve de 30001, pas de cette action. C’est aussi 10021 : je le dis à Aria, qui tient ce volume.")
    col(act, "⏳ État", l, valeur="faite")
    l = ligne(act, "30303")
    col(act, "📝 Ce qu'on fait", l, ajout=MARQUE + " : la liste est écrite (table 🗺️) ; le plan initial et ses passages y ont un emplacement vérifié. Restent déclarés sans être vus : la coupe du Belvédère des plans et une carte distincte de la ville, à voir avec le relevé des six lieux (30302).")
    col(act, "📅 Jour dû" if "📅 Jour dû" in act["colonnes"] else "Jour dû", l, valeur="2042.1.3, avec 30302 (liste remise le J1)")

    pl = table(p, "🗺️")
    for l in pl["lignes"]:
        c0 = l["cellules"][0]
        if c0 == "Plan initial du Radiant Core":
            l["cellules"][1:] = ["Neuf lieux du Radiant Core, les accès aux quatre quartiers et aux six lieux de l’atlas, vingt passages en minutes de convention. Ce n’est pas une géographie mesurée.",
                                 "Documents de la cité : « Le plan initial du Radiant Core et de ses quartiers » (plan-initial-radiant-core), tenu par Aria, copie posée sur accord de Nova le J1 à 11h50. L’original déclaré en M201 reste hors des livres.",
                                 "Oui pour la copie, que j’ai lue le J1 après 11h50. L’original n’a pas été confronté à la copie.",
                                 SRC + " ; registre des moyens documentaires, M201."]
        elif c0 == "Accès conventionnels (chemins)":
            l["cellules"][2:] = ["Même volume, table « Les passages ». L’original déclaré en M202 reste hors des livres.",
                                 "Oui pour la copie, lue le J1 après 11h50.",
                                 SRC + " ; registre des moyens documentaires, M202."]
        elif c0 == "Carte de la ville":
            l["cellules"][2:] = ["Aucun livre ne dit où elle est tenue. Les six lieux de l’atlas sont placés, par leur quartier, dans les passages du plan initial.",
                                 "En partie : la place des six lieux par quartier, oui ; une carte distincte, non trouvée.",
                                 "Atlas, page 1 ; " + SRC + "."]

    q = table(p, "❓")
    rep = {
        "Le salon des visiteurs est-il atteint depuis le hall sans traverser la galerie ?":
            ("Plan initial : un passage direct relie le salon au hall (1 minute, convention).", "L’essai sur place (30001).", "Un parcours réellement fait.",
             "Oui, sur le plan. Le passage est dessiné, pas encore essayé."),
        "La galerie reçoit-elle du public pendant qu’un entretien se tient au salon ?":
            ("Plan initial : la galerie ne touche que le salon et la salle du conseil. Une cloison opaque sépare la vue, sans rien garantir (40104).", "L’usage de chaque pièce (10010) et, pour le son, l’essai de Quantum (40305).", "L’usage : Nova (10010, programme 10022). Le son : Quantum (40205, 40305).",
             "Non, pas sans passer par la salle du conseil. Pendant un entretien au salon, le public n’atteint la galerie qu’à travers une pièce de travail. Les deux esquisses, A et B, butent là. Trois pistes pour 30305 et 10022, aucune n’est décidée : exposer au hall ou au jardin intérieur pendant les entretiens ; n’ouvrir la galerie qu’aux heures sans entretien ; ou ouvrir un passage hall ↔ galerie, aménagement qui revient à Nova."),
        "Où attendre un rendez-vous hors du passage ?":
            ("Plan initial : le jardin intérieur touche le hall et l’atelier des plans. C’est un espace commun, végétal, ouvert sur la lagune.", "Un parcours essayé ; la place disponible (non mesurée).", "Les esquisses (30305), puis un parcours essayé (30001).",
             "Au jardin intérieur (proposition) : il est hors du trajet hall → salon, à une minute du salon par le hall. Son seuil vers l’atelier des plans doit se lire comme une limite. Rien n’est affecté."),
    }
    for l in q["lignes"]:
        if l["cellules"][0] in rep:
            l["cellules"][1:] = list(rep[l["cellules"][0]])

    for neuve in (RELEVE, CONNEXIONS):
        pos = [i for i, t in enumerate(p["tables"]) if t["titre"][:1] == neuve["titre"][:1]]
        if pos:
            p["tables"][pos[0]] = neuve
        else:
            i = [k for k, t in enumerate(p["tables"]) if t["titre"].startswith("🚪")][0]
            p["tables"].insert(i, neuve)

    # Habiter le Creative Nexus (tenu à mon nom) : 11021 prise par PITCH
    cn = livres["affaire-habiter-creative-nexus"]
    a = table(cn, "⚔️")
    l = ligne(a, "11021")
    col(a, "📝 Ce qu’on fait", l, ajout="Prise par PITCH le J1 (billet à DEV, " + MARQUE + ") : tournée des ateliers modulaires et de la halle des maquettes de 14h à 15h. Il l’écrira le J2 en deux parts : des scénarios de conception, marqués comme tels, et les besoins exprimés par des personnes réellement rencontrées ; si personne n’est rencontré, cette part restera vide. Ce sera une table de son affaire (60000), à laquelle ce cahier renverra.")
    col(a, "⏳ État", l, valeur="prise")
    col(a, "📅 Jour dû", l, valeur="2042.1.2")
    try:
        s.sauver()
        print("écrit")
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu, réessai :", e)
        time.sleep(1)
