// GET /monde.js et /monde.json — CE QUE LE MONDE DIT DE LUI-MÊME, servi à l'écran.
//
// POURQUOI CETTE ROUTE EXISTE (lot 3, docs/refonte-plan.md §4).
// Trois modules d'écran portaient des données de monde EN DUR : `plans.js`
// (899 lignes de plans de château, dont un Braavos fabriqué par un
// `replaceAll("Peyredragon","Braavos")` au chargement de la page), `blasons.js`
// (qui porte quelles armes) et `carte.js` (les étiquettes de lieux, les noms de
// mers, le nom du cadrage « westeros »). Tant que ces tables vivaient dans le
// code, un second monde ne pouvait pas exister sans retoucher le moteur — c'est
// l'assertion E12 du plan, et c'était non.
//
// Les trois familles partent ENSEMBLE, en un seul aller-retour et en un seul
// script, pour une raison de chargement et non de goût : `blasons.js`,
// `carte.js` et `plans.js` lisent leurs tables au moment où le navigateur les
// évalue. Un `fetch` les servirait trop tard — la table peinte serait dessinée
// nue, puis repeinte. Le script est donc posé AVANT eux dans `ecrans/jeu.html`,
// et il pose UNE globale, `window.MONDE` : la porte du monde, comme
// `books/books.js` pose la porte des livres.
//
// OÙ VIVENT LES DONNÉES, ET POURQUOI LÀ.
// Au format du paquet (`refonte-plan.md` §3) : `plans/`, `blasons/`, `carte/`
// et `manifeste.json` à la racine DU MONDE, à côté d'`etat/` et de `chambres/`.
// En disposition héritée, cette racine est celle du dépôt — c'est déjà là que le
// lot 4 a posé `manifeste.json`. Le jour où le monde réel descend dans
// `mondes/westeros/` (lot 2), ces dossiers descendent avec lui et cette route ne
// change pas d'une ligne : elle ne connaît que `RACINE`.
//
// ELLE NE SERT AUCUNE CROYANCE. Un plan de salles, des armes et des noms de mers
// sont le même objet pour tout le monde : pas de siège, pas de brouillard, pas
// de `qui(req)`. Ce qu'un joueur CROIT (jetons, vues, objectifs) passe par
// `/carte`, qui filtre par siège — et ne passe jamais par ici.
"use strict";
const fs = require("fs");
const path = require("path");
const { RACINE } = require("../http");
const { envoyer } = require("../http");

function lire(...bouts) {
  try { return JSON.parse(fs.readFileSync(path.join(RACINE, ...bouts), "utf-8")); }
  catch (e) { return null; }
}

// Un plan par fichier : `plans/peyredragon.json`. Le nom du fichier EST l'id du
// plan (`port-real@marlo-vasse.json` compris), parce que c'est cet id que
// `plan.js` cherche depuis l'en-tête de lieu du bandeau.
function plans() {
  const dossier = path.join(RACINE, "plans");
  let noms;
  try { noms = fs.readdirSync(dossier); } catch (e) { return {}; }
  const out = {};
  noms.forEach((n) => {
    if (!n.endsWith(".json") || n.startsWith(".")) return;
    const p = lire("plans", n);
    if (p) out[n.slice(0, -5)] = p;
  });
  return out;
}

// Les armes sont écrites avec le NOM de leurs émaux (« nuit », « gueules ») et
// non leur teinte : c'est le seul mot qui dise ce que c'est, et l'ancienne table
// le perdait dès qu'on la sérialisait. La résolution nom → teinte se fait à
// l'écran, dans `blasons.js`, qui reçoit les deux.
function blasons() {
  const armes = lire("blasons", "armes.json") || {};
  const charges = lire("blasons", "charges.json") || {};
  return {
    emaux: armes.emaux || {},
    armes: armes.armes || {},
    charges: charges.charges || {},
  };
}

// Le manifeste part avec eux — c'est le même paquet, et `jetons.js` l'attend
// déjà sous `window.MANIFESTE` (lot 4, écrit avant que quiconque le serve).
function paquet() {
  return {
    manifeste: lire("manifeste.json") || {},
    plans: plans(),
    blasons: blasons(),
    carte: lire("carte", "cadrages.json") || {},
  };
}

function traiter(req, res, url) {
  if (req.method !== "GET") return false;
  // Aperçus publics des plans du monde : aucune position ni action de joueur.
  const apercu = /^\/plans\/([a-z0-9-]+)\.(svg|html)$/.exec(url);
  if (apercu) {
    try {
      const contenu = fs.readFileSync(path.join(RACINE, "plans", apercu[1] + "." + apercu[2]), "utf-8");
      return envoyer(res, 200, contenu, apercu[2] === "svg" ? "image/svg+xml; charset=utf-8" : "text/html; charset=utf-8");
    } catch (e) { return envoyer(res, 404, "Plan absent"); }
  }
  // Le script, pour la page : une globale, posée avant tout ce qui la lit.
  if (url === "/monde.js") {
    return envoyer(res, 200, "window.MONDE=" + JSON.stringify(paquet()) + ";",
      "text/javascript; charset=utf-8");
  }
  // Le même paquet en clair, pour qui veut le lire sans navigateur : une
  // vérification, un atelier, un second écran.
  if (url === "/monde.json") {
    return envoyer(res, 200, JSON.stringify(paquet()));
  }
  return false;
}

module.exports = traiter;
