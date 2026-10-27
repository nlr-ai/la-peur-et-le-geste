# Agents du plateau — livraison du 11 septembre 2026

Le [design](design-agents-plateau-lumina.md) et son [TODO](todo-agents-plateau-lumina.md) sont réalisés pour le travail documentaire et logiciel : décision réelle, déplacement partagé, commandes contrôlées, objets versionnés, vérifications et constats persistants.

## Deux missions réelles terminées

| Habitant | Cible | Résultat observé |
| --- | --- | --- |
| Quantum | 40002 | Deux contrôles exécutés : forme 9/9, viz 5/5. Constat et conclusion enregistrés ; prototypes conservés sans patch. |
| Gaia | 50000 | Création et relecture de son HTML documentaire, puis constat et conclusion. Deux tableaux rendus dans le navigateur sans erreur JavaScript. |

Missions : `6d2413d4-a385-48c9-80d2-f3b10e01c659` et `316e1e48-e4fc-4023-876c-64e8307186eb`. Les décisions proviennent des sessions des habitants via `depecher.py --mode plateau`, avec outils natifs désactivés ; le serveur exécute les commandes structurées.

Objet Gaia : `objet-viz-871f3844-dde6-482b-a67a-655f4a2454b8`, version `b9269b0199e70080d33934d957dc1017b3fece12397ffc5e3ab121a80a0a71d4`. Statut : brouillon non vérifié. Sa lecture et son rendu ne prouvent pas les faits rapportés par ses sources.

## Vérification et usage

102 tests Node et 28 tests Python passés. Positions identiques dans deux onglets, ouverture des objets dans un iframe isolé, sélection Gaia/50000 vérifiées. Les tests des billets utilisent des doubles de transport ; aucune correspondance réelle envoyée. La reconstruction de carte est testée sur un registre temporaire.

Sur la [carte locale](http://localhost:3140/?scenario=lumina-prime-30101#agent-gaia), choisir l'habitant et l'état cible, puis lancer. Le panneau expose suspension, reprise, annulation, étapes et conclusion. Les billets exigent la capacité explicite de la mission. Les tâches continuent tant que le serveur tourne, même sans navigateur.

Les traces, prompts et preuves se trouvent dans `.agents-runtime/plateaux/`; les états et événements dans `lumina-prime.sqlite3`. Captures : `preuves/objet-gaia.png`, `preuves/objet-viz-isole.png` et `preuves/plateau-travail.png`.

## Limites conservées

Aucune mesure des capacités de la cité, aucune clôture de verrou, aucune mutation des livres canoniques. Quantum a relevé des écarts dans les prototypes : méthode et limite manquantes, distinction consommation/prix insuffisante et calendrier à préciser. Ces corrections métier restent une prochaine mission ; elles ne sont pas masquées par les contrôles techniques réussis.
