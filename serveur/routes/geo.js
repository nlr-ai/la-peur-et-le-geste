// GET /modules/geo.js — la géométrie de la table peinte, celle DU MONDE.
//
// `ecrans/modules/geo.js` est Westeros, engendré du mod AGOT. Servi tel quel à
// tous les mondes, il posait les côtes de Westeros sous la baie de San
// Francisco : la table était juste pour un seul monde. Un monde qui porte sa
// propre géométrie la dépose dans `<monde>/carte/geo.js` (même format,
// `window.Geo`) ; sans elle, on rend `false` et le module du dépôt part comme
// avant. Placée avant la route des modules, sinon celle-ci la masque.
"use strict";
const fs = require("fs");
const path = require("path");
const { RACINE, envoyer } = require("../http");

module.exports = function traiter(req, res, url) {
  if (req.method !== "GET" || url !== "/modules/geo.js") return false;
  let corps;
  try { corps = fs.readFileSync(path.join(RACINE, "carte", "geo.js"), "utf-8"); }
  catch (e) { return false; }
  return envoyer(res, 200, corps, "text/javascript; charset=utf-8");
};
