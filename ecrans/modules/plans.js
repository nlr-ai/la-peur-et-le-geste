// plans.js — la porte des plans de château (`window.Plans`), une entrée par lieu.
// Pendant intérieur de geo.js : là où geo.js donne le royaume vu de haut, ceci
// donne la salle où l'on est. Rien n'est généré : un plan est dessiné à la main,
// une fois, et ne bouge plus — un château ne change pas de salles.
//
// CE FICHIER NE CONTIENT PLUS UN SEUL PLAN, ET C'EST LE LOT 3.
// Il en portait 899 lignes : Peyredragon, le Donjon Rouge, le chantier de la
// vase, Barralfond — et, à la dernière ligne, un Braavos FABRIQUÉ au chargement
// de la page par `JSON.stringify(peyredragon).replaceAll("Peyredragon","Braavos")`.
// Une ville entière n'existait que comme un remplacement de texte sur une autre.
// C'était le symptôme le plus net de ce que le plan de refonte appelle « les
// données dans le code » : aucun second monde ne pouvait avoir ses propres
// salles sans qu'on retouche ce fichier-ci.
// Les plans vivent désormais dans le paquet du monde, un fichier par plan
// (`plans/<id>.json`), servis par `serveur/routes/plans.js` dans `window.MONDE`.
// Braavos a été engendré UNE fois, figé dans son fichier, et la ligne a disparu.
//
// LE REPLI EST VIDE, ET C'EST DÉLIBÉRÉ. Un plan à moitié juste — celui d'un
// autre château, ou trois salles gardées ici « au cas où » — est pire que pas de
// plan : le joueur clique une porte qui n'existe pas. Aucun plan servi veut dire
// aucun plan dessiné, et `plan.js` sait déjà ne rien montrer.
//
// Une salle :
//   id, nom          — l'id sert au canal de pensée (clic = on y songe)
//   forme            — {c:[cx,cy,r]} cercle | {r:[x,y,l,h,arrondi]} | {d:"…"} chemin
//   lignes           — le nom coupé pour tenir dans la forme (une ligne = un <text>)
//   etiq             — [x,y] ancre du nom (les lignes descendent de là)
//   quoi             — une ligne au survol : ce que la salle EST
//   etage            — "sommet" | "dessous" : la salle n'est pas de plain-pied.
//                      Un plan est plat ; le pointillé dit qu'on monte ou qu'on
//                      descend pour y aller, et `quoi` dit de combien.
//   dehors           — true : hors les murs (rendu plus pâle)
//   fond             — true : dessinée sous la muraille (la cour)
//   cle              — true : garde son nom dans la vignette étroite du décor.
//                      Les autres n'y sont que des formes (nom au survol) et
//                      retrouvent leur légende sur le plan déplié.
//   alias            — noms à rendre cliquables DANS LE FIL (distinctifs seulement :
//                      « la cour » ou « le quai » piégeraient toute la prose)
//   motifs           — ce qui, dans l'en-tête de lieu du bandeau, désigne cette
//                      salle (« Petite salle du levant, Peyredragon » → salle-levant)
//   _                — la prose du plan : pourquoi il est dessiné ainsi. Ignorée
//                      à l'écran, lue par qui vient le retoucher.
"use strict";
window.Plans = (window.MONDE && window.MONDE.plans) || {};
