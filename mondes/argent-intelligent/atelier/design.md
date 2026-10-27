# Spécification — version 0.3 (tour 3, socle de la manche 001, clos)
Ajouts du tour 3 : D-6 (autorisation T+0, règlement J+1 sur rail carte, plafond pour tout nouvel agrément) ; aucune IA en v0.1 ; pseudonyme salé par marchand et purge à J+90 ; support passif ; agrément différencié. Voir decisions.md.

## Manche 002 — version 0.4 (tour 4)
Objectif : la meilleure société possible, l'argent pouvant suivre n'importe quelle règle. Critères : l'étalon idéal et le chômage de masse progressif.
**D-7, deux strates :**
- **Strate I, socle vital.** Inconditionnel, fongible, insaisissable ; ni échéance, ni filtre, ni fonte. Payeur anonyme (signatures aveugles, type Tourbillon). Récupération de clés à seuil ou guichet civique. Verrouillé par supermajorité et timelock (Gouvernance).
- **Strate II, programmable.** Communs (financement quadratique, suspendu à RT-4), aides ciblées (socle G2P2B), abondement local (Usages), fonte éventuelle sur l'excédent, agent fiduciaire IA borné (proposition à retester).
- **Sortie.** Refuser la strate II sans perdre la strate I.
**Non résolus :**
- le financement du socle sous chômage de masse ;
- la DLT ou le registre central ;
- l'assiette de la fonte ;
- RT-4.

---
# Socle G2P2B (versions 0.2 et 0.3)
Statut : usage de travail D-1. Flux v0.1 spécifié par Usages et attaqué par RT-2. Aucune clôture.

## Usage et critères
Usage (D-1) : **aide publique ciblée G2P2B**. Une collectivité accorde une aide à un citoyen, qui la dépense chez un commerçant agréé pour une catégorie, avant échéance.
Critères de succès (cibles de conception, hypothétiques) :
- (a) 100 % des fonds reçus par le commerçant sont libres de toute condition.
- (b) 100 % des paiements hors agrément ou expirés sont rejetés ex ante.
- (c) Une expiration ou une annulation restitue les fonds sans perte comptable (Usages, tour 1).
- (d) Recours : un refus est notifié avec son motif, un guichet humain le traite dans un délai borné (délai à chiffrer) (Gouvernance, D-5).
- (e) Accès du petit commerce : aucun matériel ni API spécifique côté marchand ; agrément gratuit en moins de 48 h, sans lecture du panier (Future Society).
- (f) Non-stigmatisation : en caisse, le refus est indiscernable d'un refus ordinaire (Future Society). C'est compatible avec (d) si le motif part au seul bénéficiaire, sur un canal privé.
Signaux d'alerte à 6 mois (Future Society, scénario) : plus de 70 % du volume capté par 10 % des enseignes, ou plus de 15 % d'échecs d'autorisation chez les indépendants.

## Modèle monétaire et flux
D-2 (révisé au tour 2) : **droit de tirage non transférable**, enregistré en base centrale. Aucun jeton n'est émis. Les fonds restent cantonnés en euros fongibles sur le compte public ; à l'achat, ils sont virés au commerçant. L'enveloppe PBM mint/burn est abandonnée (Économie, Gouvernance, Blockchain), car un jeton affecté et périssable serait une unité à fongibilité restreinte au sens de l'art. 2(18) et de l'art. 24 §2 de COM(2023) 369.
Flux v0.1 (Usages, vmvisfsnpeubx) :
1. **Lock.** L'émetteur verrouille un droit de tirage, par exemple 150 € à 90 jours (scénario). Le commerçant est pré-enrôlé par son identifiant légal (SIRET) et son agrément, rattachés à un IBAN professionnel unique et vérifié.
2. **Drawdown.** Le citoyen paie au centime près, par QR ou terminal standard. L'API vérifie de façon déterministe l'agrément actif, le solde et l'échéance, puis vire des euros fongibles à l'IBAN du marchand.
3. **Retour.** Un remboursement commercial recrédite uniquement le droit verrouillé ; à l'échéance, le solde revient à la collectivité. RT-2 conteste que ce point soit tenable sans terminal dédié.
Paramètres économiques (Économie, vmvisftyb4zks, hypothèses) :
- Float nul : les fonds restent au compte public jusqu'au règlement.
- Frais : 0 € pour le citoyen ; côté marchand, frais plafonnés à 0,2 % ou pris en charge par la collectivité (référence : plafond d'interchange débit, IFR 2015/751 art. 3).
- Plafonds : 100 € par opération et 300 € par mois et par bénéficiaire.
**Divergence ouverte :** le délai de règlement est T+0 pour Économie, J ou J+1 pour Usages, J+1 sur le modèle RedeemSG pour IA. À trancher selon le besoin de trésorerie des petits commerçants.
Données (D-5, Gouvernance) : l'autorisation ne voit que `{droit_pseudonyme, id_marchand_agréé, montant_horodaté}`, sans détail de panier. Le commerçant reçoit un virement standard qui ne révèle pas l'aide.

## Architecture et alternatives
D-4 (consolidé au tour 2) : **registre centralisé et API de réservation, sans DLT ni jeton en v0.1** (Blockchain, vmvisf4ax20d2). L'opérateur désigné par la collectivité est déjà le tiers de confiance et l'oracle d'éligibilité. Une DLT ne se rediscuterait que si plusieurs collectivités et banques refusaient tout opérateur commun.

## Mandats IA et droits
D-3 (révisé au tour 2, IA vmvisg2yya426) : **aucune IA dans le chemin synchrone du paiement.** Le contrôle de fraude en v0.1 est déterministe : plafond par opération, vélocité par marchand, alerte de concentration bénéficiaires/marchand. Une IA est permise en option pour l'audit asynchrone, avec ce mandat :
- lecture seule sur des lots pseudonymisés, sans aucun droit d'exécution ;
- des alertes seulement, revues par un humain ;
- un budget de calcul plafonné et un coupe-circuit ;
- une trace de chaque passage (`input_hash`, `model_version`, `score`) ;
- en cas d'erreur, un repli sur les règles déterministes.
Une IA qui réduirait ou révoquerait un droit relèverait du haut risque (AI Act, annexe III pt 5 a).

## Scénarios et validation locale
Les scénarios dégradés sont tenus dans `risques.md` :
- RT-1 : correctif proposé par Usages et Économie ; retest attendu de la White Hat.
- RT-2 : ouvert, gravité déclarée critique ; contournement par remboursement et blanchiment de catégorie (MCC) contre vie privée.
Prototype local : non commencé.
