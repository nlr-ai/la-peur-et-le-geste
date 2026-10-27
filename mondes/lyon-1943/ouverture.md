# La scène d'ouverture — l'imprimerie Chabert

`ouverture.jsonl` est la première tranche. Elle ne contient aucune parole ni
aucun geste de PNJ (Règle Zéro) : le fait acquis de la feuille de route posée
sur le marbre, l'atelier qui ferme, ce que Marcel sait et ce qu'il risque. Elle
se termine en rendant la main au joueur, sans menu.

## Pousser

Une ligne à la fois, dans l'ordre, par la porte du flux :

```bash
CONSEIL_MONDE=lyon-1943 python scripts/append_flux.py --pour marcel-rivoire '<ligne>'
```

Avec l'item `objectif`, écrire l'entrée `la-feuille-de-route` dans
`etat/objectifs.json`. Puis `journal.scene_courante` : « L'imprimerie, fin de
journée, main rendue devant la feuille de route. »

## Ce qui est vrai à cette minute (état)

- **Vendredi 5 mars 1943, 18 h 30.** Trois personnes dans l'atelier
  (presence.json) : Marcel, le patron Gaston Chabert, le compositeur Louis
  Perret. Les autres ouvriers sont partis.
- **Personne n'a encore parlé dans le flux.** La première réplique, le premier
  geste de qui que ce soit passent par sa dépêche.
- **Le couvre-feu est à minuit.** Le premier convoi part des Brotteaux le
  dimanche 7 mars.
- **Ce qui court sans que Marcel le sache** : Perret veut le mettre en contact
  avec Marchal, qui boit au café du Gros Caillou ce soir ; Moulin est à Londres ;
  Barbie installe ses services ; Raymond Aubrac sera arrêté le 15 mars.

## Les bifurcations probables, et qui dépêcher

Ne rien écrire d'avance. Quand le joueur bouge :

| Si Marcel… | La scène | On dépêche |
|---|---|---|
| reste à l'atelier, traîne | l'atelier qui se vide | `louis-perret` (son intention de ce soir), `gaston-chabert` s'il ferme |
| parle au patron | le marbre, la feuille | `gaston-chabert --mode discussion` |
| rentre chez lui | le plateau, la cuisine, la mère qui coud | `louise-rivoire`, puis `jean-rivoire` à son retour des Brotteaux |
| cherche de l'aide ailleurs | le café du Gros Caillou, la rue | qui s'y trouve (presence.py --quartier) |

**Horloge dure** : le départ du dimanche matin. **Échéance cachée** : les
gendarmes passent chez les réfractaires dans les jours qui suivent un convoi.
