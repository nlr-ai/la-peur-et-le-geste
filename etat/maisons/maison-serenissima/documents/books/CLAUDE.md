# 📐 Ouvrir une affaire ici — le standard des champs du graphe

Ce dossier est l'étagère de **maison-serenissima** : les audits, specs et plans
techniques du dépôt. Un cahier qu'on y pose devient un **graphe** — le tisseur
en fait des nœuds et des arêtes, l'échiquier le rend en plateau. Ce fichier est
la règle opposable pour en écrire un.

Deux autorités, et elles ne disent pas la même chose :

- **La forme de fiction** — `etat/maisons/maison-targaryen-noir/documents/books/guide-des-affaires.json`
  (« Comment on ouvre une affaire ») : les sept objets et l'ordre de construction.
- **Le contrat technique** — [`affaire-regles-champs-graphe.json`](affaire-regles-champs-graphe.json),
  plage 86000. C'est LUI qui fait loi sur les champs. Ce CLAUDE.md en est le
  résumé exécutable ; en cas de doute, le cahier 86000 tranche.

---

## 1. Les sept objets, et ce qu'ils sont

**L'affaire n'est pas un septième objet.** Elle organise le problème ; les six
autres construisent le plan.

| | Objet | Ce que c'est | La faute |
|---|---|---|---|
| 🏰 | **Affaire** | Le conteneur de travail pour un sujet cohérent | En ouvrir une parce qu'une action de plus est apparue. Elle reste dans l'affaire existante |
| 🎯 | **État cible** | Une **réalité supérieure** recherchée : ce qui devient vrai, où, et ce que ça apporte | L'attribuer à quelqu'un. Les fins sont communes ; on assigne des actions |
| 🔒 | **Verrou** | Dit **positivement** la capacité qui doit devenir possible — formulé avec `doit` | L'écrire comme un bug, une négation ou un nom de solution |
| 🗝️ | **Clef** | La **transformation** qui ouvre le verrou, **nommée par un verbe** | Y poser un composant, un document ou une tâche. Une clef n'est pas son implémentation |
| ⚔️ | **Action** | Un **geste décidé** qui réalise une clef, sous une autorité, avec des moyens | Une action qui ne remonte à aucune clef. C'est une occupation : elle se supprime |
| 🔨 | **Moyen** | Une **capacité existante et adressée** (code `M…`) | Le créer ici. Il vit dans [`plan-moyens-serenissima.json`](plan-moyens-serenissima.json) et se **cite** |
| 🪶 | **Office** | L'autorité permanente qui porte l'action (ici : un container) | Lui donner un état cible. Un office porte des actions, il ne possède aucune fin |

**Test du verrou** : si tout le reste était acquis et que ceci restait vrai,
l'état serait-il impossible ? Si non, ce n'est pas un verrou.

**Clef ≠ action.** La clef décrit l'effet stable ; deux actions différentes
doivent pouvoir la réaliser sans la redéfinir. `⚖️ Décision` tranche un
principe (`à étudier` · `retenue` · `écartée`) ; `⏳ État` tranche un engagement
(`proposée` · `prise` · `en cours` · `faite`). Une clef retenue peut n'avoir
aucune action prise — ce n'est pas un trou.

---

## 2. Les deux épreuves, à chaque passe

- **DESCENDRE** — que veut-on (🎯) → qu'est-ce qui l'empêche (🔒) → par quel
  mécanisme (🗝️) → que fait-on (⚔️) → avec quoi (🔨) → sous quelle autorité (🪶).
  Si la chaîne s'arrête avant les actions, l'état est une intention sans plan.
- **REMONTER** — depuis n'importe quelle action jusqu'à l'affaire. Remontée
  impossible = l'action n'a **pas de raison stratégique démontrée** : elle se
  supprime ou se requalifie.

---

## 3. La règle des cellules — le cœur du contrat

**Une cellule qui porte une relation n'est pas une note libre.**
`⬆️ Sert`, `⛔ Bloque`, `🔓 Ouvre`, `🗝️ Réalise`, `⛓️ Dépend de`, `🧰 Moyens`
et `🪶 Office` doivent contenir des **adresses que le tissu sait résoudre** —
numéros, codes `M…`, codes `O…`, séparés par ` · `. La prose explique la valence
et la preuve ; **elle ne remplace jamais l'arête.**

- **Identité et genre** : la première cellule porte l'adresse (`**86101**`), le
  titre de la table porte le genre. Déplacer les colonnes ne doit rien changer
  au graphe produit.
- **Valence** : chaque nœud dit ce qu'il **apporte**, pas seulement qu'il existe.
  Deux états doivent être comparables sans lire leurs actions.
- **Dépendances logiques → sur le VERROU** (`⛓️ Dépend de` = quelle autre serrure
  doit déjà être levée pour que celle-ci puisse l'être). Une action ne porte une
  dépendance que s'il s'agit d'un **ordre d'exécution réel** entre deux gestes
  décidés — jamais pour reconstruire des phases de projet.
- **Statut borné à la preuve** : `présent`, `partiel`, `absent`, `proposé`,
  `pris`, `en cours`, `fait` restent distincts. Un fichier présent n'est pas une
  capacité validée ; une intention ne devient pas un fait par inférence.
- **Tout fichier employé se cite comme moyen** : un chemin écrit seulement dans
  une preuve ou un ancrage reste invisible à la topologie. Qualifier au registre
  des moyens, puis citer son `M…` dans `🧰 Moyens`.

---

## 4. Le fichier — squelette exact

Un volume est un JSON à plat. **Toute clé hors format est ignorée en silence à
l'écran** : on croit avoir écrit ce qui n'existe pas. Format complet :
[`docs/books.md`](../../../../../docs/books.md).

```json
{
  "id": "affaire-<slug>",
  "maison_id": "maison-serenissima",
  "boite": "boite-grand-plan",
  "titre": "AUDIT: <NomContainer> - <objet>",
  "sous_titre": "📐 … Plage <N>000 à <N>999.",
  "type": "plan",
  "embleme": "📐",
  "couleur": "#725f8f",
  "lieu_id": "braavos",
  "salle_id": "archive",
  "pages": ["…"],
  "tables": []
}
```

**Le titre d'un audit suit exactement `AUDIT: <NomContainer> - <objet>`**, avec
le nom canonique du container audité (`docs/containers.json`), et le champ
`🏷️ LE NOM` de l'ouverture est **identique au titre**. Les containers
secondaires restent dans le périmètre et les moyens, jamais dans le titre — il
garde une autorité principale. Une spec se nomme `SPEC: …`, un standard
`STANDARD: …`.

Après création, ajouter l'`id` à [`_ordre.json`](_ordre.json) : sans quoi le
volume ne se range pas sur l'étagère.

---

## 5. Les tables, dans cet ordre

**Écrites à la main :**

1. `🏰 Ouverture de l'Affaire` — colonnes `🧱 Le champ · ✍️ Ce qu'on y écrit ·
   📖 La règle du champ · ✅ Rempli ?`. Lignes : `🏷️ LE NOM`, `🎯 L'OBJET`,
   `🧱 LE PÉRIMÈTRE — DANS`, `🚫 LE PÉRIMÈTRE — HORS`, `📌 L'ÉTAT ACTUEL`,
   `🔢 LA PLAGE`, `💡 LA CONCLUSION`, `🔚 FERMÉE QUAND`.
   L'ouverture suffit à ouvrir : **on n'attend pas d'avoir un verrou pour créer
   l'affaire**, sans quoi on ne l'ouvrirait que pour ce qu'on sait déjà faire.
   On n'écrit jamais dans `📌 L'ÉTAT ACTUEL` ce qu'on espère faire.
2. `🔗 Affaires liées` — `🪢 Le lien · 🔗 L'affaire · 🔢 Notre pièce · 🔢 La leur · 📝 Pourquoi`.
3. `🎯 États cibles` — `🎯 N° · 🏷️ L'état · ✅ Ce qui doit être vrai · 💡 Valence ·
   📍 Où · 👁️ La preuve · ⬆️ Sert · 💯 Importance`.
4. `🔒 Verrous ouverts` — `🔒 N° · 🏷️ Le verrou ouvert · ⛔ Bloque ·
   📌 Ce qui est vrai aujourd'hui · ⛓️ Dépend de · 👁️ La preuve · 🔓 Levé quand`.
5. `🗝️ Clefs retenues` — `🗝️ N° · 🏷️ La clef · 🔓 Ouvre · 💡 Le principe et sa valence ·
   🧰 Moyens · 🧭 Ancrage · 👁️ La preuve · ⚖️ Décision`.
6. `⚔️ Actions proposées` — `⚔️ N° · 🏷️ L'action · 🗝️ Réalise · 📝 Ce qu'on fait ·
   📍 Où · 🪶 Office · 🧰 Moyens · ⛓️ Dépend de · 👁️ La preuve · ⏳ État`.

**Calculées — ne jamais écrire à la main** (leur titre porte le rappel, et une
saisie manuelle sera écrasée) :

- `⛓️ Ce qui pend, et sur qui`
- `🔨🪶 Ce qu'on engage, et qui d'autre le veut`
- `🕳️ Les trous`

---

## 6. La numérotation

**Un bloc de mille par affaire**, déclaré dans `🔢 LA PLAGE` et rappelé dans le
`sous_titre`. À l'intérieur : **un bloc de cent par état cible** — l'état en
`…000`, ses verrous en `…001` à `…009`, ses clefs en `…010` à `…019`, ses
actions en `…020` à `…099`.

**Le chiffre est une adresse, non un rang.** Il ne se renumérote jamais ; ce
qu'on abandonne le garde, pour qu'on sache qu'il a existé.

**Avant de choisir une plage, vérifier qu'elle est libre** — deux cahiers de ce
dossier partagent aujourd'hui 87000, et la règle d'adresse interdit de le
réparer après coup :

```bash
grep -ho "Plage [0-9]* .. [0-9]*" etat/maisons/maison-serenissima/documents/books/*.json | sort -u
```

Aucun script ne réserve les plages : c'est une lecture des `sous_titre`, et
c'est à l'auteur de la faire avant d'écrire une ligne.

---

## 7. Se prouver — trois preuves distinctes

Un JSON valide, un tissu résolu et une vue fidèle sont **trois choses
différentes**, et on ne conclut pas de l'une aux autres :

```bash
python scripts/tick.py --verifier
```

```bash
python scripts/tisser.py --pendantes
```

Puis ouvrir l'échiquier et vérifier que la chaîne rendue est la même. Une arête
`flou=true`, une cible `?`, une colonne qui ne descend à aucune action : le
cahier n'est pas fini. Un fixture aux colonnes permutées doit produire les mêmes
nœuds, arêtes et encarts qu'avant permutation.

---

## 8. Les deux espèces de trous

Le **trou mécanique** se détecte — verrou sans clef, clef non tranchée, action
sans office. Les détecteurs de l'échiquier ne font que ça, ils ne coûtent rien,
et ils valent peu : c'est de la tenue de registre.

Le **trou narratif** ne se détecte pas : il se trouve **en travaillant**, et il
s'écrit comme un **🔒 verrou**, dans la structure — jamais comme une phrase dans
une colonne d'avancement, où aucun détecteur ne la lira. Le mécanique est
l'**aval** du narratif, pas son concurrent. Note de conception :
[`docs/echiquier.md`](../../../../../docs/echiquier.md).
