// GET /scene — la fenêtre de flux servie au navigateur, triée par audience.
const fs = require("fs");
const path = require("path");
const { MAX_FIL, ETAT } = require("../http");
const { envoyer, inlinerFigure } = require("../http");
const { rafraichirPortraits } = require("../peinture").portraits; // LA PORTE serveur de peinture
const { ecartDe, filtrerFlux, qui } = require("../http");

function traiter(req, res, url) {
  if (req.method === "GET") {
    if (url === "/scene") {
      try {
        const brut = fs.readFileSync(path.join(ETAT, "flux.jsonl"), "utf-8");
        // Une ligne corrompue ne doit pas effacer toutes les scènes lisibles.
        // Les octets nuls seuls sont des blocs vides, jamais des items.
        let items = [];
        for (const [index, ligne] of brut.split("\n").entries()) {
          if (!ligne.replace(/\0/g, "").trim()) continue;
          try {
            const item = JSON.parse(ligne);
            if (item && typeof item === "object" && !Array.isArray(item)) items.push(item);
          } catch (e) {
            console.error("Flux illisible, ligne " + (index + 1) + " : " + e.message);
          }
        }
        // Le brouillard, à deux : un item peut porter `pour: "<personnage>"`
        // — une pensée, une question, un aparté. Il ne part qu'à celui-là.
        // Le tri se fait AVANT de descendre : ce qui n'est pas pour vous ne
        // rejoint jamais votre machine. Il vit dans `siege.js` depuis le 9.9,
        // parce que `/chercher` fouille le même fil et doit le lire du même
        // œil — voir `filtrerFlux`, et `test_siege.js` qui garde les deux.
        items = filtrerFlux(items, qui(req, url));
        // Le flux est append-only et ne cesse de grossir : au bout de
        // quelques heures de partie, chaque sondage retransmet des milliers
        // de lignes et le navigateur rejoue tout au rechargement. On ne sert
        // donc qu'une FENÊTRE. `debut` dit combien de lignes ont été coupées
        // en tête et `total` la longueur réelle du fil : le curseur du client
        // reste ainsi compté sur le flux entier — sinon la fenêtre glissant à
        // chaque nouvel item, le neuf ne serait jamais vu.
        //
        // `?avant=N` remonte le temps : la page qui précède l'index N, servie
        // quand le joueur fait défiler la chronique vers le haut. Le passé
        // descend alors par tranches, à la demande, et jamais d'un bloc.
        const total = items.length;
        const q = (req.url.split("?")[1] || "").match(/(?:^|&)avant=(\d+)/);
        let fin = q ? Math.min(Number(q[1]), total) : total;
        if (!(fin >= 0)) fin = total;
        const debut = Math.max(0, fin - MAX_FIL);
        items = items.slice(debut, fin);
        // Un volume montré en scène : sa page peut être un dessin. Le flux
        // n'en garde que le NOM — un levé pèse deux cent mille signes, et
        // trente lignes qui le portent feraient un fil illisible à charger.
        // Le nom est empreinté (voir append_flux.py) : la feuille de ce
        // jour-là ne bouge plus, même si le dessin est refait demain.
        items.forEach((it) => {
          if (it.montre && it.montre.extrait) inlinerFigure(it.montre.extrait);
          rafraichirPortraits(it);
        });
        return envoyer(res, 200, JSON.stringify({ items, debut, total, ecart: ecartDe(qui(req, url)) }));
      } catch (e) {
        return envoyer(res, 200, JSON.stringify({ items: [], debut: 0 }));
      }
    }
  }
  return false;
}

module.exports = traiter;
