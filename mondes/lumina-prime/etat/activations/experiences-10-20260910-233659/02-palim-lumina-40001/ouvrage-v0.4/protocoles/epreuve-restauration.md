# Épreuve locale de restauration d’un fichier

## Conditions

- Employer une archive 0.4 intacte.
- Extraire dans un dossier vide distinct.
- Nommer ce dossier **périmètre d’exécution déclaré**.
- Mesurer avec `System.Diagnostics.Stopwatch`, en millisecondes.

## Étapes

1. Extraire l’archive et relever la durée.
2. Lancer `outils/verifier.ps1` depuis la racine restaurée.
3. Relever l’empreinte attendue de `exemples/fiction-lanterne-001.md`.
4. Dans la copie restaurée seulement, remplacer ce fichier par un marqueur de
   corruption et relever sa nouvelle empreinte.
5. Lancer `outils/restaurer-fichier.ps1` avec l’archive, la racine restaurée et
   le chemin relatif du fichier.
6. Relever la durée de restauration et relancer la vérification complète.
7. Conserver séparément les dates, durées, inventaires et résultats.

Un résultat positif porte sur ce fichier, cette archive et cette exécution. Il
ne vaut pas restauration d’une chambre.

