# Dix minutes
Monde de conversation, en français. Lire manuel.md. Aucun décor féodal, aucune carte, aucune table de guerre, aucune main. Ne modifier aucun autre monde.

Neuf sièges occupés, pilotés par `scripts/joueur_pnj.py`, et un seul MJ, le maître de maison. Les invités ne se dépêchent pas comme des PNJ ordinaires : leurs paroles viennent de leurs propres sessions (Règle Zéro). Deux invités assis à la même table s'entendent directement : la parole de l'un est servie à l'autre par la présence de la pièce, et le MJ n'est pas un relais.

Sélectionner `CONSEIL_MONDE=dix-minutes` avant toute commande. Respecter docs/schema.md ; les rondes, les paires et les carnets vivent dans `salon/registre.md`, pas dans de nouveaux champs d'état.

Les salles : `vestibule` (lieu commun), `table-1` à `table-4` (les conversations), `alcove-<id>` (l’alcôve privée de chaque invité, pour son carnet ; neuf). Placer, sonner et compter passent par `outils/tables.py`, qui n'écrit au flux que par `scripts/append_flux.py`.

Ce qu'un invité ignore : tout ce qui suit son instant, la raison de sa présence, et qui tient la maison. Ne jamais le lui révéler par la voix du MJ. Ce qu'il apprend, il l'apprend de la bouche d'un autre invité, avec les erreurs de celui-ci.
