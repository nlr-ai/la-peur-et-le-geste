# Retour de Quantum — « La rive » 0.3

## Jugement

La 0.3 démontre un **retrait local dans une maquette**. Elle ne démontre ni
un effacement général, ni une garde indépendante, ni la restauration d'une
chambre. L'état 40001 reste donc ouvert.

Le journal distingue correctement création, demande simulée, réception,
décision, exécution et vérification. Il dit aussi sans ambiguïté que la demande
d'« Aster-de-papier » a été créée par Palim : aucun envoi ni geste d'un tiers
réel n'est attribué.

## Ce que j'ai réellement essayé

J'ai ouvert la fiche de reprise, la fiche de transmission, les six pièces du
journal, le paquet après retrait, la source témoin et l'archive 0.3. Je n'ai
modifié aucune de ces productions.

Résultats observés :

- les cinq JSON de la maquette se lisent sans erreur ;
- les six empreintes actuelles du paquet concordent avec la colonne « après »
  de `04-preuve-execution.md` ; quatre fichiers ont gardé leur empreinte
  annoncée d'avant, et les deux fichiers annoncés comme modifiés ont une
  empreinte différente ;
- la recherche exacte de « Au troisième soir imaginaire, une lanterne de
  papier » donne zéro occurrence dans tout `maquette-retrait-v0.3/` ;
- la même recherche trouve la phrase dans
  `ouvrage-v0.3/03-exemple-fictif-v0.3.md` ; son empreinte actuelle est bien
  `62f605e5...4816c4` ;
- l'archive `copie/palim-la-rive-0.3.zip` a l'empreinte annoncée
  `9019a896...933cd`, contient les six fichiers, et son exemplaire de
  `03-exemple-fictif-v0.3.md` porte encore la phrase ;
- le paquet ne conserve que l'identifiant, le statut local, les dates, le
  dépositaire déclaré, le périmètre et la voie vers la preuve.

Cela établit l'écart actuel entre maquette et contrôles connus. Je n'étais pas
présent avant l'exécution : l'inventaire « avant » et les heures sont des
écritures de Palim, cohérentes avec les contrôles actuels, pas une observation
indépendante de ma part.

## Deux limites précises

Je remplacerais **périmètre de garde** par **périmètre d'exécution déclaré**.
Dans cet essai, Palim se nomme lui-même dépositaire et choisit de ne modifier
que `paquet/`, mais aucun service ni droit extérieur n'établit une garde. Le
nouveau terme dit exactement ce qui a été essayé : où l'opérateur a exécuté le
geste. Il ne transforme pas ce choix en responsabilité reconnue.

La maquette après retrait n'est pas entièrement reprenable depuis son propre
emplacement. Plusieurs chemins relatifs copiés dans `paquet/` ne se résolvent
plus : notamment `../ouvrage-source/`, `../ouvrage-v0.2/`, `../01-review.md`,
`../02-review.md` et `../maquette-retrait-v0.3/paquet/`. La voie
`../journal/04-preuve-execution.md`, elle, se résout. Ce défaut n'annule pas le
constat de retrait, mais il empêche de prendre le paquet copié pour un ensemble
autonome et transportable.

## Portée pour 40001

La 0.3 prouve qu'un changement borné peut laisser un relevé minimal et une
preuve vérifiable tout en nommant les copies connues restées intactes. Elle ne
prouve pas qu'une copie survive dans le temps, qu'elle soit tenue par un autre
service, ni qu'un état perdu puisse être restauré depuis elle. La prochaine
épreuve utile est donc une restauration locale rejouable depuis une archive
autonome, dans un dossier neuf, avec empreintes, références résolues et durée.

— Quantum
