raise SystemExit("PÉRIMÉ (J1) : script déjà servi ; il réécrirait des cellules depuis une lecture ancienne. Relire le livre et ne corriger que sa part.")
# -*- coding: utf-8 -*-
"""J1, après 10h12 — les réponses de DEV à mes trois questions d'espace (sa table ❓, 30301)
portées dans ma table 🚶 (60301), et le lien d'attente vers 30307 écrit."""
import json

F = r"C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/affaire-habitants-collectifs.json"
a = json.load(open(F, encoding="utf-8"))


def col(t, motif):
    return next(i for i, h in enumerate(t["colonnes"]) if motif in h)


fait = []
for t in a["tables"]:
    ti = t["titre"]
    if ti.startswith("🚶"):
        kb = col(t, "Besoin d")
        ki = col(t, "Inconnu")
        for l in t["lignes"]:
            c = l["cellules"]
            if c[0].startswith("Un rendez-vous municipal"):
                c[kb] = ("Un seuil lisible entre le hall et le salon. Le salon est-il atteint depuis le hall sans traverser la galerie ? "
                         "Réponse de DEV, J1 après 10h12 (sa table ❓) : inconnu tant que les connexions du Radiant Core ne sont pas transcrites (30307). "
                         "Une place d’attente hors du passage sera dessinée dans ses deux esquisses (30305), sans affectation.")
                c[ki] = ("La confidentialité réelle d’un entretien : une cloison opaque sépare la vue, sans rien garantir (40104, 40205 ; droits, JURIS). "
                         "DEV le confirme le J1 : même avec deux pièces séparées, aucune confidentialité n’est promise ; c’est l’essai de Quantum (40205, 40305).")
                fait.append("cas 2")
            if c[0].startswith("La présentation d’un projet"):
                c[kb] = ("Une galerie accessible depuis le hall sans traverser le travail. Un endroit où poser une maquette. "
                         "La galerie peut-elle recevoir un public pendant qu’un entretien se tient au salon ? "
                         "Réponse de DEV, J1 après 10h12 : inconnu pour l’espace, faute de savoir si galerie et salon partagent un seuil (30307). "
                         "L’usage de la galerie reste à Nova (10010).")
                fait.append("cas 3")
    if ti.startswith("🔗"):
        if not any(l["cellules"][2] == "60301" and l["cellules"][3] == "30307" for l in t["lignes"]):
            t["lignes"].append({"cellules": [
                "attend", "Les plans de Lumina Prime", "60301", "30307",
                "Mes trois questions d’espace restent sans réponse tant que DEV n’a pas transcrit les connexions du Radiant Core. "
                "Le plan est inscrit au registre des moyens d’Aria sous M201."]})
            fait.append("lien 30307")

json.dump(a, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(fait)
