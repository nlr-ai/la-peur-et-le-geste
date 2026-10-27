const fs=require('fs'),vm=require('vm'),assert=require('assert');
class E {constructor(tag){this.tag=tag;this.children=[];this.dataset={};this.classList={contains:()=>false,add:()=>{}};} appendChild(x){this.children.push(x);return x;} insertBefore(x){this.children.push(x);} querySelector(){return new E('span');} querySelectorAll(){return [];} set innerHTML(x){this.children=[];} }
const saved={},sent=[];let success=true;
const context={window:{},document:{createElement:t=>new E(t)},localStorage:{getItem:k=>saved[k],setItem:(k,v)=>saved[k]=v},Bus:{envoyer:async a=>{sent.push(a);return success;}},setTimeout:()=>{},alert:()=>{}};
vm.runInNewContext(fs.readFileSync('ecrans/modules/demandes.js','utf8'),context);
const qs=JSON.parse(fs.readFileSync('scratchpad/entretien-lucien.json','utf8'));
function flatten(e){return [e,...e.children.flatMap(flatten)];}
(async()=>{const entry=new E('entry');entry.querySelector=()=>entry;context.window.Demandes.poser(entry,{entretien:qs,locuteur_id:'lucien-frere-de-michel'});
assert.equal(entry.children.length,1);success=false;await flatten(entry).find(e=>e.className==='demande-voie').onclick();assert.equal(entry.children.length,1);assert.equal(Object.keys(saved).length,0);
success=true;
for(let i=0;i<5;i++){const block=entry.children[i];await flatten(block).find(e=>e.className==='demande-voie').onclick();assert.equal(sent.at(-1).demande_id,qs[i].id);}
assert.equal(entry.children.length,6);assert.equal(Object.keys(JSON.parse(saved['demandes-repondues'])).length,5);
const reload=new E('entry');reload.querySelector=()=>reload;context.window.Demandes.poser(reload,{entretien:qs});assert.equal(reload.children.length,6);
console.log('OK: progression 1 à 5, échec réseau sans avancement, transmission et reprise après rechargement.');})();
