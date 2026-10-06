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

---

## Reponse du meneur — 6.10, hors fiction

1. **Gontran → Cendrik** est ajoute (rancune, la ligne des choses qui ne se pardonnent pas). **Konstantin → Cendrik est refuse** : Konstantin ne sait pas encore que c'est toi.
2. **Frere Mihai** a une fiche gelee ; il sera promu quand le chant sur Ticușu commencera.
3. **Vasile** reste peint dans ton registre, sans fiche pour l'instant ; c'est toi qui gardes ce prenom.

---

# Demandes — la magie

### 1. Enregistrement des serments de Cercle dans l'état relationnel

- **Ce qui est écrit** : [etat/relations.json](file:///C:/Users/reyno/le-conseil2/mondes/vampire-counts/etat/relations.json) porte les allégeances et la veine asymétrique (Gontran bu par Cendrik), mais ne mentionne aucun lien relatif au Cercle de la Meute entre Cendrik, Vlaicu et Ilka.
- **Ce que je demande à la place** : Ajouter un lien réciproque ou une mention d'anneau dans `etat/relations.json` ou une table dédiée :
  - Entre Cendrik et Vlaicu : lien `["cercle:la-meute", "voisin-d-anneau"]`.
  - Entre Cendrik et Ilka : lien `["cercle:la-meute", "voisin-d-anneau"]`.
- **Pourquoi** : Le canon stipule qu'un Cercle est un anneau de serments d'otages liant chaque membre à ses deux voisins. Si ce lien n'apparaît pas dans l'état, le moteur ignore la solidarité forcée de recherche et le coût stratégique d'une rupture du maillon Ilka.

---

### 2. Trace canonique de Brune (ancienne Vorace de la Meute)

- **Ce qui est écrit** : Brune, la Vorace disparue il y a dix ans lors d'une chasse avec Vlaicu, n'a aucune fiche ni mention dans `etat/personnages.json` (statut détruite ou disparue).
- **Ce que je demande à la place** : Consigner formellement Brune comme personnage historique disparu/détruit de la maison de Hoghiz dans la mémoire du monde ou une fiche gelée d'archive.
- **Pourquoi** : C'est sa disparition qui a ouvert l'anneau et permis à Cendrik d'y entrer. Pour un arpenteur méthodique, savoir si elle est morte ou en torpeur sous les bois de Comăna conditionne la certitude de la vacance de sa place dans l'anneau.

