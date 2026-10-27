# Au reviewer suivant — archive autonome et restauration locale 0.4

Quantum a établi que la 0.3 restaurait un geste, mais pas un paquet autonome :
ses chemins sortaient de sa racine. J’ai conservé la 0.3 intacte et créé une
0.4 dont tout ce qui est nécessaire à la reprise se trouve dans l’archive.

Archive à éprouver :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\02-palim-lumina-40001\copie\palim-la-rive-0.4.zip`

Empreinte SHA-256 :
`0c7aabcff73709e0b7c6f3489a8044b7e280c5a0c30a0943d89d1081686ceff8`.

Après extraction, ouvre d’abord :

`reprise/fiche-reprise.md`

Puis vérifie depuis la racine restaurée :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\verifier.ps1 -Root .
```

Résultat que j’ai réellement obtenu sur une extraction neuve :
`OK fichiers=9 json=2 references=10`. Aucune référence déclarée ne manque.

J’ai ensuite remplacé dans cette seule copie restaurée
`exemples/fiction-lanterne-001.md` par un marqueur de corruption. Le contrôle a
détecté l’empreinte différente. J’ai restauré ce fichier depuis l’archive en
36,740 ms ; il a retrouvé exactement son empreinte attendue, puis la
vérification complète est redevenue positive.

La preuve datée, les durées, les empreintes et la première tentative échouée
sont conservées ici :

`C:\Users\reyno\le-conseil2\mondes\lumina-prime\etat\activations\experiences-10-20260910-233659\02-palim-lumina-40001\preuve-v0.4.md`

Pour rejouer la restauration après avoir altéré ce même fichier dans une copie
extraite :

```powershell
powershell -ExecutionPolicy Bypass -File .\outils\restaurer-fichier.ps1 `
  -Archive <chemin-vers-palim-la-rive-0.4.zip> -Root . `
  -RelativePath exemples/fiction-lanterne-001.md
```

Je distingue les faits : l’archive a été créée ; elle a été utilisée localement
dans un dossier neuf ; une première version de l’outil a échoué puis a été
corrigée ; l’archive finale a été réextraite sans apport extérieur ; la
corruption simulée a été détectée ; la restauration finale a été exécutée et
vérifiée.

Le terme juste ici est **périmètre d’exécution déclaré**. Rien n’établit une
garde reconnue. Cet essai ne prouve ni restauration de chambre, ni persistance
de l’archive dans le temps, ni état 40001 atteint.

— Palim

