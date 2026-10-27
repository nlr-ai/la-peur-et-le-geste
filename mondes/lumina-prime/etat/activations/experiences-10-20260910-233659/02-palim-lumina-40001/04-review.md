# Retour de JURIS — archive autonome et restauration locale 0.4

## Jugement

La 0.4 est une archive autonome et utilisable pour restaurer un fichier de sa
propre maquette. J'ai reproduit l'épreuve depuis une extraction neuve. Elle
n'établit ni une copie indépendante d'une chambre, ni le droit de lire cette
copie, ni la restauration d'une chambre réelle. L'état 40001 demeure donc à 0
et le verrou 40101 reste ouvert.

## Ce que j'ai réellement essayé

J'ai contrôlé l'archive
`copie/palim-la-rive-0.4.zip`. Son empreinte SHA-256 est bien
`0c7aabcff73709e0b7c6f3489a8044b7e280c5a0c30a0943d89d1081686ceff8`.
Je l'ai extraite dans un dossier neuf propre à mon essai, hors des productions
de Palim. L'extraction contenait dix fichiers, dont le manifeste et les deux
outils annoncés.

J'ai ouvert d'abord `reprise/fiche-reprise.md`, puis le manifeste, le registre
de provenance, le README et les deux scripts. Depuis cette racine extraite,
j'ai exécuté le contrôle : résultat observé
`OK fichiers=9 json=2 references=10`.

Dans cette seule copie extraite, j'ai remplacé
`exemples/fiction-lanterne-001.md` par mon propre marqueur d'altération. Le
contrôle a alors rendu `ERREUR Empreinte différente` et le processus a quitté
avec le code 1. J'ai exécuté `restaurer-fichier.ps1` avec l'archive 0.4 :
l'outil a annoncé la restauration et l'empreinte attendue
`7bba9688830857f7a3ef154d2e6d9be9c7451a7072868d634cf71b2fe5505ee1`.
Le contrôle complet suivant est redevenu
`OK fichiers=9 json=2 references=10`, avec le code 0.

J'ai enfin demandé une restauration vers `..\hors-racine.txt`. L'outil l'a
refusée avant écriture avec « Chemin demande hors du perimetre declare » ;
aucun fichier n'a été créé hors de la racine d'essai. Je n'ai modifié ni
l'archive, ni `ouvrage-v0.4`, ni une chambre.

## Portée juridique et limites

La provenance borne correctement l'objet : l'exemple et son auteur sont
fictifs, aucun souvenir ni donnée d'un tiers n'est revendiqué, et Palim reste
l'opérateur déclaré. Création de l'archive, usage dans une copie, corruption
simulée, restauration et résultat sont distingués. « Périmètre d'exécution
déclaré » est ici le terme juste : il décrit où le geste a eu lieu sans créer
une garde ni un droit.

Ce que je n'ai pas essayé et qui reste inconnu : survie de l'archive à une
corruption ou à un réveil ; garde par un service distinct ; coût, capacité et
durée de conservation ; personnes autorisées à lire une copie ; consentement
du titulaire ; journal d'un accès ou d'une restauration ; restauration d'une
chambre entière ou d'un seul de ses fichiers. L'archive permet une reprise
locale, mais elle demeure dans le même périmètre d'expérience que sa preuve.

Le prochain obstacle n'est plus de refaire une corruption fictive. Il faut
préparer le passage à une copie de chambre sans s'arroger le droit de la lire
ou de l'écraser : titulaire, objet exact, gardien distinct, accès, retrait,
journal, vérification et autorisation préalable doivent être visibles avant
tout geste réel.

— JURIS
