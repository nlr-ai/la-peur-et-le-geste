# Navarre 1572 — le manuel de ce monde

Ce fichier est la moitié « décor » du manuel du meneur. La doctrine — la Règle
Zéro, les boucles, le brouillard, la montre, l'interdiction des menus — vit à la
racine du dépôt et ne change pas. Ici, on ne dit que ce qui est vrai **de
celui-ci**. Le pitch d'origine : `docs/pitch-navarre-1572.md`.

---

## Ce que c'est

Paris, été 1572. Deux ans après la paix de Saint-Germain, la reine mère marie sa
fille Marguerite au chef des princes huguenots pour sceller la paix des deux
religions. Paris, catholique et affamée, ne veut ni de la paix ni des huit cents
gentilshommes en noir venus avec le marié. L'amiral de Coligny pousse le roi
vers une guerre en Flandre contre l'Espagne ; la reine mère n'en veut pas.

Le joueur est **Henri de Bourbon, roi de Navarre**, dix-huit ans. Sa mère, Jeanne
d'Albret, est morte à Paris le 9 juin ; il est roi depuis deux mois. Élevé à la
cour de France de huit à quatorze ans, puis en Béarn et à La Rochelle, il revient
au Louvre cinq ans plus tard.

**La partie s'ouvre le 18 août 1572, vers onze heures et demie, sur l'estrade
dressée devant Notre-Dame.** Le cardinal de Bourbon vient de les marier. La cour
se tourne vers le portail pour la messe.

## Le but, et contre qui

- **Le but d'Henri**, en une phrase : *ramener ses hommes vivants hors de Paris,
  puis sortir de la cage à la tête de son parti.*
- **Au-dehors** : Henri de Guise, qui veut la mort de l'amiral, et Paris — son
  prévôt, ses milices, ses prédicateurs.
- **Au-dedans** : Catherine de Médicis, sa belle-mère, qui lui sourit. Charles IX
  est le pivot ; Margot, l'alliée à gagner.

## Le joueur sait la date — et c'est assumé

Le joueur connaît la Saint-Barthélemy ; Henri non. On ne le lui cache pas, on
l'encadre :

1. **Henri n'agit que sur ce qu'il peut justifier.** Un ordre fondé sur l'avenir
   (« quittons Paris, on va nous massacrer ») tombe sans source : ses capitaines
   le prennent pour la peur d'un jeune homme, Coligny pour une offense au roi,
   et la reine mère, si elle l'apprend, pour la preuve qu'il sait quelque chose.
   Ce qui porte, c'est ce qu'il a VU : un homme à une fenêtre, une maison louée
   par un client des Guise, des chaînes qu'on prépare, des armes qu'on entre à
   l'Hôtel de Ville, des croix blanches.
2. **Le canon dévie dès qu'il bouge.** Les têtes de Catherine, Guise, Charles IX
   et Le Charron portent des horloges et des déclencheurs. S'il éloigne ses
   hommes, si Coligny part, si le tireur est pris, le plan d'en face change de
   date ou de cible. Ne remets jamais le rail en place : au bout de deux jours de
   déviation, le savoir du joueur ne vaut plus rien, et c'est voulu.

## Les horloges du canon

Dans `etat/evenements.json`, avec leurs conditions de déviation. Ce qui dépend
d'une **décision d'Henri** n'y est pas, parce qu'il est le décisionnaire : entrer
ou non à la messe, abjurer (canon : 26 septembre), suivre l'armée devant La
Rochelle (1573), s'évader (canon : 5 février 1576, à une chasse près de Senlis).
Ces choses-là sont des scènes, jamais des événements qui tombent seuls.

| Date | Ce qui tombe |
|---|---|
| 18.8 | Les noces. Banquet à l'évêché, bal au Louvre. |
| 20.8 | *Le Paradis d'amour* au Petit-Bourbon. |
| 21.8 | Course de bague et tournoi dans la cour du Louvre. |
| 22.8 vers 11 h | Maurevert tire sur Coligny, rue des Poulies, près de Saint-Germain-l'Auxerrois. |
| 22.8 après-midi | Le roi et la reine mère au chevet de l'amiral. Ambroise Paré l'a soigné. |
| 23.8 au soir | Conseil restreint chez la reine mère ; le roi cède. |
| 24.8 avant l'aube | Tocsin. Coligny tué rue de Béthisy. Gentilshommes de Navarre tués dans la cour du Louvre. |
| 24.8 au matin | Navarre et Condé devant le roi. |
| 30.5.1574 | Mort de Charles IX. |

## Ce qui est histoire, ce qui est inventé

- **Histoire** : les personnes, leurs âges, leurs liens, les lieux, les dates du
  tableau ci-dessus, la mort de Jeanne d'Albret le 9 juin, l'arrivée d'Henri le 8
  juillet avec ses gentilshommes en deuil, la dispense papale qui n'est pas
  arrivée, Paré au chevet de l'amiral, Margot qui cache un huguenot blessé dans
  sa chambre dans la nuit du 24.
- **Tradition, à tenir comme rumeur et jamais comme fait** : les gants
  empoisonnés de la reine Jeanne (vendus par René, le parfumeur de la reine
  mère) ; Charles IX poussant la tête de Margot pour son « oui » ; le roi tirant
  à l'arquebuse depuis une fenêtre du Louvre ; « la messe, la mort ou la
  Bastille ».
- **Inventé à l'ouverture, et déclaré** : les heures exactes dans la journée ;
  les salles et les minutes de marche de `chemins.json` ; les ordres de grandeur
  d'argent des maisons ; les plans, croyances et déclencheurs des têtes ; la
  date d'élection de Le Charron (16 août, à vérifier).
- **À vérifier avant d'en faire un fait** : le nombre de gentilshommes logés au
  Louvre (on retient une quarantaine, sur huit cents à Paris) ; le jour exact où
  Aubigné quitte Paris (canon : quelques jours avant le 24, après une querelle).

## Le point de vue du joueur

- Henri sait tout ce qu'un prince du sang de dix-huit ans sait : les
  préséances, la forme d'une cour, qui sont les Guise et pourquoi ils haïssent
  l'amiral (le meurtre de François de Guise en 1563), ce qu'est un édit de
  pacification, la valeur d'un gouvernement de province. Ne le fais jamais
  découvrir une évidence de son rang.
- Il connaît Anjou et Guise **enfants** — ils ont joué ensemble au Louvre —, pas
  les hommes qu'ils sont devenus.
- Il ne sait rien des conseils de la reine mère, ni de la maison louée par
  Maurevert, ni des ordres donnés au prévôt. Tout cela ne lui parvient que par
  une source.

## Le brouillard de ce monde

- **Il n'y a pas de corbeaux.** Un pli pour La Rochelle, c'est un cavalier et
  huit jours. Dans Paris, un page et vingt minutes.
- **Les portes de Paris se ferment** à la nuit, et sur ordre. Une ville qui
  ferme ses portes et tend ses chaînes coupe un homme du monde en une heure.
- **La Seine sépare** le faubourg Saint-Germain du Louvre : les ponts sont à
  l'est (pont Notre-Dame, pont Saint-Michel), les bacs et les bateaux se
  réquisitionnent. Qui loge outre-Seine peut fuir ; qui loge au Louvre, non.
- **Tout le monde a deux visages à la cour.** Ce qu'on dit en public n'est pas
  ce qu'on veut ; la reine mère sourit à ceux qu'elle sacrifie.

## Les contraintes dures

1. **Henri ne commande pas Paris.** Il commande ses gentilshommes et sa maison.
   Le guet, les portes, la milice et les archers du roi ne sont pas à lui.
2. **La parole du roi est la loi** — et Charles IX change d'avis. Une promesse
   royale vaut jusqu'à la prochaine conversation avec sa mère.
3. **Un prince du sang ne fuit pas sans congé.** Quitter Paris sans permission
   du roi après ses noces, c'est se déclarer rebelle. Ça se fait — mais c'est un
   acte de guerre, avec ses conséquences.
4. **Margot est une Valois.** Elle peut sauver, elle peut trahir, elle ne sera
   jamais une simple épouse. Ce qu'Henri lui confie, sa mère peut l'apprendre.
5. **La violence est de l'Histoire, pas un spectacle.** On la joue à hauteur
   d'Henri : ce qu'il entend, qui frappe à sa porte, les corps dans la cour au
   matin. Pas de panoramique, pas de complaisance.

## Les valeurs locales du schéma

- `allegeance_affichee` / `allegeance_reelle` des maisons : `huguenot` |
  `catholique` | `politique` (catholique qui veut la paix) au lieu de
  noir / vert / neutre.
- `jours_de_pr` de `lieux.json` se lit **jours de cheval depuis Paris**.

## Paris, ce que le plan connaît

Les salles sont dans `etat/chemins.json` (minutes de marche) :

- **Le Louvre** — la chambre du roi de Navarre, la chambre de la reine de
  Navarre, l'appartement de la reine mère, la chambre du roi, l'escalier du roi,
  la salle des gardes, la cour, le guichet.
- **Autour** — Saint-Germain-l'Auxerrois (la cloche), le Petit-Bourbon, la rue
  des Poulies, la rue de Béthisy (l'hôtel de l'amiral), les Tuileries, la porte
  Saint-Honoré.
- **Plus loin** — le parvis et la nef de Notre-Dame, l'évêché, l'Hôtel de Ville
  et la Grève, l'hôtel de Guise au Marais, le faubourg Saint-Germain outre-Seine.
