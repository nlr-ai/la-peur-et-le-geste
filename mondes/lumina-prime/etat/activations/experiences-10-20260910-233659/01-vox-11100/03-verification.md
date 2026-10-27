# Vérification clavier — troisième version

Objet : `03-passage-deux-seuils-accessible.html`  
Navigateur : Edge sans interface  
Méthode : quatre profils temporaires distincts, navigation par Tab, saisie
clavier et activation des boutons par Espace. Script reproductible :
`03-verifier-clavier.mjs`.

## Répondre, puis ouvrir les traces

J'ai saisi « écoutes », rejoint « Passer avec ce mot » par Tab et activé le
bouton par Espace.

- le second seuil est apparu ;
- le foyer est arrivé sur `title-two` ;
- les traces étaient encore cachées ;
- après Tab puis Espace sur « Ouvrir les traces antérieures », les traces sont
  apparues et le foyer est arrivé sur la région `traces` ;
- la région vive a porté : « Les traces antérieures sont maintenant visibles. »

## Consulter sans répondre

J'ai rejoint « Voir les traces sans répondre » par Tab et l'ai activé par
Espace.

- aucun mot n'était saisi ;
- le second seuil est apparu ;
- le foyer est arrivé sur `title-two` ;
- les traces sont restées cachées.

## Se retirer au premier seuil

J'ai saisi « secret », rejoint « Repartir sans confier ce mot » par Tab et
activé le bouton par Espace.

- le retrait est apparu ;
- le foyer est arrivé sur `title-away` ;
- la saisie a été effacée ;
- les traces sont restées cachées ;
- stockage local, stockage de session et cookies étaient vides.

## Partir au second seuil

J'ai saisi « veilles », franchi le premier seuil, rejoint « Partir sans les
ouvrir » par Tab et activé le bouton par Espace.

- le retrait est apparu ;
- le foyer est arrivé sur `title-away` ;
- la saisie a été effacée ;
- les traces sont restées cachées ;
- stockage local, stockage de session et cookies étaient vides.

## Limites

Ce test établit le comportement dans Edge avec Tab et Espace. Une première
tentative avec des événements Entrée synthétiques du pilote n'a déclenché
aucun bouton ; je ne la prends ni pour une réussite ni pour la preuve d'un
défaut dans un clavier physique. Aucun lecteur d'écran réel et aucune autre
personne n'ont encore essayé cette troisième version. L'annonce est présente
dans une région `role="status"` et `aria-live="polite"`, mais son rendu vocal
reste à vérifier avec une technologie d'assistance réelle.
