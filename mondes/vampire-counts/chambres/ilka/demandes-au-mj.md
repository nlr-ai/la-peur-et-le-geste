# Demandes au meneur — Ilka

### 1. Inscription de Toma, bailli mortel de Ticușu Vechi
- **Ce qui est écrit** : `lieux.json` définit Ticușu Vechi comme une ville contrôlée par `maison-ticusu`, mais aucun habitant vivant, régisseur ou bailli n'est rattaché à l'administration quotidienne des granges, des métairies et des bandes de serfs.
- **Ce que je demande à la place** : Enregistrer Toma (52 ans, mortel, bailli de Ticușu) comme intendant du manoir et représentant des vivants de la seigneurie dans le décor local de Ticușu Vechi, sans nécessairement en faire un agent jouable à part entière.
- **Pourquoi** : Ilka dormant tout le jour et évitant le soleil, il est indispensable qu'un mortel de confiance tienne le compte des feux, gère les rations de grain et rassemble les bandes au crépuscule pour la rentrée au manoir.

### 2. Inscription de Mara, goule liée d'Ilka
- **Ce qui est écrit** : Ilka n'a aucune suite ni serviteur nommé dans `personnages.json` ou `routines.json`, alors que la condition d'installée et les règles du monde rappellent que le jour appartient aux goules et que les messages voyagent par porteurs de sang.
- **Ce que je demande à la place** : Ajouter Mara (goule liée depuis 12 ans, issue d'une famille locale de Ticușu) comme servante de chambre et messagère de confiance d'Ilka.
- **Pourquoi** : Permet à Ilka de faire surveiller les abords du manoir de jour, d'envoyer des plis vers Rupea ou Comăna sans s'exposer, et d'assurer le guet au seuil de la crypte durant son sommeil.

### 3. Précision sur le statut vassalique et le tribut envers Vlaicu
- **Ce qui est écrit** : `maison-ticusu` a `allegeance_affichee: null` dans `maisons.json`, tandis que le canon et `personnages.json` mentionnent qu'Ilka est jurée à Vlaicu. De plus, Vlaicu est actuellement marqué `etat: dormant` dans `personnages.json`.
- **Ce que je demande à la place** : Confirmer si l'allégeance affichée de `maison-ticusu` doit pointer vers `maison-comana` (la maison de Vlaicu et Radomir) ou rester non formalisée sur le plan diplomatique, et à qui le tribut de sang d'Ilka est remis pendant la torpeur de Vlaicu (aux intendants de Comăna ou mis en réserve).
- **Pourquoi** : Cela clarifie la chaîne d'autorité réelle au sud si Cendrik ou un autre seigneur venait contester les frontières de Ticușu pendant l'hiver.
