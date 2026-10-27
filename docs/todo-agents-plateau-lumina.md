# TODO — Agents actifs sur le plateau

Implémentation du [design](design-agents-plateau-lumina.md), demandée par « todo et go ».

- [x] Registre persistant, carte stable, commandes idempotentes et événements.
- [x] Déplacements partagés, réservations et reprise (trajet réel testé jusqu'à code).
- [x] API et panneau de travail avec historique ; deux onglets vérifiés.
- [x] Objets versionnés, lectures, modifications et constats ; versions périmées refusées.
- [x] Vérifications bornées sur les versions candidates : contrôles de forme et vraie viz dans Chromium sandboxé.
- [x] Mode de décision de l'habitant, contexte et prompts existants : six réponses réelles, outils natifs vides dans chaque trace.
- [x] Admission, budgets, attente, suspension et annulation : garde commune avec les journées et reprise bornée de l'admission.
- [x] Première boucle réelle de Quantum sur 40002 : mission terminée, deux contrôles et un constat.
- [x] Tests des contrats, readback HTTP et parcours dans le navigateur ; la viz versionnée s'ouvre dans son iframe isolé.

Les cases ne seront cochées qu'après vérification. La marche du plateau ne modifie pas la présence dans la ville ; aucune mesure ni clôture d'affaire ne sera déduite d'un test de logiciel.

## Vérifications déjà exécutées

- `node --test` : 102 tests passés, dont pause, reprise, collision, création, reconstruction et autorisation des billets.
- Tests Python admission, runtime, conservation des canaux et parloir MJ unique : 28 tests passés.
- Contrôle navigateur : mêmes positions dans deux onglets, aucune erreur JavaScript.
- Contrôles des objets initiaux : neuf assertions de forme et cinq assertions de viz, dont export téléchargé puis relu.

## Adaptations d'implémentation

- La grille a des coûts uniformes : parcours en largeur pour un chemin minimal, sans heuristique supplémentaire.
- Un snapshot transactionnel SQLite porte les projections techniques ; commandes et événements ont leurs tables propres. Pas de duplication des livres canoniques.
- Les décisions du plateau passent par Claude avec la liste d'outils vide et sans MCP/skills/settings. Le fournisseur global reste inchangé.
- Le code candidat est évalué dans le renderer sandboxé d'Edge, jamais dans Node ; les réponses réseau sont fournies uniquement depuis le manifeste de versions. La viz est éprouvée dans ce même navigateur.

## Résultat du pilote

Mission `6d2413d4-a385-48c9-80d2-f3b10e01c659`, terminée. Six décisions modèle réussies ; une première tentative technique a échoué sur un nom de fichier Windows, puis a été corrigée. 137 événements conservés. Quantum a choisi de vérifier les versions existantes sans les modifier : forme 9/9, viz 5/5. Son constat et sa conclusion sont consultables sur la carte. Les capacités de la cité et les verrous restent inchangés.

## Généralisation livrée

- [x] Créer de nouveaux objets versionnés, limités à la cible de mission. Gaia a produit et relu un brouillon réel pour 50000.
- [x] Ajouter les billets par le parloir avec référence durable, contrôle de capacité et relecture du dépôt. Tests simulés ; aucun billet réel envoyé par ces missions.
- [x] Reconstruire explicitement la disposition, en refusant une reconstruction pendant le travail. Route `POST /api/plateau/lumina-prime/map/rebuild`, testée sur registre temporaire.
- [x] Choisir habitant et état cible dans le panneau. Sélection Gaia/50000 et ouverture de son objet vérifiées dans Edge sans erreur JavaScript.

Mission Gaia `316e1e48-e4fc-4023-876c-64e8307186eb` terminée en six décisions. Son HTML présente deux tableaux : faits documentés (dont une convention) et inconnues. Affichage inspecté ; statut conservé « brouillon non vérifié ». Le rendu ne valide pas les affirmations des sources.

## Capacités volontairement absentes

Les mutations des livres, les clôtures de verrous et les instruments de mesure physiques ne sont pas exposés. Ils nécessitent leurs propres portes et contrôles avant extension. Le plateau ne transforme pas une réussite logicielle en changement canonique.
