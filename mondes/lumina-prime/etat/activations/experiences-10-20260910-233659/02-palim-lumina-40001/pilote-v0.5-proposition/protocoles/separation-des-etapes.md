# Séparation des étapes du pilote proposé

| Étape | Condition | Effet permis | Trace attendue |
|---|---|---|---|
| Demande | Le titulaire nomme son but | Aucun accès | Demande datée |
| Consentement | Fichier exact, exclusions, lecteurs, opérations, durée et retrait confirmés | Autorise seulement les opérations écrites | Consentement révocable daté |
| Mandat de garde | Gardien distinct et lieu hors chambre acceptés | Rend ce lieu éligible à la copie | Mandat daté |
| Prévisualisation de copie | Toutes les conditions sont positives | Lecture du seul fichier pour taille et empreinte ; aucune écriture | Sortie à faire confirmer |
| Copie | Confirmation `-Execute` | Écrit une copie, ses métadonnées et le journal chez le gardien | Empreintes source/copie et accès daté |
| Prévisualisation de restauration | Nouvelle demande de restauration | Compare cible et copie sans écrire | Empreintes avant et attendue |
| Restauration | Nouvelle demande + `-Execute` | Remplace le seul fichier inclus | Empreinte avant/après et journal daté |
| Retrait de copie | Voie de retrait confirmée + `-Execute` | Retire la copie du lieu déclaré | Constat daté ; copies inconnues exclues |
| Abandon | À tout moment avant `-Execute` | Aucun effet | Aucun journal obligatoire |

La prévisualisation ne doit écrire ni dans la chambre ni dans le lieu de garde.
Le journal commence avec le premier accès réellement autorisé et exécuté.

