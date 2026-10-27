// Un bureau appartient au paquet recu ; aucun nom d'univers n'est code ici.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { spawn } = require("node:child_process");

function creerBureau(racine, depot, options = {}) {
  const lire = p => JSON.parse(fs.readFileSync(path.join(racine, p), "utf8").replace(/^\uFEFF/, ""));
  const manifeste = lire("manifeste.json");
  if (manifeste.interface !== "bureau") throw new Error("Ce paquet ne declare pas de bureau.");
  const profils = lire("etat/personnages.json");
  const plan = lire("plans/bureau.json");
  const parId = new Map(profils.map(p => [p.id, p]));
  if (parId.size !== profils.length || plan.salles.length !== profils.length
      || new Set(plan.salles.map(s => s.agent_id)).size !== profils.length
      || plan.salles.some(s => !parId.has(s.agent_id))) throw new Error("Une salle distincte par profil est requise.");
  const runtime = path.join(racine, ".runtime", "bureau");
  fs.mkdirSync(runtime, { recursive: true });
  const filPath = path.join(racine, "etat", "bureau-fil.jsonl");
  const fil = fs.readFileSync(filPath, "utf8").split(/\r?\n/).filter(x => x.trim()).map(x => JSON.parse(x));
  const actifs = new Map();
  const attente = [];
  const cles = new Map(fil.filter(e => e.type === "message_envoye").map(e => [e.requete_id, e]));
  const secret = crypto.randomUUID();
  let adresse = null;
  let ferme = false;
  const max = Math.max(1, Math.min(8, manifeste.runtime?.concurrence || 2));
  const lancer = options.spawn || spawn;

  function ajouter(type, champs = {}) {
    const e = { ...champs, id: crypto.randomUUID(), numero: fil.length + 1, type, heure: new Date().toISOString() };
    fs.appendFileSync(filPath, JSON.stringify(e) + "\n");
    fil.push(e);
    return e;
  }
  // Les requetes precedentes restent visibles, mais ne sont jamais rejouees en aveugle.
  const termines = new Set(fil.filter(e => ["termine", "erreur", "interrompu"].includes(e.type)).map(e => e.requete_id));
  for (const e of [...cles.values()]) {
    if (!termines.has(e.requete_id)) ajouter("interrompu", { agent_id: e.a, requete_id: e.requete_id,
      texte: "La session precedente n'a pas de fin attestee. Relance manuelle necessaire." });
  }

  function etat(apres = 0) {
    return { manifeste, plan, profils: profils.map(p => ({ ...p,
      statut: actifs.has(p.id) ? "travaille" : attente.some(x => x.a === p.id) ? "attente" : "disponible" })),
      fil: fil.filter(e => e.numero > apres).slice(-300), total: fil.length,
      actifs: actifs.size, en_attente: attente.length };
  }

  function deposer({ a, texte, requete_id, de = "operateur", profondeur = 0 }) {
    if (!parId.has(a)) throw new Error("Destinataire inconnu dans ce bureau.");
    if (de !== "operateur" && !parId.has(de)) throw new Error("Expediteur inconnu.");
    if (typeof texte !== "string" || !texte.trim() || texte.length > 12000) throw new Error("Le message doit contenir entre 1 et 12000 caracteres.");
    if (!/^[a-zA-Z0-9-]{12,80}$/.test(requete_id || "")) throw new Error("Identifiant de message invalide.");
    if (profondeur > 3) throw new Error("Cette chaine a deja trois transmissions. Conclus pour l'operateur avant de poursuivre.");
    const deja = cles.get(requete_id);
    if (deja) {
      if (deja.a !== a || deja.de !== de || deja.texte !== texte.trim()) throw new Error("Identifiant deja utilise pour un autre message.");
      return { message: deja, doublon: true };
    }
    const message = ajouter("message_envoye", { de, a, agent_id: de === "operateur" ? a : de,
      texte: texte.trim(), requete_id, profondeur });
    cles.set(requete_id, message);
    attente.push(message);
    setImmediate(avancer);
    return { message, doublon: false };
  }

  function avancer() {
    if (ferme) return;
    while (actifs.size < max) {
      const index = attente.findIndex(x => !actifs.has(x.a));
      if (index < 0) return;
      const message = attente.splice(index, 1)[0];
      demarrer(message);
    }
  }

  function demarrer(message) {
    const id = message.a;
    const requete = path.join(runtime, message.requete_id + ".json");
    fs.writeFileSync(requete, JSON.stringify({ racine, agent_id: id, message, historique: fil.filter(e =>
      e.agent_id === id || e.a === id || e.de === id).slice(-40) }));
    let enfant;
    try {
      enfant = lancer(process.env.PYTHON || "python", [path.join(depot, "scripts", "bureau.py"), "executer", requete], {
        cwd: depot, windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
        env: { ...process.env, CONSEIL_RACINE: racine, CONSEIL_MONDE: manifeste.id,
          BUREAU_URL: adresse || "", BUREAU_SECRET: secret, BUREAU_AGENT: id,
          BUREAU_PROFONDEUR: String(message.profondeur || 0) },
      });
    } catch (e) {
      ajouter("erreur", { agent_id: id, requete_id: message.requete_id, texte: e.message });
      return;
    }
    actifs.set(id, { enfant, message });
    ajouter("message_recu", { agent_id: id, de: message.de, a: id, texte: message.texte, requete_id: message.requete_id });
    ajouter("demarre", { agent_id: id, requete_id: message.requete_id, texte: "Session en cours" });
    let tampon = "", erreur = "", derniere = null, final = false;
    const sauver = (type, data) => ajouter(type, { ...data, agent_id: id, requete_id: message.requete_id });
    const ligne = brut => {
      let e;
      try { e = JSON.parse(brut); } catch { return; }
      if (e.type === "intermediaire" && typeof e.texte === "string" && e.texte.trim()) {
        derniere = sauver("intermediaire", { texte: e.texte.slice(0, 16000) });
      } else if (e.type === "activite") {
        sauver("activite", { texte: String(e.texte || "Travail en cours").slice(0, 300) });
      } else if (e.type === "final" && typeof e.texte === "string" && e.texte.trim()) {
        final = true;
        // La derniere parole peut etre la reponse finale : la marquer sans la dupliquer.
        sauver("reponse_finale", { texte: e.texte.slice(0, 30000), remplace: derniere?.texte === e.texte ? derniere.id : null });
      } else if (e.type === "erreur") erreur = String(e.texte || "Erreur de session").slice(0, 1500);
    };
    enfant.stdout.setEncoding("utf8");
    enfant.stdout.on("data", chunk => {
      tampon += chunk;
      const lignes = tampon.split("\n");
      tampon = lignes.pop();
      for (const l of lignes) ligne(l);
    });
    enfant.stderr.setEncoding("utf8");
    enfant.stderr.on("data", chunk => { erreur = (erreur + chunk).slice(-1500); });
    enfant.on("error", e => { erreur = e.message; });
    enfant.on("close", code => {
      if (tampon) ligne(tampon);
      sauver(final && code === 0 ? "termine" : "erreur", {
        texte: final && code === 0 ? "Session terminee" : erreur || `Session arretee sans reponse finale (code ${code}).`,
      });
      actifs.delete(id);
      avancer();
    });
  }

  function transmettre(secretRecu, agent, contenu) {
    if (secretRecu !== secret || !actifs.has(agent)) throw new Error("Session d'envoi non reconnue.");
    return deposer({ ...contenu, de: agent,
      profondeur: (actifs.get(agent).message.profondeur || 0) + 1 });
  }

  return { etat, deposer, transmettre, definirAdresse: url => { adresse = url; },
    fermer: () => { ferme = true; }, actifs };
}
module.exports = { creerBureau };
