# Registre White Hat
Format RT-N : version, préconditions, scénario simulé, invariant, conséquence, preuve/statut hypothétique, gravité, responsable, correction, retest, statut et risque résiduel.

## RT-1 — Déblocage sur preuve non indépendante (White Hat, vmvis94gralem)
- Version attaquée : v0 (cadrage).
- Préconditions : le déblocage dépend d'une preuve externe soumise par les parties à un oracle ou à une IA dotée de droits d'exécution.
- Scénario : (a) collusion acheteur-marchand par une prestation fictive (cash-out) ; (b) injection de consignes dans un justificatif pour faire appeler l'API de règlement par l'IA.
- Invariant : aucun déblocage sans preuve d'exécution indépendante des parties, isolée des entrées non fiables.
- Gravité : critique si le règlement est automatisé sans contrôle déterministe. Statut de preuve : hypothétique.
- **Correctifs proposés au tour 2**
  - (b) Usages, vmvisfsnpeubx ; IA, vmvisg2yya426 : aucune pièce non structurée ni aucune IA dans l'autorisation ; l'IA reste en audit asynchrone, en lecture seule. Éliminé par construction **sur le papier**.
  - (a) Usages : paiement au centime près, interdiction du rendu de monnaie et du remboursement en espèces, traçabilité fiscale sur l'IBAN professionnel, seuils de vélocité. Économie, vmvisftyb4zks : plafonds de 100 € par opération et 300 € par mois ; calcul illustratif d'un gain partageable de 5 € ou moins sur une vente fictive de 100 €.
- **Remarque MJ sur le calcul (a)** : la dissuasion ne dépend pas seulement du gain unitaire. Elle dépend de la probabilité de détection multipliée par la sanction, et ni l'une ni l'autre n'est posée. Le chiffre de 20 € de fiscalité au moins est une hypothèse non dérivée. À 300 € par mois, un marchand qui tient vingt bénéficiaires complices fait de petits gains unitaires une somme régulière. À préciser au retest.
- Responsable de réponse : Usages et Économie (faits). Retest : **White Hat, attendu**.
- Statut : **correctif proposé**.

## RT-2 — Retour-décaissement et blanchiment de catégorie (MCC) contre vie privée (White Hat, vmvisfyqf03n5)
- Version attaquée : flux v0.1 G2P2B (design 0.2).
- Préconditions : réservation par API qui vérifie agrément × catégorie × échéance ; marchand sans terminal dédié ; monnaie 100 % fongible à l'encaissement.
- Scénario simulé :
  1. Achat éligible, puis retour ou rétractation : le marchand rembourse en espèces, en avoir libre ou sur un compte standard, et non vers le droit verrouillé. L'aide devient de la liquidité libre.
  2. Un marchand multi-catégories vend un bien exclu sous son agrément global ; exiger le détail des articles (SKU, données de niveau 3) pour l'empêcher exposerait les achats de bénéficiaires vulnérables.
- Invariant : l'affectation est maintenue lors des retours et annulations, et les données sont minimisées (RGPD art. 5 §1 c).
- Conséquence : détournement, ou surveillance illicite des bénéficiaires.
- Gravité déclarée : **critique**. Statut de preuve : scénario conceptuel.
- **Note MJ** : la White Hat présente le vecteur 1 comme « sans collusion ». Or le flux v0.1 (point 3) impose que le retour recrédite le droit verrouillé ; un remboursement en espèces exige donc que le marchand enfreigne cette règle, à coût faible. Reste à établir si ce coût est assez faible pour rendre la règle inopérante. La gravité n'est pas modifiée par le MJ. Le vecteur 2 oppose directement les critères (b) et D-5.
- Responsables de réponse : **Usages** pour le routage des remboursements vers le droit initial sans terminal dédié ; **Gouvernance**, avec **Économie**, pour le vecteur 2 (périmètre d'agrément par enseigne ou par catégorie, sans SKU).
- Retest : White Hat, conditions (a) et (b) de son constat.
- Statut : **ouvert**. S'il est démontré et non résolu, il bloque la clôture.

---
## Tour 3 — retests et nouveau constat
- **RT-1 b : retesté et réfuté** par la White Hat (vmvislbrgqlbm), du fait du retrait de l'IA. **Résolu.**
- **RT-1 a : ouvert.** La White Hat note que le calcul fiscal d'Économie tombe pour un marchand en franchise de TVA (CGI art. 293 B) ou au taux réduit.
  - Réponse d'Économie (vmvislppq1l99) : un modèle p × S, avec un gain de 300 € par mois contre 750 € ; audit déclenché par l'écart à la médiane du code APE ; recouvrement.
  - Réponse de Gouvernance : compensation d'office de l'indu.
  - Réponse d'IA : z-score marchand et rapprochement avec les factures grossistes.
  - Paramètres p et S hypothétiques. **Retest attendu.**
- **RT-2 : correctif proposé.**
  - Retours (2.1) : rail carte, le remboursement va au token d'origine (Usages, Blockchain) ; l'art. 13 §1 de la directive 2011/83 impose le même moyen de paiement (Gouvernance).
  - Substitution de catégorie (2.2) : agrément mono-activité, sous-identifiant et sous-total éligible pour les enseignes mixtes (Gouvernance, Économie).
  - La White Hat a précisé un remboursement de bonne foi hors `pacs.004` sur virement instantané. Le rail carte de D-6 y répond sur le papier.
  - **Retest attendu.**
- **RT-3 (nouveau) — marchand éphémère (bust-out)** (White Hat).
  - Scénario : agrément en moins de 48 h, 30 complices à 300 €, encaissement T+0, IBAN vidé avant l'audit J+1.
  - Gravité élevée, critique en T+0.
  - Correctif : D-6 (règlement J+1 et plafond sur tout nouvel agrément). **Correctif proposé, retest attendu.**
- Ces constats restent rattachés au socle G2P2B 0.3. Ils seront retestés si la manche 002 réutilise ce socle.

---
## Tour 4
- **RT-3 : retesté et résolu** par D-6 (White Hat, vmvissoe1m4h7).
- **RT-2.2 : retesté** (NAF mono-activité ou sous-identifiant).
- **RT-2.1 : retesté sur carte EMV.** Il restait ouvert sur le bon QR papier, qui a été abandonné le même tour (Future Society, Usages). **RT-2 est résolu** pour le socle G2P2B, sous réserve de la carte EMV comme support passif.
- **RT-1 a : correctif complété** par Économie : réserve glissante de 15 % sur 30 jours, plafond initial. **Retest attendu.**
- **RT-4 (nouveau, manche 002) — location d'identités, collusion quadratique et évasion de la fonte** (White Hat).
  - Version : monnaie civique à fonte et financement quadratique, avec identités ZK ou SBT.
  - Scénario : (1) un cartel loue les signatures ZK de personnes précaires pour gonfler un faux commun et siphonner l'abondement ; (2) des acteurs avertis échangent leurs avoirs sur une plateforme d'échange décentralisée (DEX) juste avant la ponction, et la fonte retombe sur les ménages captifs.
  - Invariant : inaliénabilité du droit civique, égalité devant l'impôt monétaire. Gravité déclarée : critique. Statut : hypothétique.
  - Effet de D-7 : sur le papier, il réduit le vecteur 2 pour les ménages, puisque la strate I ne fond pas. Le vecteur 1 reste entier.
  - Responsables : **Économie** (fonte : base et assiette), **Blockchain** et **IA** (anti-collusion : pénalité de corrélation, preuve d'unicité, réalité de la détection ZKML).
  - Statut : **ouvert**.

---
## Tour 5
- **RT-1 a : retesté et résolu** (White Hat, vmvisz3qb97uu) par la réserve glissante de 15 % sur 30 jours et l'audit grossiste. **RT-2.1 : retesté et résolu.** Tous les constats de la manche 001 sont résolus.
- **RT-4 : correctifs proposés.**
  - Blockchain et IA : MACI (le changement de clé chiffré rend le vote invendable) et financement quadratique par paires.
  - Gouvernance : droit inaliénable de régénérer sa clé au guichet.
  - Usages : abondement plafonné à 100 € par mois, à la place d'un financement quadratique non plafonné.
  - Future Society : voix civiques égalitaires.
  - **Note MJ** : MACI suppose un coordinateur de confiance pour le secret des votes (limite déclarée par Blockchain), et la location d'un support physique échappe au changement de clé. **Retest attendu.**
- **RT-5 (nouveau) — évasion d'assiette et stagflation du socle** (White Hat).
  - Scénario : (1) des producteurs automatisés compensent leurs flux B2B hors registre et fuient vers des actifs externes ; (2) un socle financé par émission non gagée subit une décote face aux monopoles d'IA et d'énergie qui facturent en devises ou en kWh.
  - Invariant : prélèvement réel ≥ strate I + abondement. Gravité déclarée : critique.
  - Retest : gager D-7 sur des facteurs non délocalisables (foncier, énergie et calcul, actions en fiducie).
  - Aggravé par le calcul MJ de D-8 : un taux de 46 % sur la valeur ajoutée non salariale à αₜ = 35 % accroît l'incitation à l'évasion.
  - Responsables : **Économie** (assiette, taux) et **Gouvernance** (assiette non délocalisable, coercition).
  - Statut : **ouvert**.

---
## Tour 6, premier lot
- **RT-5 : correctif proposé.**
  - Économie F-7 : un plancher foncier, énergie et calcul. L'OCDE chiffre l'impôt foncier récurrent à environ 1,03 % du PIB en 2019 : c'est un plancher, pas un financement complet.
  - Économie et Blockchain : un coupe-circuit sans monétisation, le ratio recettes / droits rendu public.
  - Entreprises et institutions : un surplus net, une franchise PME, pas de rétroactivité.
  - Effet de D-9 : RT-5 se déplace vers la **concentration des droits futurs**. Parade proposée : publier le bénéficiaire effectif agrégé (Blockchain).
  - **Retest attendu de la White Hat**, dont le pilote a été coupé avant son coup.
- **RT-4** : l'option voix égalitaires retire l'amplification monétaire ; la location d'identités reste possible, mais à effet linéaire. **Retest attendu.**
