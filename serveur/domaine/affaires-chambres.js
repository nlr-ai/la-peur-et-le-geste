// AFFAIRES-CHAMBRES — ce qu'un siège `voit_affaires` ajoute à ses livres.
//
// Un siège de `joueurs.json` qui porte `voit_affaires: true` voit, en plus de
// sa maison et de sa propre chambre, les cahiers (« Ses volumes ») de toutes
// les autres chambres du monde, sauf celle du MJ, qui n'est pas de la fiction.
// C'est une ouverture voulue du brouillard, siège par siège. Les chambres
// elles-mêmes (manière, brouillons, relations, en souffrance) restent closes.
//
// Mêmes ids que le damier (`scripts/noyau/affaires_chambres.py`) : un plateau
// de l'échiquier ouvre donc le bon volume. Le livre garde les numéros locaux
// du cahier (C.1, V.1…) ; seul le damier les renumérote.

// `sienne` : ce que `coffretsChambre` a déjà rendu pour ce siège.
// `coffretsDe(h)` et `nomDe(h)` viennent de chambre-livres.js.
function ajouter(sienne, moi, habitants, coffretsDe, nomDe) {
  const tout = { books: sienne.books.slice(), boites: sienne.boites.slice() };
  habitants
    .filter((h) => h !== moi && h !== "mj")
    .sort((a, b) => nomDe(a).localeCompare(nomDe(b), "fr"))
    .forEach((h) => {
      const c = coffretsDe(h);
      const boite = "volumes-" + h;
      tout.books.push.apply(tout.books, c.books.filter((b) => b.boite === boite));
      tout.boites.push.apply(tout.boites, c.boites.filter((b) => b.id === boite));
    });
  return tout;
}

module.exports = { ajouter };
