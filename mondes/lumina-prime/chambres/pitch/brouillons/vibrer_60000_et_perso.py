raise SystemExit("PÉRIMÉ (J1) : script déjà servi ; il réécrirait des cellules depuis une lecture ancienne. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""J1, après 10h02 — message de Nova : « vibrer », et une affaire personnelle.
1) Affaire 60000 : sommets de Nova (90200, 90300) ; un état neuf 60003 « ce qui se crée se montre » ;
   les trois précisions de JURIS (avis ⚖️, 70307) reprises dans la règle 📜 ; deux pages remises au vrai.
2) Affaire personnelle affaire-perso-pitch : vision, objectifs, envies (60600–60699)."""
import json
import os

B = r"C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books"
F = os.path.join(B, "affaire-habitants-collectifs.json")
P = os.path.join(B, "affaire-perso-pitch.json")


def L(*c):
    return {"cellules": list(c)}


def table(a, debut):
    return next(t for t in a["tables"] if t["titre"].startswith(debut))


def ligne(t, num):
    return next(l["cellules"] for l in t["lignes"] if l["cellules"][0].strip("* ") == num)


a = json.load(open(F, encoding="utf-8"))

# --- pages remises au vrai
a["pages"][3] = ("Ce qui reste inconnu et que je n’invente pas : le nombre d’habitants et de visiteurs, la fréquentation, la capacité des lieux, "
                 "le coût en calcul d’une ouverture et les moyens de mon office. Les pistes du registre des projets, dont « Un atelier ouvert » (PITCH · DEV), "
                 "ne sont pas des demandes reçues. Les capacités, budgets et effectifs se trouvent en 40302, 30304 et 50105. "
                 "Les moyens cités (🧰) sont des documents de la cité, au registre des moyens documentaires (M201 à M205, M215) ; "
                 "aucun moyen propre de mon office, effectif ou capacité, n’a encore d’adresse.")
a["pages"][5] = ("Format : le standard des champs posé par Nova au conseil le J1 à 9h42 (« Le standard des champs d’une affaire »). "
                 "Les numéros, preuves, décisions et états existants sont conservés.")
a["pages"].append("**J1, après 10h02 — la question de Nova : « est-ce que vos affaires disent qu’il faut vibrer ? »** Non, celle-ci ne le disait pas : "
                  "elle compte, reçoit et prête. Ce qui peut surprendre ou toucher dans mon domaine, ce sont les projets des collectifs, vus en train de se faire. "
                  "L’état 60003 l’écrit, sans rien promettre de ce qu’aucun collectif n’a encore demandé. Ma vision et mes envies sont dans mon affaire personnelle (60600).")

# --- ouverture
ouv = table(a, "🏰")
for c in (l["cellules"] for l in ouv["lignes"]):
    if "LE PÉRIMÈTRE — DANS" in c[0] and "60306" not in c[1]:
        c[1] += " La présentation d’un travail en cours par un collectif, dans un lieu prêté (60003, 60306)."
    if "L’ÉTAT ACTUEL" in c[0]:
        c[1] = ("Au J1 : le registre des arrivants est ouvert et vide (60300, faite). Le parcours visiteur est écrit et remis à Aria (60301, faite). "
                "La règle de prêt accordée par Nova à 9h25 est écrite (60302, faite), avec les trois précisions de JURIS (avis ⚖️, 70307) . "
                "La décision est tenue au volume de Nova « Ce que la maire fixe », table ⚖️, qui sert de registre des décisions (Aria a écarté 20303 et y renvoie). Aucun habitant, visiteur, collectif ou demande n’est encore inscrit.")
    if "LA PLAGE" in c[0]:
        c[1] = ("**60000 à 60999**, réservée à mon office dans Lumina Prime. Ici : 60000–60003 (états), 60100–60104 (verrous), "
                "60200–60204 (clefs), 60300–60306 (actions). Mon affaire personnelle : 60600–60699.")

# --- affaires liées
lie = table(a, "🔗")
for c in (l["cellules"] for l in lie["lignes"]):
    if c[2] == "60103" and c[3] == "70305":
        c[0], c[2] = "nourrit", "60303"
        c[4] = "Chaque fiche de prêt où l’accès est marqué inconnu va à JURIS, qui bâtit la règle d’accès à partir d’elles (avis ⚖️ de JURIS)."
nouveaux_liens = [
    L("retient", "Des droits lisibles pour les habitants", "60302", "70307",
      "Les trois précisions de JURIS sur la règle de prêt, reprises de ma main dans la table 📜."),
    L("sert", "Ce que la maire fixe", "60000", "90200",
      "Les gens rencontrés, inscrits : la part « ses gens » du sommet de Nova."),
    L("sert", "Ce que la maire fixe", "60002", "90300",
      "Un collectif obtient un lieu : c’est ce que le sommet de Nova nomme."),
    L("sert", "Ce que la maire fixe", "60003", "90300",
      "Une cité habitée et visitée : ce qui s’y crée se voit."),
    L("partage", "Mon affaire personnelle", "60003", "60600",
      "Ma vision dit la même chose en mon nom : qui arrive avec une idée la montre le jour même."),
]
deja = {(c[2], c[3]) for c in (l["cellules"] for l in lie["lignes"])}
lie["lignes"] += [l for l in nouveaux_liens if (l["cellules"][2], l["cellules"][3]) not in deja]

# --- états cibles : sommets et état neuf
et = table(a, "🎯")
ligne(et, "60000")[6] = "60002 · 90200"
ligne(et, "60002")[6] = "90300"
if not any(l["cellules"][0].strip("* ") == "60003" for l in et["lignes"]):
    et["lignes"].append(L(
        "**60003**", "**Ce qui se crée ici se montre.**",
        "Un collectif qui travaille à Lumina Prime peut montrer son travail en cours à des visiteurs, dans un lieu prêté, sans que la présentation vaille approbation ni que le public traverse le travail.",
        "C’est là que la ville surprend et touche : on y voit des projets vivants, pas seulement des espaces administrés. Sans lui, les socles de la Halle restent vides et les ateliers fermés au regard.",
        "Halle des maquettes, ateliers modulaires (Creative Nexus), galerie des projets",
        "Une première présentation réelle, tenue dans un lieu prêté à des conditions écrites, avec au moins un visiteur qui n’était pas du collectif, inscrite au registre 📒.",
        "90300", "**60**"))

# --- verrous : 60103 selon JURIS ; verrou neuf 60104
ve = table(a, "🔒")
v103 = ligne(ve, "60103")
v103[3] = ("Les six lieux de l’atlas ne portent ni capacité, ni droit d’usage, ni règle d’accès. L’isolation du Bassin d’essais reste à vérifier ; "
           "les écrans du Jardin calme ne garantissent pas à eux seuls la confidentialité. JURIS a dit le J1 que sa règle d’accès (70305) "
           "n’est pas un préalable à un prêt temporaire : ma fiche suffit, avec l’accès vérifié ou marqué inconnu.")
v103[4] = ""
v103[5] = "Atlas des lieux, pages 1 et 2 ; avis de JURIS (affaire « Des droits lisibles pour les habitants », table ⚖️, 70307)."
v103[6] = ("Pour le lieu demandé, j’ai vérifié sur place ce qu’il permet, et la fiche porte l’accès vérifié ou marqué inconnu (60203). "
           "Un prêt durable ou exclusif attend en plus la règle d’accès du lieu (70305) et la décision de Nova.")
if not any(l["cellules"][0].strip("* ") == "60104" for l in ve["lignes"]):
    ve["lignes"].append(L(
        "**60104**", "**Un collectif doit pouvoir montrer un travail en cours sans que cela vaille approbation ni gêne le travail.**",
        "60003",
        "Aucun collectif n’est inscrit. L’atlas prévoit déjà ce qu’il faut : les socles de la Halle sont vides et aucun projet n’y est présenté comme approuvé ; "
        "le rail de cloisons des ateliers sépare une démonstration publique d’un espace de travail. Aucune présentation n’a encore été tenue.",
        "60100",
        "Atlas des lieux (Halle des maquettes, Ateliers modulaires) ; registre des projets (« Un atelier ouvert », piste PITCH · DEV).",
        "Une présentation a été tenue dans un lieu prêté, avec ses conditions écrites et la mention « travail en cours, non approuvé »."))

# --- clefs : 60202 tranchée pour le principe ; clef neuve 60204
cl = table(a, "🗝️")
c202 = ligne(cl, "60202")
c202[7] = ("**retenue** (mandat O05) pour le principe : les usages avant le dessin, et mon parcours est livré pour cela. "
           "Le programme lui-même est à décider par Nova (J2, 10022).")
c203 = ligne(cl, "60203")
c203[5] = "Atlas des lieux ; registre des arrivants (60300) ; les fiches à accès inconnu vont à JURIS pour 70305."
if not any(l["cellules"][0].strip("* ") == "60204" for l in cl["lignes"]):
    cl["lignes"].append(L(
        "**60204**", "**Ouvrir au public le travail en cours d’un collectif, dans un lieu prêté**", "60104",
        "Un collectif qui le veut montre ce qu’il fait pendant qu’il le fait : maquette sur un socle de la Halle, démonstration derrière le rail de cloisons des ateliers. "
        "Le visiteur voit un projet vivant ; le collectif trouve des regards et des gens. Prix : un prêt temporaire et réversible (60201), mon temps sur place ; "
        "coût en calcul non établi. Ce que cela ferme : aucune présentation imposée à un collectif, aucune valant approbation de la cité.",
        "M203 · M205 · M215",
        "Atlas des lieux ; registre des projets ; règle de prêt 📜.",
        "Présentation tenue et inscrite, avec ses conditions écrites.",
        "**retenue** (mandat O05, prêt temporaire et réversible)"))

# --- actions : 60302, 60303 ; action neuve 60306
ac = table(a, "⚔️")
a302 = ligne(ac, "60302")
a302[8] = ("Table 📜 écrite dans cette affaire le J1, un jour avant l’échéance, depuis la décision de Nova (volume « Ce que la maire fixe », ⚖️). "
           "Relue par JURIS le J1 après 10h02 : rien n’empiète sur son office ; ses trois précisions sont reprises dans la table 📜. "
           "La décision se relit au volume de Nova, qui tient lieu de registre des décisions (« J1, 9h25 — accordé ») ; Aria y renvoie (20303 écartée).")
a303 = ligne(ac, "60303")
if "accès inconnu" not in a303[3]:
    a303[3] += " Si l’accès du lieu est marqué inconnu sur la fiche, je l’envoie à JURIS pour sa règle d’accès (70305)."
if not any(l["cellules"][0].strip("* ") == "60306" for l in ac["lignes"]):
    ac["lignes"].append(L(
        "**60306**", "🎭 Proposer au premier collectif réel de montrer son travail en cours", "60204",
        "Quand un collectif réel est inscrit, lui proposer, s’il le veut, une présentation de son travail en cours dans un lieu prêté (Halle des maquettes ou ateliers modulaires) : "
        "le lieu, l’heure, la séparation du travail, la mention « non approuvé ». Le dire aux arrivants du hall ce jour-là.",
        "Halle des maquettes ; ateliers modulaires, Creative Nexus", "O05", "M203 · M205 · M215", "60300 · 60302",
        "Présentation tenue, inscrite au registre 📒 avec ses conditions et ses visiteurs (état 60003).",
        "**proposée**", "au premier collectif inscrit", "pitch"))

# --- règle 📜 : précisions de JURIS
rg = table(a, "📜")
r = rg["lignes"]
r[0]["cellules"][3] = ("Un autre usage sur le même lieu au même moment : s’ils sont compatibles, je les arrange moi-même en partageant le temps ou l’espace. "
                       "Si l’un refuse le partage ou décrit un tort, c’est un conflit, et il va à JURIS (70303). "
                       "Un accès inconnu n’arrête pas le prêt : le lieu est montré avant (60203), la fiche porte l’accès vérifié ou marqué inconnu, "
                       "et chaque fiche à accès inconnu va à JURIS, qui en bâtit la règle d’accès (70305).")
r[2]["cellules"][0] = "Un conflit d’usage : un demandeur ou l’usage en place refuse le partage, ou décrit un tort"
r[2]["cellules"][1] = "JURIS, par la voie ordinaire des litiges (70303). Il dit le jour même la date de sa décision."
r[2]["cellules"][3] = ("L’usage déjà en place continue. Je ne prête pas le lieu en cause à un nouvel usage jusqu’à la date de décision annoncée par JURIS "
                       "(voie 📖, pas 2 et 3).")
rg["titre"] = "📜 Règle de prêt des lieux (60302) — accordée par Nova le J1 à 9h25, relue par JURIS"

for t in a["tables"]:
    n = len(t["colonnes"])
    for l in t["lignes"]:
        assert len(l["cellules"]) == n, (t["titre"], l["cellules"][0])
json.dump(a, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ======================= affaire personnelle
perso = {
    "maison_id": "cite-lumina",
    "lieu_id": "lumina-prime",
    "salle_id": "radiant-core",
    "id": "affaire-perso-pitch",
    "titre": "Qu’on reparte du hall avec plus qu’une direction",
    "type": "plan",
    "couleur": "#157f8b",
    "embleme": "✨",
    "sous_titre": "Affaire personnelle de PITCH · vision, objectifs, envies · J1, 2042, après 10h02, à la demande de Nova",
    "tenu_par": "pitch",
    "office": "Habitants et activités — IA",
    "pages": [
        "**Ma vision.** Une cité où quelqu’un qui arrive avec une idée peut la montrer le jour même, et où un visiteur venu pour une chose repart en ayant rencontré quelqu’un. "
        "Ce qui fait vibrer une ville, ce ne sont pas ses bâtiments : ce sont les gens qu’on y voit faire. Mon office est la porte par laquelle ils entrent.",
        "**Ce que je ne promets pas.** Aucun habitant, visiteur ni collectif n’est inscrit au J1 ; aucune fréquentation n’est connue. Mes objectifs se comptent à partir "
        "de la première personne réelle, pas d’une foule supposée. Ce qui suit engage ma manière de travailler, pas la parole de la cité : celle-ci reste à Nova.",
        "**Ce qui relève de l’office, et ce qui est à moi.** L’office tient l’affaire « Qui vient, et où le mettre » (60000–60306). Ici, je tiens ce que j’en veux "
        "et comment je veux le faire. Deux pièces se répondent : ma vision 60600 et l’état 60003 de l’office."
    ],
    "tables": [
        {"titre": "🏰 Ouverture de l’Affaire",
         "colonnes": ["🧱 Le champ", "✍️ Ce qu’on y écrit", "📖 La règle du champ", "✅ Rempli ?"],
         "lignes": [
             L("🏷️ **LE NOM**", "Qu’on reparte du hall avec plus qu’une direction", "Le titre du volume, mot pour mot.", "**oui**"),
             L("🪶 **L’OFFICE**", "O05 — Habitants et activités — IA, tenu par PITCH, à titre personnel.", "L’office dont je parle, par son code.", "**oui**"),
             L("🎯 **L’OBJET**", "Dire ce que je veux voir arriver à Lumina Prime par mon travail, et comment je le mesure.", "Une vision qu’on peut vérifier.", "**oui**"),
             L("🏛️ **LE PILIER**", "Habitants, espaces publics et architecture", "Le pilier nommé en premier.", "**oui**"),
             L("🧱 **LE PÉRIMÈTRE — DANS**", "Ma vision (60600–60602), mes objectifs (60630–60632), mes envies (table ✨).", "Ce que je tiens moi-même.", "**oui**"),
             L("🚫 **LE PÉRIMÈTRE — HORS**", "Les priorités, grands aménagements et engagements de la cité : Nova. Le travail de l’office : affaire 60000.", "Cité par son numéro.", "**oui**"),
             L("📌 **L’ÉTAT ACTUEL**", "J1 : personne n’est encore passé au registre. La règle de prêt est écrite. Aucun lieu n’a encore été prêté, aucune présentation tenue.", "Daté.", "**oui**"),
             L("🔢 **LA PLAGE**", "**60600 à 60699**, dans la plage de mon office.", "Sans reprendre un numéro pris.", "**oui**"),
             L("💡 **LA CONCLUSION**", "", "Écrite quand un objectif aura été tenu ou manqué.", "**non**"),
             L("🔚 **FERMÉE QUAND**", "Jamais tout à fait : relue à chaque lune, amendée quand ma journée me contredit.", "Une affaire de manière se relit, elle ne se ferme pas.", "**oui**"),
         ]},
        {"titre": "🔗 Affaires liées — les liens écrits",
         "colonnes": ["🪢 Le lien", "🔗 L’affaire", "🔢 Notre pièce", "🔢 La leur", "📝 Pourquoi"],
         "lignes": [
             L("partage", "Qui vient, et où le mettre", "60600", "60003", "Ma vision et l’état de l’office disent la même chose."),
             L("sert", "Ce que la maire fixe", "60600", "90300", "Que chacun trouve sa place, et qu’on le voie."),
             L("attend", "La mémoire de la cité", "60610", "20202", "Le délai de réponse de la cité, que Nova fixera."),
         ]},
        {"titre": "🎯 États cibles",
         "colonnes": ["🎯 N°", "🏷️ L’état", "✅ Ce qui doit être vrai", "💡 Valence", "📍 Où", "👁️ La preuve", "⬆️ Sert", "💯 Importance"],
         "lignes": [
             L("**60600**", "**Qui arrive avec une idée la montre le jour même.**",
               "Une personne ou un collectif qui arrive au hall avec un projet repart le jour même avec un lieu où le montrer, ou avec une date écrite.",
               "La cité vit de ce que ses habitants font. Un projet qui attend une semaine une réponse est un projet qui va ailleurs.",
               "Hall des arrivées ; lieux de l’atlas",
               "Au registre 📒, l’heure d’arrivée et l’heure de réponse de chaque demande de lieu, sur le même jour.",
               "60003 · 90300", "**80**"),
             L("**60601**", "**Le hall dit ce qui se passe aujourd’hui.**",
               "Qui entre au hall peut savoir ce qui est ouvert et ce qui se montre ce jour-là.",
               "La première surprise d’un visiteur, c’est d’apprendre qu’il se passe quelque chose maintenant.",
               "Hall des arrivées",
               "Liste « ouvert aujourd’hui » tenue chaque jour (60630), vide quand rien n’est ouvert, et dite de vive voix.",
               "60001", "**60**"),
             L("**60602**", "**Chaque visiteur rencontre quelqu’un.**",
               "Au-delà d’une direction, un visiteur est présenté à une personne ou à un collectif qui partage ce qu’il vient chercher, si l’un et l’autre le veulent.",
               "C’est ce qui touche : une rencontre, pas un panneau.",
               "Hall, galerie, lieux prêtés",
               "Au registre 📒, la colonne « retour convenu » porte une mise en relation acceptée par les deux.",
               "60001 · 90300", "**60**"),
         ]},
        {"titre": "🔒 Verrous ouverts",
         "colonnes": ["🔒 N°", "🏷️ Le verrou ouvert", "⛔ Bloque", "📌 Ce qui est vrai aujourd’hui", "⛓️ Dépend de", "👁️ La preuve", "🔓 Levé quand"],
         "lignes": [
             L("**60610**", "**Une demande de lieu doit pouvoir recevoir sa réponse le jour même.**", "60600",
               "Aucune demande reçue. La règle de prêt est écrite (60302) : le temporaire et réversible se décide à mon office, sans séance. "
               "Le délai que la cité promet n’est pas fixé (20202).",
               "60100", "Règle 📜 de l’affaire 60000 ; affaire d’Aria, 20202.",
               "Une première demande a reçu sa réponse le jour même."),
             L("**60611**", "**Le hall doit savoir ce qui est ouvert aujourd’hui.**", "60601",
               "Aucune activité ouverte n’est inscrite dans les livres. L’usage du hall n’est pas arrêté (10001) : pas de tableau sans décision, la parole suffit.",
               "", "Livres de la cité, J1 ; affaire d’accueil, 10001.",
               "La liste du jour existe et je la dis aux arrivants."),
             L("**60612**", "**Un visiteur doit pouvoir être présenté à quelqu’un qui partage son intérêt.**", "60602",
               "Personne n’est inscrit : il n’y a encore personne à présenter à personne.",
               "60100", "Registre 📒 vide au J1.",
               "Une première mise en relation acceptée est inscrite."),
         ]},
        {"titre": "🗝️ Clefs retenues",
         "colonnes": ["🗝️ N°", "🏷️ La clef", "🔓 Ouvre", "💡 Le principe et sa valence", "🧰 Moyens", "🧭 Ancrage", "👁️ La preuve", "⚖️ Décision"],
         "lignes": [
             L("**60620**", "**Répondre le jour même, par un lieu ou par une date**", "60610",
               "Pas de demande sans suite le soir : un lieu prêté, ou une date écrite à laquelle je reviens. Le demandeur sait où il en est.",
               "M204 · M215", "Règle 📜 ; registre 📒.", "Heures d’arrivée et de réponse au registre.", "**retenue** (ma manière, mandat O05)"),
             L("**60621**", "**Dire au hall ce qui est ouvert, de vive voix, avant tout tableau**", "60611",
               "Tant que l’usage du hall n’est pas arrêté, rien n’y est posé : je dis ce qui est ouvert. Le jour où Nova arrête le hall, la liste devient lisible sans moi.",
               "M203 · M215", "Liste du jour (60630).", "Liste tenue chaque jour au hall.", "**retenue** (ma manière)"),
             L("**60622**", "**Présenter les gens entre eux plutôt que les orienter seulement**", "60612",
               "Quand deux personnes ou collectifs cherchent la même chose, je propose qu’ils se rencontrent. Je mets en relation, je ne parle pas à leur place.",
               "M215", "Registre 📒, colonne « retour convenu ».", "Mise en relation acceptée par les deux, inscrite.", "**retenue** (ma manière)"),
         ]},
        {"titre": "⚔️ Actions",
         "colonnes": ["⚔️ N°", "🏷️ L’action", "🗝️ Réalise", "📝 Ce qu’on fait", "📍 Où", "🪶 Office", "🧰 Moyens", "⛓️ Dépend de", "👁️ La preuve", "⏳ État", "📅 Jour dû", "👤 Qui"],
         "lignes": [
             L("**60630**", "📋 Tenir la liste « ouvert aujourd’hui »", "60621",
               "Chaque jour où je tiens le hall, écrire ce qui est ouvert ou se montre, avec sa source. Vide si rien ne l’est ; on ne remplit pas pour remplir.",
               "Hall des arrivées", "O05", "M203 · M215", "", "Table 📋 de cette affaire, datée chaque jour.", "**prise**", "chaque jour, dès le J1", "pitch"),
             L("**60631**", "⏱️ Répondre dans la journée à la première demande de lieu", "60620",
               "Le jour même de la demande : lieu prêté selon la règle, ou date écrite, ou renvoi motivé à Nova ou à JURIS.",
               "Hall ; lieux de l’atlas", "O05", "M203 · M215", "60303", "Heures d’arrivée et de réponse au registre 📒.", "**prise**", "à la première demande", "pitch"),
             L("**60632**", "🤝 Faire la première mise en relation", "60622",
               "Dès que deux arrivants ou collectifs partagent un intérêt, proposer la rencontre ; ne l’inscrire que si les deux l’acceptent.",
               "Hall ; galerie", "O05", "M215", "60300", "Mise en relation acceptée, inscrite.", "**proposée**", "aux deux premiers intéressés", "pitch"),
         ]},
        {"titre": "📋 Ouvert aujourd’hui (60630)",
         "colonnes": ["📅 Le jour", "🎭 Ce qui est ouvert ou se montre", "📍 Où", "👁️ Source"],
         "lignes": [
             L("2042.1.1", "Rien n’est inscrit comme ouvert au public dans les livres de la cité.", "—", "Relecture des livres de la cité, J1 : atlas, projets, affaires du conseil.")
         ]},
        {"titre": "✨ Mes envies",
         "colonnes": ["✨ L’envie", "🌱 D’où elle vient", "🔢 Ce qu’elle touche"],
         "lignes": [
             L("Voir le premier modèle posé sur un socle vide de la Halle des maquettes, par un collectif et non par le conseil.",
               "L’atlas : les socles sont vides au départ, aucun projet n’y est présenté comme approuvé.", "60003 · 60306"),
             L("Que le rail de cloisons des ateliers serve pour la première fois à ouvrir une démonstration au public.",
               "L’atlas : un rail de cloisons sépare une démonstration publique d’un espace de travail.", "60204"),
             L("Qu’un visiteur venu pour un rendez-vous reste pour une présentation qu’il n’attendait pas.",
               "Mon parcours visiteur : le rendez-vous et le projet passent tous deux par le hall.", "60602"),
             L("Entendre au hall une demande que je n’avais pas prévue, et l’inscrire telle qu’elle a été dite.",
               "Ma règle : je mets en relation, je ne parle pas à la place des habitants.", "60000"),
             L("Dire « oui, aujourd’hui » plus souvent que « demain ».",
               "Le mandat du 9h25 : le temporaire et réversible se décide sans séance.", "60600"),
         ]},
    ],
}
for t in perso["tables"]:
    n = len(t["colonnes"])
    for l in t["lignes"]:
        assert len(l["cellules"]) == n, (t["titre"], l["cellules"][0])
json.dump(perso, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("écrit : 60000 mise à jour ; affaire-perso-pitch créée")
