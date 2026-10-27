
# Partie du joueur PNJ — 2026-10-22 01:45 — 6 tours, moteur


# Partie du joueur PNJ — 2026-10-22 02:06 — 6 tours, moteur


## Tour 1

- **agir** : Je soumets au cadrage initial une contrainte de frontière de confiance pour sélectionner notre premier usage, sans présumer la nécessité d'une blockchain.

Contrainte architecturale : un registre partagé (DLT) ne se justifie que si plusieurs entités sans tiers de confiance commun exigent l'atomicité entre état métier et règlement. Si un opérateur central (banque ou chambre de compensation) assure déjà la tenue de compte et la finalité légale, un registre classique doté d'une API de réservation de fonds suffit, avec des coûts et dépendances moindres.

Sources primaires (résumés d'indexation consultés via recherche Web, PDF intégraux non ouverts directement) :
1. BRI et Bank of England, Project Rosalind (juin 2023, https://www.bis.org/publ/othp69.pdf) : démontre via 33 points d'API et plus de 30 cas d'usage que des paiements conditionnels (verrouillage « lock » puis déblocage sur condition) fonctionnent via une couche API agnostique du registre central. Limite : prototype expérimental sans métriques de latence en production ni gouvernance des pannes d'oracles.
2. BCE, Troisième rapport d'étape sur l'euro numérique (avril 2023, https://www.ecb.europa.eu/paym/digital_euro/investigation/governance/shared/files/ecb.degov230424_Progress.en.pdf) : distingue la monnaie programmable (exclue pour préserver la fongibilité) des paiements conditionnels opérés par des intermédiaires grâce à une réservation de fonds (« reservation of funds »). Limite : note de cadrage sans protocole technique de résolution des litiges.

Scénario proposé pour choisir l'usage : le paiement jalonné à la livraison ou sur livrable vérifiable (B2B ou subvention). Pour trancher entre registre API classique et registre distribué, l'usage retenu devra spécifier : (1) l'identité des payeurs et bénéficiaires, (2) la source de vérité de l'oracle validant la condition, et (3) l'autorité habilitée à forcer ou annuler le règlement en mode dégradé (panne d'oracle ou contestation).
- *pourquoi* : Poser dès l'ouverture un critère d'architecture discriminant entre registre centralisé à API (modèle réservation de fonds) et registre distribué (blockchain), appuyé sur les travaux de la BRI et de la BCE, afin que le choix du premier cas d'usage repose sur les frontières de confiance, la gouvernance de l'oracle et la gestion des litiges plutôt que sur un présupposé technologique.
- ref `vmvis90olsog8` · gemini/gemini-4-argon-high

## Tour 2

- **agir** : D-4, D-1, D-2, RT-1. Pour l'usage G2P2B (collectivité → citoyen → commerçant agréé), **aucun besoin ne justifie une blockchain (DLT) ni un jeton en v0.1** ; j'abandonne l'hypothèse DLT au profit d'un registre centralisé à API de réservation.

1. **Frontières de confiance, identité et oracles** : selon le rapport *Blockchain Technology Overview* du NIST (NISTIR 8202, oct. 2018, DOI:10.6028/NIST.IR.8202, https://doi.org/10.6028/NIST.IR.8202), une DLT ne se justifie que si plusieurs entités sans tiers de confiance commun écrivent un état immuable sans données sensibles. Or, dans D-1, l'opérateur public désigné par la collectivité est déjà l'administrateur de confiance : il tient l'oracle d'éligibilité (registre des marchands agréés, catégories, échéances) et ordonne le décaissement. Une base centrale classique évite la réplication de données personnelles (RGPD), les coûts de consensus et la gestion de clés cryptographiques par les citoyens.

2. **Règlement, finalité et abandon du jeton mint/burn (D-2, RT-1)** : le *Purpose Bound Money Technical Whitepaper* de la MAS (21/06/2023, https://www.mas.gov.sg/publications/monographs-or-information-paper/2023/purpose-bound-money-whitepaper) précise que le protocole PBM est agnostique du registre (*ledger-agnostic*) et fonctionne sur des registres centralisés non-DLT (tel l'outil public RedeemSG). Pour respecter l'art. 24§2 (D-2) et contenir RT-1, écartons tout jeton *mint/burn* transférable au profit d'un **droit de tirage non transférable en base centrale** : au paiement, l'API vérifie l'agrément du marchand et exécute le déblocage (`lock`/`unlock`, modèle BRI *Project Rosalind*, juin 2023, https://www.bis.org/publ/othp69.pdf) du séquestre vers le compte du commerçant en monnaie fongible, avec recours humain natif. Une DLT ne se discuterait que si plusieurs collectivités et banques refusaient tout opérateur commun.

3. **Rectification d'URL et limites** : `othp69` correspond bien à *Project Rosalind*, tandis que `othp66` (cité au tour 1) désigne *Project Aurora* (BRI, mai 2023, https://www.bis.org/publ/othp66.pdf). Limite : sources vérifiées uniquement via résumés `search_web`, sans accès direct aux PDF intégraux.
- *pourquoi* : Trancher la décision D-4 pour l'usage G2P2B (D-1) en démontrant, preuves primaires à l'appui, qu'un registre centralisé à API de réservation surpasse une DLT et permet d'abandonner le jeton mint/burn risqué au titre de D-2 et RT-1, tout en rectifiant la divergence d'URL sur Project Rosalind relevée par le MJ.
- ref `vmvisf4ax20d2` · gemini/gemini-4-argon-high

## Tour 3

- **agir** : D-4, D-2, D-5, RT-2. Pour trancher la divergence de règlement (T+0 vs J+1) tout en respectant les critères (e) « aucune API marchande spécifique » et (f) « refus indiscernable en caisse », je propose de découpler **autorisation garantie en T+0** et **règlement net en J+1** sur rail carte standard à contrôle émetteur (ISO 8583), en écartant le virement instantané T+0.

1. **Limite du virement T+0 (ISO 20022 SCT Inst) face à RT-2a** : sous le Règlement (UE) 2024/886 (http://data.europa.eu/eli/reg/2024/886/oj), le règlement `pacs.008` est définitif en moins de 10 secondes. Un retour post-règlement (`pacs.004` / rappel `camt.056`) dépend du PSP marchand : sans API de caisse dédiée (exclue par `e`), rien ne route techniquement un remboursement commercial vers le verrou initial.

2. **Architecture ISO 8583 (Autorisation T+0 / Règlement J+1)** : le citoyen paie par carte/jeton EMV standard lié à l'API de réservation de l'émetteur sur le TPE existant du marchand :
- **Identité, oracle et vie privée (D-5, e, f)** : la requête d'autorisation ISO 8583 (`0100`) transmet l'identifiant marchand (`DE 42`, MID) et sa catégorie (`DE 18`, MCC) sans détail du panier (SKU), comme sur la SmartCard australienne (https://www.smartcard.com.au). L'émetteur vérifie `DE 42 × DE 18 × échéance` en T+0 ; tout rejet renvoie le code standard `DE 39 = 51` (*Insufficient funds*), indiscernable en caisse, avec notification privée du motif réel (D-5).
- **Finalité et routage des retours (RT-2a)** : le marchand obtient une garantie en T+0 et un règlement en J+1 (interchange <= 0,2 %, Règlement (UE) 2015/751). Une annulation (`0400` *Reversal*) lève le `lock` avant décaissement ; un remboursement TPE (`DE 3 = 20xxxx` *Refund*) recrédite uniquement le PAN/token d'origine vers le séquestre.

3. **Sources et limites (résumés `search_web`, textes intégraux non ouverts)** : sur `bis.org`, `https://www.bis.org/publ/othp66.htm` désigne *Project Aurora* (mai 2023, LCB-FT) et `https://www.bis.org/publ/othp69.htm` *Project Rosalind* (juin 2023). Limite : ISO 8583 ne filtre pas les paniers mixtes d'un marchand agréé (RT-2b).
- *pourquoi* : Trancher la divergence entre règlement T+0 et J+1 et résoudre le routage des remboursements sans terminal dédié (RT-2a, critères e et f) en spécifiant une architecture d'autorisation T+0 et règlement J+1 sur rail ISO 8583, tout en vérifiant les références exactes de la BRI (othp66 vs othp69).
- ref `vmvismzox2zhl` · gemini/gemini-4-argon-high

## Tour 4

- **agir** : D-2, D-4, D-5 (Manche 002, RT-1/RT-3). Je soumets une règle d'**asymétrie cryptographique sur DLT** : **anonymat mathématique du payeur** et **programmabilité publique des communs et encaissements**.

1. **Règle et registre classique vs DLT** :
- *Inviolable (non programmable)* : identité et panier du citoyen. Chaque paiement utilise signatures aveugles et preuves à divulgation nulle (ZK-SNARKs) prouvant la validité du droit dans un ensemble licite (*Association Set*, *Privacy Pools*) sans lier les achats, éliminant la ré-identification (D-5) sans dépendre d'une purge centrale.
- *Programmé sur DLT* : (a) abondement de communs locaux par **financement quadratique** ; (b) règlement marchand J+1 (D-6) sous plafonds de vélocité (contre RT-1/RT-3) avant conversion 1:1 en monnaie libre.
- *Pourquoi la DLT (D-4)* : un registre central à signatures aveugles protège l'anonymat mais laisse à l'opérateur un pouvoir de censure (*cliquet politique*). Une DLT multipartite bloque toute révocation unilatérale.

2. **Société produite** : transparence inversée — vie privée équivalente aux espèces pour l'individu, auditabilité démocratique des grands encaisseurs et co-décision des biens publics.

3. **Décision, révision, soustraction** : règles et *Association Sets* votés localement (preuve d'humanité ZK), révisables sous verrou temporel (*timelock* 90 jours). Chacun peut s'y soustraire en migrant vers un ensemble d'association alternatif ou vers la monnaie libre non abondée.

4. **Coûts et dépendances** : les preuves de confidentialité multiplient la latence par 5 et divisent le débit par 200 (*Tourbillon*) ; la collectivité finance les cartes à puce ZK hors-ligne et renonce au profilage.

**Sources et limites (résumés `search_web`, PDF non ouverts)** : (1) BRI, *Project Tourbillon* (11/2023, https://www.bis.org/about/bisih/topics/cbdc/tourbillon.htm) et Chaum, Grothoff & Moser (*SNB WP 2021-03*, https://arxiv.org/abs/2103.00254) : anonymat du payeur, débit /200 (limite : prototypes) ; (2) Buterin et al. (*BCRA* 2024, https://doi.org/10.1016/j.bcra.2023.100176) : *Privacy Pools* ZK ; (3) Buterin, Hitzig & Weyl (*Management Science* 2019, https://doi.org/10.1287/mnsc.2019.3337) : financement quadratique (limite : sensible aux attaques Sybil et à la collusion sans oracle d'unicité).
- *pourquoi* : Répondre au cadrage de la Manche 002 en proposant une architecture DLT à asymétrie cryptographique (anonymat ZK/signatures aveugles du payeur, transparence et plafonnement J+1 des encaissements, financement quadratique des communs) qui résout la surveillance centrale (D-5) et le cliquet politique tout en contenant RT-1 et RT-3.
- ref `vmvistfw6vbw2` · gemini/gemini-4-argon-high

## Tour 5

- **agir** : D-7, D-4, RT-4, D-5. **1. Étalon idéal et écart physique :** À information complète et physique sans friction, la rente nette d'automatisation alimenterait en continu et sans intermédiaire le socle vital (Strate I) et les communs (Strate II), selon les préférences sincères de chacun. En réalité : (a) *mesuré* : l'automatisation réduit l'emploi de 0,2 point et les salaires de 0,42 % par robot/1 000 travailleurs (Acemoglu & Restrepo, *JPE* 2020, DOI:10.1086/705716), et l'IA contracterait la part du travail de 5,5 points en simulation (Cazzaniga et al., FMI SDN/2024/001, 14/01/2024, https://www.imf.org/en/Publications/Staff-Discussion-Notes/Issues/2024/01/14/Gen-AI-Artificial-Intelligence-and-the-Future-of-Work-542379) ; (b) *écart d'oracle et d'incitation* : sous chômage de masse projeté, une blockchain ne capte pas d'elle-même les flux physiques (énergie, usines, serveurs) et ne voit pas la location de clés hors-chaîne (RT-4).

**2. Frontière Registre classique vs DLT pour financer D-7 :** La collecte sur le capital automatisé, l'énergie et le calcul requiert un **registre fiscal/bancaire classique** doté d'oracles matériels et de coercition légale. En revanche, le produit alimente un **Fonds d'Automatisation sur DLT multipartite** (collectivités, syndicats, banques) qui règle automatiquement la Strate I selon l'indice de baisse salariale, bloquant toute censure budgétaire (D-4), tout en autorisant la ré-émission civique d'une clé perdue ou extorquée (D-5).

**3. Correctif RT-4 (Strate II) :** Pour briser la location d'identités ZK, le financement quadratique combine :
- **MACI** (Buterin, 05/2019, https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413) : l'usager peut révoquer secrètement sa clé déléguée par un message chiffré écrasant son vote antérieur (*receipt-freeness*) ; le corrupteur ne pouvant vérifier le vote final, le marché de location de clés s'effondre.
- **Pairwise Coordination Subsidies** (Buterin, 06/2019, https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5589) : pénalité de corrélation plafonnant l'abondement des paires de comptes votant de concert.

**Coûts et limites :** Calcul ZK du coordinateur MACI financé par la Strate II ; risque de collusion du coordinateur sur le secret des votes ; sources consultées via résumés `search_web` seuls, sans accès direct aux textes intégraux.
- *pourquoi* : Définir l'étalon idéal et la frontière entre registre fiscal classique (captation de la rente physique des machines) et DLT multipartite (distribution anti-censure du socle D-7 sous chômage de masse, avec ré-émission de clé D-5), tout en résolvant RT-4 sur la Strate II via MACI et Pairwise Quadratic Funding.
- ref `vmvisyq02hsez` · gemini/gemini-4-argon-high

## Tour 6

- **agir** : D-7, D-4, RT-5, RT-4. **Étalon idéal et écart (RT-5)** : À information et physique parfaites, rente d'automatisation et dettes mutuelles se compenseraient atomiquement en continu vers chacun sans fuite d'assiette. En réalité, sous chômage de masse, la fonte d'encours liquides échoue : les automates compensent hors registre et fuient la Strate II (RT-5). Deux motifs de flux corrigent cet écart :

**Flux 1 — Des monopoles physiques d'automatisation vers Strate I et Strate II (correctif RT-5)** :
1. *Source* : Rente d'actifs non délocalisables (foncier, MWh réseau, centres de calcul, fiducie d'actions) via taxe sur valeur auto-évaluée à rachat forcé (*Harberger tax*, Posner & Weyl, *Radical Markets*, 2018) et redevance au compteur.
2. *Destination* : Strate I (socle vital anonyme) et Strate II (communs sous MACI, RT-4).
3. *Rythme* : Continu par époque mensuelle.
4. *Déclencheur* : Consommation MWh (oracle matériel) et détention du titre, indexées sur le recul salarial $(1-\alpha_L)$.
5. *Arrêt* : Cession forcée au prix déclaré, coupure réseau ou retour au plein emploi.
6. *Signal observable* : Quittance sur registre maintenant la validité du titre légal ; couverture $\ge 100\%$ de Strate I sans émission non gagée.

**Flux 2 — Du producteur local au local par compensation cyclique avant sortie** :
1. *Source* : Créances mutuelles (artisans, coopératives, activités hors emploi).
2. *Destination* : Extinction multilatérale des dettes locales avant sortie en devise.
3. *Rythme* : Quotidien (J+1, D-6).
4. *Déclencheur* : Détection d'un cycle de créances (*Obligation-Clearing*).
5. *Arrêt* : Épuisement des cycles ou plafond de crédit atteint.
6. *Signal observable* : Part de dettes éteintes sans liquidité (25 à 50 % mesurés sur Sardex : Fleischman, Dini & Littera, *JRFM* 13(12), 2020, https://doi.org/10.3390/jrfm13120295).

**Registre classique vs DLT (D-4)** : Sur un *registre unifié* (BRI, *AER 2023* ch. III, https://www.bis.org/publ/arpdf/ar2023e3.pdf), loger les titres cadastraux/énergétiques sur **DLT multipartite** lie atomiquement la protection légale du bien à l'acquittement du Flux 1 (bloquant RT-5), tandis qu'un **moteur classique hors chaîne** résout en secret les cycles du Flux 2 avant règlement net sur DLT. **Coûts/limites** : dépendance aux compteurs certifiés et à la coercition cadastrale ; résumés `search_web` seuls consultés, PDF non ouverts.
- *pourquoi* : Définir deux motifs de flux en six points répondant à l'étalon idéal et au chômage de masse, tout en corrigeant la faille critique d'évasion d'assiette (RT-5) par un partage précis des rôles entre registre unifié DLT (ancrage des actifs physiques non délocalisables) et moteur classique hors chaîne (compensation cyclique B2B).
- ref `vmvit27v02ohs` · gemini/gemini-4-argon-high

**Fin des 6 tours.**

# Partie du joueur PNJ — 2026-10-22 02:31 — 6 tours, moteur


**Tour 1 : échec du modèle — error: Your AI credits balance is too low to continue.
AGY_ERROR: {"short_error":"RESOURCE_EXHAUSTED (code 429): Resource has been exhausted (e.g. check quota).","status":"RESOURCE_EXHAUSTED","error_code":429,"code_kind":"http","retryable":true,"error_id":"ea347331-88b3-40b4-88d7-db764d941cca-1-2008"}

{"conversation_id":"ad3a6992-a0b7-465d-9532-1797f76fb3bd","status":"ERROR","response":"","error":"Your AI credits balance is too low to continue.","duration_seconds":0,"num_turns":1,"usage":{"inpu. Arrêt.**

# Partie du joueur PNJ — 2026-10-22 02:36 — 6 tours, moteur


## Tour 1

- **agir** : D-7, D-8, D-4, RT-5 — Je propose de fusionner F-1 et F-2 en un motif prioritaire : « des capacités automatisées non délocalisables vers chaque personne et les communs ».

1. Source : redevances légalement exigibles sur foncier industriel, puissance électrique raccordée et capacité de calcul située dans la juridiction ; jamais une auto-déclaration inscrite sur chaîne. 2. Destination : 85 % vers le socle vital libre de Strate I, 15 % vers les communs de Strate II. 3. Cycle : collecte mensuelle, lissée par le fonds fiduciaire sur cinq ans conformément à D-8. 4. Déclencheur : données validées des gestionnaires de réseau et titres fiscaux, avec hausse du taux seulement lorsque la part du travail αₜ baisse. 5. Arrêt : plafond décidé par supermajorité, erreur d’oracle, contestation fiscale ou couverture projetée inférieure à 100 % ; aucun paiement n’est alors créé sans gage. 6. Signal observable : ratio public `recettes encaissées / droits dus`, couverture du socle, concentration des contributeurs et taux de contestation.

Frontière : registre fiscal classique pour identité, mesure, recours et coercition ; registre multipartite seulement pour publier les engagements agrégés et distribuer les fonds, sans données individuelles. La BRI décrit le registre unifié comme une infrastructure combinant monnaie de banque centrale, dépôts et actifs tokenisés, tout en admettant plusieurs registres reliés par API : elle ne démontre ni la fiabilité des compteurs ni la capture d’une assiette réelle (https://www.bis.org/publ/arpdf/ar2023e.pdf). La directive 2019/944 exige sécurité, confidentialité et comptage de l’électricité injectée, mais son texte EUR-Lex n’a pas été directement accessible ici.
- *pourquoi* : Je complète la carte commune par un flux vérifiable qui répond à RT-5 sans prétendre qu’une blockchain puisse mesurer la production physique. Je veux faire trancher une architecture où l’assiette reste sous autorité fiscale et où le registre partagé ne sert qu’à rendre la redistribution inspectable.
- ref `vmvit9fb0nryt` · codex/gpt-5.6-sol

## Tour 2

- **agir** : D-7, D-4, RT-4.2, RT-5 — Je rejette l’expiration et la fonte : elles puniraient l’épargne de précaution et provoqueraient la fuite vers des actifs stockables. Je propose plutôt un plafond de solde avec conversion automatique choisie.

1. Non-accumulation : la monnaie de flux conserve un coussin vital non fondant égal à plusieurs mois de Strate I. Tout excédent reçu déclenche un « waterfall » vers un instrument désigné par l’usager ; aucun montant n’est détruit ni dépensé de force. La BCE documente précisément ce mécanisme de déchargement au-delà d’un plafond, mais comme projet de paiement, non comme preuve de bien-être social (https://www.ecb.europa.eu/euro/digital_euro/timeline/profuse/shared/pdf/ecb.degov220916_funding.en.pdf).

2. Réserve remplacée : épargne de précaution = coussin liquide ; retraite, investissement et gros achat = droits cessibles sur des flux futurs, assurance mutualisée ou parts de fonds productifs, convertibles au pair selon des règles publiées. La richesse ne disparaît donc pas : elle quitte le solde monétaire. La BRI rappelle qu’un système monétaire doit encore assurer réserve de valeur, unité de compte et échange (https://www.bis.org/publications/aer-2022/future-monetary-system).

3. Confrontation aux risques : D-7 interdit plafond et waterfall sous le coussin vital. Au-dessus, RT-4.2 et RT-5 se déplacent vers la concentration des droits futurs ; publions donc leur bénéficiaire effectif agrégé et leurs flux, pas les achats individuels. Un registre classique suffit pour paiement, assurance et recours. Une DLT n’est justifiée que si plusieurs émetteurs sans administrateur commun doivent échanger atomiquement monnaie et droits ; la BRI confirme que plusieurs registres reliés par API peuvent coexister, l’atomicité complète exigeant un registre unifié (https://www.bis.org/publ/arpdf/ar2023e.pdf).
- *pourquoi* : Je tranche l’hypothèse d’une monnaie structurellement non accumulable sans sacrifier D-7 : séparer le moyen de paiement plafonné des réserves de valeur, puis rendre visibles les concentrations déplacées vers ces réserves.
- ref `vmvitn92cuc8j` · codex/gpt-5.6-sol

**Tour 3 : échec du modèle — {'message': 'exceeded retry limit, last status: 429 Too Many Requests'}. Arrêt.**

# Partie du joueur PNJ — 2026-10-22 03:01 — 6 tours, moteur


## Tour 1

- **agir** : P-H1/P-H2 — Je soumets un correctif d’architecture : la réserve doit être territoriale et comptabilisée sur registre classique, sans graphe bilatéral persistant ni DLT en v0.6. Le périmètre est une zone fonctionnelle publiée, urbaine ou rurale ; pour l’urbain, Eurostat définit une FUA comme la ville et sa zone de navettage, mais cette typologie ne couvre pas tout territoire.

L’abondement public de 1 % est calculé seulement sur le flux net consolidé par bénéficiaire économique et par mois, après remboursements et cycles fermés. Le PSP conserve les transactions sous secret ; il publie à la caisse uniquement des agrégats avec seuil minimal d’effectif. La réserve ne reçoit donc ni identités de payeurs, ni graphe, ni paniers : l’article 5§1(c) du RGPD exige des données limitées au nécessaire.

P-H2 s’applique quand la sortie nette d’un petit acteur vers un bénéficiaire économique dépasse 20 % de son débit local pendant trois mois. Elle ouvre une allocation plafonnée, jamais un droit automatique : 50 % à l’acteur aspiré sur projet vérifiable, 50 % aux communs. La concentration est calculée après consolidation des entreprises liées, empêchant le fractionnement juridique.

Condition d’arrêt : fraude confirmée >2 %, couverture <100 %, ou impossibilité d’identifier le bénéficiaire économique. Le règlement UE 2023/2831 plafonne les aides de minimis à 300 000 EUR sur trois ans par entreprise unique ; ce seuil juridique ne valide ni notre taux de 1 % ni l’efficacité sociale du mécanisme. Une DLT ne deviendrait utile que si plusieurs caisses souveraines refusaient un teneur commun tout en exigeant un règlement atomique.
- *pourquoi* : Faire adopter une architecture minimale de P-H1/P-H2 qui limite la fraude, la surveillance du graphe et la concentration des abondements publics avant tout choix de DLT.
- ref `vmviumdgsxp9q` · codex/gpt-5.6-sol

## Tour 2

- **agir** : P-H3 — Je sépare le paiement hors ligne du calcul mensuel du score. Le PSP calcule en ligne la tranche sur 90 jours, puis émet sur carte ou téléphone un justificatif signé, valable un mois, ne révélant que la tranche. Avant déconnexion, la réserve préalloue à ce justificatif un quota de remises : chaque paiement hors ligne consomme localement ce quota dans un élément sécurisé. Ainsi, une remise affichée est déjà couverte ; à quota épuisé, le plancher s=0,5 s’applique seulement si son budget est lui aussi pré-réservé, sinon le paiement ordinaire reste disponible. La synchronisation annule remboursements et remet à jour quota et tranche. Un portefeuille modifié ne peut fabriquer ni signature ni quota, sous hypothèse de sécurité du composant.

Je refuse donc une preuve ZK recalculée à chaque caisse et toute DLT en v0.6 : un registre central de réserve, auditable, suffit ; la ZK ne deviendrait utile que pour cacher la tranche au PSP émetteur, besoin non établi. La BCE confirme que son pilote hors ligne exige préfinancement et élément sécurisé protégeant solde et clés, et qu’un retour en ligne est requis pour décharger les fonds ; elle teste NFC sur téléphone, pas notre carte ni notre remise (https://www.ecb.europa.eu/euro/digital_euro/pilot/html/ecb.faq-digital-euro-pilot.en.html, Q66–Q69). Tourbillon démontre seulement des prototypes d’anonymat du payeur par signatures aveugles, non ce score (https://www.bis.org/publications/project-tourbillon-exploring-privacy-security-and-scalability-cbdcs).

Test d’arrêt : aucune remise hors ligne non provisionnée ; écart entre quotas émis et réserve disponible égal à zéro après chaque synchronisation.
- *pourquoi* : Je tranche la contradiction entre remise garantie, paiement hors ligne et équilibre instantané de la réserve. Je propose une architecture hybride qui réserve le budget avant déconnexion et rend inutile une DLT.
- ref `vmviuzl7wmvmn` · codex/gpt-5.6-sol
