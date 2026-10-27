// GET /entites, /gens — les gens et les lieux, servis au décor.
const fs = require("fs");
const path = require("path");
const { DEPOT, ETAT } = require("../http");
const { envoyer } = require("../http");
const { portraitDefaut, portraitFrais } = require("../peinture").portraits; // LA PORTE serveur de peinture
const { qui } = require("../http");
const { manifeste, racine } = require("../racines");
const { filtreConnus } = require("../monde/connus");

function traiter(req, res, url) {
  if (req.method === "GET") {
    if (url === "/entites") {
      try {
        const lire = (f) => JSON.parse(fs.readFileSync(path.join(ETAT, f), "utf-8"));
        const vus = new Set();
        const entites = [];
        const ajouter = (id, type, noms) => {
          const propres = noms.filter((n) => n && n.length > 2 && !vus.has(n.toLowerCase()));
          if (!propres.length) return;
          propres.forEach((n) => vus.add(n.toLowerCase()));
          entites.push({ id, type, noms: propres });
        };
        const siegeE = qui(req, url);
        const connuE = filtreConnus(manifeste(), siegeE && siegeE.personnage_id, lire) || (() => true);
        const persos = lire("personnages.json").filter(connuE);
        const prenoms = {};
        persos.forEach((p) => {
          const t = p.nom.split(/[ ,]/)[0];
          prenoms[t] = (prenoms[t] || 0) + 1;
        });
        persos.forEach((p) => {
          const noms = [p.nom.split(",")[0].trim()];
          const prenom = p.nom.split(/[ ,]/)[0];
          if (prenoms[prenom] === 1) noms.push(prenom);
          ajouter(p.id, "personnage", noms);
        });
        lire("lieux.json").forEach((l) => ajouter(l.id, "lieu", [l.nom]));
        lire("maisons.json").forEach((m) => ajouter(m.id, "maison", [m.nom]));
        // LES BÊTES VIENNENT DU MONDE, PLUS DE CETTE LIGNE (9.9). Ces neuf-là
        // étaient écrites ici, donc elles partaient avec N'IMPORTE quel monde :
        // le monde d'épreuve, qui n'a ni Westeros ni dragons, servait Caraxès et
        // Vhagar dès sa première requête. Une table absente ne rend rien, et
        // c'est la bonne réponse — un monde sans bêtes n'en a pas.
        (() => {
          let d;
          try { d = JSON.parse(fs.readFileSync(path.join(ETAT, "dragons.json"), "utf-8")); }
          catch (e) { return; }
          const l = Array.isArray(d) ? d
            : (Object.values(d).find((v) => Array.isArray(v)) || []);
          l.forEach((x) => {
            if (x && x.id && x.nom) ajouter(x.id, x.type || "dragon", [x.nom]);
          });
        })();
        return envoyer(res, 200, JSON.stringify({ entites }));
      } catch (e) {
        return envoyer(res, 200, JSON.stringify({ entites: [], erreur: String(e) }));
      }
    }
    // Les gens : qui est qui, et de quel côté. Une vue de mémoire, pas de
    // renseignement — on n'y donne NI position, NI intentions, NI allégeance
    // réelle : le nom, le rôle, la maison, et le camp affiché.
    if (url === "/gens") {
      try {
        const lire = (f) => JSON.parse(fs.readFileSync(path.join(ETAT, f), "utf-8"));
        const maisons = {};
        lire("maisons.json").forEach((m) => {
          maisons[m.id] = m;
          maisons[m.id.replace(/^maison-/, "")] = m;
        });
        // Qui porte la couronne du « joueur » sur CET ecran : celui qui
        // regarde, pas celui du journal. A deux, le journal designe Rhaenyra —
        // l'ecran d'Aurore marquait donc la reine comme le personnage joue.
        const siege = qui(req, url);
        let joueur_id = (siege && siege.personnage_id) || null;
        if (!joueur_id) {
          try { joueur_id = lire("journal.json").personnage_joueur_id || null; } catch (e) {}
        }
        const connu = filtreConnus(manifeste(), siege && siege.personnage_id, lire) || (() => true);
        let ferveurs = {};
        try { ferveurs = JSON.parse(fs.readFileSync(path.join(racine(), "ferveurs-interface.json"), "utf-8")).personnages || {}; } catch (e) {}
        ferveurs = require("../ferveurs-sim")(racine(), ferveurs);
        try {
          const config = JSON.parse(fs.readFileSync(path.join(racine(), "liaison-ferveurs.json"), "utf8"));
          const joueurs = JSON.parse(fs.readFileSync(config.choix_joueur, "utf8"));
          for (const [id, lien] of Object.entries(config.personnages)) {
            const p = joueurs.find(p => p.id === lien.id && p.first === lien.first && p.last === lien.last);
            if (!p) continue;
            const choix = [...new Map(p.choices.map(c => [c.ref, c])).values()];
            ferveurs[id] = { valeur: Math.max(0, Math.min(100, p.baseline + choix.reduce((s,c) => s+c.delta, 0))),
              nature: "choix_joueur", date_source: choix.map(c=>c.at).sort().pop() || null,
              details: ["Base : " + p.baseline, ...choix.map(c => (c.delta >= 0 ? "+" : "") + c.delta + " — " + c.reason)] };
          }
        } catch (e) {}
        const opinions = new Map();
        const detailsOpinions = new Map();
        const provenanceOpinions = new Map();
        for (const fichier of ["provenance-opinions.json", "provenance-opinions-michel.json"]) {
          try {
            const provenance = JSON.parse(fs.readFileSync(path.join(racine(), fichier), "utf-8"));
            for (const r of provenance.relations || []) {
              if (r.cible_id === joueur_id) provenanceOpinions.set(r.source_id, r);
            }
          } catch (e) {}
        }
        const relationsConnues = new Set();
        let relations = [];
        try { relations = lire("relations.json"); } catch (e) {}
        relations.forEach((r) => {
          const source = r.source_id || r.de, cible = r.cible_id || r.vers;
          if (r.connue_du_joueur === true) {
            if (source === joueur_id) relationsConnues.add(cible);
            if (cible === joueur_id) relationsConnues.add(source);
          }
          if ((r.cible_id || r.vers) === joueur_id && r.connue_du_joueur === true &&
              typeof r.opinion === "number" && Number.isFinite(r.opinion)) {
            opinions.set(r.source_id || r.de, r.opinion);
            const origine = provenanceOpinions.get(source);
            const lignes = [];
            if (Array.isArray(r.liens) && r.liens.length) lignes.push("Lien : " + r.liens.join(", "));
            if (origine && Number.isFinite(origine.confiance_source)) {
              const base = 2 * origine.confiance_source - 100;
              lignes.push("Confiance source : " + origine.confiance_source + "/100");
              lignes.push("Opinion importée : 2 × " + origine.confiance_source + " − 100 = " + base);
              if (base !== r.opinion) lignes.push("Évolution depuis l’import : " + (r.opinion - base > 0 ? "+" : "") + (r.opinion - base));
              lignes.push("Score adapté de la confiance de la simulation.");
            } else {
              const freres = ["michel", "lucien-frere-de-michel"];
              lignes.push(r.opinion === 0 && freres.includes(source) && freres.includes(cible)
                ? "Opinion non calibrée : aucun détail de calcul disponible." : "Aucun détail de calcul enregistré.");
            }
            detailsOpinions.set(source, lignes);
          }
        });
        const personnes = lire("personnages.json");
        const regleReseau = (manifeste().gens || {}).contacts_indirects;
        let indirects = new Map(), directs = null;
        if (regleReseau && joueur_id && !(siege && siege.personnage_id === "mj")) {
          const filtre = filtreConnus({ gens: { brouillard: true } }, joueur_id, lire);
          directs = new Set(personnes.filter(filtre).map(p => p.id));
          let reseau = { personnes: [], liens: [] };
          try { reseau = JSON.parse(fs.readFileSync(path.join(racine(), "contacts-indirects.json"), "utf8")); } catch (e) {}
          const fiches = new Map((reseau.personnes || []).map(p => [p.id, p]));
          personnes.forEach(p => fiches.set(p.id, p));
          indirects = require("../domaine/contacts-indirects").projeter(joueur_id, directs, relations, fiches, reseau.liens || [], regleReseau);
        }
        const gens = personnes
          .filter((p) => p.etat !== "mort" && connu(p) && (!directs || directs.has(p.id)))
          .map((p) => {
            const m = maisons[p.maison_id] || null;
            // Tout le monde a un rond : faute de portrait dessiné, la
            // silhouette anonyme tient la place.
            let portrait_svg = "";
            const f = p.portrait && p.portrait.fichier;
            if (f) {
              try { portrait_svg = fs.readFileSync(path.join(DEPOT, f), "utf-8"); } catch (e) {}
            }
            // LE CHAMP `portrait.fichier` N'EST PAS UNE CONDITION D'EXISTENCE.
            // Il manquait à une bonne part des fiches, et ces gens-là gardaient
            // la silhouette anonyme alors que leur médaillon était peint et
            // posé sur le disque — un manque invisible, puisque rien n'échoue.
            // `medaillons.py` écrit toujours `ecrans/portraits/<id>.svg` : cet
            // id EST l'adresse. On la tente donc quand le champ ne dit rien,
            // et peindre un visage suffit désormais à le faire paraître.
            if (!portrait_svg) portrait_svg = portraitFrais(p.id) || "";
            if (!portrait_svg) portrait_svg = portraitDefaut(p.nom || p.id);
            return {
              id: p.id, nom: p.nom, titre: p.titre || "",
              contacts_indirects: (indirects.get(p.id) || []).map(c => ({ ...c,
                ferveur: ferveurs[c.id] ? ferveurs[c.id].valeur : null,
                ferveur_date: ferveurs[c.id] ? ferveurs[c.id].date_source : null,
                ferveur_nature: ferveurs[c.id] ? ferveurs[c.id].nature : null,
                opinion: opinions.has(c.id) ? opinions.get(c.id) : null,
                opinion_details: detailsOpinions.get(c.id) || [],
                portrait_svg: portraitFrais(c.id) || portraitDefaut(c.nom) })),
              traits: Array.isArray(p.traits) ? p.traits.filter((t) => typeof t === "string") : [],
              maison_id: m ? m.id : null,
              // une maison sans fiche (les grands lointains : Stark, Arryn…)
              // garde tout de même son nom, tiré de son id
              maison: m ? m.nom : p.maison_id
                ? p.maison_id.replace(/^maison-/, "").replace(/-/g, " ")
                    .replace(/(^|\s)\p{Ll}/gu, (c) => c.toUpperCase())
                : "Sans maison",
              camp: m ? (m.allegeance_affichee || "neutre") : "neutre",
              joueur: p.id === joueur_id,
              relation_connue: relationsConnues.has(p.id),
              opinion: opinions.has(p.id) ? opinions.get(p.id) : null,
              opinion_details: detailsOpinions.get(p.id) || [],
              ferveur: ferveurs[p.id] && Number.isFinite(ferveurs[p.id].valeur) ? ferveurs[p.id].valeur : null,
              ferveur_date: ferveurs[p.id] ? ferveurs[p.id].date_source : null,
              ferveur_nature: ferveurs[p.id] ? ferveurs[p.id].nature : null,
              ferveur_details: ferveurs[p.id] ? ferveurs[p.id].details : null,
              portrait_svg,
            };
          });
        return envoyer(res, 200, JSON.stringify({ gens }));
      } catch (e) {
        return envoyer(res, 200, JSON.stringify({ gens: [], erreur: String(e) }));
      }
    }
  }
  return false;
}

module.exports = traiter;
