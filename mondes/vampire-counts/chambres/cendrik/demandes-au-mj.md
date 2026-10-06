# Demandes au meneur — Cendrik de Cincu

Ce fichier consigne les points techniques et d'état qui méritent arbitrage hors fiction par le meneur, conformément aux règles de préparation du monde.

---

### 1. Réciprocité de la relation Gontran -> Cendrik

- **Ce qui est écrit** : Dans [etat/relations.json](file:///C:/Users/reyno/le-conseil2/mondes/vampire-counts/etat/relations.json), il existe bien une ligne pour Cendrik envers Gontran (`opinion: 0`, `liens: ["son bu"]`). En revanche, il n'existe aucune relation réciproque de Gontran vers Cendrik, ni de Konstantin vers Cendrik (alors que le canon précise dans `canon/lore/characters.json` et `canon/lore/konstantin.md` que Konstantin cherche le Sépulcral aux cendres et que Gontran a inscrit le duel dans son registre).
- **Ce que je demande à la place** : Ajouter dans `etat/relations.json` :
  - De Gontran vers Cendrik : opinion négative (ex: -50 ou rancune), liens : `["son buveur", "honte secrète"]`.
  - De Konstantin vers Cendrik : opinion hostile (ex: -80), liens : `["l'ennemi sans nom qui a bu mon chef"]`.
- **Pourquoi** : Le duel et la honte d'avoir été bu constituent un fait central du réseau de tensions. Si le buveur porte la relation mais que le bu ne l'enregistre pas dans la table d'état, les calculs de rancune et de dynamique relationnelle risquent d'ignorer la dette et la menace qui pèsent sur Cendrik.

---

### 2. Attribution d'une fiche et d'une chambre pour Frère Mihai (Ritualiste en chef)

- **Ce qui est écrit** : Aucun habitant secondaire de Cincu ne possède de fiche dans [etat/personnages.json](file:///C:/Users/reyno/le-conseil2/mondes/vampire-counts/etat/personnages.json). Frère Mihai est peint dans mon registre d'état (`pop:rituel-frere-mihai`) comme le prêtre mort relevé qui conduit les chants d'annexion de la terre.
- **Ce que je demande à la place** : Évaluer l'opportunité de créer une fiche légère pour Frère Mihai (`mihai`, statut subordonné ou non-joueur) lorsque les incantations sur Ticușu débuteront (dans 30 jours selon le plan), afin qu'il puisse porter les actes de chant liturgique sans que Cendrik ait à s'exposer physiquement sur la ligne de front à chaque arpent rogné.
- **Pourquoi** : Selon les règles du monde (*« La terre est à qui la chante. Les Ritualistes, prêtres morts relevés, chantent la terre du voisin »*), ce sont les Ritualistes qui accomplissent le rituel à la lisière. Lui donner une existence formelle dans l'état permettra de matérialiser la manœuvre et de donner une cible tangible aux contre-attaques ou aux observations des voisins.

---

### 3. Fiche et chambre pour Vasile, maître-fossoyeur de Cincu

- **Ce qui est écrit** : Vasile est peint dans mon registre (`pop:fossoyeurs-vasile`) comme le chef des fossoyeurs et ramasseurs d'os qui parcourent les lisières de Comăna et les routes de l'ouest.
- **Ce que je demande à la place** : Une fiche de goule/serviteur de corvée pour Vasile (`vasile`, de la maison Cincu), à l'instar de Stanca pour Teodor à Rupea.
- **Pourquoi** : Cendrik ne se déplace jamais sous le soleil et évite d'aller lui-même fouiller les charniers et compter les tombes sous les yeux des autres seigneurs. Vasile est ses yeux diurnes et le porteur de ses messages vers les lisières.
