const { chromium } = require('C:/Users/reyno/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:"msedge"});
 const page=await browser.newPage({viewport:{width:1600,height:900}});
 await page.goto('http://localhost:3212/?vue=royaume');
 await page.waitForTimeout(1800);
 const measure=()=>page.evaluate(()=>{const r=id=>{let b=document.getElementById(id).getBoundingClientRect();return {x:b.x,w:b.width,right:b.right}};return {fil:r('fil'),scene:r('scene'),menu:r('lateral'),handle:r('poignee'),overflow:document.documentElement.scrollWidth>innerWidth}});
 console.log('default',await measure());
 let h=await page.locator('#poignee').boundingBox();
 await page.mouse.move(h.x+h.width/2,450);await page.mouse.down();await page.mouse.move(h.x+105,450,{steps:10});await page.mouse.up();
 console.log('drag',await measure());
 await page.reload();await page.waitForTimeout(700);console.log('reload',await measure());
 await page.locator('#lateral-bascule').click();await page.waitForTimeout(500);console.log('menu open',await measure());
 await page.setViewportSize({width:700,height:900});await page.waitForTimeout(400);console.log('compact open',await measure());
 await page.locator('#lateral-bascule').click();await page.waitForTimeout(400);console.log('compact closed',await measure());
 await browser.close();
})();

