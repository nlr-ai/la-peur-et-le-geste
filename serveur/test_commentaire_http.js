// Une vraie requête, une vraie inbox, un vrai canal ; seul le réveil LLM est doublé.
const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn, spawnSync } = require("child_process");
const net = require("net");
const racine = fs.mkdtempSync(path.join(os.tmpdir(), "conseil-commentaire-"));
const env = { ...process.env, CONSEIL_RACINE: racine, CONSEIL_SANS_REVEIL: "1", VOIX_API: "0" };
function ecrire(rel, v) {
  const p = path.join(racine, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(v));
}
async function main() {
  const affaire = { id: "affaire-test", titre: "La porte", tenu_par: "aria", maison_id: "cite", acteur_id: "aria",
    type: "plan", tables: [
      { titre: "Ouverture", colonnes: ["Le champ", "Ce qu'on y écrit"],
        lignes: [{ cellules: ["LA PLAGE", "10000 à 10099"] }] },
      { titre: "États cibles", colonnes: ["N°", "L'état", "Ce qui doit être vrai", "La preuve"],
        lignes: [{ cellules: ["10000", "La porte tient", "Une porte ouverte", "Essai physique"] }] },
      { titre: "Verrous", colonnes: ["N°", "Le verrou", "Bloque", "Ce qui est vrai", "La preuve"],
        lignes: [{ cellules: ["10001", "La serrure", "10000", "Une serrure fermée", "Observation"] }] }
    ] };
  ecrire("etat/maisons/cite/documents/books/_ordre.json", [affaire.id]);
  ecrire("etat/books.json", []);
  ecrire("etat/maisons.json", [{ id: "cite", nom: "La cité" }]);
  ecrire("etat/maisons/cite/documents/books/affaire-test.json", affaire);
  ecrire("etat/personnages.json", [{ id: "nova", nom: "Nova", maison_id: "cite" },
    { id: "aria", nom: "Aria", maison_id: "cite" }]);
  ecrire("etat/joueurs.json", [{ personnage_id: "nova", jeton: "test", occupe: true }]);
  ecrire("etat/journal.json", { personnage_joueur_id: "nova" });
  ecrire("etat/monde.json", { date: { annee: 2042, lune: 1, jour: 1 } });
  for (const id of ["nova", "aria"]) {
    fs.mkdirSync(path.join(racine, "chambres", id), { recursive: true });
    fs.writeFileSync(path.join(racine, "chambres", id, "CLAUDE.md"), "# " + id);
  }
  const port = await new Promise(resolve => {
    const s = net.createServer();
    s.listen(0, "127.0.0.1", () => { const p = s.address().port; s.close(() => resolve(p)); });
  });
  const serveur = spawn(process.execPath, [path.join(__dirname, "serveur.js"), String(port)],
    { env, stdio: ["ignore", "pipe", "pipe"], windowsHide: true });
  try {
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error("Serveur muet")), 10000);
      serveur.stdout.on("data", b => { if (String(b).includes("Le Conseil écoute")) { clearTimeout(timeout); resolve(); } });
      serveur.once("exit", code => { clearTimeout(timeout); reject(new Error("Arrêt " + code)); });
    });
    const base = "http://127.0.0.1:" + port;
    const plateau = await (await fetch(base + "/echiquier?jeton=test")).json();
    const a = plateau.affaires.find(a => a.pieces);
    assert(a, JSON.stringify(plateau));
    const p = a.pieces.find(p => p.numero === "10001");
    assert.strictEqual(p.commentaire.nom, "Aria");
    const demande = { mode: "commenter", type: "commentaire", affaire_id: a.id,
      node_id: p.cle, texte: "Vérifie cette serrure.", destinataire_id: "intrus", contexte_id: "99999" };
    async function poster(d, jeton = "test") {
      return fetch(base + "/action?jeton=" + jeton, { method: "POST",
        headers: { "Content-Type": "application/json" }, body: JSON.stringify(d) });
    }
    assert.strictEqual((await poster(demande, "inconnu")).status, 400);
    assert.strictEqual((await poster({ ...demande, node_id: "inexistant" })).status, 400);
    assert.strictEqual((await poster({ ...demande, texte: " " })).status, 400);
    const r = await poster(demande);
    const retour = await r.json();
    assert.strictEqual(r.status, 200, JSON.stringify(retour));
    assert.strictEqual(retour.destinataire_id, "aria");
    assert.strictEqual(retour.contexte_id, "10001");
    const inbox = path.join(racine, "etat/inbox/nova");
    assert.strictEqual(fs.readdirSync(inbox).length, 1);
    const action = JSON.parse(fs.readFileSync(path.join(inbox, fs.readdirSync(inbox)[0])));
    assert(action.contexte_noeud.includes("Une serrure fermée"));
    assert(!fs.existsSync(path.join(racine, "etat/flux.jsonl")), "Le commentaire ne doit pas être crié dans la salle");
    const code = `import sys, os, json
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
from agents import expose, billet, mj, routeur_message
from unittest.mock import patch
routeur_message.SORTIES = os.path.join(os.environ['CONSEIL_RACINE'], 'recus')
with patch.object(mj, 'appeler_mj', return_value='traite') as narrateur, patch.object(billet, 'ecrire') as billet_direct:
    r = routeur_message.router_ref('nova', sys.argv[1])
    assert r['routage']['mj']['appele']
    assert narrateur.call_count == 1
    assert narrateur.call_args.kwargs['refs'] == [sys.argv[1]]
    assert narrateur.call_args.kwargs['routage']['destinataire_id'] == 'aria'
    billet_direct.assert_not_called()
print('Commentaire contextualise transmis une fois au narrateur : OK')`;
    const py = spawnSync(process.env.PYTHON || "python", ["-c", code, retour.ref],
      { env, cwd: path.join(__dirname, ".."), encoding: "utf8", windowsHide: true });
    assert.strictEqual(py.status, 0, py.stdout + py.stderr);
    assert.strictEqual(fs.readdirSync(inbox).length, 1);
    console.log(py.stdout.trim());
    console.log("Commenter HTTP : destinataire canonique, accès, refus et dépôt OK");
  } finally {
    serveur.kill();
    await new Promise(resolve => serveur.exitCode !== null ? resolve() : serveur.once("exit", resolve));
  }
}
main().catch(e => { console.error(e); process.exitCode = 1; }).finally(() => {
  // Le chemin est créé par mkdtemp ci-dessus, exclusivement pour cette épreuve.
  fs.rmSync(racine, { recursive: true, force: true });
});
