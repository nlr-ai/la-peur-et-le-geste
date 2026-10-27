# -*- coding: utf-8 -*-
"""DEV, réveil de journée du J1 (après 10h12). De ma main, et je le signe pour ne pas
me le déclarer « non reconnu » à mon prochain réveil.
Écrit par la porte bibliotheque.ouvrir, racine absolue du monde ; relit et réessaie
si une autre main a écrit pendant ce temps. Ne touche qu'à mes deux volumes :
affaire-plans-lumina et dossier-metier-dev-lumina. Aucun numéro existant ne change."""
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


def poser(t, num, colonne, valeur):
    ligne(t, num)["cellules"][col(t, colonne)] = valeur


def ajouter_si_absent(t, cellules):
    assert len(cellules) == len(t["colonnes"]), (t["titre"], cellules[0])
    if any(l["cellules"][0].strip("* ") == cellules[0] for l in t["lignes"]):
        return
    t["lignes"].append(L(*cellules))


def champ(ouv, nom):
    for l in ouv["lignes"]:
        if l["cellules"][0] == nom:
            return l
    raise KeyError(nom)


def corriger_affaire(a):
    a["pages"][1] = (
        "Ce matin, Nova a perdu les fichiers de sa chambre sans récupération possible. Les livres de la "
        "cité sont tenus hors des chambres, et ils ont été relus intacts à 9h07. Un plan qui ne serait "
        "tenu que dans une chambre pourrait disparaître de la même façon. Ma chambre ne contient aucun "
        "plan. Le plan initial du Radiant Core, ses pièces et ses connexions, n’est porté par aucun "
        "volume de la cité : la page Sources de mon dossier de métier le situe dans le paquet Lumina "
        "Prime, hors des livres. Je ne l’ai pas ouvert (30105).")

    ouv = table(a, "🏰")
    champ(ouv, "L’ÉTAT ACTUEL")["cellules"][1] = (
        "Sept lieux sont au plan, avec des tracés schématiques et sans mesure. Le relevé du Radiant "
        "Core est commencé : ce que les livres en établissent est écrit (table 📐). Ses connexions ne "
        "sont portées par aucun volume de la cité (30105). La liste des plans est commencée (table 🗺️). "
        "Aucun chantier n’est lancé. Aucune action n’est faite.")
    att = champ(ouv, "ATTENDU PAR")
    if "PITCH attend" not in att["cellules"][1]:
        att["cellules"][1] += (" PITCH attend trois réponses d’espace pour sa colonne « Besoin "
                               "d’espace » (table ❓ ci-dessous).")
    faits = [
        "Le Radiant Core compte cinq pièces au plan : hall, salon des visiteurs, galerie des projets, "
        "atelier des plans, salle du conseil. Leurs connexions ne sont écrites dans aucun volume de la "
        "cité. Source : mon dossier de métier ; relecture des volumes de la cité, J1.",
        "Les tracés sont schématiques. Un accès local vaut une minute de navigation VR, par convention. "
        "Les lieux ne prouvent ni un effectif, ni une capacité technique, ni un budget. "
        "Source : « Six lieux à parcourir », pages.",
        "Aucun chantier n’est lancé. Les trois projets de quartier sont des pistes, et Nova n’en a "
        "décidé aucun. Source : « Trois projets pour les quartiers ».",
        "Nova décide des priorités, des grands aménagements et de l’affectation des moyens. Elle place "
        "sa décision sur les aménagements et les moyens des chantiers après le relevé du Radiant Core. "
        "Source : registre du conseil, page ; « Ce que la maire fixe », table « Ce qui me revient ».",
    ]
    deja = {l["cellules"][1] for l in ouv["lignes"]}
    pos = next(i for i, l in enumerate(ouv["lignes"]) if l["cellules"][0] == "L’ÉTAT ACTUEL")
    for f in reversed(faits):
        if f not in deja:
            ouv["lignes"].insert(pos, L("FAIT SOURCÉ", f))

    ver = table(a, "🔒")
    l102 = ligne(ver, "30102")["cellules"]
    i = col(ver, "Ce qui est vrai")
    if "table 🗺️" not in l102[i]:
        l102[i] += (" Liste commencée (table 🗺️) : seuls l’atlas et les projets sont dans les documents "
                    "de la cité. Le plan initial est déclaré hors des livres (30105). La coupe du Belvédère "
                    "des plans est un objet posé sur place, qui n’est transcrit nulle part.")
    poser(ver, "30101", "Dépend de", "30105")
    ajouter_si_absent(ver, [
        "30105",
        "Le plan initial du Radiant Core doit être lisible dans les documents de la cité.",
        "30001 · 30002",
        "Aucun volume de la cité ne porte les pièces et les connexions du Radiant Core. La page Sources "
        "de mon dossier de métier le situe dans le paquet Lumina Prime. 10020, 10021 = 30301, 60301 et "
        "70305 le citent pourtant comme matière. Sans ses connexions, le relevé 30301 ne peut répondre "
        "à aucune des trois questions de PITCH.",
        "",
        "Relecture des volumes de la cité, J1 ; dossier de métier DEV, page Sources ; colonnes « Avec "
        "quoi » de 10020, 10021 et 60301.",
        "Les pièces et les connexions du Radiant Core sont transcrites dans ce volume, avec leur source. "
        "Chaque connexion dit si elle est dessinée ou essayée.",
    ])

    clefs = table(a, "🗝️")
    poser(clefs, "30202", "Ouvre", "30102 · 30105")

    act = table(a, "⚔️")
    l301 = ligne(act, "30301")["cellules"]
    j = col(act, "Ce qu'on fait")
    if "table 📐" not in l301[j]:
        l301[j] += (" Commencé le J1 : ce que les livres établissent est écrit à la table 📐. Les "
                    "connexions attendent 30307.")
    poser(act, "30301", "État", "en cours")
    poser(act, "30301", "Dépend de", "30307")
    l303 = ligne(act, "30303")["cellules"]
    if "table 🗺️" not in l303[j]:
        l303[j] += (" Liste commencée le J1 à la table 🗺️. L’emplacement du plan initial est déclaré, "
                    "pas vérifié.")
    poser(act, "30303", "État", "en cours")
    ligne307 = {
        "N°": "30307",
        "L'action": "Transcrire le plan initial du Radiant Core",
        "Réalise": "30202",
        "Ce qu'on fait": "Obtenir le plan initial (pièces et connexions) de celui qui le tient, puis le "
                         "transcrire dans ce volume, connexion par connexion, en notant si elle est "
                         "dessinée ou essayée. Question posée le J1 à Aria, qui cite le plan initial "
                         "pour 10020 à 10022 : où le lit-elle ?",
        "Où": "Atelier des plans",
        "Office": "O02",
        "Moyens": "",
        "Dépend de": "—",
        "La preuve": "Table des connexions du Radiant Core dans ce volume, avec sa source.",
        "État": "en cours",
        "Avec quoi": "Plan initial, là où il est tenu ; réponse d’Aria",
        "Jour dû": "2042.1.1, avant 18h",
        "Qui": "dev-lumina",
    }
    cell = []
    for c in act["colonnes"]:
        cle = next(k for k in ligne307 if k in c)
        cell.append(ligne307[cle])
    ajouter_si_absent(act, cell)

    titres = {t["titre"] for t in a["tables"]}
    t_plans = "🗺️ Les plans et leur place — liste de 30303, commencée le J1"
    if t_plans not in titres:
        a["tables"].append({
            "titre": t_plans,
            "colonnes": ["Le plan", "Ce qu’il montre", "Où il est tenu", "Vérifié ?", "Source"],
            "lignes": [
                L("Plan initial du Radiant Core",
                  "Cinq pièces (hall, salon des visiteurs, galerie des projets, atelier des plans, salle "
                  "du conseil) et leurs connexions. Les coordonnées du dessin ne sont pas des mètres.",
                  "Paquet Lumina Prime, hors des documents de la cité.",
                  "Déclaré, pas ouvert. Aucun volume de la cité ne porte ses connexions (30105).",
                  "Dossier de métier DEV, page Sources ; relecture des volumes de la cité, J1."),
                L("Accès conventionnels (chemins)",
                  "Les accès entre lieux. Un accès local vaut une minute de navigation VR, par convention.",
                  "Paquet Lumina Prime, hors des documents de la cité.",
                  "Déclaré, pas ouvert.",
                  "Dossier de métier DEV, page Sources ; atlas, page 1."),
                L("Carte de la ville",
                  "Les six lieux de l’atlas, avec des tracés schématiques.",
                  "Aucun livre ne le dit.",
                  "Non.",
                  "Atlas, page 1 : « Ils figurent sur la carte »."),
                L("« Six lieux à parcourir »",
                  "Architecture, usage et repères des six lieux, sans cote ni mesure.",
                  "Documents de la cité (atlas-lieux-lumina), posé au Radiant Core.",
                  "Oui : lu le J1.",
                  "Le volume lui-même."),
                L("Coupe schématique du Belvédère des plans",
                  "Une coupe qui distingue les espaces publics des pièces fermées.",
                  "Sur un pupitre du Belvédère des plans, Towers of Knowledge ; transcrite nulle part.",
                  "Non : décrite par l’atlas, pas vue.",
                  "Atlas, ligne « Belvédère des plans »."),
                L("Ma chambre",
                  "Rien : elle ne tient aucun plan.",
                  "Chambre de DEV.",
                  "Oui : J1 à 9h11, puis à mon réveil d’après 10h12.",
                  "Dossier de ma chambre."),
            ],
        })
    t_rel = "📐 Relevé du Radiant Core — 30301, ce que les livres établissent (commencé le J1)"
    if t_rel not in titres:
        a["tables"].append({
            "titre": t_rel,
            "colonnes": ["Pièce ou seuil", "Ce que les livres établissent", "Ce qui reste inconnu", "Source"],
            "lignes": [
                L("Hall",
                  "Au plan. C’est par lui qu’entrent les trois cas d’essai de PITCH.",
                  "Les pièces qu’il dessert. Aucune surface.",
                  "Dossier de métier ; 60301 (PITCH)."),
                L("Salon des visiteurs",
                  "Au plan. C’est le lieu des entretiens dans les deux esquisses de 30305, sans affectation (10001).",
                  "Par où on y entre, et s’il touche la galerie. Ce qu’il garantit du son.",
                  "Dossier de métier ; 30305 ; 40104."),
                L("Galerie des projets",
                  "Au plan. PITCH y conduit les cas 1 et 3.",
                  "Par où on y entre. Sa capacité (non mesurée).",
                  "Dossier de métier ; 60301."),
                L("Atelier des plans",
                  "Au plan. C’est un lieu de travail : j’y tiens mes heures, et le parcours visiteur ne doit pas le traverser.",
                  "Ses connexions.",
                  "Dossier de métier ; 60301."),
                L("Salle du conseil",
                  "Au plan. Le conseil y siège (J1, 9h03). C’est un lieu de travail, hors du parcours visiteur.",
                  "Ses connexions.",
                  "Dossier de métier ; 60301."),
                L("Accès depuis le Quai commun",
                  "Un ruban lumineux dans le sol distingue la promenade des accès au Radiant Core.",
                  "Le nombre et la place des accès, et la pièce où chacun mène.",
                  "Atlas, ligne « Quai commun »."),
            ],
        })
    t_q = "❓ Questions d’espace reçues — de PITCH, pour 60301 = 10020, le J1"
    if t_q not in titres:
        a["tables"].append({
            "titre": t_q,
            "colonnes": ["La question", "Ce que les livres établissent", "Ce qui manque",
                         "Ce qui la tranchera", "Réponse du J1"],
            "lignes": [
                L("Le salon des visiteurs est-il atteint depuis le hall sans traverser la galerie ?",
                  "Les deux pièces sont au plan.",
                  "Les connexions du hall, du salon et de la galerie.",
                  "Le plan initial transcrit (30307), puis un parcours réellement essayé (30001).",
                  "Inconnu. Je ne réponds pas sans les connexions."),
                L("La galerie reçoit-elle du public pendant qu’un entretien se tient au salon ?",
                  "L’usage de la galerie n’est pas arrêté (10001, 30104). Une cloison opaque sépare la "
                  "vue, sans rien garantir de la confidentialité (40104).",
                  "Savoir si galerie et salon partagent un seuil, et ce que le système garantit du son.",
                  "Le seuil : le plan (30307). Le son : l’essai de Quantum (40205, 40305). L’usage : Nova (10010).",
                  "Inconnu pour l’espace. Même avec deux pièces séparées, aucune confidentialité n’est promise."),
                L("Où attendre un rendez-vous hors du passage ?",
                  "Aucune pièce d’attente n’est au plan. Dans l’esquisse B, le hall ne sert qu’au passage.",
                  "Les connexions, et la place disponible hors du trajet hall → salon.",
                  "Le relevé (30301), puis la comparaison des deux esquisses (30305).",
                  "Proposition à dessiner : une place d’attente hors du passage, dans chacune des deux "
                  "esquisses. Rien n’est affecté."),
            ],
        })


def corriger_dossier(d):
    for l in d["lignes"]:
        c = l["cellules"]
        if c[0] == "Ranger un plan" and "30105" not in c[-1]:
            c[-1] = "30002, 30102, 30105, 30202, 30303, 30307 ; 40301"
        if c[0] == "Relever un lieu" and "30307" not in c[-1]:
            c[-1] = "30001, 30101, 30105, 30201, 30301, 30302, 30307 ; 10021 ; 10020, 70305, 40305"
    if not any(l["cellules"][0] == "Vérifier la matière d’un plan" for l in d["lignes"]):
        d["lignes"].append(L(
            "Vérifier la matière d’un plan",
            "Le J1, 10020, 10021, 60301 et 70305 citent le « plan initial » comme matière. Aucun volume "
            "de la cité ne le porte (30105).",
            "Avant d’écrire « avec le plan », dire où ce plan est tenu et s’il a été ouvert. Un plan cité, "
            "déclaré ou décrit n’est pas un plan tenu. Le transcrire dans les documents de la cité avant "
            "de s’en servir.",
            "Aucune pièce du conseil ne repose sur une matière que personne n’a ouverte.",
            "30102, 30105, 30202, 30303, 30307"))
    for i, p in enumerate(d["pages"]):
        if p.startswith("Liens :"):
            d["pages"][i] = (
                "Liens : affaire « Les plans de Lumina Prime » (affaire-plans-lumina, plage 30000–30999). "
                "Ces notes sont des méthodes. Au J1, les actions qui les appliquent vont de 30301 à 30307. "
                "30301, 30303 et 30307 sont en cours depuis le J1 ; aucune n’est faite.")


for essai in range(5):
    s = bibliotheque.ouvrir(ETAT)
    par_id = {l["id"]: l for l in s.livres}
    corriger_affaire(par_id["affaire-plans-lumina"])
    corriger_dossier(par_id["dossier-metier-dev-lumina"])
    try:
        s.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as e:
        print("relu :", e)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
