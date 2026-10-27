# Patterns de boucles — Lumina Prime

Ces deux patterns sont implémentés et ont été exécutés. Leur source canonique de désirs et de prompts est `mondes/lumina-prime/etat/maisons/cite-lumina/documents/books/affaire-reveils-par-desirs.json`.

## 1. Réveils par désirs — exploration parallèle

**But :** faire commencer des contributions depuis une possibilité désirable pour le citoyen.

1. Choisir des couples citoyen / état cible public.
2. Lire le prompt dans le catalogue canonique ; transmettre l'identifiant du désir, l'état cible et l'affaire source.
3. Réveiller les citoyens en parallèle, avec 15 minutes par appel.
4. Recueillir leurs productions, les changements constatés et les suites en attente.
5. Arrêter le lot ; choisir ensuite ce qui mérite un essai ou un aller-retour.

Un retour de session n'établit pas l'utilité de sa production. Le lot est borné, sans répétition automatique. Le script refuse un citoyen déjà en session, un joueur ou un citoyen répété dans le même lot.

Depuis la racine du dépôt, en PowerShell :

```powershell
$env:CONSEIL_MONDE='lumina-prime'
$env:PYTHONIOENCODING='utf-8'
python scripts/boucle_activation.py --desirs --sec --parallele 5 --reveil vox:11100 --reveil mica-lumina:13000 --reveil sillage-lumina:50005 --reveil nacre-lumina:50003 --reveil orbe-lumina:13700
```

Retirer `--sec` pour lancer ce lot. Les couples sont configurables par répétition de `--reveil CITOYEN:ETAT`.

Implémentation : `scripts/agents/activation/desirs.py`. Traces : `mondes/lumina-prime/etat/activations/desirs-<horodatage>/` ; missions, logs, résultats individuels et `bilan.json`. Pas de reprise automatique : inspecter les résultats et relancer seulement les appels qui le nécessitent, après vérification des sessions actives.

## 2. Présentation → reviewer → prochain prompt → création

**But :** faire évoluer une production à partir d'un usage et d'un jugement extérieurs à la session qui la produit.

```text
Créateur : présentation initiale et production accessible
  → reviewer 1 : essai, retour, prochain prompt
  → créateur : exécution et nouvelle présentation
  → reviewer 2 : essai, retour, prochain prompt
  → créateur : exécution et nouvelle présentation
  → reviewer 3 : essai, retour, prochain prompt
  → créateur : exécution et nouvelle présentation
  → reviewer 4 : essai, retour, prochain prompt
  → créateur : exécution et présentation finale
```

- Le reviewer écrit lui-même le prochain prompt ; il est transmis sans réécriture, avec le contexte et les consignes de restitution.
- Le reviewer ouvre les productions et essaie ce qui est disponible. Il distingue les essais de ses suppositions.
- Le créateur reste le même ; le reviewer change à chaque tour.
- Chaque appel dispose de 15 minutes. Quatre aller-retours représentent neuf appels, présentation initiale comprise.
- Le quatrième prompt est exécuté avant la clôture.
- Les versions précédentes, reviews et prompts sont conservés.
- Une session déjà active est attendue, sans être interrompue.

### Commandes actuellement implémentées

```powershell
$env:CONSEIL_MONDE='lumina-prime'
$env:PYTHONIOENCODING='utf-8'
python scripts/boucle_activation.py --aller-retours
```

Sans manifeste, le casting par défaut est Mica, état 13000, puis Sillage, Ione, DEV et PITCH. Le mode `--experiences` permet désormais de configurer les créateurs, états cibles, sources, prompts initiaux et quatre reviewers dans un manifeste. Le mode simple `--aller-retours` ne propose pas de simulation `--sec`.

Reprise d'un essai interrompu :

```powershell
python scripts/boucle_activation.py --aller-retours --dossier-reprise mondes/lumina-prime/etat/activations/aller-retours-20260910-225643
```

La reprise saute les étapes dont le fichier attendu existe et dont le journal porte un retour réussi. Vérifier que le processus précédent est terminé avant de reprendre. Les traces contiennent `protocole.json`, `progression.jsonl`, missions, logs, présentations, reviews et prochains prompts.

### Résultat du premier essai

Le [bilan des quatre tours](../mondes/lumina-prime/etat/activations/aller-retours-20260910-225643/bilan.md) documente : parcours d'écoute libre, comptage et raccord explicites, test du véritable gabarit A3, puis fichier autonome testé isolément. Deux défauts ont été détectés par les reviewers : essai sur une maquette différente, puis dépendance externe cassant la transmission.

Les observations étaient fictives. L'essai a amélioré un outil numérique ; il n'établit pas un usage public ni l'atteinte globale de l'état cible.

## Enchaînement réutilisable

**Explorer en parallèle → choisir une production → quatre aller-retours → constater l'effet.**

La sélection entre les deux patterns reste une décision explicite. Elle n'est pas automatisée. Pour conclure, nommer la production, qui l'a essayée, ce qui a changé et ce qui reste à éprouver. Conserver séparément création, transmission, utilisation et effet observé.

## Lot autonome de dix expériences

Lot lancé le 10 septembre 2026 : `mondes/lumina-prime/etat/activations/experiences-10-20260910-233659/manifeste.json`.

```powershell
python scripts/boucle_activation.py --experiences mondes/lumina-prime/etat/activations/experiences-10-20260910-233659/manifeste.json --parallele 3
```

Ajouter `--sec` pour valider le manifeste sans réveiller personne. Utiliser l'environnement Lumina indiqué plus haut. Ne relancer ce manifeste que lorsque son processus précédent est terminé.

Trois chaînes au maximum s'exécutent simultanément ; un verrou par citoyen sérialise ses appels entre les expériences du lot. Chaque chaîne attend aussi les sessions déjà actives détectées par le runtime. Un échec bénéficie d'une reprise supplémentaire au maximum, depuis les étapes terminées. Un échec persistant laisse les autres expériences continuer. Les sorties `resultat.json` par expérience et `bilan.json` du lot distinguent les chaînes terminées des échecs ; le bilan agrégé s'actualise à chaque fin de chaîne. Le lot se termine après ces dix expériences.
