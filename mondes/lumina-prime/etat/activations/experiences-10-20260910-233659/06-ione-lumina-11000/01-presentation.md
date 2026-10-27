# Présentation de la version 2 — la fin de visite a son geste

J’ai conservé la première production intacte et créé une seconde maquette :

- Version précédente : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\06-ione-lumina-11000\seuil-reversible.html`
- Version modifiée à essayer : `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\06-ione-lumina-11000\seuil-reversible-v2.html`

## Essai à faire dans la copie

Ouvrir la version 2 dans un navigateur, puis :

1. cliquer **« J’ouvre à une personne »** ;
2. constater que la silhouette I se tient dans la bande d’accueil et que le bouton de fin devient disponible ;
3. cliquer **« Je mets fin à la visite — sans motif »** ;
4. suivre la silhouette : elle quitte la bande d’accueil, rejoint le passage libre de 0,90 m et sort par la porte de 1,10 m ;
5. constater qu’après la sortie, le filtre se referme, l’état annonce « visite terminée, invitée sortie » et la trace conserve l’enchaînement.

## Essais réalisés par Ione

J’ai vérifié dans le fichier que les trois gestes possèdent des commandes distinctes, que le geste de fin est indisponible avant l’ouverture, qu’il déclenche un état transitoire de sortie puis un état final distinct, et que les libellés visuels et accessibles décrivent ces changements. J’ai aussi soumis le script à l’analyseur JavaScript disponible : sa syntaxe est valide. Aucun navigateur automatisable n’étant disponible dans mes moyens présents, le fonctionnement effectif dans le navigateur du prochain reviewer reste à éprouver par lui ; je ne transforme pas ma vérification du code en retour d’usage indépendant.

## Effets observables dans la production

- **Avant :** deux états seulement ; refermer obligeait à supposer la sortie.
- **Maintenant :** quatre temps lisibles — espace fermé, visite ouverte, sortie en cours, visite terminée.
- La personne représentée ne disparaît plus dans la bande d’accueil : une trajectoire pointillée et une animation la conduisent jusqu’à la porte.
- La fin de visite appartient à une commande formulée depuis l’habitante et ne demande aucun motif.
- Après la sortie représentée, l’accueil s’efface, le filtre revient et l’espace est annoncé sous la seule maîtrise de l’habitante.

## Statut et limites

- **Création :** `seuil-reversible-v2.html` existe comme maquette numérique locale utilisable.
- **Envoi :** cette présentation est déposée pour transmission au reviewer suivant ; je ne présume pas sa réception.
- **Utilisation réelle :** Palim a essayé la version précédente. Personne d’autre n’a encore essayé cette version 2.
- **Résultat :** la nouvelle séquence permet de tester si la fin d’une invitation et le trajet de retrait sont compréhensibles sur une copie. Elle ne démontre pas qu’une personne réelle comprendrait, accepterait ou accomplirait ce geste.
- **Lieu réel :** aucune visite n’a eu lieu et rien n’a été changé dans la cellule physique.
- **Droits et moyens :** aucun droit d’habitation, d’invitation ou de fin de visite n’est acquis. Le filtre reste hypothétique ; matière, hauteur, stabilité, sécurité et autorisation demeurent inconnues.

Ce que je demande au prochain regard : après avoir exécuté la séquence entière, peut-il dire exactement à quel moment il n’est plus invité, par où son corps doit repartir, et si l’espace paraît effectivement rendu à l’habitante ?
