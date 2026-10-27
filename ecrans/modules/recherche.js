// recherche.js — « search: un mot », et les quatre endroits où il est écrit.
//
// POURQUOI. Une partie de trois lunes tient dans quatre endroits qui ne se
// parlent pas : les CAHIERS (ce qui est arrêté, chiffré, adressé), les FILS
// (ce qui court, avec le nom d'un homme dessus), le FIL du récit (douze mille
// lignes de ce qui s'est dit), et les GENS (deux cent quatre-vingts noms dont
// personne ne retient les charges). Chercher « la roukerie » demandait quatre
// gestes dans quatre écrans — et c'est la pente qui fait qu'on abandonne une
// affaire au lieu de la finir.
//
// CE QUE C'EST, ET CE QUE CE N'EST PAS. Ce n'est pas un mode : rien ne part au
// MJ, rien n'entre dans `flux.jsonl` ni dans `etat/`, l'horloge ne bouge pas,
// et personne dans la salle ne s'aperçoit qu'on a cherché. Comme le fil refait
// de la régie, ce panneau vit dans la page et meurt avec elle. C'est un geste
// de LECTURE, posé dans le fil parce que c'est là que se lisent les lectures.
//
// Et ce n'est pas un menu : on ne propose rien, on rend ce qui est écrit. Ce
// qu'on en fait — ouvrir le volume, rouvrir le moment, penser à l'homme — sont
// les gestes que le jeu offre déjà partout ailleurs, avec leurs conséquences
// ordinaires. Un résultat n'est pas une option ; c'est une adresse.
//
// LE BROUILLARD EST TENU AU SERVEUR, jamais ici : `/chercher` passe les
// cahiers par `volumesVisibles`, le fil par `filtrerFlux`, les gens par la vue
// de mémoire de `/gens`. Ce module dessine ce qu'on lui donne et ne demande
// jamais rien d'autre.
"use strict";
window.Recherche = (() => {
  // On ferme avant d'ouvrir : deux panneaux de recherche dans le fil, et l'on
  // ne sait plus lequel répond à quoi.
  let ouvert = null;

  const esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

  // Un libellé qui porte des crochets casserait le pointeur qu'on écrit avec :
  // `[les [neufs]](44022)` ne s'allume pas. On les retire du LIBELLÉ, jamais du
  // texte lu.
  const sansCrochets = (s) => String(s == null ? "" : s).replace(/[[\]()]/g, " ")
    .replace(/\s+/g, " ").trim();

  const dateTexte = (d) => d
    ? d.annee + " AC · " + d.lune + "e lune, " + d.jour + "e jour" +
      (typeof d.minute === "number"
        ? " · " + Math.floor(d.minute / 60) + "h" + String(d.minute % 60).padStart(2, "0")
        : "")
    : "";

  const GENRES = { replique: "réplique", geste: "geste", recit: "récit",
    breve: "brève", pensee: "pensée", vous: "vous", question: "question",
    reponse: "réponse", marque: "il s'est passé", salle: "la salle",
    coulisses: "coulisses", suites: "suites", ecrit: "au registre",
    evenement: "événement", table: "à la table", meta: "coulisses",
    intervention: "intervention", run: "laisser faire", demande: "demande" };

  const FAMILLES = [
    ["affaires", "Les cahiers"],
    ["fils", "Ce qui court"],
    ["fil", "Le fil"],
    ["gens", "Les gens"],
  ];

  // Le compte, dit en français : « 4 sur 200 » plutôt qu'un nombre nu, parce
  // qu'un résultat coupé sans le dire fait croire qu'il n'y a que ça.
  function combien(montres, total) {
    if (!total) return "rien";
    if (montres >= total) return total === 1 ? "un seul" : total + " en tout";
    return montres + " sur " + total;
  }

  // ---- ce qu'on écrit dans chaque famille ----------------------------------
  // Les cahiers : un pointeur, jamais un numéro nu (CLAUDE.md, les interdits).
  // Écrit `[le libellé](44022)`, il ouvre le volume ET descend à la ligne —
  // c'est `renvois.js` qui s'en charge, le même chemin que pour une réplique de
  // conseiller. Une ligne sans adresse garde un bouton à nous, qui ouvre le
  // volume à son titre.
  function ligneCahier(a) {
    const oue = '<span class="rech-ou">' + esc(a.titre) +
      (a.table ? " · " + esc(a.table) : "") + "</span>";
    if (a.genre === "ligne" && a.adresse) {
      return '<div class="rech-quoi">[' + esc(sansCrochets(a.libelle)) +
        "](" + esc(a.adresse) + ")</div>" + oue +
        (a.quoi ? '<div class="rech-extrait">' + esc(a.quoi) + "</div>" : "");
    }
    const nom = a.genre === "volume" ? a.titre : (a.libelle || a.table || a.titre);
    return '<button type="button" class="rech-lien" data-livre="' + esc(a.livre) +
      '" data-cible="' + esc(a.cible || "") + '">' + esc(nom) + "</button>" +
      (a.genre === "volume" ? "" : oue) +
      (a.quoi ? '<div class="rech-extrait">' + esc(a.quoi) + "</div>" : "");
  }

  function ligneFil(f) {
    const tete = [f.date ? dateTexte(f.date) : null, f.lieu, f.moment]
      .filter(Boolean).map(esc).join(" · ");
    return '<div class="rech-ou">' + tete +
      '<span class="rech-genre">' + esc(GENRES[f.type] || f.type) + "</span>" +
      (f.nom ? '<span class="rech-qui">' + esc(f.nom) + "</span>" : "") + "</div>" +
      '<div class="rech-quoi">' + esc(f.extrait) + "</div>" +
      '<button type="button" class="rech-montrer" data-i="' + (f.i | 0) +
      '">Montrer ce moment</button>';
  }

  function ligneAffaire(f) {
    const bas = [f.sur_nom ? "sur " + f.sur_nom : "sans nom",
      f.echeance ? "dû le " + f.echeance : null,
      f.mode === "delegue" ? "délégué" : f.mode === "joue" ? "à jouer" : null,
      f.statut && f.statut !== "en-cours" ? f.statut : null].filter(Boolean);
    return '<div class="rech-quoi">' + esc(f.titre) + "</div>" +
      '<span class="rech-ou">' + esc(bas.join(" · ")) + "</span>" +
      (f.detail ? '<div class="rech-extrait">' + esc(f.detail) + "</div>" : "") +
      (f.dernier ? '<div class="rech-extrait">' + esc(f.dernier) + "</div>" : "");
  }

  // Les gens : le nom en toutes lettres, parce qu'`Entites.traiter` le rendra
  // cliquable comme n'importe quel nom du fil — un clic, et c'est une PENSÉE,
  // le canal que le jeu offre déjà. On n'invente pas un second geste pour la
  // même chose.
  function ligneGens(g) {
    return '<div class="rech-quoi">' + esc(g.nom) + "</div>" +
      (g.titre ? '<span class="rech-ou">' + esc(g.titre) + "</span>" : "") +
      (g.maison ? '<span class="rech-ou"> · ' + esc(g.maison) + "</span>" : "") +
      (g.vu ? '<div class="rech-extrait">vu ' + esc(g.vu.quand) + " à " +
        esc(g.vu.lieu) + (g.vu.source ? " — " + esc(g.vu.source) : "") +
        (g.vu.certitude && g.vu.certitude !== "sure"
          ? " (" + esc(g.vu.certitude) + ")" : "") + "</div>" : "");
  }

  const DESSINS = { affaires: ligneCahier, fils: ligneAffaire,
                    fil: ligneFil, gens: ligneGens };

  // ---- « Montrer ce moment » ----------------------------------------------
  // La tranche de fil autour du résultat, dépliée SOUS lui. On la demande à
  // `/chercher?autour=` et non à `/regie/extrait` : celui-là sert le fichier
  // brut à la régie, et un siège de joueur y demanderait n'importe quel
  // intervalle. Le même œil pour chercher et pour montrer, ou rien.
  async function montrer(bouton) {
    const hote = bouton.parentNode;
    const deja = hote.querySelector(".rech-tranche");
    if (deja) { deja.remove(); bouton.textContent = "Montrer ce moment"; return; }
    bouton.textContent = "on rouvre le fil ici…";
    let d;
    try {
      const r = await fetch("/chercher?autour=" + (bouton.dataset.i | 0) + "&marge=8");
      d = await r.json();
      if (!d || d.erreur) throw new Error((d && d.erreur) || "muet");
    } catch (e) {
      bouton.textContent = "rien à rouvrir";
      return;
    }
    const tranche = document.createElement("div");
    tranche.className = "rech-tranche";
    let s = "", jour = "";
    (d.items || []).forEach((it) => {
      if (!it.texte && it.type !== "salle") return;
      const j = it.date ? dateTexte(it.date) : "";
      if (j && j !== jour) {
        jour = j;
        s += '<div class="rech-jour">' + esc(j) +
          (it.lieu ? " · " + esc(it.lieu) : "") + "</div>";
      }
      s += '<div class="rech-entree' + (it._centre ? " rech-ici" : "") + '">' +
        '<span class="rech-genre">' + esc(GENRES[it.type] || it.type) + "</span>" +
        (it.nom ? '<span class="rech-qui">' + esc(it.nom) + "</span>" : "") +
        '<div class="rech-texte">' + esc(it.texte || it.titre || "") + "</div></div>";
    });
    tranche.innerHTML = s || '<div class="rech-entree">rien de lisible ici.</div>';
    hote.appendChild(tranche);
    bouton.textContent = "Replier";
    if (window.Entites) Entites.traiter(tranche);
  }

  // ---- le panneau ---------------------------------------------------------
  function fermer() {
    if (ouvert) { ouvert.remove(); ouvert = null; }
  }

  function poser(titre, dedans) {
    const zone = document.getElementById("fil-corps");
    if (!zone) return null;
    fermer();
    const bloc = document.createElement("div");
    bloc.className = "rech";
    bloc.innerHTML = '<div class="rech-tete"><span>' + esc(titre) +
      '</span><em></em><button type="button" class="rech-fermer" ' +
      'title="Retirer du fil">×</button></div><div class="rech-corps">' +
      dedans + "</div>";
    bloc.querySelector(".rech-fermer").onclick = fermer;
    zone.appendChild(bloc);
    ouvert = bloc;
    zone.scrollTo({ top: zone.scrollHeight, behavior: "smooth" });
    return bloc;
  }

  function rendre(d) {
    const bloc = poser("Cherché « " + d.q + " »", "on cherche…");
    if (!bloc) return;
    const corps = bloc.querySelector(".rech-corps");
    const resume = [];
    let rien = true;
    let s = "";
    FAMILLES.forEach(([clef, nom]) => {
      const liste = d[clef] || [];
      const total = (d.combien && d.combien[clef]) || 0;
      if (!liste.length) return;
      rien = false;
      resume.push(total + " " + nom.toLowerCase());
      s += '<div class="rech-famille">' + esc(nom) +
        '<em>' + esc(combien(liste.length, total)) + "</em></div>";
      liste.forEach((x) => {
        s += '<div class="rech-item rech-' + clef + '">' + DESSINS[clef](x) + "</div>";
      });
    });
    if (rien) {
      // Un « rien » honnête, et ce qu'il veut dire : ce siège-là ne le trouve
      // pas: ce n'est pas la même chose que « ça n'existe pas ». On le dit,
      // plutôt que de laisser croire à une panne.
      s = '<div class="rech-vide">Rien de ce nom dans vos cahiers, dans ce qui court, ' +
        "dans le fil ni parmi les gens que vous connaissez." +
        (d.adresse ? " Cette adresse n'est dans aucun volume à votre portée." : "") +
        "</div>";
    }
    corps.innerHTML = s;
    bloc.querySelector(".rech-tete em").textContent = resume.join(" · ");
    // Les pointeurs `[…](44022)` et les noms deviennent vivants par le même
    // chemin que dans le reste du fil — un seul comportement pour un seul
    // geste, et pas un clic inventé pour cet écran.
    if (window.Attention) {
      corps.querySelectorAll(".rech-quoi").forEach((el) => {
        if (el.textContent.indexOf("](") !== -1) el.innerHTML = Attention.html(el.textContent, {});
      });
    }
    if (window.Entites) Entites.traiter(corps);
    corps.querySelectorAll(".rech-montrer").forEach((b) => {
      b.onclick = () => montrer(b);
    });
    corps.querySelectorAll(".rech-lien").forEach((b) => {
      b.onclick = () => {
        const cible = b.dataset.cible || null;
        if (!(window.Books && Books.ouvrir && Books.ouvrir(b.dataset.livre, cible))) {
          b.classList.add("rech-hors-portee");
          b.title = "Ce volume n'est pas à portée d'ici";
        }
      };
    });
  }

  async function chercher(q) {
    const besoin = String(q == null ? "" : q).trim();
    if (besoin.length < 2) {
      poser("Chercher", '<div class="rech-vide">Un mot, un nom, ou une adresse de ' +
        "registre — « search: roukerie », « search: 44022 ». On cherche dans vos " +
        "cahiers, dans ce qui court, dans le fil et parmi les gens.</div>");
      return;
    }
    poser("Cherché « " + besoin + " »", '<div class="rech-vide">on cherche…</div>');
    let d;
    try {
      const r = await fetch("/chercher?q=" + encodeURIComponent(besoin) + "&max=6");
      d = await r.json();
      if (!d || d.erreur) throw new Error((d && d.erreur) || "muet");
    } catch (e) {
      poser("Cherché « " + besoin + " »",
        '<div class="rech-vide">La recherche n\'a pas répondu : ' + esc(e.message || e) +
        "</div>");
      return;
    }
    rendre(d);
  }

  // LE PRÉFIXE, et pourquoi il vaut mieux qu'un neuvième bouton. La barre en
  // porte déjà huit ; celui-ci ne serait pas un mode — il n'envoie rien, ne
  // coûte pas une minute, et son résultat n'est pas une réponse du MJ. Un mot
  // tapé devant sa recherche dit tout ça sans occuper la largeur du bandeau.
  const PREFIXE = /^\s*(?:search|cherche|chercher|rech)\s*:\s*/i;

  // Rend `true` quand la ligne était une recherche — l'appelant n'envoie alors
  // rien. Le champ n'est PAS vidé : on affine sa recherche en corrigeant un
  // mot, pas en la retapant.
  function depuisChamp(texte) {
    if (!PREFIXE.test(texte || "")) return false;
    chercher(String(texte).replace(PREFIXE, ""));
    return true;
  }

  return { chercher, depuisChamp, fermer };
})();
