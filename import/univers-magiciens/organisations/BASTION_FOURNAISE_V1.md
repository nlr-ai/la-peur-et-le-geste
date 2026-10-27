# 🔥 La Fournaise à chaleur conduite — détail et épreuves v1

[← Manuel des recettes](BASTION_DEFENSE_RECETTES_V1.md) · [Bastion](01-bastion.md) · [Carte](../visuels/bastion-v1.svg)

## 📌 Statut

Développement proposé de R11–R12. La première application défensive détaillée chauffe une surface extérieure. La projection de flammes exige un développement distinct.

Les quatre épreuves sont des scénarios de conception, pas des essais réalisés. Températures, débits thermiques, capacités, consommations et délais restent à dimensionner.

## 🎯 Fonction

Les foyers du Bastion servent quotidiennement aux ateliers. En défense, une partie de leur chaleur est dirigée vers les ouvrages menacés.

**Question centrale : changer la destination de la chaleur sans rendre les quartiers inhabitables.**

La chaleur provient d’une source réelle. Le changement de destination ne multiplie pas l’énergie disponible.

## 🧩 Montage

```text
                         → Ateliers
Foyer → Collecteur chaud → Circuit défensif extérieur
                         → Dissipateur

Foyer → Cheminée → Extérieur : trajet matériel des fumées
```

Trois branches séparées, avec commandes locales. Le dissipateur doit rester disponible lorsque les autres branches ferment ; cela exige un montage adapté et ne découle pas d’une correction magique automatique.

| Pièce | Fonction |
|---|---|
| Foyer | Produire de la chaleur en consommant combustible et air |
| Collecteur | Recevoir la chaleur et fournir les prises élémentaires |
| Branches | Conduire la chaleur vers des destinations préparées |
| Régulation | Mesurer les supports et réduire les admissions lorsqu’ils deviennent trop chauds |
| Dissipateur | Recevoir la chaleur dont les autres usages ne peuvent disposer |
| Cheminée | Évacuer les fumées par un trajet matériel distinct |

Les fumées ne suivent pas automatiquement le transfert magique de chaleur. Elles restent à évacuer depuis le foyer.

## ✨ Rôles des magies

- **[Matière](../magies/MATIERE_V1.md)** : préparer supports, joints et contenants. La modification de conductivité thermique n’a pas encore sa recette complète ; elle n’est pas supposée acquise ici.
- **[Élémentaire](../magies/ELEMENTAIRE_V1.md)** : prendre et conduire la chaleur disponible, par paroles, gestes, runes et cercles préparés.
- **[Enchantement](../magies/ENCHANTEMENT_V1.md)** : fixer les opérations répétables et leurs régulations avec les spécialistes concernés.
- **[Protection](../magies/PROTECTION_V1.md)** : protéger les zones exposées avec des filtres thermiques et leurs récepteurs réels.

La volonté et les commandes ne produisent pas d’énergie. Un transfert ou un mécanisme demandant un travail supplémentaire doit disposer d’une alimentation réelle.

## ⚒️ Préparation de l’ouvrage

1. Construire foyer, arrivée d’air et cheminée capables de fonctionner matériellement.
2. Installer le collecteur et identifier les contraintes thermiques de ses appuis.
3. Préparer les trois trajets avec des moyens de sectionnement accessibles.
4. Désigner une destination réelle pour chaque transfert.
5. Prévoir l’évacuation de chaleur du dissipateur ; sa capacité n’est pas infinie.
6. Installer les mesures locales et les commandes de branches.
7. Réaliser les accords entre praticiens pour les procédures enchantées.
8. Préparer des coupures indépendantes et des moyens de réduire la production au foyer.

Cette séquence ne fixe pas de dimensions ni de recette de combustible. Les matériaux doivent être éprouvés selon leurs capacités effectives.

## ⚙️ Régulation et conduite

La régulation de référence reprend R11 : une prise de chaleur, un Mercure Chaud et un Barrer sur supports appropriés. La mesure commande le transfert concerné ; elle ne contrôle pas à elle seule toute la combustion.

- Vérifier la disponibilité des destinations avant ouverture.
- Choisir la répartition entre usages civils et défense.
- Surveiller l’échauffement des supports et des récepteurs.
- Garder un moyen d’isoler une branche sans abandonner la chaleur restante sans issue.
- Réduire la production si les destinations ne peuvent plus recevoir.

**Barrer sans Trace reste ouvert.** La perte d’un capteur est donc un cas de défaillance à traiter par une coupure indépendante, pas un arrêt sûr implicite.

## ⚔️ Première recette défensive : les dalles d’approche

Une portion de surface extérieure reçoit la chaleur conduite depuis le collecteur.

- Les dalles chauffent et deviennent difficiles à traverser ou à occuper selon leur température réelle.
- Leur comportement dépend de la matière, de la chaleur reçue et des pertes.
- Les appuis et les structures voisines reçoivent aussi des contraintes à considérer.
- La chaleur accumulée demeure après fermeture de l’admission.

Cette première recette n’inclut pas de projection de flammes. Une flamme demande combustible et conditions de combustion au lieu où elle se produit.

## 🧪 Quatre épreuves

### A. Fermeture de la branche défensive

Le foyer continue de produire de la chaleur après la fermeture de cette branche.

**À examiner :** destination du surplus, capacité du dissipateur et réduction éventuelle de production. Fermer une commande ne supprime pas l’énergie.

### B. Perte de la mesure

Le capteur ou son fil cesse de transmettre. Le Barrer reste ouvert.

**À examiner :** possibilité d’isoler le transfert par une commande indépendante et d’empêcher la surchauffe des supports. Aucun capteur de secours n’est supposé présent sans être ajouté au montage.

### C. Dissipateur saturé

Le récepteur ne peut plus évacuer suffisamment la chaleur entrante.

**À examiner :** réduction de production, autre destination disponible ou échauffement subi de l’installation. Une nouvelle branche ne constitue une solution que si elle possède un récepteur capable de recevoir.

### D. Perte de toute magie

Le transfert enchanté s’arrête, mais le feu peut continuer à brûler. Les supports restent chauds.

**À examiner :** fonctionnement matériel de la cheminée, accès aux manœuvres du foyer, tenue des structures et gestion de la chaleur résiduelle.

## 🔧 Arrêt et entretien

- Réduire la production et isoler les transferts selon l’état des récepteurs.
- Maintenir l’évacuation nécessaire des fumées et de la chaleur résiduelle.
- Attendre ou organiser le refroidissement réel avant réparation.
- Examiner collecteur, joints, supports, capteurs et sectionnements.
- Rééprouver les voies civiles et défensives après modification.

Un ordre d’arrêt n’est jamais un refroidissement instantané.

## 🌑 Rencontre avec un Obstiné

Un Obstiné pourrait trouver dans le réseau les ressources nécessaires à la poursuite de sa commande.

Couper le contrôle ne suffit pas forcément : il faut aussi isoler les ressources thermiques ou le combustible auxquels il accède. Sa capacité exacte à exploiter les circuits reste à définir.

**Dilemme d’Héloïse : arrêter une fournaise qui défend le rempart avant qu’elle ne mette le quartier en danger.**

## ❓ À dimensionner

Matériaux, températures admissibles, puissances et débits, capacité et refroidissement des récepteurs, inertie du foyer, délais d’arrêt, besoins d’alimentation auxiliaire, protections des habitants et comportement précis des Obstinés.

