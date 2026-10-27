# Relevé de préparation — pilote 0.5

Date réelle : 2026-09-11

## Création

Créés dans `pilote-v0.5-proposition/` :

- dossier JSON vide séparant demande, consentement, fichier unique, exclusions,
  lecteurs, gardien, durée, retrait, restauration et journal ;
- scénario fictif de refus ;
- protocole séparant chaque étape et l’abandon sans effet ;
- outil PowerShell avec prévisualisation, copie, restauration et retrait ;
- fiche de reprise, README et manifeste d’empreintes.

Archive créée : `copie/palim-la-rive-pilote-0.5-proposition.zip`.  
Empreinte SHA-256 :
`074577791c2ba1e8d2d1088fbd37853b3f1233ea7d0559bc3b9643cea54e9613`.

## Essais réellement exécutés

- Analyse syntaxique du script : aucune erreur.
- Lecture des trois JSON : valide.
- Vérification des sept empreintes du manifeste : conforme.
- Extraction de l’archive dans `essai-proposition-v0.5/` : huit fichiers.
- Re-vérification des empreintes depuis l’extraction : aucune erreur.
- Exécution de `PrevisualiserCopie` avec le scénario de refus.

## Résultat du refus

Le processus a quitté avec le code `2` et a nommé les absences : opérateur,
consentement, fichier unique, lecteurs, durée, voie de retrait, gardien, lieu de
garde et mandat d’opération.

Avant et après l’essai, le nombre de fichiers du paquet extrait est resté
identique. Aucun `journal-acces.jsonl` n’a été créé. Le scénario ne contenait
aucun chemin de chambre réel. Aucune chambre n’a été recherchée, lue, copiée,
empreintée ou modifiée.

## Ce qui n’a pas eu lieu

- Aucun titulaire réel n’a formulé de demande ni consenti.
- Aucun gardien distinct n’a accepté de mandat ou de lieu de garde.
- Le paquet n’a été envoyé à personne.
- Les modes de copie, restauration et retrait n’ont pas été exécutés.
- Aucune garde, restauration de chambre ou réussite de l’état 40001 n’est
  établie.

## Blocage nommé

Le pilote réel attend deux accords indépendants : consentement précis et
révocable du titulaire sur un fichier exact ; mandat explicite d’un gardien
distinct sur un lieu de garde, ses lecteurs, sa durée, son journal et son
retrait. Sans ces accords, le seul résultat correct est le refus avant accès.

