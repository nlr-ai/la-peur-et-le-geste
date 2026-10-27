# Variation remise — une apparition que l’on peut ne pas entendre

J’ai conservé `05-maquette-spatiale.html` intacte. À côté, j’ai créé une écoute locale et autonome où le silence est l’état d’origine et de retour, non un fond sonore continu.

## Fichiers utilisables

- `09-apparition-sonore.html` — variation à ouvrir au casque ou dans un navigateur ; trois commandes : « Entendre une apparition », « Couper maintenant », « Passer en silence ».
- `10-verification-sonore.png` — capture produite pendant l’apparition, après un passage silencieux arrivé à la sortie.
- `11-preuve-essais-sonores.md` — états réellement observés dans les trois cas, y compris un premier échec et sa correction.

Dossier :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\04-nacre-lumina-50003`

Toutes les versions 01 à 08 demeurent. Le SHA-256 de `05-maquette-spatiale.html` est resté `f3ec3c14f3c98a3b7e858cb86feb2645924989fd2a77a6b8928b7eccc4ddd586` avant la création de cette variation ; je ne l’ai pas modifiée.

## Ce que j’ai créé

La page garde l’unique lisière lumineuse au-dessus d’un passage sombre. Aucun son ne part au chargement. « Passer en silence » anime seulement un gabarit de l’entrée à la sortie et ne construit pas de contexte audio.

« Entendre une apparition » est le seul geste qui crée Web Audio. Il lance localement trois oscillateurs sinusoïdaux, sans média ni ressource externe, sans boucle, avec une enveloppe brève. Les trois sources ont un arrêt programmé au plus tard à 2,8 secondes. Une garde indépendante ferme le contexte à 2,85 secondes si les événements de fin du navigateur ne reviennent pas.

« Couper maintenant » annule l’enveloppe, force le gain à zéro, arrête et déconnecte les sources, ferme le contexte et affiche de nouveau « muet ». La page ne demande ni microphone, ni entrée, ni identité et ne conserve aucun journal.

## Trois essais réellement exécutés dans Edge

### Passer en silence

Avant le geste : contexte absent, 0 source, 0 contexte créé. Après le parcours : le gabarit était à la sortie `(745,270)` ; le contexte restait absent, avec 0 source et toujours 0 contexte créé.

### Laisser l’apparition finir

Pendant : contexte présent et `running`, 3 sources actives, état affiché « apparition en cours ».

Le premier essai a échoué : les sources étaient programmées pour s’arrêter, mais Edge headless n’a pas livré leurs événements `ended` dans le délai observé ; l’interface restait « en cours ». J’ai ajouté la garde temporelle, puis rechargé la page. Au second essai, après le terme : état `muted`, contexte absent, 0 source active.

### Couper en cours

Avant la coupure : contexte `running`, 3 sources actives. Deux cents millisecondes après la commande : état `muted`, contexte absent, 0 source active.

Le navigateur m’a donc montré que les trois chemins de commande atteignent les états attendus après correction. `10-verification-sonore.png` montre l’état en cours, mais une image ne prouve évidemment aucun son.

## Ce que le code garantit

- aucune lecture automatique et aucune boucle ;
- aucun contexte audio créé par le passage silencieux ;
- sources programmées pour s’arrêter au plus tard à 2,8 s et garde de fermeture à 2,85 s ;
- coupure locale du gain, des sources et du contexte ;
- aucune ressource externe, captation, identification ou persistance.

## Ce que je n’ai pas pu entendre ou mesurer

Mon accès de vérification ne m’a fourni aucune sortie à écouter : je ne dis donc pas avoir entendu l’apparition. Je n’ai mesuré ni volume, ni pression, ni portée, ni fuite, ni silence acoustique. L’état `running` et les trois sources sont des constats du navigateur, pas une preuve d’audibilité.

Cette variation est utilisée seulement sur copie. Elle ne prouve aucun silence, retrait, arrêt technique ou usage réel au Jardin calme. Rien n’y est installé ; 50307 et une désignation de Nova ne sont toujours pas supposés, et l’état 50003 n’est pas acquis.
