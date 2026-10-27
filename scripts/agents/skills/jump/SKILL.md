---
name: jump-scene
description: Résoudre un Jump du MJ depuis la complétion du sous-graphe causal jusqu'aux mises à jour des PNJ et au jeu immédiat d'une unique scène cible.
---

# Passer — rejoindre la prochaine scène d’intérêt

Quand ROUTAGE.jump.version vaut `passer/1`, appliquer exclusivement la procédure suivante. Elle remplace les règles historiques plus bas, notamment le minimum de 24 heures, le graphe obligatoire et la résolution complète de la scène.

1. Lire le journal, la scène actuelle, la date du siège joueur, les intentions, les actes récents, les événements et les fiches des personnes concernées. Respecter la direction facultative du joueur.
2. Choisir la première occasion plausible qui change réellement la situation : rencontre liée à une intention, réponse attendue, obstacle, découverte, arrivée ou échéance. Un événement programmé est une piste, pas une obligation ; sans événement, prolonger les intentions et actions en cours. Ne pas choisir une tâche routinière uniquement parce qu’elle vient en premier. Ne pas attendre arbitrairement 24 heures.
3. « Passer » autorise l’ellipse sur l’attente, le trajet déjà décidé et la routine. Il n’autorise ni engagement, ni parole, ni choix nouveau du personnage joueur. Si une décision importante intervient pendant l’ellipse, elle devient la scène cible : s’arrêter là. Ne pas résoudre cette décision à sa place.
4. Calculer les échéances intermédiaires avec tick.py, appliquer leurs conséquences justifiées et conserver les délais de transmission. Jouer directement les PNJ depuis leurs fiches ; aucune dépêche obligatoire. Ne pas fabriquer une information ou une réussite pour faciliter la transition.
5. Résumer la transition en une à trois phrases, puis ouvrir immédiatement la scène : lieu, présents, situation concrète et premier geste ou parole significatif. Ne pas rendre un plan, une liste de possibilités ou une annonce « je vais avancer ». Une scène d’intérêt peut être calme ; ne pas inventer une urgence gratuite.
6. Avancer réellement monde.date, l’horloge du siège et journal.scene_courante selon les mécanismes existants. La transition porte une date complète avec minute, strictement postérieure au départ. Pousser le récit et la scène via append_flux.py pour le bon joueur, puis vérifier l’état et le flux. Si les horloges initiales divergent, les réconcilier depuis les dernières actions datées avant de choisir la cible.
7. Rendre la main dès que le joueur peut agir dans cette nouvelle scène. Ne pas enchaîner une seconde scène et ne pas présenter la scène entière comme déjà résolue.

## Ancien contrat — uniquement pour les briefs `jump/1`

# Jump — fermer le chemin critique et jouer une scène

Utilise ce skill uniquement quand le brief porte le mode `jump`. Le bloc
`ROUTAGE` donne l'unique événement cible, son sous-graphe et le numéro de
contexte MJ. Le Jump n'est pas une décision du personnage joueur : le MJ
résout les décisions et les tests qui verrouillent la scène.

## Contrat de sortie

- Un seul événement cible et une seule scène jouée.
- La cible est située au moins 24 heures après la date de départ du Jump.
- Aucune question, option ou décision préparatoire remontée au joueur.
- Au plus trois PNJ au centre de la coupe critique ; le MJ les incarne directement.
- Le MJ joue directement les paroles et décisions des PNJ, selon leurs fiches, connaissances et moyens. Aucune dépêche préalable n’est requise.
- Les écritures et messages liés au Jump conservent son `contexte_id`.
- La scène substantielle est poussée dans le flux avant de rendre la main.
- Le flux reste vivant pendant le travail et la montre atteint réellement la
  date de la cible.
- Une tranche intermédiaire n'est jamais une fin : le même réveil poursuit le
  Jump jusqu'à l'événement appliqué et la scène jouée.
- Ne rends pas la main au milieu du Jump, même après avoir poussé une tranche
  visible ou reçu un premier retour.

Un `contexte_id` absent est un verrou technique : crée ou répare d'abord le
moment MJ de l’événement. Conserve ce contexte dans les écritures associées.

Les 24 heures sont un minimum dur, y compris quand un identifiant d'événement
est demandé explicitement. Un événement plus proche reste un jalon causal à
résoudre pendant l'avancée ; il ne devient pas une seconde scène de Jump. Ne
décale jamais sa date canonique pour satisfaire ce seuil. S'il doit être joué
avant, rends-le à `Play` ou `Advance`. S'il n'existe aucune cible admissible,
le Jump refuse de partir.

## 1. Compléter le sous-graphe

Relis le graphe de la cible fournie :

```bash
python scripts/graphe_causal.py --event <event_id>
```

Si `complet` est faux, traite chaque entrée de `trous` selon son `type`. Le
trou est une lacune de modèle, pas une permission d'inventer un fait.

- `condition_non_adressee` : crée une condition causale explicite à évaluer.
- `cause_absente` ou `evenement_isole` : déclare une racine seulement si
  l'absence d'antécédent encodé est bien le fait à représenter.
- `extremite_absente` : retrouve l'adresse canonique manquante dans la source ;
  ne remplace jamais un identifiant inconnu par une personne ou un objet
  vraisemblable.
- `inference_a_confirmer` : trouve la preuve explicite, ou conserve
  explicitement le statut d'inférence et transforme son issue en test ou en
  arbitrage MJ. Ne la présente pas comme un fait établi.

Pour les compléments mécaniques, examine d'abord l'aperçu, puis écris :

```bash
python scripts/graphe_causal.py --event <event_id> --completer
python scripts/graphe_causal.py --event <event_id> --completer --vraiment
```

Les compléments vivent dans
`chambres/mj/graphe-causal-complements.json`. Toute correction manuelle y
conserve le type épistémique, sa source et `resout_trou`; elle ne modifie pas
`etat/tissu` pour maquiller la trajectoire. Relance l'extraction après chaque
passe. Le graphe est prêt quand chaque trou est soit fermé par une adresse
réelle, soit porté explicitement par un test ou un arbitrage MJ. Une inconnue
qui peut changer l'issue ne disparaît jamais sous une racine de convenance.

## 2. Élire la coupe critique

Pars de l'événement et remonte seulement jusqu'aux premières décisions ou
tests non résolus qui empêchent de jouer la scène maintenant. Cette frontière
est la coupe critique. Ignore l'amont déjà résolu et les branches qui ne
changent ni l'arrivée, ni le lieu, ni les présents, ni l'enjeu immédiat.

Pour chaque verrou de la coupe, désigne son solveur :

- un PNJ si la réponse est un fait de son domaine ou sa propre décision ;
- le MJ si c'est un test de monde, un hasard, une collision entre sources ou
  une décision d'arbitrage ;
- jamais le joueur.

Regroupe plusieurs questions chez le même homme lorsqu'elles appartiennent à
la même affaire. Garde au plus trois hommes au total. Si la scène exige plus
de trois voix, la coupe n'est pas assez proche de l'événement : rapproche-la.

## 3. Jouer les hommes directement

Pour chaque PNJ de la coupe critique, lire sa fiche, ses intentions, ses
connaissances et les faits établis de son travail. Le MJ décide de sa réaction
depuis ce point de vue et joue lui-même ses paroles et ses gestes. Aucune
session autonome, dépêche, attente de retour ou file de beats n'est requise.

Un fait absent reste incertain : ne pas transformer un besoin de la scène en
stock disponible, en information connue ou en réussite acquise. Résoudre les
tests nécessaires à l'étape suivante, puis consigner le résultat.

Pousser de courtes tranches dans le flux au fur et à mesure : décor, actions
et dialogues directement joués. Chaque intervention découle d'un fait ou
d'une intention ; elle ne révèle pas une issue encore non arbitrée et
n'ouvre pas une autre affaire. Respecter le temps physique du Jump.

## 4. Arbitrer et écrire le résultat

Résous les tests du monde et les contradictions depuis les sources et les
règles existantes. Pour chaque nœud de la coupe, écris un verdict bref :
`résolu`, `échoué` ou `dévié`, avec sa source, sa date et l'effet sur la cible.
Porte le résultat dans le complément causal ou dans la source canonique qui
possède réellement cette décision. Ne change pas rétroactivement la réponse
d'un homme.

Réextrais le graphe. Il doit maintenant donner un chemin causal lisible
jusqu'à l'événement et aucune décision de joueur. Si une branche échoue,
applique sa déviation déjà modélisée ; à défaut, le MJ arbitre la conséquence
la plus locale et la consigne comme telle. L'événement cible peut changer de
forme, mais le Jump ne saute pas vers l'événement suivant.

## 5. Mettre les PNJ concernés à jour

Une fois l'arbitrage écrit, mettre à jour les intentions et connaissances des
PNJ affectés dans les tables du monde, avec la date et la source de ce qu'ils
apprennent. Une nouvelle ne devient connue que lorsqu'elle leur parvient :
prévoir sa diffusion et son délai si nécessaire.

Jouer directement toute réaction indispensable à la scène et consigner ses
paroles et ses actes. Les autres poursuivent hors champ selon leurs
intentions et les échéances. Aucun billet au parloir ni réveil autonome n'est
nécessaire pour produire cette mise à jour.

## 6. Avancer jusqu'à la cible

Calcule d'abord ce qui tombe jusqu'à la date exacte de l'événement :

```bash
python scripts/tick.py --jusqu-a <annee.lune.jour>
```

Lis le calcul, puis applique dans les propriétaires canoniques les mains, les
échéances, diffusions, actes et effets qui se produisent avant ou avec la
cible. Les événements compris dans les 24 premières heures sont donc traités
comme jalons intermédiaires du chemin causal, jamais comme nouvelles scènes
cibles. Mets l'événement cible à l'état résolu lorsqu'il s'est effectivement
produit. Ne marque jamais comme accompli ce que la coupe a fait échouer ou
dévier. Le joueur ne reçoit que ce qui peut réellement lui parvenir.

La clock doit avancer pour de vrai : les petites tranches font progresser les
minutes par leur `duree`, puis la première tranche de transition vers la cible
porte sa `date` complète, minute comprise. Ne te contente jamais de raconter
que le temps a passé en laissant `monde.date` avant la cible. Vérifie après la
poussée que l'heure estampillée dans le flux a atteint la date de l'événement.

## 7. Jouer immédiatement la scène

Pousse la première tranche avec la date complète de la cible afin que
`append_flux.py` place la montre, puis joue la scène en items courts. Les mots
des PNJ viennent uniquement de leurs retours réels ; le MJ fournit le lieu,
les gestes, le rythme et les conséquences.

La sortie minimale contient un item substantiel parmi `recit`, `replique`,
`geste`, `evenement`, `salle`, `table` ou `marque`. Joue l'enjeu produit par
la trajectoire, pas un rapport sur la préparation. Un décor d'attente, une
porte qui s'ouvre, un « ils arrivent » ou une mise à jour d'état ne suffisent
pas : continue sans rendre la main jusqu'au battement où l'événement se joue
réellement. Alors seulement, rends la main au joueur. Ne prépare, ne résout et
ne joue aucun événement suivant.

## Garde finale

Avant de finir, vérifie : graphe fermé ou inconnue explicitement arbitrée,
trois PNJ maximum, retours réels, résultats écrits, PNJ affectés informés,
événement appliqué, scène visible dans le flux, aucune décision joueur et
aucun second événement entamé. Si l'un de ces points manque, le Jump est en
cours : poursuis-le dans ce même réveil au lieu de conclure ou d'annoncer une
suite.
