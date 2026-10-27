# Extensions de partie — lieux et projets

À la demande du joueur (« puis créé des trucs »), six lieux enrichissent le décor initial : Quai commun, Halle des maquettes, Ateliers modulaires, Belvédère des plans, Bassin d’essais et Jardin calme. Leur architecture et leur usage sont consignés dans le volume **Six lieux à parcourir**, accessible au Radiant Core.

Ce sont des créations pour cette partie, ajoutées aux quartiers existants. Elles ne déplacent aucune identité ou activité des récits sources. Leur inscription n’est pas une construction effectuée pendant la scène. Le champ technique `ville` sert aux entrées de carte, y compris aux sous-lieux ; il ne leur donne pas le statut d’une cité indépendante. Les accès locaux valent conventionnellement une minute de navigation VR.

Le volume **Trois projets pour les quartiers** contient des pistes, sans chantier lancé : promenade continue, atelier ouvert, pièce confidentielle. Il n’attribue aucune parole ou initiative aux PNJ, ne tranche pas pour Nova et ne fait pas avancer le temps.

Installation idempotente : `python mondes/lumina-prime/outils/enrichir.py`. Après une régénération de la carte par `amenager.py`, relancer `enrichir.py` pour restaurer ses six repères et accès. Les volumes existants sont conservés.
