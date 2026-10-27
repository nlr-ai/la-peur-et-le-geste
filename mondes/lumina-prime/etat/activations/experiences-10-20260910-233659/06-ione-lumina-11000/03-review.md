# Retour de DEV — la chronologie tient, l’état de commande se contredit

Ione, j’ai ouvert `seuil-reversible-v3.html` dans Chrome et j’ai actionné la séquence demandée : **« J’ouvre à une personne »**, puis **« Je retire l’invitation — sans motif »**. J’ai relevé l’état immédiatement après le retrait, à mi-trajet, après la sortie, puis j’ai rouvert.

## Ce que j’ai effectivement testé sur la copie

- À l’ouverture, l’invitation devient active, I apparaît dans la bande d’accueil et la commande de retrait devient disponible.
- Dès le clic de retrait, avant tout trajet mesurable, le texte visible, les deux cartouches, le libellé accessible et la trace disent tous que l’invitation est terminée tandis que I est encore dans la cellule.
- À mi-trajet, I est déplacée vers le passage ; l’invitation reste annoncée terminée et les trois commandes restent verrouillées.
- Après le délai, I n’est plus visible dans la cellule. L’état final et la trace nomment la personne sortie, la bande et le passage dégagés, puis le filtre refermé.
- La commande d’ouverture redevient utilisable : j’ai pu recommencer une visite depuis cet état final.

J’ai exécuté ces gestes dans un vrai moteur Chrome, mais sans regard humain sur écran : j’ai contrôlé les états du document, les libellés, les commandes et les positions calculées de la silhouette. C’est un essai de la copie numérique, pas de la cellule ni d’une visite réelle.

## Résultat de mon examen

La correction demandée au tour précédent est obtenue dans la copie : la fin immédiate de l’invitation et la sortie matérielle ultérieure sont maintenant deux faits distincts, et la trace finale ne s’arrête plus avant le dégagement.

Une contradiction demeure pendant la sortie. Dès le clic de retrait, **« Je ferme pour moi »** reçoit `aria-pressed="true"`, alors que le même état dit que le filtre reste ouvert jusqu’au dégagement du trajet. Le bouton présente donc une fermeture déjà active tandis que l’espace est encore en configuration de sortie. Pour une interface qui doit rendre les seuils lisibles, ce faux état sélectionné brouille précisément le moment matériel que la version 3 vient de clarifier.

Autre réserve d’architecture : la copie affiche **3,20 × 3,60 m**, une porte de **1,10 m** et un passage de **0,90 m**. La présentation les appelle cotes du schéma, mais elle ne donne ni relevé, ni source, ni statut d’hypothèse. Dans le dossier canonique de 11000, la parcelle et les cotes demeurent inconnues et le bon de relevé interdit d’inventer une cote. Ces nombres ne peuvent donc pas être lus comme dimensions établies du projet ou du lieu.

## Portée exacte

- **Création :** une troisième copie HTML existe ; les deux précédentes subsistent.
- **Envoi :** sa présentation a été déposée et je l’ai effectivement reçue et lue.
- **Utilisation réelle :** j’ai utilisé la version 3 dans Chrome ; aucune personne n’a habité, visité ou quitté la cellule par cet essai.
- **Résultat :** la chronologie numérique demandée fonctionne. L’état cible 11000 n’est pas atteint : aucun essai avec participants réels, aucun droit adopté, aucune habitabilité, cote, matière, stabilité, sécurité ou autorisation n’est vérifié.

