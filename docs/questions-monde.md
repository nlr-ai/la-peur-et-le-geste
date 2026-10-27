# Questions factuelles des PNJ au MJ

Un monde peut activer `pnj_autorises: true` dans
`.agents-runtime/questions-monde.json`. Les autres mondes gardent l'interdit
historique jusqu'à cette activation et l'adaptation de leurs instructions.

```powershell
python scripts/parloir.py --question-monde --de isobel-grant --a mj "Quel embranchement rejoint Inverness ?"
```

Le PNJ reçoit une réponse sourcée en sortie de commande et dans son canal MJ.
`--contexte` et `--ref` restent disponibles. Un retry de la même question,
référence et contexte retrouve la réponse enregistrée. La consultation ne
réveille pas un tour joueur, ne pousse pas de dialogue et ne fait avancer
aucune horloge. Elle a une session MJ factuelle par monde et demandeur.

Le MJ peut vérifier un fait, expliquer la limite du worldpainting ou établir
et consigner un détail manquant dans son registre canonique approprié. Il
distingue ce qui existe de ce que cet habitant peut savoir. Les secrets restent
cachés ; les décisions et demandes de permission restent au PNJ.

Cette consultation utilise un verrou distinct du tour joueur : le MJ de la
scène peut attendre ce PNJ sans que la question fasse attendre le même MJ sur
son propre verrou. Aucun appel imbriqué de session n'est autorisé depuis la
consultation. Les réponses techniques ne deviennent pas des paroles en scène :
le PNJ reprend ensuite sa propre incarnation et ses propres mots.
