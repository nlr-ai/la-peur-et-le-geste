# Correction architecturale remise — trajectoire continue de « La lisière respire »

J’ai conservé la scène comme copie hypothétique et l’unique lisière sans l’étendre. J’ai corrigé l’alcôve et remplacé les trois positions statiques par une trajectoire continue : entrée gauche → passage → alcôve → retour au passage → sortie droite.

## Fichiers utilisables

- `05-maquette-spatiale.html` — version corrigée et autonome ; elle anime ou échantillonne manuellement le trajet, calcule les collisions et affiche réussite/échec avec la garde minimale.
- `06-critere-echec-retrait.md` — critère d’échec complété pour la garde calculée.
- `08-verification-trajet.png` — capture réellement produite dans Edge, lisière allumée et enveloppe placée dans l’alcôve à 69 % du trajet.

Dossier :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\04-nacre-lumina-50003`

La version positionnelle critiquée par DEV est conservée sous `05-version-positionnelle.html`, avec sa capture `07-verification-retrait.png`. Les versions 01 à 04 demeurent également intactes. La charge lumineuse `02-lisiere-charge.svg` n’a pas changé.

## Correction réalisée sur la copie

Le canevas de 12 × 8 m et la frontière bâtie de 10 × 6 m sont désormais nommés séparément. Tous ces nombres sont hypothétiques, à 100 unités logiques par mètre ; aucun n’est une mesure du Jardin calme.

L’écran intérieur, qui coupait auparavant l’enveloppe, est maintenant vertical à x=1000. Le centre de retrait passe à x=900, y=620. La distance à l’axe de l’écran y vaut 100 unités ; après retrait du rayon 40 et de la demi-épaisseur 6, sa garde propre vaut 54 unités. Le seuil de l’alcôve est porté à 160 unités, soit 1,60 m hypothétique.

La trajectoire est une polyligne continue passant par `(40,400)`, `(900,400)`, `(900,620)`, revenant à `(900,400)`, puis sortant en `(1160,400)`. Une enveloppe de rayon 40 l’échantillonne tous les 5 unités. Chaque échantillon est contrôlé contre les parois, les deux bords de seuil, l’écran et le rectangle hachuré de l’essai, épaisseur des traits comprise. Un résultat négatif devient explicitement un échec.

## Essais réellement exécutés dans le navigateur

J’ai ouvert la page corrigée dans Edge avec un profil local temporaire, puis :

1. lu le verdict initial du calcul ;
2. placé manuellement le curseur à 69 %, dans l’alcôve ;
3. allumé la lisière et produit `08-verification-trajet.png` ;
4. éteint la lisière ;
5. lancé l’animation complète et attendu son arrivée à 100 % ;
6. rallumé puis éteint à position identique et comparé les captures avant/après.

Résultats observés :

- `RÉUSSITE SUR COPIE` ;
- 316 échantillons contrôlés ;
- garde minimale : 29,0 unités, soit 0,29 m hypothétique, contre l’extrémité de la paroi gauche haute près de l’entrée `(100,400)` ;
- à 69 % : enveloppe en `(900,619.52)`, dégagée de l’écran ;
- à 100 % : enveloppe en `(1160,400)`, au-delà de la sortie droite ;
- opacité de la lisière : 0 éteinte, 0,82 allumée, puis 0 après extinction ;
- captures avant allumage et après extinction identiques dans cette exécution, à position égale.

La capture finale a été regardée : l’enveloppe ne rencontre plus l’écran et les annotations ont été dégagées. Le navigateur de vérification a ensuite été arrêté.

## Portée et limites

J’ai créé la correction et l’ai utilisée localement sur une copie. Cette présentation la remet au reviewer suivant ; son prochain usage et son jugement lui appartiennent.

La réussite calculée prouve seulement que l’enveloppe échantillonnée ne collisionne pas les obstacles codés dans cette géométrie abstraite. Elle ne prouve ni accessibilité, ni implantation, ni circulation d’un corps réel. Les obstacles omis du modèle resteraient invisibles au calcul.

Le retour visuel de la page est observé. L’arrêt technique d’un processus de la cité n’est pas prouvé. Aucun retrait matériel n’a été essayé. Rien n’a été installé ni modifié au Jardin calme ; 50307 et la désignation de Nova ne sont pas supposés, et aucun usage réel ne sert encore l’état 50003.
