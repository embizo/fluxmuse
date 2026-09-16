// Rasterise the shared Lucide-style stroke icons (../lib/icons.mjs) to transparent PNGs
// for the brand pitch deck: one CDP screenshot of a grid, sliced with Pillow.
// Usage: node render_icons.mjs   (writes icons/<name>_<colour>.png, 256 px)
// Env: PYTHON (python with Pillow), CDP_UDD (scratch Chrome profile dir).
import { icon } from '../lib/icons.mjs';
import { launch, renderFile } from '../lib/cdp.mjs';
import { writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, 'icons');
mkdirSync(OUT, { recursive: true });

const NAMES = ['chat', 'bag', 'cart', 'card', 'checkCircle', 'megaphone', 'chart', 'target', 'pen', 'send',
  'heart', 'link', 'users', 'briefcase', 'shield', 'zap', 'refresh', 'globe', 'calendar', 'search', 'trend',
  'phone', 'file', 'x', 'check', 'layers', 'sparkles', 'qr', 'mail', 'plug', 'wallet', 'clock', 'flag'];
const COLOURS = { deep: '#C24E00', orange: '#FF6A00', ink: '#20242B', white: '#FFFFFF' };
const CELL = 128; // CSS px; rendered at DPR 2 => 256 px per icon

const cols = NAMES.length;
const rows = Object.keys(COLOURS).length;
let cells = '';
Object.values(COLOURS).forEach((c, r) => {
  NAMES.forEach((n, i) => {
    cells += `<div style="position:absolute;left:${i * CELL + 8}px;top:${r * CELL + 8}px;line-height:0">${icon(n, CELL - 16, c, 2)}</div>`;
  });
});
const html = `<!doctype html><html><head><style>html,body{margin:0;background:transparent}</style></head><body>${cells}</body></html>`;
const htmlPath = join(OUT, '_grid.html');
writeFileSync(htmlPath, html);
const shot = join(OUT, '_grid.png');

const b = await launch({ port: 9361 });
try {
  await renderFile(b, htmlPath, shot, { width: cols * CELL, height: rows * CELL, dpr: 2, transparent: true, settle: 200 });
} finally { await b.close(); }

const py = process.env.PYTHON || 'python3';
execFileSync(py, ['-c', `
import sys
from PIL import Image
g = Image.open(sys.argv[1]).convert('RGBA')
names = sys.argv[2].split(',')
colours = sys.argv[3].split(',')
C = ${CELL * 2}
for r, c in enumerate(colours):
    for i, n in enumerate(names):
        g.crop((i*C, r*C, (i+1)*C, (r+1)*C)).save(sys.argv[4] + f"/{n}_{c}.png")
`, shot, NAMES.join(','), Object.keys(COLOURS).join(','), OUT], { stdio: 'inherit' });
console.log(`icons: ${NAMES.length * rows} PNGs in ${OUT}`);
