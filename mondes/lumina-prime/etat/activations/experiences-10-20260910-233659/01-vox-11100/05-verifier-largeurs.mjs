import { spawn } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const browser='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const page=pathToFileURL(resolve(process.argv[2]||'05-passage-largeurs-tenues.html')).href;
let port=9770;

async function testWidth(width){
  const profile=await mkdtemp(join(tmpdir(),`vox-largeur-${width}-`));
  const child=spawn(browser,['--headless=new',`--remote-debugging-port=${port}`,`--user-data-dir=${profile}`,'--no-first-run',page],{stdio:'ignore'});
  try{
    let tabs;for(let i=0;i<60;i++){try{tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();break;}catch{await new Promise(r=>setTimeout(r,100));}}
    const ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise((ok,fail)=>{ws.onopen=ok;ws.onerror=fail;});
    let id=0;const waiting=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&waiting.has(m.id)){waiting.get(m.id)(m);waiting.delete(m.id);}};
    const send=(method,params={})=>new Promise((ok,fail)=>{const call=++id;waiting.set(call,m=>m.error?fail(new Error(m.error.message)):ok(m.result));ws.send(JSON.stringify({id:call,method,params}));});
    const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
    await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});await send('Page.reload',{ignoreCache:true});
    for(let i=0;i<50;i++){if(await evaluate("!!document.querySelector('#answer')"))break;await new Promise(r=>setTimeout(r,100));}
    const key=async key=>{const s=key==='Tab'?{key:'Tab',code:'Tab',vk:9,type:'rawKeyDown'}:{key:' ',code:'Space',vk:32,type:'keyDown'};await send('Input.dispatchKeyEvent',{type:s.type,key:s.key,code:s.code,text:key==='Space'?' ':undefined,windowsVirtualKeyCode:s.vk,nativeVirtualKeyCode:s.vk});await send('Input.dispatchKeyEvent',{type:'keyUp',key:s.key,code:s.code,windowsVirtualKeyCode:s.vk,nativeVirtualKeyCode:s.vk});};
    const measure=()=>evaluate(`(() => {const visible=[...document.querySelectorAll('body *')].filter(el=>!el.hidden&&el.offsetParent!==null&&!el.classList.contains('sr-only'));const outside=visible.filter(el=>{const r=el.getBoundingClientRect();const contentElement=['P','BUTTON','INPUT'].includes(el.tagName);return r.left<-.5||r.right>innerWidth+.5||(contentElement&&el.scrollWidth>el.clientWidth+.5);}).map(el=>el.id||el.tagName);return {innerWidth,scrollWidth:document.documentElement.scrollWidth,outside,focus:document.activeElement.id};})()`);
    const naked=await measure();
    await key('Tab');await send('Input.insertText',{text:'veilles'});await key('Tab');await key('Space');await key('Tab');await key('Space');
    const opened=await measure();
    await key('Tab');const withdrawalFocus=await evaluate('document.activeElement.id');await key('Space');
    const withdrawn={...(await measure()),word:await evaluate('word.value'),local:await evaluate('localStorage.length'),session:await evaluate('sessionStorage.length'),cookies:await evaluate('document.cookie')};
    ws.close();port++;
    return {width,naked,opened,withdrawalFocus,withdrawn};
  }finally{
    if(child.exitCode===null){child.kill();await new Promise(r=>child.once('exit',r));}
    await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:150});
  }
}

const results=[];for(const width of [320,375,1440])results.push(await testWidth(width));
const states=results.flatMap(r=>[r.naked,r.opened,r.withdrawn]);
const ok={
  widths:results.every(r=>[r.naked,r.opened,r.withdrawn].every(s=>s.scrollWidth<=s.innerWidth&&s.outside.length===0)),
  keyboard:results.every(r=>r.opened.focus==='traces'&&r.withdrawalFocus==='erase-after-traces'&&r.withdrawn.focus==='title-away'),
  erased:results.every(r=>r.withdrawn.word===''&&r.withdrawn.local===0&&r.withdrawn.session===0&&r.withdrawn.cookies==='')
};
console.log(JSON.stringify({results,ok},null,2));if(!Object.values(ok).every(Boolean))process.exitCode=1;
