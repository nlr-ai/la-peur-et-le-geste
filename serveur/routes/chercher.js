// GET /chercher — un mot, et les quatre endroits où il peut être écrit : les
// cahiers, les fils qui courent, le fil du récit, les gens.
//
//   /chercher?q=roukerie[&max=8]     les quatre familles, comptées
//   /chercher?autour=7412[&marge=6]  la tranche de fil autour d'un résultat
//
// Le moteur est dans `domaine/recherche.js` ; ici, du transport et rien
// d'autre. Le siège est résolu une fois et descend au moteur : c'est LUI qui
// tient le brouillard (`filtrerFlux`, `volumesVisibles`), et non cette route —
// un tri écrit dans une route est un tri que la route suivante oubliera.
const { envoyer } = require("../http");
const { monPersonnage, qui } = require("../http");
const { autour, chercher } = require("../domaine/recherche");

function traiter(req, res, url) {
  if (req.method === "GET" && url === "/chercher") {
    const p = new URLSearchParams(req.url.split("?")[1] || "");
    // Sans jeton, on n'est personne, ici comme dans la scène : le moteur rend
    // alors un fil vide et une étagère vide. On ne le refuse pas par un 403 —
    // une recherche muette est la bonne réponse, et elle n'apprend rien sur ce
    // qu'il y avait à trouver.
    const siege = qui(req, url);
    try {
      if (p.has("autour")) {
        return envoyer(res, 200, JSON.stringify(autour({
          i: Number(p.get("autour")) || 0,
          marge: Number(p.get("marge")) || 0, siege })));
      }
      return envoyer(res, 200, JSON.stringify(chercher({
        q: p.get("q"), siege, moi: monPersonnage(req, url),
        max: Number(p.get("max")) || 0 })));
    } catch (e) {
      // Une recherche qui casse ne doit pas casser la scène : la page dira
      // qu'elle n'a rien trouvé, le journal du serveur portera la raison.
      console.error("GET /chercher —", e.message || e);
      return envoyer(res, 500, JSON.stringify({ erreur: "recherche-indisponible" }));
    }
  }
  return false;
}

module.exports = traiter;
