// Dépôt documentaire réservé au monde scientifique. Aucun contenu n'est exécuté.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { envoyer, qui, RACINE, DEPOT } = require('../http');
const racines = require('../racines');
const MAX = 20 * 1024 * 1024;
const dossier = path.join(RACINE, 'recherche', 'fichiers');
const fail = (res, code, erreur) => envoyer(res, code, JSON.stringify({ erreur }));
module.exports = function(req, res, url) {
  if (!url.startsWith('/recherche-fichiers')) return false;
  if (racines.courant() !== 'frontieres-du-vivant') return fail(res, 404, 'Indisponible dans ce monde.');
  const joueur = qui(req, req.url);
  if (!joueur || !['infection', 'immunite'].includes(joueur.personnage_id)) return fail(res, 401, 'Ouvrez un siège joueur.');
  if (req.method === 'GET' && url === '/recherche-fichiers/ui.js') {
    return envoyer(res, 200, fs.readFileSync(path.join(DEPOT, 'ecrans', 'recherche-fichiers.js')), 'text/javascript; charset=utf-8');
  }
  if (req.method === 'GET' && url === '/recherche-fichiers') {
    try {
      const fichiers = fs.existsSync(dossier) ? fs.readdirSync(dossier).filter(n => /^[a-f0-9-]{36}\.json$/.test(n)).map(n => JSON.parse(fs.readFileSync(path.join(dossier, n), 'utf8'))).sort((a,b) => b.date.localeCompare(a.date)) : [];
      return envoyer(res, 200, JSON.stringify({ fichiers }));
    } catch { return fail(res, 500, 'Lecture des fichiers impossible.'); }
  }
  const match = /^\/recherche-fichiers\/([a-f0-9-]{36})$/.exec(url);
  if (req.method === 'GET' && match) {
    try {
      const meta = JSON.parse(fs.readFileSync(path.join(dossier, match[1] + '.json'), 'utf8'));
      return envoyer(res, 200, fs.readFileSync(path.join(dossier, match[1] + '.bin')), 'application/octet-stream', {
        'Content-Disposition': "attachment; filename*=UTF-8''" + encodeURIComponent(meta.nom),
        'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "sandbox; default-src 'none'"
      });
    } catch { return fail(res, 404, 'Fichier introuvable.'); }
  }
  if (req.method === 'POST' && url === '/recherche-fichiers') {
    // Le corps est le fichier brut ; un en-tête dédié empêche les formulaires intersites.
    if (req.headers['x-recherche-upload'] !== '1') return fail(res, 403, 'Envoi non autorisé.');
    if (req.headers.origin) {
      try { if (new URL(req.headers.origin).host !== req.headers.host) return fail(res, 403, 'Origine non autorisée.'); }
      catch { return fail(res, 403, 'Origine invalide.'); }
    }
    let nom;
    try { nom = decodeURIComponent(req.headers['x-fichier-nom'] || ''); } catch { return fail(res, 400, 'Nom invalide.'); }
    nom = nom.split(/[\\/]/).pop().replace(/[\x00-\x1f\x7f]/g, '').slice(0, 180).trim();
    if (!nom) return fail(res, 400, 'Nom requis.');
    if (Number(req.headers['content-length']) > MAX) return fail(res, 413, 'Limite : 20 Mo par fichier.');
    let taille = 0, chunks = [], refuse = false;
    req.on('data', chunk => {
      if (refuse) return;
      taille += chunk.length;
      if (taille > MAX) { refuse = true; chunks = []; fail(res, 413, 'Limite : 20 Mo par fichier.'); return; }
      chunks.push(chunk);
    });
    req.on('error', () => { refuse = true; chunks = []; if (!res.writableEnded) fail(res, 400, 'Envoi interrompu.'); });
    req.on('end', () => {
      if (refuse) return;
      const id = crypto.randomUUID();
      try {
        const contenu = Buffer.concat(chunks);
        const meta = { id, nom, taille, date: new Date().toISOString(), auteur: joueur.personnage_id, statut: 'à vérifier', sha256: crypto.createHash('sha256').update(contenu).digest('hex') };
        fs.mkdirSync(dossier, { recursive: true });
        fs.writeFileSync(path.join(dossier, id + '.bin'), contenu, { flag: 'wx' });
        fs.writeFileSync(path.join(dossier, id + '.json'), JSON.stringify(meta, null, 2), { flag: 'wx' });
        return envoyer(res, 201, JSON.stringify(meta));
      } catch { fs.rmSync(path.join(dossier, id + '.bin'), { force: true }); return fail(res, 500, 'Le fichier n’a pas pu être enregistré.'); }
    });
    return;
  }
  return fail(res, 404, 'Route inconnue.');
};
