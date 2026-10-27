# Instructions locales au réveil

Le moteur compose le prompt à chaque appel, pour tous les fournisseurs.

## MJ

1. `mondes/<id>/prompts/mj.md`, si présent, reste la constitution explicite.
2. Sans ce fichier, un paquet distinct du dépôt avec `manuel.md` reçoit le socle neutre `scripts/agents/prompts/mj-socle.md`. La disposition héritée et les paquets sans manuel gardent leur repli historique sur `CLAUDE.md`.
3. Le spectacle est le fichier local `prompts/mj-spectacle.md` ou le spectacle commun.
4. `AGENTS.md` et `manuel.md` locaux sont incorporés après ces blocs. Ils priment sur les exemples de décor ; le MJ reçoit leur contenu, pas seulement un chemin à lire.
5. Les règles de partie et de mode ainsi que le cahier personnel restent composés comme avant.

## PNJ

Le métier commun, puis `prompts/pnj.md` facultatif, puis les instructions locales `AGENTS.md`. Le manuel de MJ et le canon ne sont pas injectés dans le PNJ. Le cahier personnel reste à sa place. Une instruction technique n'est pas une croyance du personnage.

## Créer un monde

Écrire `manuel.md` et `AGENTS.md` dans son paquet suffit pour le branchement MJ. Ajouter `prompts/pnj.md` pour adapter l'incarnation. Les règles locales doivent préciser les conventions de départ, les points de vue, les éléments encore inconnus et les exemples du socle à écarter. Ne pas recopier toute la doctrine commune.

Les changements sont relus au prochain appel ; une session déjà en cours n'est pas interrompue. Ce contrat ne prouve pas à lui seul qu'un fournisseur suit ses consignes, ni que toutes les commandes résolvent correctement les chemins d'état.
