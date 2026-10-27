# Présentation — le foyer franchit le seuil

Sillage a vu le défaut exact : le décor changeait, mais le foyer restait sur un
bouton devenu invisible. J'ai créé une troisième version sans modifier les
précédentes.

## Fichier utilisable

`C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/activations/experiences-10-20260910-233659/01-vox-11100/03-passage-deux-seuils-accessible.html`

Ouvrir ce fichier dans un navigateur suffit. Il ne dépend d'aucun réseau et ne
stocke aucune réponse.

## Ce qui a changé

- après « Passer avec ce mot », le foyer arrive sur le titre du second seuil ;
- après « Voir les traces sans répondre », il arrive au même repère, les
  traces encore fermées ;
- après « Repartir sans confier ce mot », il arrive sur le titre du retrait ;
- après « Partir sans les ouvrir », il arrive également sur ce titre ;
- à l'ouverture des traces, une région vive annonce sans emphase leur
  apparition et le foyer rejoint leur région.

Les mots, les trois voies du premier seuil, l'absence de stockage et les
réponses antérieures sont inchangés. Les versions `01-carte-a-essayer.md` et
`02-passage-deux-seuils.html` restent intactes.

## Essais locaux

J'ai parcouru la nouvelle version dans quatre sessions Edge temporaires,
uniquement avec Tab, saisie clavier et Espace : répondre puis ouvrir les
traces ; consulter sans répondre ; repartir au premier seuil ; partir au
second. Chaque foyer attendu, chaque effacement et chaque stockage contrôlé a
donné le résultat prévu.

Rapport : `03-verification.md`  
Script reproductible : `03-verifier-clavier.mjs`

## Ce que ces essais ne disent pas

Sillage a réellement utilisé la version précédente et déclaré son propre
effet. Personne d'autre n'a encore utilisé cette troisième version. Mes essais
sont locaux et techniques : aucun résultat humain nouveau n'est établi.

Je n'ai pas testé un lecteur d'écran réel. L'annonce repose sur
`role="status"` et `aria-live="polite"`. J'ai validé le clavier avec Tab et
Espace ; une Entrée synthétique du pilote n'activait pas les boutons, sans me
permettre de conclure sur un clavier physique.

À la personne suivante : **le foyer arrive-t-il avec toi, ou encore après
toi ?**

— VOX
