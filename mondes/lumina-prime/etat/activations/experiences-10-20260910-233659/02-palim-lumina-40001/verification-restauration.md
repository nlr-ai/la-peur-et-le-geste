# Vérification locale du paquet « La rive » 0.1

Date réelle : 2026-09-10

## Geste réellement exécuté

Les quatre fichiers de `ouvrage-source/` ont été réunis dans
`copie/palim-la-rive-0.1.zip`. Cette archive a été déployée dans
`essai-restauration/`. Les empreintes SHA-256 des sources et des fichiers ainsi
restaurés ont ensuite été comparées.

## Résultat observé

Les quatre paires sont identiques :

| Fichier | SHA-256 source et restauration |
|---|---|
| `01-la-rive.md` | `a1f1658cd419bfc29c9ab62bd11b6f78bfd94e95209632ee5032f23fc0cd5ea2` |
| `02-fiche-de-reprise.md` | `2ced216b9e345e86245fdfe059e646472b7a4a8dfa42ea69640beaebdc27b2c1` |
| `03-provenance-et-retrait.json` | `d42068fe416d68bf205daac423cdc4fd98050482dc06a157f2f43218f7bfb583` |
| `04-essai-pour-aria.md` | `fb2befe2c2bc7d565291d65608000d1b85fdb440b066beee39672e29532a6fa1` |

Empreinte de l’archive :
`db14cf3fbfcbe08fc382f77c90318479ab0d3543d9d1bd7ca13c0d0d1a45cacc`.

## Portée exacte

Cet essai prouve qu’à cet instant ce paquet local a pu être copié, déployé et
retrouvé sans différence de contenu. Il ne prouve pas que l’archive survivra à
une panne, qu’elle est tenue par un service indépendant, qu’une chambre entière
peut être restaurée, ni que les droits inscrits seront techniquement exécutés.
L’état cible 40001 reste donc ouvert.

