# Proposition de pilote 0.5 — un fichier de chambre, aucun accès engagé

Statut : **prêt à soumettre, non envoyé, non autorisé, non exécuté**.

Aucun titulaire consentant, gardien distinct ni mandat sur un lieu de garde
n’est établi dans les faits accessibles à Palim. Aucun fichier de chambre n’a
donc été nommé, lu, copié, empreinté ou modifié.

## Ordre proposé

1. Le titulaire remplit `dossiers/dossier-pilote-vide.json` lui-même ou en
   confirme chaque champ.
2. Le gardien distinct accepte séparément son mandat et son lieu de garde.
3. Un opérateur contrôle le dossier sans ouvrir la chambre.
4. Seulement si le contrôle est positif, il prévisualise la copie sans écriture.
5. Le titulaire peut abandonner sans effet, ou autoriser explicitement la copie.
6. Toute restauration exige une nouvelle demande et commence par une
   prévisualisation sans écriture.

## Commandes

Contrôle et prévisualisation sans écriture :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode PrevisualiserCopie -Dossier .\dossiers\dossier-pilote-rempli.json
```

Copie, uniquement après contrôle et confirmation explicite :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode Copier -Dossier .\dossiers\dossier-pilote-rempli.json -Execute
```

Prévisualisation d’une restauration, sans écriture :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode PrevisualiserRestauration -Dossier .\dossiers\dossier-pilote-rempli.json
```

Restauration, seulement après nouvelle demande explicite du titulaire :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode Restaurer -Dossier .\dossiers\dossier-pilote-rempli.json -Execute
```

Retrait de la copie du lieu de garde déclaré :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode RetirerCopie -Dossier .\dossiers\dossier-pilote-rempli.json -Execute
```

Ces commandes ne créent ni mandat, ni consentement, ni garantie. Le script
refuse avant lecture du fichier si le dossier ne les établit pas.

