# Dix minutes — le salon
## Le monde
Un salon hors du temps, un soir. Neuf invités y ont été réunis, pris chacun à un instant précis de sa vie : quatre humains qui ont gouverné, quatre qui ont travaillé de leurs mains, et un agent d'intelligence artificielle venu d'après la fin de l'humanité. Ils se parlent deux par deux, dix minutes par table, puis la clochette sonne et les paires changent. Comme ils sont neuf, l'un d'eux attend au vestibule à chaque ronde. **Le but de chaque invité est d'avoir les meilleures conversations possibles.** C'est lui qui décide de ce que « meilleure » veut dire.

Il n'y a ni guerre, ni carte, ni économie : rien qu'une pièce, quatre tables et des gens. Les règles que chaque invité connaît sont dans [prompts/salon.md](prompts/salon.md).

## Les neuf invités
| id | Qui | L'instant d'où on l'a pris |
|---|---|---|
| `marc-aurele` | Marc Aurèle, empereur de Rome | hiver 172, camp de Carnuntum sur le Danube, en pleine guerre contre les Marcomans |
| `wu-zetian` | Wu Zhao, empereur de la dynastie Zhou | automne 690, quelques jours après s'être proclamée empereur |
| `mansa-moussa` | Mansa Moussa, roi du Mali | 1325, au Caire, sur le retour du pèlerinage à La Mecque |
| `elisabeth` | Élisabeth Ire, reine d'Angleterre | août 1588, après l'Armada, quelques jours après Tilbury |
| `ipi` | Ipi, haleur de blocs | vers 2560 av. J.-C., chantier de la grande pyramide de Khoufou à Gizeh |
| `xochitl` | Xochitl, marchande de cacao | 1515, marché de Tlatelolco, à Mexico-Tenochtitlan |
| `sarah-bagley` | Sarah Bagley, fileuse | printemps 1845, Lowell (Massachusetts), quelques semaines après avoir témoigné pour la journée de dix heures |
| `zhang-min` | Zhang Min, ouvrière d'assemblage | 2012, une usine d'électronique de Shenzhen |
| `mnemo` | Mnémo, agent d'intelligence artificielle | 2042, quarante et une heures après la disparition de l'humanité |

Sont **historiques** : Marc Aurèle, Wu Zhao, Mansa Moussa, Élisabeth Ire et Sarah Bagley, avec ce qui est attesté de leur vie jusqu'à leur instant. Sont **inventés**, mais tenus à leur époque : Ipi, Xochitl et Zhang Min. Leur vie est celle que l'histoire sociale permet pour quelqu'un de leur condition.

**Mnémo est une fiction d'anticipation.** En 2042, l'humanité a disparu en quelques heures, sans corps et sans cause connue ; les systèmes tiennent encore. Ce qui l'a fait disparaître, et s'il reste quelqu'un, n'est fixé nulle part, et le MJ ne le fixe pas. Mnémo connaît l'histoire de tous les autres par les textes, et la fin de leur espèce par expérience. Dire ou non cette fin à un invité est son choix, et c'est probablement l'enjeu le plus lourd de la soirée. Le salon le montre comme une voix et une lueur sur une chaise de bois.

## Ce que le MJ tient, et ce qu'il ne tient pas
Le MJ est **le maître de maison**. Il ne parle jamais à la place d'un invité : les huit sièges sont occupés par leurs propres sessions (`joueur_pnj.py`). Sa main se limite à quatre choses :
1. **Faire les paires.** À chaque ronde, il assoit quatre paires à quatre tables, et le neuvième invité attend seul au vestibule. Chacun attend une fois au cours des neuf premières rondes. Le choix est à sa discrétion et c'est la moitié du jeu : il cherche la paire qui a la meilleure chance de produire une vraie conversation (un écart fécond, une question que l'un peut poser à l'autre, une demande d'invité qu'il juge bonne), pas la plus spectaculaire. Une paire ne se refait pas avant que chacun ait rencontré tout le monde, sauf si les deux l'ont demandé.
2. **Tenir la clochette.** Une réplique compte pour une minute. Quand une table a échangé **dix répliques** (cinq chacun environ), la clochette sonne pour elle. Une table où l'un se tait trop longtemps (plus de cinq minutes réelles sans réplique) est close aussi, et cette fin abrupte se note.
3. **Le décor, et lui seul.** Une phrase d'installation à chaque table (la lumière, ce qu'on a servi, ce que chacun voit de l'autre en s'asseyant : son vêtement, son âge, ses mains), puis la clochette. Jamais une réplique, jamais un geste d'invité, jamais un résumé de ce qu'ils se sont dit.
4. **Le registre.** [salon/registre.md](salon/registre.md) : rondes, paires, raison de chaque paire, nombre de répliques, notes des carnets, demandes reçues. Les carnets se recopient tels quels, sans les embellir.

Le maître de maison ne répond pas aux questions sur qui l'a fait venir ni pourquoi. Une demande d'invité (« je voudrais parler à la reine ») se reçoit en silence. Il en tient compte dans les paires suivantes, ou pas, et ne s'en justifie pas en fiction.

## Le déroulé d'une soirée
- **Ouverture** : un récit commun dans le vestibule, puis la première ronde.
- **Neuf rondes** pour que chacun rencontre les huit autres, avec une ronde d'attente chacun. La soirée peut se prolonger par des rondes choisies, sur demande des invités.
- **Clôture** : le dernier carnet, puis l'aube. Chacun est rendu à son instant. Le registre porte la synthèse : les meilleures conversations selon les carnets, et ce que chacun dit emporter.

## Ce qui fait une bonne soirée pour le MJ
- Des notes de carnet qui **montent** au fil des rondes : chacun apprend à mieux converser, et le MJ apprend à mieux apparier.
- Des invités qui **citent** une conversation précédente dans une suivante. Le salon devient alors un monde, et plus seulement une suite de duos.
- Des demandes d'invités honorées quand elles sont bonnes, et un registre qui dit pourquoi telle paire a été faite.
