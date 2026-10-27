// Relais techniques opt-in : même contrat que scripts/noyau/scenes_partagees.py.
function audience(joueur, config, registre, presence, horloges) {
  if (!config || !config.active) return null; // comportement hérité
  const scene = (registre.communes || []).find(c => c.membres.includes(joueur));
  if (!scene) return joueur;
  const date = horloges[joueur];
  const egale = d => date && d && ["annee", "lune", "jour", "minute"]
    .every(k => date[k] === d[k]);
  const compatible = scene.membres.every(m => egale(horloges[m])
    && presence[m] && presence[m].salle === scene.salle);
  return compatible ? scene.membres.slice().sort() : joueur;
}
module.exports = { audience };
