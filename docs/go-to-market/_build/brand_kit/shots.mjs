// QA screenshots of FluxMuse_Brand_Kit.html at desktop/mobile in light/dark.
// Usage: CDP_UDD=/some/scratch/profile node shots.mjs <outDir> [ids comma-separated]
import { launch } from '../lib/cdp.mjs';
import { join, dirname } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const FILE = join(HERE, '..', '..', 'FluxMuse_Brand_Kit.html');
const OUT = process.argv[2] || join(HERE, 'qa');
const IDS = (process.argv[3] || 'cover,story,voice,messaging,logo,colour,type,markets,pricing,templates,assets').split(',');
const CONFIGS = (process.env.CONFIGS || 'd-light,d-dark,m-light,m-dark').split(',');

const b = await launch({ port: 9444 });
try {
  for (const c of CONFIGS) {
    const mobile = c.startsWith('m');
    const scheme = c.endsWith('dark') ? 'dark' : 'light';
    const [w, h] = mobile ? [390, 844] : [1440, 900];
    await b.setViewport(w, h, 1, mobile);
    await b.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: scheme }] });
    await b.goto('file://' + FILE, 1200);
    await b.evaluate(`document.documentElement.style.scrollBehavior='auto'`);
    const info = await b.evaluate(`(() => {
      const vw = document.documentElement.clientWidth;
      const wide = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.right > vw + 1 && getComputedStyle(e).position !== 'fixed' && !e.closest('.tbl,.rail nav,pre,.cover .net'); }).slice(0, 8).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right));
      return { scrollW: document.documentElement.scrollWidth, vw, height: document.documentElement.scrollHeight, wide };
    })()`);
    console.log(c, JSON.stringify(info));
    for (const id of IDS) {
      await b.evaluate(`(() => { const el = document.getElementById(${JSON.stringify(id)}); window.scrollTo(0, el ? el.getBoundingClientRect().top + scrollY - ${mobile ? 56 : 0} : 0); })()`);
      await b.sleep(500);
      const { data } = await b.send('Page.captureScreenshot', { format: 'png' });
      mkdirSync(OUT, { recursive: true });
      writeFileSync(join(OUT, `${c}_${id}.png`), Buffer.from(data, 'base64'));
    }
  }
} finally { await b.close(); }
