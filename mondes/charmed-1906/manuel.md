# Charmed 1906 — le manuel de ce monde

Ce fichier est la moitié « décor » du manuel du meneur. La doctrine — la Règle
Zéro, les boucles, le brouillard, la montre, l'interdiction des menus — vit à la
racine du dépôt et ne change pas. Ici, on ne dit que ce qui est vrai **de
celui-ci**.

---

## Ce que c'est

San Francisco, mercredi 18 avril 1906, cinq heures du matin. Dans douze minutes,
la terre tremble ; pendant trois jours, la ville brûle.

La joueuse est **Prudence Warren**, sorcière de la lignée de Melinda Warren,
veuve, trente-cinq ans, télékinésiste. Elle vit sur Prescott Street avec sa fille
Lillian, sept ans, et Bridget O'Connell, sa domestique. Sa sœur cadette,
**Patience**, qui fige le temps, a quitté la maison à la mort de leur mère et
loue une chambre dans une pension de Howard Street. Sous la maison, dans la
cave, une Ombre est scellée sur un Nexus. Le Livre des Ombres dort au grenier.

Ce qu'elle bâtira après le feu, c'est la maison que Prue, Piper et Phoebe
trouveront en 1998. Chaque page qu'elle réécrit est une page qu'elles liront.

## Ce qui est canon, ce qui est histoire, ce qui est inventé

- **Canon** (la série, saison 1) : la lignée, la prophétie de Melinda, le Nexus
  sous la maison, l'Ombre libérée par un séisme et bannie par la lumière et une
  comptine-sort, les règles de la magie. Source : `canon/`.
- **Histoire** : le séisme à 5 h 12, les trois jours de feu, la dynamite de
  l'armée, l'ordre de tirer sur les pillards, les réfugiés.
- **Inventé, et déclaré** : Prudence, Patience, Lillian, Bridget, leur vie ; que l'Ombre
  soit déjà là en 1906 ; **le feu qui brûle le Livre** — ce qu'elle en sauve se
  décide en jeu, par ce qu'elle fait (`evenements.json`, `le-livre-brule`).

## Le brouillard de ce monde

- **Le télégraphe tombe avec la terre.** Pendant des jours, les nouvelles vont à
  pied, en rumeur, et se trompent de rue. Un journal de fortune vaut ce qu'il vaut.
- **La magie est un secret.** Chaque usage devant un mortel le menace. Bridget
  a choisi de ne pas voir ; ce choix a une limite.
- **Le Livre ne sait que ce qu'on y a écrit.** La vérité sur une créature est dans
  `canon/` ; Prudence n'en connaît que ce que le Livre ou sa vie lui ont appris.

## Les contraintes dures

1. **Elle est seule.** Le Pouvoir des Trois n'existe pas avant la troisième sœur —
   et deux sœurs ne font pas trois : Patience ajoute ses mains, pas un pouvoir commun.
   Une menace de rang 3 s'évite, s'emprisonne ou s'écrit pour plus tard — elle ne
   se vainc pas.
2. **Sa télékinésie passe par la colère et par les mains**, et elle n'agit ni sur
   une sorcière bonne, ni sur un esprit, ni sur l'Ombre.
3. **La peur coupe tous les pouvoirs.**
4. **Pas de magie pour son propre gain** : elle se retourne.
5. **On ne tue pas un mortel**, même hostile.
6. **Un banni n'est pas un détruit.** Ce qu'elle renvoie peut revenir, et c'est
   une génération future qui paiera.

## La partie est une danse

Une chorégraphie du bien contre le mal. **Chaque camp a ses échelles de
déploiement et ses attaques, et chaque coup rencontre son opposé** : une
attaque appelle sa parade, une parade appelle la prochaine attaque. Rien ne
monte par un compteur ; tout monte par des coups.

- **L'Être de lumière sonde les démons.** C'est le travail de Thomas Ashby : aller
  les chercher. Les démons existent sans lui et agissent sans lui ; ce qu'il
  trouve en sondant entre dans la partie — on lui écrit alors sa fiche et sa
  tête, tirées du bestiaire (`canon/`).
- **À chaque niveau de préparation, un piège plus tendu.** Ce qui entre est à la
  mesure de ce que les sorcières savent déjà faire, et un cran au-dessus : une
  sorcière qui vient de maîtriser son pouvoir rencontre ce qui l'oblige à le
  pousser. C'est la règle de la série — les pouvoirs grandissent avec la pratique
  et le danger (`canon/camp-du-bien-s1.json`, `croissance`).
- **Le démon entré agit selon sa tête**, comme tout acteur : sa loi, sa proie,
  sa fenêtre, ses déclencheurs. Il ne frappe pas parce que la scène en a besoin.
- **Le mal a un joueur : Josiah Crewe**, troisième siège, lieutenant de la Source
  pour la côte du Pacifique. Il n'a plus de tête dans `intentions.json` — ce qu'il
  croyait, ignorait et avait lancé en s'asseyant est sur sa fiche. Il ne se bat
  pas lui-même : il envoie, compte et punit. Marsh suit son horloge ; les autres
  démons gardent leur tête et ne lui obéissent que si la fiction le leur fait
  apprendre. Il ne sait ni le séisme, ni ce que les Warren gardent sous la maison,
  ni le visage de leur Être de lumière : on ne le lui dit pas, même en scène.
- **Les sorcières le gèrent, éventuellement.** Prudence, Patience, Mei — avec ce
  qu'elles ont : leurs pouvoirs, le Livre (ce qu'il en reste), la maison. Celle
  qui ne peut pas le vaincre l'évite, l'emprisonne ou l'écrit.
- **Plus il y a de pièces actives, plus c'est une partie d'échecs.** Quand les
  démons entrés, les protégés et les mandats se comptent par plusieurs à la fois,
  on cesse de jouer coup par coup en scène : on pose la position et l'on joue la
  partie (`scripts/agents/prompts/mj-partie.md`, `scripts/partie.py`).

## Comment on joue les habitants

- **Lillian** entend la voix de la cave. Sa mère ne le sait pas.
- **Bridget** court à l'enfant d'abord, se signe devant l'impossible, et continue.
- **Patience** n'habite plus la maison, mais elle y est née : enfant, elle aussi a
  entendu la voix de la cave, et elle ne l'a jamais dit à sa sœur. Elle veut qu'on
  dise à Lillian ce qu'elle est. Son gel part quand elle panique, pas quand elle veut.
- **L'Ombre** ne parle que par la bouche de qui elle possède. Elle veut la petite,
  née dans la maison.

## Ce que ce monde n'a pas

Pas de dragons, pas de corbeaux, pas de mestres, pas de 1998. Pas de Leo : l'Être
de lumière de cette ville est Thomas Ashby, et il ne connaît pas l'avenir. Si l'un
de ces mots apparaît dans une scène, c'est une fuite d'un autre monde.

## Où chercher le décor

- **L'heure, la rue, le prix, la rumeur** : `canon/histoire-1906.md`. Ce qui brûle
  et quand ; Prescott Street est à l'ouest de Van Ness et le grand feu ne l'atteint
  pas — seul le sien la menace ; la ville reste dans le noir, sous couvre-feu, et
  c'est le temps de l'Ombre.
- **Le Livre lui-même** : le volume entier est dans le livre de maison
  (`etat/maisons/maison-warren/documents/books/livre-des-ombres.json`), posé au
  grenier, `lecteurs` : Prudence, Patience, Thomas. Ce qui brûle s'y retire à
  mesure. L'inventaire du MJ — les mains, la dette envers 1998, ce que le feu
  prend selon ce qu'elle fait — reste dans `canon/livre-1906.json`.
- **Les nouvelles qui vont courir** : les événements datés du 18 au 21 dans
  `etat/evenements.json`, chacun avec qui l'apprend, où, et de travers comment.
- **Les rues** : `etat/lieux.json`, avec la marche depuis Prescott Street.
- **De quoi l'on vit** : `etat/maisons/maison-warren/documents/mains.json` — cinq
  jours de manger, dix-sept dollars dans la maison ; la banque est fermée pour des
  semaines.
