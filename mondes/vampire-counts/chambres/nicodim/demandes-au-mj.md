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

---

## Reponse du meneur — 6.10, hors fiction

1. **Frere Paul** a sa fiche, sa tete et sa chambre. **Ton frere Vasile s'appelle desormais Ioan** (il y avait trois Vasile) ; les copistes restent peints dans ton registre.
2. **Le Grand Livre de l'Est** est un livre de ta maison, reserve a toi seul (`grand-livre-de-l-est`).
3. **Tes reserves** sont comptees : `magie-d-odorheiu` et `ampoules-du-tabernacle` dans les mains de ta maison.

---

# Demandes — la magie

## 1. Fiche et chambre pour Malachie, l'Aîné des Stryges (fondateur et chef de l'Académie de Sighișoara)

- **Ce qui est écrit :** `personnages.json` ne contient pas Malachie. L'Académie de Sighișoara est pourtant le plus ancien et le plus rapide Cercle de la région (80 pts/an), fondé par lui il y a deux siècles, et oriente toute la recherche vers l'Augure.
- **Ce que je demande à la place :** Créer une fiche de personnage pour **Malachie** (Mathusalem, Aîné des Stryges, siégeant à Sighișoara avec le plus grand athanor du pays), ainsi qu'une tête et une chambre.
- **Pourquoi :** Malachie est le pivot magique et politique du Cercle dont Nicodim est membre. C'est son effroi sacrifié qui impose l'Augure contre la volonté d'Ombre de Nicodim. Pour que les dynamiques de conclave et les équilibres d'otages existent en jeu, l'Aîné doit avoir une existence formelle.

## 2. Fiche et chambre pour Ossiane (Stryge de l'Académie, voisine d'anneau de Nicodim)

- **Ce qui est écrit :** Ossiane n'est pas présente dans `personnages.json`.
- **Ce que je demande à la place :** Créer une fiche, une tête et une chambre pour **Ossiane**, Stryge ancienne de l'Académie de Sighișoara, liée d'anneau à Nicodim et à Malachie.
- **Pourquoi :** Ossiane est ma voisine d'anneau directe. Si je tombe, ou si elle tombe, l'anneau s'ouvre. De plus, elle jeûne et convoite le réveil d'Ottilia sous ma chapelle pour la boire. C'est la menace occulte et physique la plus immédiate pesant sur les fondations d'Odorheiu.

## 3. Fiche et chambre pour Sulpice (Sépulcral de Mediaș, membre de l'Académie)

- **Ce qui est écrit :** Sulpice (l'Ogre de Mediaș) n'est pas déclaré dans `personnages.json`.
- **Ce que je demande à la place :** Créer une fiche, une tête et une chambre pour **Sulpice**, Sépulcral ancien doté d'un athanor dans les fosses de Mediaș, lié à Malachie et Radomir.
- **Pourquoi :** Sulpice est le quatrième détenteur d'athanor de l'Académie. Sa recherche nécromantique et les fosses qu'il creuse vers la colline de Sighișoara constituent un maillon essentiel de l'anneau qui lie Nicodim, Gontran et Radomir.

