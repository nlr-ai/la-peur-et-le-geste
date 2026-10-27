# Icônes des actions et objets

Dessins SVG originaux pour La peur et le geste. Les 60 actions ont une silhouette de menuiserie et un indice du sens initial (assemblage, trajet, contrôle, rupture). Les 14 ressources ont aussi leur pictogramme de chantier : clous, bons de livraison, gabarits, chaux, huisseries, carreaux, sable, huile, outils, pointes, poudre, sonnette, cotes et agrément. Le manifeste conserve leur nom couvert, leur sens initial et leur unité réelle sans inventer de conversion. Les identifiants et chemins sont conservés. La première version est conservée dans actions-resistance-original.py. Source des types : fichiers de contenu Modern Front. Les 60 actions viennent de resistance_actions.json, sans ajout ni modification de règles ; une action propre au jeu, Organiser une réunion, s’y ajoute depuis actions_locales.py. Les 67 icônes de mobilier et de décor ont été retirées ; les biens sont réduits à 13 types principaux, sans variantes de marque, de bijou, de pièce, de calibre ou de radio. Seize termes de présence, de contrôle et d’infrastructure sont ajoutés comme propositions dans lexique.py. Les noms de couverture sont des propositions graphiques ; les clés source restent inchangées. Ce sont des pictogrammes, pas des reproductions historiques précises de modèles ou de marques.

- `index.html` : planche autonome, recherche, filtres, fond clair/sombre et tailles 64/32/24 px.
- `svg-clair/` : les 104 dessins littéraux, raccordés au langage clair du tableau.
- `index-clair.html` et `objets-clairs.sprite.svg` : planche et sprite en langage clair.
- `svg/` : un fichier autonome par type, action ou terme, transparent, viewBox 0 0 64 64.
- `manifest.json` : identifiants stables, libellés, chemins et clés des données source.
- `objets.sprite.svg` : symboles utilisables avec `<svg><use href="objets.sprite.svg#action-print_tracts"/></svg>`.
- `generer.py` : génération reproductible depuis les fichiers source locaux.

Le trait utilise `currentColor` (2 unités). En SVG inline ou sprite, la couleur suit la propriété CSS `color`; dans une balise `img`, elle reste noire. Les animaux ne font pas partie du catalogue d’objets. Les fichiers sont créés dans le nouveau dépôt, sans modification de Modern Front. Les icônes ne changent pas la simulation ; leur présence ne signifie pas qu’une action est actuellement disponible.
