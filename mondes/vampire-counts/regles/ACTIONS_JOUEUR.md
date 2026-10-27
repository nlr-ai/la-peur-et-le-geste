# 🎯 Actions du joueur et leurs contraintes

> État du code sur la branche `duchies`, relevé le 2026-10-06 dans les handlers de commandes (`src/VampireKings.Sim`) et le client Godot (`game/`).
> Les chiffres viennent de `content/*.json`. Le joueur et l'IA envoient les mêmes commandes.

## Règles générales

- **Être actif** : un 🧛 vampire en ⚰️ torpeur ou détruit n'est pas actif. Il ne peut ni étreindre, ni améliorer une 🏘️ ville, ni construire, ni recruter, ni choisir d'héritier, ni 🗡️ assassiner, ni ouvrir une 🤝 veine.
- **Sans terre** : aucune règle propre. Un sans-terre est simplement bloqué par « ce n'est pas votre 🏘️ ville / votre 📍 Lieu ». Il lui reste la fiche personnage, ses unités, ses ✨ sorts, les 💥 duels, les 🤝 veines, l'🗡️ assassinat et les 📜 événements.
- **Jour et nuit** : aucune restriction dans les commandes pour l'instant.
- **Délai** : un ordre est validé quand on l'envoie, puis validé à nouveau et exécuté au pas suivant.

---

## 🏘️ Villes et 🏛️ bâtiments

### Améliorer une 🏘️ ville · `towns.action.001` · écran 🏘️ Ville
- Il faut tenir la 🏘️ ville et être actif.
- Une seule amélioration à la fois, et pas au-delà du niveau maximal.
- Paiement immédiat :

| Vers | 🩸 Sang | 🔮 Magie | 😱 Effroi | Durée |
|---|---|---|---|---|
| Bourg | 3000 | 2000 | 400 | 52 semaines |
| Grande ville | 10000 | 8000 | 1500 | 156 semaines |

### Construire un 🏛️ bâtiment militaire sur un 📍 Lieu · `sites.action.001` · écran 🏘️ Ville
- Il faut tenir le 📍 Lieu et être actif.
- Le type de 📍 Lieu doit correspondre au bâtiment, et un seul bâtiment est permis par Lieu.

| 🏛️ Bâtiment | 📍 Lieu requis | Coût |
|---|---|---|
| Ossuaire (Squelettes) | Cimetière | 5 🩸 + 5 🔮 |
| Caserne des serfs (Arbalétriers) | Village asservi | 10 🩸 + 5 😱 |
| Chenil noir (🦇 Bêtes noires) | Bosquet mort | 5 🩸 + 10 🔮 |
| Autel de liaison (Élémentaires) | Nœud de ley | 20 🔮 |
| Chambre des rites (Ritualistes) | Crypte | 5 🩸 + 15 🔮 |
| Arsenal maudit (Gardes lourds) | Forteresse de col | 15 🩸 + 10 🔮 |

### Saigner un 🛖 village · `humans.action.001` · écran 🏘️ Ville
- Il faut tenir le 🛖 village (aucun test d'activité).
- Trois intensités :
  - **légère** : rendement ×0,5, sans usure ;
  - **normale** : rendement ×1, usure 0,0055 par jour ;
  - **forte** : rendement ×2, usure 0,055 par jour.

### Construire un 🏛️ *Athanor* · `towns.action.002` · **IA seulement**, pas de bouton
- Il faut tenir la 🏘️ ville et être actif. Un seul par ville. Coût : 10 🩸 et 30 🔮.

---

## 🧬 Lignée et 🧛 personnage

### Étreindre un infant · `character.action.001` · fiche 🧛 personnage
- Il faut être actif, et attendre 45 jours depuis la dernière Étreinte.
- Coût : 20 🩸 et 10 🔮, multipliés par (1 + nombre d'infants non détruits).

### Désigner son 🔁 héritier · `succession.action.001` · fiche 🧛 personnage, écran 🔁 Succession
- L'héritier doit être un infant direct, et les deux doivent être actifs.
- Sans choix, c'est le Droit du Sire qui s'applique.

### Entrer en ⚰️ torpeur volontaire · `character.action.002` · fiche 🧛 personnage
- Seulement pour soi, en étant actif. L'écran propose de 100 à 600 jours.
- Pendant la torpeur, ses 🏘️ villes passent à son 🔁 héritier.

---

## 🐾 Meute et 🤝 serments

### 🤝 Serment de Meute et règle de la Meute · `pacts.action.007` · écran Serments
- Réservé au seigneur de la table. On ne se fixe pas de serment à soi-même.
- Cinq clauses :
  - 🩸 ration : 0, la Soif ou le double ;
  - 🐺 droit de chasse : aucun, nos terres, terres de la 🧬 lignée, toutes terres ;
  - part des prises pour la table : 0, 25, 50 ou 75 % ;
  - 💥 duels : autorisés ou interdits ;
  - 🛡️ service armé : aucun, protection du domaine, armée.

### 🐾 Règle de la soif · `economy.action.010` · écran Cour
- Réservé au chef de la 🐾 Meute.
- Un quota de villageois par période (1 par semaine par défaut), ou « à votre faim ».

### 🐾 Rendre un membre prioritaire · `economy.action.012` · écran Cour
- Réservé au chef de la 🐾 Meute. Le membre doit être dans sa Meute et ne peut pas être le chef lui-même.

### 🩸 Prendre sa part ou tout boire · `economy.action.011` · écran Cour
- Seulement pour sa propre chasse.

> La 🔥 chasse elle-même (envoyer ou rappeler un chasseur sans terre) est décidée par le système, pas par le joueur.

---

## ⚔️ Unités et 💥 combat (sur la 🗺️ carte)

Ces ordres ne portent que sur ses propres unités, et seulement si elles sont vivantes.

### Recruter une compagnie · `armies.action.002` · écran 🏘️ Ville, panneau Armée
- Il faut le 🏛️ bâtiment du bon type sur le 📍 Lieu, et aucune compagnie déjà présente sur ce Lieu.
- Chaque compagnie déjà tenue du même type augmente le coût de 25 %.
- Les 💀 cadavres sont pris dans le stock de la 🏘️ ville du Lieu.
- **Plafond** : le total des troupes ne peut pas dépasser ⚡ Puissance × 0,3.

| Unité | Coût de base | Taille |
|---|---|---|
| Squelettes (⚔️ Relevés) | 1 🔮 + 20 💀 | 20 |
| Arbalétriers | 3 🩸 + 2 😱 | 20 |
| 🦇 Bêtes noires | 3 🩸 + 3 🔮 | 5 |
| Élémentaires | 8 🔮 | 3 |
| Ritualistes | 5 🔮 + 3 💀 | 3 |
| Gardes lourds | 4 🔮 + 10 💀 | 10 |

### Déplacer · `field.action.001` · sélection sur la 🗺️ carte
- La destination doit être sur la carte. L'ordre interrompt un 💥 combat en cours.

### Attaquer une unité · `field.action.003` · 🗺️ carte
- La cible doit être vivante, éveillée et hostile.

### Coordonner · `field.action.004` · 🗺️ carte
- Le meneur doit pouvoir mener. Il faut le même seigneur et au moins un suiveur.

### Escorter · `field.action.005` · 🗺️ carte
- Le protégé doit être d'un type qu'on peut escorter (`field.json`). Il faut le même seigneur.

### Renvoyer au sol · `field.action.006` · panneau Armée
- Impossible de renvoyer son propre 🧛 vampire.

---

## 🔮 Magie et ⭕ Cercle

### Lancer un ✨ sort de champ · `magic.action.008` · barre de sorts sur la 🗺️ carte
- Le lanceur est son propre 🧛 vampire sur la carte : il doit être vivant, éveillé et ne pas être déjà en train d'incanter.
- Portée maximale : 30.
- Le sort doit avoir fini de recharger, et il faut assez de 🔮 Magie.
- Le rang d'école requis n'est vérifié que par l'écran, pas par la simulation.

| ✨ Sort | Coût 🔮 | Recharge |
|---|---|---|
| Rage sanguine | 1 | 84 h |
| Moisson | 2 | 168 h |
| Brume | 1,5 | 252 h |
| Appel de la meute | 2 | 336 h |
| Cendres | 3 | 336 h |
| Vent noir | 1 | 168 h |

### Fixer la priorité du ⭕ Cercle · `magic.action.007` · écran Cercle
- Il faut être membre d'un Cercle et miser du 😱 Effroi qu'on possède (par pas de 5 à l'écran).
- Les mises repartent à zéro tous les 10 ans.

### 💥 Duel · écran Duel
- Le duel ne se déclenche pas sur ordre du joueur. Il naît d'une rencontre sur la carte ou d'un 📜 événement.
- **Jouer une passe** (3 passes par duel), avec un choix par passe :
  - une option peut être fermée par la 🐺 Bête ou par le Regard ;
  - une option de ✨ sort exige son rang d'école et coûte de 1 à 3 🔮.
- **🩸 Boire le vaincu** · `magic.action.009` : réservé au vainqueur, si l'issue le permet, une seule fois.

> Fonder ou refermer un ⭕ Cercle (`pacts.action.005`) : **IA seulement** pour l'instant.

---

## 🤝 Pactes et 🗡️ intrigue

### Ouvrir une 🤝 veine · `pacts.action.004` · écran Intrigue
- On doit être l'une des deux parties, et les deux doivent être actives.
- Au moins un des deux montants doit être positif, et chacun ne peut promettre que son revenu net.
- Si l'autre refuse, il faut attendre 20 jours avant de reproposer. L'écran va de 0 à 50 par jour, par pas de 0,5.

### 🗡️ Assassiner · `schemes.action.002` · fiche du personnage visé
- Il faut être actif, et on ne peut pas se viser soi-même. La cible ne doit pas être détruite ; elle peut être en ⚰️ torpeur.
- On engage du 🔮 et du 🩸 : les deux montants doivent être positifs et dans la limite de ses stocks.
- Ce qui est engagé est **perdu dans tous les cas**.

> Prêter allégeance (`pacts.action.006`) : **pas d'écran joueur**. Seuls l'IA et la console du meneur de jeu le font.

---

## 📜 Événements à choix

Seul le 🧛 vampire concerné répond, dans la fenêtre de l'événement.

| 📜 Événement | Qui choisit | Choix | Contrainte |
|---|---|---|---|
| La chaise vide | le membre, puis le chef | prévenir ou se taire ; laisser partir, promettre double ration, retenir par la peur | la peur coûte 5 😱 |
| Le serment acheté | l'affamé | refuser, accepter, dénoncer | accepter exige que l'acheteur ait 5 🩸 |
| La lettre égarée | le seigneur | croire, enquêter, ignorer | enquêter coûte 5 😱 |
| La double désertion | le seigneur | retenir l'un, retenir l'autre, laisser partir, effrayer | effrayer coûte 5 😱 par tête |
| Le dormeur volontaire | l'Ascète | dormir (30 jours de ⚰️ torpeur), rester | — |
| Deux trônes | le seigneur | égaliser, 💥 duel, l'un ou l'autre comme 🔁 héritier | l'héritier doit être son infant |
| La curée | le seigneur | 💥 duel, partager, séparer | — |
| Les 9 scènes de faim de la 🐾 Meute | le membre, puis le seigneur | 3 choix par scène (voir [REGLES_DU_JEU.md](REGLES_DU_JEU.md)) | chaque scène a sa propre condition |

---

## ⏳ Temps

- Pause avec Espace. Cinq vitesses : heure, nuit, semaine, mois, année.

---

## Ce qui manque ou cloche

- **Pas d'écran** pour le 🏛️ *Athanor*, l'allégeance 🤝 ni le ⭕ Cercle : seuls l'IA ou le meneur de jeu y ont accès.
- **Fossoyeur** (`field.action.002`) : la commande existe, mais rien dans le client ne l'envoie.
- **Torpeur** : la simulation n'impose aucune durée minimale ni maximale ; seul l'écran limite de 100 à 600 jours.
- **Rang d'école des ✨ sorts** : il n'est vérifié que par l'écran, pas par la simulation.
- **Pas de test d'activité** pour la saignée, les règles de 🐾 Meute, les serments et les déplacements : un 🧛 vampire en ⚰️ torpeur peut donc encore donner ces ordres.
