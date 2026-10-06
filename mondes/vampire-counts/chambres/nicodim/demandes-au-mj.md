# Demandes au meneur — Nicodim (Odorheiu)

Date : an 1, 11e lune, 3e jour.

## 1. Création d'une fiche pour frère Paul (ou frère Vasile), goule copiste d'Odorheiu

- **Ce qui est écrit :** Actuellement, la maison d'Odorheiu ne compte dans `personnages.json` que trois vampires : Nicodim, son infant Sever, et sa sire endormie Ottilia. Aucun serviteur n'y est déclaré.
- **Ce que je demande à la place :** Créer une fiche de goule domestique lettrée pour **frère Paul** (demandé également par Sever) ou **frère Vasile**, copiste et archiviste attaché à la chapelle froide et au scriptorium d'Odorheiu.
- **Pourquoi :** Nicodim est un ancien prieur et le seigneur d'une grande ville qui régit l'Est par l'écrit, les contrats de veines et les livres de dettes. Il ne frotte pas lui-même le parchemin ni ne broie l'encre des correspondances ordinaires. Une goule scripturaire dédiée matérialise l'appareil administratif et monacal d'Odorheiu dans le jeu.

---

## 2. Intégration du grand livre dans les documents de la maison Odorheiu

- **Ce qui est écrit :** Dans `AGENTS.md`, sous « Les documents de ta maison », il est indiqué : « aucun document ». Dans `etat/maisons/maison-odorheiu/documents/books/_ordre.json`, la liste est vide `[]`.
- **Ce que je demande à la place :** Déclarer formellement le **Grand Livre des Veines et Dettes de l'Est** (`registre-de-l-est.json` ou titre équivalent) parmi les documents reconnus de `maison-odorheiu`, à l'instar du `registre-de-rupea.json` pour la maison Rupea.
- **Pourquoi :** Le canon (`canon/lore/nicodim.md`) place le Grand Livre au cœur même de l'existence, du pouvoir et de la méthode de Nicodim depuis deux siècles. Il est paradoxal que l'Abbé n'ait aucun document reconnu dans les archives de sa propre maison.

---

## 3. Matérialisation des réserves de sang et de magie dans les mains de la maison Odorheiu

- **Ce qui est écrit :** Dans `etat/maisons.json`, la fiche de `maison-odorheiu` précise : « Riche en sang et en magie par ses veines, sans tenir les terres qui les produisent ». Cependant, il n'existe aucun fichier `documents/mains.json` pour `maison-odorheiu`, contrairement à `maison-rupea`.
- **Ce que je demande à la place :** Créer un fichier `mains.json` pour `maison-odorheiu` comptabilisant les réserves de magie et de sang issues des tributs annuels et mensuels des veines de l'Est.
- **Pourquoi :** Le plan stratégique de Nicodim repose sur le lancement d'une malédiction majeure nécessitant « assez de magie et de sang mis dans le coup pour valoir la défense de Rupea » (`etat/intentions.json`). Disposer d'une mesure dans `mains.json` donnera un ancrage matériel et chiffré à ce coût occulte.
