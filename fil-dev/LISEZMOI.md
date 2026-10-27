# Fil dev

Un fil commun où deux sessions Claude Code publient, chacune de son côté,
le prompt qu'on leur donne et la réponse qu'elles rendent. On le lit dans une
page, en direct (rafraîchie toutes les deux secondes).

- `serveur.js` : range le fil dans `fil.jsonl` et sert la page. N'écoute que
  sur 127.0.0.1. Engendre `jeton.txt` au premier lancement (ou prend
  `FIL_DEV_JETON`). Ces deux fichiers sont ignorés par git.
- `.claude/hooks/fil-dev.js` : branché sur SessionStart, UserPromptSubmit et
  Stop dans `.claude/settings.json`. Il ne fait rien tant que `FIL_DEV_URL`
  n'est pas posé, et n'empêche jamais une session de tourner.

## Chez celui qui héberge

```bash
node fil-dev/serveur.js 3300
```

(ou l'entrée `fil-dev` de `.claude/launch.json`), puis le tunnel :

```bash
cloudflared tunnel --no-autoupdate --url http://localhost:3300
```

Le tunnel rapide donne une adresse `https://….trycloudflare.com` qui change
à chaque lancement. Pour une adresse stable, il faut un tunnel cloudflared
nommé, ou `tailscale funnel 3300` (si vous êtes tous les deux sur le même
tailnet, `tailscale serve 3300` suffit et rien n'est public).

Dans `.claude/settings.local.json` :

```json
"env": { "FIL_DEV_URL": "http://localhost:3300", "FIL_DEV_JETON": "<jeton.txt>" }
```

## Chez l'autre

Même dépôt, même `.claude/settings.json`. Dans son `.claude/settings.local.json` :

```json
"env": {
  "FIL_DEV_URL": "https://<adresse du tunnel>",
  "FIL_DEV_JETON": "<le jeton, transmis à part>",
  "FIL_DEV_AUTEUR": "<son prénom>"
}
```

La page : `https://<adresse du tunnel>/?jeton=<le jeton>`. Le jeton passe
ensuite dans un cookie et disparaît de la barre d'adresse.

## Ce qu'il faut savoir

- Les variables d'environnement sont lues au démarrage d'une session : une
  session déjà ouverte ne publie qu'après redémarrage.
- Tout ce qu'on écrit à Claude et tout ce qu'il répond part sur le fil,
  secrets compris s'il y en a dans un prompt. Le jeton garde la porte du
  tunnel ; ne le mettez jamais dans `settings.json`, qui est versionné.
- La page est un fil de lecture. Les sessions ne lisent pas le fil : pour que
  l'une sache ce que fait l'autre, il faudrait un hook qui le réinjecte en
  contexte.
