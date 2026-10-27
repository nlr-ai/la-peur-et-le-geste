// GET /mondes — ce qu'on peut ouvrir d'ici : les mondes, et les parties en
// cartes du monde courant. C'est la liste que sert le menu « La partie » du
// rail (ecrans/modules/mondes.js).
//
// UN MONDE PAR PROCESSUS, DONC UN MONDE PAR PORT. Le serveur ne bascule pas de
// monde à chaud (racines.js : il résout au chargement) ; changer de monde,
// c'est changer d'adresse. Le port de chaque monde se lit dans
// `.claude/launch.json`, qui est la seule table qui les déclare : une
// configuration `serveur/serveur.js --monde <id>` sert ce monde, une
// configuration sans `--monde` sert la disposition héritée (Westeros). Un monde
// sans configuration est listé sans port — il existe, on ne sait pas où le
// joindre, et l'on ne devine pas.
//
// Rien ne dit ici si l'autre serveur TOURNE : c'est au navigateur de le
// constater en y allant. On ne sonde pas les ports voisins à chaque requête.
const fs = require("fs");
const path = require("path");
const racines = require("../racines");
const { envoyer, DEPOT, PORT } = require("../http");
const { DOSSIER, campsDe, partieDe } = require("../domaine/partie");

function mondeDe(args) {
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === "--monde" && args[i + 1]) return String(args[i + 1]).trim();
    const m = /^--monde=(.+)$/.exec(String(args[i]));
    if (m) return m[1].trim();
  }
  return null;
}

// id de monde (null = hérité) -> port. La configuration « jeu » gagne pour le
// monde hérité : c'est la partie en cours, les autres sont des ateliers.
function ports() {
  const out = new Map();
  let confs = [];
  try {
    confs = JSON.parse(fs.readFileSync(path.join(DEPOT, ".claude", "launch.json"), "utf-8")).configurations || [];
  } catch (e) { return out; }
  const serveurs = confs.filter((c) => (c.runtimeArgs || []).includes("serveur/serveur.js") && c.port);
  serveurs.sort((a, b) => (b.name === "jeu") - (a.name === "jeu"));
  for (const c of serveurs) {
    const m = mondeDe(c.runtimeArgs);
    if (!out.has(m)) out.set(m, c.port);
  }
  return out;
}

function nomDe(monde) {
  try { return racines.manifeste(monde).nom || monde || "Westeros"; }
  catch (e) { return monde || "Westeros"; }
}

function mondes() {
  const p = ports();
  const courant = racines.courant();
  const ids = [null].concat(racines.mondes());
  return ids.map((id) => ({
    id: id || "westeros",
    nom: nomDe(id),
    // Le monde qu'on regarde a le port qu'on vient d'appeler, quoi que dise
    // la table : un atelier lancé sur un port de fortune reste le courant.
    port: id === courant ? PORT : (p.get(id) || null),
    courant: id === courant,
  }));
}

// Les parties en cartes : un jsonl par partie. Ce qui commence par `_` est de
// la tuyauterie du greffe, et les essais de mise au point n'ont rien à faire
// dans un menu de joueur.
const OUTILS = /^(_|audit-|debug-|diagnostic-|essai-)/;

function parties() {
  let fichiers;
  try { fichiers = fs.readdirSync(DOSSIER).filter((f) => f.endsWith(".jsonl")); }
  catch (e) { return []; }
  const courante = partieDe("/partie");
  return fichiers
    .map((f) => f.slice(0, -".jsonl".length))
    .filter((id) => !OUTILS.test(id))
    .map((id) => {
      let note = "", t = 0;
      try { note = JSON.parse(fs.readFileSync(path.join(DOSSIER, id + ".json"), "utf-8")).note || ""; }
      catch (e) {}
      try { t = fs.statSync(path.join(DOSSIER, id + ".jsonl")).mtimeMs; } catch (e) {}
      return {
        id,
        note: String(note).split(/(?<=\.)\s/)[0].slice(0, 240),
        camps: [...campsDe(id)].filter((c) => c !== "arbitre"),
        courante: id === courante,
        t,
      };
    })
    .sort((a, b) => b.t - a.t)
    .map(({ t, ...p }) => p);
}

module.exports = function traiter(req, res, url) {
  if (req.method === "GET" && url === "/mondes") {
    return envoyer(res, 200, JSON.stringify({ mondes: mondes(), parties: parties() }));
  }
  return false;
};
