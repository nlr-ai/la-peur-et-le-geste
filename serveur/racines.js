// RACINES — ou vit l'etat, et de quel monde il est. Le jumeau exact de
// `scripts/noyau/racines.py`, aux memes variables et aux memes mots.
//
// POURQUOI DEUX IMPLEMENTATIONS, ET POURQUOI CE N'EST PAS UNE FAUTE.
// Le depot execute son monde dans deux langues : le hors-scene et les agents en
// Python, le service de la scene en Node. Aucune ne peut appeler l'autre pour
// savoir ou lire — ce serait un `spawn` de plus a chaque requete, sur le chemin
// le plus chaud du serveur. Elles doivent donc TOMBER SUR LE MEME DOSSIER par
// construction, et c'est ce que ce fichier promet : memes variables, meme
// ordre, memes defauts. Le precedent est dans le depot et il a deja coute :
// `noyau/diffusion.py` et `serveur/domaine/regie.js` lisent un seul
// `diffusion.json` PARCE QUE les deux implementations avaient silencieusement
// diverge. Ici, l'enjeu est plus grave qu'une constante : deux racines qui ne
// s'accordent pas, c'est le brouillard d'un monde servi dans un autre.
//
// L'ORDRE, ET POURQUOI DANS CE SENS.
//   1. CONSEIL_RACINE — un chemin absolu qui CONTIENT `etat/`. C'est ce que les
//      tests du serveur emploient depuis toujours pour monter une partie
//      miniature dans un dossier temporaire ; on ne change pas ce contrat.
//   2. CONSEIL_MONDE — un id de paquet sous `mondes/`.
//   3. Rien — la disposition heritee : `etat/` a la racine du depot. C'est le
//      defaut, et il est identique a l'octet pres a ce qui existait avant ce
//      fichier. Rien ne bouge tant que personne ne nomme un monde.
//
// CE QU'IL NE FAIT PAS ENCORE. Il resout au CHARGEMENT du module, comme
// `contexte.js` le faisait. Un menu qui bascule de monde a chaud (lot 6) demande
// une resolution PAR REQUETE, donc que les lectures de routes passent toutes par
// la porte de `contexte.js` au lieu de rouvrir les fichiers elles-memes. La
// fonction `racine(monde)` prend deja son argument pour ce jour-la.
"use strict";
const fs = require("fs");
const path = require("path");

// La racine du DEPOT — la seule deduction legitime depuis l'emplacement du
// fichier : le code est la ou le code est. serveur/racines.js -> serveur -> .
const DEPOT = path.join(__dirname, "..");
const MONDES = path.join(DEPOT, "mondes");

// Un monde nomme qui n'existe pas ARRETE le serveur, et ne se rabat sur rien.
// Meme raison que le refus de se rabattre sur un autre port : « deux parties
// ouvertes en meme temps et une salle qui parle en double. On prefere mourir. »
// Servir en silence l'etat du monde d'a cote parce qu'on a mal tape son nom est
// la meme faute, en pire : elle ne se voit pas.
// LE MONDE SE NOMME A LA LIGNE DE COMMANDE AUSSI (9.9). `CONSEIL_MONDE` reste le
// contrat — c'est lui que le Python lit, et les deux langues doivent s'accorder.
// Mais lancer un monde ne peut pas demander de poser une variable a la main :
// `.claude/launch.json` ne declare que l'executable, ses arguments et un port.
// On accepte donc `--monde <id>` (ou `--monde=<id>`), et on le REPOSE dans
// l'environnement, pour que tout ce que le serveur lance ensuite — les scripts
// Python detaches, le routeur, la porte des tables — herite du meme monde. Sans
// ce report, le serveur servirait un monde et ses sous-processus un autre.
function _duCommande() {
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i += 1) {
    if (a[i] === "--monde" && a[i + 1]) return a[i + 1].trim();
    const m = /^--monde=(.+)$/.exec(a[i]);
    if (m) return m[1].trim();
  }
  return null;
}
const _ARG = _duCommande();
if (_ARG && !process.env.CONSEIL_MONDE) process.env.CONSEIL_MONDE = _ARG;

function courant() {
  return (process.env.CONSEIL_MONDE || "").trim() || _ARG || null;
}

function mondes(tous) {
  let noms;
  try { noms = fs.readdirSync(MONDES); } catch (e) { return []; }
  return noms.filter((n) => {
    if (n.startsWith(".")) return false;
    if (!tous && n.startsWith("_")) return false;
    try { return fs.statSync(path.join(MONDES, n)).isDirectory(); } catch (e) { return false; }
  }).sort();
}

// Le dossier qui CONTIENT `etat/`. `monde` non fourni : celui de
// l'environnement. `monde === null` : la disposition heritee, quoi que dise
// l'environnement — ce dont une migration a besoin pour lire l'ancien monde
// pendant qu'elle ecrit le neuf.
function racine(monde) {
  const explicite = arguments.length > 0;
  if (!explicite && process.env.CONSEIL_RACINE) {
    return path.resolve(process.env.CONSEIL_RACINE);
  }
  const m = explicite ? monde : courant();
  if (!m) return DEPOT;
  const p = path.join(MONDES, m);
  let bon = false;
  try { bon = fs.statSync(p).isDirectory(); } catch (e) { bon = false; }
  if (!bon) {
    throw new Error("monde inconnu : " + m + " (" + p + " n'existe pas)\n"
      + "Mondes disponibles : " + (mondes(true).join(", ") || "aucun"));
  }
  return p;
}

function etat(monde) {
  return path.join(arguments.length ? racine(monde) : racine(), "etat");
}

function chambres(monde) {
  return path.join(arguments.length ? racine(monde) : racine(), "chambres");
}

// Ce que le monde declare de lui-meme : calendrier, monnaie, titres, genres
// d'unites, canaux, offices, signes, lieu de depart. Absent en disposition
// heritee, ou ces valeurs sont encore en dur dans le code — le lot 4 les fait
// descendre ici, une famille a la fois.
function manifeste(monde) {
  const p = path.join(arguments.length ? racine(monde) : racine(), "manifeste.json");
  try { return JSON.parse(fs.readFileSync(p, "utf-8")); } catch (e) { return {}; }
}

module.exports = { DEPOT, MONDES, courant, mondes, racine, etat, chambres, manifeste };
