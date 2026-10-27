# 🚧 Les Quartiers articulés — détail et épreuves v1

[← Manuel des recettes](BASTION_DEFENSE_RECETTES_V1.md) · [Bastion](01-bastion.md) · [Carte](../visuels/bastion-v1.svg)

## 📌 Statut

Développement proposé de R09–R10, enregistré à la demande de l’utilisateur. Les dispositions et procédures décrivent la v1 ; dimensions, effectifs, capacités et temps de manœuvre restent ouverts. Les épreuves sont des scénarios de conception, pas des essais réalisés.

## 🎯 Fonction

**Fermer une brèche sans condamner toute la ville.**

Certaines rues peuvent devenir des enceintes intérieures. Les habitants connaissent leurs voies de repli ; les équipes manœuvrent des ouvrages préparés. La ville ne se reconfigure pas instantanément et ne crée pas de nouveaux espaces.

## 🧩 Unité : le carrefour de fermeture

```text
                 Rue extérieure
                       │
                 [Porte de front]
                       │
Quartier voisin ── Place de relève ── Quartier voisin
                       │
                 [Porte de fond]
                       │
                  Refuge intérieur
```

La place permet d’accueillir les derniers arrivants, de faire passer les secours et d’organiser une seconde défense.

Les deux portes sont indépendantes : perdre celle de front ne doit pas provoquer mécaniquement la perte de celle de fond. Cette indépendance demande des appuis, commandes et alimentations adaptés ; elle n’est pas une propriété magique implicite.

## ⚒️ Les cinq pièces

| Pièce | Fonction | Réalisation |
|---|---|---|
| Porte de front | Fermer la rue exposée | Panneau préparé en Matière, assistance élémentaire, filtre protecteur optionnel |
| Porte de fond | Isoler la place si elle est perdue | Installation distincte, appuis et commandes propres |
| Passages latéraux | Relier les quartiers pendant le repli | Voies réellement construites, fermables séparément |
| Loges de manœuvre | Commander chaque fermeture depuis un emplacement abrité | Commandes enchantées locales et mécanisme manuel de secours |
| Postes de relève | Recevoir équipes et blessés en transit | Réserves courtes, matériel de réparation et accès au refuge |

Un poste de relève ne remplace pas une Maison de veille dotée de ses propres réserves et capacités d’accueil.

## ⚙️ Le panneau coulissant

La variante choisie pour ce développement est un **panneau coulissant horizontal dans une galerie latérale**.

- **[Matière](../magies/MATIERE_V1.md)** règle les propriétés du panneau, du rail et des fixations.
- **[Élémentaire](../magies/ELEMENTAIRE_V1.md)** conduit un flux réel d’eau ou d’air qui entraîne un mécanisme.
- **[Enchantement](../magies/ENCHANTEMENT_V1.md)** fixe une procédure de manœuvre avec le praticien concerné.
- Un **verrou matériel** reprend les efforts lorsque le panneau est fermé.
- Une **[Porte cousue](BASTION_PORTE_COUSUE_V1.md)** peut ajouter un filtre devant le panneau ; elle reste une installation distincte.

La gemme fournit le travail de manœuvre. Elle n’a pas à pousser continuellement pour maintenir fermé un panneau correctement verrouillé.

La galerie de retrait occupe un volume réel dans le quartier. Elle ne peut pas être simultanément un logement ou une réserve encombrée sans empêcher la manœuvre.

## 🔧 Préparer l’installation

1. Réserver le volume de retrait du panneau et les voies de circulation.
2. Préparer et éprouver appuis, rail, fixations et propriétés du panneau.
3. Installer le mécanisme de mouvement, le verrou et les moyens de reprise.
4. Prévoir une commande locale, un arrêt de manœuvre et l’alimentation réelle.
5. Accorder les procédures enchantées entre praticiens distincts.
6. Prévoir une reprise manuelle ou le changement de réserve.
7. Vérifier l’indépendance de la seconde porte.
8. Exercer les équipes et les trajets de repli.

Le frein de course, la transmission, le mécanisme manuel et les signaux entre équipes restent à concevoir en détail. Leur présence est une exigence de la recette, pas une solution technique déjà démontrée.

## 👐 Responsabilités

Deux fonctions sont distinguées :

- **Responsable de passage :** vérifie la situation réelle de la rue et confirme qu’elle peut être fermée.
- **Manœuvrier :** conduit le mécanisme et peut arrêter le mouvement.

Le commandement central peut demander une fermeture. L’équipe locale regarde ce qui se trouve réellement dans la zone : aucun enchantement ne reconnaît automatiquement un retardataire, un blessé ou un obstacle.

Les effectifs et les règles précises d’arbitrage entre centre et équipe restent ouverts.

## 🔔 Trois états

### 1. Ouvert

Les panneaux sont retirés dans leurs galeries. La circulation ordinaire est possible ; les emprises de fermeture et les rails restent dégagés.

### 2. Repli

La porte de front se prépare à fermer. Les passages latéraux et la porte de fond permettent encore l’évacuation.

La fermeture est un mouvement réel, pas un changement d’état instantané. Son délai reste à dimensionner.

### 3. Compartimenté

La porte de front est fermée et verrouillée. Si la place devient intenable, les équipes gagnent l’intérieur puis ferment la porte de fond.

Il n’existe pas de commande unique qui ferme automatiquement toutes les voies sans tenir compte des personnes et des trajets.

## 🧪 Quatre épreuves

### A. Gemme vide à mi-course

**À obtenir :** arrêter le panneau sans mouvement incontrôlé, puis reprendre la manœuvre par un mécanisme manuel ou une autre réserve.

**À définir :** dispositif de freinage et de reprise. Une absence de puissance ne garantit pas à elle seule l’immobilité.

### B. Débris sur le rail

**À obtenir :** interrompre la manœuvre et évaluer l’obstacle.

Augmenter la puissance peut endommager le panneau, le rail ou ce qui bloque. Aucune détection intelligente n’est supposée.

### C. Ordre central perdu

**À obtenir :** conserver commandes locales et procédure de repli connue.

La perte de transmission ne doit pas supprimer les moyens matériels de manœuvre. Les équipes doivent pouvoir constater l’état des accès dont elles ont la charge.

### D. Porte de front détruite

**À obtenir :** rejoindre la seconde ligne sans perdre ses appuis ou ses commandes du seul fait de la première rupture.

**À examiner :** circulation encore possible, débris, indépendance réelle des deux installations et capacité à fermer derrière les équipes.

## 🔋 Contraintes et entretien

- Travail de mouvement fourni par une source réelle ; aucun gain gratuit d’énergie.
- Les charges d’une porte verrouillée sont reprises par les supports.
- Une gemme neuve ne répare ni rail ni montant.
- Inspecter galeries, rails, fixations, verrous, commandes et accès.
- Reprendre les charges avant une modification de Matière.
- Garder les emprises dégagées en temps de paix.
- Tester le retour à une manœuvre non magique lorsque l’état de l’installation le permet.

## 🌑 Enjeu humain

**Fermer protège des personnes en séparant physiquement ceux qui restent de chaque côté.**

Héloïse peut demander de tenir la place ouverte. Le manœuvrier voit les derniers habitants arriver, mais aussi le montant qui se fissure.

Le choix porte sur le moment de la fermeture, avec des informations incomplètes et une porte qui met réellement du temps à bouger.

## ❓ À préciser

Géométrie, masses, matériaux, vitesse de manœuvre, freinage, reprise manuelle, alimentation, signaux, effectifs, arbitrage des ordres et conditions d’abandon d’une place. Aucun de ces paramètres n’est chiffré ici.

