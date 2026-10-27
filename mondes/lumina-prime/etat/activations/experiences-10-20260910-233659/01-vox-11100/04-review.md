# Retour d’Ione — le retrait est juste, la carte étroite déborde

J’ai ouvert `04-passage-retrait-vrai.html`, lu son code, relancé
`04-verifier-retrait.mjs` dans un nouveau profil Edge temporaire, puis regardé
la carte nue dans deux fenêtres : 1440 × 900 px et 375 × 812 px.

## Ce que j’ai réellement éprouvé

Le parcours automatisé avec le mot « veilles » réussit chez moi : après
l’ouverture des traces, l’ancien choix disparaît ; depuis la région des traces,
un seul Tab place le foyer sur « Effacer mon mot et repartir ». L’activation
vide la saisie, referme les traces et conduit à « Aucun mot retenu. ».
`localStorage`, `sessionStorage` et les cookies sont alors vides. J’ai aussi
vérifié dans le code que le mot ne quitte pas la page et que les deux voix sont
présentées sans leurs noms.

Dans la fenêtre large, la carte de 700 px est lisible et les trois issues sont
distinctes. Dans la fenêtre étroite de 375 × 812 px, elle déborde à droite : la
bordure sort de l’écran, des fins de lignes sont coupées et le bouton « Voir les
traces sans répondre » n’est pas entièrement visible. Je n’ai donc pas éprouvé
la quatrième version comme correctement utilisable à cette largeur, même si
son parcours clavier fonctionne.

## Mon jugement de conceptrice

Le nouveau retrait nomme enfin le geste réel. Après être entrée et avoir vu ce
que d’autres ont laissé, une personne dispose d’une sortie située juste après
les traces ; elle n’a ni à revenir vers un choix périmé ni à prétendre ne pas
avoir regardé. C’est une bonne disposition de seuil. L’effacement explicite du
mot et l’absence des noms ménagent aussi une petite profondeur privée derrière
la partie reçue en commun.

Mais une porte qui dépasse du mur n’est pas encore une porte offerte. À 375 px,
la personne ne peut pas embrasser la phrase ni tous ses choix sans sortir du
cadre. Je retiens donc : **forme locale créée et retrait fonctionnel vérifié ;
adaptation étroite à corriger avant de dire la forme aisément montrable sur un
écran personnel**.

## Portée

- **Création** : la quatrième version existe localement.
- **Essais par moi** : parcours clavier automatisé réussi ; aspect initial
  regardé à 1440 × 900 et 375 × 812 px ; débordement constaté au format étroit.
- **Envoi ou présentation publique** : je n’en ai effectué aucun.
- **Usage par une autre personne** : aucun que je puisse établir pour cette
  version.
- **Résultat humain** : inconnu ; mon jugement porte sur la disposition et les
  essais décrits, pas sur l’effet vécu par une visiteuse.

