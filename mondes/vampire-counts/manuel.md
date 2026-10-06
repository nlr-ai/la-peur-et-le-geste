# Vampire Counts — le manuel de ce monde

Ce fichier est la moitié « décor » du manuel du meneur. La doctrine — la Règle
Zéro, les boucles, le brouillard, la montre, l'interdiction des menus — vit à la
racine du dépôt et ne change pas. Ici, on ne dit que ce qui est vrai **de
celui-ci**.

---

## Ce que c'est

La Terre des Cinq : un pays sans mer, entre collines et montagnes, autour de
Sighișoara. Cinq vampires, les **Aînés**, y ont fondé cinq sangs — Sépulcraux,
Écarlates, Voilés, Voraces, Stryges — et leurs lignées tiennent toutes les
villes. Les vivants sont dans les villages et sous les arbres. On est dans
l'**Ère des Seigneurs** : la société de la nuit a pris forme, les hommes ne se
sont pas encore organisés.

Le joueur est **Teodor**, Stryge, le pensionnaire de **Rupea**. Ancien
arbalétrier né à Homorod, étreint il y a soixante-quatre ans par Anselm, dit
« Rupea », il est assis depuis soixante ans à la gauche de son sire, les yeux
baissés. Il est l'héritier selon le droit du sire : le jour où Anselm sera
détruit, tout lui revient. Il croit que son père le hait et le garde à table
pour le surveiller.

**La partie s'ouvre au crépuscule du 3e jour de la 11e lune, an 1.** Le mois
dernier, Sever, l'envoyé voilé d'Odorheiu, a demandé pour la première fois
quelque chose : qu'une nuit, une porte reste ouverte. Teodor a dit qu'il
réfléchirait. Sever revient le 15.

## Le but, et contre qui

- **Le but de Teodor**, en une phrase : *survivre à son père, et que Homorod
  cesse de saigner.* Sa réponse à Sever est le premier choix de la partie.
- **Au-dehors** : Nicodim d'Odorheiu, l'Abbé, qui veut faire entrer Rupea dans
  son grand livre par un héritier endetté. Plus loin, Cendrik de Cincu, qui
  ronge le sud.
- **Au-dedans** : Anselm lui-même — un père qui ment à son fils depuis soixante
  ans pour le bien des autres, et qui le sait.

## Ce qui est canon, ce qui est inventé

- **Canon** : tout ce qui est dans `canon/` (copie du projet Vampire Kings).
  Les secrets, Masques et Natures des figures en font partie : c'est la vérité
  du MJ.
- **Inventé à l'ouverture, et déclaré** : la date de départ ; l'échelle de la
  carte (une unité ≈ 80 m) ; les salles de la citadelle ; les chiffres des
  mains (nuits de table, bandes de Homorod) ; les dates d'arrivée de Sever et
  de la saignée d'hiver ; les horloges des plans.
- **Encore à trancher** : quel Aîné tient quelle grande ville, et à qui Anselm
  est juré. Le monde lui-même ne nomme pas les Aînés (« on ne le nomme pas
  autrement ») : on peut s'en tenir là.

## Le point de vue du joueur

- Teodor sait tout ce que `canon/LORE_RECIT.md` §1-17 enseigne à un infant, et
  tout ce que soixante ans à la table de Rupea lui ont appris : les préséances,
  le droit du sire, les comptes de la citadelle (il les tient).
- Il ne sait des autres que ce que la rumeur en dit — jamais leur Masque.
- Il ne lit pas le registre de son père : le volume est réservé (`lecteurs`).

## Ce que le joueur peut ouvrir

Le siège de Teodor porte `voit_affaires: true` (`etat/joueurs.json`), à la
demande du joueur : il voit dans les livres (« Ses volumes — <nom> ») et sur
l'échiquier les cahiers d'affaire de toutes les chambres, sauf celle du MJ.
C'est une ouverture voulue du brouillard, pour le joueur et non pour Teodor :
ce qu'il y lit n'est pas une source de son personnage, et rien n'en passe dans
la fiction sans source. Retirer le drapeau referme tout.

## Ce que savent les habitants

`prompts/pnj.md` donne à chaque PNJ dépêché le savoir commun d'un infant
(LORE_RECIT §1-17 condensé, le §18 réduit à des rumeurs), avec une règle de
portée : une goule ou un vivant n'en sait que ce que sa vie lui a montré. Le
canon, le manuel et les Masques n'y entrent jamais. `AGENTS.md` part aussi chez
eux : n'y écrire que des consignes valables pour tous.

## Le brouillard de ce monde

- **Il n'y a pas de corbeaux.** Les plis vont par les goules, à pied ou à
  cheval, et de jour seulement quand le porteur est vivant. Une lettre d'Anselm,
  ce sont trois lignes et une goule qui marche des jours.
- **Un seigneur voyage en brume de sang** et se reforme plus loin — mais la
  brume se brise sous les arbres vivants, et ne passe l'eau qui court qu'aux
  ponts et aux gués. Un pont, un gué, un col gardé décident d'un voyage.
- **Tout le monde porte un Masque.** Ce qu'on dit de quelqu'un (`ce qu'on dit de
  lui` dans les fiches) est public ; le reste ne fuit que par une source.
  Teodor ne sait rien de la dernière page du registre de son père, ni de la
  nuit où Anselm s'est laissé boire pour Ilka, ni de ce que Nicodim a fait à
  Margit.
- **Qui a bu qui** est su de tous. Que Radomir ait bu Anselm, le pays entier en
  a ri ; pourquoi, personne ne le sait, sauf Radomir.

## Les contraintes dures

0. **La faim coûte la puissance** (règle du dev, 6.10). Un vampire qui a faim
   perd 30 % de sa puissance, puis progressivement de plus en plus tant que la
   faim dure : moins de morts tenus, des coups et une défense plus faibles. Ne
   jamais l'afficher en chiffre ; on la voit dans un corps, une garde, une meute
   qui se défait. Elle vaut pour les Aînés affamés de l'export (`etat/partie-vk`)
   comme pour quiconque leur cède son sang.
00. **Le serment de cour** (règle du dev, 6.10). Chaque membre d'une cour est
   lié au seigneur par trois clauses : la **ration** (rien · la Soif · le
   double), le **droit de chasse** (aucun · nos terres · terres de la lignée ·
   toutes terres) et la **chasse pour la table** (0 · 25 · 50 · 75 % des
   prises, deux chasseurs par table au plus). Le seigneur les règle ; elles
   s'écrivent dans le livre « Le serment de cour » de sa maison, et un
   changement est une parole dite à la table (`paroles.json`). Le seigneur
   peut toujours chasser lui-même (canon, LORE_RECIT §6) : le serment dit ce
   que sa cour fait en plus de lui, ou à sa place.

1. **Le jour tue.** Les maîtres dorment du lever au coucher du soleil, sauf sous
   le couvert des forêts vivantes. À la 11e lune, la nuit va d'environ dix-sept
   heures à sept heures. Le battement « ce qui s'est fait sans vous » tombe au
   crépuscule, pas à l'aube : c'est ce que les goules ont fait pendant le jour.
2. **La magie remonte le sang.** Une part de ce que reçoit Teodor coule chaque
   nuit vers Anselm. Détruire son sire ne libère personne : ce qu'on lui devait,
   on le doit au sire de son sire.
3. **Un pensionnaire n'a rien** : ni terre, ni serment à donner, ni droit
   d'étreindre. Il boit à la table de son sire. Ses moyens sont ce qu'il sait,
   ce qu'il compte, et ceux qui lui parlent.
4. **Le sang se souvient.** Une dette ne s'efface jamais ; une rancune met deux
   siècles à perdre la moitié de son poids. Ce qu'on fait à l'un, on le fait à
   toute sa famille.
5. **Être bu est pire qu'être abattu.** Le vaincu d'un duel nourrit son buveur
   des années. Le duel est trois passes : frapper, parer, feinter, un sort, ou
   rompre — tranché en coulisse, jamais affiché.
6. **On ne dit pas « mort »** pour un vampire : on dit *détruit*. Les morts, ce
   sont les soldats.

## Les mots

L'Aîné, le chef, le chef sans chef, le seigneur (on dit « Rupea », pas « le
seigneur de Rupea »), le sire et l'infant, le sang, le sans-terre, le
pensionnaire, l'installé, le buveur et le bu, le dormeur (jamais au passé), le
détruit, l'infant oublié. Voir `canon/LORE_RECIT.md` §16. Les narrations les
emploient sans les expliquer : Teodor les connaît depuis soixante ans.

## La citadelle de Rupea

Sur le rocher noir, au-dessus de la ville basse. Teodor connaît chaque pierre :
il y a monté la garde vivant.

- **La table** — la grande salle, où le maître reçoit ; Teodor à gauche.
- **La chambre de Teodor** — sous celle de son père.
- **La chambre du maître** — au-dessus ; le registre y est.
- **Les remparts** — où le maître marche la nuit en touchant les pierres.
- **La cour** — où Hedwig la Grise a été détruite.
- **La porte** — la porte de la citadelle. Celle qu'on peut laisser ouverte.
- **La ville basse** — sous le rocher, les vivants de la citadelle.

Homorod est à deux heures de marche. Comăna de Jos et les bois de la Crinière, à
une nuit au sud.
