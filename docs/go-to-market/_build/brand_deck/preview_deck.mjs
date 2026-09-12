// Render a pptx layout JSON (from qa_deck.py) to per-slide PNGs in headless Chrome, using the real
// Poppins/Inter web fonts, and measure text overflow / table growth.
// Usage: node preview_deck.mjs layout.json outDir   -> outDir/slide-NN.png + outDir/overflow.json
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { launch } from '../lib/cdp.mjs';

const [, , layoutPath, outDir] = process.argv;
const L = JSON.parse(readFileSync(layoutPath, 'utf8'));
mkdirSync(outDir, { recursive: true });
const PX = 96; // px per inch
const PT = 96 / 72;
// Single-line height factors approximating PowerPoint line spacing per font (conservative).
const LH = { Poppins: 1.5, Inter: 1.25 };
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function runsHTML(paras, dflt = {}) {
  return paras.map((p) => {
    const size = Math.max(...p.runs.map((r) => r.size), 8);
    const font = p.runs[0]?.font || 'Inter';
    const lh = (LH[font] || 1.2) * (p.lsp || 1);
    const al = { l: 'left', ctr: 'center', r: 'right', just: 'justify' }[p.align] || 'left';
    const inner = p.runs.map((r) => `<span style="font-family:'${r.font}',Arial;font-size:${r.size * PT}px;font-weight:${r.bold ? 700 : 400};color:#${r.color || dflt.color || '20242B'};letter-spacing:${(r.spc || 0) * PT}px">${esc(r.text)}</span>`).join('');
    return `<p style="margin:0 0 ${(p.space_after || 0) * PT}px 0;line-height:${lh};text-align:${al};font-size:${size * PT}px">${inner || '&nbsp;'}</p>`;
  }).join('');
}

function slideHTML(s) {
  let h = '';
  s.els.forEach((e, i) => {
    const st = `left:${e.x * PX}px;top:${e.y * PX}px;width:${e.w * PX}px;height:${e.h * PX}px`;
    if (e.type === 'pic') {
      const [l, t, r, b] = e.crop;
      const iw = (e.w * PX) / (1 - l - r), ih = (e.h * PX) / (1 - t - b);
      h += `<div class="e" style="${st};overflow:hidden;${e.rounded ? `border-radius:${Math.min(e.w, e.h) * PX * 0.1667}px` : ''}"><img src="file://${e.src}" style="position:absolute;width:${iw}px;height:${ih}px;left:${-l * iw}px;top:${-t * ih}px"></div>`;
    } else if (e.type === 'shape') {
      let rad = '0';
      if (e.prst === 'roundRect') rad = `${(e.adj ?? 0.1667) * Math.min(e.w, e.h) * PX}px`;
      if (e.prst === 'ellipse') rad = '50%';
      const border = e.line ? `border:${e.line.w * PT}px ${e.line.dash ? 'dashed' : 'solid'} #${e.line.color};` : '';
      const clip = e.prst === 'downArrow' ? 'clip-path:polygon(25% 0,75% 0,75% 50%,100% 50%,50% 100%,0 50%,25% 50%);' : '';
      h += `<div class="e" style="${st};box-sizing:border-box;background:${e.fill ? '#' + e.fill : 'transparent'};border-radius:${rad};${border}${clip}"></div>`;
      if (e.paras) h += textBox(e, i);
    } else if (e.type === 'text') {
      h += textBox(e, i);
    } else if (e.type === 'table') {
      const cols = e.cols.map((c) => `<col style="width:${c * PX}px">`).join('');
      const rows = e.rows.map((r) => `<tr style="height:${r.h * PX}px">${r.cells.map((c) => `<td style="background:#${c.fill || 'FFFFFF'};padding:${0.04 * PX}px ${0.12 * PX}px;border-bottom:1px solid #E3E6EA;vertical-align:middle;overflow-wrap:break-word">${runsHTML(c.paras)}</td>`).join('')}</tr>`).join('');
      h += `<table class="e tbl" data-i="${i}" data-h="${e.h * PX}" style="left:${e.x * PX}px;top:${e.y * PX}px;width:${e.w * PX}px;border-collapse:collapse;table-layout:fixed">${cols}${rows}</table>`;
    }
  });
  return `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Inter:wght@400;700&display=block" rel="stylesheet">
<style>html,body{margin:0;width:${L.w * PX}px;height:${L.h * PX}px;overflow:hidden;background:#${s.bg}}
.e{position:absolute}.tb{display:flex;flex-direction:column}.tb .in{width:100%;overflow-wrap:break-word}
.tb.m{justify-content:center}.tb.b{justify-content:flex-end}</style></head><body>${h}</body></html>`;
}

function textBox(e, i) {
  const a = { t: 't', ctr: 'm', b: 'b' }[e.anchor] || 't';
  return `<div class="e tb ${a}" data-i="${i}" data-name="${esc(e.name)}" style="left:${e.x * PX}px;top:${e.y * PX}px;width:${e.w * PX}px;height:${e.h * PX}px"><div class="in">${runsHTML(e.paras)}</div></div>`;
}

const HERE = dirname(fileURLToPath(import.meta.url));
const b = await launch({ port: 9371 });
const report = [];
try {
  await b.setViewport(Math.round(L.w * PX), Math.round(L.h * PX), 1.25);
  for (const s of L.slides) {
    const file = join(outDir, `slide-${String(s.n).padStart(2, '0')}.html`);
    writeFileSync(file, slideHTML(s));
    await b.goto('file://' + file, 250);
    const res = await b.evaluate(`(() => {
      const out = [];
      document.querySelectorAll('.tb').forEach((d) => {
        const inner = d.firstElementChild;
        const over = inner.scrollHeight - d.clientHeight;
        const wide = inner.scrollWidth - d.clientWidth;
        if (over > 2) out.push(d.dataset.name + ' overflows by ' + (over / 96).toFixed(2) + ' in');
        if (wide > 2) out.push(d.dataset.name + ' too wide by ' + (wide / 96).toFixed(2) + ' in');
      });
      document.querySelectorAll('.tbl').forEach((t) => {
        const grow = t.getBoundingClientRect().height - Number(t.dataset.h);
        if (grow > 3) out.push('table grows by ' + (grow / 96).toFixed(2) + ' in (rows expand)');
      });
      return out;
    })()`);
    res.forEach((msg) => report.push({ slide: s.n, msg }));
    await b.shot(join(outDir, `slide-${String(s.n).padStart(2, '0')}.png`), { clip: { x: 0, y: 0, width: L.w * PX, height: L.h * PX } });
  }
} finally { await b.close(); }
writeFileSync(join(outDir, 'overflow.json'), JSON.stringify(report, null, 2));
console.log(`rendered ${L.slides.length} slides, ${report.length} overflow findings`);
