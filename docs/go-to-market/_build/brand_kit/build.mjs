// Builds docs/go-to-market/FluxMuse_Brand_Kit.html from src/*.html partials.
// - injects the asset library table (from assets/ASSETS_INDEX.md + files found on disk)
// - injects the revenue chart figure only if assets/charts/revenue_by_stream_fy1_fy5.png exists
// - reports referenced image weight and missing files (image_report.json)
// Usage: node docs/go-to-market/_build/brand_kit/build.mjs
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const GTM = join(HERE, '..', '..');
const ASSETS = join(GTM, 'assets');
const OUT = join(GTM, 'FluxMuse_Brand_Kit.html');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const kb = (b) => (b >= 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.round(b / 1024) + ' KB');

function pngDims(file) {
  try {
    const b = readFileSync(file);
    if (b.toString('ascii', 12, 16) !== 'IHDR') return '';
    return `${b.readUInt32BE(16)}×${b.readUInt32BE(20)}`;
  } catch { return ''; }
}
function walk(dir) {
  const out = [];
  for (const n of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, n.name);
    if (n.isDirectory()) out.push(...walk(p));
    else if (/\.(png|jpe?g|webp|svg)$/i.test(n.name)) out.push(p);
  }
  return out;
}
function catOf(rel) {
  if (rel.startsWith('brand/')) return 'brand';
  if (rel.startsWith('infographics/')) return 'infographics';
  if (rel.startsWith('screenshots/composites/')) return 'composites';
  if (rel.startsWith('screenshots/crops/')) return 'crops';
  if (rel.startsWith('screenshots/')) return 'screenshots';
  if (rel.startsWith('charts/')) return 'charts';
  return 'other';
}

// ---- parse ASSETS_INDEX.md ----
const index = new Map();
const idxPath = join(ASSETS, 'ASSETS_INDEX.md');
if (existsSync(idxPath)) {
  for (const line of readFileSync(idxPath, 'utf8').split('\n')) {
    const m = line.match(/^\|\s*`([^`]+)`\s*\|(.*)\|\s*$/);
    if (!m) continue;
    const cols = m[2].split('|').map((c) => c.trim());
    index.set(m[1], { px: cols[0] || '', ground: cols[1] || '', what: cols[2] || '', use: cols[3] || '' });
  }
}

// ---- asset rows ----
const CAT_LABEL = { brand: 'Brand', infographics: 'Infographics & workflows', composites: 'Device composites', screenshots: 'Product screenshots', crops: 'Screenshot crops', charts: 'Charts', other: 'Other' };
const files = existsSync(ASSETS) ? walk(ASSETS).map((p) => relative(ASSETS, p).split('\\').join('/')) : [];
const all = new Set([...files, ...index.keys()]);
const byCat = {};
for (const rel of [...all].sort()) (byCat[catOf(rel)] ||= []).push(rel);

let rows = '';
for (const cat of ['brand', 'infographics', 'composites', 'screenshots', 'crops', 'charts', 'other']) {
  const list = byCat[cat];
  if (!list || !list.length) continue;
  rows += `<tr class="cat" data-cat="${cat}"><td colspan="6">${CAT_LABEL[cat]} · ${list.length}</td></tr>\n`;
  for (const rel of list) {
    const abs = join(ASSETS, rel);
    const onDisk = existsSync(abs);
    const meta = index.get(rel) || {};
    const size = onDisk ? kb(statSync(abs).size) : '—';
    const px = meta.px || (onDisk ? pngDims(abs) : '');
    const text = `${meta.what || ''} ${meta.use || ''}`;
    const internal = /internal (reference|only)/i.test(meta.use || '') || /SHOWS/.test(meta.what || '');
    let status;
    if (!onDisk) status = '<span class="chip bad">Missing</span>';
    else if (internal) status = '<span class="chip bad">Internal only</span>';
    else if (/SnapScan/i.test(text)) status = '<span class="chip warn">Shows SnapScan</span>';
    else if (/_guides\.png$/.test(rel)) status = '<span class="chip warn">Planning only</span>';
    else if (!index.has(rel)) status = '<span class="chip acc">New · not indexed</span>';
    else status = '<span class="chip ok">OK</span>';
    rows += `<tr data-cat="${cat}" data-internal="${internal ? 1 : 0}"><td><a href="assets/${esc(rel)}">${esc(rel.replace(/^(screenshots\/)?(composites|crops)\//, '$2/'))}</a></td><td class="r">${esc(px)}</td><td class="r">${size}</td><td>${status}</td><td>${esc(meta.what || (onDisk ? 'Added after the index was written; see ASSETS_INDEX.md once updated.' : ''))}</td><td>${esc(meta.use || '')}</td></tr>\n`;
  }
}

// ---- charts (only if present) ----
const chartRel = 'charts/revenue_by_stream_fy1_fy5.png';
const chartHtml = existsSync(join(ASSETS, chartRel))
  ? `\n  <div class="sub"><figure class="fig"><div class="frame"><img class="r169" src="assets/${chartRel}" width="${(pngDims(join(ASSETS, chartRel)).split('×')[0]) || 1920}" height="${(pngDims(join(ASSETS, chartRel)).split('×')[1]) || 1080}" loading="lazy" alt="Revenue by stream, FY1 to FY5, from the financial model"></div><figcaption><span>Model chart in house style: R m units, direct labels, Flux Orange lead series.</span><code>charts/revenue_by_stream_fy1_fy5.png</code></figcaption></figure></div>\n`
  : '';

// ---- assemble ----
const SRC = join(HERE, 'src');
let html = readdirSync(SRC).filter((f) => f.endsWith('.html')).sort().map((f) => readFileSync(join(SRC, f), 'utf8')).join('\n');
html = html.replace(/<!--ASSET-TABLE:START-->[\s\S]*?<!--ASSET-TABLE:END-->/, `<!--ASSET-TABLE:START-->\n${rows}<!--ASSET-TABLE:END-->`);
html = html.replace(/<!--CHARTS:START-->[\s\S]*?<!--CHARTS:END-->/, `<!--CHARTS:START-->${chartHtml}<!--CHARTS:END-->`);
writeFileSync(OUT, html);

// ---- referenced image report ----
const refs = new Set();
for (const m of html.matchAll(/<(?:img|source)\b[^>]*?\s(?:src|srcset)="(assets\/[^"]+)"/g)) refs.add(m[1]);
let total = 0, darkOnly = 0; const missing = []; const present = [];
for (const r of [...refs].sort()) {
  const abs = join(GTM, r);
  if (existsSync(abs)) {
    const s = statSync(abs).size; total += s; present.push([r, s]);
    if (/_dark\.png$|_night\.png$/.test(r) && html.includes(`srcset="${r}"`)) darkOnly += s;
  } else missing.push(r);
}
const report = { built: new Date().toISOString(), output: relative(GTM, OUT), referenced: refs.size, present: present.length, totalBytes: total, total: kb(total), darkVariantBytes: darkOnly, darkVariants: kb(darkOnly), missing, assetRows: [...all].length };
writeFileSync(join(HERE, 'image_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
