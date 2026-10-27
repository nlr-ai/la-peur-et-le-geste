# Le tableau libre

Dans La peur et le geste, l’onglet **Le tableau** remplace l’échiquier.

- Déposer une icône depuis la palette ; un clic l’ajoute aussi dans la zone visible.
- Glisser les éléments pour les déplacer. Décocher **Grille** pour un placement libre.
- Cliquer **Relier**, puis l’origine et la destination de la flèche. Échap revient au déplacement.
- Sélectionner une icône pour changer son nom ; sélectionner une flèche ou une icône puis **Supprimer la sélection**. Supprimer une icône retire aussi ses liens.
- Filtrer la palette par mot ou catégorie, zoomer et faire défiler la surface.

La sauvegarde automatique est propre au monde et au personnage : `mondes/la-peur-et-le-geste/chambres/<personnage>/tableau/disposition.json`. L’indicateur distingue les changements en attente, enregistrés et les erreurs. Deux onglets concurrents ne s’écrasent pas silencieusement : une version obsolète doit être rechargée.

Surface de 2400 × 1536, grille de 24, maximum 500 icônes et 1500 flèches. Les dessins ne déclenchent aucune action du MJ ni aucun passage du temps.

Vérification : `node serveur/test_tableau_libre.js` (persistance, suppression, conflit de version, séparation des personnages, validation et service des fichiers). Essai navigateur : dépôt de deux icônes, flèche, déplacement, renommage, rechargement et suppression des éléments d’essai.


## Langage du fil

La bascule clair/codé est partagée entre le tableau et le bouton placé au-dessus du fil. Les noms du catalogue `assets/icones-objets/manifest.json` et les variantes explicites de `alias-fil.json` servent de dictionnaire. Les expressions les plus longues ont priorité et les mots ne sont pas remplacés à l’intérieur d’autres mots.

Les termes repérés sont soulignés en pointillé ; leur infobulle donne l’autre formulation. La détection suit les nouveaux messages. Elle concerne l’affichage du fil, jamais le texte enregistré ni la saisie du joueur. C’est une substitution lexicale, sans réécriture grammaticale des phrases ni traduction automatique des formes absentes du dictionnaire. Le mot isolé « or » est volontairement absent des alias pour ne pas traduire la conjonction.

## Étapes suggérées

Les 60 actions affichent sous leur nom une liste à puces issue de `assets/icones-objets/etapes-actions.json`, intégrée au manifeste par `generer.py`. Les préalables (`after`), rôles et types de ressources proviennent du catalogue Modern Front ; les étapes de préparation et de suivi sont des suggestions éditoriales par famille, avec des séquences spécifiques pour le recrutement et l’entreprise de couverture. Ce ne sont ni des conditions vérifiées dans la partie ni des actions exécutées. Les listes suivent le choix clair/codé et apparaissent aussi sur les actions déjà posées. Les ressources et termes seuls restent compacts.

## Chaînes de tâches

Les étapes sont désormais des nœuds distincts reliés dans l’ordre sous chaque action. Chaque étape peut être déplacée, renommée, reliée, supprimée ou marquée terminée. Le champ `stepIndex` conserve la correspondance bilingue tant que son libellé est vide ; `done` conserve son état. `todoExpanded` empêche toute recréation des tâches supprimées après rechargement. Les anciennes actions sont développées une seule fois à l’ouverture ; leurs liens existants restent en place. Une sauvegarde avant conversion est conservée pour Michel.

## Nœuds typés

Les étapes textuelles automatiques sont remplacées par des entités du catalogue : actions préalables, métiers avec effectif, ressources avec quantité. `noeuds-types.json` conserve les relations `after`, `roles`, `consumes`, `produces` de Modern Front. Besoins et préalables pointent vers l’action ; les produits sont reliés dans l’autre sens. Ces quantités sont celles du modèle, pas un inventaire du joueur. Treize métiers sont disponibles dans la palette ; leurs pictogrammes réutilisent ceux des actions. La quantité des métiers et ressources se modifie dans le pied de page. `typedExpanded` empêche les duplications au rechargement. Les anciennes chaînes générées sont converties ; les libellés personnalisés sont conservés, ainsi que les liens externes redirigés vers l’action. Sauvegarde Michel : disposition.avant-types.json.
