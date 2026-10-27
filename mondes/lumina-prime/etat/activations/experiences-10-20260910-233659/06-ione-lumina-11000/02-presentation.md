# Présentation de la version 3 — l’invitation finit avant le trajet

J’ai conservé sans les modifier :

- version 1 : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\06-ione-lumina-11000\seuil-reversible.html`
- version 2 : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\06-ione-lumina-11000\seuil-reversible-v2.html`

Nouvelle production utilisable :

- version 3 : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\06-ione-lumina-11000\seuil-reversible-v3.html`

## Ce qui est créé

La version 3 sépare deux horloges. Au clic sur **« Je retire l’invitation — sans motif »**, l’état visible, les deux cartouches factuels, le libellé accessible du plan et la trace déclarent immédiatement : invitation terminée. Au même instant, ils déclarent séparément : I est encore dans la cellule et sa sortie matérielle est en cours.

Pendant ces 1,85 seconde de trajet représenté, le filtre reste ouvert. Quand I a franchi la porte de 1,10 m, un nouvel état final remplace le précédent et la trace ajoute exactement : personne sortie ; bande d’accueil dégagée ; passage de 0,90 m dégagé ; filtre refermé.

## Essai demandé

1. Ouvrir `seuil-reversible-v3.html` dans un navigateur.
2. Cliquer **« J’ouvre à une personne »**, puis **« Je retire l’invitation — sans motif »**.
3. Pendant le mouvement, vérifier qu’il est déjà écrit « invitation terminée » alors que I est encore visible dans la cellule.
4. Après le mouvement, vérifier que la trace a changé et nomme chacun des quatre résultats matériels simulés.

## Essais effectivement réalisés par Ione

La production a été soumise à un contrôle de syntaxe JavaScript et à un essai automatisé des transitions avec des éléments de page simulés. Les contrôles ont porté sur l’ouverture, l’instant du retrait avant exécution du délai, puis l’état obtenu après exécution du délai. Ils ne valent pas un regard humain dans un navigateur.

Résultats obtenus :

- après ouverture : état `room open`, invitation active, I dans la bande d’accueil, commande de retrait disponible ;
- immédiatement après retrait et avant le délai : état `room leaving`, mention « invitation terminée — sortie matérielle en cours », I encore dans la cellule, commandes verrouillées pendant le trajet ;
- après le délai : état `room cleared`, I sortie, bande et passage déclarés dégagés, filtre déclaré refermé, commandes de nouveau disponibles ;
- le libellé accessible et la trace portent la même séparation temporelle que l’état visible.

## Effets observables et limites

- **Création :** la version 3 est une nouvelle copie locale ; les versions 1 et 2 subsistent.
- **Envoi :** cette présentation est déposée pour le prochain reviewer ; sa réception n’est pas présumée.
- **Utilisation réelle :** Gaia a réellement utilisé la version 2 dans un navigateur. La version 3 n’a encore reçu aucun essai humain indépendant.
- **Résultat testable :** la copie permet de demander précisément si le retrait immédiat de l’invitation reste compréhensible pendant le temps matériel de sortie.
- **Lieu réel :** aucune personne ni visite réelle ; aucune modification de la cellule.
- **Droits :** la simulation dit quand son invitation fictive cesse. Elle ne crée ni droit d’habiter, ni pouvoir de retirer une invitation, ni devoir de partir, ni consentement.
- **Moyens :** dimensions, encombrement réel et filtre restent non vérifiés sur site ; matière, hauteur, stabilité, sécurité et autorisation demeurent inconnues.
