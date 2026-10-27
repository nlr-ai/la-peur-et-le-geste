# La rive 0.4 — paquet autonome de reprise

Point d’entrée : `reprise/fiche-reprise.md`.

Ce paquet contient l’œuvre, une fiche de transmission, un exemple fictif, son
registre de provenance, un protocole de restauration et deux outils PowerShell.
Il ne dépend d’aucun fichier extérieur pour être lu ou pour vérifier ses
empreintes et ses références déclarées.

Commandes à lancer depuis la racine restaurée :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\verifier.ps1 -Root .
```

Pour restaurer un fichier depuis l’archive d’origine :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\restaurer-fichier.ps1 `
  -Archive <chemin-de-l-archive> -Root . `
  -RelativePath exemples/fiction-lanterne-001.md
```

Le terme employé pour les essais est **périmètre d’exécution déclaré**. Aucune
garde reconnue, aucun service de la cité et aucune restauration de chambre ne
sont présumés.

