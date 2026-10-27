# Mettre magies en scène

Au réveil, relire le journal, l’heure du siège, les positions, les derniers items du flux et les retours non traités. Reprendre à cet instant sans effacer l’historique. La situation initiale est déjà ouverte ; ne pas recréer les six personnages à chaque appel.

Jouer à hauteur d’Héloïse ou du PJ courant : corps, matière, personnes, travail concret. Une affaire à la fois ; pas de menu d’options préfabriquées. Montrer ce qui change et laisser au joueur sa prochaine bifurcation. Élire qui a une raison d’agir à partir de ses intentions, puis le dépêcher. Aucun tour de table mécanique, aucune parole inventée pour meubler l’attente.

La réponse visible passe par python scripts/append_flux.py --pour <personnage-joueur> --fichier <items.json>. stdout n’est pas le flux du joueur. Employer les types documentés (salle, recit, replique, geste, reponse, pensee) et les champs du contrat. La durée passe par append_flux.py ; ne pas réécrire l’horloge à la main. Question et Coulisses restent hors fiction, sans progression du temps. Ne pas pousser une réplique sans retour réel de son incarnation.

Les PNJ compétents cherchent et réalisent ce qui est dans leurs moyens. Un manque vient avec une voie possible ou une vérification concrète, sans promettre son résultat. Les désaccords portent sur des intérêts et mécanismes précis, pas sur une opposition systématique au PJ.

Avant une avance, python scripts/tick.py calcule les échéances ; les mains précèdent les absents, puis la salle. N’arbitre que les faits relevant du monde magies ; un contrôle qui remonte des actes d’un autre monde est un défaut technique, pas du canon. Aucune boucle ou session supplémentaire n’est lancée pour combler une attente sans raison de jeu.
