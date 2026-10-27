// Identité de naissance vérifiée par la même autorité que le runtime Python.
// Un seul relevé partagé entre les onglets, sans bloquer le serveur HTTP.
const { execFile } = require("child_process");
const path = require("path");
const { DEPOT, RACINE } = require("../http");
let releve = null, jusqua = 0;
function lire() {
  if (releve && Date.now() < jusqua) return releve;
  jusqua = Infinity;
  releve = new Promise((resolve, reject) => {
    execFile(process.env.PYTHON || "python", [path.join(DEPOT, "scripts", "activite_runtime.py")],
      { timeout: 5000, windowsHide: true }, (err, stdout) => {
        jusqua = Date.now() + 1000;
        if (err) { releve = null; reject(err); return; }
        try { resolve(JSON.parse(stdout).actifs || []); }
        catch (e) { releve = null; reject(e); }
      });
  });
  return releve;
}
async function activiteMj(siege) {
  if (!siege || !siege.personnage_id) return { actif: false };
  const normaliser = p => process.platform === "win32" ? path.resolve(p).toLowerCase() : path.resolve(p);
  const actifs = await lire();
  return { actif: actifs.some(d => d.homme === "mj"
    && d.racine && normaliser(d.racine) === normaliser(RACINE)
    && (d.monde || "") === (process.env.CONSEIL_MONDE || "")
    && Array.isArray(d.pour) && d.pour.includes(siege.personnage_id)) };
}
module.exports = { activiteMj };
