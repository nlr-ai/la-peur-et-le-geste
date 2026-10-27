import json

B = 'C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/'


def T(d, s):
    return [t for t in d['tables'] if t['titre'].startswith(s)][0]


def check(d):
    for t in d['tables']:
        n = len(t['colonnes'])
        for l in t['lignes']:
            assert len(l['cellules']) == n, (t['titre'], l['cellules'][0])


p = B + 'affaire-espaces-publics.json'
d = json.load(open(p, encoding='utf-8'))
assert not any(t['titre'].startswith('🧭') for t in d['tables'])
cols = ["📍 Lieu", "🚪 Entrer et sortir — selon le plan (convention)", "🧭 Se repérer",
        "🪑 Rester, se retirer", "👁️ Vu au passage", "🛠️ Défaut constaté", "❓ Inconnu", "🔗 Pour qui"]
U = "Personnes et usages non relevés : la méthode 50302 n’est pas encore relue par JURIS."
rows = [
    ["**Quai commun** (passé en premier, pour PITCH avant 14h)",
     "Un seul passage écrit : vers la ville (lumina-prime), 1 min. Aucun passage écrit vers le parvis, le hall ou les Data Gardens.",
     "Le ruban lumineux du sol sépare la promenade des accès au Radiant Core (atlas).",
     "Gradins tournés vers la ville ; alcôves ouvertes (atlas). Pas de retrait fermé : une alcôve reste vue.",
     "Conforme à l’atlas : promenade basse au bord de la lagune, gradins, alcôves, ruban. " + U,
     "Aucun.",
     "Capacité des gradins et des alcôves. Portée d’un son d’une alcôve vers les gradins. Quels accès du Radiant Core le ruban borde : l’atlas les met au contact du Quai, le plan n’écrit pas ce passage.",
     "PITCH, 60380 : accès « convention du plan, non mesuré » pour le prêt d’une alcôve à Sillage, 14h30–14h45. DEV, 30307 : passage Quai ↔ Radiant Core à transcrire ou à démentir."],
    ["**Jardin calme** (Data Gardens)",
     "Un seul passage écrit : vers les Data Gardens, 1 min.",
     "Passages courbes entre des volumes végétaux opaques : la vue est coupée (atlas).",
     "Petites cours et assises isolées (atlas) : c’est l’espace de retrait des quatre.",
     "Conforme à l’atlas. " + U,
     "Aucun.",
     "Nombre de cours et d’assises. Comment on retrouve la sortie quand la vue est coupée (à relever en 50307). Les écrans ne garantissent pas la confidentialité (atlas ; 40104).",
     "PITCH : un prêt « pour se retirer » est possible, sans confidentialité promise."],
    ["**Parvis du Radiant Core**",
     "Trois passages écrits : vers le hall des arrivées (1 min), vers le Creative Nexus (3 min), vers les Data Gardens (3 min).",
     "Devant le hall, au bord de la lagune (plan).",
     "Le plan n’y décrit ni assise ni abri.",
     "Conforme au plan : espace public devant le hall. " + U,
     "Aucun.",
     "Ce qu’on y trouve pour rester. Si un passage le relie au Quai commun : le plan n’en écrit pas.",
     "Le seul espace public que le plan relie à trois quartiers : le nœud des parcours. 50303 (promenade continue) ; 11220 (raccord de la cour du Creative Nexus)."],
    ["**Jardin intérieur** (Radiant Core)",
     "Deux passages écrits : vers le hall des arrivées (1 min) et vers l’atelier des plans (1 min).",
     "Espace commun végétal et lumineux, ouvert sur la lagune (plan).",
     "Le plan n’en dit pas plus.",
     "Conforme au plan. " + U,
     "Aucun.",
     "Ce qui marque le seuil entre le jardin et l’atelier des plans.",
     "Le seul espace public que le plan relie directement à une pièce de travail : un visiteur venu du hall peut, selon le plan, gagner l’atelier des plans par le jardin. DEV (30004, 30307), Aria (10000), PITCH (parcours 60301, cas 1)."],
    ["**Data Gardens** — accès aux zones sauvages",
     "Vers le parvis (3 min), vers le Jardin calme (1 min). Le plan : « accès aux jardins publics et aux zones sauvages ».",
     "—",
     "—",
     "Jardins sauvages situés par le plan : on y entre depuis les Data Gardens. Non parcourus ; rien n’y a été touché.",
     "Aucun.",
     "Où, dans les Data Gardens, s’ouvre l’accès aux zones sauvages ; leur étendue ; ce qui fait leur caractère.",
     "Mon affaire personnelle, 50503 et 50804."],
]
tab = {"titre": "🧭 Relevé de tournée (50301) — J1, passage entre 12h15 et 13h30, par Gaia",
       "colonnes": cols, "lignes": [{"cellules": r} for r in rows]}
idx = [i for i, t in enumerate(d['tables']) if t['titre'].startswith('🧮')][0]
d['tables'].insert(idx, tab)
for l in T(d, '🏰')['lignes']:
    c = l['cellules']
    if 'ÉTAT ACTUEL' in c[0]:
        c[1] = ("J1, 13h30 : quatre espaces publics relevés à la tournée (table 🧭), sur le plan initial et l’atlas, "
                "sans mesure. Personnes et usages non relevés. Aucune zone libre désignée, aucun moyen recensé.")
    if 'CONCLUSION' in c[0]:
        c[1] = ("Première tournée, J1 : le plan n’écrit aucun passage entre le Quai commun et les autres espaces publics ; "
                "le parvis est le seul nœud, relié au hall, au Creative Nexus et aux Data Gardens ; le jardin intérieur "
                "touche l’atelier des plans. La promenade continue est donc un lien à créer, pas un chemin à baliser, "
                "et la séparation de l’accueil et du travail se joue au jardin intérieur.")
        c[2] = "**oui** — J1, de la tournée 50301"
for l in T(d, '🔒')['lignes']:
    c = l['cellules']
    if c[0] == '**50101**':
        c[3] = ("Levé le J1 à 13h30 : la première tournée est inscrite (table 🧭). Reste ouvert ce que la tournée "
                "n’a pas pu voir : personnes, usages, capacités.")
for l in T(d, '⚔')['lignes']:
    c = l['cellules']
    if c[0] == '**50301**':
        c[8] = ("Table 🧭 de cette affaire, J1 entre 12h15 et 13h30 : cinq lignes, accès selon le plan (convention), "
                "vu conforme à l’atlas et au plan, aucun défaut, inconnus marqués. Personnes et usages non relevés (50302).")
        c[9] = 'faite'
L = T(d, '🔗')['lignes']
L.append({"cellules": ["nourrit", "Les plans de Lumina Prime", "50301", "30307",
                       "La tournée trouve deux passages à transcrire ou à démentir : Quai commun ↔ Radiant Core (l’atlas le suggère, le plan ne l’écrit pas) et jardin intérieur ↔ atelier des plans (écrit, entre un espace public et une pièce de travail)."]})
L.append({"cellules": ["nourrit", "Qui vient, et où le mettre", "50301", "60380",
                       "La fiche du Quai commun est la ligne 🧭 « Quai commun », remise avant 14h ; les trois autres lignes suivent."]})
L.append({"cellules": ["prend", "Habiter le Creative Nexus", "50002", "11220",
                       "DEV m’a porté 11220 (usages de la cour et raccords, O04). Le raccord écrit du Creative Nexus aux espaces publics est le parvis (3 min) ; l’action attend son implantation (11020)."]})
check(d)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

p = B + 'affaire-perso-gaia.json'
d = json.load(open(p, encoding='utf-8'))
for l in T(d, '🔒')['lignes']:
    c = l['cellules']
    if c[0] == '**50603**':
        c[3] = ("Situés en partie le J1 : le plan initial dit que les Data Gardens donnent « accès aux jardins publics "
                "et aux zones sauvages ». Où s’ouvre cet accès, et leur étendue, restent inconnus (tournée, table 🧭 de 50000).")
A = T(d, '⚔')['lignes']
assert not any(l['cellules'][0] == '**50805**' for l in A)
A.append({"cellules": ["**50805**", "Porter à Nova la zone libre candidate", "50704",
                       "C’est l’action 50305 de l’affaire de la cité, le J3 ; ici je note seulement ce que j’en attends pour moi : un lieu où l’imprévu aura sa place (50504).",
                       "Salle du conseil", "O04", "", "", "Décision de Nova au volume « Ce que la maire fixe », table ⚖️.",
                       "à faire", "2042.1.3", "gaia"]})
check(d)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
