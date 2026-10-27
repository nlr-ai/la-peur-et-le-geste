window.Echiquier = (() => {
  function monter(){
    if(!document.getElementById('style-tableau-libre')){
      const style=document.createElement('style');style.id='style-tableau-libre';
      style.textContent=`body:has(#echiquier:not(.vue-off)) #fil{display:flex;min-height:0}
      body:has(#echiquier:not(.vue-off)) #scene{min-height:0}
      @media(max-width:1100px){body:has(#echiquier:not(.vue-off)){grid-template-rows:minmax(0,55vh) minmax(0,1fr)}}
      body:has(#echiquier:not(.vue-off)) #decor,body:has(#echiquier:not(.vue-off)) #cartes{min-height:0;flex:1 1 0}
      #echiquier:not(.vue-off){min-height:0;flex:1 1 0;overflow:hidden}
      #echiquier iframe{flex:1 1 0;min-height:0!important;height:100%!important}`;
      document.head.appendChild(style);
    }

    const h=document.getElementById('echiquier');
    if(!h || h.querySelector('iframe'))return;
    const frame=document.createElement('iframe');frame.src='/tableau-libre';frame.title='Tableau libre';
    frame.style.cssText='width:100%;height:100%;min-height:0;border:0;display:block';
    h.appendChild(frame);
  }
  window.addEventListener('DOMContentLoaded',()=>{
    Plan.echelle({id:'echiquier',nom:'Le tableau',hote:'echiquier',ordre:2.5,dispo:()=>true,reparu:monter});
    if(window.Nav)Nav.enregistrer('echiquier',{clefs:[],etat:()=>({}),poser:()=>{monter();return true;}});
  });
  return {charger:monter,relire:()=>{},connait:()=>false,sorte:()=>null,nom:()=>'',designer:()=>{},oublier:()=>{},pourLivre:()=>null,montrer:()=>{Plan.montrer('echiquier');monter();},fermer:()=>{},relacher:()=>{}};
})();
