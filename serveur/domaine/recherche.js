// LA RECHERCHE — un mot, et les quatre endroits où il peut être écrit.
//
// POURQUOI CE FICHIER EXISTE. Une partie de trois lunes tient dans quatre
// endroits qui ne se parlent pas : les CAHIERS (ce qui est arrêté, chiffré,
// adressé), les FILS (ce qui court, avec le nom d'un homme dessus), le FIL du
// récit (ce qui s'est dit et fait, douze mille lignes), et les GENS (deux cent
// quatre-vingts noms dont personne ne retient les charges). Le joueur qui
// cherche « la roukerie » devait ouvrir les Livres, se rappeler dans quel
// volume, faire défiler la chronique à la molette, et deviner qui la tient.
// Quatre gestes, trois échecs, et l'affaire abandonnée — c'est la pente qui
// fait qu'on rejoue au lieu de continuer.
//
// CE QU'ELLE NE FAIT PAS, ET C'EST VOULU :
//
//   — ELLE NE JUGE PAS. Elle rend les endroits où la chose est écrite, jamais
//     « le bon ». « Le moment où Steffon est arrivé » n'est pas une chaîne de
//     caractères, c'est un jugement — la première occurrence du mot est
//     presque toujours la mauvaise. Le lecteur lit et tranche.
//   — ELLE NE VOIT QUE CE QUE CE SIÈGE VOIT. Les cahiers passent par
//     `volumesVisibles`, le fil par `filtrerFlux`, les fils par le dossier du
//     siège, les gens par ce que `/gens` sert déjà (le nom, la charge, la
//     maison — NI position, NI tête, NI allégeance réelle). Une recherche est
//     le premier endroit où l'on trahirait le brouillard : on n'y ouvre pas
//     une porte que les Livres et la scène tiennent fermée.
//   — ELLE NE COÛTE PAS UNE MINUTE et n'écrit rien. Ni `flux.jsonl`, ni
//     `etat/`, ni l'inbox du MJ : chercher, comme penser, est gratuit et
//     silencieux. Personne dans la salle ne s'aperçoit qu'on a cherché.
//
// Un module de `domaine/` ne connaît ni `req` ni `res` : il prend des valeurs
// (le siège, déjà résolu par la route) et rend un objet sérialisable.
const fs = require("fs");
const path = require("path");
const { RACINE, ETAT } = require("../contexte");
const { filtrerFlux, volumesVisibles } = require("../siege");
const { dateCourte, jourAbsolu, vieillir, AGE_DIT } = require("../dates");
const bibliotheque = require("../plan/bibliotheque"); // LA PORTE serveur du plan

// Combien on en montre par famille. Un mur de résultats est le même mal qu'un
// registre déballé : personne n'en ouvre aucun. Le compte total est rendu à
// côté, pour que la page puisse dire « et trente et un autres » sans mentir.
const PAR_FAMILLE = 8;
const MARGE = 6;                       // lignes de fil autour d'un moment
const ADRESSE = /^\s*(?:\*\*)?\s*(\d{4,6})\b/;

const lire = (f, defaut) => {
  try { return JSON.parse(fs.readFileSync(path.join(ETAT, f), "utf-8")); }
  catch (e) { return defaut; }
};

// Sans accents et sans casse : on cherche « peyredragon » en tapant
// « Peyredragon », et « échéance » en tapant « echeance ». Un joueur ne tape
// pas ses accents dans une barre de recherche.
const plat = (t) => String(t == null ? "" : t)
  .normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

// Le gras du markdown et les espaces doublées ne sont pas du texte cherché :
// ils sont de la mise en page tombée dans la donnée.
const nu = (t) => String(t == null ? "" : t)
  .replace(/\*\*/g, "").replace(/\s+/g, " ").trim();

// LE FILTRE EST CONJONCTIF : tous les mots utiles dans le MÊME endroit. Un
// « et » de plus ne doit pas rendre la moitié du dépôt. Les mots de deux
// lettres sont écartés — « la », « de », « on » n'apprennent rien —, sauf
// quand la requête entière est courte, auquel cas on cherche la chaîne telle
// quelle : « or » et « nef » sont des mots de ce monde.
function tamis(q) {
  const b = plat(q).trim();
  const mots = b.split(/\s+/).filter((m) => m.length > 2);
  if (!mots.length) return (t) => b.length >= 2 && plat(t).indexOf(b) !== -1;
  return (t) => { const p = plat(t); return mots.every((m) => p.indexOf(m) !== -1); };
}

// LE FRAGMENT — le mot cherché, avec ce qui l'entoure et rien de plus.
//
// Sans lui, un résultat rendait les deux cent quarante premiers signes de la
// ligne : quand le mot tombait à la fin d'un paragraphe de mille signes, le
// joueur lisait un extrait où sa recherche n'apparaissait PAS et concluait à
// une panne. On centre donc sur la première occurrence.
//
// Les offsets sont comptés sur le texte à plat (sans accents) et appliqués au
// texte original : les deux ont la même longueur pour de l'accentuation
// ordinaire (un « é » composé rend un « e »). Un décalage d'un ou deux signes
// sur un cas exotique déplace la fenêtre, il ne la rate pas.
function fragment(texte, mots, large) {
  const t = nu(texte);
  const plage = large || 240;
  if (t.length <= plage) return t;
  const p = plat(t);
  let pos = -1;
  (mots || []).forEach((m) => {
    const k = p.indexOf(m);
    if (k !== -1 && (pos === -1 || k < pos)) pos = k;
  });
  if (pos <= plage / 2) return t.slice(0, plage) + " …";
  const de = Math.max(0, pos - Math.floor(plage / 3));
  return "… " + t.slice(de, de + plage) + (de + plage < t.length ? " …" : "");
}

// ---- 1. LES CAHIERS : ce qui est arrêté ------------------------------------
// Une ligne de cahier qui commence par un numéro est ADRESSABLE : écrite
// `[les neufs](44022)`, elle ouvre le volume et se surligne. On rend donc le
// numéro et le libellé séparément, parce que c'est la seule forme qui mène
// quelque part — un numéro nu ne dit rien à personne (CLAUDE.md, les interdits).
function cahiers(volumes, va, adresse, mots) {
  const trouves = [];
  volumes.forEach((v) => {
    const livre = v.id;
    const titre = nu(v.titre || v.id);
    // Le volume lui-même : on cherche « murs », et le cahier « Rendre les murs
    // solides » est la réponse avant n'importe laquelle de ses lignes.
    if (!adresse && (va(v.titre) || va(v.sous_titre))) {
      trouves.push({ genre: "volume", livre, titre,
        quoi: nu(v.sous_titre) || null, cible: null, adresse: null, rang: 0 });
    }
    const tables = (v.tables || []).slice();
    if (v.colonnes) tables.push({ colonnes: v.colonnes, lignes: v.lignes || [] });
    tables.forEach((t) => {
      (t.lignes || []).forEach((l) => {
        const cells = ((l && (l.cellules || l)) || []).map((c) => nu(c));
        if (!cells.length) return;
        const m = ADRESSE.exec(cells[0]);
        const num = m ? m[1] : null;
        if (adresse) { if (num !== adresse) return; }
        else if (!va(cells.join(" · "))) return;
        // OU LE MOT TOMBE COMPTE PLUS QUE L'ORDRE DES VOLUMES. Une ligne qui
        // s'APPELLE « gardien de la roukerie » vaut mieux que trente lignes
        // qui la mentionnent en passant dans leur troisieme colonne — et sans
        // ce tri, les cahiers calcules (`plan-verrous`, `plan-etats-cibles`,
        // les plus fournis) prenaient les huit places a eux seuls.
        const nomme = adresse ? true : va(cells.slice(0, 2).join(" · "));
        // Le libellé est ce qu'un homme DIT de cette ligne : la deuxième
        // cellule, débarrassée de son émoji de tête. À défaut, la première
        // sans son numéro.
        const lib = nu((cells[1] || "").replace(/^[^\w(«"']+/, "")) ||
                    nu(cells[0].replace(ADRESSE, ""));
        trouves.push({ genre: "ligne", livre, titre,
          table: nu(t.titre) || null,
          adresse: num, libelle: lib || "…",
          // Ce qui ouvre le volume à la bonne place : le numéro s'il y en a
          // un, le libellé sinon — `Books.ouvrir` accepte les deux.
          cible: num || lib || null,
          quoi: fragment(cells.slice(num ? 1 : 0).filter(Boolean).join(" · "),
                          mots, 260),
          rang: (nomme ? 1 : 3) + (num ? 0 : 1) });
      });
    });
    if (adresse) return;
    // Les pages : la prose du cahier, celle qui explique pourquoi la ligne dit
    // ce qu'elle dit. On rend le PARAGRAPHE et non la page — une page entière
    // dans un résultat de recherche est un mur.
    (v.pages || []).forEach((p) => {
      const texte = typeof p === "string" ? p : (p && (p.texte || p.corps)) || "";
      const nomPage = typeof p === "string" ? null : nu(p && p.titre);
      String(texte).split(/\n{2,}/).forEach((par) => {
        if (!va(par)) return;
        trouves.push({ genre: "page", livre, titre, table: nomPage || null,
          adresse: null, cible: nomPage || null,
          quoi: fragment(par, mots, 300), rang: 5 });
      });
    });
  });
  trouves.sort((a, b) => a.rang - b.rang);
  return trouves;
}

// ---- 2. LES FILS : ce qui court --------------------------------------------
// Par siège, comme le rail : `etat/joueurs/<siège>/fils.json`. Un fil porte le
// nom de l'homme qui tient la plume et l'heure où c'est dû — c'est ce qu'on
// vient chercher quand on tape un mot, bien plus que son intitulé exact.
function fils(siegeId, va, noms) {
  if (!siegeId) return [];
  let doc = {};
  try {
    doc = JSON.parse(fs.readFileSync(
      path.join(ETAT, "joueurs", siegeId, "fils.json"), "utf-8"));
  } catch (e) { return []; }
  return (doc.fils || [])
    .filter((f) => f && va([f.titre, f.detail, f.dernier,
                            noms.get(f.sur) || f.sur].join(" · ")))
    .map((f) => ({ id: f.id, titre: nu(f.titre), detail: nu(f.detail) || null,
      sur: f.sur || null, sur_nom: (f.sur && (noms.get(f.sur) || f.sur)) || null,
      echeance: dateCourte(f.echeance) || null,
      mode: f.mode || null, statut: f.statut || null,
      dernier: nu(f.dernier) || null }));
}

// ---- 3. LE FIL : ce qui s'est dit ------------------------------------------
// Le fil filtré pour ce siège, et rien d'autre. Les indices comptent ce fil-là
// — voir `filtrerFlux` : un index n'est une adresse que dans le fil de celui
// qui l'a reçu, et `autour()` les relit du même œil.
function fluxDuSiege(siege) {
  let brut = "";
  try { brut = fs.readFileSync(path.join(ETAT, "flux.jsonl"), "utf-8"); }
  catch (e) { return []; }
  const items = brut.split("\n").filter((l) => l.trim()).map((l) => {
    try { return JSON.parse(l); } catch (e) { return {}; }
  });
  return filtrerFlux(items, siege);
}

// La date et le lieu ne sont pas sur chaque item : ils VALENT jusqu'au
// prochain. Sans ce report, neuf résultats sur dix sortiraient sans date.
function courants(items) {
  let date = null, lieu = "", moment = "";
  return items.map((it) => {
    if (it.date) date = it.date;
    if (it.lieu) lieu = it.lieu;
    if (it.moment) moment = it.moment;
    return { date, lieu, moment };
  });
}

function fil(items, va, noms, mots) {
  const ctx = courants(items);
  const trouves = [];
  items.forEach((it, i) => {
    const t = it.texte || "";
    if (!t || !va(t)) return;
    const qui = it.locuteur_id || it.acteur_id || null;
    trouves.push({ i, type: it.type, date: ctx[i].date,
      lieu: ctx[i].lieu || null, moment: ctx[i].moment || null,
      qui, nom: (qui && (noms.get(qui) || qui)) || null,
      extrait: fragment(t, mots) });
  });
  // Les derniers d'abord : on cherche presque toujours quelque chose de récent.
  return trouves.reverse();
}

// ---- 4. LES GENS : qui est qui --------------------------------------------
// La même vue que `/gens` : le nom, la charge, la maison. NI position, NI
// intentions, NI allégeance réelle — la charge écrite dans `titre` est ce qui
// rend la recherche utile (« qui tient la roukerie ? »), et c'est déjà ce que
// le rail affiche.
//
// LES MORTS N'Y SONT PAS, comme dans `/gens`. Ce n'est pas de la pudeur : un
// mort dont la nouvelle n'a pas voyagé se signalerait par son absence même, et
// l'absence est une réponse. Il reste dans le fil, qui le nomme.
//
// La dernière position CONNUE vient de `etat/joueurs/<siège>/vues.json` — la
// croyance du joueur, jamais `personnages.lieu_id` —, et elle VIEILLIT : au
// bout de quarante-cinq jours elle sort de la vue au lieu de mentir.
function gens(siege, va) {
  const persos = lire("personnages.json", []) || [];
  const maisons = {};
  (lire("maisons.json", []) || []).forEach((m) => { maisons[m.id] = m; });
  const lieux = {};
  (lire("lieux.json", []) || []).forEach((l) => { lieux[l.id] = l; });
  const monde = lire("monde.json", {}) || {};
  const aujourdhui = jourAbsolu(monde.date);
  const vues = new Map();
  if (siege && siege.personnage_id) {
    let d = {};
    try {
      d = JSON.parse(fs.readFileSync(path.join(ETAT, "joueurs",
        siege.personnage_id, "vues.json"), "utf-8"));
    } catch (e) { d = {}; }
    (d.vues || []).forEach((v) => {
      if (v && v.personnage_id) vues.set(v.personnage_id, v);
    });
  }
  return persos
    .filter((p) => p && p.etat !== "mort" &&
                   va([p.nom, p.titre].filter(Boolean).join(" · ")))
    .map((p) => {
      const m = maisons[p.maison_id] || null;
      const v = vues.get(p.id);
      let vu = null;
      if (v && aujourdhui !== null) {
        const age = aujourdhui - (jourAbsolu(v.date) || 0);
        const degre = vieillir(v.certitude || "sure", age);
        if (degre) {
          vu = { lieu: (lieux[v.lieu_id] && lieux[v.lieu_id].nom) || v.lieu_id,
                 quand: AGE_DIT(age), source: v.source || null,
                 certitude: degre };
        }
      }
      return { id: p.id, nom: nu(p.nom), titre: nu(p.titre) || null,
               maison: (m && nu(m.nom)) || null, vu };
    });
}

// DEUX PAR CAHIER AVANT D'EN REPRENDRE UN TROISIÈME. Huit résultats pris dans
// l'ordre venaient tous du même volume : le plus fourni gagnait toujours, et la
// recherche jurait que la chose n'était écrite qu'à un endroit. On sert donc
// large d'abord, profond ensuite — le reste suit si la place le permet.
function repartir(trouves, plafond, cle) {
  const compte = new Map();
  const large = [], profond = [];
  trouves.forEach((t) => {
    const k = cle(t);
    const n = compte.get(k) || 0;
    if (n < 2) { compte.set(k, n + 1); large.push(t); } else profond.push(t);
  });
  return large.concat(profond).slice(0, plafond);
}

// ---- ce qui sort ----------------------------------------------------------
function nomsDeTous() {
  const noms = new Map();
  (lire("personnages.json", []) || []).forEach((p) => {
    if (p && p.id) noms.set(p.id, nu(p.nom) || p.id);
  });
  return noms;
}

function volumesDuSiege(siege, moi) {
  let tous = [];
  try { tous = bibliotheque.charger(RACINE) || []; } catch (e) { tous = []; }
  const { liste } = volumesVisibles(tous, moi);
  // Les coffrets de chambre (modèle habitant) : des volumes assemblés à la
  // volée, servis par `/books` et donc ouvrables. Ce que l'étagère montre, la
  // recherche doit le trouver — sinon elle jure qu'une chose n'existe pas
  // alors qu'elle est à deux gestes.
  let ch = [];
  try {
    ch = (require("../agents").chambreLivres.coffretsChambre(siege, moi) || {}).books || [];
  } catch (e) { ch = []; }
  return liste.concat(ch);
}

// `q` peut être une ADRESSE : « 44022 » ne se cherche pas comme un mot, il se
// résout. C'est le geste de qui relit une réplique et veut savoir de quoi elle
// parlait — la ligne d'abord, et les endroits du fil qui l'ont citée.
function chercher({ q, siege, moi, max } = {}) {
  const besoin = String(q == null ? "" : q).trim();
  const plafond = Math.max(1, Math.min(40, max || PAR_FAMILLE));
  if (besoin.length < 2) {
    return { q: besoin, adresse: null, affaires: [], fils: [], fil: [], gens: [],
             combien: { affaires: 0, fils: 0, fil: 0, gens: 0 } };
  }
  const adresse = /^\d{4,6}$/.test(besoin) ? besoin : null;
  const va = tamis(besoin);
  const mots = plat(besoin).split(/\s+/).filter(Boolean);
  const noms = nomsDeTous();
  const tout = {
    affaires: cahiers(volumesDuSiege(siege, moi), va, adresse, mots),
    fils: adresse ? [] : fils(siege && siege.personnage_id, va, noms),
    fil: fil(fluxDuSiege(siege), va, noms, mots),
    gens: adresse ? [] : gens(siege, va),
  };
  const rendu = { q: besoin, adresse, combien: {} };
  Object.keys(tout).forEach((k) => {
    rendu.combien[k] = tout[k].length;
    rendu[k] = k === "affaires"
      ? repartir(tout[k], plafond, (t) => t.livre)
      : tout[k].slice(0, plafond);
  });
  return rendu;
}

// « Montre-moi ce moment » : la tranche de fil autour d'un résultat, lue avec
// le même œil que la recherche l'a rendue. On ne passe PAS par
// `/regie/extrait`, qui sert le fichier brut à la régie : un siège de joueur y
// demanderait n'importe quel intervalle, et le brouillard tomberait par la
// porte de derrière.
function autour({ i, marge, siege } = {}) {
  const items = fluxDuSiege(siege);
  const noms = nomsDeTous();
  const ctx = courants(items);
  const centre = Math.max(0, Math.min(i | 0, items.length ? items.length - 1 : 0));
  const m = Math.max(1, Math.min(30, marge || MARGE));
  const de = Math.max(0, centre - Math.ceil(m / 2));
  const a = Math.min(items.length, centre + m + 1);
  return { i: centre, de, a, total: items.length,
    items: items.slice(de, a).map((it, k) => {
      const qui = it.locuteur_id || it.acteur_id || null;
      return { _i: de + k, _centre: de + k === centre, type: it.type,
        date: ctx[de + k].date, lieu: ctx[de + k].lieu || null,
        qui, nom: (qui && (noms.get(qui) || qui)) || null,
        titre: it.titre || null, texte: it.texte || "" };
    }) };
}

module.exports = { chercher, autour };
