# Carte des Highlands

Même table interactive que Westeros : vignette autour d'Inverness, carte entière, zoom, lieux et pièces du siège. Le fond est figé dans `geo.js` et ne demande aucun accès réseau au jeu.

Les côtes et îles sont extraites de [Natural Earth, terres au 1:10m](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-land/), données du domaine public. Projection locale équirectangulaire corrigée à 57,5° N ; nord en haut. Le cadrage est géographique, sans frontière administrative ou territoire de clan présumé.

Inverness et les repères géographiques secondaires ont des coordonnées réelles arrondies. Craigh na Dun, les trois lieux locaux, Leoch et Cranesmuir ont seulement des positions graphiques indicatives regroupées près d'Inverness : ni canon, ni sites de tournage, ni distances de trajet. Le titre de la grande carte signale cette limite. Aucune route ni connaissance de PJ n'est créée ; les tables d'état restent l'autorité du jeu.

Rivières et lacs : Natural Earth 1:10m, réseau principal et complément européen. La couverture est généralisée, pas exhaustive des petits cours d'eau. Les traits sont épaissis pour la lecture.

Relief : [Terrain Tiles / Mapzen, hébergées sur AWS](https://registry.opendata.aws/terrain-tiles/), tuiles Terrarium au zoom 7. Deux bandes d'altitude mesurée : collines à partir de 300 m, montagnes à partir de 700 m, obtenues par lissage gaussien des altitudes puis interpolation des isolignes, et découpées à la côte. Il s'agit d'un relief simplifié, pas de limites de massifs ni de données de franchissabilité. Voir [l'attribution des sources Terrain Tiles](https://github.com/tilezen/joerd/blob/master/docs/attribution.md).

Régénération : `python mondes/outlander/carte/generer.py` (Python, Shapely, NumPy, Pillow et ContourPy). Les sources sont mises en cache local dans les fichiers `*-source.geojson` et `terrain-source/`. Le jeu reste autonome et ne télécharge rien à l'exécution.

Repères Fraser : Lallybroch (domaine familial, position fictive indicative), Beauly et château de Beaufort (repères géographiques arrondis, aucun contrôle de ville ni route de jeu ajouté). Beaufort désigne le siège de Lovat dans la fiction ; le bâtiment actuel est postérieur à 1743. Source : https://static.visitscotland.com/site/vs/1.3.58/see-do/attractions/tv-film/outlander/itinerary/

Détail Inverness : six axes de déplacement schématiques, douze repères locaux et cours de Ness/Nairn simplifiés. Ces axes situent les destinations sans attester une chaussée précise en 1743 ; ils ne créent pas de route, durée ni franchissement dans l’état de jeu. Culloden est nommé comme lande, sans bataille future ni canal calédonien anachronique. Positions arrondies ; couverture non exhaustive. Sources : https://www.visitscotland.com/wsimgs/Inverness-Cycling-Routes-Map_439339504.pdf et https://www.visitscotland.com/things-to-do/attractions/free/highlands .
