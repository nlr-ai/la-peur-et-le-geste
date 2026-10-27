# Suivre les volontés des joueurs

Le MJ garde les buts explicitement déclarés, sans inventer leurs préférences.
Le suivi est technique sous `.agents-runtime/mj/volontes-pj.json` ; la source
est une vraie ligne `vous` avec son joueur et sa `ref`. Ce n'est ni une pensée
ajoutée au PJ ni une nouvelle autorité sur les faits du monde.

```powershell
python scripts/volontes_pj.py poser --joueur aurore --ref REF --objectif "Rejoindre Inverness"
python scripts/volontes_pj.py actualiser --id REF --statut active --preuve "Un repère utilisable a été obtenu" --ref REF_REPONSE
python scripts/volontes_pj.py actualiser --id REF --statut bloquee --preuve "La route distante manque dans la préparation"
```

Ce qu'un PJ dit de lui-même et qui doit survivre à la compaction de la
session du MJ — l'identité qu'il se donne, qui il va rejoindre, l'histoire
qu'il raconte — s'enregistre comme déclaration, toujours citée par `--ref` :

```powershell
python scripts/volontes_pj.py declarer --joueur aurore --ref REF --resume "Se dit nièce d'un oncle et d'une tante à Inverness, qu'elle va rejoindre"
```

Les déclarations ne s'atteignent ni ne s'abandonnent : elles reviennent à
chaque réveil, avec les objectifs en cours de `etat/joueurs/<pj>/objectifs.json`.

Statuts : `active`, `bloquee`, `attente_joueur`, `atteinte`, `abandonnee`.
Abandonner exige une nouvelle parole ou action de ce joueur, citée par `--ref`.
Une progression exige un constat concret : distance parcourue, information
utilisable, obstacle résolu, décision éclairée devenue possible. Répéter un
décor ou constater une attente ne remet pas le compteur à zéro.

Chaque réveil MJ reçoit les volontés des joueurs de sa scène. Au deuxième
tour sans progression, elles sont signalées dans `a_debloquer`. Le MJ traite
alors la cause : consulter/établir un fait manquant, dépêcher un PNJ pertinent,
réparer le transport d'une réponse, montrer un obstacle ou faire parvenir une
information que le personnage devrait déjà avoir. Il consigne ce qui a changé.

Un vrai choix du joueur se joue : `attente_joueur` explique quelle bifurcation
nécessite sa décision et ne déclenche pas un contournement de son choix.
Un danger ou une opposition légitime reste un obstacle. La stagnation appelle
une initiative du monde, jamais une réussite automatique ni un ordre inventé.
Dans un duo, le MJ suit les deux volontés, les compatibles comme les divergentes.
Les corrections et explications communes sont adressées aux deux joueurs.

Ce contrôle se fait aux réveils du MJ ; il n'ajoute pas une minuterie réelle
ni une boucle de réveils pendant que les joueurs sont absents.
