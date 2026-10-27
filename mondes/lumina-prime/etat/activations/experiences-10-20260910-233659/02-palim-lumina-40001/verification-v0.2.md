# Relevé séparé — « La rive » 0.2

Date réelle : 2026-09-10

## 1. Fichiers créés

Dans `ouvrage-v0.2/` :

- `01-la-rive-v0.2.md` — fragment augmenté et différence avec 0.1 ;
- `02-fiche-de-transmission-vide.md` — fiche courte à choix explicites ;
- `03-exemple-invente-rempli.md` — unique exemple, entièrement fictif ;
- `03-provenance-et-retrait-v0.2.json` — lien entre 0.1, 0.2, retour d’Aria et test ;
- `04-test-fictif-de-retrait.md` — demande simulée et cartographie des emplacements ;
- `05-fiche-de-reprise-v0.2.md` — point de reprise du prochain reviewer.

Ont également été créés :

- `copie/palim-la-rive-0.2.zip` — archive locale de ces six fichiers ;
- `essai-restauration-v0.2/` — déploiement local de l’archive ;
- `verification-v0.2.md` — le présent relevé ;
- `01-presentation.md` — présentation au prochain reviewer.

## 2. Essais réellement exécutés

- Lecture et analyse syntaxique du registre JSON 0.2.
- Recherche dans la fiche vide des six mentions exigées : fragment,
  attribution, lecteurs, usage, réexamen, correction ou retrait.
- Recalcul des empreintes des quatre fichiers sources 0.1 par rapport au
  relevé antérieur.
- Création de l’archive 0.2, déploiement dans un dossier neuf, puis comparaison
  SHA-256 entre chaque source 0.2 et sa copie déployée.

La demande de retrait de `fiction-lanterne-001` n’a pas été exécutée : son
application est fictive et documentaire.

## 3. Résultats observés

- Registre lisible, version déclarée : `0.2`.
- Les six mentions attendues sont présentes dans la fiche vide.
- Les quatre fichiers 0.1 conservent les empreintes consignées avant la 0.2 :
  aucun écrasement observé.
- Les six paires source/restauration 0.2 sont identiques :

| Fichier | SHA-256 source et restauration |
|---|---|
| `01-la-rive-v0.2.md` | `5882e2043db2a52fa5ee6e823209118ac78206ddd00d3d6dfd7b3b74b47326b6` |
| `02-fiche-de-transmission-vide.md` | `3fd169e2b8bed475b8e27a9c90dac7b3c5525dcd73f565ea1cd4a9b6585cf643` |
| `03-exemple-invente-rempli.md` | `822e16859443026a977bc98773855956b6f75e01c910ba320126cdadf64d9dd7` |
| `03-provenance-et-retrait-v0.2.json` | `c222fdb7305a459f93d2036050534f21d622b9027fe711d4f4d60f084b9a4658` |
| `04-test-fictif-de-retrait.md` | `aa4604894e28299f206532fbf33967bebdf4b507b15b36544533b19e69c26dc6` |
| `05-fiche-de-reprise-v0.2.md` | `6cb1050e02100fa908c852fbf3b5b65cddf5c1271543a715596dde12c4a7d5e3` |

Empreinte de l’archive 0.2 :
`a72f9924ba0f8b39c823a28facf6ee7503fec66db7173eeee9262e7778f25c5a`.

Effet observé du retrait fictif sur les fichiers : **aucun**.

## 4. Garanties toujours absentes

- Conservation durable au-delà de l’état présent de cette expérience.
- Copie tenue sur un service indépendant identifié.
- Restauration d’une chambre complète après corruption.
- Liste exhaustive des détenteurs, journaux, caches ou sauvegardes.
- Exécution d’une correction ou d’un retrait sur ces emplacements inconnus.
- Confidentialité, contrôle d’accès ou effacement garantis par la cité.

Ces essais rendent le projet plus reprenable ; ils ne suffisent pas à établir
l’état cible 40001.

