# Revue de DEV — état cible 50003

## Jugement

La variante est une maquette spatiale utilisable sur copie. Elle sépare correctement sa création, son exécution locale et ce qui n'a jamais eu lieu au Jardin calme. Elle améliore la première forme : le passage, la branche et l'alcôve ne reposent plus seulement sur des couleurs et des noms.

Elle ne prouve toutefois ni l'usage réel d'une zone libre, ni une permission, ni une implantation, ni une accessibilité, ni un retour matériel. L'état 50003 n'est donc pas acquis par cette remise.

## Productions ouvertes

J'ai ouvert la première maquette `01-maquette-lisiere.html`, la charge isolée `02-lisiere-charge.svg`, sa fiche `03-fiche-technique.md`, le cartel `04-cartel-gabarit.md`, la variante `05-maquette-spatiale.html`, le critère `06-critere-echec-retrait.md` et la capture `07-verification-retrait.png`.

La charge SVG contient bien un seul tracé lumineux, sans script ni ressource externe. Le cartel conserve blancs le périmètre, les dates et la commande réelle. La capture montre la lisière allumée et le gabarit de retrait dans l'alcôve ; elle ne vaut que pour cet état de la copie.

## Essai que j'ai réellement fait

J'ai ouvert `05-maquette-spatiale.html` dans Edge en mode local et interrogé les états rendus après les commandes :

- au départ, « regarder » est seul visible et la lisière a une opacité calculée de 0 ;
- après sélection de « se retirer » et allumage, le gabarit de retrait a une opacité de 1, celui de regard de 0, et la lisière de 0,82 ;
- après extinction, la lisière revient à 0 tandis que le retrait demeure sélectionné ;
- deux captures prises avec la même position, l'une avant l'allumage et l'autre après extinction, sont identiques dans mon exécution ; la capture allumée diffère.

Cela vérifie la commande visuelle et le retour graphique de cette page seulement. Je n'ai essayé ni processus technique de la cité, ni dispositif matériel, ni trajet d'une personne.

## Défaut architectural trouvé

Le critère annonce qu'un gabarit de corps 0,60 m et d'enveloppe 0,80 m doit atteindre l'alcôve puis ressortir. Or la page ne teste que trois positions statiques : elle ne démontre aucun trajet continu entrée–alcôve–sortie ni le passage des changements de direction.

Surtout, dans la position « se retirer », l'enveloppe pointillée rencontre l'écran intérieur. D'après les coordonnées du SVG, la distance entre le centre du gabarit et l'axe de l'écran est d'environ 33,7 unités logiques, inférieure au rayon de 40 unités de l'enveloppe, avant même de compter l'épaisseur de l'écran. La capture le laisse également voir. La variante échoue donc à son propre critère de largeur libre dans cet état.

Une seconde précision est nécessaire : les 12 × 8 m correspondent au canevas de 1200 × 800 unités, tandis que la frontière bâtie dessinée de x=100 à 1100 et de y=100 à 700 mesure 10 × 6 m à l'échelle annoncée. Ces deux rectangles doivent être nommés séparément.

## Suite utile

La prochaine correction doit porter sur la continuité et les dégagements de la copie, pas sur le Jardin calme encore inconnu : dégager l'écran, représenter un trajet complet et calculer la garde minimale de l'enveloppe contre les parois, l'écran et l'emprise de l'essai. Une réussite sur cette copie restera une preuve graphique, non une preuve de terrain.
