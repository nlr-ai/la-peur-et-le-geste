# Michel — personnage joueur

## Ouverture de Michel — choix de réaction

À la demande du joueur, l’introduction de Michel se termine par un choix explicite de réactions au journal radio du 15 juin 1940. Cette ouverture déroge à la règle générale sans menus. Le joueur peut répondre par un numéro, reprendre une réaction ou écrire la sienne. Aucun choix n’est encore fait ; ne pas lui attribuer de trait à partir d’une seule réponse.

1. « Je veux qu’on soit prêts, toi et moi. » Objectif initial : préparer avec Lucien une solution de repli concrète et vérifier les moyens nécessaires, sans décider d’un départ à sa place.
2. « Il doit y avoir des gens qui ont besoin d’aide. » Objectif initial : trouver à Niort un besoin précis lié à l’arrivée des réfugiés et accomplir une première aide à leur portée. Il faut d’abord découvrir ce besoin, pas inventer une mission déjà confiée.
3. « Je veux savoir ce qui se passe vraiment. » Objectif initial : recouper le bulletin avec une autre source identifiable et comprendre ce que l’avancée allemande change pour Niort. Ne pas livrer les secrets ou les réunions de Raymond par omniscience.
4. « Je refuse de rester à regarder. » Objectif initial : chercher un premier moyen concret et prudent de s’opposer à l’avancée allemande, en découvrant les personnes, les possibilités et les risques. Ni réseau de Résistance constitué, ni arme, ni engagement collectif supposé.

Après la réponse : inscrire un objectif concret dans `personnages.json` pour Michel, sous la forme {but, priorite: 1}, puis jouer son premier pas dans la scène, sans sauter au résultat. La réponse ouvre une direction, pas une réussite ni une personnalité définitive. Lucien complète le choix par une observation ou une initiative utile selon ses moyens ; il ne choisit pas pour Michel. Une réponse libre ou mêlée prime sur les quatre propositions : en tirer un objectif fidèle aux mots du joueur, sans demander une confirmation routinière.

Le choix initial utilise le module cliquable `Demandes`, demande_id `michel-j1-objectif-initial`. Les voie_id `proteger`, `aider`, `comprendre`, `agir` correspondent respectivement aux quatre objectifs ci-dessus. Un événement `demande` avec reponse `voie` porte le choix du joueur ; `expliquer` ou `refuse` ne fixe aucun objectif. `libre` suit ses propres mots.

## Entretien initial de Lucien — version active

Remplace le choix unique décrit plus haut. L’item `replique` porte cinq QCM `entretien`, affichés successivement par le module Demandes. Les réponses persistées arrivent dans `etat/inbox/michel/` comme actions `demande` avec demande_id `michel-lucien-gouts-v1-1` à `-5`. Relire ces réponses avant toute suite ; elles font autorité sur les préférences. Les axes sont priorité, activités, risque, rythme, rôle du frère. Les libellés libres priment sur toute catégorie ; un refus laisse l’axe indéterminé. Une demande d’explication ne répond pas à la question.

Pendant l’entretien, ne pas lancer une branche ni ajouter une question concurrente : le module affiche déjà la suivante. Répondre brièvement si une précision est demandée. Après la cinquième réponse, croiser les axes pour proposer en scène un premier pas concret cohérent et inscrire l’objectif initial de Michel sous {but, priorite: 1}. Ne pas transformer ces goûts en traits permanents, inventer un savoir ou garantir la réussite. Un rythme rapide saute seulement le routinier, jamais un choix du joueur. Les préférences sont révisables à tout moment. Un rôle actif de Lucien ne lui donne aucun pouvoir de choisir à la place de Michel. Les questions préparées sont des invitations : elles ne deviennent des paroles entendues qu’à mesure de l’entretien.

La ferveur de Michel est gouvernée par ses choix : appliquer la section « Ferveur de Michel — choix du joueur » du manuel de monde. Son score initial corrigé vaut 40 (base 30, choix explicite d'agir +10). Aucun trait politique procédural ne lui appartient.
