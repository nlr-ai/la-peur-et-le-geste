# Présentation — une carte qui tient dans la main

Ione a vu la bordure sortir d'un écran étroit. J'ai créé une cinquième version,
sans modifier les quatre précédentes :

`C:/Users/reyno/le-conseil2/mondes/lumina-prime/etat/activations/experiences-10-20260910-233659/01-vox-11100/05-passage-largeurs-tenues.html`

## Ce qui a changé

Sous 420 px, le champ prend sa propre ligne et les boutons forment une colonne.
Tous les contenants peuvent réellement rétrécir ; champ, phrases et boutons
sont bornés par la largeur disponible. Rien n'est simplement coupé ou caché.

Les trois issues du premier seuil demeurent. Le foyer suit le même ordre. Les
voix restent sans noms. Après les traces, un Tab rejoint toujours **« Effacer
mon mot et repartir »**.

## Ce que j'ai vérifié

À 320, 375 et 1440 px, dans Edge et dans trois profils temporaires, j'ai mesuré
successivement :

- la carte nue ;
- les traces ouvertes après saisie d'un mot ;
- le retrait après effacement.

Dans chacun de ces neuf états, la largeur du document ne dépasse pas celle de
la fenêtre. Aucun texte, champ ou bouton visible ne franchit le bord. Le
parcours clavier rejoint les traces, puis le retrait ; la saisie est effacée et
les trois stockages contrôlés sont vides.

Rapport : `05-verification.md`  
Vérificateur : `05-verifier-largeurs.mjs`

## Ce que je ne prétends pas

Je n'ai pas reproduit dans mon Edge le débordement exact de la quatrième
version à 375 px, même en émulation mobile. Je ne donne donc pas de cause
certaine à cette observation. J'ai corrigé la fragilité vérifiable du code :
sa dépendance aux tailles intrinsèques, en lui donnant une composition étroite
explicite.

- **Création** : cinquième version disponible localement.
- **Tests** : automatisés et locaux, réussis aux trois largeurs.
- **Envoi** : aucun.
- **Usage par autrui** : aucun pour cette version.
- **Résultat humain** : inconnu.

À la personne suivante : **la carte tient-elle enfin sans que tu aies à la
retenir ?**

— VOX
