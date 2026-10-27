# La refonte — le plan, et son épreuve : Venise dans Venise

Écrit le 9 septembre 2026, après la relecture consignée dans
[`refonte-points-forts.md`](refonte-points-forts.md). Ce document dit **dans
quel ordre on démonte**, et **à quoi on saura que c'est fait**.

Les quarante invariants à emporter sont dans l'autre document et ne sont pas
répétés ici. Celui-ci ne parle que du chantier.

---

## 1. L'épreuve

Une refonte qui se juge sur une intention se juge sur rien. L'épreuve est
celle-ci, et elle est binaire :

> **Venise et Westeros vivent dans deux paquets séparés, servis par le même
> moteur, et l'on passe de l'un à l'autre par un menu. Aucun des deux ne peut
> nommer l'autre. Le moteur ne peut nommer ni l'un ni l'autre.**

Elle a été choisie parce qu'elle n'est pas hypothétique : les deux mondes sont
**déjà** dans le dépôt, fondus l'un dans l'autre sans que rien ne le déclare.
Elle a donc la propriété qu'on demande à une épreuve : elle échoue aujourd'hui,
pour des raisons qu'on peut compter.

### Les assertions à tenir

Chacune est vérifiable par une commande, sans jugement.

| # | Assertion | Comment on la vérifie |
|---|---|---|
| E1 | Deux paquets existent, chacun complet | `mondes/venise/` et `mondes/westeros/` portent chacun `etat/`, `chambres/`, `manifeste.json`, `manuel.md` |
| E2 | Westeros ne connaît pas Venise | `grep -ril "braavos\|serenissima\|ducat" mondes/westeros/` rend zéro |
| E3 | Venise ne connaît pas Westeros | `grep -ril "peyredragon\|targaryen\|rhaenyra\|dragon" mondes/venise/` rend zéro |
| E4 | Le moteur ne connaît aucun des deux | même grep, les deux vocabulaires, sur `scripts/` hors `scripts/mondes/`, `serveur/`, `ecrans/` : zéro |
| E5 | Chaque monde tient ses gardes seul | `CONSEIL_MONDE=venise python scripts/tick.py --verifier` sort 0, et de même pour `westeros` |
| E6 | Les horloges sont séparées | Venise n'est pas au 12e jour de la 5e lune de l'an 129 ; changer l'heure d'un monde ne bouge pas l'autre |
| E7 | Le menu bascule | `/moi` liste les deux mondes ; `/bascule-monde?vers=venise` sert Venise, avec ses lieux, ses visages, ses livres |
| E8 | Un homme dépêché reste chez lui | une journée d'homme lancée à Venise n'écrit aucun octet sous `mondes/westeros/` |
| E9 | Les sessions ne se croisent pas | deux personnages homonymes dans les deux mondes ont deux identifiants de session distincts |
| E10 | Le fil est propre | le flux de Venise ne contient aucun item de Westeros, et réciproquement |
| E11 | Le moteur passe ses tests sans monde | la suite de tests tourne sur un monde d'épreuve minuscule, ni Venise ni Westeros |
| E12 | Un troisième monde coûte un dossier | ajouter un monde vide et le voir au menu ne demande aucune modification de `scripts/`, `serveur/`, `ecrans/` |

**E12 est l'assertion décisive.** Les onze autres peuvent être obtenues en
déplaçant des fichiers. Seule la douzième prouve qu'on a construit une
mécanique et non rangé un placard.

---

## 2. Ce que l'épreuve révèle aujourd'hui

Mesuré le 9 septembre sur l'arbre de travail. Venise n'est pas « un peu »
présente : elle est majoritaire dans trois tables sur cinq.

| Ce qui est partagé | Part de Venise |
|---|---|
| `etat/personnages.json` | 154 fiches sur 280 |
| `chambres/` | 76 dossiers sur 313 |
| `etat/chemins.json`, les arêtes | 49 sur 193 |
| `etat/lieux.json` | `braavos` y est un lieu comme `peyredragon` |
| `etat/maisons.json` | `maison-serenissima` y est une maison, avec 26 volumes |
| `etat/flux.jsonl` | 140 items sur 12 720 |
| Fichiers Python nommant Venise | 27 |
| Fichiers d'écran ou de serveur la nommant | 10 |

Et le fait qui décide de tout le reste :

> **Un siège joueur vit déjà à Braavos** (`nicolas-lester-reynolds`, `lieu:
> "braavos"` dans `joueurs.json`), et son horloge est dans le même fichier que
> celle de Rhaenyra, calée sur le 12e jour de la 5e lune de l'an 129.

Venise tourne à l'heure des Targaryen. Ce n'est pas un défaut cosmétique : le
temps est la seule chose que le moteur possède en propre, et il est
aujourd'hui indexé par siège au lieu de l'être par monde. Tant que c'est le
cas, deux mondes ne peuvent pas exister, seulement deux décors dans un monde.

**Le point encourageant, et il est réel** : `chemins.json` fait déjà la
séparation qui compte. Braavos y est une composante connexe distincte, et la
règle « composante d'abord, durée ensuite » du quartier interdit déjà à un
homme de Venise d'être « à vingt minutes » de la Table Peinte. La topologie a
donc déjà la notion de monde, sous un autre nom. Le plan consiste largement à
remonter cette notion jusqu'en haut.

---

## 3. Le concept qui manque

> **Un monde est un paquet.** Le moteur n'en connaît aucun ; il en reçoit un.

Un paquet contient, et rien d'autre ne le contient :

```
mondes/<id>/
  manifeste.json      identité, calendrier, monnaie, titres, genres d'unités,
                      canaux de transmission, lieu de départ, siège par défaut
  etat/               monde, personnages, lieux, chemins, maisons, relations,
                      intentions, evenements, actes, paroles, info, annales,
                      flux.jsonl, joueurs, horloges, joueurs/<siege>/
  chambres/           une par habitant
  livres/             les volumes, par maison
  plans/              les plans de salles, la géométrie locale
  blasons/            les armes
  carte/              les cadrages, les bannières, la table peinte
  habillage/          le visage de la partie : habillage.css (chargée après
                      jeu.css), habillage.json (onglet, bandeau, logo), images
                      — facultatif, voir serveur/routes/habillage.js
  manuel.md           ce que le meneur doit savoir de CE monde
  voix.json           les timbres
```

Ce que le manifeste doit porter, parce que c'est exactement ce qui est en dur
dans le code aujourd'hui :

| Clef | Ce qu'elle remplace |
|---|---|
| `calendrier` | 12 lunes × 30 jours, gravé dans le schéma |
| `monnaie` | le tuple `("dragon","cerf","sol")` de `chiffrer.py` |
| `titres` | l'expression régulière `(ser|dame|lord|mestre…)` de `criticite/hommes.py` |
| `unites` | le dragon comme type de jeton, sa famille de filtre, son verbe, son canal |
| `canaux` | corbeau, cavalier, rumeur, et leurs vitesses |
| `offices` | les mots-clés d'attribution de `taches.js` et `reparer_renvois.py` |
| `signes` | la table d'emojis de `partie_signes.py` |
| `depart` | le lieu et le siège d'ouverture |

**Le moteur ne lit jamais une valeur de cette table en dur.** C'est la règle
qui rend E4 vérifiable mécaniquement, et E12 possible.

---

## 4. Les sept lots

Chaque lot dit ce qu'il change, ce qu'il prouve, et ce qu'il débloque. Ils
sont ordonnés : chacun suppose le précédent.

### Lot 0 — Le ménage, et le filet

Rien de structurant, mais rien ne se démonte proprement dans un dépôt qui
porte ses brouillons.

- Sortir les ~170 fichiers de travail de la racine, les instantanés manuels
  d'`etat/`, les cinq correctifs à usage unique, le dossier de transit d'août.
- Réparer `metier.md` : il est dupliqué mot pour mot, et se termine par un bloc
  étranger injecté dans chaque PNJ.
- Faire d'`AGENTS.md` un pointeur vers `CLAUDE.md` au lieu d'une copie.
- Supprimer le code mort nommé dans la relecture, et la branche de fournisseur
  inachevée.
- **Mettre dans `verifier.mjs` les deux tests serveur qui gardent le brouillard
  et la marche.** Ils existent, ils sont vérifiés par mutation, et ils ne
  tournent pas.
- Écrire les tests qui manquent là où le risque est : le calcul de fenêtre du
  tick, et les gardes qui verrouillent chaque écriture d'état.

**Prouvé par** : la suite verte, et une racine lisible.
**Débloque** : tout le reste. On ne déplace pas 189 Mo d'état sans filet.

### Lot 1 — Une racine, deux langues, une porte

Le lot dur, et le plus mécanique.

- `tables.py` lit la racine depuis l'environnement au lieu de son propre
  chemin de fichier. Une ligne.
- Migrer les 80 fichiers Python qui collent `etat` en dur sur une racine
  calculée. Un par commit, en commençant par ce qui écrit la mémoire du jeu.
- Supprimer le préambule de chemin recopié dans ~110 fichiers, au profit de
  la déclaration de paquets qui existe déjà mais ne sert pas.
- Côté serveur, faire passer les ~48 lectures de fichier recopiées dans les
  routes par la porte de `contexte.js`, et **résoudre la racine par requête**
  et non au chargement du module.
- `chambres/` et le dossier d'exécution suivent la même racine.

**Prouvé par** : E5 sur un monde d'épreuve minuscule, et la suite de tests qui
tourne sans jamais toucher le monde réel.
**Débloque** : E1, E8, E11.

### Lot 2 — Venise sort

Le déménagement proprement dit, une fois qu'il y a où déménager.

- Créer les deux paquets, et un troisième minuscule pour les tests.
- Répartir les tables partagées. C'est un travail de données, pas de code :
  154 fiches, 76 chambres, 49 arêtes, une maison, 140 items de flux.
- **Le siège à cheval — tranché le 9.9, et dans les deux sens.** Nicolas devient
  un siège de Venise et sort du roster de Westeros, **et** la traversée devient
  une chose écrite : [`traversee.md`](traversee.md). Ce n'est pas un compromis,
  c'est l'ordre — on ne peut traverser que si l'on a un chez-soi d'où partir, et
  un personnage sans monde natal n'est pas un voyageur mais une incohérence.
  Ce que le lot 2 en retient tient en deux champs : `monde_natal` sur le siège,
  et **une amarre** — une seule correspondance datée entre les deux calendriers,
  d'où tout le reste se calcule. La visite et ses gardes viennent après.
  La contrainte que la note impose au lot 2, et la seule : **ne pas supposer
  qu'une fiche appartient à exactement un monde.**
- Les horloges deviennent par monde, puis par siège dans le monde. Venise se
  donne son propre calendrier dans son manifeste, et cesse d'être en 129 AC.
- Les importateurs de citoyens, les scripts de regroupement et de liaison
  descendent dans `scripts/mondes/venise/`, hors du moteur.

**Prouvé par** : E2, E3, E6, E10.
**Débloque** : le menu a enfin deux choses à proposer.

### Lot 3 — Les données sortent du code

Le verrou de l'écran, mesuré à quatre endroits.

- Les plans de salles quittent le JavaScript pour le paquet du monde. C'est le
  fichier où Braavos est fabriqué par un remplacement de texte sur
  Peyredragon ; il disparaît avec le lot.
- Le registre des lieux 3D, les cadrages nommés de la table peinte et la table
  de blasons deviennent des données servies.
- Le serveur sert la géométrie, l'héraldique et les cadrages du monde courant,
  et n'en connaît aucun.

**Prouvé par** : E4 sur `ecrans/` et `serveur/`, et E7 pour de vrai : le menu
change les visages, les plans et les bannières, pas seulement les noms.

### Lot 4 — Le vocabulaire de règles vient du monde

Le seul lot qui touche la sémantique, et le seul qui demande de réfléchir.

- Le dragon cesse d'être un type d'unité écrit dans le moteur. Il devient une
  entrée `unites` du manifeste, avec son glyphe, sa famille de filtre, son
  verbe et son canal. Une gondole vénitienne s'y déclare de la même façon.
- La monnaie, les titres, les mots-clés d'office, la table d'emojis de la
  partie suivent le même chemin.
- Le moteur gagne une notion qu'il n'a pas : **un genre d'unité**, avec ce
  qu'on peut en dire et ce qu'on peut en faire.

**Prouvé par** : E4 sur `scripts/`, et une partie jouée à Venise dont les
pièces parlent de ducats et de galères sans qu'une ligne de moteur ait bougé.

### Lot 5 — La doctrine et le décor se séparent

Sans ce lot, le menu change le monde et le meneur continue de se croire à
Peyredragon.

- La constitution est courte, stable, générique : les trois boucles, la Règle
  Zéro, l'autonomie, le brouillard, la montre, l'interdiction des menus.
- Les exemples, les noms, les manières, les usages de cour descendent dans le
  `manuel.md` du monde.
- Le manuel du meneur s'assemble : constitution, plus manuel du monde courant,
  plus les modules du moment. La conditionnalité qui existe déjà pour la
  partie devient la règle générale.
- Le manuel de l'homme dépêché est déjà presque générique ; il le devient
  entièrement.

**Prouvé par** : une scène jouée à Venise où personne ne dit « Votre Grâce »
sans qu'on l'ait demandé, et un prompt de meneur qui a maigri de moitié.

### Lot 6 — Le menu, et la vie des processus

Le lot visible, et le dernier, parce qu'il ne vaut rien sans les six autres.

- `/moi` liste les mondes ; `/bascule-monde?vers=` pose un cookie et
  redirige. C'est la copie exacte du menu des sièges, qui marche déjà.
- Les identifiants de session d'agents sont préfixés par le monde. Deux
  homonymes dans deux mondes cessent de partager une tête.
- Le plafond de sessions, la file d'appels et le journal d'exécution deviennent
  conscients du monde.
- **Basculer pendant qu'un homme travaille est refusé, avec le nom de qui
  travaille.** Ce n'est pas une limite technique, c'est la seule réponse
  honnête : une journée en cours appartient au monde où elle a commencé.

**Prouvé par** : E7, E9, E12.

---

## 5. L'ordre, et pourquoi

```
Lot 0  ménage et filet
  └─ Lot 1  une racine, une porte          ← le lot dur
       ├─ Lot 2  Venise sort                (données)
       │    └─ Lot 6  le menu               (visible)
       ├─ Lot 3  les données sortent du code
       └─ Lot 4  le vocabulaire vient du monde
            └─ Lot 5  doctrine contre décor
```

Trois raisons à cet ordre, et une seule compte vraiment.

- **Le lot 1 est un remaniement mécanique de plusieurs centaines de fichiers.**
  On ne le fait pas sans les tests du lot 0, et on ne le fait qu'une fois.
- **Les lots 3 et 4 sont indépendants du lot 2** et peuvent avancer en
  parallèle : l'un est de l'écran, l'autre du moteur.
- **Le lot 6 est en dernier**, contre l'envie. Un menu livré tôt donnerait
  deux décors dans un monde, avec une horloge commune et des sessions qui se
  marchent dessus. Ce serait pire que rien, parce que ça ressemblerait à une
  réussite.

**S'il faut voir le menu avant** : un processus de serveur par monde, chacun
avec sa racine, le menu se contentant de rediriger vers l'autre port. Cela
demande le lot 1 seul, ne bloque aucun lot suivant, et ne ment sur rien.

---

## 6. Ce qui reste commun, volontairement

Le but n'est pas de tout séparer. Ce qui suit est le moteur, et il n'a pas
d'univers :

- les trois boucles, la montre, le tick et ses gardes ;
- la présence calculée, le quartier, les creux ;
- les deux brouillards symétriques, et le pli comme objet ;
- le siège, le jeton, le tri par audience, le fil append-only ;
- la dépêche, le parloir, la chambre, le percept, le péage de la parole ;
- la criticité, les mains, les livres ;
- le plateau de la partie, ses coups et son greffe ;
- l'écran : le bus, le fil, la barre à sept modes, les échelles du décor.

**Un ajout à ce moteur qui nomme un monde est une régression**, et E4 le dit
sans discussion.

---

## 7. Les pièges nommés

Trouvés pendant la mesure. Chacun coûterait une journée s'il était découvert
en chemin.

1. **Le siège à cheval.** Tranché le 9.9 : il part à Venise, et la traversée
   s'écrit — [`traversee.md`](traversee.md). Le piège reste entier pour qui
   l'ignorerait : dupliquer une chambre dans deux paquets ne fabrique pas un
   voyageur, ça fabrique deux hommes du même nom qui divergent au premier
   réveil.
2. **L'horloge est indexée par siège, pas par monde — et c'est JUSTE.** C'était
   noté ici comme la racine du problème du temps ; la note de traversée montre
   que c'est l'inverse. Un homme vit des minutes, et il en vit autant où qu'il
   soit : ce qui change d'un monde à l'autre n'est pas la durée, c'est le NOM
   qu'on donne au jour. L'horloge par siège reste ; ce qui manque est l'amarre.
   Le vrai défaut est ailleurs, et il est plus bête : les quatre sièges se
   partagent un fichier, et Venise y est donc calée sur le calendrier des
   Targaryen.
3. **Les identifiants de session sont dérivés du nom et de la date.** Deux
   Marie dans deux mondes partagent une tête, en silence, sans erreur.
4. **La topologie fait déjà la moitié du travail.** Braavos est une composante
   connexe distincte. Ne pas refaire ce qui est fait ; s'en servir comme
   contrôle de cohérence pendant la répartition du lot 2.
5. **Le monde en 3D pèse 1,2 Go et se régénère.** Il ne descend pas dans le
   paquet : le paquet porte la recette et le témoin, pas la matière.
6. **La moitié des mentions de décor sont des commentaires.** Le grep de E2 à
   E4 doit les compter comme des échecs sur les données, et comme du bruit sur
   le code. Sinon on passe une semaine à réécrire des commentaires justes.
7. **`presence.json`, `pensees.json` et le flux sont relus en entier, souvent.**
   Séparer par monde les rend deux fois plus petits, ce qui masquera un moment
   le vrai problème de coût. Ne pas confondre les deux chantiers.

---

## 8. Où en est le chantier

Journal, tenu à mesure. Une ligne n'y entre que quand elle est **vérifiée**.

### 9 septembre 2026 — lot 0 fait, lot 1 posé

**Lot 0.**

- 101 fichiers retirés de la racine : 94 brouillons de poussée suivis par git,
  plus `NUL`, `err.txt`, `sec.txt`, `dec.txt`, `sur.txt`, `msg.json`,
  `prev.json` et `patch_gemini.py` (un correctif à usage unique déjà appliqué).
  Le `.gitignore` ferme les motifs, avec le raisonnement au-dessus des lignes.
- `metier.md` réparé : il faisait 108 lignes dont les 45 premières étaient
  l'exact doublon des suivantes, tronqué en pleine phrase. Il en fait 58. Le
  bloc final « Directive Évolutive / agent autotélique / tu es autorisé à
  chercher du pouvoir sur la simulation » est retiré — il était injecté dans le
  prompt système de **chaque** PNJ, dans un registre étranger à tout le reste
  du manuel.
- Le miroir des manuels est réparé. Il avait dérivé **avant** ce chantier :
  `scripts/noyau/AGENTS.md` avait perdu les cinq modules de partie ajoutés la
  semaine précédente, alors qu'un script et un test existent pour le tenir.
- **La route de vérification passe de cinq gardes à huit.** Les trois ajoutées
  existaient toutes, écrites et vertes, et ne tournaient pas :
  `serveur/test_siege.js` (le brouillard, vérifié par mutation),
  `serveur/test_marche.js` (les distances), et `scripts/tests/essai_occupation.py`
  — trente cas qu'aucun lanceur ne collectait, son nom ne commençant pas par
  `test_`.

**Lot 1.**

- `scripts/noyau/racines.py` et `serveur/racines.js` : deux implémentations, un
  seul contrat. `CONSEIL_RACINE`, puis `CONSEIL_MONDE`, puis la disposition
  héritée. Un monde nommé qui n'existe pas plante et ne sert jamais celui d'à
  côté.
- **La disposition héritée est le défaut, à l'octet près.** Sans variable, tout
  rend exactement ce qui était rendu avant. Le lot est donc additif : rien ne
  bouge tant que personne ne nomme un monde.
- `tables.py` et `serveur/contexte.js` passent par le résolveur. Les deux
  racines sont désormais **nommées séparément** : `DEPOT` (le code, immuable) et
  `RACINE`/`ETAT` (le monde). Le piège a failli se refermer deux fois pendant
  l'écriture — le `--verifier` des tables balaie les `*.py` suivis par git, et
  le serveur sert `ecrans/jeu.html`, tous deux depuis une variable nommée
  `RACINE` : pointer un monde y ferait chercher du code dans un dossier de
  données.
- `mondes/_epreuve/` existe : un monde de service, an 1, une salle, un témoin,
  sa propre monnaie. Caché du menu du joueur, jamais de la machine.
- `scripts/tests/test_racines.py` : dix épreuves, dont **l'accord des deux
  langues**, comparé sur les deux SORTIES et non sur les deux textes.
  **Vérifié par mutation** : casser le côté Node fait tomber deux épreuves avec
  le bon message ; restaurer les fait passer.
- Mesure neuve dans la route : **74 fichiers décident encore seuls où vit
  l'état.** Ce chiffre ne doit que descendre, un fichier par commit.

**Ce que le monde d'épreuve a trouvé le jour même.** Le serveur démarré dessus
servait Caraxès, Vhagar, Meleys et Syrax à un monde qui n'a ni Westeros ni
dragons : neuf entités étaient recopiées **en dur** dans une route, et
partaient donc avec n'importe quel monde. Elles vivent maintenant dans
`etat/dragons.json` — un fichier que `noyau/partie_cartes.py` lisait déjà, sans
qu'il existe, si bien que la partie rendait des ids nus là où elle voulait des
noms. Le monde d'épreuve n'a servi que ses deux entités, le monde réel ses 320.

**Deux serveurs, deux mondes, côte à côte, au même instant.** C'est la bascule
démontrée — pas encore le menu, qui est le lot 6.

**Ce qui reste rouge, et ne vient pas d'ici** : `chainage-actions` signale 13
références d'action vers des actes absents. C'était rouge avant ce chantier ;
ce sont des données de jeu, pas du code, et rien n'y a été touché.

### 9 septembre, seconde passe — la panne, et ce qu'elle a appris

Cinq chantiers ont été menés en parallèle. La session s'est interrompue pendant
qu'ils travaillaient : trois avaient posé du travail partiel, deux n'avaient
rien posé, et **le dépôt était cassé** — deux gardes vertes passées au rouge.

**La panne, parce qu'elle vaut une règle.** La migration avait remplacé

```
RACINE = os.path.dirname(...)   ;   ETAT = os.path.join(RACINE, "etat")
```

par `ETAT = racines.etat()` **seul**, en retirant `RACINE`. Quatre modules
frères importaient ce nom, à travers un import circulaire. Le symptôme n'a pas
été une erreur de nom à la ligne fautive, mais
`ImportError: cannot import name 'RACINE' from partially initialized module`
**à l'autre bout du cercle**, à trois fichiers de distance de la cause.

> **On ne supprime jamais un nom qu'un module exposait.** Un fichier qui
> définissait `RACINE` continue de la définir — `racines.DEPOT` — même quand
> plus rien ne semble la lire. Ce qui la lit peut être de l'autre côté d'un
> cycle, où la disparition ne se signale pas.

Quatre modules réparés (`temps/regence.py`, `lecture.py`, `disponibilite.py`,
`gardes/sieges.py`). Le dernier portait en prime un vrai défaut : il lisait le
fil par `RACINE + "etat"`, donc **le fil du monde d'à côté** dès qu'un monde
était nommé — et c'est la garde des audiences.

**Ce qui a été fini à la main :** `serveur/monde3d.js`, qui mélangeait trois
racines (quinze chemins vers les artefacts 3D et les sources Python, deux vers
l'état, un déjà juste) ; et la moitié écran du lot 4, laissée déclarée mais non
câblée — un `UNITES` lu nulle part, avec un grand commentaire décrivant un
dispositif qui n'existait pas. Un constant mort documenté se lit comme fini.

**Le manifeste du monde réel existe** (`manifeste.json`), et il est **prouvé
inerte** : la même sonde, avec et sans lui, rend des valeurs identiques, les
deux exécutions ayant abouti. La première tentative de preuve était fausse — les
deux côtés plantaient sur le même import circulaire, et le `diff` vide donnait
un vert obtenu par deux échecs identiques.

**Et la preuve inverse, qui est celle qui compte** : sous `CONSEIL_MONDE=_epreuve`,
la monnaie devient « piece », les titres deviennent « sieur, dame », et le
compteur d'argent suit. Le moteur ne connaît plus la monnaie ; le monde la lui
dit. Les deux sens sont gardés par `test_racines.py` (12 épreuves), dans des
processus séparés — ces tables se calculent au chargement, les comparer dans une
même session ne mesurerait que l'ordre des imports.

### 9 septembre, troisième passe — E12 tenue, et la mesure qui mentait

**Un troisième monde existe : `mondes/cities-of-light/`.** Notre époque, peuplée
d'agents — huit habitants, huit villes, six maisons, sa monnaie en dollars, six
genres d'unités dont **l'agent, qui est le dragon de ce monde** (la seule pièce
qui décide seule d'une journée, d'où sa propre famille de filtre). Il a son
manifeste, son état, ses chambres, son plan de ville, ses armes, ses cadrages,
un volume qu'on peut ouvrir, et une scène d'ouverture jouée.

**E12 est tenue, et voici la formulation honnête.** Le monde lui-même est
**purement de la donnée** : aucune ligne de moteur n'a été écrite pour qu'il
fonctionne. Mais l'ajouter a **révélé quatre fuites** qui ne pouvaient pas se
voir avec un seul monde, et celles-là ont demandé du code :

1. Le registre des lieux 3D annonçait « le monde 3D de Peyredragon est PÉRIMÉ »
   au démarrage d'un monde qui n'a pas de Peyredragon.
2. La date s'affichait « **2026 AC** » — notre époque datée depuis la conquête
   d'Aegon. Le format vient maintenant du manifeste.
3. Le même correctif a d'abord échoué en lisant le manifeste **au chargement**
   du module, alors que sa balise est déclarée après : on lit à l'appel.
4. Et la plus grave, ci-dessous.

**LA MESURE MENTAIT, ET ELLE A COÛTÉ UNE LIGNE DE FIL.** Une poussée lancée
sous `CONSEIL_MONDE=cities-of-light` a écrit dans le fil de **Westeros**, en la
validant contre les horloges de Westeros — le refus parlait de `rhaenyra` et de
`nicolas-lester-reynolds` dans un monde qui n'a ni l'un ni l'autre. Il a fallu
retirer la ligne à la main.

La cause tient à un nom. `scripts/scene/flux_scribe.py` — **la seule plume du
flux et le seul possesseur de l'horloge** — nommait sa racine `racine`, en
minuscules, et la mesure ne cherchait que `RACINE`. Elle annonçait donc « 19
fichiers restants » alors que **trente** restaient, dont les satellites de la
porte de l'état (`etat/entree.py`, `empreintes.py`, `purge.py`) et la feuille de
reprise.

> **Un compteur qui ne compte qu'une convention de nommage est pire qu'aucun
> compteur : il donne l'air d'avoir fini.** La mesure capture désormais le nom,
> quel qu'il soit, et vérifie que c'est bien lui qu'on colle à `etat`.

Vrai compte après réparation de la mesure **et** de la plume : **29**.

**Ce que les autres chantiers ont rendu** : les plans de château ont quitté le
code (899 lignes → 44 ; le `replaceAll` qui fabriquait Braavos depuis Peyredragon
a disparu), les blasons et les cadrages avec eux, et 45 fichiers Python ont
migré. Le vocabulaire de règles vient du manifeste, prouvé dans les deux sens :
sous le monde d'épreuve la monnaie devient « piece » et les titres « sieur,
dame ».

**Un piège de parallélisme, pour mémoire** : le chantier des plans avait retiré
sa route de la table après vérification, en le signalant. Sans cette lecture, le
plan du château et les bannières seraient restés **vides** — le repli est vide à
dessein, un plan à moitié juste faisant cliquer une porte qui n'existe pas.

### 10 septembre — la porte d'écriture change de monde

Préalable au quatrième monde (`charmed-1906`) : **la porte de `ajouter.py`
écrivait encore dans Westeros.** `etat/entree.py` calculait sa racine depuis
`__file__` ; sous n'importe quel monde nommé, chaque acte, parole ou annale
posé « une entrée à la fois » partait dans l'état de Rhaenyra. Même défaut dans
ses deux satellites (`empreintes.py` pour `veille.py`, `purge.py` pour
`purger.py`) et dans `agents/matiere.py`, la matière de `dossier.py` — qui
aurait rassemblé le dossier d'un habitant dans les tables d'un autre monde.

Les quatre lisent `racines.racine()`. Le nom `racine` est **gardé** et désigne
désormais la racine du monde : `test_chainage_actions` le détourne vers un
dossier jetable, et le retirer aurait fait écrire ce test dans le vrai `etat/`.
Vérifié : sous `CONSEIL_MONDE=cities-of-light`, `entree.chemin("actes")`,
`veille --voir`, `dossier --sur fanal` et `purger` (mode montrer) visent le
paquet ; sans variable, les mêmes chemins qu'avant. Huit gardes, sept vertes,
`chainage-actions` rouge comme avant. **Mesure : 29 → 25.**

### Ce que le prochain lot prend

Lot 1, la suite : les 74 fichiers, et la vingtaine d'usages du serveur qui
visent le code depuis `RACINE` au lieu de `DEPOT`. Puis le lot 2, qui n'a plus
d'obstacle technique — seulement un travail de données, et la décision sur le
siège à cheval.

---

## 9. Ce que l'épreuve ne dit pas

Elle ne dit rien de la scalabilité ni de l'accessibilité, qui sont les deux
autres contraintes du chantier. C'est délibéré : ce sont des travaux
orthogonaux, avec leurs propres épreuves, et les mêler à celle-ci rendrait
chacune inconcluante.

- **Scalable** s'éprouve autrement : le fil servi sans être reparsé à chaque
  sondage, une politique de rétention, un plafond et un délai sur les appels
  d'agents. Le lot 1 les rend possibles, aucun ne les fait.
- **Accessible** s'éprouve au lecteur d'écran et au clavier seul : le fil
  annoncé, les trois panneaux nommés, le décor atteignable. Le lot 3, en
  sortant les données du code, rend le décor descriptible ; il ne le rend pas
  accessible.

Les deux méritent leur document et leur épreuve. Celui-ci s'arrête ici.
