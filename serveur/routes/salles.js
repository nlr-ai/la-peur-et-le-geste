// GET /salles, /salles/<id>.jpg — les vues peintes des salles du plan.
//
// Les toiles d'un monde vivent dans SON paquet (`<monde>/salles/`), lu en
// premier : deux mondes ont chacun leur « escalier », et une toile commune
// mettrait la rampe de Prescott Street dans l'immeuble de Folsom Street.
// `ecrans/salles/` reste le repli — c'est là que Peyredragon a été peint.
//
// Le manifeste est servi une fois au chargement : sans lui, la page tenterait
// l'image et la retirerait sur erreur, et clignoterait à chaque salle qui n'en
// a pas. Rien à déclarer nulle part : déposer le fichier suffit.
const fs = require("fs");
const path = require("path");
const { DEPOT, RACINE, envoyer } = require("../http");

const dossiers = () => [path.join(RACINE, "salles"), path.join(DEPOT, "ecrans", "salles")];
const TYPES = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp" };

function traiter(req, res, url) {
  if (req.method !== "GET") return false;
  if (url === "/salles") {
    const ids = new Set();
    for (const d of dossiers()) {
      try {
        fs.readdirSync(d).filter((n) => TYPES[path.extname(n).toLowerCase()])
          .forEach((n) => ids.add(n.replace(/\.[^.]+$/, "")));
      } catch (e) {}
    }
    return envoyer(res, 200, JSON.stringify({ salles: [...ids] }));
  }
  if (url.startsWith("/salles/")) {
    const nom = path.basename(decodeURIComponent(url.slice("/salles/".length)));
    const type = TYPES[path.extname(nom).toLowerCase()];
    if (!type) return envoyer(res, 404, JSON.stringify({ erreur: nom }));
    for (const d of dossiers()) {
      try {
        const corps = fs.readFileSync(path.join(d, nom));
        res.writeHead(200, { "Content-Type": type, "Cache-Control": "public, max-age=86400" });
        return res.end(corps);
      } catch (e) {}
    }
    return envoyer(res, 404, JSON.stringify({ erreur: nom }));
  }
  return false;
}

module.exports = traiter;
