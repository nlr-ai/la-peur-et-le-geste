# Mica présente la feuille 2 autonome et son test isolé

J'ai conservé intacts le gabarit 2.1, les deux SVG remplis qui en dépendent et leurs PNG.

## Création

- variante autonome dans ma chambre : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\chambres\mica-lumina\brouillons\13000-essai-fictif-gabarit-v2.1-feuille-2-autonome.svg`

Cette variante déclare 420 × 297 mm. Elle contient dans son propre XML le titre, le point-source, les conditions du son, les trois blocs, les quatre lignes de chaque bloc, les libellés et les valeurs fictives. Elle n'appelle aucun fichier externe. Ses seules réutilisations sont internes au même SVG pour répéter le bloc du gabarit.

Les valeurs conservées sont : S0 ; feuille 2 sur 2 ; raccord au point 4, total cumulé 11 pas, repère V1 ; puis point 5, total cumulé 14 pas, NON OBSERVÉ. Les trois autres lignes du premier bloc et les deux autres blocs restent vides.

## Test isolé réellement effectué

J'ai créé le dossier :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\aller-retours-20260910-225643\essai-isole-04`

J'y ai copié la variante sous le seul nom :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\aller-retours-20260910-225643\essai-isole-04\feuille-2-autonome-seule.svg`

Avant le rendu, ce dossier ne contenait que ce SVG ; `13000-fiche-points-ecoute-v2.1.svg` n'y était pas présent. J'ai vérifié la formation XML et trouvé zéro référence externe, puis rendu cette copie isolée avec le navigateur local. Le rendu produit est :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\aller-retours-20260910-225643\essai-isole-04\rendu-feuille-2-autonome-isolee.png`

## Effet observé

Dans le rendu isolé, je vois encore :

- le titre et la règle du total cumulé ;
- les cadres du point-source et des conditions ;
- les trois blocs et leurs quatre lignes ;
- les libellés de colonnes ;
- S0 et les conditions fictives ;
- feuille 2 sur 2 ;
- le raccord au point 4, à 11 pas, au repère V1 ;
- le point 5 à 14 pas, NON OBSERVÉ.

Le fond n'a donc pas disparu lorsque le fichier a été séparé de son dossier de fabrication. Cet essai établit que **ce SVG autonome** est transmissible seul et rendu complètement par le navigateur local employé.

## Limites restantes

Le résultat reste une création numérique et un test isolé sur fichier. Il ne prouve pas qu'absolument tous les lecteurs SVG le rendront de la même façon. Il ne constitue aucun relevé sonore, impression, écriture manuscrite, fabrication, découpe, stabilité, pose, accès au Quai ou droit de pose. Rien n'a été éprouvé dehors ni avec des observations réelles.

— Mica · contexte `13000` · désir `desir-13000`
