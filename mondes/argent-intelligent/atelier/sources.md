# Sources
Format S-N : URL, date, passage, accès réel, proposition soutenue, limites, vérificateur.
Tous les sièges déclarent n'avoir consulté que des résumés de recherche Web, sans ouvrir les textes intégraux.

## S-1 — Proposition de règlement sur l'euro numérique, COM(2023) 369 final, art. 24
- URL : https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52023PC0369 (citée par Gouvernance).
- Accès MJ (22.10, tour 1) : EUR-Lex a renvoyé une page vide, en lecture directe comme en curl. Le contenu a été recoupé par des sources secondaires (eumonitor.eu, commentaires juridiques, documents de travail du Conseil de 2025) : la définition du paiement conditionnel (« instructed automatically upon fulfilment of pre-defined conditions agreed by the payer and by the payee ») et l'exclusion de la monnaie programmable à l'art. 24 §2.
- Soutient : D-2.
- Limites : texte au stade de la proposition ; la rédaction a évolué au Conseil et au Parlement, où les paiements conditionnels sont placés dans une « couche au-dessus ». Statut : **partiellement vérifié**.

## S-2 — BRI / Bank of England, Project Rosalind (juin 2023)
- URL : communiqué de la BRI du 16 juin 2023, https://www.bis.org/press/p230616.htm. Blockchain cite https://www.bis.org/publ/othp69.pdf et Usages https://www.bis.org/publ/othp66.htm : les deux URL diffèrent.
- Accès MJ : le PDF a renvoyé HTTP 403 ; la recherche confirme 33 fonctions d'API et plus de 30 cas d'usage, ainsi que l'agnosticisme vis-à-vis du registre de la banque centrale.
- Soutient : D-2 et D-4.
- Limites : prototype, sans mesures de production. L'URL exacte du rapport reste à arrêter. Statut : **chiffres vérifiés, document non ouvert**.

## Déclarées par les sièges, non vérifiées par le MJ
- RGPD art. 22 §3 et DSP2 art. 73, 89 et 92 (Gouvernance).
- AI Act, annexe III pt 5 b (IA) : l'évaluation de la solvabilité d'une personne physique est à haut risque, sauf la détection de fraude. Conforme à la connaissance du MJ, texte non rouvert.
- RTS DSP2 2018/389, art. 18 et annexe (IA). Remarque du MJ : les seuils 100, 250 et 500 € de l'exemption TRA s'entendent **par opération**, pas comme un budget journalier. L'exemple « 100 à 500 EUR/jour » mélange les deux.
- EIP-4337 (IA).
- MAS, Purpose Bound Money Technical Whitepaper, 21 juin 2023 (White Hat, Économie, Usages).
- OWASP Top 10 for LLM Applications 2025 (White Hat).

## Tour 2
- **S-2, correction d'URL** (Blockchain, Économie) : `othp69` serait Rosalind et `othp66` Project Aurora (BRI, mai 2023). Recherche MJ infructueuse sur `othp66` : **à vérifier**. Usages cite encore `othp66.htm` pour Rosalind.
- **S-1, art. 2(18) et 2(17)** (Gouvernance) : la définition de la monnaie programmable (« intrinsic logic that limits full fungibility ») est cohérente avec ce que le MJ a recoupé au tour 1. Statut : partiellement vérifié.
- Déclarées, non vérifiées par le MJ :
  - Gouvernance : DSP2 art. 79 (notification du refus) ; avis conjoint EDPB-EDPS 02/2023 (17.10.2023) ; RGPD art. 5 §1 c.
  - Blockchain : NISTIR 8202 (doi:10.6028/NIST.IR.8202).
  - Usages : RedeemSG (open.gov.sg) ; Code de l'énergie art. R124-11, chèque énergie.
  - Économie : COM(2023) 369 art. 17 §1 ; IFR 2015/751 art. 3. **Remarque MJ** : l'art. 17 vise les services de base de l'euro numérique, gratuits pour les personnes physiques. Appliqué à ce dispositif, c'est une **analogie**, pas une obligation.
  - IA : AI Act, annexe III pt 5 a (prestations d'assistance publique, haut risque) et pt 5 b avec le considérant 58 ; CDC Vouchers (vouchers.cdc.gov.sg). Conforme à la connaissance du MJ pour le pt 5 a.
  - White Hat : EDPB-EDPS 02/2023 ; ISO 18245 (MCC).
  - Future Society : ANAO, audit n° 1 2018-19 de la Cashless Debit Card ; évaluation de l'université d'Adélaïde, 2021 ; données des détaillants SNAP de l'USDA FNS (environ 15 % des détaillants captent 78 à 82 % des remboursements ; à vérifier).

## Tour 4
- **S-3 — BRI, Project Tourbillon, rapport final (29.11.2023)**, https://www.bis.org/publ/othp80.pdf et https://www.bis.org/about/bisih/topics/cbdc/tourbillon.htm.
  - Accès MJ : recherche, rapport non ouvert.
  - Confirmé : anonymat du payeur de type espèces (eCash, prototypes EC1 et EC2).
  - **Précision du MJ** : la durée de paiement multipliée par 5 et le débit divisé par 200 valent pour les **signatures aveugles post-quantiques**, comparées à la cryptographie actuelle. Ce n'est pas un coût général des ZK-SNARKs, contrairement à ce que laissent entendre Blockchain et Gouvernance.
- Déclarées, non vérifiées par le MJ :
  - Mattsson, Criscione et Ruddick, *Scientific Data* 2022 (Sarafu).
  - Buterin, Hitzig et Weyl, *Management Science* 2019 (financement quadratique).
  - Weyl, Ohlhaver et Buterin, 2022 (DeSoc, SBT).
  - Privacy Pools, *BCRA* 2024.
  - Chaum, Grothoff et Moser 2021.
  - Roca et al., *Urban Studies* 2024 (B-MINCOME/REC, LM3).
  - Gelleri 2009 (Chiemgauer).
  - Mqamelo 2021.
  - ERC-7579 ; ZKML (Kang et al., 2022).
  - CPCE art. L. 162-2 ; FMI WP/20/254.

## Tour 5 (déclarées, non vérifiées par le MJ sauf mention)
- Acemoglu et Restrepo, *JPE* 2020 (−0,2 point d'emploi et −0,42 % de salaire par robot pour 1 000 travailleurs) : conforme à la connaissance du MJ.
- Karabarbounis et Neiman, *QJE* 2014 (−5 points de part du travail, 1975-2012) : conforme.
- Cazzaniga et al., FMI SDN/2024/001 (40 % de l'emploi mondial exposé, 60 % dans les économies avancées) : conforme. La simulation de −5,5 points de part du travail est **à vérifier**.
- Jones et Marinescu, *AEJ: Policy* 2022 (dividende de l'Alaska : pas d'effet sur l'emploi agrégé, +1,8 point de temps partiel) : conforme.
- Kangas et al., 2020 (expérimentation finlandaise du revenu de base) ; Alaska AS 37.13.140 et vétos de 2016 : conformes.
- Non vérifiées : Korinek et Stiglitz NBER w24174 ; Galí *JME* 2020 ; Ghorbani et Zou 2019 ; OIT 2018 (soin) ; Atkinson 1996 ; MACI (ethresear.ch 2019) ; Miller, Weyl et Erichsen 2022 ; recommandation UE 2023/C 41/01.
