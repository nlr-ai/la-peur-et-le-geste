# Atelier de développement de Barralfond

L'atelier relie une affaire à une expérience exécutable, à ses sources et à ses
résultats. La première expérience raccordée est **90312 : comparer le ralliement
avec et sans arbitre**, sur le moteur historique conservé dans le dépôt.

## Des noms lisibles

Les noms de travail ci-dessous sont affichés dans la commande `equipe` et dans le
brief des membres de Barralfond. Les identifiants des personnages, les canaux et
les mémoires restent les mêmes.

| Nom de travail | Responsabilité |
|---|---|
| Nicolas — Responsable du projet | Choisir le résultat utile et les critères de livraison |
| Sarn — Historien | Retrouver les décisions et les expériences précédentes |
| Bren — Analyste du code | Identifier les causes et les vrais points d'appel |
| Ygga — Développeuse | Produire une modification et un essai reproductible |
| Toll — Testeur | Vérifier les résultats bruts et contredire les conclusions fragiles |
| Wenna — Documentaliste | Rendre le résultat et la prochaine étape compréhensibles |

La Souche devient **Tableau des travaux**, l'Établi **Développement**, le Bassin
noir **Banc de tests**, l'Arbre des Âges **Historique Git** et le Lit des Racines
**Analyse du code** dans ce vocabulaire de travail. Les lieux de fiction et les
anciens chemins ne sont pas renommés.

## Utilisation

Depuis la racine du dépôt :

```powershell
python scripts/atelier.py equipe
python scripts/atelier.py dossier 90312
python scripts/atelier.py essayer 90312 --profil court
python scripts/atelier.py resultat 90312
python scripts/atelier.py historique 90312
```

Le profil `court` demande 30 hommes, une seconde simulée et une limite de
60 secondes réelles par variante. Il vérifie la chaîne technique ; il est trop
court pour démontrer un effet sur le ralliement.

```powershell
python scripts/atelier.py essayer 90312 --profil reference
python scripts/atelier.py essayer 90312 --effectif 100 --duree 120 --limite 90
python scripts/atelier.py resultat 90312 --json
```

Le profil `reference` conserve la cible de 1 700 hommes et 600 secondes simulées,
avec une limite de 900 secondes réelles par variante. La durée simulée doit être
un multiple du pas de 0,05 seconde. `--serveur` choisit le serveur de données
(par défaut `http://localhost:3129`). Un seul banc peut s'exécuter à la fois.
Ces commandes lancent des essais techniques locaux, sans appel de modèle.

## Ce qu'un essai conserve

Chaque tentative reçoit son dossier sous `.agents-runtime/atelier/90312/` :

- `demande.json` : item canonique relu, paramètres et identité du travail ;
- `sources.json` et `source/` : provenance Git et copie exacte des sources ;
- `comparer-ralliement.js` : copie du banc exécuté ;
- `donnees/` : réponses du serveur enregistrées par le témoin puis relues par
  la variante avec arbitre ;
- `temoin-commande.json`, `arbitre-commande.json` : commandes et dossiers réels ;
- `temoin.json`, `arbitre.json` : sorties brutes, y compris un fichier vide en échec ;
- `temoin.log`, `arbitre.log`, `journal.jsonl` : progression et erreurs ;
- `resultat.json` : résultat final, même après une erreur ou un délai dépassé.

Le registre SQLite `work_identity` existant conserve l'identité du travail et
numérote ses tentatives. Le verrou du banc est un verrou du système : il est
libéré quand le pilote se ferme. Un enfant encore vivant après une interruption
brutale bloque une nouvelle admission ; le pilote ne le tue pas à partir d'un
ancien PID. Un dépassement normal de délai arrête l'arbre du processus qu'il a
lui-même lancé. Les anciens dossiers restent consultables.

## Ce que le verdict signifie

**Mesure obtenue** exige deux processus terminés normalement, des JSON valides,
la durée simulée réellement atteinte, le même état initial et les mêmes données.
Le témoin doit avoir zéro appel à l'arbitre, la variante doit en avoir au moins
un. Les sources copiées doivent rester identiques pendant les essais.

Le banc compte aussi les appels de `rallier` et les passages qui atteignent sa
décision. Si cette décision n'est pas exercée dans les deux variantes, le verdict
reste **non concluant sur le ralliement**, même avec deux sorties correctes.

Une différence de morts ou de ralliements ne prouve pas à elle seule une
amélioration : retirer l'arbitre affecte plusieurs comportements et le générateur
aléatoire est partagé. L'outil ne clôture aucune affaire et n'intègre aucun code
automatiquement. La livraison du moteur courant demande une vérification propre.

## Raccordement aux agents

`agents/depeche/manuel.py` ajoute le mode d'emploi et le chemin de la dernière
preuve au brief de l'équipe. Pour un appel contextualisé, cette section est
limitée à 90312 ; elle ne détourne pas les agents de leurs autres affaires.
Le parloir et ses reçus restent le moyen de transmettre un résultat et de
constater la remise. Lire le dossier commun n'affirme pas qu'un billet a été reçu.

Les nouveaux modules vivent dans `scripts/agents/atelier/`. La commande publique
`scripts/atelier.py` passe par `agents/expose.py`. Le chemin ancien
`analyse/branchement-90312/rallier.js` reste une entrée compatible vers le banc
`comparer-ralliement.js` ; les sources historiques ne sont pas réécrites.

Pour raccorder une autre expérience, il reste à déclarer son item, ses entrées,
sa commande et ses critères observables. 90312 est la première tranche
fonctionnelle, pas une généralisation déjà démontrée à toutes les affaires.

## Vérification

Les tests de `scripts/tests/test_atelier.py` utilisent des dépôts, des processus
et un registre SQLite temporaires. Ils sont découverts par la garde Python déjà
déclarée dans `scripts/verifier.mjs`.

```powershell
python -m unittest discover -s scripts/tests -p test_atelier.py -v
```
