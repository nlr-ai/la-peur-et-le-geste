// Commenter une pièce : sa main vient de son cahier source, pas du plateau
// qui l'affiche (une dépendance peut traverser plusieurs affaires).
function annoter(affaires, groupes, gens, joueurs) {
  const sources = new Map();
  for (const g of groupes) for (const numero of g.ecrites) {
    if (!sources.has(numero)) sources.set(numero, []);
    sources.get(numero).push(g.volume);
  }
  for (const affaire of affaires) for (const p of affaire.pieces) {
    const volumes = sources.get(String(p.numero)) || [];
    if (volumes.length !== 1) continue;
    const v = volumes[0];
    const main = gens.find(g => g.id === v.tenu_par);
    if (!main || joueurs.includes(main.id)) continue;
    p.commentaire = { destinataire_id: main.id, nom: main.nom,
      livre_id: v.id, titre: v.titre };
  }
}

function preparer(plateau, demande, livres) {
  const texte = typeof demande.texte === "string" ? demande.texte.trim() : "";
  if (!texte || texte.length > 12000) throw new Error("Écrivez un commentaire de 1 à 12 000 caractères.");
  const affaire = plateau.affaires.find(a => a.id === demande.affaire_id);
  const piece = affaire && (affaire.pieces || []).find(p => p.cle === demande.node_id);
  if (!piece || !piece.commentaire) throw new Error("Ce nœud n’a pas de main PNJ disponible.");
  const numero = String(piece.numero);
  if (!/^\d{4,6}$/.test(numero)) throw new Error("Ce nœud n’a pas d’adresse d’affaire.");
  const source = livres.find(v => v.id === piece.commentaire.livre_id);
  const lignes = [];
  for (const table of (source && source.tables) || []) {
    for (const ligne of table.lignes || []) {
      const cellules = Array.isArray(ligne) ? ligne : ligne.cellules;
      if (!cellules || String(cellules[0]).replace(/[*\s]/g, "") !== numero) continue;
      lignes.push("Table : " + table.titre);
      cellules.forEach((valeur, i) => lignes.push((table.colonnes[i] || "N°") + " : " + valeur));
    }
  }
  if (!lignes.length) throw new Error("La ligne source de ce nœud est introuvable.");
  return { type: "commentaire", mode: "commenter", texte,
    destinataire_id: piece.commentaire.destinataire_id, contexte_id: numero,
    affaire_id: affaire.id, node_id: piece.cle,
    contexte_noeud: "Commentaire sur #" + numero + " — " + piece.nom +
      "\nCahier : " + source.titre + " (" + source.id + ")\n" + lignes.join("\n") };
}

module.exports = { annoter, preparer };
