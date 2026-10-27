const fs = require('fs');
const path = require('path');
const { RACINE, DEPOT, monPersonnage, envoyer } = require('../http');
const base = path.join(DEPOT, 'assets', 'icones-objets');
function valider(b, ids) {
  if (!b || !Number.isInteger(b.revision) || !Array.isArray(b.nodes) || !Array.isArray(b.edges) || b.nodes.length > 500 || b.edges.length > 1500) throw Error('Tableau invalide');
  const seen = new Set();
  const nodes = b.nodes.map(n => {
    if (!n || typeof n.id !== 'string' || !/^[\w-]{1,80}$/.test(n.id) || seen.has(n.id) || !ids.has(n.icon) || !Number.isFinite(n.x) || !Number.isFinite(n.y) || n.x<0 || n.y<0 || n.x>2304 || n.y>1440 || typeof n.label !== 'string' || n.label.length>120) throw Error('Icône invalide');
    if(n.stepIndex!==undefined && (!n.icon.startsWith('action-') || !Number.isInteger(n.stepIndex) || n.stepIndex<0 || n.stepIndex>30)) throw Error('Étape invalide');
    if(n.todoExpanded!==undefined && typeof n.todoExpanded!=='boolean') throw Error('Chaîne invalide');
    if(n.done!==undefined && typeof n.done!=='boolean') throw Error('État de tâche invalide');
    if(n.quantity!==undefined && (!Number.isFinite(n.quantity)||n.quantity<=0||n.quantity>1000000000)) throw Error('Quantité invalide');
    if(n.typedExpanded!==undefined && typeof n.typedExpanded!=='boolean') throw Error('Graphe invalide');
    if(n.relation!==undefined && !['besoin','produit','prerequis'].includes(n.relation)) throw Error('Type de lien invalide');
    seen.add(n.id); return {id:n.id,icon:n.icon,x:n.x,y:n.y,label:n.label,...(n.stepIndex!==undefined?{stepIndex:n.stepIndex}:{}),...(n.done!==undefined?{done:n.done}:{}),...(n.quantity!==undefined?{quantity:n.quantity}:{}),...(n.relation!==undefined?{relation:n.relation}:{}),...(n.typedExpanded!==undefined?{typedExpanded:n.typedExpanded}:{}),...(n.todoExpanded!==undefined?{todoExpanded:n.todoExpanded}:{})};
  });
  const links=new Set();
  const edges=b.edges.map(e=>{
    if (!e || typeof e.id!=='string' || !/^[\w-]{1,80}$/.test(e.id) || links.has(e.id) || !seen.has(e.from) || !seen.has(e.to) || e.from===e.to) throw Error('Flèche invalide');
    links.add(e.id); return {id:e.id,from:e.from,to:e.to};
  });
  return {revision:b.revision,nodes,edges};
}
function traiter(req,res,url) {
  if (path.basename(RACINE)!=='la-peur-et-le-geste') return false;
  const send=(code,data)=>envoyer(res,code,JSON.stringify(data));
  if (req.method==='GET' && url==='/modules/echiquier.js') return envoyer(res,200,fs.readFileSync(path.join(base,'tableau-module.js'),'utf8')+'\n'+fs.readFileSync(path.join(base,'langage-fil.js'),'utf8'),'text/javascript; charset=utf-8');
  if (req.method==='GET' && url==='/tableau-libre') return envoyer(res,200,fs.readFileSync(path.join(base,'tableau.html')),'text/html; charset=utf-8');
  if (req.method==='GET' && url==='/tableau-alias') return envoyer(res,200,fs.readFileSync(path.join(base,'alias-fil.json')));
  if (req.method==='GET' && url==='/tableau-catalogue') return envoyer(res,200,fs.readFileSync(path.join(base,'manifest.json')));
  if (req.method==='GET' && /^\/tableau-svg(?:-clair)?\/[a-z0-9_-]+\.svg$/.test(url)) {
    const file=path.join(base,url.startsWith('/tableau-svg-clair/')?'svg-clair':'svg',path.basename(url));
    return fs.existsSync(file)?envoyer(res,200,fs.readFileSync(file),'image/svg+xml'):send(404,{erreur:'Icône absente'});
  }
  if(url!=='/tableau-etat') return false;
  const who=monPersonnage(req,url);
  if(!who || !/^[a-z0-9_-]+$/.test(who)) return send(401,{erreur:'Ouvrez le jeu avec votre personnage.'});
  const dir=path.join(RACINE,'chambres',who,'tableau');
  const file=path.join(dir,'disposition.json');
  const read=()=>fs.existsSync(file)?JSON.parse(fs.readFileSync(file,'utf8')):{revision:0,nodes:[],edges:[]};
  if(req.method==='GET') {try{return send(200,read());}catch(e){return send(500,{erreur:'Lecture impossible ; sauvegarde conservée.'});}}
  if(req.method!=='PUT') return send(405,{erreur:'Méthode refusée'});
  let body='',size=0,tooLarge=false;
  req.on('data',chunk=>{size+=chunk.length;if(size>500000)tooLarge=true;else body+=chunk;});
  req.on('end',()=>{
    if(tooLarge)return send(413,{erreur:'Tableau trop grand'});
    let data;
    try{data=valider(JSON.parse(body),new Set(JSON.parse(fs.readFileSync(path.join(base,'manifest.json'),'utf8')).map(e=>e.id)));}
    catch(e){return send(400,{erreur:e.message});}
    try{
      const old=read();
      if(old.revision!==data.revision)return send(409,{erreur:'Le tableau a changé dans un autre onglet. Rechargez avant de poursuivre.'});
      data.revision++;
      fs.mkdirSync(dir,{recursive:true});
      const tmp=file+'.tmp';fs.writeFileSync(tmp,JSON.stringify(data,null,2)+'\n');fs.renameSync(tmp,file);
      return send(200,{revision:data.revision});
    }catch(e){return send(500,{erreur:'Sauvegarde impossible. Vos changements restent à l’écran.'});}
  });
}
module.exports=traiter;
module.exports.valider=valider;
