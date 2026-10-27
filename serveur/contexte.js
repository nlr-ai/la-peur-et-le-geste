// Le socle : la racine du dépôt, le port, la fenêtre de fil, et les chemins de
// l'état — où lire les croyances d'un siège, son heure, ses notes. Rien qui
// connaisse `req` ou `res` : le transport est dans http.js, le brouillard dans
// siege.js.

// Les tests d'intégration servent une partie miniature dans un dossier
// temporaire. En production, l'absence de variable garde le dépôt courant.

const fs = require("fs");
const path = require("path");
const childProcess = require("child_process");

const racines = require("./racines");

// DEUX RACINES, ET IL FAUT LES DISTINGUER (9.9).
//
// `RACINE` designait tout : `etat/` et `chambres/` (le MONDE), mais aussi
// `scripts/*.py`, `ecrans/` et `monde/` (le DEPOT). Tant qu'il n'y avait qu'un
// monde a la racine du depot, les deux etaient le meme dossier et la confusion
// ne coutait rien. Elle coute des le premier `CONSEIL_MONDE` : servir `jeu.html`
// depuis `mondes/venise/ecrans/` ne trouve rien.
//
// La confusion est d'ailleurs DEJA payee, en silence, par les tests : ils
// pointent `CONSEIL_RACINE` sur un dossier temporaire qui ne contient que
// `etat/` et `chambres/`, et le serveur y cherche pourtant `scripts/presence.py`
// et `ecrans/`. Ces chemins-la sont faux depuis toujours ; ils ne se voient pas
// parce que les epreuves n'empruntent pas ces branches.
//
//   DEPOT    — le code, les ecrans, les scripts, les artefacts 3D. Immuable.
//   RACINE   — le monde courant : le dossier qui CONTIENT `etat/`.
//   ETAT, CHAMBRES — les deux dossiers du monde, nommes pour qu'on cesse de les
//                    recomposer a la main a vingt endroits.
//
// `RACINE` garde son nom et son sens de monde : c'est ce que les vingt et une
// routes en attendent aujourd'hui. Ce qui reste a faire est nomme et compte —
// migrer vers `DEPOT` les usages qui visent le code (voir `--racines` de
// `scripts/verifier.mjs`) ; ce compte ne doit que descendre.
const DEPOT = racines.DEPOT;
const RACINE = racines.racine();
const ETAT = racines.etat();
const CHAMBRES = racines.chambres();

// 3129 est le port du jeu. Un atelier (vérification d'écran pendant qu'une
// partie tourne) passe un port en argument ou par PORT, pour ne pas se
// disputer le port de la partie en cours.
const PORT = Number(process.argv[2]) || Number(process.env.PORT) || 3129;

// Longueur d'une fenêtre de fil servie au navigateur. Le reste du passé se
// réclame page par page (`/scene?avant=N`) quand le joueur remonte la
// chronique. Le fichier, lui, garde tout — c'est la mémoire de la partie.
//
// 500 était trop : rien n'est perdu, mais tout est MONTÉ. Cinq cents entrées
// font autant de nœuds vivants dans la chronique, avec leurs vieillissements
// et leurs survols, et le défilement se paie à chaque image.
//
// 80 est calé sur la SCÈNE et non sur la session : un conseil fait une
// quarantaine de répliques, donc la fenêtre porte celle qu'on joue et celle
// d'avant. Ce qui précède est du passé qu'on relit, et il redescend tout seul
// quand on remonte (`/scene?avant=N`). Descendre plus bas ferait paginer à
// l'intérieur d'une même scène — c'est là qu'est la limite, pas dans le coût.
const MAX_FIL = 80;

// ---- les croyances, une par joueur --------------------------------------
// `vues`, `jetons`, `objectifs` ne décrivent pas le monde : ils décrivent ce
// qu'UN joueur croit du monde. À deux, les partager revient à donner la table
// de guerre de la reine à sa maîtresse de la voix. Chacun a donc son dossier —
// `etat/joueurs/<personnage_id>/` — et l'on retombe sur `etat/` quand il existe
// encore : une partie seule ne voit aucune différence.
//
// Le repli racine peut être absent (archivé une fois les deux joueuses
// migrées) : on rend alors null plutôt qu'un chemin qui n'ouvre rien. Un
// visiteur sans jeton n'a AUCUNE croyance à lui — il ne doit pas hériter de
// celles d'autrui, et une table vide est la seule réponse honnête.
function cheminEtat(nom, siege) {
  if (siege) {
    const p = path.join(ETAT, "joueurs", siege.personnage_id, nom);
    if (fs.existsSync(p)) return p;
  }
  const racineNom = path.join(ETAT, nom);
  return fs.existsSync(racineNom) ? racineNom : null;
}

// Les notes du joueur — un carnet HORS FICTION. Ce n'est pas un livre du monde
// et ce n'est pas une croyance : personne dans la salle ne l'écrit, aucun PNJ
// ne le lit, le MJ n'y touche pas. Du texte brut, gardé tel quel, un fichier
// par siège — ce que la reine griffonne n'est pas ce que griffonne sa
// maîtresse de la voix. Contrairement à `cheminEtat`, on rend le chemin où le
// fichier DEVRA s'écrire, même s'il n'existe pas encore.
function cheminNotes(siege) {
  return siege
    ? path.join(ETAT, "joueurs", siege.personnage_id, "notes.txt")
    : path.join(ETAT, "notes.txt");
}

// Les croyances du demandeur, ou le défaut fourni quand il n'en a pas.
function lireCroyance(nom, siege, defaut) {
  const p = cheminEtat(nom, siege);
  if (!p) return defaut;
  try { return JSON.parse(fs.readFileSync(p, "utf-8")); } catch (e) { return defaut; }
}

// Les mesures sont possedees par les maisons mais la regie les montre comme
// un seul ensemble. Les ids restent globaux et un doublon est une faute.
function lireMainsMaisons() {
  let maisons = [];
  try {
    const brut = JSON.parse(fs.readFileSync(path.join(ETAT, "maisons.json"), "utf-8"));
    maisons = (Array.isArray(brut) ? brut : (brut.maisons || []))
      .map((m) => m && m.id).filter(Boolean);
  } catch (e) {}
  maisons.push("_sans-maison");
  const resultat = [], vus = new Set();
  maisons.forEach((maison) => {
    const fichier = path.join(ETAT, "maisons", maison,
      "documents", "mains.json");
    if (!fs.existsSync(fichier)) return;
    const brut = JSON.parse(fs.readFileSync(fichier, "utf-8"));
    if (!brut || brut.maison_id !== maison)
      throw new Error(fichier + " doit porter maison_id=" + maison);
    (brut.mains || []).forEach((main) => {
      if (!main || !main.id || vus.has(main.id))
        throw new Error("main absente ou en double : " + ((main && main.id) || "?"));
      vus.add(main.id);
      resultat.push(Object.assign({ maison_id: maison }, main));
    });
  });
  return resultat;
}

// L'heure de CE joueur. Le front de chacun vit dans `etat/horloges.json`
// (tenu par scripts/append_flux.py) ; `monde.date` n'est que le minimum des
// fronts — la date acquise pour tout le monde, celle du tick. Servir celle-là
// au navigateur ferait vieillir la carte d'un joueur au rythme du plus lent.
function dateDe(siege) {
  let monde = null;
  try { monde = JSON.parse(fs.readFileSync(path.join(ETAT, "monde.json"), "utf-8")).date || null; } catch (e) {}
  if (!siege) return monde;
  try {
    const h = JSON.parse(fs.readFileSync(path.join(ETAT, "horloges.json"), "utf-8"));
    if (h && h[siege.personnage_id]) return h[siege.personnage_id];
  } catch (e) {}
  return monde;
}

// OÙ EST TOUT LE MONDE, à cette minute-là — le calcul, pas le cache.
// `scripts/presence.py --json` fait le travail : routines, topologie, marche en
// cours. On ne le refait pas à chaque sonde (le navigateur en tire une toutes
// les quinze secondes, et par siège) : la réponse vaut tant que ni l'heure
// demandée ni les trois fichiers d'entrée n'ont bougé. Un échec rend null, et
// l'appelant retombe sur l'instantané figé — le jeu ne s'arrête pas pour ça.
let cachePresence = null;
function resoudrePresence(date) {
  if (!date) return null;
  let cle = [date.annee, date.lune, date.jour, date.minute].join(".");
  for (const f of ["presence.json", "routines.json", "chemins.json"]) {
    try { const s = fs.statSync(path.join(ETAT, f)); cle += "|" + s.mtimeMs; }
    catch (e) { cle += "|?"; }
  }
  if (cachePresence && cachePresence.cle === cle) return cachePresence.gens;
  let gens = null;
  try {
    gens = JSON.parse(childProcess.execFileSync("python",
      [path.join(DEPOT, "scripts", "presence.py"), "--json", "--quand", cle.split("|")[0]],
      { cwd: DEPOT, encoding: "utf-8", timeout: 20000,
        windowsHide: true, maxBuffer: 8 * 1024 * 1024,
        env: Object.assign({}, process.env, { PYTHONIOENCODING: "utf-8" }) })).gens || null;
  } catch (e) { gens = null; }
  cachePresence = { cle, gens };
  return gens;
}

module.exports = { RACINE, DEPOT, ETAT, CHAMBRES, PORT, MAX_FIL,
  cheminEtat, cheminNotes,
  lireCroyance, lireMainsMaisons, dateDe, resoudrePresence };
