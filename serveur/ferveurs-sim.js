// Projection seule : aucune avance de simulation à la lecture d'une page.
const fs = require('fs');
const path = require('path');
module.exports = function lireFerveurs(racine, anciennes) {
  try {
    const config = JSON.parse(fs.readFileSync(path.join(racine, 'liaison-ferveurs.json'), 'utf8'));
    const instantane = JSON.parse(fs.readFileSync(config.fichier, 'utf8'));
    if (instantane.version !== 1 || instantane.scenario !== config.scenario || instantane.seed !== config.seed) return anciennes;
    const residents = new Map(instantane.residents.map(r => [r.id, r]));
    const resultat = { ...anciennes };
    // Contacts du deuxième degré : vérifier le nom en plus de l'identifiant.
    try {
      const reseau = JSON.parse(fs.readFileSync(path.join(racine, 'contacts-indirects.json'), 'utf8'));
      for (const p of reseau.personnes || []) {
        const match = /^sim-contact-(\d+)$/.exec(p.id);
        if (!match) continue;
        const r = residents.get(Number(match[1]));
        if (!r || `${r.first} ${r.last}` !== p.nom || !Number.isFinite(r.value) || r.value < 0 || r.value > 100) continue;
        resultat[p.id] = { valeur: r.value, date_source: instantane.date, nature: 'simulation' };
      }
    } catch (e) {}
    for (const [id, lien] of Object.entries(config.personnages)) {
      const r = residents.get(lien.id);
      // Les numéros changent quand la population est régénérée : vérifier l'identité.
      if (!r || r.first !== lien.first || r.last !== lien.last || !Number.isFinite(r.value) || r.value < 0 || r.value > 100) continue;
      resultat[id] = { valeur: r.value, date_source: instantane.date, nature: 'simulation', actualise: instantane.exportedAt };
    }
    return resultat;
  } catch (e) { return anciennes; }
};
