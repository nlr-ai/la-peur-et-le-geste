# Vérification — le retrait après les traces

Objet : `04-passage-retrait-vrai.html`  
Navigateur : Edge sans interface, profil temporaire  
Parcours : Tab, saisie clavier et activation par Espace  
Script reproductible : `04-verifier-retrait.mjs`

## Parcours exécuté

J'ai saisi « veilles », puis :

1. rejoint et activé « Passer avec ce mot » ;
2. constaté le foyer sur `title-two`, traces fermées ;
3. rejoint et activé « Ouvrir les traces antérieures » ;
4. constaté le foyer sur `traces` et l'annonce « Les traces antérieures sont
   maintenant visibles. » ;
5. constaté la disparition du choix devenu faux « Partir sans les ouvrir » ;
6. appuyé une fois sur Tab depuis les traces ;
7. constaté le foyer sur « Effacer mon mot et repartir » ;
8. activé ce retrait ;
9. constaté le foyer sur `title-away`, la saisie vide et les traces refermées.

Après le retrait, `localStorage`, `sessionStorage` et les cookies étaient
vides. Tous les contrôles de ce parcours ont réussi.

## Noms dans les traces

Le test a également vérifié que les noms ECHO et Nacre n'apparaissent pas dans
la nouvelle région des traces. Ils ont été remplacés par « une première voix »
et « une seconde voix ». Les versions antérieures, qui constituent la trace de
l'expérience, n'ont pas été modifiées.

## Portée

Il s'agit d'un essai local automatisé dans un profil temporaire, non de l'usage
d'une autre personne. Il vérifie le fonctionnement du clavier et de la page ;
il n'établit aucun effet humain, aucune présentation publique et aucune
permission d'exposer les noms associés aux traces.
