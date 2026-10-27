// Preuve dans Chrome : vrai marqueur runtime et vraie route, monde miniature.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const depot = path.resolve(import.meta.dirname, "..");
const racine = fs.mkdtempSync(path.join(os.tmpdir(), "conseil-activite-"));
process.env.CONSEIL_RACINE = racine;
process.env.CONSEIL_SANS_REVEIL = "1";
delete process.env.CONSEIL_MONDE;
fs.mkdirSync(path.join(racine, "etat"));
fs.writeFileSync(path.join(racine, "etat", "joueurs.json"), JSON.stringify([
  { personnage_id: "alice", jeton: "test", role: "principal", occupe: true }
]));
const route = require("./routes/fils.js");
const actionRoute = require("./routes/action.js");
fs.writeFileSync(path.join(racine,"etat/personnages.json"),JSON.stringify([{id:"alice",nom:"Alice"},{id:"bob",nom:"Bob"}]));
const serveur = http.createServer((req, res) => {
  res.setHeader("Content-Type", req.url.endsWith(".js") ? "application/javascript; charset=utf-8" : "text/html; charset=utf-8");
  if(req.url === "/actions.js" || req.url === "/paroles.js") { res.end(fs.readFileSync(path.join(depot,"ecrans/modules",req.url.slice(1)))); return; }
  if(req.url === "/bus.js") { res.end(fs.readFileSync(path.join(depot,"ecrans/modules/bus.js"))); return; }
  if(req.url === "/moi") { res.end(JSON.stringify({moi:{personnage_id:"alice"}})); return; }
  if(req.url === "/scene") { res.end('{"items":[]}'); return; }
  if(req.url === "/action") { actionRoute(req,res,req.url); return; }
  if(req.url === "/") { res.end('<style>#attente{display:none}#attente.actif{display:block}</style><div id="attente">...</div><div id="lieu">Atelier</div><div id="fil-corps"></div><div id="fil-actions"></div><script>window.activerLocuteur=()=>{};window.Gens={qui:id=>({nom:id=== "bob"?"Bob":id}),marquer:()=>{}};</script><script src="/bus.js"></script><script src="/actions.js"></script><script src="/paroles.js"></script>'); return; }
  if(route(req,res,req.url) === false) { res.statusCode=404; res.end(); }
});
await new Promise(r=>serveur.listen(0,"127.0.0.1",r));
const url = `http://127.0.0.1:${serveur.address().port}`;
const pause = ms=>new Promise(r=>setTimeout(r,ms));
let chrome, socket, worker;
const profil = path.join(racine,"chrome");
const debug = 9347;
async function vivant(pour) {
  const code = `import sys,os\nsys.path.insert(0,${JSON.stringify(path.join(depot,"scripts"))})\nfrom agents.expose import runtime\nwith runtime._activite('mj','epreuve', {'CONSEIL_RACINE':${JSON.stringify(racine)},'LE_CONSEIL_AUDIENCE':${JSON.stringify(pour)}}):\n print('pret',flush=True)\n sys.stdin.readline()\n`;
  worker = spawn(process.env.PYTHON || "python", ["-c",code], {windowsHide:true});
  await new Promise((resolve,reject)=>{worker.stdout.once("data",resolve);worker.once("error",reject);worker.once("exit",c=>c && reject(new Error("worker "+c)));});
}
async function finir(){
  const fini = new Promise(r=>worker.once("exit",r)); worker.stdin.end("fin\n"); await fini; worker=null;
}
try {
  chrome = spawn("C:/Program Files/Google/Chrome/Application/chrome.exe",[
    "--headless=new","--disable-gpu","--no-first-run",`--user-data-dir=${profil}`,`--remote-debugging-port=${debug}`,url
  ],{windowsHide:true,stdio:"ignore"});
  let cible;
  for(let i=0;i<60&&!cible;i++){try{cible=(await (await fetch(`http://127.0.0.1:${debug}/json`)).json()).find(x=>x.type==="page");}catch{} if(!cible)await pause(100);}
  assert.ok(cible,"Chrome disponible");
  socket=new WebSocket(cible.webSocketDebuggerUrl);
  await new Promise(r=>socket.addEventListener("open",r,{once:true}));
  let id=0; const demandes=new Map();
  socket.addEventListener("message",e=>{const d=JSON.parse(e.data);if(demandes.has(d.id)){demandes.get(d.id)(d);demandes.delete(d.id);}});
  async function evaluer(expression){const n=++id;const p=new Promise(r=>demandes.set(n,r));socket.send(JSON.stringify({id:n,method:"Runtime.evaluate",params:{expression,returnByValue:true,awaitPromise:true}}));const d=await p;assert.ok(!d.result.exceptionDetails,JSON.stringify(d));return d.result.result.value;}
  async function attendreEtat(oui){for(let i=0;i<65;i++){if(await evaluer('!!window.Bus && document.getElementById("attente").classList.contains("actif")')===oui)return;await pause(100);}assert.fail("attente attendue "+oui);}
  await attendreEtat(false);
  await vivant("autre"); await pause(2500); await attendreEtat(false);
  assert.deepEqual(await (await fetch(url+"/activite-mj")).json(),{actif:false});
  await finir(); await vivant("alice"); await attendreEtat(true);
  await evaluer('Bus.rendre({type:"reponse"})'); await attendreEtat(true);
  await evaluer('location.reload()'); await pause(500); await attendreEtat(true);
  await finir(); await attendreEtat(false);
  await evaluer('Bus.rendre({type:"replique",locuteur_id:"bob",texte:"Bonjour"}); document.querySelector(".chr-repondre").click()');
  assert.equal(await evaluer('document.querySelector(".reponse-cible").textContent'),"À Bob ×");
  await evaluer('document.getElementById("champ-libre").value="Je vous réponds."; document.getElementById("btn-libre").click()');
  await pause(300);
  const inbox=path.join(racine,"etat/inbox/alice");
  const messages=()=>fs.readdirSync(inbox).map(n=>JSON.parse(fs.readFileSync(path.join(inbox,n))));
  assert.equal(messages().find(m=>m.texte==="Je vous réponds.").destinataire_id,"bob");
  await evaluer('document.querySelector(".chr-repondre").click(); document.getElementById("mode-agir").click(); document.getElementById("champ-libre").value="Je me lève."; document.getElementById("btn-libre").click()');
  await pause(300);
  assert.equal(messages().find(m=>m.texte==="Je me lève.").destinataire_id,undefined);
  const avantRun = messages().length;
  await evaluer('document.getElementById("mode-run").click(); document.getElementById("champ-libre").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));');
  await pause(200);
  assert.equal(messages().length, avantRun, "Entrée vide crée un run involontaire");
  await evaluer('document.getElementById("btn-libre").click()');
  await pause(200);
  assert.equal(messages().length, avantRun + 1);
  assert.equal(messages().filter(m=>m.mode==="run").length, 1);
  await evaluer('document.getElementById("btn-libre").click(); document.getElementById("champ-libre").dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));');
  await pause(200);
  assert.equal(messages().length, avantRun + 1, "Le mode run reste armé après envoi");
  await evaluer('Bus.rendre({type:"reponse"})');
  await evaluer('Bus.poster({type:"question",texte:"essai"})'); await attendreEtat(true);
  await evaluer('Bus.rendre({type:"reponse"})'); await attendreEtat(false);
  await vivant("alice"); await attendreEtat(true);
  worker.kill(); await new Promise(r=>worker.once("exit",r)); worker=null;
  await attendreEtat(false);
  console.log("Chrome : activité MJ, bouton Répondre, destinataire dans la vraie inbox HTTP et changement de mode vérifiés.");
} finally {
  if(worker)worker.kill(); if(socket)socket.close(); if(chrome)chrome.kill();
  await new Promise(r=>serveur.close(r));
  // Retire uniquement les marqueurs de ce monde miniature, y compris le crash.
  const actifs=path.join(depot,".agents-runtime/active");
  for(const n of fs.readdirSync(actifs)){if(!n.endsWith(".json"))continue;try{const p=path.join(actifs,n);const d=JSON.parse(fs.readFileSync(p));if(d.racine===racine.toLowerCase())fs.unlinkSync(p);}catch{}}
}
