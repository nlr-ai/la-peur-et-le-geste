# Implantation initiale — conventions de partie

Le joueur a accepté la préparation du départ avec Claire déjà à Leoch depuis quelques jours. Le présent lot fixe trois jours, et une horloge conventionnelle au 4 mai 1743 à 10 h. Ces repères sont des choix de partie ; ce n'est pas une datation exacte de l'épisode. La date de notre époque reste ouverte.

Aurore arrive seule aux pierres ; Nicolas arrive à la lisière en contrebas, à huit minutes de marche conventionnelle. Aucun des deux ne voit l'autre ni ne connaît sa position. Cette correction demandée par le joueur remplace le départ commun ; les anciens items du flux sont conservés comme historique, puis remplacés à l'écran par deux introductions privées. Claire, Jamie, Colum et Dougal sont initialement situés à Leoch. Les quatre PNJ ont des intentions générales de préparation ; aucun acte, dialogue ou résultat de travail n'a été inventé pour eux. Leurs plans datés et routines seront établis par leurs sessions avant une simulation hors scène.

## Géographie locale ajoutée

Pierres → lisière : 8 minutes à pied ; lisière → croisée : 7 minutes ; croisée → ferme du ruisseau : 12 minutes. Ces durées et ces trois lieux secondaires sont des ajouts déclarés, pas une géographie officielle de la série. Le relief retenu est une colline boisée avec un chemin descendant. La ferme est une habitation possible, sans occupants ni ressources présumés. Sa présence dans l'état ne donne pas aux PJ la connaissance du chemin.

Inverness, Leoch et Cranesmuir sont référencés, mais leurs routes ne sont pas raccordées : aucune distance canonique n'est inventée. Il n'y a aucune patrouille placée pour rencontrer les PJ.

## Sièges et connaissances

Les deux sièges sont protégés comme PJ pendant la préparation. Le drapeau d'occupation ne constitue pas la preuve d'une session web active. Les profils ne portent ni naissance, ni métier, ni relation présumée, ni bagage. Les dossiers de croyances sont vides ; les PJ n'ont pas appris l'année ou la présence de Claire par la seule création de l'état.

Le journal choisit Aurore comme siège principal technique ; Nicolas possède un siège distinct. `maison_joueur_id` est nul : aucune maison de voyageurs n'est inventée. Ne pas déclencher la création de maison westerosienne à cause de ce champ.

La première scène n'est pas ouverte. Aucun flux, appel PNJ ou avance de temps n'a eu lieu. Avant simulation, établir les routines des PNJ et gérer l'occupation réelle des sièges. Les ressources du clan ne sont pas chiffrées ; aucune dépense ou levée ne peut être déduite d'une absence de valeur.

## Vérification du moteur

L'audit `tick.py --verifier` lit cet état, mais ne le valide pas pour une simulation : aucun signal de session ne prouve encore l'occupation des deux sièges et les rapporteurs de plan n'ont jamais tourné dans ce monde neuf. Ne pas fabriquer de signaux de présence ou une tête de PJ pour rendre cet audit vert. Les croyances initiales canoniques sont des données de départ, pas des rapports de PNJ obtenus dans cette partie.
