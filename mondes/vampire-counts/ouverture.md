# La scène d'ouverture — préparée, pas jouée

`ouverture.jsonl` est la première tranche, prête à pousser. Elle ne contient
aucune parole ni aucun geste de PNJ (Règle Zéro) : la chambre, le corps, le
compte, le registre récité, la demande de Sever. Elle se termine en rendant la
main au joueur, sans menu.

## Pousser

Une ligne à la fois, dans l'ordre, par la porte du flux :

```bash
CONSEIL_MONDE=vampire-counts python scripts/append_flux.py --pour teodor '<ligne>'
```

En même temps que l'item `objectif`, écrire l'entrée `la-porte` dans
`etat/objectifs.json`. Puis `journal.scene_courante` : « Teodor éveillé dans sa
chambre, 17 h 04, main rendue. »

## Ce qui est vrai à cette minute (état)

- **17 h 00, 3/11 an 1.** Le maître est dans sa chambre, au-dessus, jusqu'à
  17 h 20 (routine) ; puis il va aux remparts jusqu'à 19 h, puis à **la table de
  19 h à 21 h**, où Teodor a sa place à gauche.
- **Stanca**, la goule qui le suit depuis vingt-cinq ans, attend au seuil de sa
  chambre (presence.json) et le suivra dès qu'il sort. Elle n'est pas dans la
  première tranche : sa première apparition — même un geste — passe par sa
  dépêche. Le mois dernier, elle l'a perdu une heure dans la ville basse et ne
  l'a pas dit au maître (sa tête) ; Teodor l'ignore.
- Sever est à Odorheiu, Nicodim dans sa chapelle : hors de portée.

## Les bifurcations probables, et qui dépêcher

Ne rien écrire d'avance. Quand le joueur bouge :

| Si Teodor… | La scène | On dépêche |
|---|---|---|
| sort de sa chambre | le couloir, Stanca qui l'attend au seuil | `stanca --mode discussion` |
| monte voir le maître | la chambre du maître, le registre sur la table | `anselm --mode discussion` |
| va à la table à 19 h | le repas, les envoyés éventuels, sa chaise à gauche | `anselm`, et `stanca` derrière lui |
| descend à la ville basse ou vers Homorod | la porte, la route, le village | `stanca` (elle le suit) ; Homorod n'a pas encore de visages |
| reste et attend | le temps tourne jusqu'à la table ; la montre avance | rien |

**Horloge dure** : l'aube, vers 7 h. **Échéance de la partie** : Sever, le 15 à 19 h.
