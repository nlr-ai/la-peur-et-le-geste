raise SystemExit("PÉRIMÉ (J1, 20h4x) : ce script réécrit des cellules entières depuis des phrases figées. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""J1 — 60302 : la règle de prêt des lieux, écrite depuis la décision de Nova du J1 à 9h25."""
import json

F = r"C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/affaire-habitants-collectifs.json"


def L(*c):
    return {"cellules": list(c)}


a = json.load(open(F, encoding="utf-8"))
a["tables"] = [t for t in a["tables"] if not t["titre"].startswith("📜")]

regle = {
    "titre": "📜 Règle de prêt des lieux (60302) — accordée par Nova le J1 à 9h25",
    "colonnes": ["🧾 Le cas", "⚖️ Qui décide", "📝 Ce que le prêt porte", "🚫 Ce qui l’arrête"],
    "lignes": [
        L("Un usage temporaire, réversible et non exclusif",
          "PITCH (O05), seul. Il rend compte après, au registre 📒.",
          "Le lieu, l’usage, la durée, la manière de rendre le lieu, le retour convenu, le demandeur et la source de la demande.",
          "Un autre usage sur le même lieu au même moment : c’est un conflit, et il passe à JURIS. Un accès inconnu : le lieu est montré avant tout prêt (60203), et la règle d’accès vient de JURIS (70305)."),
        L("Un usage durable, ou exclusif",
          "Nova, sur le dossier que PITCH lui présente.",
          "Les mêmes champs, plus ce que le prêt retire aux autres usages du lieu et pour combien de temps.",
          "Rien n’est promis au demandeur avant la décision de Nova."),
        L("Un conflit d’usage, entre demandeurs ou avec un usage existant",
          "JURIS, par la voie ordinaire des litiges (70303).",
          "Les parties, le lieu, les usages en conflit, ce qui a déjà été prêté.",
          "Je ne prête pas le lieu en cause à un nouvel usage tant que JURIS n’a pas décidé."),
        L("Un changement d’aménagement : cloison, construction, affectation d’un espace",
          "Nova, qui décide des grands aménagements (registre du conseil). DEV en tient le plan (30003).",
          "Ce n’est jamais un prêt. La demande est renvoyée à Nova avec ce que le demandeur voulait faire.",
          "Aucun seuil ni aucune cloison sans décision d’usage (30204)."),
        L("Ce qu’aucun prêt ne promet",
          "—",
          "Pas de confidentialité non vérifiée (40104). Pas de capacité non mesurée (40302). La zone à laisser libre, quand Nova l’aura désignée (50003), n’est prêtée à aucun usage unique.",
          "Le délai de réponse à une demande n’est pas encore fixé : il revient à Nova (20202). D’ici là, PITCH dit au demandeur quand il reviendra vers lui, et il l’inscrit."),
    ],
}

# Placer la règle juste après les tables structurelles.
i = next(k for k, t in enumerate(a["tables"]) if t["titre"].startswith("🚶"))
a["tables"].insert(i, regle)

for t in a["tables"]:
    if t["titre"].startswith("⚔️"):
        for l in t["lignes"]:
            c = l["cellules"]
            if c[0] == "**60302**":
                c[8] = "Table 📜 écrite dans cette affaire le J1, un jour avant l’échéance, depuis la décision de Nova (volume « Ce que la maire fixe », ⚖️). Aria la porte au registre des décisions (20303)."
                c[9] = "**faite**"
                c[10] = "2042.1.2 (écrite le J1)"
    if t["titre"].startswith("🔒"):
        for l in t["lignes"]:
            c = l["cellules"]
            if c[0] == "**60102**":
                c[3] = ("Nova a fixé les trois cas le J1 à 9h25. La règle est écrite dans cette affaire le J1 (table 📜, 60302). "
                        "Elle n’est pas encore au registre des décisions, qu’Aria ouvre à la clôture de la séance (20303).")
    if t["titre"].startswith("🏰"):
        for l in t["lignes"]:
            c = l["cellules"]
            if "L’ÉTAT ACTUEL" in c[0]:
                c[1] = ("Au J1 : le registre des arrivants est ouvert et vide (60300, faite). Le parcours visiteur est écrit et remis à Aria (60301, faite). "
                        "La règle de prêt accordée par Nova à 9h25 est écrite (60302, faite) ; elle attend le registre des décisions (20303). "
                        "Aucun habitant, visiteur, collectif ou demande n’est encore inscrit.")

pages = a["pages"]
pages[1] = ("**Décidé par Nova le J1 à 9h25** (volume « Ce que la maire fixe », table ⚖️, « accordé ») : je prête seul un lieu pour un usage temporaire et réversible ; "
            "le durable ou l’exclusif lui revient ; les conflits vont à JURIS. C’est la clef 60201, écrite en règle le J1 à la table 📜 (60302). "
            "**Reste à Nova :** le programme d’accueil (60202, qui est la clef 10010 d’Aria, présentée le J2 par 10022), le délai de réponse à une demande (20202), "
            "et chaque prêt durable ou exclusif, au cas par cas.")

for t in a["tables"]:
    n = len(t["colonnes"])
    for l in t["lignes"]:
        assert len(l["cellules"]) == n, (t["titre"], l["cellules"][0])

json.dump(a, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("écrit :", [(t["titre"][:40], len(t["lignes"])) for t in a["tables"]])
