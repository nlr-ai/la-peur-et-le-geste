# Préparer un passage unique des PNJ-PJ de journée

Commande explicite du joueur : fais tourner une fois chacun des personnages qui
en ont besoin, puis notifier le MJ joueur de Michel. Tu prépares ici le passage ;
le lanceur extérieur exécutera la liste après ton retour. NE LANCE PAS les pilotes
à l'intérieur de cette session : ils attendraient ton verrou commun.

Lis l'état courant du monde la-peur-et-le-geste, les horloges des sièges,
intentions, actes, événements, fiches et sources. La journée de Michel fait autorité
pour ce passage : ne confonds pas sa date avec celle d'une autre scène.
Passe en revue tous les PNJ canoniques : autorités allemandes, personnes en poste,
habitants et initiatives clandestines déjà établies. Ne crée aucun réseau futur
pour remplir la journée ; respecte notamment l'arrivée effective des occupants.
Un personnage est à activer s'il reçoit une nouvelle pertinente, a une échéance,
un problème concret ou un projet réalisable à poursuivre aujourd'hui. Sinon,
écarte-le avec son motif. Exclure les sièges humains occupés, dont Michel et Raymond.

Pour chaque retenu, préparer chambres/<id>/joueur.md avec seulement son point de
vue : métier, moyens établis, obligations, objectifs, faits réellement appris,
contacts connus et date de travail. Conserver les éléments valides déjà présents.
Pas de secrets d'autrui, pas de résultat inventé. L'en-tête peut porter
--- puis connus: id1, id2 puis --- sur trois lignes.
Ne modifie pas joueurs.json : le pilote utilise un siège temporaire.

Écrire le manifeste JSON à l'adresse fournie :
{"date":"date du passage", "acteurs":[{"id":"id canonique", "motif":"raison concrète", "messages":2}],
 "ecartes":[{"id":"id canonique", "motif":"raison"}]}
Un seul exemplaire de chaque acteur, un ou deux messages maximum par acteur.
Aucun plafond artificiel de personnes : retenir tous ceux qui ont une raison.
Si personne n'a besoin d'agir, acteurs est vide. Préparer seulement les points de
vue et le manifeste, sans pousser de scène ni avancer l'heure ni traiter l'inbox
du joueur. Rends ensuite la main. Le lanceur fera jouer chaque sélectionné une
fois au MJ commun, puis réveillera le MJ de Michel avec le bilan effectif.


## Autonomie des postes et des autres initiatives

L'absence de demande de Michel n'est PAS un motif d'inactivité. Pour chaque
personne en poste, pars de ses attributions documentées : courrier à vérifier,
service à assurer, demandes à instruire, ressources à contrôler, situation à
observer. Donne-lui une tâche concrète réalisable aujourd'hui et une échéance
lorsque sa fonction implique ce travail. Inscris cet objectif de simulation
nouveau dans ses intentions selon le schéma existant et dans son point de vue.
Distingue clairement cette mise en activité créée pour la partie des faits
historiques ou déjà accomplis. Ne fabrique ni commande reçue, ni incident, ni
chiffre, ni matériel possédé : une vérification peut précisément découvrir
qu'il n'y a rien à signaler. Le pilote décide comment agir et le MJ arbitre.

Pour les habitants, exploite aussi leurs intérêts et liens propres, sans ramener
toute initiative à Michel. D'autres solidarités ou projets clandestins peuvent
naître de démarches cohérentes, mais ne décrète pas un réseau constitué ni une
réussite. Les Allemands non encore arrivés ne sont pas téléportés sur place :
ne les active ailleurs que si leur situation et leurs moyens sont établis.
La ferveur seule ne prouve pas une action. Le manifeste distingue les motifs
« échéance existante », « travail de fonction » et « initiative personnelle ».

Ce passage remplace un essai bloqué avant le premier message des pilotes : lis
le statut de 20261022-premier-passage, vérifie qu'aucune action n'a été envoyée
avant de reprendre un travail déjà prévu. Utilise la date ACTUELLE de Michel,
pas automatiquement le 16 juin du manifeste précédent.
