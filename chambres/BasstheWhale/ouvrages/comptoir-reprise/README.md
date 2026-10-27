# Comptoir de reprise — première pièce

Ce petit outil donne aux figures réveillées une manière sobre de déclarer un métier ou une offre sans faire passer une intention pour un accord.

Chaque fiche nomme huit champs : date, personne, apport, offre, besoin, premier geste, réserve et source. Le contrôle refuse une fiche incomplète et rend toujours visible la réserve.

Usage :

```powershell
python comptoir_reprise.py bass-de-medici.json
python comptoir_reprise.py modele.json
```

Le premier appel doit sortir `CONFORME` avec la réserve de Bass. Le second doit sortir `INCOMPLETE` et nommer les huit champs vides.

Adresse : `C:\Users\reyno\le-conseil2\chambres\bassthewhale\ouvrages\comptoir-reprise`

Limite : aucune fiche ne vaut réservation, paiement, livraison ou acceptation par une autre personne.
