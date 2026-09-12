// Shared helpers: HTML page shell, node-network motif, corner brand mark, batch render.
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { launch, renderFile } from './cdp.mjs';

export const BUILD = join(dirname(fileURLToPath(import.meta.url)), '..');
export const ASSETS = join(BUILD, '..', 'assets');

export const C = {
  orange: '#FF6A00', glow: '#FF8533', tint: '#FFF4EB', slate: '#37474F', ink: '#20242B',
  night: '#0F1419', paper: '#FFFFFF', mist: '#F3F4F6',
  violet: '#6A2DC8', blue: '#1E88E5', teal: '#00A6A6', green: '#43A047',
  yellow: '#FDD835', amber: '#FFA000', red: '#E53935', magenta: '#D81B60',
};

// deterministic PRNG so the motif is identical on every rebuild
export function rng(seed = 7) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

// Low-poly node network echoing the logo's lower half. Returns an <svg> string.
export function netSVG(w, h, { seed = 11, n = 26, color = 'currentColor', opacity = 0.12, region = null, r = 3.2 } = {}) {
  const rand = rng(seed);
  const [x0, y0, x1, y1] = region || [0, 0, w, h];
  const pts = Array.from({ length: n }, () => [x0 + rand() * (x1 - x0), y0 + rand() * (y1 - y0)]);
  const lines = [];
  pts.forEach((p, i) => {
    const d = pts.map((q, j) => [j, Math.hypot(p[0] - q[0], p[1] - q[1])]).filter(([j]) => j !== i).sort((a, b) => a[1] - b[1]).slice(0, 3);
    d.forEach(([j]) => { if (j > i) lines.push([p, pts[j]]); });
  });
  return `<svg class="netbg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="true" style="opacity:${opacity}">
  ${lines.map(([a, b]) => `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${color}" stroke-width="1.4"/>`).join('')}
  ${pts.map((p) => `<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="${r}" fill="${color}"/>`).join('')}</svg>`;
}

// Page shell. `rel` = relative path from the html file dir to assets/ for image refs.
export function page({ title, w, h, dark = false, body, css = '', bg }) {
  return `<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><title>${title}</title>
<link rel="stylesheet" href="../lib/fm.css">
<style>html,body{width:${w}px;height:${h}px;overflow:hidden;${bg ? `background:${bg};` : ''}} .canvas{width:${w}px;height:${h}px;${bg ? `background:${bg};` : ''}} ${css}</style></head>
<body class="${dark ? 'dark' : ''}"><div class="canvas">${body}</div></body></html>`;
}

// corner brand mark: icon + typeset "FLUXMUSE" (the wordmark colours from the brand system)
export function brandmark({ pos = 'right:56px;bottom:40px', icon = '../../assets/brand/fluxmuse-icon-512.png', size = 44 } = {}) {
  return `<div class="brandmark" style="${pos}"><img src="${icon}" style="height:${size}px" alt=""><span><span class="f">FLUX</span><span class="m">MUSE</span></span></div>`;
}

// Render jobs: [{name, dir, html, w, h, dpr, transparent, out}]
export async function renderJobs(jobs, { port = 9340 } = {}) {
  const b = await launch({ port, userDataDir: process.env.CDP_UDD ? `${process.env.CDP_UDD}-${port}` : undefined });
  try {
    for (const j of jobs) {
      const file = join(BUILD, j.dir, j.name + '.html');
      mkdirSync(dirname(file), { recursive: true });
      writeFileSync(file, j.html);
      await renderFile(b, file, j.out, { width: j.w, height: j.h, dpr: j.dpr ?? 2, transparent: !!j.transparent, settle: j.settle ?? 500 });
      console.log('rendered', relative(ASSETS, j.out));
    }
  } finally { await b.close(); }
}
