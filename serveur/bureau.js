// Un processus par monde pendant la migration des racines (refonte-plan, §5).
const http = require("node:http");
const { racine, DEPOT } = require("./racines");
const { creerBureau } = require("./domaine/bureau");
const { routesBureau } = require("./routes/bureau");

const port = Number(process.env.PORT || process.argv[2] || 3135);
let traiter, bureau;
const serveur = http.createServer((req, res) => {
  try { traiter(req, res); }
  catch (e) { res.writeHead(500, { "Content-Type": "application/json" }); res.end(JSON.stringify({ erreur: e.message })); }
});
serveur.listen(port, "127.0.0.1", () => {
  try {
    bureau = creerBureau(racine(), DEPOT);
    bureau.definirAdresse(`http://127.0.0.1:${serveur.address().port}`);
    traiter = routesBureau(bureau, DEPOT);
    console.log(`Bureau disponible : http://127.0.0.1:${serveur.address().port}`);
  } catch (e) { console.error(e.message); serveur.close(); process.exitCode = 1; }
});
serveur.on("error", e => { console.error(e.message); process.exitCode = 1; });
process.on("SIGINT", () => {
  if (bureau?.actifs.size) { console.error("Des agents travaillent encore ; attendre leur fin."); return; }
  bureau?.fermer(); serveur.close();
});
