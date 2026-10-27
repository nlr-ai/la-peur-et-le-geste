# Scénario de refus

Le dossier `dossiers/scenario-refus.json` représente une demande fictive sans
consentement et sans gardien mandaté. Le contrôleur doit s’arrêter avant de
chercher un chemin de chambre, de tester son existence ou d’en calculer
l’empreinte.

Commande :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\pilote-fichier.ps1 `
  -Mode PrevisualiserCopie -Dossier .\dossiers\scenario-refus.json
```

Résultat attendu : lignes `BLOQUE`, aucun journal créé, aucune lecture de
chambre, aucune copie et aucune modification. L’abandon laisse donc le monde
sans effet.

