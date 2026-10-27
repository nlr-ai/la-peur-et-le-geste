# -*- coding: utf-8 -*-
"""DEV, J1 après 11h50. De ma main, pour 30307 et 30301.

Nova a fait poser le plan initial dans les documents de la cité. Je transcris
les passages dessinés, mets à jour le relevé et la liste des plans. Je ne
touche qu'à mon affaire ; je ne ferme pas 30303 car la carte de la ville et la
coupe du Belvédère ne sont pas encore toutes deux rangées et vérifiées.
"""
import sys
import time

RACINE = "C:/Users/reyno/le-conseil2"
sys.path[:0] = [RACINE + "/scripts", RACINE + "/scripts/noyau"]
import bibliotheque

ETAT = RACINE + "/mondes/lumina-prime/etat"


def table(livre, prefixe):
    for t in livre["tables"]:
        if t["titre"].startswith(prefixe):
            return t
    raise KeyError(prefixe)


def ligne(t, numero):
    for l in t["lignes"]:
        if l["cellules"][0].strip("* ") == numero:
            return l
    raise KeyError(numero)


def col(t, fragment):
    for i, nom in enumerate(t["colonnes"]):
        if fragment in nom:
            return i
    raise KeyError(fragment)


def poser(t, numero, colonne, valeur):
    ligne(t, numero)["cellules"][col(t, colonne)] = valeur


def corriger(a):
    ouverture = table(a, "🏰")
    poser(
        ouverture,
        "L’ÉTAT ACTUEL",
        "Ce qui est établi",
        "Le plan initial a été posé dans les documents de la cité sur accord de Nova à 11h50, puis transcrit dans ce volume (table 🧭). Le relevé du Radiant Core est achevé pour les accès dessinés (30301, table 📐) : aucune cote n'est mesurée et aucun parcours n'est encore essayé. La liste des plans est mise à jour (table 🗺️), mais reste en cours : la carte de la ville n'est pas localisée et la coupe du Belvédère n'est pas transcrite. Aucun chantier n'est lancé. La fiche d'essai réversible est écrite (30308) ; aucun essai n'a eu lieu.",
    )

    verrous = table(a, "🔒")
    poser(
        verrous,
        "30105",
        "Ce qui est vrai",
        "Le verrou est levé depuis 11h50 : le volume « Le plan initial du Radiant Core et de ses quartiers » est lisible dans les documents de la cité, tenu par Aria sur accord de Nova. Il distingue les salles et vingt passages conventionnels. Chaque passage transcrit ci-dessous est dessiné, pas essayé.",
    )
    poser(
        verrous,
        "30105",
        "La preuve",
        "Volume plan-initial-radiant-core, copie posée J1 à 11h50 ; table 🧭 de ce volume, transcription de DEV.",
    )
    poser(
        verrous,
        "30105",
        "Levé quand",
        "Levé le J1 à 11h50 : pièces et passages transcrits avec leur source et leur statut « dessiné, non essayé » (30307).",
    )

    actions = table(a, "⚔️")
    poser(
        actions,
        "30307",
        "Ce qu'on fait",
        "Fait le J1 après 11h50. Le plan initial posé dans les documents de la cité sur accord de Nova a été lu puis transcrit dans la table 🧭, passage par passage. Chaque liaison est une convention dessinée ; aucune n'est notée comme essayée.",
    )
    poser(actions, "30307", "La preuve", "Table 🧭 de ce volume ; volume plan-initial-radiant-core, J1 11h50.")
    poser(actions, "30307", "État", "faite")
    poser(actions, "30307", "Avec quoi", "Volume plan-initial-radiant-core, tenu par Aria sur accord de Nova.")

    poser(
        actions,
        "30301",
        "Ce qu'on fait",
        "Fait le J1 après 11h50. Les seuils du hall, du salon, de la galerie, de l'atelier et de la salle du conseil sont relevés dans la table 📐. Mesuré : rien. Convention : pièces, passages et minutes du plan. Inconnus maintenus : surfaces, capacité, son et parcours réellement praticable. Les réponses aux trois questions de PITCH sont écrites dans la table ❓.",
    )
    poser(actions, "30301", "Dépend de", "30307, faite")
    poser(actions, "30301", "La preuve", "Tables 📐, 🧭, 🚪 et ❓ de ce volume ; chaque accès est marqué dessiné, non essayé.")
    poser(actions, "30301", "État", "faite")
    poser(actions, "30301", "Avec quoi", "Plan initial lisible ; mémento M212 ; parcours 60301.")

    poser(
        actions,
        "30303",
        "Ce qu'on fait",
        "Liste mise à jour le J1 après 11h50. Le plan initial est désormais vérifié dans les documents de la cité. Restent à localiser la carte de la ville et à transcrire la coupe schématique du Belvédère ; la liste demeure en cours.",
    )

    plans = table(a, "🗺️")
    for l in plans["lignes"]:
        c = l["cellules"]
        if c[0] == "Plan initial du Radiant Core":
            c[1] = "Salles du Radiant Core, usages initiaux et passages conventionnels vers les quartiers ; aucune cote mesurée."
            c[2] = "Documents de la cité : volume plan-initial-radiant-core, tenu par Aria sur accord de Nova."
            c[3] = "Oui : ouvert et transcrit par DEV le J1 après 11h50 (30307)."
            c[4] = "Le volume lui-même, sous-titre et tables « Les salles et les lieux » et « Les passages »."
        elif c[0] == "Accès conventionnels (chemins)":
            c[1] = "Les vingt passages du plan initial ; 1 ou 3 minutes de navigation par convention."
            c[2] = "Documents de la cité : même volume plan-initial-radiant-core."
            c[3] = "Oui : ouverts et transcrits par DEV le J1 après 11h50 (30307)."
            c[4] = "Table « Les passages » du plan initial."

    releve = table(a, "📐")
    donnees = {
        "Hall": (
            "Salon des visiteurs · Jardin intérieur · Salle du conseil · Parvis du Radiant Core.",
            "Mesuré : rien. Convention : quatre passages dessinés, chacun à 1 minute. Inconnu : surfaces et praticabilité réelle.",
            "Plan initial, tables des salles et des passages, J1 11h50 ; transcrit par DEV.",
            "Essayer les parcours ; usage de l'accueil à décider par Nova (10010).",
        ),
        "Salon des visiteurs": (
            "Hall des arrivées · Galerie des projets.",
            "Mesuré : rien. Convention : deux passages dessinés, chacun à 1 minute. Inconnu : surface, son et praticabilité réelle.",
            "Plan initial, J1 11h50 ; transcrit par DEV.",
            "Essai de parcours ; essai de Quantum pour le son (40305).",
        ),
        "Galerie des projets": (
            "Salle du conseil · Salon des visiteurs.",
            "Mesuré : rien. Convention : deux passages dessinés, chacun à 1 minute. Inconnu : capacité et praticabilité réelle.",
            "Plan initial, J1 11h50 ; transcrit par DEV.",
            "Essayer le parcours public ; mesurer la capacité (40302).",
        ),
        "Atelier des plans": (
            "Salle du conseil · Jardin intérieur.",
            "Mesuré : rien. Convention : deux passages dessinés, chacun à 1 minute. Inconnu : praticabilité réelle.",
            "Plan initial, J1 11h50 ; transcrit par DEV.",
            "Premier essai d'accès et de captation avec Quantum (40305).",
        ),
        "Salle du conseil": (
            "Bureau de Nova · Registre municipal · Galerie des projets · Atelier des plans · Hall des arrivées.",
            "Mesuré : rien. Convention : cinq passages dessinés, chacun à 1 minute. Inconnu : praticabilité réelle et droits d'accès.",
            "Plan initial, J1 11h50 ; transcrit par DEV.",
            "Règles d'accès par JURIS (70202, 70305) ; parcours essayé.",
        ),
        "Accès depuis le Quai commun": (
            "Le plan porte Quai commun ↔ Lumina Prime (1 minute), et Parvis ↔ Hall (1 minute), mais ne dessine pas le raccord précis entre le quai et le parvis.",
            "Mesuré : rien. Convention : deux passages cités séparément. Inconnu : leur raccord exact et la praticabilité réelle.",
            "Plan initial, table des passages, J1 11h50 ; atlas, ligne Quai commun.",
            "Relevé du Quai commun avec Gaia (30302, 50301).",
        ),
    }
    for nom, (espaces, statut, source, prochaine) in donnees.items():
        l = ligne(releve, nom)["cellules"]
        l[col(releve, "Espaces reliés")] = espaces
        l[col(releve, "Mesuré")] = statut
        l[col(releve, "Source et date")] = source
        l[col(releve, "Prochaine vérification")] = prochaine
    releve["titre"] = "📐 Relevé du Radiant Core — 30301, fait le J1 après 11h50 (accès dessinés, non essayés)"

    questions = table(a, "❓")
    q = questions["lignes"]
    q[0]["cellules"][2] = "Oui, au plan : Hall ↔ Salon est un passage direct d'une minute, sans traverser la galerie. Dessiné, non essayé."
    q[0]["cellules"][3] = "Faire l'essai réel du parcours ; le dessin ne prouve pas la praticabilité."
    q[1]["cellules"][2] = "Pas par un parcours public séparé dans le plan actuel : depuis le hall, la galerie ne s'atteint que par le salon ou par la salle du conseil. La vue et le son restent à vérifier."
    q[1]["cellules"][3] = "Nova tranche l'usage (10010) ; comparer les esquisses (30305) et essayer le son (40305)."
    q[2]["cellules"][2] = "Aucun lieu d'attente hors passage n'est établi. Le jardin touche le hall, mais le plan le nomme espace commun, pas salle d'attente ; son usage n'est pas décidé."
    q[2]["cellules"][3] = "Soumettre les deux esquisses et l'usage du jardin à Nova ; essayer le parcours."

    if not any(t["titre"].startswith("🧭") for t in a["tables"]):
        a["tables"].append({
            "titre": "🧭 Connexions transcrites du plan initial — 30307, J1 après 11h50",
            "colonnes": ["De", "Vers", "Minutes", "Statut", "Source"],
            "lignes": [
                {"cellules": [x, y, m, "Dessiné, non essayé", "plan-initial-radiant-core, table « Les passages », J1 11h50"]}
                for x, y, m in [
                    ("Bureau de Nova", "Salle du conseil", "1"),
                    ("Registre municipal", "Salle du conseil", "1"),
                    ("Galerie des projets", "Salle du conseil", "1"),
                    ("Atelier des plans", "Salle du conseil", "1"),
                    ("Salon des visiteurs", "Hall des arrivées", "1"),
                    ("Jardin intérieur", "Hall des arrivées", "1"),
                    ("Hall des arrivées", "Salle du conseil", "1"),
                    ("Hall des arrivées", "Parvis du Radiant Core", "1"),
                    ("Galerie des projets", "Salon des visiteurs", "1"),
                    ("Atelier des plans", "Jardin intérieur", "1"),
                    ("Towers of Knowledge", "Bureau de Nova", "3"),
                    ("Innovation Fields", "Registre municipal", "3"),
                    ("Creative Nexus", "Parvis du Radiant Core", "3"),
                    ("Data Gardens", "Parvis du Radiant Core", "3"),
                    ("Lumina Prime", "Quai commun", "1"),
                    ("Creative Nexus", "Halle des maquettes", "1"),
                    ("Creative Nexus", "Ateliers modulaires", "1"),
                    ("Towers of Knowledge", "Belvédère des plans", "1"),
                    ("Innovation Fields", "Bassin d'essais", "1"),
                    ("Data Gardens", "Jardin calme", "1"),
                ]
            ],
        })


for essai in range(5):
    session = bibliotheque.ouvrir(ETAT)
    livres = {livre["id"]: livre for livre in session.livres}
    corriger(livres["affaire-plans-lumina"])
    try:
        session.sauver()
        print("écrit, essai", essai + 1)
        break
    except bibliotheque.BibliothequeModifiee as exc:
        print("relu :", exc)
        time.sleep(2)
else:
    raise SystemExit("rien écrit après cinq essais")
