import { spawn } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const browser = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const page = pathToFileURL(resolve(process.argv[2] || '02-passage-deux-seuils.html')).href;

async function cdp(port, expression) {
  const profile = await mkdtemp(join(tmpdir(), 'vox-deux-seuils-'));
  const child = spawn(browser, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', page], { stdio: 'ignore' });
  try {
    let tabs;
    for (let i = 0; i < 60; i++) {
      try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; }
      catch { await new Promise(r => setTimeout(r, 100)); }
    }
    if (!tabs) throw new Error('Navigateur inaccessible');
    const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
    await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
    const result = await new Promise((ok, fail) => {
      ws.onmessage = event => { const msg = JSON.parse(event.data); if (msg.id === 1) ok(msg.result.result.value); };
      ws.onerror = fail;
      const waitedExpression = `(async () => {
        for (let i = 0; i < 50 && !document.querySelector('#answer'); i++) {
          await new Promise(r => setTimeout(r, 100));
        }
        if (!document.querySelector('#answer')) throw new Error('Carte non chargée');
        return (${expression});
      })()`;
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: waitedExpression, returnByValue: true, awaitPromise: true } }));
    });
    ws.close();
    return result;
  } finally {
    if (child.exitCode === null) {
      child.kill();
      await new Promise(resolveExit => child.once('exit', resolveExit));
    }
    for (let i = 0; i < 5; i++) {
      try { await rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 150 }); break; }
      catch (error) { if (i === 4) throw error; await new Promise(r => setTimeout(r, 250)); }
    }
  }
}

const answering = await cdp(9331, `(() => {
  word.value='ménages'; answer.click();
  const before = {one:one.hidden,two:two.hidden,traces:traces.hidden,gesture:gesture.textContent};
  reveal.click();
  return {before, tracesVisible:!traces.hidden, echo:traces.textContent.includes('ECHO'), nacre:traces.textContent.includes('Nacre')};
})()`);

const withdrawing = await cdp(9332, `(() => {
  word.value='secret'; leave.click(); return {
    one:one.hidden, two:two.hidden, away:away.hidden, cleared:word.value==='', tracesHidden:traces.hidden,
    storage:{local:localStorage.length,session:sessionStorage.length,cookies:document.cookie}
  };
})()`);

const explicit = await cdp(9333, `(() => {
  document.querySelector('#see-without-answer').click();
  return {one:one.hidden,two:two.hidden,traces:traces.hidden,gesture:gesture.textContent,word:word.value};
})()`);

const okAnswer = answering.before.one && !answering.before.two && answering.before.traces && answering.tracesVisible && answering.echo && answering.nacre;
const okLeave = withdrawing.one && withdrawing.two && !withdrawing.away && withdrawing.cleared && withdrawing.tracesHidden && withdrawing.storage.local===0 && withdrawing.storage.session===0 && withdrawing.storage.cookies==='';
const okExplicit = explicit.one && !explicit.two && explicit.traces && explicit.word==='' && explicit.gesture.includes('sans déposer de mot');

console.log(JSON.stringify({ answering, withdrawing, explicit, okAnswer, okLeave, okExplicit }, null, 2));
if (!okAnswer || !okLeave || !okExplicit) process.exitCode = 1;
