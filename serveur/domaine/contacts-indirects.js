"use strict";
// Projection à deux liens dirigés. Aucune découverte n'est écrite dans l'état.
function projeter(joueur, directs, relations, personnes, liens, regle = {}) {
  const seuil = regle.seuil_confiance ?? 40;
  const seuilCombine = regle.seuil_combine ?? 25;
  const confiance = new Map();
  for (const r of liens) if (Number.isFinite(r.confiance)) confiance.set(r.source_id + "|" + r.cible_id, r.confiance);
  // Les opinions courantes priment sur l'instantané importé.
  for (const r of relations) {
    const a = r.source_id || r.de, b = r.cible_id || r.vers;
    if (Number.isFinite(r.opinion)) confiance.set(a + "|" + b, Math.max(0, Math.min(100, (r.opinion + 100) / 2)));
  }
  const resultat = new Map();
  for (const id of directs) {
    if (id === joueur) continue;
    const versJoueur = confiance.get(id + "|" + joueur);
    if (!Number.isFinite(versJoueur) || versJoueur < seuil) continue;
    const contacts = [];
    for (const [cible, p] of personnes) {
      if (cible === id || directs.has(cible) || cible === joueur || p.etat === "mort") continue;
      const versCible = confiance.get(id + "|" + cible);
      if (!Number.isFinite(versCible) || versCible < seuil) continue;
      const score = versJoueur * versCible / 100;
      if (score < seuilCombine) continue;
      contacts.push({ id: cible, nom: p.nom, titre: p.titre || "", score: Math.round(score),
        confiance_joueur: versJoueur, confiance_cible: versCible });
    }
    contacts.sort((a,b) => b.score-a.score || a.nom.localeCompare(b.nom, "fr"));
    if (contacts.length) resultat.set(id, contacts);
  }
  return resultat;
}
module.exports = { projeter };
