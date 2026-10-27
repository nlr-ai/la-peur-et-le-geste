# Séparer les mondes — l'inventaire du lot 2

Note de mesure, 9 septembre 2026. Elle rend compte de
`scripts/migrations/separer_mondes.py`, qui répartit **à sec** les données entre
Westeros et Venise et dit ce que la séparation casserait. Le script ne déplace
rien, jamais ; `--vraiment` ne fait que déposer sa répartition sous
`.agents-runtime/separation/`, et **refuse tant qu'une rupture n'est pas
tranchée**.

Elle répond aux lots posés par [`refonte-plan.md`](refonte-plan.md) § 4 et
applique la contrainte de [`traversee.md`](traversee.md) : *ne pas supposer
qu'une fiche appartient à exactement un monde.*

```bash
python scripts/migrations/separer_mondes.py            # le rapport
python scripts/migrations/separer_mondes.py --bavard   # les listes entières
python scripts/migrations/separer_mondes.py --table personnages
```

---

## 1. Le critère d'appartenance — six voix, dont une qui ne vote pas

Le plan disait « c'est un travail de données, pas de code ». C'est vrai, et
c'est exactement pour cela que le critère est le cœur : un `grep braavos` compte
140 items de flux quand **1 078 sont adressés au siège vénitien**, et ne voit
aucune fiche à la Fosse aux Dragons quand **76 citoyens de Venise y sont posés**.

Les six voix, de la plus solide à la plus faible :

| Critère | Ce qu'il lit | Ce qu'il vaut |
|---|---|---|
| `corps.monde` | `etat/corps.json`, champ `monde` | **Le meilleur, et personne ne le savait** — voir § 2 |
| `maison` | `maison_id` → siège → lieu | solide ; 153 fiches |
| topologie | composante connexe de `chemins.json` | solide, mais dit le **site**, pas le monde — voir § 3 |
| `lieu_id` | la fiche | **c'est lui qui ment** — voir § 4 |
| marqueur de chambre | fichier `serenissima` dans `chambres/<id>/` | **le plus faible** — il rate la moitié — voir § 5 |
| lexique | le mot « braavos », « peyredragon »… | **ne vote jamais.** Il sert de contrôle |

Le lexique est délibérément exclu du vote : la moitié des mentions de décor sont
des commentaires justes (refonte-plan § 7.6). Il n'est utilisé qu'en dernier
recours sur les items de flux qui n'ont aucune audience déclarée, et pour
signaler du bruit.

### Les quatre catégories

`westeros` · `venise` · `traverse` (les critères se contredisent, et un
**traversant déclaré** l'explique) · `indecidable` (ils se contredisent sans
raison, ou aucun ne parle). Le script liste les deux dernières, **il ne les
tranche pas**.

---

## 2. Ce que l'inventaire a trouvé et que personne n'avait vu

**`corps.json` déclare déjà un monde.** 153 corps y portent `"monde":
"braavos"`, et ce sont **exactement** les 153 fiches de `maison-serenissima` —
accord parfait, vérifié dans les deux sens, aucun écart. C'est la seule
déclaration de monde qui existe aujourd'hui dans tout l'état, elle est juste, et
elle ne servait à rien. Le lot 2 devrait la promouvoir plutôt que d'en inventer
une autre.

---

## 3. La topologie fait la moitié du travail — mais pas celle qu'on croyait

Le plan (§ 7.4) dit « Braavos est une composante connexe distincte ». C'est vrai.
Ce qu'il ne dit pas, c'est qu'il y en a **quatre**, pas deux :

| Composante | Salles | Arêtes | Monde |
|---|---|---|---|
| Peyredragon | 36 | 80 | westeros |
| Port-Réal | 52 | 52 | westeros |
| Braavos | 34 | **49** | venise |
| Barralfond (au-delà du Mur) | 6 | 12 | westeros |

**Une composante est un SITE, pas un monde.** Trois de ces quatre sites sont
Westeros. Un script qui traduirait « composante distincte » par « autre monde »
enverrait Barralfond et ses cinq habitants à Venise. Le critère topologique doit
donc passer par une table de **témoins déclarés** — une salle par site — et c'est
ce que fait `TEMOINS` dans le script.

**Zéro arête coupée.** Les 193 arêtes tombent proprement d'un côté ou de l'autre.
La topologie n'a rien à réparer, et c'est la bonne nouvelle du lot.

---

## 4. Les désaccords entre critères — ce qui coûterait une journée

### ① 76 citoyens de Venise habitent la Fosse aux Dragons

`maison-serenissima` + `corps.monde: braavos` d'un côté ; `lieu_id:
"fosse-dragons"` de l'autre — le chaudron de la colline de Rhaenys, à Port-Réal,
contrôlé par les Verts. Tous les 76 sont `dormant`, sans routine et sans chambre :
ce sont les citoyens importés qu'on a garés là. C'est **le plus gros désaccord de
critères du dépôt**, et il est bénin à réparer (repointer sur `braavos`) à
condition de le voir avant le déménagement, pas après.

Répartition réelle des 153 fiches Serenissima : **77 à `braavos`** (76 actifs
avec routine et chambre, plus Nicolas) et **76 à `fosse-dragons`** (tous
dormants).

### ② Le marqueur de chambre en rate la moitié

Le plan comptait « 76 dossiers sur 313 ». **C'est 154.** Le fichier marqueur
`serenissima` n'est posé que dans 76 chambres ; 78 autres appartiennent à Venise
par leur fiche sans porter la marque. Le marqueur ne doit pas servir seul.

Trois défauts de nommage s'y ajoutent, tous déjà présents :

- **`efficiency-maestro` et `efficiency_maestro` sont deux chambres pour un seul
  homme.** C'est exactement l'interdit de `traversee.md` § 5 — déjà réalisé, sans
  traversée pour l'excuser. À fusionner avant tout déménagement.
- **182 dossiers sur 313 ne portent pas le nom exact d'une fiche.** La
  normalisation (casse, tirets, soulignés — `adriatic_captain` contre
  `adriatic-captain`) en résout 139 ; **43 restent sans fiche**. Cinq d'entre eux
  sont des renommages non propagés : `DonPaolo_Castello`, `DonPaolo_Wanderer`,
  `FraAngelo_SanMarco`, `PadreMarco_Preacher`, `PadreMarco_Scholar` sont les cinq
  `cleroshepherd1..5` de `personnages.json`. Une vingtaine d'autres sont des
  chambres de Westeros ouvertes sous le nom complet quand la fiche porte l'id
  court (`mestre-gerardys` / `gerardys`, `daemon-targaryen` / `daemon`,
  `ser-robert-quince` / `robert-quince`) ; le reste est de l'outillage
  (`_broadcast`, `_claims`, `_hooks`, `_tools`, `dev`, `mj`, `boucle`,
  `purge-arriere`).
- Un dossier de `chambres/` s'appelle
  `precision-observer,living-stone-architect,shiren,efficiency-maestro,ducalepalace,system-diagnostician`
  — une liste de noms passée en nom de dossier.

### ③ 21 volumes de Venise sont posés dans une salle qui n'existe pas

Les livres de `maison-serenissima` portent `salle_id: "archive"`. Cette salle
n'est dans **aucune** composante : Peyredragon a `archives` (au pluriel), Braavos
a `braavos-archives`. Les 21 volumes s'ouvriront dans le paquet de Venise en
pointant vers rien.

### ④ Deux identités pour le même siège

`nicolas-reynolds` et `nicolas-lester-reynolds` cohabitent : le premier n'a pas
de fiche et porte pourtant **49 actes** et **203 items de flux**. Il est déclaré
comme traversant dans le script pour ne pas fausser le compte, mais c'est une
dette à solder, pas un fait de fiction.

---

## 5. Ce qui traverse — et c'est un seul homme

**66 lignes tombent en `traverse`, et toutes concernent Nicolas Lester
Reynolds.** Aucune autre entité du dépôt ne touche les deux mondes.

| Table | Lignes qui traversent |
|---|---|
| `relations.json` | **25** — c'est-à-dire *toutes* les relations inter-mondes du dépôt |
| `actes.json` | 23 |
| `paroles.json` | 16 |
| `evenements.json` | 2 |

**Et elles penchent toutes du même côté : Westeros.** Il est le frère de Yohanna
Reynolds de Pierrefitte, employé par Corlys à Lamarck en 126, par Rhaenyra en
127, vérifié par Marlo à Port-Réal en 128 ; son journal de siège s'ouvre sur son
débarquement au quai de Peyredragon ; sa table de guerre porte la levée de
Pierrefitte (144 hommes) ; ses `vues` sont Yohanna à Pierrefitte et Rhaenyra à
Peyredragon. Sa seule attache vénitienne est administrative :
`maison_id: maison-serenissima`, `lieu_id: braavos`, et 152 citoyens dans son
`pnj`.

**Autrement dit : `traversee.md` § 6 décide que son monde natal est Venise, et
les données disent le contraire.** Ce n'est pas une contradiction à corriger
mécaniquement — c'est une décision de jeu, et elle a un prix chiffré : § 6 ①.

---

## 6. Ce que la séparation casserait, par gravité

Quatre classes. `deja-rompu` est compté à part parce qu'on ne met pas sur le dos
de la séparation ce qui était cassé avant elle.

### RUPTURE — 137 : un fait du jeu est détruit

| # | Quoi | Pourquoi c'est grave |
|---|---|---|
| ① | **135 items de flux** servis à des sièges des deux mondes | Ces scènes ont été **entendues** par Rhaenyra, Aurore et Nicolas ensemble. Après séparation, un des deux mondes doit les oublier — et le flux est append-only : on ne réécrit pas |
| ② | **`etat/horloges.json`** : un fichier, quatre sièges, deux mondes | C'est le défaut nommé par le plan (§ 7.2). Venise est au 12e jour de la 5e lune de l'an 129 |
| ③ | **`efficiency-maestro` + `efficiency_maestro`** | Deux chambres pour un homme : la faute que `traversee.md` interdit, déjà commise |

Les 135 items se répartissent en 109 (Aurore + Nicolas + Rhaenyra), 20 (+ Marlo),
5 (`nicolas-reynolds` + Rhaenyra) et 1 (+ Corneille). Ils tiennent en quatre blocs
de fil, pas en poussière : lignes 10081–10116, 11515, 11772–11860 et 12243–12350.

### PENDANTE — 98 : une référence pointera vers rien

| # | Quoi | Combien |
|---|---|---|
| ① | Fiches dont le `lieu_id` reste dans l'autre monde (§ 4 ①) | **76** |
| ② | Volumes posés dans la salle `archive`, absente de la topologie (§ 4 ③) | **21** |
| ③ | **Le dossier de siège de Nicolas** — `jetons.json`, `vues.json`, `objectifs.json` | **1**, et c'est le plus cher |

**Le ③ est la catégorie manquante.** `traversee.md` tranche que « la mémoire
appartient à l'homme » : son dossier de croyances part donc à Venise avec lui.
Mais ce dossier ne contient que des ids de Westeros — `levee-pierrefitte`,
`yohanna-reynolds`, `rhaenyra`, `peyredragon`. Un brouillard de guerre qui
décrit un monde étranger n'est ni « la mémoire de l'homme » ni « les actes du
lieu » : c'est un **carnet de voyage**, et le partage en deux de la note n'a pas
de case pour lui. Il faudra soit l'écrire (les ids étrangers restent lisibles
comme du texte figé, à la manière d'un pli qui arrive périmé), soit accepter que
la table de guerre de Nicolas s'ouvre vide à Venise.

### DÉJÀ-ROMPU — 232 : cassé avant nous

53 identifiants cités par `actes.json` et `paroles.json` n'ont aucune fiche
(`sara-poulain` ×23, `garde-tour` ×26, `cour-du-banquet` ×20, `crieur` ×13,
`wat`…), 43 chambres sans fiche, un dossier `etat/joueurs/joueur/` sans siège.
Rien de tout cela ne vient de la séparation ; la séparation les rendra seulement
plus visibles, chaque paquet devenant assez petit pour qu'on les voie.

### BRUIT — 1 753 : le vocabulaire, et les items sans audience

- **1 744 items de flux sans `pour`.** Personne ne sait de quel monde ils sont.
  Ils sont tous antérieurs à l'ouverture du siège vénitien, donc Westeros par
  chronologie — mais **c'est un raisonnement, pas une donnée**, et il faut le
  décider une fois pour toutes plutôt que le refaire à chaque table.
- **9 salles de Venise portent des noms westeriens** : `braavos-table-peinte`,
  `braavos-porte-dragon`, `braavos-jardin-aegon`, `braavos-septuaire`,
  `braavos-tour-dragon-mer`, `braavos-appartements-reine`,
  `braavos-guivre-des-vents`, `braavos-roukerie`, `braavos-chambre-enfants`. Le
  plan de Braavos est une **copie littérale de celui de Peyredragon**, préfixée.
  E3 (« Venise ne connaît pas Westeros ») tombe dessus, et pas sur un
  commentaire : sur des identifiants que le jeu utilise.

---

## 7. L'amarre — quelle date poser, et sur quoi la caler

> **Le 12e jour de la 5e lune de l'an 129 (après la Conquête) était le
> <jour vénitien à nommer> de Venise.**

**Pourquoi cette date, et pas une autre.** C'est la seule qui soit un FAIT et non
un choix : les quatre sièges lisent aujourd'hui `129 / 5 / 12` dans
`etat/horloges.json`, `monde.json` porte la même, et **toute** la vie vénitienne
écrite dans l'état y est datée — les 25 actes de Braavos, les 33 conclusions, les
1 078 items de flux de Nicolas, jusqu'à la minute. Tant que les deux mondes
lisent la même date, cette date est leur dernier point de contact honnête ;
après la séparation il n'y en aura plus jamais d'autre. Le script l'affiche à
chaque passage, sous « L'AMARRE ».

**Le fait sur lequel la caler.** Pas la date d'un fichier, un événement du
monde : **`acte-convocation-premier-conseil-porteurs-129-5-12`** — Nicolas
convoque les mains des neuf affaires au premier conseil de Braavos. C'est le
dernier acte de la journée, il est vénitien, il est daté, et il est le moment où
Venise se donne ses propres institutions. Une amarre calée sur lui se raconte en
une phrase, ce qui est la seule chose qu'on demande à une amarre.

**Ce qui reste à trancher, et qui n'est pas mesurable.** Le côté vénitien du
couple. Le dépôt ne porte aucune date de fiction pour Venise : les chambres
importées portent des dates réelles (`CreatedAt: 2025-05-17`) et leurs manuels
disent « 1500s Venice » (12 fois), « 1490s » (4), « 1470s » (2). Il faut choisir
l'année une fois, l'écrire dans le manifeste de Venise, et poser l'amarre
dessus. Rien dans les données ne le fera à votre place.

---

## 8. Les comptes, table par table

Mesurés le 9 septembre. `traverse` et `indécidable` ne sont pas répartis.

| Table | westeros | venise | traverse | indécidable |
|---|---:|---:|---:|---:|
| `lieux.json` | 24 | 1 | 0 | 0 |
| `maisons.json` | 19 | 1 | 0 | 0 |
| `personnages.json` | 127 | 77 | 0 | **76** |
| `chambres/` | 121 | **154** | 0 | 38 |
| `chemins.json` (arêtes) | 144 | 49 | 0 | **0** |
| livres (`maisons/*/documents/books`) | 139 | 25 | 0 | 5 |
| sièges (`joueurs.json`) | 4 | 1 | 0 | 0 |
| `flux.jsonl` | 9 755 | 1 089 | 0 | 1 879 |
| `relations.json` | 115 | 0 | **25** | 0 |
| `actes.json` | 638 | 25 | 23 | 2 |
| `paroles.json` | 668 | 2 | 16 | 0 |
| `info.json` | 18 | 0 | 0 | 58 |
| `intentions.json` | 81 | 0 | 0 | 0 |
| `pensees.json` | 1 581 | 9 | 0 | 0 |
| `conclusions.json` | 26 | 33 | 0 | 0 |
| `evenements.json` | 147 | 0 | 2 | 5 |
| `joueurs/<siège>/` | 3 | 1 | 0 | 1 |
| `depeches/` | 1 081 | 1 229 | 0 | 139 |
| `activations/` | 204 | 70 | 0 | 40 |

**Sur les 2 243 indécidables, 211 seulement sont un désaccord de critères ; les
2 032 autres sont un silence** — aucun critère ne parle, parce que l'entrée ne
nomme personne (les 58 `info`, les 1 744 items de flux sans `pour`). Les deux ne
coûtent pas la même chose : le désaccord demande une décision, le silence une
règle par défaut, écrite une fois.

**Ce que le script ne compte pas, et qui n'a rien à répartir.** `corps.json` ne
porte **aucune** affectation de bâtiment à Braavos sur ses 207 : Venise n'a pas
de géométrie, donc rien à déménager de ce côté. `intentions.json` est
intégralement Westeros — Venise n'a aucune tête. `presence.json` a 33 de ses 45
entrées dans des salles `braavos-*`.

---

## 9. La séparation est-elle possible en l'état ?

**Oui, et le coût est petit — mais quatre choses doivent être tranchées avant, et
une seule d'entre elles est vraiment difficile.**

Ce qui est prêt : la topologie ne demande rien (zéro arête coupée), Venise n'a ni
géométrie ni têtes ni intentions à démêler, `intentions.json`, `pensees.json`,
`corps.json` tombent d'un seul côté, et `corps.monde` fournit un critère juste
déjà écrit.

### À trancher, du plus dur au plus simple

1. **Nicolas, et le carnet de voyage.** La décision de `traversee.md` (monde
   natal = Venise) est prise ; sa conséquence ne l'est pas. Ses 25 relations, ses
   23 actes, ses 16 paroles et **tout** son dossier de siège regardent Westeros.
   Il faut décider ce qu'un homme emporte de ses croyances sur un monde qui n'est
   plus le sien : soit une troisième forme (le carnet de voyage, des ids
   étrangers figés et lisibles comme un pli périmé), soit l'acceptation qu'il
   arrive à Venise la table de guerre vide. **C'est la seule vraie question du
   lot**, et c'est celle que le § 3 de la note laissait ouverte sans le dire.
2. **Les 135 items de flux entendus des deux côtés.** Le flux est append-only :
   on ne peut ni les couper ni les réécrire. Trois voies : les donner au monde
   du siège principal et accepter que Nicolas perde son passé partagé ; les
   dupliquer dans les deux flux (ce qui ne viole pas « une mémoire ne se coupe
   pas en deux », un flux étant une trace de scène et non une mémoire d'homme) ;
   ou couper le fil à la ligne 10081 et archiver l'avant comme un seul monde.
3. **Le défaut des 1 744 items sans `pour`.** Une règle, une fois : « un item de
   flux sans audience appartient au monde du siège principal ». À écrire, pas à
   deviner table par table.
4. **L'année vénitienne** (§ 7), et les trois réparations bénignes : les 76
   `lieu_id: fosse-dragons`, les 21 `salle_id: "archive"`, la chambre en double.

### Ce qui devrait entrer dans la route de vérification

Trois requêtes, la même discipline que les gardes de `traversee.md` § 7.3 :
une chambre présente dans deux paquets, une fiche dont le `lieu_id` n'est pas de
son monde, un item de flux servi à des sièges de deux mondes. Les trois sont déjà
écrites dans ce script ; il ne reste qu'à les brancher sur `verifier.mjs` le jour
où les paquets existent.
