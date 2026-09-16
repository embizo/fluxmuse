// Exports docs/go-to-market/01_Brand_Kit/FluxMuse_Brand_Kit.pdf from FluxMuse_Brand_Kit.html.
// A4 landscape (from @page CSS), light theme forced, backgrounds printed, nav hidden by print CSS.
// Re-run after assets change:  node build.mjs && node export_pdf.mjs
// Optional: CDP_UDD=/scratch/profile to choose the Chrome profile directory.
import { launch } from '../lib/cdp.mjs';
import { writeFileSync, mkdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const GTM = join(HERE, '..', '..');
const FILE = join(GTM, 'FluxMuse_Brand_Kit.html');
const OUT = join(GTM, '01_Brand_Kit', 'FluxMuse_Brand_Kit.pdf');

const b = await launch({ port: 9445 });
try {
  await b.setViewport(1280, 900, 1, false);
  await b.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
  await b.goto('file://' + FILE, 800);
  // Force light theme, load every image eagerly, wait until all have settled (missing ones error out).
  const imgs = await b.evaluate(`(async () => {
    document.documentElement.setAttribute('data-theme', 'light');
    const list = [...document.images];
    list.forEach(i => { i.loading = 'eager'; });
    await new Promise(r => setTimeout(r, 50));
    await Promise.race([
      Promise.all(list.map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))),
      new Promise(r => setTimeout(r, 60000)),
    ]);
    await document.fonts.ready;
    return { total: list.length, broken: list.filter(i => !i.naturalWidth).map(i => i.getAttribute('src')) };
  })()`);
  console.log('images', imgs.total, 'broken', imgs.broken.length, imgs.broken);
  await b.sleep(800);
  const { stream } = await b.send('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true, transferMode: 'ReturnAsStream',
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font:8px Arial,sans-serif;color:#5B6570;padding:0 13mm;display:flex;justify-content:space-between"><span>FluxMuse Brand Kit v1.0 · September 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    marginTop: 0.43, marginBottom: 0.5,
  });
  const chunks = [];
  for (;;) {
    const r = await b.send('IO.read', { handle: stream, size: 8 * 1024 * 1024 });
    chunks.push(Buffer.from(r.data, r.base64Encoded ? 'base64' : 'utf8'));
    if (r.eof) break;
  }
  await b.send('IO.close', { handle: stream });
  mkdirSync(dirname(OUT), { recursive: true });
  const pdf = Buffer.concat(chunks);
  writeFileSync(OUT, pdf);
  const pages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  console.log('wrote', OUT, (statSync(OUT).size / 1048576).toFixed(1) + ' MB', pages ? pages + ' pages' : '');
} finally { await b.close(); }
