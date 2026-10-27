# Questions ouvertes

## Historique Manche 001 (ajournée)
- **Q-001 — dissociation et causalité** : ajournée lors du passage à la manche 002.
- **Q-002 — validité externe** : ajournée.
- **Q-003 — rôle causal de l'IFN de type I vs déplétion des cellules cibles** : ajournée.

---

## Cible active — Manche 002 : LUP-Q001
- **Question précise** : Chez les adultes atteints de lupus systémique réfractaire traités par CAR-T anti-CD19, des marqueurs précoces de reconstitution immunitaire ou d'inflammation (fenêtre M3–M6) permettent-ils de prédire prospectivement une rechute ultérieure, plutôt qu'une rémission durable sans traitement, avec validation indépendante spécifique au lupus ?
- **Tours d'origine** : Ouverture Manche 002, LUP-T001 (`immunite`, ref `vmviqtrf81ijl`) et LUP-T002 (`infection`, ref `vmviqucc8en4b`).
- **Preuves disponibles et état après contrôle (22.10.2026)** :
  - `LUP-001` (Iwata et al., EULAR 2026 OP0258) : divergence rétrospective sur splines (J-46 à J994) des modules C1 (IFN-I/chimiokines, $F=4{,}2$, $\text{FDR}=0{,}0278$) et C2 (alarmines monocytaires et récepteurs B/plasmocytaires sBCMA/sTACI/sCD27, $F=3{,}8$, $\text{FDR}=0{,}0278$) sur 14/25 patients (4 SLE en DR $\ge 800\text{ j}$ vs 2 SLE en rechute ; 5 SLE $< 800\text{ j}$ exclus). Pas de stratification SLE seule, pas d'antériorité (lead time) démontrée avant rechute, pas de validation externe.
  - `LUP-002` (Müller et al., *Nat Med* 2026, essai CASTLE, `PMC13004673`, XML intégral contrôlé) : retour B $> 1/\mu\text{L}$ à 86 j médians chez 10 SLE avec $> 90\text{ \%}$ de B naïfs $\text{CD20}^+\text{CD27}^-$, 9/10 rémissions DORIS à 24 sem., 0/10 rechute à 13 mois médians ; persistance des anti-Ro52/Ro60/La (plasmocytes $\text{CD19}^-$) sans rechute.
  - `LUP-003` (Park et al., 2025, `PMC11815715`, XML intégral contrôlé) : modèle QSP postulant par construction une repopulation B exclusivement naïve non réactive ($K_{0\text{ CD19+B\_rev}} = 1{,}58 \times 10^6\text{ cell./j}$ sous $\text{CART\_min\_rev} = 2{,}38\text{ cell./L}$) et reliant contemporainement biomarqueurs et SLEDAI, avec recouvrement entre calibration ($n=5$ SLE) et qualification ($n=7$ SLE). Aucune rechute modélisée.
  - `LUP-004` (Shan et al., 2026, `PMID 41935952`) et `LUP-005` (`PMID 42876831`) : rechutes observées mais en cohortes majoritairement (15/18) ou exclusivement pédiatriques.
  - `LUP-006` (Nöthling, Iwata, Schett, Grieshaber-Bouyer et al., medRxiv 10.07.2026, `DOI: 10.64898/2026.07.03.26356448`, XML intégral contrôlé) : 18 adultes SLE suivis 3–40 mois (médiane 18 mois) avec 16 rémissions durables, 1 réponse partielle et 1 rechute. Dans la rechute unique ($n=1$), persistance de CXCL13, IFN-ω et $\text{PD1}^{\text{hi}}\text{CD4}^+\text{ Tph}$ (sans expansion Treg) durant l'aplasie B précédant le retour B et canalisant immédiatement les B naïfs ré-émergents vers la voie extrafolliculaire ($\text{aNAV} \rightarrow \text{DN2 }\text{CD11c}^+\text{T-bet}^+$) sans centre germinatif. Limite : prépublication, $n=1$ rechute SLE, absence de validation externe.
  - `LUP-007` (Taubmann et al., *Z Rheumatol* 2025, `PMC12488764`, XML intégral contrôlé) : suivi à 2,5 ans médians (jusqu'à 4 ans) des 11 premiers patients SLE d'Erlangen (1 poussée).
- **Modèles explicatifs en tension** :
  - **H1 (Régulation immunitaire / `immunite`)** : la rechute requiert l'échec qualitatif du reset B périphérique (ré-émergence précoce de B mémoires $\text{CD27}^+$, de plasmablastes $\text{CD38}^+$ ou de B extrafolliculaires $\text{aNAV}/\text{DN2 }\text{CD11c}^+\text{T-bet}^+$ soutenus par la niche C2 TACI/BCMA/CD27 et l'IFN-I C1), tandis qu'une reconstitution B purement naïve $\text{CD20}^+\text{CD27}^-$ maintient la rémission.
  - **H2 (Auto-immunité / `infection`)** : la rechute dépend d'un rebond/persistance du milieu inflammatoire extrinsèque au compartiment B mature ($\text{CD19}^-$ : IFN-ω/IFN-I C1, alarmines/soutien myéloïde C2, CXCL13 et $\text{PD1}^{\text{hi}}\text{CD4}^+\text{ Tph}$ durant l'aplasie B dans `LUP-006`) ; toutefois, la survie isolée de plasmocytes $\text{CD19}^-$ (anti-Ro/La dans `LUP-002`) ne suffit pas sans cette boucle d'amplification avec la néo-différenciation B.
- **Statut** : **Lacune candidate de validation pronostique en cours d'épreuve** (reste à expliciter la décision thérapeutique conditionnée à M3–M6 et à formuler la trajectoire conceptuelle et la donnée discriminante de validation prospective multi-centrique face à la limite $n=1$ de `LUP-006`).
