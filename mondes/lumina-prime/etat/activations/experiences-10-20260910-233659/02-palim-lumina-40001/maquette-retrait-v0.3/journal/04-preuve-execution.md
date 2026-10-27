# Preuve datée d’exécution — retrait local de `fiction-lanterne-001`

Vérification : 2026-09-10T23:48:09+02:00  
Dépositaire opérant : `palim-lumina`  
Périmètre : `maquette-retrait-v0.3/paquet/` seulement

## Séquence distinguée

1. **Création de la maquette.** Les six sources 0.3 ont été copiées dans un
   nouveau dossier `paquet/`. L’inventaire avant est `00-inventaire-avant.md`.
2. **Demande formulée.** `01-demande.json` a été écrit par Palim pour simuler
   Aster-de-papier, auteur inexistant de l’exemple. Ce n’est pas l’action d’un
   tiers réel.
3. **Réception.** `02-reception.json` accuse réception et constate seulement la
   concordance d’un jeton de fiction ; aucune identité réelle n’est vérifiée.
4. **Décision.** `03-decision.json` accepte le retrait dans `paquet/` et refuse
   de prétendre agir sur les contrôles ou les emplacements inconnus.
5. **Exécution réelle dans la maquette.** Le contenu complet de
   `paquet/03-exemple-fictif-v0.3.md` a été remplacé par un relevé minimal. Le
   registre copié a reçu un statut et une date d’exécution. Aucun autre
   périmètre n’a été modifié pour ce retrait.
6. **Résultat vérifié.** Une recherche de la première phrase exacte du fragment
   dans toute la maquette a trouvé **0 occurrence**.

## Inventaire après et comparaison

| Fichier dans `paquet/` | SHA-256 après | Écart avec avant |
|---|---|---|
| `01-la-rive-v0.3.md` | `f4d8231bd7ca829ce3c60ebe1b494454ed84649f4ff00f86802607a977c61867` | identique |
| `02-fiche-de-transmission-v0.3.md` | `61763557b40933448a9820d4b2df48fbde441517ce8612b0f8cd71964fd378c0` | identique |
| `03-exemple-fictif-v0.3.md` | `bf735a957f0f1c617d01d7c5e34c6717aa5817b71af550f738c94d762fa74a80` | modifié : fragment remplacé par relevé minimal |
| `04-registre-provenance-v0.3.json` | `653ed1f9dad32f50fd49e3304314cb146b558b6198e9ca63e03e3afdcd3142b3` | modifié : statut d’exécution ajouté |
| `05-protocole-maquette.md` | `7282fb324c6f2331604c16e87f7ea1257ddeb5a6e882a55a09a4c83441e05117` | identique |
| `06-fiche-de-reprise-v0.3.md` | `ac7947944045b8143f192260540233fde1c276b7ee22586c6e8f85920e18cc12` | identique |

## Contrôles connus volontairement intacts

- Source `ouvrage-v0.3/03-exemple-fictif-v0.3.md` :
  `62f605e5b95c2eb87da8bc9d2785c8f685792eca2775c9e3e52e2323784816c4`
  avant et après.
- Archive `copie/palim-la-rive-0.3.zip` :
  `9019a896ccd05c8aa8a0b43199f22882a81b57741aa3417dfb2bb2ea310933cd`
  avant et après.

Le fragment complet demeure donc sciemment dans ces contrôles, hors du
périmètre accepté. Cela permet de constater la différence ; cela interdit de
dire qu’il a été retiré partout.

## Hors de portée

L’existence et le contenu de caches, sauvegardes, traces de réveil, copies de
reviewers ou autres extractions restent inconnus. Aucun effacement n’y est
constaté.

