// connus.js — qui un siège peut connaître, pour un monde qui le demande.
//
// « Les gens » sert ce que la cour sait de la cour. À Westeros, la cour sait
// tout le monde : un grand nom est public. Ailleurs, non — une sorcière ne
// connaît pas le nom du chasseur que les Enfers ont lâché sur son amant, ni
// même qu'il existe. Un monde le déclare dans son manifeste :
//
//   "gens": { "brouillard": true }
//
// et le registre ne sert alors à un siège que :
//   - lui-même et les gens de sa maison ;
//   - ceux de son entourage déclaré (`pnj` de son entrée de joueurs.json) ;
//   - ceux sur qui il a une relation à lui (de = siège) — on sait de qui l'on pense ;
//   - ceux qui ont une relation vers lui que le joueur connaît (connue_du_joueur).
// Sans déclaration, rien ne change : tout le monde est servi, comme avant.
"use strict";

function filtreConnus(manifeste, siegeId, lire) {
  if (!manifeste || !manifeste.gens || !manifeste.gens.brouillard || !siegeId) return null;
  const connus = new Set([siegeId]);
  let persos = [], relations = [], joueurs = [];
  try { persos = lire("personnages.json"); } catch (e) {}
  try { relations = lire("relations.json"); } catch (e) {}
  try { joueurs = lire("joueurs.json"); } catch (e) {}
  const moi = persos.find((p) => p.id === siegeId);
  if (moi && moi.maison_id) persos.forEach((p) => { if (p.maison_id === moi.maison_id) connus.add(p.id); });
  const siege = joueurs.find((j) => j.personnage_id === siegeId);
  ((siege && siege.pnj) || []).forEach((id) => connus.add(id));
  relations.forEach((r) => {
    const de = r.de || r.source_id, vers = r.vers || r.cible_id;
    if (de === siegeId) connus.add(vers);
    else if (vers === siegeId && r.connue_du_joueur) connus.add(de);
  });
  return (p) => connus.has(p.id);
}

module.exports = { filtreConnus };
