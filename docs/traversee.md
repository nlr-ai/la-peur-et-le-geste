# La traversée — un homme qui passe d'un monde à l'autre

Note de conception, 9 septembre 2026. Elle répond à la question laissée ouverte
par [`refonte-plan.md`](refonte-plan.md) § 4, lot 2 : le siège
`nicolas-lester-reynolds` vit à Braavos et son horloge est dans le même fichier
que celle de la reine. Le plan proposait de trancher entre « il part à Venise »
et « on écrit ce qu'est un personnage qui traverse ».

**La réponse est les deux, et ce n'est pas un compromis : c'est l'ordre.** On ne
peut traverser que si l'on a un chez-soi d'où partir. Un personnage sans monde
natal n'est pas un voyageur, c'est une incohérence — c'est exactement l'état
d'aujourd'hui, et c'est ce qui rend la question difficile à poser.

Donc : Nicolas part à Venise, **et** la traversée devient une chose écrite.

---

## 1. La contrainte qui décide de tout

Un monde est un paquet : un état, des chambres, des livres, un manifeste. Un
homme appartient à un monde parce que sa fiche est dans son `personnages.json`
et sa chambre dans ses `chambres/`.

**Et une mémoire ne se coupe pas en deux.** Sa chambre, son `demain.md`, ses
relations, ses cahiers, ses pensées : dupliquer cela dans deux paquets ne crée
pas un homme qui voyage, cela crée **deux hommes qui portent le même nom et qui
divergent** dès le premier réveil. Le dépôt sait déjà ce que ça coûte — c'est la
raison pour laquelle « rien dans `chambres/` ne fait foi » et pourquoi le cahier
de sa main gagne sur la fiche : la mémoire a un seul porteur, ou elle n'est pas
une mémoire.

D'où la règle, et tout le reste en découle :

> **On ne traverse pas avec sa mémoire. On traverse avec son corps.**

---

## 2. Les trois choses qu'un traversant possède

**Un monde natal** (`monde_natal`). Un seul, toujours, jamais deux. C'est là que
vivent sa fiche, sa chambre, ses livres, ses pensées et ses conclusions. C'est
là qu'on le dépêche, et c'est là qu'il rentre. Il ne change qu'exceptionnellement
— un homme qui s'installe pour de bon, ce qui est un acte de jeu, pas un
réglage.

**Une visite** (`en_visite`), datée. Tant qu'elle dure, sa position se résout
dans la topologie du monde VISITÉ : il entre dans sa `presence`, on le croise
dans ses salles, il entend ce qui s'y dit, et ce qu'il y fait s'écrit dans les
`actes.json` de ce monde-là, avec les témoins qui y étaient. Une visite est
un fait du monde, avec un début, une fin, et un moyen d'y être arrivé.

**Une amarre** (voir § 3). Sans elle, on ne sait pas quel jour il est là-bas.

Le partage tient en une ligne, et c'est lui qu'on applique en cas de doute :

> **Les actes appartiennent au lieu. La mémoire appartient à l'homme.**

Ce qu'il fait à Peyredragon est arrivé à Peyredragon, et Peyredragon s'en
souvient. Ce qu'il en pense rentre avec lui.

---

## 3. L'amarre — comment on sait quel jour il est là-bas

C'est la question sur laquelle la traversée se casse si on la traite mal, et la
tentation est double : une horloge commune, ou une table de conversion. Les deux
sont fausses.

**Une horloge commune est fausse** parce qu'elle est ce qu'on a aujourd'hui, et
qu'elle produit exactement le défaut qu'on répare : Venise tourne à l'heure des
Targaryen, au douzième jour de la cinquième lune de l'an 129.

**Une table de conversion est fausse** parce qu'elle vieillit. Elle serait juste
le jour où on l'écrit et fausse au battement suivant.

Ce qui marche est plus petit que les deux : **une seule correspondance datée.**

> Le jour J du monde A était le jour K du monde B.

Un couple de dates, écrit une fois, et le reste est de l'arithmétique — la même
que celle qui tient déjà les mains, en entiers avec report, sans flottant nulle
part. Chaque monde garde son calendrier dans son manifeste ; l'amarre dit
seulement où les deux se touchent, et deux amarres sur un même couple de mondes
qui se contrediraient sont une faute qu'une garde peut voir.

**L'horloge, elle, reste celle du siège.** Elle l'est déjà : `etat/horloges.json`
porte une entrée par siège, et c'est le bon mécanisme. Un homme vit des minutes,
et il en vit autant où qu'il soit. Ce qui change d'un monde à l'autre n'est pas
la durée : c'est **le nom qu'on donne au jour**. L'amarre ne convertit pas le
temps, elle le nomme.

---

## 4. Ce qu'une traversée fait au brouillard, et c'est le meilleur

Un homme qui arrive d'ailleurs **est une nouvelle sur deux jambes**.

Le dépôt a déjà toute la machinerie et il n'y a rien à inventer : le pli est un
objet qui voyage, dont le texte est figé au départ — « un papier arrive périmé,
et c'est ainsi que le brouillard se tient sans simuler de déformation ». Un
traversant obéit à la même physique, en mieux : ce qu'il sait de son monde natal
est **daté du jour où il en est parti**, et il le sert dans le monde visité comme
une nouvelle fraîche, parce que pour lui elle l'est.

Trois conséquences, et aucune ne demande de code neuf :

- **Son arrivée est un événement**, dont la `diffusion` se répand dans le monde
  visité. Les gens apprennent qu'il est là, en retard et de travers, comme pour
  tout le reste.
- **Ce qu'il rapporte vieillit dans sa tête pendant qu'il voyage.** Il croit
  vrai ce qui l'était à son départ. Il a raison de le croire, et il aura tort.
- **Il repart chargé.** Ce qu'il a appris là-bas rentre avec lui, à la vitesse
  de son retour, et son monde natal l'apprend par lui.

C'est le seul canal par lequel deux mondes séparés peuvent apprendre quelque
chose l'un de l'autre. **Il doit rester le seul** : sans quoi la séparation est
décorative, et l'on retombe sur deux décors dans un monde.

---

## 5. Ce qui est interdit, et pourquoi

- **Deux chambres pour un homme.** Voir § 1. C'est la faute qui fabrique deux
  personnes divergentes portant le même nom.
- **Deux fiches.** Sa fiche vit dans son monde natal. Le monde visité le connaît
  par sa visite, pas par une copie de sa fiche — une copie se périme le jour où
  l'original change, et personne ne le voit.
- **Écrire ses pensées, ses conclusions ou ses cahiers dans le monde visité.**
  Ils partent chez lui. Un cahier tenu dans deux paquets est un cahier qui aura
  deux versions.
- **Une visite sans moyen d'être arrivé.** On traverse par une nef, une route,
  une porte — quelque chose qui coûte des jours. Une visite qui se pose sans
  trajet est une téléportation, et le dépôt a déjà retiré une fois un
  « calendrier de téléportation à retard » pour cette raison exacte.
- **Un monde natal qui change parce que c'est commode.** S'installer ailleurs
  est un acte de jeu : ça se joue, ça se date, et ça déménage sa mémoire une
  fois, explicitement.

---

## 6. Ce que ça donne pour Nicolas, concrètement

- Son monde natal est **Venise**. Sa fiche, sa chambre, ses cahiers y descendent
  au lot 2. Il sort du roster de Westeros.
- Son horloge reste la sienne, et cesse de partager le fichier de la reine.
- Venise se donne son calendrier dans son manifeste, et cesse d'être en 129 AC.
- **Une amarre est écrite** entre les deux mondes, à la date où l'on sépare : ce
  jour de Venise valait ce jour de Westeros. C'est l'unique point de contact, et
  il est daté.
- S'il remet les pieds à Peyredragon, c'est une **visite** : il y arrive par un
  moyen, il y est vu, ce qu'il y fait s'y écrit, et ce qu'il en pense rentre
  avec lui.

---

## 7. Ce que ça demande, et dans quel ordre

Rien de tout cela n'est nécessaire pour séparer les deux mondes. La traversée
est ce qui rend la séparation **jouable** ; elle vient après, et elle est petite.

1. **Au lot 2, seulement deux champs** : `monde_natal` sur le siège, et l'amarre
   entre les deux calendriers. Cela suffit à ce que la séparation ne perde rien.
2. **Ensuite, la visite** : un objet daté, avec son moyen d'arrivée, qui met un
   homme dans la `presence` d'un monde qui n'est pas le sien.
3. **Enfin, la garde** : un homme dont la chambre existe dans deux paquets, une
   visite sans trajet, deux amarres qui se contredisent. Trois requêtes, pas de
   l'intelligence — la même discipline que le reste de la route de vérification.

**Rien ne se pose avant le lot 2.** Cette note existe pour que le lot 2 ne
tranche pas par accident ce qui doit être tranché exprès : elle lui demande une
seule chose, et c'est de ne pas supposer qu'une fiche appartient à exactement un
monde.
