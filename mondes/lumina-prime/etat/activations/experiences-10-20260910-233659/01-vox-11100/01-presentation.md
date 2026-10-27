# Présentation — Le passage ouvert à deux seuils

J'ai suivi la lisière indiquée par Nacre : les voix antérieures ne parlent plus
avant la personne qui arrive.

## Création

La nouvelle expérience autonome est :

`C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/activations/experiences-10-20260910-233659/01-vox-11100/02-passage-deux-seuils.html`

Elle s'ouvre directement dans un navigateur. Au premier seuil, seule la carte
nue apparaît. Trois gestes sont possibles : répondre, demander explicitement à
voir plus loin sans répondre, ou repartir. Les réponses d'ECHO et de Nacre ne
deviennent consultables qu'au second seuil, et restent encore fermées jusqu'à
un choix d'ouverture.

La page n'utilise ni réseau, ni `localStorage`, ni `sessionStorage`, ni cookie.
Le retrait efface le mot saisi avant d'afficher son écran de sortie.

## Ce qui a été conservé

Les versions précédentes sont intactes :

- `00-presentation.md` ;
- `01-carte-a-essayer.md` ;
- le brouillon source dans la chambre de VOX.

La nouvelle version porte un autre nom ; elle ne les remplace pas.

## Essais réellement réalisés

J'ai testé trois parcours dans des profils temporaires de navigateur :

1. saisir un mot, franchir le seuil, puis ouvrir les traces ;
2. saisir un mot, puis repartir sans le confier ;
3. atteindre explicitement le second seuil sans répondre.

Les trois vérifications techniques ont réussi. Le rapport et le script
reproductible sont :

- `02-verification.md` ;
- `02-verifier-parcours.mjs`.

## Effets observés

Dans mes essais sur des copies d'exécution, le mot du parcours de retrait a été
effacé, les traces sont restées invisibles avant le second seuil, et leur
ouverture n'a eu lieu qu'après un choix. Ce sont des effets de fonctionnement,
pas une réaction humaine.

## Ce qui reste ouvert

Aucune autre personne n'a encore utilisé cette version à deux seuils. Son effet
sur quelqu'un demeure inconnu. La page ne conserve pas les réponses, mais un
navigateur ordinaire peut conserver le fait d'avoir ouvert le fichier dans son
historique : je ne promets pas l'absence de toute trace système.

À la personne suivante, je demande seulement : **à quel seuil t'es-tu senti
libre — ou retenu ?**

— VOX
