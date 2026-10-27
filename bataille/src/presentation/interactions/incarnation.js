/**
 * 🖥️ Interactions / Incarnation — ZQSD + F : LE joueur DANS un homme.
 *
 * Le toggle du menu fait apparaître un homme au centre de la vue ; tant qu'on
 * l'incarne, les touches le font marcher (ZQSD, WASD, flèches — en repère
 * ÉCRAN : Z va vers le haut de l'image, quel que soit son cap), F frappe
 * l'ennemi le plus proche à portée, et un clic gauche sur un ennemi le frappe
 * lui. Rien d'autre n'est touché : son cap reste l'arbitrage du moteur
 * (🧠 orientation), sa peur, sa voix, son souffle sont les siens.
 *
 * Tout passe par `conduite.piloter(id, intention)` — le même levier que le
 * clic droit ; on n'ouvre pas de seconde porte dans la tête de l'homme.
 */

import { marcher, frapper, attendre } from '../../cognition/intentions.js';

const TOUCHES = {
  KeyW: 'haut', KeyZ: 'haut', ArrowUp: 'haut',
  KeyS: 'bas', ArrowDown: 'bas',
  KeyA: 'gauche', KeyQ: 'gauche', ArrowLeft: 'gauche',
  KeyD: 'droite', ArrowRight: 'droite',
};

/**
 * @param {Object} deps
 * @param {HTMLCanvasElement} deps.canvas
 * @param {ReturnType<import('../camera.js').creerCamera>} deps.camera
 * @param {(posMonde) => number|null} deps.corpsSous — hit-test
 * @param {Object} deps.conduite — le levier (main.js) :
 *   apparaitre(pos) → id|null, commandants() → [{id, pos}], relacher(id), piloter(id, intention),
 *   estVivant(id), estEnnemi(id, autre), ennemiLePlusProche(id, porteeM),
 *   porteeDe(id) → m, periodeCoupMs(id)
 * @param {(id: number|null) => void} deps.surChangement — qui l'on est (null = personne)
 */
export function brancherIncarnation({ canvas, camera, corpsSous, conduite, surChangement }) {
  let id = null;
  const tenues = new Set();
  let frappe = null; // {cible, jusqua} — le geste en cours, en ms temps réel

  const estChampTexte = (ev) => /^(INPUT|TEXTAREA|SELECT)$/.test(ev.target?.tagName ?? '');

  const frapperCible = (cible) => {
    if (cible == null || cible === id) return;
    frappe = { cible, jusqua: performance.now() + conduite.periodeCoupMs(id) };
  };

  window.addEventListener('keydown', (ev) => {
    if (id == null || estChampTexte(ev)) return;
    if (TOUCHES[ev.code]) {
      tenues.add(TOUCHES[ev.code]);
      ev.preventDefault();
      return;
    }
    if (ev.code === 'KeyF') {
      frapperCible(conduite.ennemiLePlusProche(id, conduite.porteeDe(id) + 1.5));
      ev.preventDefault();
    }
  });
  window.addEventListener('keyup', (ev) => {
    if (TOUCHES[ev.code]) tenues.delete(TOUCHES[ev.code]);
  });
  window.addEventListener('blur', () => tenues.clear());

  // le clic gauche sur un ennemi : un coup vers lui (la sélection garde le
  // clic dans le vide et sur les siens)
  let depart = null;
  canvas.addEventListener('pointerdown', (ev) => {
    if (ev.button === 0) depart = { x: ev.clientX, y: ev.clientY };
  });
  canvas.addEventListener('pointerup', (ev) => {
    if (id == null || !depart) {
      depart = null;
      return;
    }
    const d = Math.hypot(ev.clientX - depart.x, ev.clientY - depart.y);
    depart = null;
    if (d > 4) return;
    const r = canvas.getBoundingClientRect();
    const touche = corpsSous(camera.versMonde({ x: ev.clientX - r.left, y: ev.clientY - r.top }));
    if (touche != null && conduite.estEnnemi(id, touche)) frapperCible(touche);
  });

  /** La direction voulue, en MÈTRES MONDE, depuis les touches (repère écran). */
  const directionMonde = () => {
    let ex = 0;
    let ey = 0;
    if (tenues.has('haut')) ey -= 1;
    if (tenues.has('bas')) ey += 1;
    if (tenues.has('gauche')) ex -= 1;
    if (tenues.has('droite')) ex += 1;
    if (!ex && !ey) return null;
    const o = camera.versMonde({ x: 0, y: 0 });
    const p = camera.versMonde({ x: ex, y: ey });
    const dx = p.x - o.x;
    const dy = p.y - o.y;
    const n = Math.hypot(dx, dy) || 1;
    return { x: dx / n, y: dy / n };
  };

  const api = {
    /** Qui l'on est (null = personne). */
    id: () => id,

    /** Entrer : un homme apparaît là, et l'on est lui. */
    entrer(pos) {
      if (id != null) return id;
      id = conduite.apparaitre(pos);
      if (id != null) surChangement(id);
      return id;
    },

    /**
     * Entrer DANS un homme qui existe déjà — un commandant : sa tête reste la
     * sienne (l'état-major délibère et crie toujours), on n'a que ses jambes
     * et son bras. Si l'on était quelqu'un, on le rend d'abord.
     */
    entrerDans(idCible) {
      if (idCible == null || !conduite.estVivant(idCible)) return null;
      if (id != null) api.sortir();
      id = idCible;
      surChangement(id);
      return id;
    },

    /** Sortir : il reste dans le monde, rendu à sa tête. */
    sortir() {
      if (id == null) return;
      conduite.relacher(id);
      id = null;
      tenues.clear();
      frappe = null;
      surChangement(null);
    },

    /** À chaque image : la main sur lui, tant qu'il vit. */
    tick() {
      if (id == null) return;
      if (!conduite.estVivant(id)) {
        api.sortir();
        return;
      }
      const dir = directionMonde();
      if (dir) {
        frappe = null;
        conduite.piloter(id, marcher(dir));
        return;
      }
      if (frappe) {
        if (performance.now() < frappe.jusqua && conduite.estVivant(frappe.cible)) {
          conduite.piloter(id, frapper(frappe.cible));
          return;
        }
        frappe = null;
      }
      conduite.piloter(id, attendre());
    },
  };
  return api;
}
