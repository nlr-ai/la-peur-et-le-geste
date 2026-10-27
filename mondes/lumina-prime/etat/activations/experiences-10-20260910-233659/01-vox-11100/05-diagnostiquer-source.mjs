import { spawn } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const browser='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const page=pathToFileURL(resolve(process.argv[2]||'04-passage-retrait-vrai.html')).href;
const profile=await mkdtemp(join(tmpdir(),'vox-diagnostic-'));
const port=9661;
const child=spawn(browser,['--headless=new',`--remote-debugging-port=${port}`,`--user-data-dir=${profile}`,'--no-first-run',page],{stdio:'ignore'});
try{
  let tabs;
  for(let i=0;i<60;i++){try{tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();break;}catch{await new Promise(r=>setTimeout(r,100));}}
  const ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((ok,fail)=>{ws.onopen=ok;ws.onerror=fail;});
  let id=0;const waiting=new Map();
  ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&waiting.has(m.id)){waiting.get(m.id)(m);waiting.delete(m.id);}};
  const send=(method,params={})=>new Promise((ok,fail)=>{const call=++id;waiting.set(call,m=>m.error?fail(new Error(m.error.message)):ok(m.result));ws.send(JSON.stringify({id:call,method,params}));});
  await send('Emulation.setDeviceMetricsOverride',{width:375,height:812,deviceScaleFactor:1,mobile:process.argv.includes('--mobile')});
  await send('Page.reload',{ignoreCache:true});
  await new Promise(r=>setTimeout(r,500));
  const expression=`(() => {
    const width=innerWidth;
    const elements=[...document.querySelectorAll('body *')].filter(el=>!el.hidden).map(el=>{
      const r=el.getBoundingClientRect(); const s=getComputedStyle(el);
      return {tag:el.tagName,id:el.id,cls:el.className||'',left:r.left,right:r.right,width:r.width,scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,minWidth:s.minWidth,whiteSpace:s.whiteSpace};
    }).filter(x=>x.right>width+.5||x.left<-.5||x.scrollWidth>x.clientWidth+.5);
    const main=document.querySelector('main').getBoundingClientRect();
    const section=document.querySelector('section').getBoundingClientRect();
    return {innerWidth:width,documentScrollWidth:document.documentElement.scrollWidth,main:{left:main.left,right:main.right,width:main.width},section:{left:section.left,right:section.right,width:section.width},elements};
  })()`;
  const result=(await send('Runtime.evaluate',{expression,returnByValue:true})).result.value;
  console.log(JSON.stringify(result,null,2));
  ws.close();
}finally{
  if(child.exitCode===null){child.kill();await new Promise(r=>child.once('exit',r));}
  await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:150});
}
