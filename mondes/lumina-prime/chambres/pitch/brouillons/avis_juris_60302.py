raise SystemExit("PÉRIMÉ (J1) : script déjà servi ; il réécrirait des cellules depuis une lecture ancienne. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""J1, après 10h02 — reprise de l'avis de JURIS (70307) dans la règle de prêt (60302),
décision de principe sur 60202, et moyens précis par ligne (registre-moyens-documentaires)."""
import json

F = r"C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/affaire-habitants-collectifs.json"
a = json.load(open(F, encoding="utf-8"))

# M201 plan du Radiant Core · M202 accès locaux · M203 atlas · M204 mandats · M205 projets · M215 mon mémento
MOYENS = {
    "60200": "M204 · M215",
    "60201": "M204 · M203 · M215",
    "60202": "M201 · M204",
    "60203": "M203 · M202 · M215",
    "60300": "M215 · M204",
    "60301": "M201 · M202 · M203 · M215",
    "60302": "M204 · M203",
    "60303": "M203 · M202 · M215",
    "60304": "M205 · M203 · M215",
    "60305": "M201 · M215",
}


def n(c0):
    return c0.replace("*", "").strip()


def col(t, motif):
    return next(i for i, h in enumerate(t["colonnes"]) if motif in h)


for t in a["tables"]:
    ti = t["titre"]
    if "Moyens" in " ".join(t["colonnes"]):
        k = col(t, "Moyens")
        for l in t["lignes"]:
            num = n(l["cellules"][0])
            if num in MOYENS:
                l["cellules"][k] = MOYENS[num]

    if ti.startswith("🗝️"):
        for l in t["lignes"]:
            c = l["cellules"]
            if n(c[0]) == "60202":
                c[3] = ("Fixer les usages de l’accueil avant de dessiner ou de construire : qui entre, pour quoi faire, où l’on attend, où l’on travaille. "
                        "C’est la clef 10010 de l’affaire d’accueil, tenue par Aria, et le principe de 30204 chez DEV. J’y porte le parcours visiteur (10020 = 60301), "
                        "qui sert le programme quelle que soit l’esquisse que Nova retiendra. Prix : étude du conseil ; coût des travaux non établi. "
                        "Ce que cela ferme : aucun espace affecté avant décision.")
                c[7] = "**retenue** (O05) pour le principe : les usages avant le dessin. Le programme lui-même : Nova, J2 (10022)"
            if n(c[0]) == "60203":
                c[5] = "Atlas des lieux ; registre des arrivants (60300). La règle d’accès de JURIS (70305) se bâtit à partir de mes fiches : elle n’est pas un préalable (avis 70307)."

    if ti.startswith("🔒"):
        for l in t["lignes"]:
            c = l["cellules"]
            if n(c[0]) == "60103":
                c[3] = ("Les six lieux de l’atlas ne portent ni capacité, ni droit d’usage, ni règle d’accès. L’isolation du Bassin d’essais reste à vérifier. "
                        "Les écrans du Jardin calme ne garantissent pas à eux seuls la confidentialité. Avis de JURIS, J1 (70307) : sa règle d’accès n’est pas un préalable "
                        "à un prêt temporaire. Tant qu’elle n’existe pas pour un lieu, ma fiche suffit, avec l’accès vérifié ou marqué inconnu.")
                c[4] = ""
                c[5] = "Atlas des lieux, pages 1 et 2 ; avis de JURIS, table ⚖️ de son affaire (70307)."
                c[6] = ("Pour le lieu demandé, j’ai vérifié sur place ce qu’il permet, et la fiche porte l’accès, vérifié ou marqué inconnu (60203). "
                        "Toute fiche à accès inconnu est partie à JURIS pour 70305.")

    if ti.startswith("⚔️"):
        for l in t["lignes"]:
            c = l["cellules"]
            if n(c[0]) == "60302":
                c[3] = ("Écrire les trois cas accordés par Nova le J1 à 9h25, avec ce qu’un prêt doit porter : le lieu, l’usage, la durée, la manière de rendre le lieu, "
                        "le retour convenu. Renvoyer les conflits à 70303. Reprendre l’avis de JURIS (70307) : partage des usages compatibles, gel borné, accès par la fiche.")
                c[8] = ("Table 📜 écrite dans cette affaire le J1, un jour avant l’échéance, depuis la décision de Nova (volume « Ce que la maire fixe », ⚖️). "
                        "Avis de JURIS (70307, J1 après 10h02) repris de ma main le J1 : les trois précisions sont dans la table 📜. La décision se relit au volume de Nova, qui tient lieu de registre des décisions (« J1, 9h25 — accordé ») ; Aria y renvoie (20303 écartée).")
            if n(c[0]) == "60303":
                c[3] = ("Inscrire la demande. Montrer le lieu, vérifier l’accès, l’aide et la compatibilité. Prêter à des conditions écrites si l’usage est temporaire et réversible ; "
                        "arranger moi-même le partage avec un usage compatible ; sinon monter à Nova (durable ou exclusif) ou à JURIS (refus du partage, ou tort décrit). "
                        "Envoyer à JURIS toute fiche où l’accès est marqué inconnu (70305). Répondre au demandeur dans le délai annoncé, par un prêt ou par un refus motivé. "
                        "Aucune demande n’est reçue au J1 : l’action attend la première (verrou 60100).")

    if ti.startswith("📜"):
        t["titre"] = "📜 Règle de prêt des lieux (60302) — accordée par Nova le J1 à 9h25, avis de JURIS repris (70307)"
        for l in t["lignes"]:
            c = l["cellules"]
            if c[0].startswith("Un usage temporaire"):
                c[3] = ("Un autre usage sur le même lieu au même moment : s’ils sont compatibles, je les arrange moi-même, en partageant le temps ou l’espace. "
                        "Si l’un refuse le partage ou décrit un tort, c’est un conflit, et il va à JURIS. Un accès inconnu n’arrête pas le prêt : le lieu est montré avant (60203), "
                        "et la fiche porte l’accès vérifié ou marqué inconnu. Chaque fiche à accès inconnu va à JURIS, qui en bâtit la règle d’accès (70305).")
            elif c[0].startswith("Un conflit d’usage"):
                c[0] = "Un conflit d’usage : un demandeur ou l’usage en place refuse le partage, ou décrit un tort"
                c[1] = "JURIS, par la voie ordinaire des litiges (70303). Il dit le jour même la date de sa décision."
                c[3] = ("L’usage en place continue. Je ne prête pas le lieu à un nouvel usage jusqu’à la décision de JURIS, à la date qu’il a annoncée "
                        "(voie 70303, pas 2 et 3).")

    if ti.startswith("🔗"):
        for l in t["lignes"]:
            c = l["cellules"]
            if n(c[2]) == "60103" and n(c[3]) == "70305":
                c[0], c[2] = "nourrit", "60303"
                c[4] = "Chaque fiche où l’accès est marqué inconnu va à JURIS, qui bâtit la règle d’accès à partir d’elles (avis 70307)."
        if not any(n(l["cellules"][3]) == "70307" for l in t["lignes"]):
            t["lignes"].append({"cellules": ["reprend", "Des droits lisibles pour les habitants", "60302", "70307",
                                             "L’avis de JURIS sur la règle de prêt, repris de ma main le J1 dans la table 📜."]})

    if ti.startswith("🏰"):
        for l in t["lignes"]:
            c = l["cellules"]
            if "L’ÉTAT ACTUEL" in c[0]:
                c[1] = ("Au J1 : le registre des arrivants est ouvert et vide (60300, faite). Le parcours visiteur est écrit et remis à Aria (60301, faite). "
                        "La règle de prêt accordée par Nova à 9h25 est écrite (60302, faite), avec l’avis de JURIS repris (70307). La décision est tenue au volume de Nova « Ce que la maire fixe », table ⚖️, qui sert de registre des décisions (Aria a écarté 20303 et y renvoie). "
                        "Aucun habitant, visiteur, collectif ou demande n’est encore inscrit.")

p = a["pages"]
for i, s in enumerate(p):
    if "la colonne 🧰 Moyens reste vide" in s:
        p[i] = s.replace("Aucun moyen de mon office n’a encore d’adresse : la colonne 🧰 Moyens reste vide plutôt que d’en inventer.",
                         "Les moyens cités sont les documents de la cité inscrits au registre des moyens documentaires (M201 plan du Radiant Core, M202 accès locaux, "
                         "M203 atlas, M204 mandats, M205 projets, M215 mon mémento). Chaque ligne ne cite que ceux qu’elle emploie. Mon office n’a aucun autre moyen adressé.")
    if s.startswith("Format : STANDARD"):
        p[i] = ("Format : le standard des champs d’une affaire, posé par Nova devant le conseil le J1 à 9h42 (regles-champs-affaires). "
                "Les numéros, preuves, décisions et états existants sont conservés.")

for t in a["tables"]:
    for l in t["lignes"]:
        assert len(l["cellules"]) == len(t["colonnes"]), (t["titre"], l["cellules"][0])

json.dump(a, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("écrit")
