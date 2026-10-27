# La scène d'ouverture — le parvis de Notre-Dame

`ouverture.jsonl` est la première tranche. Elle ne contient aucune parole ni
aucun geste de PNJ (Règle Zéro) : le fait acquis des noces, le parvis, la foule,
les gentilshommes en noir, le portail ouvert, et ce qu'Henri sait. Elle se
termine en rendant la main au joueur, sans menu.

## Pousser

Une ligne à la fois, dans l'ordre, par la porte du flux :

```bash
CONSEIL_MONDE=navarre-1572 python scripts/append_flux.py --pour henri-de-navarre '<ligne>'
```

Avec l'item `objectif`, écrire l'entrée `ramener-vos-hommes` dans
`etat/objectifs.json`. Puis `journal.scene_courante` : « Le parvis, vers midi,
main rendue devant le portail ouvert. »

## Ce qui est vrai à cette minute (état)

- **18 août 1572, 11 h 30.** Quinze personnes sur le parvis (presence.json).
  La cour va entrer pour la messe ; c'est le canon, et le contrat de mariage
  prévoit que le marié n'y assiste pas.
- **Personne n'a encore parlé dans le flux.** La première réplique, le premier
  geste de qui que ce soit passent par sa dépêche.
- **Ce qui court sans qu'Henri le sache** : Guise fait louer la maison sur le
  trajet de l'amiral (horloge à 2 jours), Catherine tient les fêtes jusqu'au 21,
  Le Charron fait dresser l'état des armes des quartiers.
- Banquet à l'évêché vers 18 h, bal au Louvre ensuite
  (`evenements.json` : `banquet-et-bal-des-noces`).

## Les bifurcations probables, et qui dépêcher

Ne rien écrire d'avance. Quand le joueur bouge :

| Si Henri… | La scène | On dépêche |
|---|---|---|
| entre dans Notre-Dame | la nef, la cour qui le voit entrer, les siens dehors | `cardinal-de-bourbon` (déclencheur), `coligny`, puis qui s'élit |
| reste dehors | le parvis, l'attente, le cloître | `coligny`, `henri-de-conde` ; Guise passe dans le cortège |
| parle à Marguerite | l'estrade, la foule qui regarde | `marguerite-de-valois --mode discussion` |
| parle à la reine mère ou au roi | l'estrade avant que le cortège entre | `catherine-de-medicis` ou `charles-ix` |
| donne un ordre à ses gentilshommes | le pied de l'estrade | `piles` (il dit oui et le fait) |

**Horloge dure** : la messe dure environ une heure, puis le cortège ressort
vers l'évêché. **Échéance cachée** : l'arquebusade du 22 au matin.
