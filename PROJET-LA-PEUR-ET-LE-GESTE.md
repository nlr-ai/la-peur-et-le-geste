# La peur et le geste

Dépôt indépendant créé le 22 octobre 2026 à partir de l’état de travail de `C:\Users\reyno\le-conseil2`, avec son historique Git et ses modifications locales.

## Projet

Construire ici « La peur et le geste », en reprenant les lieux, les personnages et la simulation existants de `C:\Users\reyno\Modern Front`.

Le travail de ce projet doit se faire dans `C:\Users\reyno\la-peur-et-le-geste`. Les deux dépôts sources sont des références à lire, pas des cibles de modification.

## État initial

La copie contient encore les mondes et les données de Le Conseil. Les sources des trois premières réunions politiques et leurs dossiers de préparation sont copiés sous `sources/modern-front/`. Les sept fiches sont accessibles dans [le répertoire des personnages](personnages/README.md). Les fiches sont maintenant raccordées aux tables du monde, aux chambres et au prompt du MJ. Le moteur externe de simulation Modern Front reste à raccorder.

Les dossiers `.agents-runtime`, `.git` imbriqués, `node_modules`, `__pycache__` et `.pytest_cache` ont été exclus de la copie des fichiers. Le dépôt racine possède son propre `.git`, cloné sans liens physiques, sur la branche `codex/la-peur-et-le-geste`, sans dépôt distant.

Avant de lancer un serveur dans cette copie, prévoir un port propre et vérifier les chemins absolus de sa configuration. Aucun serveur ni agent n’a été lancé lors de la copie.

## Lieux canoniques et vue château

Les dix lieux retenus sont maintenant inscrits sous `mondes/la-peur-et-le-geste/etat/lieux.json`. Les 60 pièces des plans et leurs passages intérieurs sont définis. Leur provenance est conservée dans `provenance-lieux.json` ; les intérieurs sont des créations de fiction.

Ouvrir `http://localhost:3217/plans/lieux.html` après lancement avec `node serveur/serveur.js 3217 --monde la-peur-et-le-geste`. La vue lit les plans du monde par `/monde.json`, comme le jeu. Cette création ne place aucun personnage. Un autre travail a depuis initialisé Raymond Moreau et un début de partie en juin 1940 ; consulter les tables courantes du monde. Le raccordement de la simulation Modern Front n’est pas réalisé par ce chantier.

## Intégration jouable

Le site du monde est disponible sur http://localhost:3217/ : neuf personnages (les sept participants documentés, Michel et son petit frère fictif Lucien), avec Raymond comme personnage joueur. La scène reprend chez les Moreau à la fin de la troisième réunion, le 18 juin 1940 ; 21 h est une convention technique. Les dix lieux importés sont conservés. Le MJ incarne directement les PNJ, avec leurs fiches dans son contexte.

Vérification : scène visible dans le navigateur et 11 tests du routeur réussis. Aucun tour de dialogue du MJ lancé pour ce contrôle. L’audit hérité signale encore l’absence de signal de présence du joueur, des routines et des rapporteurs de gestion non initialisés ; cela ne constitue pas une simulation autonome validée.
