// blasons.js — DESSINER une bannière. Qui porte quoi vient du monde.
// Sur la table peinte, une bannière fait douze pixels de haut : un lion rampant
// y serait une tache. On garde donc ce qu'une bannière dit vraiment à cette
// distance — ses ÉMAUX et sa partition — et la charge y est ramenée à deux ou
// trois traits épais, qui deviennent une bête à mesure qu'on approche.
//
// CE FICHIER NE NOMME PLUS AUCUNE MAISON, ET C'EST LE LOT 3.
// Il portait dix-neuf entrées d'armes (« maison-targaryen-noir », « maison-stark »)
// et seize tracés de charges (le dragon, l'hippocampe, le loup) : un monde sans
// dragons ne pouvait pas exister sans qu'on retouche ce fichier-ci. Les trois
// tables — les émaux, les armes, les charges — vivent maintenant dans le paquet
// du monde (`blasons/armes.json`, `blasons/charges.json`), servies par
// `serveur/routes/plans.js` dans `window.MONDE`. Ce qui reste ici est du DESSIN
// et rien d'autre : la toile, les partitions, la hampe, le semé — ce qu'on
// saurait faire pour n'importe quelles armes de n'importe quel monde.
//
// LE REPLI EST VIDE. Des armes à moitié justes — le champ d'une maison sur la
// place d'une autre — mentent sur qui tient la place, et c'est la seule chose
// que cette bannière ait à dire. Rien de servi : `banniere()` rend "" et la
// place garde son point et son nom, exactement comme pour une maison qu'on n'a
// jamais dessinée.
//
// La source de FICTION reste `blason` dans etat/maisons.json, une description
// héraldique en toutes lettres ; les fichiers du monde disent comment la tracer.
"use strict";
window.Blasons = (() => {
  const D = (window.MONDE && window.MONDE.blasons) || {};
  // Les émaux, tenus bas en saturation : ce sont des teintures sur toile, pas
  // des écrans. Ils doivent tenir sur le parchemin sans le trouer.
  const E = D.emaux || {};
  const ARMES = D.armes || {};
  const CHARGES = D.charges || {};

  // Les armes sont écrites avec le NOM de l'émail (« nuit », « gueules ») et non
  // sa teinte : c'est le seul mot qui dise ce que c'est, et l'ancienne table le
  // perdait — `champ: [E.nuit]` se sérialisait en `["#1b1613"]`. On résout ici,
  // au dernier moment. Un nom inconnu passe tel quel : un monde a le droit
  // d'écrire une couleur en clair sans déclarer d'émail pour elle.
  const teint = (nom) => E[nom] || nom;

  // La toile. Rectangulaire, sans queue d'aronde : l'échancrure demanderait de
  // découper le champ, donc un clipPath, donc un identifiant unique par carte —
  // et à douze pixels, personne ne verra jamais la différence.
  const L = 4.6, HAUT = -5.4, BAS = 3.4;

  // Le champ, selon la partition. Tout est découpé à la main : une bannière de
  // douze pixels ne supporte ni motif ni dégradé.
  function toile(a) {
    const c = (a.champ || []).map(teint), p = a.partition || "plain";
    const rect = (x, w, f) => '<rect x="' + x + '" y="' + HAUT + '" width="' + w +
      '" height="' + (BAS - HAUT) + '" fill="' + f + '"/>';
    if (p === "pal3") {
      return rect(-L, L * 2 / 3, c[0]) + rect(-L / 3, L * 2 / 3, c[1]) + rect(L / 3, L * 2 / 3, c[2]);
    }
    if (p === "pal2") return rect(-L, L, c[0]) + rect(0, L, c[1]);
    if (p === "ecartele") {
      const h = (BAS - HAUT) / 2;
      return '<rect x="' + -L + '" y="' + HAUT + '" width="' + L + '" height="' + h + '" fill="' + c[0] + '"/>' +
        '<rect x="0" y="' + HAUT + '" width="' + L + '" height="' + h + '" fill="' + (c[1] || c[0]) + '"/>' +
        '<rect x="' + -L + '" y="' + (HAUT + h) + '" width="' + L + '" height="' + h + '" fill="' + (c[1] || c[0]) + '"/>' +
        '<rect x="0" y="' + (HAUT + h) + '" width="' + L + '" height="' + h + '" fill="' + c[0] + '"/>';
    }
    let s = rect(-L, L * 2, c[0]);
    if (p === "fusele") {           // fuselé : quelques losanges suffisent à le dire
      const d = [];
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 2; j++) {
          const x = -L + 1.5 + i * 3, y = HAUT + 2.2 + j * 4.4;
          d.push("M" + x + " " + (y - 2.1) + "l1.5 2.1-1.5 2.1-1.5-2.1z");
        }
      }
      s += '<path d="' + d.join("") + '" fill="' + c[1] + '"/>';
    }
    if (p === "hermine") {          // hermine : trois mouchetures et l'œil comprend
      s += '<path d="M-2.4-3.2v1.4M0-.6v1.4M2.4-3.2v1.4M-1.2 2v1.4" stroke="' + teint("sable") +
        '" stroke-width=".8" fill="none" stroke-linecap="round" opacity=".75"/>';
    }
    return s;
  }

  function armesDe(id) { return ARMES[id] || null; }
  // Une charge est `{_: "…", trace: "<path…>"}` : la prose voyage avec le tracé,
  // parce qu'un tracé de deux traits est illisible sans elle.
  const traceDe = (nom) => (CHARGES[nom] || {}).trace || "";

  // Une bannière, dessinée dans sa boîte locale puis posée par un transform.
  // L'échelle voulue par l'appelant est posée par lui, sur le groupe rendu.
  function banniere(maisonId) {
    const a = armesDe(maisonId);
    if (!a) return "";
    const semee = a.partition === "seme" && a.charge;
    let s = '<g class="banniere">';
    // la hampe, plantée dans la place
    s += '<path class="hampe" d="M' + (-L - .9) + " " + (HAUT - 1.4) + "V" + (BAS + 3.6) + '"/>';
    s += '<g class="toile">' + toile(a) +
      '<rect class="pli" x="' + -L + '" y="' + HAUT + '" width="' + (L * 2) +
      '" height="' + (BAS - HAUT) + '"/></g>';
    if (a.bordure) {
      s += '<rect class="bordure" x="' + -L + '" y="' + HAUT + '" width="' + (L * 2) +
        '" height="' + (BAS - HAUT) + '" fill="none" stroke="' + teint(a.bordure) + '" stroke-width="1.1"/>';
    }
    if (a.charge && traceDe(a.charge)) {
      const email = teint(a.email);
      const g = '<g class="charge" fill="' + email + '" stroke="' + email +
        '" stroke-width="1.05">' + traceDe(a.charge) + "</g>";
      if (semee) {
        // semé : la même charge répétée petit, trois fois vaut « partout »
        s += '<g transform="translate(-2,-3) scale(.42)">' + g + "</g>" +
          '<g transform="translate(2.1,-.4) scale(.42)">' + g + "</g>" +
          '<g transform="translate(-1.6,2) scale(.42)">' + g + "</g>";
      } else s += g;
    }
    return s + "</g>";
  }

  // La teinture dominante d'une maison — pour un liseré, une pastille, un rappel.
  function teinte(maisonId) {
    const a = armesDe(maisonId);
    return a && a.champ && a.champ.length ? teint(a.champ[0]) : null;
  }

  const decrit = (maisonId) => (armesDe(maisonId) || {}).note || "";

  return { banniere, teinte, armes: armesDe, decrit, LARGEUR: L * 2, HAUT, BAS, E };
})();
