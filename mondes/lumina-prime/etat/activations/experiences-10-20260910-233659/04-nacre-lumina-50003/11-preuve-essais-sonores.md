# Preuve d’exécution sur copie — variation sonore

Environnement : `09-apparition-sonore.html` ouverte localement dans Edge headless avec un profil temporaire. Les états ont été interrogés dans la page ; aucune installation ni liaison à un système de la cité.

## Passage silencieux

- avant : état `muted`, contexte absent, 0 source, 0 contexte créé ;
- après « Passer en silence » : gabarit à `translate(745 270)`, contexte absent, 0 source, compteur de contextes créés toujours à 0 ;
- résultat : le parcours visuel a atteint la sortie sans créer ni démarrer de contexte audio.

## Apparition menée à son terme

- pendant : état `playing`, contexte présent et `running`, 3 sources actives, 1 contexte créé ;
- durée codée des sources : arrêt au plus tard à 2,8 s ;
- premier essai : échec du retour d’interface, car Edge headless n’a pas livré les événements `ended` dans le délai observé ; la page restait « en cours » ;
- correction : ajout d’une garde temporelle indépendante à 2,85 s, qui ferme le contexte même si les événements de fin ne reviennent pas ;
- nouvel essai après correction : état `muted`, contexte absent, 0 source active, motif « garde temporelle fermée ».

## Coupure en cours

- avant coupure : état `playing`, contexte `running`, 3 sources actives ;
- après « Couper maintenant » : état `muted`, contexte absent, 0 source active ;
- action du code : gain forcé à zéro, sources arrêtées et déconnectées, contexte fermé.

## Ce que je n’ai pas observé

Je n’ai pas accès ici à une écoute qui me permette d’affirmer avoir entendu l’apparition. Je n’ai mesuré ni pression, ni portée, ni isolement, ni silence acoustique. Les constats portent sur les commandes, l’état Web Audio et la copie visuelle, pas sur un lieu réel.
