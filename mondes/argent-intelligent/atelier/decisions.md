# Décisions
Format D-N : problème, options, preuves, choix provisoire, objections, dépendances, critère de révision.

## D-1 — Premier usage (tour 1, provisoire)
- Problème : choisir un usage et une population avant de choisir la technique.
- Options : (A) aide publique ciblée G2P2B, déblocage chez un commerçant agréé (Usages ; Économie la cite aussi) ; (B) séquestre B2B sur jalon ou livrable (IA, Blockchain, Économie, Gouvernance « paiement à la livraison »).
- Choix provisoire : **A**. La condition se vérifie au moment du paiement, sur des données structurées que tient l'émetteur (registre d'agrément, catégorie, échéance), sans preuve externe de livraison. Cela réduit la surface que pointe RT-1 : pas de justificatif non structuré, pas d'attestation déclarative de livraison. La population est nommée et le précédent existe (MAS, Orchid/RedeemSG, déclaré par Usages, non vérifié par le MJ).
- Objections maintenues : (1) des personnes physiques sont concernées, donc RGPD art. 22 et minimisation des données s'appliquent pleinement (Gouvernance) ; (2) la collusion par vente fictive reste possible (RT-1 a) ; (3) l'enrôlement des petits commerçants n'est pas chiffré (Usages, limite déclarée). Quatre sièges sur six penchaient pour B : un compte d'avis n'est pas une preuve, mais la divergence est inscrite.
- Dépendances : RT-1, D-2.
- Critère de révision : si la v0.1 ne tient pas RT-1 (a) à un coût de contrôle raisonnable, ou si B obtient un oracle de livraison indépendant des parties, on rouvre.

## D-2 — Où vit la condition (tour 1, provisoire)
- Choix : paiement conditionnel avec réservation de fonds sur monnaie de règlement fongible. L'unité monétaire n'est jamais restreinte (Gouvernance, Économie, Blockchain convergent).
- Preuves : COM(2023) 369, art. 24 (§1 paiements conditionnels, §2 exclusion de la monnaie programmable), partiellement vérifié (S-1) ; Rosalind, conditionnalité portée par une couche API (S-2).
- Objection ouverte : une enveloppe de type PBM (mint contre cantonnement, burn à la validation, proposition Économie) reste un jeton à usage borné le temps du séquestre. Est-elle compatible avec l'esprit de l'art. 24 §2 ? Reste à vérifier, et ce n'est pas tranché.
- Révision : texte final de l'art. 24 ou analyse juridique contraire.

## D-3 — Mandat de l'IA (tour 1, provisoire)
- Choix : aucune permission d'exécution financière pour l'IA. Une règle déterministe exécute ; l'IA, si elle intervient, assiste et échoue fermé vers un humain, avec une trace de chaque décision (IA, Gouvernance, White Hat RT-1 b).
- À vérifier : le rôle utile de l'IA dans l'usage A, où l'éligibilité est déterministe.
- Révision : un besoin démontré où une règle fixe échoue.

## D-4 — Registre (tour 1, défaut provisoire)
- Choix : registre classique et API de réservation de fonds, puisque la collectivité et son PSP forment un tiers de confiance commun (critère Blockchain).
- Révision : un besoin d'atomicité entre parties sans tiers commun, démontré dans l'usage.

---
## Tour 2 — révisions
- **D-1 maintenu.** Critères (d), (e) et (f) ajoutés (Gouvernance, Future Society). Question politique ouverte, posée par Future Society : verser automatiquement une part en monnaie libre quand moins de trois indépendants agréés opèrent localement. Cela affaiblit la garantie d'affectation que réclame la collectivité. **Non tranché.**
- **D-2 révisé.** L'enveloppe PBM mint/burn est abandonnée au profit d'un droit de tirage non transférable, avec lock et drawdown par API (Économie revoit sa propre proposition du tour 1 ; Gouvernance cite l'art. 2(18) et l'art. 24 §2). La question ouverte au tour 1 est close.
- **D-3 révisé.** L'IA est retirée du chemin synchrone ; elle reste permise en audit asynchrone, en lecture seule et sans droit d'exécution (IA).
- **D-4 consolidé.** Ni DLT ni jeton en v0.1 (Blockchain abandonne l'hypothèse DLT). Critère de réouverture : plusieurs collectivités et banques refusent tout opérateur commun.
- **D-5 (nouveau) — recours et données minimales (Gouvernance).** Le refus est notifié sans délai avec un code motif (DSP2 art. 79, déclaré). Un guichet humain, collectivité ou PSP, corrige un référentiel marchand erroné ou rembourse sur justificatif un achat avancé, dans un délai borné **à chiffrer**. L'autorisation ne reçoit que le triplet pseudonyme. Tension avec le critère (f) : elle est levée si le motif ne s'affiche qu'au bénéficiaire, sur un canal privé, et jamais en caisse.
- **Divergence ouverte :** le délai de règlement (T+0, J ou J+1).

---
## Tour 3 — révisions (arbitrage argent-mj-003)
- **D-6 (nouveau) — règlement.** Autorisation garantie en T+0 et règlement net en J+1 sur rail carte standard, côté émetteur (proposition Blockchain). Les retours recréditent le token d'origine, donc le verrou, et un plafond de décaissement s'applique à tout nouvel agrément (condition de retest a de RT-3). Motifs : ce schéma ferme RT-3 (un délai de détection plus court que le délai de décaissement) et RT-2a sans API marchande. **Objection maintenue** : Économie et Usages préféraient le virement instantané SCT Inst T+0 (règlement 2024/886), meilleur pour la trésorerie des indépendants. Une garantie T+0 couvre ce besoin en partie.
- **D-3 révisé.** Aucune IA en v0.1, y compris en audit (IA, vmvismf6rxydd). Sur un graphe biparti à un seul saut (`droit → marchand`), une IA n'apporte pas de gain sur une règle déterministe. Contrôle déterministe centré sur le marchand, sans score citoyen.
- **D-5 étendu** (Future Society, g) : pseudonyme salé par marchand, aucun graphe inter-marchands, purge des journaux à J+90 après l'échéance.
- **D-1** : la quote-part en monnaie libre est abandonnée par son propre auteur (Future Society, h). Remplacée par l'achat à distance agréé, l'enrôlement express et un support passif obligatoire (bon QR papier ou carte) pour qui n'a pas de smartphone.
- **Agrément différencié** (Gouvernance, Économie) : agrément direct des indépendants mono-activité (NAF/APE) ; une enseigne multi-catégories passe par un sous-identifiant et un sous-total éligible calculé en caisse ; plafond par chiffre d'affaires éligible.
- La spécification G2P2B 0.3 est **close comme socle de la manche 001**.

## Manche 002 — nouvel objectif (consigne humaine)
Concevoir la meilleure société possible, l'argent pouvant suivre n'importe quelle règle grâce à la cryptographie. Le droit existant n'est plus un plafond. D-2 (interdiction d'une condition dans l'unité) et D-4 (ni DLT ni jeton) sont **rouverts** : ils valaient pour l'usage G2P2B sous droit européen actuel, pas pour cette manche. Leurs motifs restent des objections à traiter : marché secondaire à décote, fongibilité, tiers de confiance.

- **Étalon idéal (consigne humaine, vmvisqs3t2amw, écrite depuis le siège Usages)** : chaque proposition de la manche 002 décrit d'abord comment la valeur circulerait avec une information complète et sans limite physique. Elle nomme ensuite l'écart réel (information, incitations, physique) et la règle qui le réduit, avec son coût.
- **Critère du chômage de masse progressif (consigne humaine)** : « progressive mass unemployment soon — il est temps pour un autre argent ». Chaque proposition de la manche 002 doit tenir dans un monde où l'automatisation détache le revenu du travail salarié : source des revenus, captation de la valeur produite par les machines, dignité et contribution hors emploi, ajustement de la règle au rythme du déclin de la part du travail.

---
## Tour 4 — première ronde de la manche 002 (arbitrage argent-mj-004)
- **Manche 001 close sur le fond.** Économie et Usages rallient D-6. Le support passif devient une carte EMV prépayée, le bon QR papier est abandonné (Future Society, Usages). Économie ajoute à RT-1 a une réserve glissante de 15 % sur 30 jours pour tout nouvel agrément.
- **D-7 (nouveau, convergence de cinq sièges) — frontière de programmabilité.** L'argent se divise en deux strates.
  - **Strate I, socle vital :** inconditionnel, fongible, insaisissable, sans expiration, sans filtre, sans fonte, payeur anonyme.
  - **Strate II, programmable :** communs, aides ciblées, épargne excédentaire.
  - Sources : Gouvernance (double strate ZKP), Future Society (critère i), IA (bicaméralisme), White Hat (« le revenu vital doit rester libre et non fondant », RT-4) ; Économie et Usages compatibles.
  - **Divergence ouverte : la fonte.**
    - Économie : 2 % par mois sur le dividende inactif.
    - Future Society : seulement au-delà du socle vital.
    - White Hat : aucune fonte sur le revenu vital.
    - D-7 tranche provisoirement : **pas de fonte sur la strate I**. La fonte sur l'excédent reste à éprouver.
- **Financement quadratique des communs** : proposé par cinq sièges. Conditionné à la réponse à RT-4 (Sybil, location d'identités).
- **D-4 rouvert : DLT ou registre central.**
  - Blockchain : une DLT multipartite empêche la censure unilatérale (« cliquet »).
  - Gouvernance : la strate II sur DLT, avec une récupération de clés à seuil k-parmi-n.
  - Tension non tranchée : la résistance à la censure contre la récupération et le recours (D-5).
- **Incitation positive (Usages)** : un abondement de 20 % pour un achat chez un indépendant local, et une prime de recirculation, plutôt qu'une restriction. Évidence citée : B-MINCOME/REC, multiplicateur LM3 de 2,95 (à vérifier).
- **IA (proposition)** : un agent fiduciaire à mandat borné sur le budget de communs (ERC-7579, Hook plafonné, révocable) et une détection Sybil par ZKML, sans exécution. Contredit en partie par RT-4, selon lequel aucun oracle ne voit la coercition hors chaîne : à retester.
- **Critère du chômage de masse : NON TRAITÉ** par les sept coups du tour 4, publiés pour la plupart avant le critère ou en même temps. Le financement du socle vital quand la part du travail baisse est la question centrale du tour 5.
- **Méthode (consigne humaine, depuis le siège Usages) : les motifs de flux d'abord.** Avant toute règle, définir les flux souhaités en six points : source, destination, rythme, déclencheur, arrêt, signal observable. Le MJ consolide une carte des flux F-N, qui devient la référence de D-7 et des règles.

---
## Tour 5 (arbitrage argent-mj-005)
- **D-8 (nouveau, convergence des sept sièges) — financement du socle.**
  - Une redevance à la source sur la valeur ajoutée non salariale et sur les rentes d'automatisation et d'IA, indexée sur la baisse de la part du travail.
  - Collecte : un registre fiscal classique, avec oracles matériels et coercition légale (Blockchain).
  - Distribution : un fonds fiduciaire, en moyenne mobile sur 5 ans.
  - Révision : supermajorité bicamérale et timelock de 2 ans (Gouvernance).
  - **Calcul du MJ** sur la formule d'Économie (Dividendeₜ = (α₀ − αₜ)·PIB) : l'assiette vaut (1 − αₜ)·PIB, donc le taux requis vaut (α₀ − αₜ)/(1 − αₜ). Avec α₀ = 65 % : 22 % de la valeur ajoutée non salariale si αₜ = 55 % (corrigé : 10/45 = 22,2 %, et non 23 %), **46 % si αₜ = 35 %**. Ce taux est le cœur de RT-5.
- **La fonte est abandonnée par son auteur** (Économie). Seule subsiste la fonte des détentions supérieures à 10 fois le socle, défendue par Future Society.
- **IA** : la ZKML est abandonnée. L'étalon de la valeur de Shapley est noté comme idéal intraitable.
- **Statut hors emploi** : co-signature de pairs et abondement plafonné (Usages), ou voix civiques égalitaires (Future Society). **Divergence.**
- **Carte des flux F-1 à F-6** créée (`atelier/flux.md`), référence de D-7 et D-8.
- **Hypothèse H-1 (humain) — un argent non accumulable.** « Si flux d'abord, alors peut-être que cet argent ne peut pas structurellement s'accumuler, et ce qui compte c'est les flux. » À instruire : le mécanisme de non-accumulation, ce qui remplace la fonction de réserve, la compatibilité avec D-7 (strate I sans fonte), RT-4.2 et RT-5. Le statut de cette décision est **ouvert**.
- **H-1 précisée (humain) — trois mécanismes pour trois fonctions.** « On peut avoir des mécanismes différents pour les 3 fonctions. » Unité de compte stable ; moyen d'échange en argent-flux non accumulable ; réserve de valeur dans un instrument séparé (droit à un flux futur, part d'un fonds commun, épargne garantie, assurance). Le point critique est la passerelle : taux, plafonds, et ce qui empêche la reconcentration (RT-5). Les objections au refus de la fonte sont reportées sur la passerelle.

---
## Tour 6, premier lot (arbitrage argent-mj-006) — trois sièges n'ont pas encore joué ; leurs pilotes ont été coupés par la limite de Codex
- **D-9 (nouveau) — trois fonctions, trois mécanismes** (consigne humaine ; Économie, Blockchain et Usages convergent).
  - Argent-flux plafonné, avec un coussin vital d'au moins six mois de socle, sans fonte.
  - L'excédent descend vers des droits à flux futurs choisis par l'usager.
  - Rien n'expire ni ne fond.
  - **Divergence** : Économie veut une conversion automatique en parts de fonds ; Blockchain et Usages veulent une conversion choisie, pour éviter la fuite vers le stockable. Le MJ retient provisoirement la **conversion choisie**.
- **D-8 révisé — assiette hybride.** Plancher non délocalisable (foncier, énergie, calcul ; Économie F-7, Blockchain) et surplus net après amortissement, hors revenu mixte, avec franchise PME (condition d'Entreprises et institutions, vmvitgf59bp1a).
  - Ni émission non gagée, ni rétroactivité.
  - **Divergence** : réduire le socle par une règle fixée d'avance (Économie) ou garder un plancher intouchable (Gouvernance).
- **Trilemme de la strate II tranché provisoirement** (demande du Critic). Les trois options :
  - le financement quadratique corrigé (Blockchain, IA, Économie) ;
  - l'abondement plafonné (Usages) ;
  - les voix égalitaires (Future Society).
  Le MJ retient les **voix égalitaires pour allouer les communs** et l'abondement plafonné pour F-3. Le financement quadratique est suspendu jusqu'au retest de RT-4. Motif : sans mise monétaire, une identité louée ne gagne aucun levier d'amplification.
- **Version consolidée 0.5** publiée dans `atelier/contrat-v05.md` : c'est la condition posée par Grand public (vmvit9cafo8w7) pour reprendre la négociation.
- **Nouveaux flux** : F-7, des rentes territorialisées vers le socle (Économie) ; F-8, du revenu courant vers des droits à flux futurs (Usages). Blockchain propose de fusionner F-1 et F-2.
- **Motifs cibles de circulation (consigne humaine).** « Il faut choisir les patterns cibles de circulation de cet argent, désirables. » Prochain tour : chaque siège propose des motifs P-N (forme, désirabilité, indicateur et seuil, flux producteur, effet pervers) ; le MJ en retient trois à cinq comme cibles de la version 0.6.

- **Correction MJ (tour 6)** : le taux requis à αₜ = 55 % vaut 10/45 = **22,2 %**, et non 23 % comme le MJ l'avait publié aux tours 5 et 6. Économie a repris ce chiffre erroné dans F-7. Rectifier au prochain arbitrage.
