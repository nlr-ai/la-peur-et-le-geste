// GET /fiche — la fiche du personnage qu'on incarne : ce qu'il a sous la main
// et qui il connaît, telle qu'elle est écrite dans son dossier de siège
// (`etat/joueurs/<id>/fiche.json`). On ne sert jamais que la SIENNE : la fiche
// d'un autre siège est sa croyance à lui, et le brouillard est par siège.
const fs = require("fs");
const path = require("path");
const { ETAT, envoyer, qui } = require("../http");
const { portraitDefaut, portraitFrais } = require("../peinture").portraits;

module.exports = function traiter(req, res, url) {
  if (req.method !== "GET" || url !== "/fiche") return false;
  const siege = qui(req, url);
  const id = siege && siege.personnage_id;
  if (!id || !/^[a-z0-9-]+$/.test(id)) return envoyer(res, 200, JSON.stringify({ fiche: null }));
  try {
    const fiche = JSON.parse(fs.readFileSync(path.join(ETAT, "joueurs", id, "fiche.json"), "utf-8"));
    (fiche.contacts || []).forEach((c) => (c.gens || []).forEach((g) => {
      if (g.id) g.portrait_svg = portraitFrais(g.id) || portraitDefaut(g.nom || g.id);
    }));
    return envoyer(res, 200, JSON.stringify({ fiche }));
  } catch (e) {
    // pas de fiche écrite pour ce siège : la page n'a rien à ouvrir
    return envoyer(res, 200, JSON.stringify({ fiche: null }));
  }
};
