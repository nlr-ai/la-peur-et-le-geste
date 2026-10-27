// statut.js — le battement du MJ.
//
// Quand le MJ calcule, il lit l'état, dépêche un homme et attend sa journée :
// l'écran resterait muet des minutes entières. scripts/agents/battement_mj.py
// pousse alors, par minute de silence, un item `statut` hors fiction — depuis
// combien de temps le MJ travaille, quels hommes sont dehors. Ce n'est ni un
// geste ni une parole : aucun PNJ n'y dit rien.
//
// UNE seule ligne vivante : tant que rien d'autre n'est tombé dessous, le
// battement suivant la réécrit sur place. Au rechargement on ne la rejoue
// pas — c'était de l'attente, pas de l'histoire.
"use strict";
(() => {
  let vivant = null;
  Bus.enregistrer("statut", (it, ctx) => {
    if (ctx && ctx.instant) return;
    const zone = document.getElementById("fil-corps");
    if (vivant && zone && zone.lastElementChild === vivant) {
      const t = vivant.querySelector(".chr-texte");
      if (t) { t.textContent = it.texte; return; }
    }
    vivant = Bus.chronique("chr-statut", "Le monde travaille", it.texte);
  });
})();
