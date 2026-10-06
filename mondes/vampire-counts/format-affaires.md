# Les affaires de la Terre des Cinq — préparer un monde avant les rencontres

Le modèle reprend la forme actuelle des livres (`docs/books.md`) et le rangement des affaires personnelles (`scripts/agents/chambre_affaire.py`) : JSON de livre, tables, colonnes, lignes et cellules. Il conserve les quatre types du graphe personnel : états cibles C, verrous V, clefs K, actions P. Aucun champ n’est ajouté au schéma d’état.

## Une affaire par porteur stratégique

`chambres/<id>/books/affaire-<id>.json` est son dossier durable : plusieurs ambitions dans le même cahier, pas une affaire neuve pour chaque obstacle. Le registre compagnon est `registre-etats-<id>.json`. Ces cahiers techniques n’établissent pas l’existence de carnets physiques. Les modèles vivent sous `modeles/`, hors des bibliothèques jouées.

Les huit dimensions sont : fins et doctrine ; personnes et relations ; pouvoir et accès ; moyens matériels ; savoirs et secrets ; engagements et temps ; stratégie et alternatives ; zones à peindre. Elles sont des angles de préparation : ne pas inventer une ambition dans chaque case pour remplir le tableau.

Les cibles décrivent ce que le porteur souhaite rendre vrai. Les verrous décrivent ce qui l’empêche. Les clefs sont des voies possibles avec leur prix ; les actions sont ses démarches, leur porteur et leur échéance. La stratégie explique pourquoi il choisit cette voie et quand il en changerait. Les trous désignent ce qu’il doit encore définir, rechercher, produire ou obtenir.

## États de choses

Six catégories : lieux et passages ; objets et documents ; ressources et populations ; organisations et dispositifs ; usages et institutions ; situations et processus. Une chose peut avoir des liens vers plusieurs catégories sans être dupliquée. Une référence locale n’est pas un numéro global de registre.

Chaque ligne pose son identité, sa place, sa responsabilité, son état, ses propriétés, usages, limites, liens, évolutions, provenance et répartition des connaissances. Distinguer statut `établi`, `peint`, `hypothèse`, `inconnu`. La propriété d’une chose, l’accès à cette chose et la connaissance de son existence sont distincts.

Les tables existantes gardent autorité pour personnages, lieux, relations, actes et intentions. Une quantité suivie par les mains reste chez sa maison d’autorité. Le registre cite ces sources ; il n’en tient pas une seconde copie concurrente. Un détail descriptif sans table spécialisée peut rester dans le registre.

## Combler les trous

- **Définir** : peindre l’implantation initiale encore indéfinie, cohérente avec canon, époque, rang et ressources. Objets ordinaires, lieux, habitudes, activités, personnes secondaires et relations peuvent ainsi exister avant les PJ. Noter provenance et statut peint.
- **Chercher** : une information inconnue du personnage nécessite une source accessible. Une hypothèse ne devient pas une nouvelle reçue.
- **Produire** : fabriquer ou modifier pendant le jeu engage compétence, matière, outils et durée. Écrire le fait après accomplissement, pas en cochant une préparation.
- **Obtenir** : un accord, une réponse ou une décision d’autrui passe par cet autre acteur ; l’issue n’est pas inventée.

Créer une nouvelle personne ne joue pas ses paroles et gestes. Lui donner une fiche, une tête et un cahier si elle porte une stratégie ; la dépêcher avant de la jouer. Ne pas fabriquer une rencontre avec les PJ. Un moyen conséquent exige une implantation et des contreparties cohérentes ; pas de réserve, preuve ou allié providentiel pour effacer un verrou.

## Usage au réveil

Le porteur ouvre ses deux cahiers, examine les zones manquantes utiles à ses fins, puis les complète selon les quatre gestes ci-dessus. Il n’a pas à remplir toutes les catégories avant de répondre. Les cases inconnues ne sont ni des interdictions de créer ni des excuses pour rester muet. Les croyances et plans exécutables demeurent dans `intentions.json` ; seuls les choix arrêtés et leurs étapes datées y passent.

Le graphe existant reconnaît C/V/K/P. Les tables supplémentaires sont lisibles comme livres ; elles ne deviennent pas automatiquement des nœuds calculés. Les états de choses n’ont pas de moteur générique nouveau dans ce lot.
