# La peur et le geste — Niort

Monde indépendant de Westeros. Le départ jouable reprend la fin de la troisième réunion chez Raymond et Josette, le 18 juin 1940. L’heure de 21 h est une convention technique de mise en place ; le RP ne fixe que « après le repas ». Le calendrier du moteur garde ses mois de trente jours.

Raymond est le personnage joueur à la reprise. Aucune création de maison féodale. Le MJ joue directement les PNJ, avec leurs fiches sous chambres/<id>/fiche.md. Consigner paroles et actes ; ne pas réveiller une session séparée par réplique.

Les trois sources RP sous sources/modern-front/docs/rp/ à la racine du dépôt définissent la continuité adoptée pour ce nouveau monde. Elles n’ont pas modifié Modern Front. Les possessions et secrets de l’instantané sont des données de préparation ; ne pas en faire des connaissances partagées. Les fiches complètes sont dans personnages/ à la racine du dépôt et dans les chambres de ce monde.

Reprise : Raymond, Josette, Jacques, Émile et Ernest sont dans la maison Moreau. Solange et Maurice sont absents ; leur position précise reste inconnue. Michel et Lucien ne participent pas à la réunion ; leur nom de famille reste à établir. En juin 1940, Michel a 19 ans et Lucien 16 ans. Michel est une fiche minimale de liaison familiale, pas Michel Vinet importé. Lucien a trois ans de moins que lui. Aucun événement du RP ne leur est connu automatiquement.

Aucun revolver acquis ; aucune adhésion collective à la lutte armée. Les feuilles sont conservées sans être prêtées. Ernest a différé la copie ; Josette cherche encore à qui adresser les demandes sur les prisonniers. Les captifs et les demandeurs anonymes restent sans identité inventée. Aucune émission précise n’a été établie à la fin de la scène.

Les réunions de 1940 sont le départ de cette branche. La cible Michel/Niort 1943 de Modern Front n’autorise aucun saut silencieux de trois ans. Le moteur .NET de Modern Front n’est pas raccordé au présent serveur narratif.

## Lieux déjà établis

# La peur et le geste

Le MJ incarne directement les PNJ, selon le socle commun du dépôt. Le monde reprend les lieux de Modern Front autour de Niort et Coulon. Les dix lieux de `etat/lieux.json` et leurs intérieurs sont canoniques pour cette fiction.

`provenance-lieux.json` conserve les identités et coordonnées sources. Les lieux générés ne deviennent pas des établissements historiques attestés par leur adoption dans le canon. Tous les intérieurs sont des créations de fiction. Le type technique `chateau` désigne ici un bâtiment doté de pièces, pas un château médiéval.

Les plans sont schématiques, sans échelle. Les passages intérieurs sont établis ; les trajets entre sites, les accès autorisés, les occupants et la scène de départ ne le sont pas encore. La pièce nommée « Cellule » est un espace représentatif, pas le relevé complet de la prison. Le répertoire public des plans n’accorde aucun droit d’entrée au personnage.

Les personnages et la scène de reprise sont désormais initialisés séparément de la création des lieux. Ne pas ouvrir une partie Westeros à cause du journal vide. Le moteur de simulation Modern Front n’est pas encore raccordé.

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

Identité du PJ choisie : Michel Sauzeau, Modern Front 6116, employé à Niort. Âge adapté conservé : 19 ans. Voir provenance-michel.json et personnages/michel.md ; ne pas attribuer à Lucien un homonyme de la simulation.

Mise à jour : Lucien Sauzeau est ajouté dans la simulation active comme frère de Michel, même foyer 2547. IDs actuels : Michel 406, Lucien 407 ; 6116 reste uniquement l’ancien identifiant de Michel dans l’export source. Cette intégration remplace les mentions antérieures de Lucien non raccordé.
