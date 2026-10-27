// fiche.js — la page de son propre personnage. Un clic sur SON nom (dans le
// fil ou dans « Les gens ») ouvre ce qu'il a sous la main — lieux, matériel,
// fournitures, argent, travail en cours — et qui il connaît, un mot sur
// chacun. La matière est écrite dans `etat/joueurs/<siège>/fiche.json` et
// servie par GET /fiche, qui ne rend jamais que la fiche du siège qui demande.
// Aucun chiffre de jeu n'y paraît : ce sont ses souvenirs, pas un tableau.
// Sans fiche écrite, le clic retombe sur la question au narrateur.
"use strict";
window.Fiche = (() => {
  const esc = (s) => String(s == null ? "" : s)
    .replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function styler() {
    if (document.getElementById("fiche-style")) return;
    const st = document.createElement("style");
    st.id = "fiche-style";
    st.textContent = [
      "#fiche-voile{position:fixed;inset:0;z-index:900;background:rgba(30,22,14,.45);",
      "  display:flex;justify-content:center;align-items:flex-start;overflow:auto;padding:4vh 16px}",
      "#fiche{background:var(--fond);color:var(--ink);max-width:760px;width:100%;",
      "  border:1px solid var(--bord);border-radius:6px;padding:1.4rem 1.6rem 2rem;",
      "  box-shadow:0 10px 40px rgba(0,0,0,.3);position:relative}",
      "#fiche h2{margin:0;font-weight:normal;font-size:1.6rem}",
      "#fiche .fi-sous{color:var(--muted);font-size:.85rem;margin:.2rem 0 1rem}",
      "#fiche .fi-pres{line-height:1.6;margin:0 0 1.2rem}",
      "#fiche h3{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;",
      "  color:var(--accent);font-weight:normal;margin:1.6rem 0 .6rem;",
      "  border-bottom:1px solid var(--bord);padding-bottom:.3rem}",
      "#fiche h4{font-size:.85rem;margin:1rem 0 .4rem;color:var(--muted);font-weight:normal;font-style:italic}",
      "#fiche .fi-res{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.5rem}",
      "#fiche .fi-item{background:var(--paper);border:1px solid var(--bord);border-radius:4px;padding:.5rem .65rem}",
      "#fiche .fi-item b{display:block;font-size:.9rem;margin-bottom:.15rem}",
      "#fiche .fi-item span{font-size:.8rem;color:var(--muted);line-height:1.45}",
      "#fiche .fi-gens{display:flex;flex-direction:column;gap:.45rem}",
      "#fiche .fi-pnj{display:flex;gap:.7rem;align-items:flex-start;padding:.4rem 0;",
      "  border-bottom:1px dashed var(--bord)}",
      "#fiche .fi-rond{flex:0 0 40px;width:40px;height:40px;border-radius:50%;overflow:hidden;",
      "  background:var(--paper)}",
      "#fiche .fi-rond svg{width:100%;height:100%}",
      "#fiche .fi-pnj b{font-size:.92rem}",
      "#fiche .fi-qual{font-size:.75rem;color:var(--muted)}",
      "#fiche .fi-pnj p{margin:.15rem 0 0;font-size:.84rem;line-height:1.45}",
      "#fiche .fi-fermer{position:absolute;top:.6rem;right:.8rem;background:var(--btn);",
      "  border:1px solid var(--bord);border-radius:4px;color:var(--ink);cursor:pointer;",
      "  font:inherit;padding:.2rem .6rem}",
      "#fiche .fi-fermer:hover{background:var(--btn-hover)}",
    ].join("\n");
    document.head.appendChild(st);
  }

  function fermer() {
    const v = document.getElementById("fiche-voile");
    if (v) v.remove();
  }

  function age(g) {
    return g.age ? g.age + " ans" : "";
  }

  function peindre(f) {
    styler();
    fermer();
    const h = [];
    h.push('<button class="fi-fermer" title="Fermer (Échap)">Fermer</button>');
    h.push("<h2>" + esc(f.nom) + "</h2>");
    h.push('<div class="fi-sous">' + esc(f.sous_titre || "") +
      (f.au ? " — au " + esc(f.au) : "") + "</div>");
    if (f.presentation) h.push('<p class="fi-pres">' + esc(f.presentation) + "</p>");

    h.push("<h3>Ce que tu as à ta disposition</h3>");
    (f.ressources || []).forEach((g) => {
      h.push("<h4>" + esc(g.groupe) + "</h4><div class=\"fi-res\">");
      (g.items || []).forEach((it) => {
        h.push('<div class="fi-item"><b>' + esc(it.nom) + "</b><span>" + esc(it.detail || "") + "</span></div>");
      });
      h.push("</div>");
    });

    const tous = (f.contacts || []).reduce((n, c) => n + (c.gens || []).length, 0);
    h.push("<h3>Les gens que tu connais" + (tous ? " (" + tous + ")" : "") + "</h3>");
    (f.contacts || []).forEach((c) => {
      h.push("<h4>" + esc(c.cercle) + "</h4><div class=\"fi-gens\">");
      (c.gens || []).forEach((g) => {
        const qual = [g.metier, age(g), g.lien].filter(Boolean).map(esc).join(" · ");
        h.push('<div class="fi-pnj"><div class="fi-rond">' + (g.portrait_svg || "") + "</div><div>" +
          "<b>" + esc(g.nom) + '</b> <span class="fi-qual">' + qual + "</span>" +
          "<p>" + esc(g.presentation || "") + "</p></div></div>");
      });
      h.push("</div>");
    });

    const voile = document.createElement("div");
    voile.id = "fiche-voile";
    voile.innerHTML = '<div id="fiche">' + h.join("") + "</div>";
    voile.addEventListener("click", (e) => {
      if (e.target === voile || e.target.classList.contains("fi-fermer")) fermer();
    });
    document.body.appendChild(voile);
  }

  document.addEventListener("keydown", (e) => { if (e.key === "Escape") fermer(); });

  // Est-ce le personnage que ce siège incarne ?
  function estMoi(id) {
    return !!(window.Moi && id && window.Moi.personnage_id === id);
  }

  // Ouvre la fiche ; `sinon` est rappelé quand ce siège n'en a pas d'écrite.
  function ouvrir(sinon) {
    fetch("/fiche").then((r) => r.json()).then((d) => {
      if (d && d.fiche) peindre(d.fiche);
      else if (sinon) sinon();
    }).catch(() => { if (sinon) sinon(); });
  }

  return { ouvrir, fermer, estMoi };
})();
