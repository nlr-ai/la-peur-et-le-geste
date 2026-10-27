#!/usr/bin/env node
// -*- coding: utf-8 -*-
/**
 * FIL DEV — le fil commun de deux sessions de développement.
 *
 * Chaque session Claude Code publie, par son hook (.claude/hooks/fil-dev.js),
 * le prompt qu'on lui donne et la réponse qu'elle rend. Ce serveur les range
 * dans un fichier append-only et les sert à une page qui les déroule. Le
 * collègue y accède par un tunnel (cloudflared ou Tailscale) : voir LISEZMOI.md.
 *
 * IL N'ÉCOUTE QUE SUR 127.0.0.1. Le tunnel se branche localement ; rien d'autre
 * ne doit pouvoir l'atteindre. Et comme le tunnel, lui, est public, tout passe
 * par un jeton : sans lui, on n'est personne — ni pour lire, ni pour publier.
 *
 * Usage : node fil-dev/serveur.js [port]   (3300 par défaut)
 */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const PORT = Number(process.argv[2]) || 3300;
const ICI = __dirname;
const FIL = path.join(ICI, "fil.jsonl");
const FICHIER_JETON = path.join(ICI, "jeton.txt");
const PLAFOND_CORPS = 2 * 1024 * 1024;   // une réponse énorme reste une réponse, pas un déni de service

// Le jeton : l'environnement d'abord, sinon celui qu'on a déjà engendré,
// sinon un neuf qu'on garde pour la prochaine fois (jeton.txt est ignoré par git).
function jeton() {
  if (process.env.FIL_DEV_JETON) return process.env.FIL_DEV_JETON.trim();
  try { return fs.readFileSync(FICHIER_JETON, "utf8").trim(); } catch (_) {}
  const neuf = crypto.randomBytes(18).toString("base64url");
  fs.writeFileSync(FICHIER_JETON, neuf + "\n");
  return neuf;
}
const JETON = jeton();

// Le fil tient en mémoire : on le relit une fois au démarrage, puis on ajoute.
let items = [];
try {
  items = fs.readFileSync(FIL, "utf8").split("\n").filter(Boolean)
    .map((l) => { try { return JSON.parse(l); } catch (_) { return null; } })
    .filter(Boolean);
} catch (_) {}

function egal(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(b);
  return x.length === y.length && crypto.timingSafeEqual(x, y);
}

function cookies(req) {
  const c = {};
  for (const p of String(req.headers.cookie || "").split(";")) {
    const i = p.indexOf("=");
    if (i > 0) c[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim());
  }
  return c;
}

function autorise(req, url) {
  const h = String(req.headers.authorization || "");
  if (h.startsWith("Bearer ") && egal(h.slice(7), JETON)) return true;
  if (egal(url.searchParams.get("jeton"), JETON)) return true;
  return egal(cookies(req).fil_dev, JETON);
}

function envoyer(res, code, corps, type, entetes) {
  res.writeHead(code, Object.assign({
    "Content-Type": type || "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  }, entetes || {}));
  res.end(corps);
}

function publier(req, res) {
  let brut = "", trop = false;
  req.setEncoding("utf8");
  req.on("data", (d) => {
    brut += d;
    if (brut.length > PLAFOND_CORPS) { trop = true; req.destroy(); }
  });
  req.on("end", () => {
    if (trop) return;
    let m;
    try { m = JSON.parse(brut); } catch (_) { return envoyer(res, 400, '{"erreur":"json"}'); }
    if (!m || !["prompt", "reponse", "session"].includes(m.type)) {
      return envoyer(res, 400, '{"erreur":"type"}');
    }
    const item = {
      n: items.length,
      ts: new Date().toISOString(),
      type: m.type,
      auteur: String(m.auteur || "?").slice(0, 40),
      session: String(m.session || "").slice(0, 64),
      branche: String(m.branche || "").slice(0, 120),
      projet: String(m.projet || "").slice(0, 120),
      texte: String(m.texte || ""),
    };
    items.push(item);
    fs.appendFileSync(FIL, JSON.stringify(item) + "\n");
    envoyer(res, 200, JSON.stringify({ n: item.n }));
  });
}

http.createServer((req, res) => {
  const url = new URL(req.url, "http://x");
  if (!autorise(req, url)) {
    return envoyer(res, 401, "Jeton requis.", "text/plain; charset=utf-8");
  }
  // Un jeton passé dans l'URL se range dans un cookie, puis on le retire de la
  // barre d'adresse : on ne le partage pas en copiant le lien de la page.
  if (url.searchParams.has("jeton")) {
    return envoyer(res, 302, "", "text/plain", {
      "Set-Cookie": "fil_dev=" + encodeURIComponent(JETON) +
        "; Path=/; Max-Age=31536000; SameSite=Lax; HttpOnly",
      Location: url.pathname,
    });
  }
  if (req.method === "POST" && url.pathname === "/publier") return publier(req, res);
  if (req.method === "GET" && url.pathname === "/fil") {
    const depuis = Math.max(0, Number(url.searchParams.get("depuis")) || 0);
    return envoyer(res, 200, JSON.stringify(items.slice(depuis)));
  }
  if (req.method === "GET" && url.pathname === "/") {
    return envoyer(res, 200, fs.readFileSync(path.join(ICI, "page.html")),
      "text/html; charset=utf-8");
  }
  envoyer(res, 404, '{"erreur":"inconnu"}');
})
  .listen(PORT, "127.0.0.1", () => {
    console.log("Fil dev : http://localhost:" + PORT + "/?jeton=" + JETON);
  })
  .on("error", (e) => {
    console.error(e.code === "EADDRINUSE" ? "Port " + PORT + " déjà pris." : e);
    process.exit(1);
  });
