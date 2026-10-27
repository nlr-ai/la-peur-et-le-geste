# Ferveur de Modern Front

`liaison-ferveurs.json` raccorde les identités narratives aux résidents de la simulation `arrival`, graine 1. Le serveur vérifie le numéro, le prénom et le nom avant d'utiliser une valeur. Les personnages issus d'anciens exports dont l'identité n'est pas raccordée conservent leur valeur importée.

Le pont `tools/ModernFront.UnityBridge` de Modern Front publie atomiquement `out/la-peur-et-le-geste/ferveurs-sim.json` après chaque requête snapshot, sample ou advance. Il lit la ferveur courante des réunions, puis le tempérament par défaut ; pour les occupants allemands, il utilise leur ferveur propre. L'export ne contient ni secrets ni intentions. `MODERN_FRONT_FERVOUR_OUTPUT` permet de choisir un autre fichier de sortie.

Le site relit cet export dans `/gens`. Le navigateur rafraîchit son registre toutes les 30 secondes. Le survol de la flamme indique la date simulée du dernier état. Si le pont est arrêté, le dernier export reste affiché ; une erreur de lecture conserve les anciennes valeurs importées. Le site ne fait pas avancer la simulation en ouvrant une page.

Mise en service : export réel de l'initialisation `arrival`, 15 juin 1940 à 08:00, Michel 0/100, Lucien 36/100. Ce n'est pas une reprise d'une sauvegarde Unity. La progression ultérieure vient du pont Unity lorsqu'il tourne. Les actions du MJ narratif ne sont pas encore transmises à Modern Front ; cette liaison est uniquement simulation → interface.

## Michel : autorité du joueur

Depuis la correction du profil de Michel, `choix_joueur` dans la configuration désigne `Modern Front/content/player_choices.json`. Ce registre daté est l'autorité de sa ferveur : base 30, puis conséquences explicites des choix. Son premier choix d'agir ajoute 10, donc 40 au 15 juin à 12:30. Le site montre le dernier choix consigné même si le pont de simulation n'a pas encore atteint cette heure ; le moteur applique chaque conséquence uniquement à partir de sa date. Les infobulles distinguent cette origine de celle des PNJ.

Le moteur conserve la consommation du tirage aléatoire pour ne pas changer les autres habitants, mais remplace le résultat de Michel par un profil `player`, sans traits imposés. Les effets automatiques des nouvelles et réunions sont ignorés pour sa ferveur. Le pont recharge le registre de choix avant chaque requête. Après une mise à jour du code, relancer un pont Unity déjà ouvert pour prendre en compte le profil corrigé.

Les décisions en texte libre sont évaluées par le MJ via `scripts/ferveur_joueur.py`, avant nettoyage de l'inbox ; il n'y a pas de classement automatique par mots-clés. Le script vérifie la référence, exige une date de fiction et refuse les commandes hors fiction ainsi que les préférences de l'entretien. Chaque référence est comptée une seule fois. Voir le barème et les obligations dans AGENTS.md du monde.
