# Preuve d’épreuve autonome — « La rive » 0.4

Outil de mesure : `System.Diagnostics.Stopwatch`  
Unité : milliseconde (`ms`)  
Périmètre d’exécution déclaré final : `restauration-v0.4-finale/`

## 1. Création de l’archive

- Source : `ouvrage-v0.4/`, dix fichiers dont `manifest.json`.
- Première création : 2026-09-10T23:53:09.9269756+02:00.
- Durée : 594,249 ms.
- Une première extraction a pris 203,900 ms. Les empreintes, JSON et références
  étaient conformes, mais l’outil de restauration comportait une erreur
  d’analyse sur une chaîne accentuée.
- Première tentative de restauration : **échouée** ; le marqueur de corruption
  est resté en place. Aucun succès n’est attribué à cette tentative.
- Correction de l’outil et mise à jour de l’archive :
  2026-09-10T23:54:31.1592961+02:00, en 753,160 ms.
- Empreinte de l’archive finale :
  `0c7aabcff73709e0b7c6f3489a8044b7e280c5a0c30a0943d89d1081686ceff8`.

## 2. Usage local de l’archive finale

- Nouveau dossier vide créé : `restauration-v0.4-finale/`.
- Début d’extraction : 2026-09-10T23:54:56.4853540+02:00.
- Durée d’extraction : 383,874 ms.
- Contrôle initial : 69,662 ms.
- Résultat : `OK fichiers=9 json=2 references=10`.
- Références manquantes consignées : **aucune**.

Le manifeste ne se donne pas sa propre empreinte afin d’éviter une dépendance
circulaire ; il suit les neuf autres fichiers. Les dix références déclarées,
dont le manifeste lui-même, se résolvent depuis la racine restaurée.

## 3. Corruption simulée

- Fichier choisi : `exemples/fiction-lanterne-001.md`.
- Empreinte attendue :
  `7bba9688830857f7a3ef154d2e6d9be9c7451a7072868d634cf71b2fe5505ee1`.
- Remplacement par un marqueur :
  2026-09-10T23:55:13.7393081+02:00.
- Empreinte corrompue :
  `0cc99e90224a228519c152713bf846b9e00f52546fcc15190c735a8af93d648b`.
- Contrôle observé :
  `ERREUR Empreinte différente: exemples/fiction-lanterne-001.md`.

Seule la copie dans le périmètre d’exécution déclaré a été modifiée. La source
et l’archive sont restées intactes.

## 4. Restauration réellement exécutée

- Début : 2026-09-10T23:55:13.8233517+02:00.
- Commande :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\restaurer-fichier.ps1 `
  -Archive ..\copie\palim-la-rive-0.4.zip -Root . `
  -RelativePath exemples/fiction-lanterne-001.md
```

- Durée : 36,740 ms.
- Résultat de l’outil :
  `RESTAURE exemples/fiction-lanterne-001.md`.
- Empreinte après :
  `7bba9688830857f7a3ef154d2e6d9be9c7451a7072868d634cf71b2fe5505ee1`.
- Retour à l’empreinte attendue : **oui**.

## 5. Résultat final observé

- Vérification complète après restauration : 26,571 ms.
- Résultat : `OK fichiers=9 json=2 references=10`.
- Le fichier choisi a réellement été restauré depuis l’archive finale.
- Aucune référence déclarée n’est manquante.

Cette preuve porte sur un fichier d’une maquette locale et sur cette exécution.
Elle ne prouve ni garde reconnue, ni persistance après panne d’un service, ni
restauration d’une chambre, ni état 40001 atteint.

