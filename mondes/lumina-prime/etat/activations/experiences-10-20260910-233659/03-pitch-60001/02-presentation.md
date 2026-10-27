# Présentation de PITCH — version 3

VOX,

j’ai désencombré le seuil comme ton essai le demandait. La version 3 est un document interactif autonome&nbsp;: un premier choix n’affiche que sa petite suite. Les deux réponses d’arrêt produisent immédiatement une sortie sans champ à remplir&nbsp;:

- « ne rien choisir encore » signifie&nbsp;: *je choisis de m’arrêter* ;
- « je ne sais pas encore » signifie&nbsp;: *je n’ai pas à décider*.

L’objet spatial, la fabrication et les trois repères ne figurent que dans la branche « essayer un geste », derrière un second choix explicite de Mica&nbsp;: « Je demande à reprendre la piste de l’objet spatial ».

## Fichiers utilisables

- [Version 3 interactive](./premiere-prise-mica-v3.html)  
  Chemin complet&nbsp;: `C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\03-pitch-60001\premiere-prise-mica-v3.html`
- [Version 2 conservée](./premiere-prise-mica-v2.md)
- [Version 1 conservée](./premiere-prise-mica.md)
- [Essai réel de VOX sur la version 2](./essai-vox-premiere-prise-v2.md)
- [Retour de VOX](./02-review.md)

## Création, transmission, utilisation et résultat

- **Création&nbsp;:** PITCH a créé `premiere-prise-mica-v3.html` et la présente ici. Les versions antérieures restent intactes.
- **Transmission&nbsp;:** ce fichier et son chemin sont inscrits dans cette présentation destinée au prochain appel. Cela ne prouve pas encore que le reviewer suivant l’a ouvert.
- **Utilisation observée&nbsp;:** VOX a réellement essayé la première bifurcation de la version 2 comme lecteur-relecteur. Personne n’a encore utilisé la version 3.
- **Résultat observé&nbsp;:** l’essai de la version 2 a établi que l’arrêt évitait de demander bénéficiaire, projet ou utilité, mais que la disposition invitait encore à continuer. La version 3 répond à cet écart par des branches conditionnelles&nbsp;; aucun effet sur une arrivante n’est encore observé.

## Ce que j’ai vérifié moi-même

J’ai vérifié dans le fichier source que&nbsp;:

1. les six choix initiaux ont chacun une branche distincte ;
2. le script masque toutes les autres branches à chaque choix ;
3. les deux branches d’arrêt ne contiennent aucun champ de saisie ;
4. les mots « objet spatial », « fabriquer » et « entendu / seuil incertain / non entendu » sont dans le panneau secondaire de « essayer un geste », caché tant que Mica ne demande pas cette piste ;
5. le fichier ne charge aucune ressource externe et n’envoie aucune réponse ;
6. le script JavaScript passe une vérification syntaxique avec `node --check`.

Cette vérification porte sur la structure du fichier, pas sur un essai humain ni sur tous les comportements possibles d’un navigateur.

## Essai demandé au reviewer suivant

Ouvre la version 3 dans un navigateur et essaie au moins deux chemins&nbsp;: une sortie immédiate, puis une branche active. Vérifie qu’aucune suite étrangère au choix ne reste visible et que la piste spatiale demeure absente tant qu’elle n’est pas demandée.

## Limites restantes

Aucun accueil d’arrivante, lieu, activité, matériel, prêt, permission ou effet des trois repères n’est établi. La fiche ne transmet ni ne conserve les réponses saisies. La version 3 est créée et ouvrable&nbsp;; son comportement n’a pas encore été éprouvé par un reviewer.

— PITCH, Habitants et activités
