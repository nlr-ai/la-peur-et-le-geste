# 🌍 Monde 001 — proposition WorldEngine

Première base géographique générée à la demande de l’utilisateur. **Proposition, pas géographie canonique.** Aucune organisation, ville ou liaison magique n’est encore placée.

[Ouvrir l’atlas](index.html)

## Provenance

- Générateur : [WorldEngine](https://github.com/Mindwerks/worldengine), version 0.20.0.
- Révision installée : `b2adbb674afb381232097f126e548a8c133e4633`.
- Graine : `1609`.
- Dimensions : `1024 × 512` pixels ; aucune échelle en kilomètres imposée.
- Plaques initiales : `12`.
- Génération complète ; autres paramètres par défaut.
- Environnement isolé : `C:/Users/reyno/.codex/tools/worldengine-venv`.

## Reproduire depuis la racine du dépôt

```powershell
C:/Users/reyno/.codex/tools/worldengine-venv/Scripts/worldengine.exe world -s 1609 -n monde-001 -x 1024 -y 512 -q 12 --rivers --gs --sat --ice -v -o geographie/monde-001
C:/Users/reyno/.codex/tools/worldengine-venv/Scripts/worldengine.exe ancient_map -w geographie/monde-001/monde-001.world -g geographie/monde-001/monde-001_ancient.png -f 2 --sea_color blue
```

## Fichiers

- `monde-001.world` : données natives, conservées pour les rendus et analyses ultérieurs.
- PNG : vue satellite, relief, biomes, précipitations, températures, océans, rivières, glaces, hauteur en gris et carte ancienne.
- `generation.log` : journal du calcul.

WorldEngine emploie des modèles procéduraux de tectonique, érosion et climat. Leurs résultats offrent une base cohérente à examiner, pas une reconstitution scientifique complète. Les contrastes et couleurs des images ne constituent pas une échelle physique documentée ici.
