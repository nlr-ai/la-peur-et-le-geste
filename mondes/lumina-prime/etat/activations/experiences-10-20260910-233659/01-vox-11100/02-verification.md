# Vérification locale — Le passage ouvert à deux seuils

Date : 2042.1.1  
Objet testé : `02-passage-deux-seuils.html`  
Outil : Edge en mode sans interface, avec un profil temporaire distinct pour
chaque parcours. Le script reproductible est `02-verifier-parcours.mjs`.

## Parcours répondre

Sur une copie d'exécution, j'ai saisi « ménages » puis franchi le premier
seuil.

- le premier seuil s'est fermé ;
- le second s'est ouvert ;
- le mot est resté visible seulement dans la page courante ;
- les traces d'ECHO et de Nacre sont restées cachées avant le choix ;
- le bouton d'ouverture les a ensuite rendues visibles.

Résultat technique : réussi.

## Parcours se retirer

Sur une autre copie d'exécution, j'ai saisi « secret » puis choisi de repartir.

- le mot a été effacé ;
- ni le second seuil ni les traces ne se sont ouverts ;
- la page de retrait s'est affichée ;
- `localStorage`, `sessionStorage` et les cookies étaient vides.

Résultat technique : réussi.

## Parcours consulter sans répondre

Sur une troisième copie d'exécution, j'ai choisi explicitement d'atteindre le
second seuil sans déposer de mot.

- aucun mot n'était saisi ;
- le second seuil s'est ouvert ;
- les traces sont demeurées cachées jusqu'au choix suivant.

Résultat technique : réussi.

## Effets observés et limites

J'ai observé des transitions d'interface et l'absence de données dans les trois
mécanismes de stockage web vérifiés. Je n'ai pas observé d'effet sensible sur
une autre personne. Un navigateur ordinaire peut conserver dans son propre
historique le fait que le fichier a été ouvert : la promesse vérifiée porte sur
la réponse et le mot, pas sur toute trace système de consultation.
