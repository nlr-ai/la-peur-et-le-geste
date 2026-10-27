# Rues et chemins de Braavos — premier relevé

Relevé documentaire du 10 septembre 2026, demandé par le joueur pour commencer le premier poste de la liste de construction. Aucun déplacement de personnage ni travaux physiques ne sont déclarés par ce relevé.

## Existant vérifié

- `monde/braavos.rues.json` contient 161 tronçons : 57 rues, 18 ruelles, 80 escaliers et 6 tronçons de quai. Les 156 sommets utilisés par ces tronçons forment une seule composante connexe en lecture non orientée.
- Les 13 autres sommets sont des repères nommés, sans arête explicite vers les tronçons. Cette absence de raccordement dans le fichier ne prouve pas une coupure physique : les repères peuvent être des annotations.
- `monde/braavos.bati.json` contient 67 volumes ; `monde/braavos.interieurs.json` décrit 34 salles. Leurs notices indiquent une copie provisoire de Peyredragon.
- `etat/personnages.json` situe 77 personnages à Braavos. Le manifeste des corps générés annonce 795 corps : ce nombre ne doit pas être confondu avec celui des personnages.
- `etat/presence.json` conserve 33 positions résolues dans sept salles de Braavos, mais elles proviennent de présences périmées : archives (9), bourg (7), Table Peinte (7), forge (4), quai (3), antichambre (2), officine (1). Elles orientent une vérification ; elles ne prouvent pas une occupation actuelle.

## Parcours prioritaires calculés

Chemins les plus courts dans les liaisons déclarées de `etat/chemins.json`, lues dans les deux sens. Les minutes sont les coûts du modèle, pas des durées mesurées en déplacement réel.

| Départ | Arrivée | Minutes du modèle | Parcours déclaré |
|---|---|---:|---|
| quai | bourg | 5 | braavos-quai → braavos-bourg |
| bourg | cuisines | 12 | braavos-bourg → braavos-baraques → braavos-porte-dragon → braavos-cour → braavos-cuisines |
| bourg | forge | 12 | braavos-bourg → braavos-baraques → braavos-porte-dragon → braavos-cour → braavos-forge |
| bourg | archives | 19 | braavos-bourg → braavos-baraques → braavos-porte-dragon → braavos-cour → braavos-tambour-de-pierre → braavos-archives |
| bourg | officine | 15 | braavos-bourg → braavos-baraques → braavos-porte-dragon → braavos-chemin-ronde → braavos-tour-dragon-mer → braavos-roukerie → braavos-officine |

## Premier travail à réaliser sur les accès

1. Vérifier quai–bourg, puis bourg–cuisines et bourg–forge, dans la géométrie servie, depuis les véritables entrées. Ces parcours relient accueil, approvisionnement et production.
2. Distinguer marche et transport de biens. La présence de 80 tronçons classés escalier interdit de conclure à la circulation de chariots à partir de la seule connexité.
3. Pour chaque accès, relever porte, seuil, pente, largeur et obstacles ; conserver les liaisons déjà utilisables. Une distance à la rue ne suffit pas à autoriser un raccordement à travers un mur ou un dénivelé.
4. Une intervention sera définie seulement sur une rupture observée : emplacement, usage empêché, réparation ou construction nécessaire, matière, responsable volontaire et condition d’arrêt.

## État du poste

**Commencé : relevé documentaire établi.** Aucun tronçon nouveau n’est encore justifié par une rupture constatée. Restent à vérifier les accès dans le rendu et les trajets réels, puis à chiffrer les interventions nécessaires.

## Sources

- [monde/braavos.rues.json](C:/Users/reyno/le-conseil2/monde/braavos.rues.json)
- [monde/braavos.graph.json](C:/Users/reyno/le-conseil2/monde/braavos.graph.json)
- [monde/braavos.bati.json](C:/Users/reyno/le-conseil2/monde/braavos.bati.json)
- [monde/braavos.interieurs.json](C:/Users/reyno/le-conseil2/monde/braavos.interieurs.json)
- [monde/braavos.gens.json](C:/Users/reyno/le-conseil2/monde/braavos.gens.json)
- [etat/chemins.json](C:/Users/reyno/le-conseil2/etat/chemins.json)
- [etat/personnages.json](C:/Users/reyno/le-conseil2/etat/personnages.json)
- [etat/presence.json](C:/Users/reyno/le-conseil2/etat/presence.json)
- [plans/braavos.json](C:/Users/reyno/le-conseil2/plans/braavos.json)
