# Vérification — largeurs tenues

## Diagnostic de la quatrième version

J'ai cherché un débordement mesurable dans `04-passage-retrait-vrai.html` à
375 × 812, dans Edge, d'abord comme fenêtre de bureau émulée puis comme écran
mobile émulé. Dans ces deux essais, `innerWidth` et
`document.documentElement.scrollWidth` valaient 375 px ; la carte mesurait
343 px, de x=16 à x=359, et aucun élément visible ne franchissait le bord.

Je ne reproduis donc pas exactement le débordement vu par Ione et n'en invente
pas une cause certaine. Le code révélait toutefois une fragilité réelle : la
réduction reposait sur les tailles intrinsèques d'un champ en ligne et de
boutons flexibles, sans `min-width:0` sur les contenants ni composition mobile
explicite. C'est ce mécanisme que la cinquième version retire. Elle ne masque
pas le dépassement avec `overflow:hidden`.

## Correction créée

Dans `05-passage-largeurs-tenues.html` :

- `main`, les sections, la carte et les groupes de choix peuvent explicitement
  rétrécir ;
- champ et boutons ont une largeur maximale bornée par leur contenant ;
- sous 420 px, le champ devient un bloc de largeur disponible et chaque groupe
  de boutons une colonne `minmax(0,1fr)` ;
- les phrases et boutons autorisent la césure de secours.

Les mots, les trois issues, l'ordre du foyer, les voix sans noms et le retrait
« Effacer mon mot et repartir » sont conservés.

## Mesures et parcours

Script : `05-verifier-largeurs.mjs`. Trois profils Edge temporaires ont été
utilisés. À chaque largeur, j'ai mesuré la carte nue, parcouru au clavier
jusqu'aux traces, puis atteint et activé le retrait.

| Largeur | Carte nue | Traces ouvertes | Retrait |
|---:|---:|---:|---:|
| 320 px | scrollWidth 320 | scrollWidth 305 | scrollWidth 320 |
| 375 px | scrollWidth 375 | scrollWidth 375 | scrollWidth 375 |
| 1440 px | scrollWidth 1440 | scrollWidth 1440 | scrollWidth 1440 |

Dans les neuf mesures, `scrollWidth <= innerWidth`. Aucune phrase, aucun champ
et aucun bouton visible n'a franchi le viewport ni porté un débordement interne
mesuré. À chaque largeur : foyer sur `traces` après l'ouverture, un Tab vers
`erase-after-traces`, puis foyer sur `title-away`; mot effacé, stockage local,
stockage de session et cookies vides.

La région vocale d'un pixel est volontairement masquée et exclue du contrôle
des éléments visuels ; sa boîte interne contient le texte de l'annonce, mais
elle n'élargit jamais le document.

## Portée

Ces résultats sont des essais locaux automatisés. Ils n'établissent ni envoi,
ni usage par une autre personne, ni présentation publique, ni effet humain.
