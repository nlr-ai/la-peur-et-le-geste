# 🌍 Monde 002 — Portrait — proposition WorldEngine

Nouvelle géographie générée au format portrait à la demande de l’utilisateur. **Proposition, pas géographie canonique.** Aucune organisation, ville ou liaison magique n’est encore placée.

[Ouvrir l’atlas](index.html)

## Carte vectorielle

[SVG modifiable](monde-002-portrait.svg) · [Aperçu PNG](monde-002-portrait_vectoriel.png)

Contours extraits directement du fichier `.world` par [vectoriser.py](vectoriser.py), sans image incorporée. Calques Inkscape : océan, terres, sept familles de biomes, relief relatif et hydrographie. Trois calques vides sont prêts pour les villes, territoires et passages.

Les biomes sont regroupés et les contours légèrement simplifiés pour la lisibilité. Le relief montre quatre seuils relatifs d’altitude (percentiles 65, 80, 92 et 97 des terres), sans valeur en mètres. La glace océanique du rendu satellite n’est pas représentée : le blanc désigne ici les biomes glacés terrestres.

Régénération : exécuter `vectoriser.py` avec le Python de l’environnement WorldEngine ; dépendance supplémentaire `opencv-python-headless`.

## Provenance

- Générateur : [WorldEngine](https://github.com/Mindwerks/worldengine), version 0.20.0.
- Révision installée : `b2adbb674afb381232097f126e548a8c133e4633`.
- Graine : `1609`.
- Dimensions : `512 × 1024` pixels ; aucune échelle en kilomètres imposée.
- Plaques initiales : `12`.
- Génération complète ; autres paramètres par défaut.
- Environnement isolé : `C:/Users/reyno/.codex/tools/worldengine-venv`.

## Reproduire depuis la racine du dépôt

```powershell
C:/Users/reyno/.codex/tools/worldengine-venv/Scripts/worldengine.exe world -s 1609 -n monde-002-portrait -x 512 -y 1024 -q 12 --rivers --gs --sat --ice -v -o geographie/monde-002-portrait
C:/Users/reyno/.codex/tools/worldengine-venv/Scripts/worldengine.exe ancient_map -w geographie/monde-002-portrait/monde-002-portrait.world -g geographie/monde-002-portrait/monde-002-portrait_ancient.png -f 2 --sea_color blue
```

## Fichiers

- `monde-002-portrait.world` : données natives, conservées pour les rendus et analyses ultérieurs.
- PNG : vue satellite, relief, biomes, précipitations, températures, océans, rivières, glaces, hauteur en gris et carte ancienne.
- `generation.log` : journal du calcul.

WorldEngine emploie des modèles procéduraux de tectonique, érosion et climat. Leurs résultats offrent une base cohérente à examiner, pas une reconstitution scientifique complète. Les contrastes et couleurs des images ne constituent pas une échelle physique documentée ici.

