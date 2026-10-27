// mondes.js — « La partie » : le monde qu'on regarde, les parties en cartes
// qu'on peut ouvrir, et par où l'on passe à une autre.
//
// UN MONDE = UN SERVEUR = UN PORT. Le serveur ne change pas de monde à chaud ;
// choisir Cities of Light depuis Westeros, c'est aller sur une autre adresse
// (la table des ports est servie par GET /mondes, lue dans .claude/launch.json).
// Rien ne dit d'ici si l'autre serveur tourne : on le constate en y allant.
//
// Une partie en cartes, elle, vit dans le monde courant : on recharge la page
// avec `?id=&camp=&vue=conseil`, pour que la page s'ouvre sur les cartes et
// non sur le château.
//
// La zone est construite ici et non dans jeu.html : elle s'insère au-dessus du
// siège, avec le même dessin (mêmes classes de choix et de groupe).
"use strict";
(() => {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                             .replace(/"/g, "&quot;");

  const STYLE = `
#mondes{position:relative;}
#mondes-bouton{display:block;width:100%;box-sizing:border-box;text-align:left;
  padding:5px 10px;font:inherit;font-size:.94em;letter-spacing:.04em;
  color:var(--muted);background:none;border:1px solid var(--bord);
  border-radius:11px;cursor:pointer;}
#mondes-bouton:hover{color:var(--accent);border-color:var(--accent);}
#mondes-liste{margin-top:6px;display:flex;flex-direction:column;padding:4px;
  background:var(--fond);border:1px solid var(--bord);border-radius:6px;
  max-height:46vh;overflow-y:auto;overflow-x:hidden;}
#mondes-liste[hidden]{display:none;}
#mondes-liste .siege-choix{white-space:normal;}
#mondes-liste .siege-choix[disabled]{opacity:.45;cursor:default;}
#mondes-liste .siege-choix[disabled]:hover{background:none;color:var(--muted);}
.mondes-partie{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;padding-right:6px;}
.mondes-partie .siege-choix{flex:1 1 auto;}
.mondes-camp{padding:1px 7px;font:inherit;font-size:.78em;color:var(--muted);
  background:none;border:1px solid var(--bord);border-radius:9px;cursor:pointer;}
.mondes-camp:hover{color:var(--accent);border-color:var(--accent);}
.mondes-camp.actif{color:var(--accent);border-color:var(--accent);}`;

  function construire() {
    const siege = document.getElementById("zone-siege");
    const parent = siege ? siege.parentNode : document.getElementById("lateral-corps");
    if (!parent) return null;
    const st = document.createElement("style");
    st.textContent = STYLE;
    document.head.appendChild(st);
    const zone = document.createElement("div");
    zone.className = "zone";
    zone.id = "zone-mondes";
    zone.innerHTML = '<div class="zone-titre">La partie</div>' +
      '<div id="mondes"><button id="mondes-bouton" type="button" aria-haspopup="true"' +
      ' aria-expanded="false"></button><div id="mondes-liste" hidden></div></div>';
    parent.insertBefore(zone, siege || parent.firstChild);
    return zone;
  }

  const joli = (id) => id.replace(/-/g, " ").replace(/^./, (c) => c.toUpperCase());

  window.addEventListener("DOMContentLoaded", () => {
    fetch("/mondes").then((r) => r.json()).then((d) => {
      const mondes = (d && d.mondes) || [];
      const parties = (d && d.parties) || [];
      if (mondes.length < 2 && !parties.length) return;
      const zone = construire();
      if (!zone) return;
      const bouton = document.getElementById("mondes-bouton");
      const liste = document.getElementById("mondes-liste");

      const q = new URLSearchParams(location.search);
      const idIci = q.get("id");
      const campIci = q.get("camp");
      const ici = mondes.find((m) => m.courant);
      bouton.textContent = (ici ? ici.nom : "Le monde") + (idIci ? " · " + joli(idIci) : "");
      bouton.title = "Changer de monde ou de partie";

      const ligneMonde = (m) => {
        const titre = m.courant ? "Vous y êtes"
          : m.port ? "Ouvrir sur le port " + m.port
          : "Aucun serveur déclaré pour ce monde dans .claude/launch.json";
        return '<button type="button" class="siege-choix' + (m.courant && !idIci ? " actif" : "") +
          '" data-monde="' + esc(m.id) + '" data-port="' + esc(m.port || "") + '"' +
          (!m.courant && !m.port ? " disabled" : "") + ' title="' + esc(titre) + '">' +
          esc(m.nom) + (m.port && !m.courant ? " <small>:" + esc(m.port) + "</small>" : "") +
          "</button>";
      };
      const lignePartie = (p) => {
        const camps = p.camps.map((c) =>
          '<button type="button" class="mondes-camp' +
          (p.id === idIci && c === campIci ? " actif" : "") +
          '" data-partie="' + esc(p.id) + '" data-camp="' + esc(c) + '">' + esc(c) + "</button>").join("");
        return '<div class="mondes-partie"><button type="button" class="siege-choix' +
          (p.id === idIci ? " actif" : "") + '" data-partie="' + esc(p.id) + '" data-camp="' +
          esc(p.camps[0] || "") + '" title="' + esc(p.note || p.id) + '">' + esc(joli(p.id)) +
          "</button>" + camps + "</div>";
      };

      liste.innerHTML =
        '<div class="siege-groupe" style="border-top:0;margin-top:0">Les mondes</div>' +
        mondes.map(ligneMonde).join("") +
        (parties.length
          ? '<div class="siege-groupe">Les parties en cartes</div>' + parties.map(lignePartie).join("")
          : "");

      const fermer = () => { liste.hidden = true; bouton.setAttribute("aria-expanded", "false"); };
      bouton.onclick = (e) => {
        e.stopPropagation();
        const ouvert = !liste.hidden;
        liste.hidden = ouvert;
        bouton.setAttribute("aria-expanded", String(!ouvert));
      };
      liste.onclick = (e) => {
        const b = e.target.closest("button");
        if (!b || b.disabled) return;
        if (b.dataset.monde) {
          if (!b.dataset.port || b.classList.contains("actif")) return fermer();
          const m = mondes.find((x) => x.id === b.dataset.monde);
          if (m && m.courant) { location.href = "/"; return; }
          location.href = location.protocol + "//" + location.hostname + ":" + b.dataset.port + "/";
          return;
        }
        if (b.dataset.partie) {
          // `vue=` est la clef de nav.js : c'est elle qui décide de l'échelle
          // à l'ouverture, avant tout ce qui est gardé dans le navigateur.
          const p = new URLSearchParams({ id: b.dataset.partie });
          if (b.dataset.camp) p.set("camp", b.dataset.camp);
          p.set("vue", "conseil");
          location.href = "/?" + p.toString();
        }
      };
      // En capture, comme le siège : le décor arrête la propagation de ses clics.
      const dehors = (e) => { if (!liste.hidden && !zone.contains(e.target)) fermer(); };
      document.addEventListener("pointerdown", dehors, true);
      window.addEventListener("blur", fermer);
      document.addEventListener("keydown", (e) => { if (e.key === "Escape") fermer(); }, true);
    }).catch(() => {});
  });
})();
