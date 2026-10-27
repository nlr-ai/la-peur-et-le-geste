import { spawn } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const browser='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const page=pathToFileURL(resolve(process.argv[2]||'03-passage-deux-seuils-accessible.html')).href;
let nextPort=9440;

async function session(run){
  const port=nextPort++;
  const profile=await mkdtemp(join(tmpdir(),'vox-clavier-'));
  const child=spawn(browser,['--headless=new',`--remote-debugging-port=${port}`,`--user-data-dir=${profile}`,'--no-first-run',page],{stdio:'ignore'});
  try {
    let tabs;
    for(let i=0;i<60;i++){
      try{ tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json(); break; }
      catch{ await new Promise(r=>setTimeout(r,100)); }
    }
    if(!tabs) throw new Error('Navigateur inaccessible');
    const ws=new WebSocket(tabs.find(t=>t.type==='page').webSocketDebuggerUrl);
    await new Promise((ok,fail)=>{ws.onopen=ok;ws.onerror=fail;});
    let id=0;
    const pending=new Map();
    ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){pending.get(m.id)(m);pending.delete(m.id);}};
    const send=(method,params={})=>new Promise((ok,fail)=>{
      const call=++id; pending.set(call,m=>m.error?fail(new Error(m.error.message)):ok(m.result));
      ws.send(JSON.stringify({id:call,method,params}));
    });
    const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
    for(let i=0;i<50;i++){
      if(await evaluate("!!document.querySelector('#answer')")) break;
      await new Promise(r=>setTimeout(r,100));
    }
    const key=async(key,modifiers=0)=>{
      const codes={Tab:{code:'Tab',vk:9},Enter:{code:'Enter',vk:13},Space:{code:'Space',vk:32}};
      const spec=codes[key]||{code:key,vk:0};
      const value=key==='Space'?' ':key;
      const downType=key==='Space'?'keyDown':'rawKeyDown';
      await send('Input.dispatchKeyEvent',{type:downType,key:value,code:spec.code,text:key==='Space'?' ':undefined,windowsVirtualKeyCode:spec.vk,nativeVirtualKeyCode:spec.vk,modifiers});
      await send('Input.dispatchKeyEvent',{type:'keyUp',key:value,code:spec.code,windowsVirtualKeyCode:spec.vk,nativeVirtualKeyCode:spec.vk,modifiers});
    };
    const api={evaluate,key,type:text=>send('Input.insertText',{text})};
    const result=await run(api);
    ws.close();
    return result;
  } finally {
    if(child.exitCode===null){child.kill();await new Promise(r=>child.once('exit',r));}
    await rm(profile,{recursive:true,force:true,maxRetries:3,retryDelay:150});
  }
}

const answerAndReveal=await session(async({evaluate,key,type})=>{
  await key('Tab'); await type('écoutes'); await key('Tab'); await key('Space');
  const afterAnswer=await evaluate(`({focus:document.activeElement.id,two:!two.hidden,tracesHidden:traces.hidden})`);
  await key('Tab'); await key('Space');
  const afterReveal=await evaluate(`({focus:document.activeElement.id,tracesVisible:!traces.hidden,announcement:announcement.textContent})`);
  return {afterAnswer,afterReveal};
});

const seeWithoutAnswer=await session(async({evaluate,key})=>{
  await key('Tab'); await key('Tab'); await key('Tab'); await key('Space');
  return evaluate(`({focus:document.activeElement.id,two:!two.hidden,tracesHidden:traces.hidden,word:word.value})`);
});

const directWithdrawal=await session(async({evaluate,key,type})=>{
  await key('Tab'); await type('secret'); await key('Tab'); await key('Tab'); await key('Tab'); await key('Space');
  return evaluate(`({focus:document.activeElement.id,away:!away.hidden,word:word.value,tracesHidden:traces.hidden,local:localStorage.length,session:sessionStorage.length,cookies:document.cookie})`);
});

const finishWithdrawal=await session(async({evaluate,key,type})=>{
  await key('Tab'); await type('veilles'); await key('Tab'); await key('Space');
  await key('Tab'); await key('Tab'); await key('Space');
  return evaluate(`({focus:document.activeElement.id,away:!away.hidden,word:word.value,tracesHidden:traces.hidden,local:localStorage.length,session:sessionStorage.length,cookies:document.cookie})`);
});

const ok={
  answer:answerAndReveal.afterAnswer.focus==='title-two'&&answerAndReveal.afterAnswer.two&&answerAndReveal.afterAnswer.tracesHidden,
  reveal:answerAndReveal.afterReveal.focus==='traces'&&answerAndReveal.afterReveal.tracesVisible&&answerAndReveal.afterReveal.announcement==='Les traces antérieures sont maintenant visibles.',
  see:seeWithoutAnswer.focus==='title-two'&&seeWithoutAnswer.two&&seeWithoutAnswer.tracesHidden&&seeWithoutAnswer.word==='',
  leave:directWithdrawal.focus==='title-away'&&directWithdrawal.away&&directWithdrawal.word===''&&directWithdrawal.tracesHidden&&directWithdrawal.local===0&&directWithdrawal.session===0&&directWithdrawal.cookies==='',
  finish:finishWithdrawal.focus==='title-away'&&finishWithdrawal.away&&finishWithdrawal.word===''&&finishWithdrawal.tracesHidden&&finishWithdrawal.local===0&&finishWithdrawal.session===0&&finishWithdrawal.cookies===''
};

console.log(JSON.stringify({answerAndReveal,seeWithoutAnswer,directWithdrawal,finishWithdrawal,ok},null,2));
if(!Object.values(ok).every(Boolean)) process.exitCode=1;
