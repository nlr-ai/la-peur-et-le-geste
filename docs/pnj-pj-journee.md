# Mode PNJ-PJ journée

Depuis le dépôt la-peur-et-le-geste :

```powershell
python scripts/joueur_pnj.py --monde la-peur-et-le-geste --qui <id-du-siege> --port 3212 --journee --messages 2 --voir
```

Retirer `--voir` pour jouer réellement. Le siège doit déjà être configuré dans
joueurs.json et disposer de chambres/<id>/joueur.md contenant uniquement son
point de vue. Ne pas lancer ce pilote sur le siège tenu par un humain.

`--messages 1` regroupe le programme en un envoi ; `--messages 2` ajoute un
ajustement après réponse du MJ. Deux est le défaut. `--tours` est incompatible
avec ce mode. Chaque lancement traite une seule journée, sans boucle quotidienne
automatique ni avancement direct de l'horloge.

Le prompt dédié est scripts/agents/prompts/joueur-pnj-journee.md : `agir` est
prioritaire, `dire` exceptionnel. Le canal API reste `agir`, pas `action`.
Le modèle propose des tentatives et des replis ; le MJ en arbitre les résultats.
Le budget est un nombre maximal d'envois du pilote, pas une garantie de résolution
de la journée. Sans retour final du MJ, le pilote signale la journée non confirmée.

Vérification locale sans appel de modèle ni écriture dans la partie :
`python -m unittest discover -s scripts/tests -p test_joueur_pnj_journee.py`

## MJ commun

Tous les envois de ce mode portent `pilote_mode: pnjpj-journee`, y compris les
rares paroles. Le routeur les adresse à une session MJ commune au monde,
indépendante de la scène de chaque acteur. La file existante sérialise les appels ;
un autre acteur en attente n'interrompt pas l'arbitrage courant. La rotation normale
de session conserve cette identité commune par génération.

Les scènes et audiences ne fusionnent pas : le MJ reçoit les intentions de chacun,
mais chaque personnage ne lit que son propre fil. Les autres modes gardent leur
routage habituel. Les reprises ne regroupent pas les actions ordinaires avec les
journées hors scène.
