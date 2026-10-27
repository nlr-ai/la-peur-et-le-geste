import { spawn } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const browser='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const page=pathToFileURL(resolve(process.argv[2]||'04-passage-retrait-vrai.html')).href;
const profile=await mkdtemp(join(tmpdir(),'vox-retrait-vrai-'));
const port=9551;
const child=spawn(browser,['--headless=new',`--remote-debugging-port=${port}`,`--user-data-dir=${profile}`,'--no-first-run',page],{stdio:'ignore'});

try {
  let tabs;
  for(let i=0;i<60;i++){
    try{tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();break;}
    catch{await new Promise(r=>setTimeout(r,100));}
  }
  if(!tabs)throw new Error('Navigateur inaccessible');
  const ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((ok,fail)=>{ws.onopen=ok;ws.onerror=fail;});
  let id=0;const pending=new Map();
  ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){pending.get(m.id)(m);pending.delete(m.id);}};
  const send=(method,params={})=>new Promise((ok,fail)=>{const call=++id;pending.set(call,m=>m.error?fail(new Error(m.error.message)):ok(m.result));ws.send(JSON.stringify({id:call,method,params}));});
  const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
  for(let i=0;i<50;i++){if(await evaluate("!!document.querySelector('#answer')"))break;await new Promise(r=>setTimeout(r,100));}
  const key=async(key)=>{
    const specs={Tab:{key:'Tab',code:'Tab',vk:9,type:'rawKeyDown'},Space:{key:' ',code:'Space',vk:32,type:'keyDown'}};
    const s=specs[key];
    await send('Input.dispatchKeyEvent',{type:s.type,key:s.key,code:s.code,text:key==='Space'?' ':undefined,windowsVirtualKeyCode:s.vk,nativeVirtualKeyCode:s.vk});
    await send('Input.dispatchKeyEvent',{type:'keyUp',key:s.key,code:s.code,windowsVirtualKeyCode:s.vk,nativeVirtualKeyCode:s.vk});
  };

  await key('Tab');
  await send('Input.insertText',{text:'veilles'});
  await key('Tab');await key('Space');
  const afterAnswer=await evaluate(`({focus:document.activeElement.id,two:!two.hidden,tracesHidden:traces.hidden})`);
  await key('Tab');await key('Space');
  const afterReveal=await evaluate(`({focus:document.activeElement.id,tracesVisible:!traces.hidden,beforeHidden:beforeTraces.hidden,afterVisible:!afterTraces.hidden,falseChoiceVisible:!!document.querySelector('#finish-before-traces').offsetParent,announcement:announcement.textContent,namesExposed:/ECHO|Nacre/.test(traces.textContent)})`);
  await key('Tab');
  const atTrueWithdrawal=await evaluate(`({focus:document.activeElement.id,label:document.activeElement.textContent.trim()})`);
  await key('Space');
  const afterWithdrawal=await evaluate(`({focus:document.activeElement.id,away:!away.hidden,word:word.value,tracesHidden:traces.hidden,local:localStorage.length,session:sessionStorage.length,cookies:document.cookie})`);

  const ok={
    answer:afterAnswer.focus==='title-two'&&afterAnswer.two&&afterAnswer.tracesHidden,
    reveal:afterReveal.focus==='traces'&&afterReveal.tracesVisible&&afterReveal.beforeHidden&&afterReveal.afterVisible&&!afterReveal.falseChoiceVisible&&afterReveal.announcement==='Les traces antérieures sont maintenant visibles.'&&!afterReveal.namesExposed,
    reach:atTrueWithdrawal.focus==='erase-after-traces'&&atTrueWithdrawal.label==='Effacer mon mot et repartir',
    withdraw:afterWithdrawal.focus==='title-away'&&afterWithdrawal.away&&afterWithdrawal.word===''&&afterWithdrawal.tracesHidden&&afterWithdrawal.local===0&&afterWithdrawal.session===0&&afterWithdrawal.cookies===''
  };
  console.log(JSON.stringify({afterAnswer,afterReveal,atTrueWithdrawal,afterWithdrawal,ok},null,2));
  if(!Object.values(ok).every(Boolean))process.exitCode=1;
  ws.close();
} finally {
  if(child.exitCode===null){child.kill();await new Promise(r=>child.once('exit',r));}
  await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:150});
}
