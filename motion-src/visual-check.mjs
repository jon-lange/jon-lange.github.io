import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import assert from 'node:assert/strict';
const base='http://127.0.0.1:8123';
const out=new URL('./screenshots/',import.meta.url);
await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const errors=[];
for(const spec of [{name:'desktop',width:1440,height:900},{name:'mobile',width:390,height:844},{name:'compact',width:358,height:760}]){
 const page=await browser.newPage({viewport:{width:spec.width,height:spec.height},deviceScaleFactor:1});
 page.on('pageerror',e=>{errors.push(spec.name+': '+e.message);console.log('PAGE ERROR',spec.name,e.message);});
 page.on('console',msg=>{if(msg.type()==='error')console.log('CONSOLE ERROR',spec.name,msg.text());});
 page.on('response',response=>{if(response.status()>=400)console.log('HTTP ERROR',spec.name,response.status(),response.url());});
 await page.goto(base+'/',{waitUntil:'networkidle'});
 await page.locator('#skill-trigger:not([disabled])').waitFor();
 await page.screenshot({path:new URL(spec.name+'-about.png',out).pathname,fullPage:true});
 await page.goto(base+'/#langspan',{waitUntil:'networkidle'});
 try { await page.locator('.ls-scene').waitFor({timeout:15000}); }
 catch(error) {
   const state=await page.evaluate(()=>({
     url:location.href,
     title:document.title,
     view:document.querySelector('#result-output')?.dataset.view,
     mountCount:document.querySelectorAll('[data-langspan-stage]').length,
     stageCount:document.querySelectorAll('.ls-scene').length,
     mountHTML:document.querySelector('[data-langspan-stage]')?.outerHTML.slice(0,2200),
     scripts:[...document.scripts].map(s=>({src:s.src,readyState:s.readyState})),
     rootText:document.querySelector('#result-output')?.textContent.slice(0,500)
   }));
   console.log('STAGE DIAG',spec.name,JSON.stringify(state,null,2));
   console.log('ERRORS',errors);
   await page.screenshot({path:new URL(spec.name+'-stage-failure.png',out).pathname,fullPage:true});
   throw error;
 }
 await page.locator('.ls-stage-outer').scrollIntoViewIfNeeded();
 await page.waitForTimeout(500);
 await page.screenshot({path:new URL(spec.name+'-langspan-start.png',out).pathname,fullPage:true});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2),false,spec.name+' overflow');
 if(spec.name==='desktop') {
   let elapsed=500;
   for(const mark of [1200,2400,3500,4700,6300,8000]){
     await page.waitForTimeout(mark-elapsed);
     await page.locator('.ls-stage-outer').screenshot({path:new URL('desktop-motion-'+String(mark).padStart(4,'0')+'.png',out).pathname});
     elapsed=mark;
   }
 } else await page.waitForTimeout(2500);
 await page.screenshot({path:new URL(spec.name+'-langspan-mid.png',out).pathname,fullPage:true});
 await page.getByRole('button',{name:'Show outcome'}).click();
 await page.locator('.ls-scene[data-step="4"]').waitFor();
 await page.screenshot({path:new URL(spec.name+'-langspan-outcome.png',out).pathname,fullPage:true});
 await page.getByRole('button',{name:'Replay demonstration'}).click();
 await page.locator('.ls-scene[data-step="0"]').waitFor();
 await page.locator('#theme-toggle').click();
 assert.equal(await page.locator('html[data-theme="light"]').count(),1,'theme');
 await page.screenshot({path:new URL(spec.name+'-light.png',out).pathname,fullPage:true});
 await page.close();
}
const reduced=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
reduced.on('pageerror',e=>errors.push('reduced: '+e.message));
await reduced.goto(base+'/#langspan',{waitUntil:'networkidle'});
await reduced.locator('.ls-scene[data-step="4"]').waitFor({timeout:15000});
await reduced.screenshot({path:new URL('reduced-motion-poster.png',out).pathname,fullPage:true});
await reduced.close();
for(const [name,path] of [['botbench-tour','tour.html#review'],['research-archive','archive.html']]){
 const p=await browser.newPage({viewport:{width:390,height:844}});
 p.on('pageerror',e=>errors.push(name+': '+e.message));
 await p.goto(base+'/'+path,{waitUntil:'networkidle'});
 await p.screenshot({path:new URL(name+'-mobile.png',out).pathname,fullPage:true});
 if(name==='research-archive'){await p.locator('.study summary').first().click();assert.equal(await p.locator('.study[open]').count(),1)}
 else assert.ok(await p.locator('.chapter').count()>2);
 await p.close();
}
await browser.close();
assert.deepEqual(errors,[],'browser errors');
console.log('PASS: desktop, mobile, compact, stage replay/outcome, light theme, reduced motion, Botbench tour, archive.');
