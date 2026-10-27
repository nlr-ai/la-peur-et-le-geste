# Relais entre scènes de joueurs

Activation par monde : `python scripts/scenes.py activer` avec les variables
`CONSEIL_MONDE` ou `CONSEIL_RACINE` habituelles. Les données techniques vivent
dans `.agents-runtime/scenes/`, jamais dans les tables de fiction.

Chaque siège garde une session MJ stable, isolée par monde. Les appels des
scènes privées travaillent en parallèle, sans verrou global de tour. Le flux
conserve sa sérialisation courte lors de chaque écriture.

Avant une rencontre, le MJ initiateur envoie un dossier à l'autre scène :

```powershell
python scripts/scenes.py proposer --de aurore --a nicolas --dossier relais.json
```

Le dossier exige `faits`, `actions_en_attente`, `savoirs_par_joueur` et
`contraintes`. La proposition enregistre les salles et les horloges actuelles.
Les connaissances privées restent séparées : le relais informe les MJ, pas
les personnages. Lire les actions non résolues dans les inbox des deux sièges.

La commande réveille la scène destinataire et lui livre le relais dans son
brief ; son résultat est conservé dans le log du relais. `--sans-reveil`
permet le dépôt seul. Le destinataire répond lui-même :

```powershell
python scripts/scenes.py repondre --de nicolas --id IDENTIFIANT --message "Préparation nécessaire : ..."
python scripts/scenes.py repondre --de nicolas --id IDENTIFIANT --pret --message "Prêt : ..."
```

Une réponse prête ne fusionne que si les sièges occupés ont la même salle et
exactement la même heure. Aucun rattrapage automatique : jouer l'attente ou le
trajet autorisé, puis accuser réception. L'initiateur devient responsable ;
les appels des deux joueurs reprennent sa session. L'autre session reste
suspendue. **La team se suit par défaut** : tout déplacement entraîne les
deux PJ, garde le responsable et avance leur horloge commune. Une salle
nouvelle ne demande aucun nouveau relais. Les pensées et les apartés restent
privés ; suivre ne signifie pas parler ou décider à la place du partenaire.
Les explications hors narration, corrections et informations communes de
régie sont envoyées aux deux joueurs, même si un seul a posé la question.
Une séparation exige un choix explicite d'un PJ ou un empêchement établi.
Pour quitter la scène commune : `python scripts/scenes.py separer
--id IDENTIFIANT --raison "Choix explicite ou empêchement constaté"`.

### Passation à la séparation

Le MJ duo annonce d'abord la séparation aux deux joueurs. La commande prépare
un dossier distinct par PJ : position et heure canoniques, faits du flux que
ce PJ a reçus depuis la fusion, ses savoirs initiaux, ses volontés suivies,
les actions encore dans son inbox et les contraintes de reprise. Ces copies
sont des sources déjà affichées, pas des événements à rejouer. Les secrets
et l'inbox de l'autre joueur ne sont pas recopiés dans son dossier.

Le MJ duo peut ajouter un bilan écrit avec `--dossier separation.json`, un
objet dont les seules clés sont les IDs des membres et dont chaque valeur
est le bilan destiné à ce membre : faits vécus, connaissances, buts, actions
non résolues, engagements et contraintes. Les sources canoniques sont ajoutées
automatiquement. Aucun fait ni temps de fiction n'est écrit par la passation.

Les deux sessions privées sont réveillées automatiquement et reçoivent leur
propre dossier dans `passations_privees` (entier tant qu'il est `envoyee` ou
`a_completer` ; une fois reçu, il n'y reste qu'en trace, sans dossier). Chacune
accuse réception :

```powershell
python scripts/scenes.py recevoir --de aurore --id ID_PASSATION --pret --message "Dossier et actions en attente lus"
```

La plume bloque la reprise narrative d'un PJ tant que sa passation n'est pas
reçue. L'accusé d'un MJ ne vaut pas pour l'autre. Le réveil technique ne publie
pas de scène, ne consomme pas les actions et ne compte pas comme un tour sans
progrès des volontés. `--sans-reveil` permet seulement le dépôt et reporte la
réception au prochain réveil privé. Répéter un accusé reçu est idempotent.

S'il manque une pièce, le destinataire répond sans `--pret`, avec la pièce
manquante dans `--message`. Le MJ émetteur est réveillé pour compléter le
bilan par `scripts/scenes.py completer --de <émetteur> --id ID_PASSATION
--dossier bilan.json`. Le destinataire est alors réveillé à nouveau pour lire
et accuser réception. Une nouvelle fusion attend les passations privées.

Le serveur adresse les paroles à la scène fusionnée seulement. La plume refuse
une audience commune sans accord ou désynchronisée. Les réponses de PNJ à une
parole publique portant une `ref` sont visibles aux membres de la scène si le
PNJ est dans cette salle ; une réponse à une question privée reste privée.
Les réponses déjà reçues avant fusion ne sont pas redistribuées.

`python scripts/scenes.py etat` affiche propositions, réponses et scènes.
Les autres mondes gardent le comportement historique tant qu'ils n'activent
pas ce protocole.
