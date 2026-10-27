# 🏺 Enchantement v1 — Le grimoire des circuits

## 📌 Statut et périmètre

Version arbitrée à la demande de l’utilisateur, après correction : **les grilles relèvent de l’Enchantement**. Elles ne remplacent pas la magie élémentaire. Ce document tranche les mécanismes qualitatifs de cette v1 ; il ne fixe pas de valeurs chiffrées de puissance ou de coût. Les [usages par institution](#-11-usages-par-institution) sont des propositions.

Référence de conception : `C:/Users/reyno/magic-designer/docs/grimoire-grille.md`. Nous reprenons l’idée des flux, supports, vannes et mesures locales. Le présent système est une adaptation autonome pour cet univers, pas une copie des règles ou des limitations du logiciel de Magic Designer.

Première application : les dispositifs élémentaires du [Bastion](../organisations/01-bastion.md). Les grilles capables de porter d’autres écoles devront respecter les accès et limites de ces écoles.

## 🧩 1. Qui fait quoi ?

| Acteur | Apport |
|---|---|
| Praticien de l’effet | Produit l’effet et l’accorde à l’ouvrage lors de sa fabrication. Un élémentaliste fournit une opération élémentaire ; un protecteur un filtre protecteur. |
| Enchanteur | Inscrit les conditions, chemins, commandes et régulations qui rendent cette opération répétable. |
| Artisan ou mage de Matière | Fabrique les supports, contenants, conduits et assemblages. La magie de Matière n’est pas obligatoire pour fabriquer un objet ordinaire. |
| Utilisateur | Actionne les commandes disponibles. Il n’acquiert pas les pouvoirs des créateurs. |

**Coopération retenue pour cette v1 : au moins deux personnes distinctes participent à l’accord d’un effet.** Un polymage peut tenir l’un ou l’autre rôle, mais ne dispense pas de cette coopération.

Exemple : Héloïse peut fournir l’effet élémentaire à un collègue enchanteur, ou inscrire un circuit accordé avec un autre élémentaliste.

## ⚡ 2. Trois choses à ne pas confondre

### La ressource traitée

Eau du réservoir, air ambiant, chaleur d’un foyer, lumière incidente, matière disponible. **Le signe ne crée pas une quantité infinie d’élément.**

### L’alimentation magique

Correction retenue : aucune création d’énergie. L’ouvrage utilise une alimentation réelle, notamment des gemmes où les mages de Matière compriment de la matière grâce à un travail fourni auparavant. La détente restitue ce travail ; la masse n’est pas convertie en énergie pure. Voir [Magie élémentaire v1](ELEMENTAIRE_V1.md).

Cette énergie stockée peut fournir le travail nécessaire, par exemple déplacer de l’eau vers le haut. Une réserve vide ne fournit plus ce travail. L’inscription et la commande ne remplacent jamais l’alimentation.

### La commande

Une Trace indique une mesure ou un appui. Elle ouvre ou ferme une vanne. **Une commande ne fournit ni élément ni puissance.**

Copier un dessin, multiplier les fils ou faire circuler une Trace en boucle ne multiplie pas l’alimentation disponible.

## 🧙 3. Pourquoi le mage peut partir

L’accord réalisé à la fabrication stabilise une **opération définie** dans le support. L’alimentation de l’Enchantement permet ensuite son exécution sans attention permanente du praticien.

- L’élémentaliste engage sa volonté pendant l’accord ; il ne laisse pas derrière lui une volonté vivante ou infinie.
- L’objet répète ce qui a été accordé dans les limites de son ouvrage.
- Un utilisateur peut le commander sans posséder le don élémentaire.
- Changer la nature de l’effet demande un nouvel accord avec le spécialiste.
- Entretenir les supports n’accorde pas le droit de modifier arbitrairement l’effet.
- Un dispositif ordinaire n’invente pas de nouveaux buts et ne devient pas spontanément un Non-Vivant.

**La stabilité, l’entretien et la puissance sont bornés.** Les durées et consommations exactes restent à dimensionner, sans fatigue permanente imposée à distance au créateur.

## ✍️ 4. Anatomie d’une grille

- Une grille est inscrite sur une face physique d’un objet.
- Le format courant est le **3 × 3**, avec une case centrale représentant le support.
- Le bord représente une interface avec l’environnement immédiat ou un raccord réel.
- Chaque case porte un seul signe ; une case vide ne transmet rien.
- L’orientation de la grille compte.
- Une liaison entre objets exige un contact ou une connexion construite et adaptée.
- Le dessin doit être accordé : recopier une inscription avec une encre ordinaire ne fabrique pas un enchantement actif.

Les grands ouvrages assemblent plusieurs grilles sur plusieurs supports. Pour cette v1, le 4 × 4 et le 5 × 5 ne sont pas nécessaires : on gagne en lisibilité en séparant les fonctions.

## 🔤 5. Alphabet retenu

### Prises élémentaires — ce qu’on prélève

| Signe | Domaine | Règle de la v1 |
|---|---|---|
| 🜁 | Air | Déplace de l’air réellement présent. L’Air est un gaz ; ce n’est pas un symbole universel du mouvement. |
| 🜂 | Chaleur / feu | Transfère de la chaleur depuis un foyer ou un corps chaud. Une flamme dépend aussi de conditions matérielles de combustion. |
| 🜄 | Eau | Prélève et conduit de l’eau disponible par une prise réelle. |
| 🜃 | Terre | Déplace des matériaux minéraux libres accessibles : grains, poussière, fragments. Ne remodèle pas à lui seul une pierre massive. |
| ☉ | Lumière | Conduit une lumière disponible depuis une source. Ne fournit pas une perception ni une divination. |

Ce sont des **prises**, pas des générateurs. Elles doivent être reliées à la ressource désignée. La Terre ne traverse pas un support plein comme si elle était un signal.

La glace résulte d’un refroidissement de l’eau avec évacuation de chaleur. La foudre reste dans le domaine élémentaire général, mais son module d’inscription n’est pas défini dans cette première grammaire.

### Opérateurs — ce que fait le circuit

| Signe | Nom | Fonction |
|---|---|---|
| → ↑ ← ↓ | Porter | Oriente le transfert vers la case ou l’interface indiquée. |
| ⇸ | Freiner | Réduit le débit ; les contraintes et dissipations doivent être supportées par l’ouvrage. Le frein n’efface pas le reste de la ressource. |
| ⇻ | Barrer | Ouvert sans Trace ; se ferme lorsqu’il en reçoit une. |
| ↪ | Crocher | Fermé sans Trace ; s’ouvre lorsqu’il en reçoit une. |
| ⇥ | Décharger | Dirige vers un récepteur réel raccordé : réservoir, dissipateur ou évacuation. Remplace le « Boire » qui faisait disparaître les flux. |
| ⇨ | Presser | Émet une Trace pendant un appui physique. |
| ∙ | Vide | Ne transmet pas ; ce n’est ni un stockage ni un puits. |

Les signes ont des orientations. Une vanne commande un transfert défini ; elle ne trie pas les ennemis et les alliés.

### Principes et qualificatifs

| Signe ou qualificatif | Fonction |
|---|---|
| ☿ Mercure | Mesure une propriété locale du support et émet une Trace vers ses cases voisines. |
| 🜔 Sel | Retient une réserve dans les limites de l’ouvrage. N’augmente pas arbitrairement la capacité physique du contenant. |
| Chaud, Mouillé, Lourd, Clair… | Spécifient la grandeur mesurée ou le flux sélectionné. |
| Étroit / Large | Distribuent une sortie sur une petite ou une grande surface ; ne multiplient pas son débit. |

Les descripteurs du grimoire peuvent conserver leurs signes directionnels, par exemple **ᐳ** pour « Chaud vers la droite » et **ᑐ** pour « Mouillé vers la droite ». Une version en mots reste préférable lorsque la police ne rend pas les glyphes.

**Mercure sans qualificatif ne mesure rien.** Sel et Mercure ne coexistent pas dans le centre d’une même grille 3 × 3 : utiliser deux supports raccordés.

Soufre et Miroir sont écartés de la v1. La rétention au-delà des capacités normales demanderait un ouvrage spécifiquement renforcé ou une coopération avec Protection ; Sel ne fournit pas cette magie gratuitement.

## 🔗 6. Circulation et régulation

1. On suit une prise réelle vers les chemins et les sorties.
2. Une flèche accepte un flux par ses côtés compatibles et le transmet vers sa pointe. Les coudes sont possibles.
3. À une dérivation, **le débit se partage**. Deux branches ne reçoivent pas chacune la totalité.
4. Un flux matériel nécessite un passage adapté. L’inscription ne crée pas un portail dans la matière.
5. Un flux entrant au centre agit sur le support selon sa nature : chaleur absorbée, remplissage d’un creux, action d’un courant d’air…
6. Une sortie vers le monde libère effectivement le flux. Il peut mouiller, chauffer ou déplacer ce qu’il rencontre.
7. Une voie fermée bloque le transfert. Une entrée encore alimentée peut provoquer pression, échauffement, accumulation ou débordement selon le montage.
8. La Trace circule entre voisins ou par un raccord de commande explicite. Une case incompatible l’arrête.
9. Les mesures sont locales : température, niveau, charge, éclairement. Ni identité, ni hostilité, ni information distante ne sont déduites.
10. Le seuil d’une régulation dépend de la calibration du support et du capteur. La puissance dépend de l’alimentation et de la capacité du montage ; aucun grand nombre inscrit ne les rend infinis.

Un circuit peut osciller : ouvrir, chauffer, fermer, refroidir. Une bonne conception amortit ces variations. Il n’existe pas de correction intelligente cachée.

## 🧱 7. Le support fait partie du sort

La matière, la forme, la masse, les raccords et la position déterminent ce qui fonctionne.

- Un contenant plein ne reçoit plus d’eau sans évacuation, débordement ou contrainte.
- Une pièce trop chaude peut se déformer et détruire ses inscriptions.
- Un jet ou un courant exerce des efforts ; le montage doit être ancré.
- Une inscription brisée coupe ou altère le circuit. Le comportement dépend de l’endroit endommagé.
- Un fil coupé supprime sa Trace : Crocher se ferme, Barrer s’ouvre.
- Une interruption de puissance magique arrête l’action enchantée ; elle n’efface ni chaleur, ni pression, ni eau accumulées.
- Les évacuations matérielles et les soutènements doivent rester utiles sans magie.

Les collisions, rotations, frottements, flaques et gaz existent dans ce monde. Leur absence éventuelle dans le prototype logiciel de référence ne constitue pas une loi de l’univers.

## 🏰 8. Trois ouvrages de référence

### A. La citerne à fermeture automatique

**Partenaires :** élémentaliste + enchanteur ; contenant et raccords fabriqués par les artisans.

- Une prise 🜄 est reliée à un bassin d’alimentation réel.
- Le flux arrive par un Crocher, fermé par défaut.
- Une grille séparée porte un Mercure Mouillé dont la Trace commande un Barrer placé en série.
- Une commande Presser maintenue autorise le remplissage via le Crocher.
- Quand le niveau calibré est atteint, le Barrer ferme.
- Un trop-plein matériel évacue l’eau si la mesure cesse de fonctionner.

**Panne lisible :** un fil de mesure coupé laisse le Barrer ouvert. La commande humaine et le trop-plein restent deux moyens de limiter l’incident. Sans eau au bassin ou sans puissance disponible, rien n’est créé.

### B. La dalle chauffante réglée

**Partenaires :** élémentaliste + enchanteur.

- Une prise 🜂 prélève la chaleur d’un foyer.
- Un Mercure Chaud mesure la dalle et commande un Barrer.
- La dalle diffuse la chaleur par contact.
- Lorsqu’elle atteint sa température calibrée, l’arrivée ferme.
- Un dissipateur matériel permet d’évacuer les excès.

**Panne lisible :** le capteur arraché ne ferme plus l’arrivée. La dalle peut surchauffer ; son énergie reste présente après coupure. Le montage doit permettre d’isoler le foyer.

### C. La couronne d’eau commandée

**Partenaires :** élémentalistes + enchanteurs ; bâtisseurs pour les conduits.

- Des citernes réelles alimentent plusieurs branches.
- Chaque branche possède un Crocher commandé depuis un poste local.
- Les sorties larges répartissent l’eau en rideaux.
- Ouvrir plusieurs branches partage le débit et la puissance disponibles.
- Le relâchement de la commande ferme l’admission enchantée ; l’eau déjà libérée poursuit sa chute.

**Panne lisible :** une branche rompue perd son eau jusqu’à son isolement. Aucun poste central ne sait automatiquement où est la fuite.

## ⚖️ 9. Frontières avec les autres écoles

- **Éléments** fournit et maîtrise les effets élémentaires ; l’inscription durable relève d’Enchantement.
- **Matière** façonne les objets ; une grille ne donne pas gratuitement le remodelage d’un mur.
- **Protection** peut fournir des filtres ou contraintes supplémentaires, accordés avec ses praticiens. Une vanne ordinaire ne devient pas un bouclier universel.
- **Divination** fournit une observation magique ciblée. Mercure ne mesure que le support local.
- **Esprit** et **Émotions** ne sont pas inclus dans les Traces. Un signal de niveau n’est pas une pensée.
- **Espace** reste nécessaire aux véritables passages entre lieux ; un raccord traverse un trajet construit, pas une distance abolie.
- **Annulation** doit comprendre le fonctionnement qu’elle interrompt ; le matériel et les effets physiques déjà produits demeurent.

## 🌑 10. L’apparition du Non-Vivant

Un ouvrage ordinaire suit ses opérations et ses ressources. Il ne cherche pas de nouveaux supports, de nouveaux habitants ou de nouveaux buts.

Le passage à un Non-Vivant marque une autre situation : un fonctionnement devient capable de se maintenir et de se propager selon ses instincts. **La condition retenue est une durée :** un fonctionnement tenu ou répété sans interruption assez longtemps pour que sa continuité cesse de dépendre des personnes qui l’assuraient. Voir [MONDE.md](../MONDE.md#-origine-des-non-vivants). Une boucle de commande ne suffit pas, par définition, à produire un Non-Vivant : c’est la durée qui compte, pas la topologie. Un circuit alimenté, entretenu et réparé sans jamais s’éteindre constitue en revanche un terrain favorable. La durée exacte du seuil reste ouverte.

Un mage retourné peut chercher cette autonomie pour dépasser les contraintes de ses ouvrages. La v1 ne lui attribue pas encore une recette garantie.

## 🏛️ 11. Usages par institution

**Statut : propositions.** Aucun de ces usages n’est un pouvoir supplémentaire : tous découlent des règles ci-dessus. Ils disent ce que les institutions *peuvent* faire de l’école, pas ce qu’elles font déjà.

### Le constat de départ : faire durer le geste d’un autre

L’Esprit est le télégraphe de ce monde, l’[Élémentaire](ELEMENTAIRE_V1.md#-usages-par-institution) sa mécanique. **L’Enchantement en est l’automatisme** : il transforme le geste rare d’un praticien doué en un ouvrage que n’importe qui actionne. C’est l’école qui met les autres à la portée de ceux qui n’ont pas le don, et c’est par là qu’elle pèse le plus sur la civilisation.

Il en découle trois choses :

- **L’enchanteur n’est pas le goulot.** L’Enchantement s’apprend ; l’Élémentaire est inné, la Protection demande l’éveil. Ce qui manque, c’est le spécialiste de l’effet, sans qui aucun accord n’est possible. Un consortium vaut par les praticiens qu’il sait réunir, pas par ses enchanteurs.
- **Un accord est un acte à deux noms.** Changer la nature d’un effet exige un nouvel accord avec le spécialiste ; entretenir ne donne pas le droit de modifier. Qui a accordé un ouvrage en tient la clé, et celui qui l’utilise en dépend.
- **Tout est lisible et rien n’est intelligent.** Une grille est inscrite sur une face physique : on peut la lire, la relever, la voler. Elle mesure le niveau, la chaleur ou la charge, jamais un ennemi.

### 🏺 Consortiums d’enchantement — la forme de transmission propre à l’école

Ils réunissent enchanteurs, fournisseurs et praticiens des autres écoles ([MAGIES_ET_RELATIONS](../MAGIES_ET_RELATIONS.md)). Leur métier est l’assemblage : un élémentaliste qui fournit l’effet, un enchanteur qui l’inscrit, un artisan qui fabrique le support, un fournisseur de gemmes. Leur pouvoir tient dans leurs carnets de praticiens, et dans les ouvrages en service qu’eux seuls peuvent faire évoluer.

### 🏰 [Bastion](../organisations/01-bastion.md) — la défense sans le défenseur

- **La procédure enchantée** permet à des opérateurs sans don de conduire couronnes, fournaises et portes ([manuel des recettes](../organisations/BASTION_DEFENSE_RECETTES_V1.md)). Le Bastion tient debout même quand Héloïse n’est pas là.
- **Le savoir de la défense est inscrit dans les grilles.** C’est une force (il survit aux départs) et une fragilité : qui relève les grilles d’un rempart connaît ses seuils et ses pannes lisibles.
- **Les ouvrages de la ville** : citernes à fermeture automatique, dalles chauffantes, éclairage conduit depuis les fournaises.

### 🚪 [Ligue des passages](../organisations/02-ligue-des-passages.md) — équiper les stations

- **Les fonctions d’accueil** : lumière conduite, citernes, salles d’attente chauffées, portes à Barrer et Crocher, filtres accordés avec ses protecteurs.
- **Ce qui reste humain** : l’ouverture elle-même. Qu’un effet d’Espace puisse être accordé dans un ouvrage n’est pas établi ; la Ligue a besoin d’ouvreurs aux deux extrémités, et l’Enchantement ne les remplace pas.
- **Une Ligue sans élémentaliste** doit acheter chaque effet de chaleur ou d’eau à un consortium, ou au Bastion.

### 🎭 [Communion des récits](../organisations/04-communion-des-recits.md) — les dispositifs de cérémonie

- **La mise en scène** : lumière conduite sur l’assemblée, air conduit dans des tuyaux sonores, et peut-être des apparences d’Illusions accordées avec leurs maîtres, si cette école s’accorde.
- **Ce qui ne s’automatise pas** : l’Esprit et les Émotions n’entrent pas dans les Traces (§ 9). Un dispositif reproduit les mêmes sensations ; il ne fait naître aucune croyance.
- **La cérémonie parfaite.** Un dispositif rend la même lumière, le même son, dans le même ordre, chaque fois. C’est l’[ancre](ESPRIT_V1.md#-11-cérémonies-dancrage) la plus nette possible, et aussi la répétition la plus exacte, donc le [sillon](ESPRIT_V1.md#le-sillon-des-cérémonies) le plus profond.

### 🕸️ [Fédération insaisissable](../organisations/07-federation-insaisissable.md) — l’équipement de la fuite

- **Des trousses préparées** que des réfugiés sans don peuvent utiliser : lampe, chauffe, filtre, petite citerne, chacun avec sa gemme.
- **Leur faiblesse** : un objet enchanté est une chose. Il se trouve, se lit, et sa grille dit d’où il vient.
- **Leur dépendance** : la Fédération n’a pas l’Élémentaire. Chaque effet de chaleur ou d’eau qu’elle inscrit, il lui faut le faire accorder par quelqu’un d’extérieur.

### Ceux qui n’ont pas l’Enchantement, mais en dépendent

- **👁️ [Collège des preuves](../organisations/03-college-des-preuves.md) — les instruments.** La Divination utilise des réserves : les enchanteurs fabriquent ses contenants et ses dispositifs de recharge ([MAGIES_ET_RELATIONS](../MAGIES_ET_RELATIONS.md)). Le Collège loue aussi des **lecteurs de grilles** pour établir ce qu’un ouvrage faisait au moment d’un incident.
- **🕳️ [Corps de résolution](../organisations/06-corps-de-resolution.md) — ses cibles.** Les ouvrages enchantés sont ce qu’il interrompt le plus souvent, et annuler exige de comprendre. Une grille relevée, un plan d’ouvrage ou l’enchanteur qui l’a inscrit valent un raccourci vers le troisième degré de l’[Annulation](ANNULATION_V1.md). Les archives des consortiums sont donc pour lui des pièces de travail, qu’ils n’ont aucune envie de lui ouvrir.

### Dans la société entière, sans employeur fixé

| Domaine | Usage | Qui doit l’accorder |
|---|---|---|
| **Maison et hospice** | Dalle chauffante, citerne qui se ferme seule, lampe conduite | Élémentaliste + enchanteur |
| **Ateliers** | Four à chauffe tenue, forge à soufflet réglé, moulin régulé | Élémentaliste + enchanteur, artisan |
| **Serrures et coffres** | Crocher qui ne s’ouvre que sur un appui précis | Enchanteur + protecteur si l’on veut filtrer |
| **Alarmes** | Mercure qui mesure un niveau, une chaleur, une charge, et commande une alerte filaire | Enchanteur + praticien de l’effet mesuré |
| **Vivres** | Glacière à décharge réglée vers un récepteur froid | Élémentaliste + enchanteur |
| **Navires et ports** | Pompe de cale, éclairage de quai | Élémentaliste + enchanteur |

### Métiers qui en découlent

| Métier | Ce qu’il vend |
|---|---|
| **Enchanteur de consortium** | L’inscription, et un carnet de spécialistes avec qui accorder. |
| **Entreteneur** | La réparation des supports, sans droit de toucher à l’effet. Le métier le plus répandu de l’école. |
| **Lecteur de grilles** | Ce que fait un ouvrage, pour un tribunal, un assureur, un annulateur ou un voleur. |
| **Fournisseur de gemmes** | L’alimentation. Sans lui, la plus belle grille ne fait rien. |
| **Opérateur** | La conduite des commandes, sans don. C’est par lui qu’une ville fonctionne. |

### Le prix de l’automatisme : l’école de la continuité

L’Enchantement est **conçu pour que le praticien puisse partir** (§ 3). C’est exactement la condition de naissance des Non-Vivants : une continuité qui cesse de dépendre des personnes qui l’assuraient ([doctrine](../../doctrine.md)). Couplé aux gemmes, il est ce qui rend possible l’âge des Non-Vivants. Son sillon se creuse dans la pierre et les métaux gravés ([modèle du Network](../../modele-unifie-network.md)), et sa famille est celle des [Greffiers](../non-vivants/GREFFIERS.md).

**Proposition : l’ouvrage orphelin.** Quand le spécialiste qui a accordé un effet meurt ou s’en va, plus personne ne peut changer cet effet. On peut seulement l’entretenir à l’identique, ou l’arrêter. Une ville qui ne peut ni modifier ni se passer d’une citerne, d’un chauffage d’hospice ou d’une pompe la fait tourner sans fin, réparée et jamais repensée. **L’ouvrage orphelin est le berceau naturel du Greffier**, et le Greffier commence par le faire mieux marcher.

Les employeurs, tarifs, droits sur les accords, sort des ouvrages orphelins et règles d’accès aux archives de grilles restent ouverts.

## ✅ Arbitrages résumés

| Problème du système importé | Décision de cette v1 |
|---|---|
| Confusion Éléments / Enchantement | Grammaire de l’Enchantement ; effets accordés avec leurs spécialistes. |
| Sources infinies | Prises sur des ressources présentes ; alimentation magique bornée. |
| Mage présent pour toujours ou volonté infinie stockée | Accord initial ; exécution alimentée par des sources réelles ou des gemmes préalablement chargées. |
| Polymage contournant toute coopération | Deux participants distincts à l’accord. |
| Flux dupliqué par une bifurcation | Partage du débit. |
| Air à la fois gaz et mouvement universel | Air = gaz déplacé ; efforts sur le support par interaction. |
| Flux disparu sur un blocage | Blocage ou évacuation réelle, avec conséquences matérielles. |
| Boire comme puits absolu | Décharger vers un récepteur réel. |
| Sel comme capacité sans limite | Rétention bornée par l’ouvrage. |
| Mesure donnant une intelligence au bâtiment | Propriété locale explicitement sélectionnée. |
| Grille copiée donnant tous les dons | Inscription, accord spécialisé et alimentation nécessaires. |
| Limitations du moteur devenant lois du monde | Écartées ; règles physiques du monde conservées. |

## ❓ Ce qui reste à dimensionner

Débits, capacités de prélèvement magique, durées d’entretien, tailles des supports, matériaux et calibrations. Les coûts particuliers des autres écoles restent ouverts. Ces paramètres demandent des essais de conception ; ils ne remettent pas en suspens les arbitrages qualitatifs ci-dessus.

Usages institutionnels, en proposition (§ 11) : droits attachés à un accord, sort des ouvrages orphelins, accès aux archives de grilles, possibilité d’accorder des effets d’Espace ou d’Illusions, et seuil de durée à partir duquel un ouvrage en service devient le berceau d’un Greffier.
