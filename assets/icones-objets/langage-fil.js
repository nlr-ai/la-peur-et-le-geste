// Traduction d'affichage uniquement. Le flux et les actions enregistrés restent intacts.
(function(){
 const KEY='peur-tableau-langage';
 let coded=true, terms=[], expression=null, observer=null, queued=false, root=null,button=null;
 try{coded=localStorage.getItem(KEY)!=='clair';}catch(e){}
 const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 const normal=s=>s.toLocaleLowerCase('fr').replace(/[’']/g,"'");
 const casing=(text,source)=>source===source.toLocaleUpperCase('fr')?text.toLocaleUpperCase('fr'):/^\p{Lu}/u.test(source)?text.charAt(0).toLocaleUpperCase('fr')+text.slice(1):text.charAt(0).toLocaleLowerCase('fr')+text.slice(1);
 const known=new Map();
 function register(clair,code){
  if(!clair||!code||normal(clair)===normal(code))return;
  for(const text of [clair,code])if(!known.has(normal(text)))known.set(normal(text),{clair,code});
 }
 function display(span){
  const original=span.dataset.original;
  const shown=coded?span.dataset.code:span.dataset.clair;
  const other=coded?span.dataset.clair:span.dataset.code;
  span.textContent=casing(shown,original);
  span.title=(coded?'Langage clair : ':'Langage codé : ')+other;
  span.setAttribute('aria-label',span.textContent+' — '+span.title);
 }
 function scan(){
  queued=false;if(!root||!expression)return;
  observer.disconnect();
  root.querySelectorAll('.mot-code').forEach(display);
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>{
    if(!n.nodeValue.trim()||n.parentElement.closest('.mot-code,button,input,textarea,select,script,style,[contenteditable=true],.gestes'))return NodeFilter.FILTER_REJECT;
    return NodeFilter.FILTER_ACCEPT;
  }});
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  for(const node of nodes){
   const text=node.nodeValue;expression.lastIndex=0;let m,last=0,frag=null;
   while((m=expression.exec(text))){
    const entry=known.get(normal(m[0]));if(!entry)continue;
    if(!frag)frag=document.createDocumentFragment();
    frag.append(document.createTextNode(text.slice(last,m.index)));
    const span=document.createElement('span');span.className='mot-code';span.dataset.original=m[0];span.dataset.clair=entry.clair;span.dataset.code=entry.code;span.tabIndex=0;display(span);frag.append(span);last=m.index+m[0].length;
   }
   if(frag){frag.append(document.createTextNode(text.slice(last)));node.replaceWith(frag);}
  }
  observer.observe(root,{childList:true,subtree:true,characterData:true});
 }
 function refresh(){if(button){button.textContent=coded?'Langage codé':'Langage clair';button.setAttribute('aria-pressed',String(coded));}scan();}
 window.addEventListener('storage',e=>{if(e.key===KEY){coded=e.newValue!=='clair';refresh();}});
 window.addEventListener('DOMContentLoaded',async()=>{
  root=document.getElementById('fil-corps');if(!root)return;
  const bar=document.createElement('div');bar.id='langage-fil';button=document.createElement('button');button.type='button';button.textContent='Chargement du vocabulaire…';button.disabled=true;bar.append(button);root.before(bar);
  const style=document.createElement('style');style.textContent='#langage-fil{flex:none;text-align:right;padding:4px 0}#langage-fil button{font-size:12px;padding:5px 9px}.mot-code{border-bottom:1px dotted currentColor;cursor:help}.mot-code:focus-visible{outline:1px solid currentColor;outline-offset:2px}';document.head.append(style);
  button.onclick=()=>{coded=!coded;try{localStorage.setItem(KEY,coded?'code':'clair');}catch(e){}refresh();};
  try{
   const responses=await Promise.all([fetch('/tableau-catalogue'),fetch('/tableau-alias')]);if(responses.some(r=>!r.ok))throw Error('Dictionnaire indisponible');
   const [catalogue,aliases]=await Promise.all(responses.map(r=>r.json()));
   aliases.forEach(e=>register(e.clair,e.code));
   catalogue.forEach(e=>register(e.nom_original||e.nom,e.nom_couvert));
   terms=[...known.keys()].sort((a,b)=>b.length-a.length);
   expression=new RegExp('(?<![\\p{L}\\p{N}_])(?:'+terms.map(t=>esc(t).replace(/'/g,"['’]")).join('|')+')(?![\\p{L}\\p{N}_])','giu');
   observer=new MutationObserver(()=>{if(!queued){queued=true;queueMicrotask(scan);}});
   button.disabled=false;refresh();
  }catch(e){button.textContent='Vocabulaire indisponible';button.title=e.message;}
 });
})();
