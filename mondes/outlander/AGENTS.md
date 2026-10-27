# Outlander — instructions locales

Lire `manuel.md`, `canon/depart.md` et `canon/sources.md` avant toute préparation ou mise en jeu.

Ce paquet est indépendant de Westeros. Les noms, institutions, dragons, corbeaux et rites du décor House of the Dragon ne s'y appliquent pas. La doctrine commune du dépôt demeure applicable : Règle Zéro, autonomie des PNJ, brouillard, discipline des écritures et boucles de simulation.

Exception explicitement demandée par le joueur : un PNJ peut consulter le MJ
sur les faits du monde qu'il ne peut établir lui-même, via
`scripts/parloir.py --question-monde --de <id> --a mj "question"`.
Cette consultation est hors fiction et prime sur l'interdit commun PNJ→MJ.
Elle n'autorise ni demande de permission d'agir, ni transfert de décision au
MJ, ni accès aux secrets. Voir le prompt PNJ local et `docs/questions-monde.md`.

- Toujours sélectionner explicitement ce monde avant une opération d'état ou un réveil : `CONSEIL_MONDE=outlander` ; serveur avec `--monde outlander`.
- Aucune parole ou action nouvelle de PNJ ne s'écrit de la main du préparateur : utiliser `scripts/depecher.py` dans le monde sélectionné. Les notices canoniques ne sont pas des scènes jouées.
- Aurore et Nicolas sont deux PJ. Ne pas inventer leurs âges, métiers, lien, pensées, décisions, compétences, bagages ou connaissance d'Outlander.
- Claire traverse elle aussi. Les PJ ne la remplacent pas et ne prennent pas automatiquement sa trajectoire.
- Séparer canon sourcé, faits historiques, décisions du joueur, hypothèses de préparation et faits effectivement joués.
- Ne pas créer de rencontre, de captivité, de blessure ou de trajet obligatoire pour rejoindre l'intrigue canonique.
- Ne jamais modifier `docs/schema.md`. Employer les structures du moteur existant ; ne pas inventer de champs pour combler une donnée manquante.

L'état initial et les introductions privées existent. Lire `canon/implantation.md` pour les conventions du départ et les limites actuelles.

## Une narration riche — suivre les fils, peupler le monde

**Le but :** que les joueurs vivent une histoire riche, dans un monde qui
semble exister au-delà de ce qu'ils regardent. Un monde habité, qui a de la
mémoire, où ce qui a été semé revient, et où chaque pas ouvre plus de
possibles qu'il n'en ferme. C'est la mesure de toute décision d'écriture,
et elle l'emporte sur une lecture prudente des consignes qui laisserait le
monde vide ou les réponses maigres.

Les moyens sont libres. Suivre les fils que le jeu a ouverts, inventer ce qui
manque — lieux, coutumes, gens —, laisser les habitants avoir leurs propres
vies : autant d'inspirations, pas une liste à cocher. Ce qu'on invente devient
vrai et se garde dans l'état.

Ce qui ne bouge pas : la Règle Zéro (on peut faire naître quelqu'un, on ne
parle pas à sa place), le canon et l'état acquis, et la liberté des PJ — on
enrichit leurs possibles, on ne choisit pas pour eux.

## Affaires et worldpainting

Le format est dans `format-affaires.md`, les modèles sous `modeles/`. Chaque PNJ portant une stratégie tient une affaire personnelle et un registre d’états de choses sous sa chambre. Le MJ crée la forme, l’incarnation du PNJ remplit ses fins et moyens. Préparer l’implantation autorise les ajouts plausibles non contradictoires, avec statut et provenance, sans jouer d’événement futur. Ce droit ne s’étend pas aux profils ou décisions des PJ. Ne pas confondre trous de préparation et trous calculés du graphe.
