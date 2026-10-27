// visage.js — UN HOMME, UN SIGNE, ET LE MÊME PARTOUT.
//
// Le portrait d'un présent était bâti à trois endroits qui ne se parlaient pas :
// la colonne des présents (`galerie.js`), la chronique (`bus.js`), et le
// registre des gens. Chacun rognait, cerclait et posait l'emblème à sa façon —
// si bien que la bordure de l'office, ajoutée dans la salle, manquait dans le
// fil, et que le recadrage qui chasse le fond noir ne valait que pour la salle.
// Deux visages du même homme, à trente centimètres l'un de l'autre.
//
// Ce module est la seule main qui dessine un visage. Il rend une chaîne HTML,
// et non un élément, parce que ses appelants construisent tous des chaînes ;
// tout ce qui doit être retouché sur le SVG (la fenêtre) l'est donc AVANT
// l'insertion, en une passe, sans dépendre du DOM.
//
// Ce qu'un visage porte, et qui vaut partout :
//   • le portrait recadré sur son sujet — pas de fond mort, pas de liseré ;
//   • un anneau à la couleur de son office, la même que sa tache sur le plan ;
//   • l'emblème de cet office dans l'angle, assez grand pour se lire seul ;
//   • et, au survol, LA LOUPE : le visage en grand avec son nom et son titre,
//     parce qu'un portrait de quarante pixels ne se reconnaît pas toujours.
"use strict";
window.Visage = (() => {
  const esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

  // ---- la fenêtre du portrait ---------------------------------------------
  // Les fichiers de `ecrans/portraits/` sont des carrés de 128 avec un disque
  // de fond sombre jusqu'au bord. Cerclé, cela donnait trois bagues au lieu
  // d'une : la bordure, un liseré clair (les coins du carré, que le rond rogne
  // sans les remplir), et le croissant noir du fond qui dépasse du sujet.
  //
  // On resserre la VUE plutôt que de retoucher trente-neuf fichiers. Deux
  // familles, deux cadrages, et les confondre coûterait quelque chose :
  //  • les photos portent une `<image>` posée en 12,12 sur 104 — on cadre
  //    dessus au pixel près, il ne reste rien du fond ;
  //  • les portraits DESSINÉS n'ont pas d'image mais un anneau héraldique à
  //    r=57.5, qui dit au service de qui l'homme est. Lui n'est pas du
  //    remplissage : on coupe le noir mort autour (r 61 à 63), on le garde.
  //
  // Hors de la forme attendue, on ne touche à rien plutôt que de couper au
  // hasard : un portrait bâti autrement garde sa vue d'origine.
  const VUE = /viewBox\s*=\s*(["'])\s*0\s+0\s+128\s+128\s*\1/;
  const IMAGE = /<image\b[^>]*>/i;
  const ATTR = (balise, nom) => {
    const m = new RegExp(nom + '\\s*=\\s*(["\'])([^"\']*)\\1', "i").exec(balise);
    return m ? parseFloat(m[2]) : NaN;
  };

  function cadrer(svg) {
    const s = String(svg || "");
    if (!s || !VUE.test(s)) return s;
    const img = IMAGE.exec(s);
    let vue = "3 3 122 122";
    if (img) {
      const x = ATTR(img[0], "x"), y = ATTR(img[0], "y");
      const w = ATTR(img[0], "width"), h = ATTR(img[0], "height");
      if (!(w > 0 && h > 0)) return s;
      vue = x + " " + y + " " + w + " " + h;
    }
    return s.replace(VUE, 'viewBox="' + vue + '"');
  }

  // ---- la couleur de l'office ---------------------------------------------
  // `Taches.teinte` en décide, et c'est déjà ce qu'on lit sur le plan du
  // château : un visage cerclé de cette couleur-là fait le pont entre la
  // rangée des présents et la tache qu'on vient de voir dans la salle. Sans
  // office reconnu, c'est une grisaille — elle ne prétend aucun rôle.
  function teinte(p) {
    if (!window.Taches || !Taches.teinte) return "";
    return Taches.teinte({ id: p.id, titre: p.titre, office: p.titre });
  }

  function embleme(titre) {
    if (window.Bus && Bus.embleme) return Bus.embleme(titre);
    if (window.Taches && Taches.office) return Taches.office({ titre: titre }) || "";
    return "";
  }

  function prefixe(titre) {
    if (document.documentElement.dataset.habillage !== "lumina-prime") return "";
    const signe = embleme(titre);
    return signe && signe !== "•" ? signe + " " : "";
  }

  // ---- le visage ----------------------------------------------------------
  // `p` : {id, nom, titre, portrait_svg}. `opts.classe` ajoute la classe que
  // l'appelant utilise déjà pour sa mise en place (`med-rond`, `chr-icone`…) :
  // le visage se pose dans SA case sans que celle-ci ait à se réécrire.
  // `opts.corps` remplace le portrait quand il n'y en a pas — le blason d'un
  // récit, par exemple, qui n'a ni office ni anneau à porter.
  // UN AVATAR QUI N'EST PAS UN SVG EST UN GLYPHE. Les annales passent « ⚜ »
  // là où une réplique passe un portrait entier : traité comme un visage, le
  // caractère se retrouvait dans une boîte à `line-height:0`, donc écrasé. On
  // regarde ce qu'on a reçu plutôt que de croire le nom du champ.
  const EST_SVG = /^\s*<svg\b/i;

  function pastilleOpinion(p) {
    const f = window.Gens && Gens.qui ? Gens.qui(p.id) : {};
    if (!p.id || p.joueur || f.joueur) return "";
    const n = f.opinion !== undefined ? f.opinion : p.opinion;
    const connu = typeof n === "number" && Number.isFinite(n);
    const texte = connu ? (n > 0 ? "+" : "") + n : "?";
    const niveau = n < -50 ? 0 : n <= 0 ? 1 : n < 50 ? 2 : 3;
    const libelles = ["Méfiance", "Réserve", "Confiance", "Confiance forte"];
    const titre = connu ? libelles[niveau] + " envers vous — score : " + texte : "Confiance envers vous inconnue";
    const forme = "M12 2L21 6V12C21 17 17 21 12 23C7 21 3 17 3 12V6Z";
    const remplissage = [100, 65, 30, 0][niveau];
    const icone = connu ? '<svg class="opinion-bouclier" viewBox="0 0 24 26" aria-hidden="true">' +
      (niveau > 0 ? '<path class="bouclier-plein" d="' + forme + '" style="clip-path:inset(' + remplissage + '% 0 0 0)"/>' : '') +
      '<path d="' + forme + '"/></svg>' : '?';
    const style = connu ? ' style="background:' + ["#14462b", "#555958", "#94702e", "#c85b12"][niveau] + '"' : "";
    return '<span class="visage-opinion ' + (connu ? n > 0 ? "positive" : n < 0 ? "negative" : "neutre" : "inconnue") +
      '"' + style + ' tabindex="0" data-opinion-details="' + esc([titre].concat(f.opinion_details || p.opinion_details || (connu ? [] : ["Aucune opinion connue pour cette relation."])).join("\n")) + '" aria-label="' + esc(titre) + '">' + icone + '</span>';
  }

  function flammeFerveur(p) {
    if (!p.id) return "";
    const f = window.Gens && Gens.qui ? Gens.qui(p.id) : {};
    const n = f.ferveur !== undefined ? f.ferveur : p.ferveur;
    const connue = typeof n === "number" && Number.isFinite(n) && n >= 0 && n <= 100;
    const niveau = connue ? n < 25 ? 0 : n < 50 ? 1 : n < 75 ? 2 : 3 : -1;
    const couleur = ["vert", "gris", "jaune", "orange"][niveau] || "inconnue";
    const date = f.ferveur_date || p.ferveur_date;
    let titre = connue ? "Ferveur : " + n + "/100 — niveau " + (niveau + 1) + "/4" +
      (date ? " (" + ((f.ferveur_nature || p.ferveur_nature) === "simulation" ? "simulation, dernier état : " : "source : ") + String(date).replace("T", " ") + ")" : "") : "Ferveur inconnue";
    if ((f.ferveur_nature || p.ferveur_nature) === "choix_joueur") titre += "\nDéterminée par vos choix\n" + (f.ferveur_details || p.ferveur_details || []).join("\n");
    return '<span class="visage-ferveur ' + couleur + '" title="' + esc(titre) + '" aria-label="' + esc(titre) +
      '"><svg class="flamme" viewBox="0 0 24 28" aria-hidden="true"><path d="M13 2C15 9 21 10 21 17a9 9 0 0 1-18 0c0-4 2-7 5-10 0 4 1 5 2 6 3-3 4-7 3-11Z"/></svg></span>';
  }

  function actualiserOpinions() {
    document.querySelectorAll(".visage[data-id]:not(.visage-nu)").forEach((el) => {
      const ancien = el.querySelector(".visage-opinion");
      if (ancien) ancien.remove();
      const flamme = el.querySelector(".visage-ferveur");
      if (flamme) flamme.remove();
      el.insertAdjacentHTML("beforeend", pastilleOpinion({id: el.dataset.id}) + flammeFerveur({id: el.dataset.id}));
    });
  }

  function html(p, opts) {
    const o = opts || {};
    const a = p || {};
    const brut = a.portrait_svg || "";
    const nu = o.corps || (brut && !EST_SVG.test(brut) ? brut : "");
    const portrait = nu || cadrer(brut);
    const e = !nu && a.titre ? embleme(a.titre) : "";
    const c = nu ? "" : teinte(a);
    return '<span class="visage' + (o.classe ? " " + o.classe : "") +
      (nu ? " visage-nu" : "") + '"' +
      (c ? ' style="--role:' + esc(c) + '"' : "") +
      ' data-nom="' + esc(a.nom || "") + '"' +
      (a.titre ? ' data-titre="' + esc(a.titre) + '"' : "") +
      (a.id ? ' data-id="' + esc(a.id) + '"' : "") + ">" +
      portrait + (!nu ? pastilleOpinion(a) + flammeFerveur(a) : "") +
      (e ? '<i class="emb-coin" aria-hidden="true">' + e + "</i>" : "") +
      "</span>";
  }

  // ---- la fiche au survol -------------------------------------------------
  // CE N'EST PAS UNE LOUPE, ET C'EST LE PLAN QUI L'A MONTRÉ. Née pour agrandir
  // un portrait trop petit, elle sert d'abord à DIRE QUI C'EST — et sur la
  // carte du château, où un homme n'est qu'une tache d'encre à deux lettres,
  // il n'y a rien à agrandir : il faut aller chercher son visage au registre.
  // Le même geste, deux sources, une seule fiche.
  //
  // POURQUOI UNE COPIE FLOTTANTE ET NON UN `scale()`. Le visage vit dans des
  // conteneurs qui défilent — la colonne des présents, la chronique — et tout
  // ce qui grandit sur place y est coupé par le bord du cadre. Une copie en
  // `position:fixed`, hors de tout parent, échappe seule à ce rognage. Sur la
  // carte, la question ne se pose même pas : il n'y a pas de copie à faire.
  //
  // Elle ne prend jamais le clic : c'est un renseignement, pas un bouton, et
  // le clic appartient à ce qu'on survole (parler à cet homme, ou ouvrir sa
  // salle). Elle porte le nom et le titre — c'est ce que l'emblème d'angle a
  // chassé de sous le visage, et ce qu'une tache ne dit pas du tout.
  const FOIS = 4;
  const COTE_CARTE = 240;          // px : la fiche d'une tache, qui n'a pas de
                                   // taille propre à multiplier
  // Deux bornes, et elles servent des cas opposés. Un PLANCHER, parce que le
  // multiplicateur seul laissait les petits médaillons de la salle (58px) à
  // 232px, c'est-à-dire moins que le visage du fil au repos : on ne survole
  // pas pour obtenir plus petit. Un PLAFOND, parce que le visage du fil fait
  // maintenant 124px et que quatre fois cela sortirait de l'écran sur un
  // portable — la fiche est un agrandissement, pas un rideau sur la page.
  const PLANCHER = 320;
  function borner(cote) {
    const plafond = Math.round(
      Math.min(window.innerWidth, window.innerHeight) * 0.56);
    return Math.min(Math.max(cote, Math.min(PLANCHER, plafond)), plafond);
  }
  let boite = null, cible = null;

  function fermer() {
    if (boite) boite.classList.remove("ouverte");
    cible = null;
  }

  // Ce qu'on montre, d'où que vienne le survol : un visage déjà dessiné qu'on
  // recopie en grand, ou un homme du registre qu'on dessine pour l'occasion.
  function fiche(src) {
    if (src.classList.contains("visage")) {
      const r = src.getBoundingClientRect();
      return { cote: borner(Math.round(Math.max(r.width, r.height) * FOIS)),
               role: src.style.getPropertyValue("--role"),
               dedans: src.innerHTML,
               nom: src.dataset.nom || "", titre: src.dataset.titre || "" };
    }
    // une tache de carte : elle n'a que son id, le registre a le reste
    const id = src.dataset.id || "";
    const f = (window.Gens && Gens.qui) ? (Gens.qui(id) || {}) : {};
    const p = { id: id, nom: f.nom || src.dataset.nom || id,
                titre: f.titre || "", portrait_svg: f.portrait_svg || "" };
    if (!p.portrait_svg) return null;   // sans visage, la fiche n'apprend rien
    return { cote: borner(COTE_CARTE), role: teinte(p),
             dedans: cadrer(p.portrait_svg) +
               (p.titre ? '<i class="emb-coin" aria-hidden="true">' +
                 embleme(p.titre) + "</i>" : ""),
             nom: p.nom, titre: p.titre };
  }

  function ouvrir(src) {
    if (src === cible) return;
    const f = fiche(src);
    if (!f) { fermer(); return; }
    cible = src;
    // Une bulle à la fois : l'encart du plateau se pose au même endroit, et
    // deux fiches superposées ne se lisent ni l'une ni l'autre. Vaut même pour
    // une bulle retenue — elle est de toute façon recouverte.
    if (window.Echiquier && Echiquier.fermer) Echiquier.fermer();
    if (!boite) {
      boite = document.createElement("div");
      boite.className = "visage-fiche";
      document.body.appendChild(boite);
    }
    boite.classList.remove("opinion-fiche");
    boite.innerHTML =
      '<span class="visage visage-grand" style="' +
      (f.role ? "--role:" + esc(f.role) + ";" : "") +
      "width:" + f.cote + "px;height:" + f.cote + 'px">' + f.dedans + "</span>" +
      (f.nom ? '<span class="visage-fiche-nom">' + esc(f.nom) +
        (f.titre ? "<small>" + esc(f.titre) + "</small>" : "") + "</span>" : "");
    // On se pose à côté, du côté où il y a la place, et l'on reste dans
    // l'écran : un visage tout en bas de la colonne — ou une tache dans le coin
    // du plan — ne doit pas sortir du cadre pour être vu.
    const r = src.getBoundingClientRect();
    const marge = 12;
    boite.classList.add("ouverte");
    const b = boite.getBoundingClientRect();
    let x = r.right + marge;
    if (x + b.width > window.innerWidth - marge) x = r.left - marge - b.width;
    if (x < marge) x = marge;
    let y = r.top + r.height / 2 - b.height / 2;
    y = Math.max(marge, Math.min(y, window.innerHeight - marge - b.height));
    boite.style.left = Math.round(x) + "px";
    boite.style.top = Math.round(y) + "px";
  }

  // `.tache-gens` : un homme sur une carte — le plan du château, la ville, le
  // champ. Tous passent par `taches.js`, donc un seul sélecteur les couvre.
  const SOURCES = ".visage,.tache-gens[data-id]";

  function ouvrirOpinion(src) {
    fermer();
    if (!boite) {
      boite = document.createElement("div");
      boite.className = "visage-fiche";
      document.body.appendChild(boite);
    }
    boite.id = "opinion-infobulle";
    boite.setAttribute("role", "tooltip");
    src.setAttribute("aria-describedby", boite.id);
    boite.classList.add("opinion-fiche", "ouverte");
    boite.textContent = src.dataset.opinionDetails;
    const r = src.getBoundingClientRect(), b = boite.getBoundingClientRect();
    boite.style.left = Math.max(12, Math.min(r.right + 12, innerWidth - b.width - 12)) + "px";
    boite.style.top = Math.max(12, Math.min(r.top, innerHeight - b.height - 12)) + "px";
  }

  document.addEventListener("mouseover", (ev) => {
    if (!ev.target.closest) return;
    const opinion = ev.target.closest(".visage-opinion");
    if (opinion) { ouvrirOpinion(opinion); return; }
    const src = ev.target.closest(SOURCES);
    if (src && !src.classList.contains("visage-nu") && !ev.target.closest(".visage-fiche")) {
      ouvrir(src);
    } else if (!ev.target.closest(".visage-fiche")) {
      fermer();
    }
  });
  document.addEventListener("focusin", (ev) => {
    if (ev.target.matches(".visage-opinion")) ouvrirOpinion(ev.target);
  });
  document.addEventListener("focusout", (ev) => {
    if (ev.target.matches(".visage-opinion")) fermer();
  });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") fermer(); });
  // Le survol ne suffit pas : on quitte un visage en défilant, en cliquant, en
  // faisant glisser la carte ou en changeant d'onglet — et la fiche resterait
  // pendue à l'écran.
  ["scroll", "mousedown", "blur", "wheel"].forEach((t) =>
    window.addEventListener(t, fermer, true));

  return { html, actualiserOpinions, cadrer, teinte, embleme, prefixe, fermer };
})();
