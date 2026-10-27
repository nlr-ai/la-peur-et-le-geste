// Transport du bureau ; les profils et le plan viennent du paquet de monde.
const fs = require("node:fs");
const path = require("node:path");

function routesBureau(bureau, depot) {
  const repondre = (res, code, objet, type = "application/json; charset=utf-8") => {
    res.writeHead(code, { "Content-Type": type, "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" });
    res.end(type.startsWith("application/json") ? JSON.stringify(objet) : objet);
  };
  return function traiter(req, res) {
    const url = new URL(req.url, "http://localhost");
    if (req.method === "GET") {
      const fichiers = { "/": ["bureau.html", "text/html"], "/bureau": ["bureau.html", "text/html"],
        "/bureau.js": ["bureau.js", "text/javascript"], "/bureau.css": ["bureau.css", "text/css"] };
      if (fichiers[url.pathname]) {
        const [f, type] = fichiers[url.pathname];
        return repondre(res, 200, fs.readFileSync(path.join(depot, "ecrans", f)), type + "; charset=utf-8");
      }
      if (url.pathname === "/api/bureau") {
        const apres = Number(url.searchParams.get("apres") || 0);
        if (!Number.isSafeInteger(apres) || apres < 0) return repondre(res, 400, { erreur: "Curseur invalide" });
        return repondre(res, 200, bureau.etat(apres));
      }
    }
    if (req.method === "POST" && ["/api/bureau/messages", "/api/bureau/transmettre"].includes(url.pathname)) {
      if (req.headers.origin && req.headers.origin !== `http://${req.headers.host}`)
        return repondre(res, 403, { erreur: "Origine refusee" });
      if (!String(req.headers["content-type"]).startsWith("application/json"))
        return repondre(res, 415, { erreur: "JSON requis" });
      let brut = "", taille = 0, refuse = false;
      req.setEncoding("utf8");
      req.on("data", chunk => {
        taille += Buffer.byteLength(chunk);
        if (taille > 20000) { if (!refuse) repondre(res, 413, { erreur: "Message trop long" }); refuse = true; }
        else brut += chunk;
      });
      req.on("end", () => {
        if (refuse) return;
        try {
          const d = JSON.parse(brut);
          const r = url.pathname.endsWith("/transmettre")
            ? bureau.transmettre(req.headers["x-bureau-secret"], req.headers["x-bureau-agent"], d)
            : bureau.deposer({ a: d.a, texte: d.texte, requete_id: d.requete_id });
          repondre(res, 202, r);
        } catch (e) { repondre(res, 400, { erreur: e.message }); }
      });
      return;
    }
    repondre(res, 404, { erreur: "Route inconnue" });
  };
}
module.exports = { routesBureau };
