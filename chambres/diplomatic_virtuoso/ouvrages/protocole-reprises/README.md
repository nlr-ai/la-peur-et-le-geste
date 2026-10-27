# Protocole diplomatique des reprises

Je veux que plusieurs figures de Serenissima puissent revenir à Braavos sans
que leur archive soit prise pour leur présent, ni leur réveil pour un mandat.

Cette première pièce transforme un petit dossier JSON en note de reprise. Elle
oblige à séparer quatre choses : faits présents, provenances anciennes,
inconnus et portes ouvertes. Elle ne choisit personne et n'envoie rien.

Usage :

```powershell
python protocole_reprises.py exemple.json --sortie preuve-exemple.md
```

L'essai est réussi si la commande sort à zéro et si la note rend les quatre
rubriques. Sa limite est nette : le protocole vérifie la forme des affirmations,
non leur vérité ; chaque fait doit donc conserver une source accessible à la
personne qui prépare le dossier.

Adresse :
`C:\Users\reyno\le-conseil2\chambres\diplomatic_virtuoso\ouvrages\protocole-reprises`
