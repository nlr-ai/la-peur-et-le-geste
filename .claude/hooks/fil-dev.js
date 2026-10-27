#!/usr/bin/env node
// -*- coding: utf-8 -*-
/**
 * FIL DEV — publie ce qu'on dit à Claude et ce qu'il répond sur le fil commun.
 *
 * SessionStart, UserPromptSubmit et Stop. Muet et inerte tant que FIL_DEV_URL
 * n'est pas posé : celui qui n'a pas branché le fil ne remarque rien. La
 * configuration vit dans le bloc `env` de .claude/settings.local.json, jamais
 * dans settings.json, parce qu'elle porte le jeton (voir fil-dev/LISEZMOI.md).
 *
 * IL NE BLOQUE JAMAIS LA SESSION : toute erreur — serveur éteint, tunnel
 * tombé, transcript illisible — est avalée, et l'on sort à 0. Un fil qui
 * manque une ligne vaut mieux qu'une session qui attend un tunnel.
 */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");

const URL_FIL = (process.env.FIL_DEV_URL || "").replace(/\/+$/, "");
const JETON = process.env.FIL_DEV_JETON || "";
const AUTEUR = process.env.FIL_DEV_AUTEUR || os.userInfo().username;

let brut = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => { brut += d; });
process.stdin.on("end", () => {
  principal().catch(() => {}).finally(() => process.exit(0));
});

async function principal() {
  if (!URL_FIL) return;
  const e = JSON.parse(brut || "{}");
  let type, texte;
  if (e.hook_event_name === "UserPromptSubmit") {
    type = "prompt";
    texte = e.prompt;
  } else if (e.hook_event_name === "Stop") {
    type = "reponse";
    texte = e.last_assistant_message || derniereReponse(e.transcript_path);
  } else if (e.hook_event_name === "SessionStart") {
    if (e.source !== "startup" && e.source !== "resume") return;
    type = "session";
    texte = e.source === "resume" ? "Session reprise." : "Session ouverte.";
  } else return;
  if (!texte || !String(texte).trim()) return;

  await fetch(URL_FIL + "/publier", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + JETON },
    body: JSON.stringify({
      type, texte, auteur: AUTEUR,
      session: e.session_id || "",
      projet: path.basename(e.cwd || process.cwd()),
      branche: branche(e.cwd),
    }),
    signal: AbortSignal.timeout(4000),
  });
}

function branche(cwd) {
  try {
    return execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"],
      { cwd: cwd || process.cwd(), encoding: "utf8", timeout: 1500, stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch (_) { return ""; }
}

// Le texte que Claude a rendu depuis la dernière vraie demande : on remonte le
// transcript jusqu'au dernier message utilisateur qui n'est pas un résultat
// d'outil, et l'on recoud les blocs de texte de l'assistant qui le suivent.
function derniereReponse(fichier) {
  if (!fichier) return "";
  const lignes = fs.readFileSync(fichier, "utf8").split("\n").filter(Boolean);
  const morceaux = [];
  for (let i = lignes.length - 1; i >= 0; i--) {
    let l;
    try { l = JSON.parse(lignes[i]); } catch (_) { continue; }
    if (l.isSidechain || l.isMeta || !l.message) continue;
    const c = l.message.content;
    if (l.type === "user") {
      const resultat = Array.isArray(c) && c.some((b) => b && b.type === "tool_result");
      if (!resultat) break;
    } else if (l.type === "assistant" && Array.isArray(c)) {
      const t = c.filter((b) => b && b.type === "text").map((b) => b.text).join("\n");
      if (t.trim()) morceaux.unshift(t.trim());
    }
  }
  return morceaux.join("\n\n");
}
