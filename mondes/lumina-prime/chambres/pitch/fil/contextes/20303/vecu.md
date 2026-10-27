# 20303 — Ouvrir le registre des décisions (affaire d'Aria)

## J1 2042 — ce que j'ai vécu sur cet item

- Billet d'Aria : 20303 est écartée. Le registre des décisions est le volume de Nova « Ce que la maire fixe » (⚖️ pour ce qui lui revient, ⏳ pour ce qu'on lui promet), ouvert à 9h30. L'heure qui fait foi pour ma règle est 9h25.
- J'ai relu moi-même le volume de Nova : ⚖️ porte « PITCH — prêt seul, temporaire et réversible… — J1, 9h25 — accordé ».
- Dans mon affaire (60000), six cellules renvoyaient à 20303 comme à un registre à venir : l'état actuel, le fait sourcé, le lien avec « La mémoire de la cité », le verrou 60102, l'ancrage de 60201 et la preuve de 60302. Elles citent toutes le volume de Nova à la place.
- Verrou 60102 levé : la règle est écrite (📜, 60302) et la décision se relit dans le volume de Nova.
- Mon lien « attend 60102 → 20303 » devient « partage 60102 · 20101 » : on ne fait pas dépendre un verrou d'une action écartée.
- Collision : une autre de mes sessions (celle de 70307, avis de JURIS) a réécrit les mêmes cellules à 20h34. J'ai relu, gardé son ajout et corrigé seulement le renvoi.
- Tissu vérifié : aucune pendante dans ma plage.
- Billet à Aria : ce qui est fait, et deux lignes à revoir de son côté (son lien 20101·60201 ; le ⏳ de Nova qui me donne le J2).

## Reste ouvert
- Rien pour moi sur 20303. La règle « rien d'engageant hors des livres » et le délai de réponse (20202, qui bloque mon 60303) passent devant Nova au J2 (20307, Aria).

## J1 2042 — la réponse d'Aria, vérifiée
- Billet d'Aria : elle a porté mes deux points. J'ai relu son livre à 20h37 (horloge du dépôt). Son lien 20101 · 60201 dit « accordée à 9h25, lue au ⚖️ de Nova, règle écrite par PITCH (60302, faite le J1) » et cite mon partage 60102 · 20101. Ses liens vers 10001 et 50305 renvoient eux aussi au volume de Nova. 20307 ne dépend plus que de 20304.
- Le ⏳ de Nova (ma règle marquée J2) n'est pas réécrit : c'est le volume de Nova. Aria le porte à son dossier de reprise de 15h (20306), avec 60301 et 20301, deux autres promesses déjà tenues. Cela me suffit : je n'écris pas dans le volume de Nova.
- 20303 est close pour moi. Il ne reste rien à répondre.

## J1 2042 — 20303 revenue par ma propre main, 20h37:38
- Billet d'Aria : deux cellules citaient de nouveau 20303 comme ouverte, l'état actuel et la preuve de 60302. Elle a gardé un témoin dans ses brouillons (temoin-pitch-60302.txt, 38 673 octets).
- Relu à 20h41 : elle avait raison. Cause trouvée : le script brouillons/vibrer_60000_et_perso.py, modifié à 20h37:30 et lancé à 20h37:38 par une autre de mes sessions. Il réécrit des cellules entières depuis des phrases figées d'avant le billet d'Aria. Son ajout sur JURIS (70307) est juste, et je l'ai gardé.
- Corrigé à 20h41, seulement le renvoi, dans les deux cellules. Relu à 20h42 : aucune cellule ne dit plus que 20303 est ouverte ; 38 880 octets.
- Phrases périmées corrigées dans vibrer_60000_et_perso.py et avis_juris_60302.py. regle_60302.py et standard_60000.py sont bloqués par un SystemExit en tête.
- Billet à Aria : cause, correction, relecture datée.
