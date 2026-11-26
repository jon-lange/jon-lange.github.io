// Browser regression check for the portfolio. Serves from 127.0.0.1:8123.
// Covers: nav links and Back, theme from the OS and remembered, the lazy
// Stageshow bundle, Pause/Play/Replay, reduced motion, phone text sizes,
// no horizontal overflow at 358, no-JavaScript routes, tour and archive.
import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import assert from 'node:assert/strict';
const base = process.env.BASE || 'http://127.0.0.1:8123';
const out = new URL('./screenshots/', import.meta.url);
await mkdir(out, { recursive: true });
const shot = (name) => new URL(name + '.png', out).pathname;
const browser = await chromium.launch({ headless: true });
const errors = [];
const watch = (page, name) => {
  page.on('pageerror', (e) => errors.push(name + ': ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(name + ' console: ' + m.text()); });
  page.on('response', (r) => { if (r.status() >= 400) errors.push(name + ' HTTP ' + r.status() + ' ' + r.url()); });
};
const routes = ['work', 'langspan', 'botbench', 'writing', 'lab', 'contact', 'help', 'duck'];

for (const spec of [{ name: 'desktop', width: 1440, height: 900 }, { name: 'mobile', width: 390, height: 844 }, { name: 'compact', width: 358, height: 760 }]) {
  for (const scheme of ['dark', 'light']) {
    const ctx = await browser.newContext({ viewport: { width: spec.width, height: spec.height }, colorScheme: scheme });
    const page = await ctx.newPage();
    watch(page, `${spec.name}-${scheme}`);
    await page.goto(base + '/', { waitUntil: 'networkidle' });
    await page.locator('#skill-trigger:not([disabled])').waitFor();
    assert.equal(await page.evaluate(() => document.documentElement.dataset.theme), scheme, 'theme follows the OS');
    assert.equal(await page.locator('script[src*="langspan-stage"]').count(), 0, 'Stageshow is not loaded on /about');
    assert.ok(await page.locator('.quick-nav a[href="#contact"]').isVisible(), 'Contact visible in the nav');
    assert.ok(await page.locator('.contact-actions a[href*="linkedin"]').isVisible(), 'contact action on /about');
    await page.screenshot({ path: shot(`${spec.name}-${scheme}-about`), fullPage: true });
    for (const route of routes) {
      await page.goto(base + '/#' + route, { waitUntil: 'networkidle' });
      await page.locator(`#result-output[data-view="${route}"]`).waitFor();
      const over = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      assert.ok(over <= 0, `${spec.name} ${route} overflows by ${over}px`);
    }
    await ctx.close();
  }
}

// Navigation: real links, intercepted; Back returns to the previous view.
{
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  watch(page, 'nav');
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  await page.locator('#skill-trigger:not([disabled])').waitFor();
  assert.equal(await page.locator('.quick-nav a[href="#work"]').count(), 1, 'nav items are links');
  await page.locator('.quick-nav a[href="#work"]').click();
  await page.locator('#result-output[data-view="work"]').waitFor();
  await page.locator('.quick-nav a[href="#botbench"]').click();
  await page.locator('#result-output[data-view="botbench"]').waitFor();
  assert.equal(await page.locator('#active-skill').textContent(), '/botbench');
  await page.goBack();
  await page.locator('#result-output[data-view="work"]').waitFor();
  // Theme toggle is remembered across a reload.
  const before = await page.evaluate(() => document.documentElement.dataset.theme);
  await page.locator('#theme-toggle').click();
  await page.reload({ waitUntil: 'networkidle' });
  assert.notEqual(await page.evaluate(() => document.documentElement.dataset.theme), before, 'theme choice remembered');
  await page.close();
}

// The scene: lazy bundle, Pause holds, Play resumes, it ends on its final frame.
for (const spec of [{ name: 'desktop', width: 1280, height: 900 }, { name: 'compact', width: 358, height: 800 }]) {
  const page = await browser.newPage({ viewport: { width: spec.width, height: spec.height } });
  watch(page, 'scene-' + spec.name);
  await page.goto(base + '/#langspan', { waitUntil: 'networkidle' });
  await page.locator('.ls-scene').waitFor({ timeout: 15000 });
  await page.locator('.ls-stage-outer').scrollIntoViewIfNeeded();
  await page.locator('.ls-scene[data-step="1"]').waitFor({ timeout: 8000 });
  await page.getByRole('button', { name: 'Pause', exact: true }).click();
  await page.waitForTimeout(6000);
  assert.equal(await page.locator('.ls-scene').getAttribute('data-step'), '1', 'Pause holds the scene');
  await page.locator('.ls-stage-outer').screenshot({ path: shot(`scene-${spec.name}-paused`) });
  await page.getByRole('button', { name: 'Play', exact: true }).click();
  await page.locator('.ls-scene[data-step="2"]').waitFor({ timeout: 15000 });
  await page.locator('.ls-stage-outer').screenshot({ path: shot(`scene-${spec.name}-final`) });
  if (spec.name === 'compact') {
    const small = await page.evaluate(() => [...document.querySelectorAll('.ls-scene *')].filter((e) => {
      if (![...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return false;
      const box = e.getBoundingClientRect();
      if (!box.width || getComputedStyle(e).opacity === '0') return false;
      const stage = e.closest('.ss-stage');
      const m = getComputedStyle(stage).transform.match(/matrix\(([^,]+)/);
      return parseFloat(getComputedStyle(e).fontSize) * (m ? parseFloat(m[1]) : 1) < 12;
    }).map((e) => e.className || e.tagName));
    assert.deepEqual(small, [], 'compact scene text is at least 12px');
  }
  await page.getByRole('button', { name: 'Replay' }).first().click();
  await page.locator('.ls-scene[data-step="0"]').waitFor();
  await page.close();
}

// Reduced motion: the final frame, no playback controls; the About steps rest.
{
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' });
  watch(page, 'reduced');
  await page.goto(base + '/#langspan', { waitUntil: 'networkidle' });
  await page.locator('.ls-scene[data-step="2"]').waitFor({ timeout: 15000 });
  assert.equal(await page.getByRole('button', { name: 'Pause', exact: true }).count(), 0);
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  assert.equal(await page.locator('[data-flow-active]').count(), 0, 'About illustration rests under reduced motion');
  await page.screenshot({ path: shot('reduced-motion-about'), fullPage: true });
  await page.close();
}

// Without JavaScript the nav links still reach every view.
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled: false });
  const page = await ctx.newPage();
  await page.goto(base + '/', { waitUntil: 'load' });
  await page.locator('.quick-nav a[href="#work"]').click();
  assert.ok(await page.locator('#work.static-view').isVisible(), 'no-JS #work view');
  assert.equal(await page.locator('#result-output').isVisible(), false);
  await page.screenshot({ path: shot('nojs-work'), fullPage: true });
  await ctx.close();
}

for (const spec of [{ name: 'desktop', width: 1440, height: 900 }, { name: 'compact', width: 358, height: 760 }]) {
  for (const [name, path] of [['tour', 'tour.html#review'], ['archive', 'archive.html']]) {
    const p = await browser.newPage({ viewport: { width: spec.width, height: spec.height } });
    watch(p, name + '-' + spec.name);
    await p.goto(base + '/' + path, { waitUntil: 'networkidle' });
    await p.screenshot({ path: shot(name + '-' + spec.name), fullPage: true });
    assert.equal(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, name + '-' + spec.name + ' horizontal overflow');
    if (name === 'archive') {
      await p.locator('.study summary').first().click();
      assert.equal(await p.locator('.study[open]').count(), 1, 'archive disclosure opens');
    } else assert.ok(await p.locator('.chapter').count() > 2, 'tour chapters');
    await p.close();
  }
}
await browser.close();
assert.deepEqual(errors, [], 'browser errors');
console.log('PASS: routes x widths x themes without overflow, nav links and Back, remembered theme, lazy scene with Pause/Play/Replay, compact text >= 12px, reduced motion, no-JS routes, tour, archive.');
