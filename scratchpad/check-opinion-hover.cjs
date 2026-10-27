const { chromium }=require('C:/Users/reyno/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,channel:'msedge'});const page=await browser.newPage({viewport:{width:1600,height:900}});await page.goto('http://localhost:3212/bascule?vers=michel');await page.waitForTimeout(1600);
const data=await page.evaluate(async()=> (await (await fetch('/gens')).json()).gens);
const c=data.find(p=>p.id==='celine-joubert'); console.log('API',c.opinion,c.opinion_details);
if(!c.opinion_details.some(s=>s.includes('18/100')))throw Error('Missing source score');
await page.evaluate(p=>{const host=document.createElement('div');host.id='hover-test';host.style='position:fixed;left:500px;top:100px;z-index:999';host.innerHTML=Visage.html(p,{classe:"chr-icone"});document.body.appendChild(host)},c);
const badge=page.locator('#hover-test .visage-opinion');await badge.hover();await page.waitForTimeout(200);console.log('HOVER',await page.locator('.opinion-fiche.ouverte').innerText());await page.keyboard.press('Escape');if(await page.locator('.opinion-fiche.ouverte').count())throw Error('Escape');await badge.focus();if(!await page.locator('.opinion-fiche.ouverte').count())throw Error('Focus');console.log('Keyboard OK');await browser.close()})();

