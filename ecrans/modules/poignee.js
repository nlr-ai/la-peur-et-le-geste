// poignee.js — le séparateur entre la chronique et le décor, qu'on déplace.
//
// La page est une grille de quatre colonnes : le rail des récents, LES
// PRÉSENTS, LA CHRONIQUE, LE DÉCOR. La dernière était figée — trop étroite dès
// qu'on ouvre le conseil de guerre ou l'échiquier, trop large pour une scène de
// dialogue où seul le fil compte. Cette largeur appartient donc au lecteur : il
// tire le trait où il veut, et on s'en souvient.
//
// ATTENTION en touchant à la grille : douze règles de jeu.css déclarent
// `body{grid-template-columns}` et SEULE LA DERNIÈRE compte. Modifier une des
// onze autres ne fait rien du tout — c'est arrivé en écrivant ce module.
//
// Ce qui bouge est une VARIABLE, `--decor`, lue par `grid-template-columns`
// dans jeu.css ; la poignée elle-même est `position:fixed` et ne prend aucune
// place dans la grille — sans quoi la déplacer changerait ce qu'elle mesure.
//
// Regarder n'est pas agir : rien ici n'entre dans l'état, ne coûte une minute,
// ni ne part au serveur. La largeur vit dans `localStorage`, par navigateur.
"use strict";
window.Poignee = (() => {
  // Clé renouvelée pour le défaut du fil à un tiers : les
  // largeurs gardées sous l'ancien défaut ne masquent pas le nouveau.
  const CLE = "conseil-largeur-decor-43-v1";
  const MIN = 360;                       // en deçà, la table peinte ne montre plus rien
  const FIL = 1.3 / 3;                   // un tiers élargi de 30 %
  let DEFAUT = 560;                      // recalculé au chargement par `aFil()`
  const marge = () => Math.max(MIN, Math.round(window.innerWidth * 0.28));
  const disponible = () => window.innerWidth -
    (document.getElementById("fil")?.getBoundingClientRect().left || 142);
  const max = () => Math.max(MIN, disponible() - 280);

  let el = null;

  const borner = (px) => Math.max(MIN, Math.min(max(), Math.round(px)));

  function poser(px, garder) {
    const v = borner(px);
    document.documentElement.style.setProperty("--decor", v + "px");
    if (el) el.style.right = v + "px";
    if (garder) { try { localStorage.setItem(CLE, String(v)); } catch (e) {} }
    // Les échelles qui dessinent sur mesure (la table peinte, le plan, le
    // damier) se calculent sur la place qu'on leur donne : sans ce rappel,
    // elles gardent le cadrage de l'ancienne largeur jusqu'au prochain
    // changement de vue.
    window.dispatchEvent(new Event("resize"));
  }

  // Le décor qui laisse au fil exactement FIL de la fenêtre : on mesure le
  // fil tel qu'il est, et l'on reporte l'écart sur le décor — le rail et les
  // présents ont leur propre largeur, qu'on ne veut pas recompter ici.
  function aFil() {
    if (window.innerWidth <= 1100) return DEFAUT;
    return borner(disponible() * (1 - FIL));
  }

  function lue() {
    try {
      const v = parseInt(localStorage.getItem(CLE) || "", 10);
      if (v > 0) return v;
    } catch (e) {}
    return DEFAUT;
  }

  function tirer(e) {
    e.preventDefault();
    const bouger = (ev) => {
      const x = (ev.touches ? ev.touches[0].clientX : ev.clientX);
      poser(window.innerWidth - x, false);
    };
    const lacher = (ev) => {
      document.removeEventListener("mousemove", bouger);
      document.removeEventListener("touchmove", bouger);
      document.removeEventListener("mouseup", lacher);
      document.removeEventListener("touchend", lacher);
      document.body.classList.remove("tire");
      const x = (ev.changedTouches ? ev.changedTouches[0].clientX : ev.clientX);
      poser(window.innerWidth - x, true);
    };
    document.body.classList.add("tire");
    document.addEventListener("mousemove", bouger);
    document.addEventListener("touchmove", bouger, { passive: false });
    document.addEventListener("mouseup", lacher);
    document.addEventListener("touchend", lacher);
  }

  function construire() {
    el = document.createElement("div");
    el.id = "poignee";
    el.setAttribute("role", "separator");
    el.setAttribute("aria-orientation", "vertical");
    el.setAttribute("aria-label", "Largeur du décor — tirez, ou les flèches");
    el.tabIndex = 0;
    el.title = "Glissez pour redimensionner · double-clic : rétablir 43 % à gauche";
    el.addEventListener("mousedown", tirer);
    el.addEventListener("touchstart", tirer, { passive: false });
    el.addEventListener("dblclick", () => poser(DEFAUT = aFil(), true));
    // Au clavier : les flèches, pas de souris exigée.
    el.addEventListener("keydown", (e) => {
      const pas = e.shiftKey ? 60 : 16;
      const w = parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue("--decor"), 10) || DEFAUT;
      if (e.key === "ArrowLeft") { poser(w + pas, true); e.preventDefault(); }
      if (e.key === "ArrowRight") { poser(w - pas, true); e.preventDefault(); }
      if (e.key === "Home") { poser(DEFAUT = aFil(), true); e.preventDefault(); }
    });
    document.body.appendChild(el);
  }

  window.addEventListener("DOMContentLoaded", () => {
    construire();
    poser(lue(), false);
    // Rien de gardé : le défaut se mesure une fois la grille posée.
    let garde = null;
    try { garde = localStorage.getItem(CLE); } catch (e) {}
    // Le rail et les présents se remplissent après coup : on observe le fil
    // lui-même et on le ramène à FIL tant que le lecteur n'a rien tiré.
    if (!garde && window.ResizeObserver) {
      const ro = new ResizeObserver(() => {
        let g = null;
        try { g = localStorage.getItem(CLE); } catch (e) {}
        if (g) { ro.disconnect(); return; }
        const v = aFil(), w = Poignee.largeur();
        if (Math.abs(v - w) > 1) poser(DEFAUT = v, false);
      });
      // le fil peut naître après ce module : on l'attend quelques images
      let essais = 300;
      const suivre = () => {
        const fil = document.getElementById("fil");
        if (fil) ro.observe(fil);
        else if (essais-- > 0) requestAnimationFrame(suivre);
      };
      suivre();
    }
    // et une mesure franche une fois la page chargée (un onglet caché ne
    // rend aucune image : ni rAF ni ResizeObserver n'y battent)
    const remesurer = () => {
      let g = null;
      try { g = localStorage.getItem(CLE); } catch (e) {}
      if (g) return;
      const v = aFil();
      if (Math.abs(v - Poignee.largeur()) > 1) poser(DEFAUT = v, false);
    };
    if (!garde) window.addEventListener("load", () => setTimeout(remesurer, 50));
    // la colonne des présents naît vide et se peuple : c'est elle qui mange
    // le fil quand elle paraît, et une mutation se voit même onglet caché
    const act = document.getElementById("acteurs");
    if (!garde && act && window.MutationObserver)
      new MutationObserver(() => setTimeout(remesurer, 0))
        .observe(act, { childList: true, attributes: true, attributeFilter: ["class", "style"] });
  });
  // La fenêtre rétrécit : la largeur gardée peut devenir plus grande que la
  // moitié de l'écran. On la reborne sans l'oublier — elle revient telle
  // quelle quand la place revient.
  window.addEventListener("resize", () => {
    const w = parseInt(getComputedStyle(document.documentElement)
      .getPropertyValue("--decor"), 10) || DEFAUT;
    let garde = null;
    try { garde = localStorage.getItem(CLE); } catch (e) {}
    // sans largeur gardée, le fil reste à FIL de la fenêtre qui change
    const v = garde ? borner(w) : aFil();
    if (Math.abs(v - w) > 1) {
      document.documentElement.style.setProperty("--decor", v + "px");
      if (el) el.style.right = v + "px";
    }
  });

  return { poser, largeur: () => parseInt(getComputedStyle(document.documentElement)
    .getPropertyValue("--decor"), 10) || DEFAUT, marge };
})();
