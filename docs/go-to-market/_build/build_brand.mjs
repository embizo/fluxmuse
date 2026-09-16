// Build brand-kit PNGs into ../assets/brand from HTML pages written to ./brand/*.html
// Usage: node build_brand.mjs [nameFilter]
import { join } from 'node:path';
import { page, netSVG, brandmark, renderJobs, ASSETS, C } from './lib/page.mjs';
import { icon } from './lib/icons.mjs';

const OUT = join(ASSETS, 'brand');
const A = '../../assets/brand/';
const ICON = A + 'fluxmuse-icon-512.png', LIGHT = A + 'fluxmuse-logo-light.png', DARK = A + 'fluxmuse-logo-dark.png';

// WCAG 2.x contrast
const lum = (h) => { const v = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const verdict = (r) => (r >= 7 ? ['AAA', 'pass'] : r >= 4.5 ? ['AA', 'pass'] : r >= 3 ? ['AA large text only', 'warn'] : ['Fail', 'fail']);
const rgbOf = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const hslOf = (h) => {
  const [r, g, b] = rgbOf(h).map((v) => v / 255); const mx = Math.max(r, g, b), mn = Math.min(r, g, b); const l = (mx + mn) / 2; let hh = 0, s = 0;
  if (mx !== mn) { const d = mx - mn; s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); hh = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hh *= 60; }
  return `${Math.round(hh)} ${Math.round(s * 100)}% ${Math.round(l * 100)}%`;
};

const jobs = [];
const add = (name, w, h, html, opts = {}) => jobs.push({ name, dir: 'brand', html, w, h, out: join(OUT, name + '.png'), ...opts });

// ---------- icon squares (1024×1024) ----------
for (const [n, bg] of [['night', C.night], ['white', C.paper], ['orange', C.orange]]) {
  add(`fluxmuse-icon-on-${n}-1024`, 512, 512, page({ title: 'icon ' + n, w: 512, h: 512, bg, body: `<img src="${ICON}" style="position:absolute;left:86px;top:86px;width:340px;height:340px">` }));
}

// ---------- logo lockups 1600×600 ----------
add('fluxmuse-logo-lockup-light-1600x600', 800, 300, page({ title: 'lockup light', w: 800, h: 300, bg: C.paper,
  body: `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><img src="${LIGHT}" style="height:190px"></div>` }));
add('fluxmuse-logo-lockup-dark-1600x600', 800, 300, page({ title: 'lockup dark', w: 800, h: 300, bg: C.night,
  body: `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><img src="${DARK}" style="height:170px"></div>` }));

// ---------- sheet header helper ----------
const head = (eyebrow, title, sub = '') => `<div style="position:absolute;left:88px;top:64px;right:88px">
  <div class="eyebrow">${eyebrow}</div><h1 class="title" style="font-size:54px;margin-top:10px">${title}</h1>${sub ? `<div class="sub" style="margin-top:10px;font-size:24px">${sub}</div>` : ''}</div>`;

// ---------- clear space & minimum size ----------
{
  const LH = 300, S = LH / 244, LW = 640 * S, X = Math.round(41 * S); // x = wordmark cap height (FLUX letters 41px tall in the 244px source)
  const capTop = 156 * S;
  const bx = 150, by = 300; // logo top-left inside the left panel
  const css = `.lab{font:600 24px Inter,Arial;color:${C.ink}} .small{font:400 22px Inter,Arial;color:#5B6570}`;
  const body = `${head('Brand kit · Logo', 'Clear space &amp; minimum size', 'Keep a margin of <b>x</b> on every side, where <b>x</b> is the cap height of the FLUXMUSE wordmark.')}
  <div class="card" style="position:absolute;left:88px;top:250px;width:1110px;height:640px;background:${C.mist};border:none"></div>
  <div style="position:absolute;left:${bx - X}px;top:${by - X}px;width:${LW + 2 * X}px;height:${LH + 2 * X}px;background:repeating-linear-gradient(45deg, rgba(255,106,0,.16) 0 10px, rgba(255,106,0,.05) 10px 20px);outline:2px dashed ${C.orange}"></div>
  <div style="position:absolute;left:${bx}px;top:${by}px;width:${LW}px;height:${LH}px;background:#fff;outline:2px dashed ${C.slate}"></div>
  <img src="${LIGHT}" style="position:absolute;left:${bx}px;top:${by}px;height:${LH}px">
  <svg style="position:absolute;left:0;top:0" width="1920" height="1080">
    <g stroke="${C.orange}" stroke-width="3" fill="none">
      <!-- cap height bracket beside the F -->
      <path d="M${bx - 20} ${by + capTop} h-14 v${X} h14"/>
      <!-- margin brackets -->
      <path d="M${bx + LW / 2} ${by - X} v${X}"/><path d="M${bx + LW / 2 - 10} ${by - X} h20 M${bx + LW / 2 - 10} ${by} h20"/>
      <path d="M${bx + LW} ${by + LH / 2} h${X}"/><path d="M${bx + LW} ${by + LH / 2 - 10} v20 M${bx + LW + X} ${by + LH / 2 - 10} v20"/>
      <path d="M${bx + LW / 2} ${by + LH} v${X}"/><path d="M${bx + LW / 2 - 10} ${by + LH} h20 M${bx + LW / 2 - 10} ${by + LH + X} h20"/>
    </g>
    <g font-family="Poppins, Arial" font-weight="700" font-size="30" fill="${C.orange}">
      <text x="${bx - 60}" y="${by + capTop + X / 2 + 10}" text-anchor="end">x</text>
      <text x="${bx + LW / 2 + 20}" y="${by - X / 2 + 10}">x</text>
      <text x="${bx + LW + X / 2}" y="${by + LH / 2 - 22}" text-anchor="middle">x</text>
      <text x="${bx + LW / 2 + 20}" y="${by + LH + X / 2 + 10}">x</text>
    </g>
  </svg>
  <div class="small" style="position:absolute;left:130px;top:${by + LH + X + 48}px;width:1030px">Shaded area = protected clear space. No text, edges, other logos or busy imagery may enter it. The same rule applies to <b>fluxmuse-logo-dark.png</b> on dark grounds.</div>

  <div style="position:absolute;left:1250px;top:250px;width:582px">
    <div class="lab" style="font-size:28px;font-family:Poppins">Minimum size</div>
    <div class="small" style="margin-top:6px">Below these sizes the wordmark and the icon's node lines stop reading.</div>
    <div class="card" style="margin-top:26px;padding:28px;display:flex;align-items:center;gap:28px">
      <div style="width:240px;height:110px;display:flex;align-items:center;justify-content:center;background:${C.mist};border-radius:12px"><img src="${LIGHT}" style="width:200px"></div>
      <div><div class="lab">Full logo</div><div class="small">200 px wide on screen<br>40 mm wide in print</div></div>
    </div>
    <div class="card" style="margin-top:20px;padding:28px;display:flex;align-items:center;gap:28px">
      <div style="width:240px;height:110px;display:flex;align-items:center;justify-content:center;gap:26px;background:${C.mist};border-radius:12px"><img src="${ICON}" style="width:48px"><img src="${ICON}" style="width:32px"><img src="${ICON}" style="width:24px"></div>
      <div><div class="lab">Icon only</div><div class="small">24 px on screen (favicon)<br>10 mm in print</div></div>
    </div>
    <div class="card" style="margin-top:20px;padding:24px 28px">
      <div class="lab">Icon clear space</div>
      <div class="small" style="margin-top:4px">Pad the icon by ¼ of its height on every side, e.g. on app icons and avatars.</div>
    </div>
  </div>
  ${brandmark({ pos: 'right:88px;bottom:30px', size: 36 })}`;
  add('logo-clear-space-minimum-size', 1920, 1080, page({ title: 'clear space', w: 1920, h: 1080, body, css }));
}

// ---------- misuse sheet ----------
{
  const tiles = [
    ['do', 'Light logo on white or Mist', `background:${C.paper}`, `<img src="${LIGHT}" style="height:120px">`],
    ['do', 'Dark logo on Night', `background:${C.night}`, `<img src="${DARK}" style="height:110px">`],
    ['dont', 'Don’t stretch or squash', `background:${C.paper}`, `<img src="${LIGHT}" style="height:120px;transform:scale(1.35,0.7)">`],
    ['dont', 'Don’t recolour', `background:${C.paper}`, `<img src="${LIGHT}" style="height:120px;filter:hue-rotate(150deg) saturate(1.3)">`],
    ['dont', 'Don’t use low-contrast grounds', `background:${C.slate}`, `<img src="${LIGHT}" style="height:120px">`],
    ['dont', 'Don’t place on busy photos or patterns', `background:radial-gradient(circle at 20% 30%, #E53935 0 60px, transparent 61px), radial-gradient(circle at 70% 60%, #1E88E5 0 80px, transparent 81px), radial-gradient(circle at 45% 85%, #FDD835 0 50px, transparent 51px), repeating-linear-gradient(60deg, #43A047 0 18px, #FFA000 18px 36px, #6A2DC8 36px 54px)`, `<img src="${LIGHT}" style="height:120px">`],
    ['dont', 'Don’t rotate', `background:${C.paper}`, `<img src="${LIGHT}" style="height:120px;transform:rotate(-14deg)">`],
    ['dont', 'Don’t add outlines, glows or shadows', `background:${C.paper}`, `<img src="${LIGHT}" style="height:120px;filter:drop-shadow(3px 0 0 #1E88E5) drop-shadow(-3px 0 0 #1E88E5) drop-shadow(0 3px 0 #1E88E5) drop-shadow(0 -3px 0 #1E88E5) drop-shadow(0 10px 12px rgba(0,0,0,.45))">`],
  ];
  const tw = (1920 - 176 - 3 * 32) / 4;
  const body = `${head('Brand kit · Logo', 'Logo do’s and don’ts', 'Use the supplied files as they are. Never redraw, distort or restyle them.')}
  <div style="position:absolute;left:88px;top:250px;display:grid;grid-template-columns:repeat(4,${tw}px);gap:34px 32px">
  ${tiles.map(([k, cap, bg, img]) => `<div>
    <div style="height:280px;border-radius:20px;overflow:hidden;display:flex;align-items:center;justify-content:center;${bg};border:1.5px solid #E3E6EA">${img}</div>
    <div style="display:flex;align-items:flex-start;gap:12px;margin-top:14px">
      <span style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px 4px 8px;border-radius:999px;font:700 20px Inter;${k === 'do' ? 'background:#E6F4EA;color:#1E6B2A' : 'background:#FDECEA;color:#B3261E'}">${icon(k === 'do' ? 'check' : 'x', 22, k === 'do' ? '#1E6B2A' : '#B3261E', 3)}${k === 'do' ? 'Do' : 'Don’t'}</span>
      <span style="font:600 22px Inter;color:${C.ink}">${cap.replace(/^Don’t /, '')}</span></div></div>`).join('')}
  </div>${brandmark({ pos: 'right:88px;top:74px', size: 36 })}`;
  add('logo-misuse-donts', 1920, 1080, page({ title: 'misuse', w: 1920, h: 1080, body }));
}

// ---------- colour palette ----------
{
  // HSL values quoted from the facts file where it lists them (source CSS tokens); computed otherwise.
  const factHSL = { '#FF6A00': '24 100% 50%', '#FF8533': '24 100% 60%', '#FFF4EB': '24 100% 96%', '#20242B': '220 15% 15%', '#F3F4F6': '220 15% 96%' };
  const sw = (name, role, hex, w, h, blockH, big = false) => {
    const [r, g, b] = rgbOf(hex); const light = lum(hex) > 0.5;
    return `<div style="width:${w}px;height:${h}px;border-radius:20px;overflow:hidden;background:#fff;border:1.5px solid #E3E6EA;display:flex;flex-direction:column">
      <div style="height:${blockH}px;background:${hex};${light ? 'border-bottom:1.5px solid #E3E6EA;' : ''}position:relative">
        ${big ? `<div style="position:absolute;left:24px;bottom:16px;font:700 30px Poppins;color:${C.night}">${name}</div>` : ''}</div>
      <div style="padding:${big ? '14px 24px' : '12px 18px'};font:400 ${big ? 21 : 20}px/1.35 Inter;color:#5B6570">
        ${big ? `<div style="font:600 21px Inter;color:${C.ink}">${role}</div>` : `<div style="font:700 22px Poppins;color:${C.ink}">${name}</div>${role ? `<div style="font:500 19px Inter;color:#5B6570;margin-top:-2px">${role}</div>` : ''}`}
        <div style="font-weight:700;color:${C.ink};margin-top:2px">${hex}</div>
        <div>RGB ${r}, ${g}, ${b}</div><div>HSL ${factHSL[hex] || hslOf(hex)}</div></div></div>`;
  };
  const body = `${head('Brand kit · Colour', 'Colour palette')}
  <div style="position:absolute;left:88px;top:196px;display:flex;gap:24px">
    ${sw('Flux Orange', 'Primary · CTAs, highlights, charts', C.orange, 520, 290, 140, true)}
    ${sw('Orange glow', 'Hover, gradients', C.glow, 280, 290, 116)}
    ${sw('Orange tint', 'Soft fills, chips', C.tint, 280, 290, 116)}
    ${sw('Slate', 'Wordmark “MUSE”', C.slate, 280, 290, 116)}
    ${sw('Ink', 'Text on light', C.ink, 280, 290, 116)}
  </div>
  <div style="position:absolute;left:88px;top:510px;display:flex;gap:24px">
    ${sw('Night', 'Dark surface', C.night, 280, 270, 100)}
    ${sw('Paper', 'Light surface', C.paper, 280, 270, 100)}
    ${sw('Mist', 'Panels, dividers', C.mist, 280, 270, 100)}
    <div style="width:844px;height:270px;border-radius:20px;background:${C.mist};padding:26px 30px;font:400 22px/1.45 Inter;color:${C.ink}">
      <div style="font:700 26px Poppins;margin-bottom:8px">Proportion</div>
      Neutrals carry most of every layout (Paper/Mist or Night). Flux Orange is the one lead accent. The Muse spectrum is for small category accents and illustrations only, never for body text.
      <div style="display:flex;height:22px;border-radius:11px;overflow:hidden;margin-top:18px">
        <div style="flex:60;background:${C.paper};border:1.5px solid #D5DAE0"></div><div style="flex:20;background:${C.night}"></div><div style="flex:10;background:${C.slate}"></div><div style="flex:8;background:${C.orange}"></div><div style="flex:2;background:linear-gradient(90deg,${C.violet},${C.blue},${C.teal},${C.green},${C.yellow},${C.amber},${C.red},${C.magenta})"></div></div>
    </div>
  </div>
  <div style="position:absolute;left:88px;top:806px;font:700 24px Poppins;color:${C.ink}">Muse spectrum <span style="font:500 21px Inter;color:#5B6570">· from the icon · accents only</span></div>
  <div style="position:absolute;left:88px;top:848px;display:flex;gap:16px">
    ${[['Violet', C.violet], ['Blue', C.blue], ['Teal', C.teal], ['Green', C.green], ['Yellow', C.yellow], ['Amber', C.amber], ['Red', C.red], ['Magenta', C.magenta]].map(([n, h]) => {
      const [r, g, b] = rgbOf(h); return `<div style="width:204px;height:200px;border-radius:18px;overflow:hidden;background:#fff;border:1.5px solid #E3E6EA">
      <div style="height:62px;background:${h}"></div><div style="padding:8px 12px;white-space:nowrap;letter-spacing:-0.01em;font:400 18px/1.36 Inter;color:#5B6570"><div style="font:700 21px Poppins;color:${C.ink}">${n}</div><div style="font-weight:700;color:${C.ink}">${h}</div><div>RGB ${r}, ${g}, ${b}</div><div>HSL ${hslOf(h)}</div></div></div>`; }).join('')}
  </div>
  ${brandmark({ pos: 'right:88px;top:74px', size: 36 })}`;
  add('colour-palette', 1920, 1080, page({ title: 'palette', w: 1920, h: 1080, body }));
}

// ---------- accessible text pairings ----------
{
  const pairs = [
    ['Ink on Paper', C.ink, C.paper, 'Body text, light mode'],
    ['Slate on Paper', C.slate, C.paper, 'Secondary text'],
    ['Paper on Night', C.paper, C.night, 'Body text, dark mode'],
    ['Flux Orange on Night', C.orange, C.night, 'Headlines & links on dark'],
    ['Night on Flux Orange', C.night, C.orange, 'Recommended button label'],
    ['Ink on Orange tint', C.ink, C.tint, 'Callouts, chips'],
    ['Paper on Slate', C.paper, C.slate, 'Inverse panels'],
    ['Deep orange #C24E00 on Paper', '#C24E00', C.paper, 'Orange text on white (derived tint)'],
    ['Paper on Flux Orange', C.paper, C.orange, 'Logo/graphics only, not text'],
    ['Flux Orange on Paper', C.orange, C.paper, 'Shapes & icons only, not text'],
    ['Blue on Paper', C.blue, C.paper, 'Muse spectrum: large text at most'],
    ['Yellow on Paper', C.yellow, C.paper, 'Never for text'],
  ];
  const tw = (1920 - 176 - 3 * 28) / 4;
  const tone = { pass: ['#E6F4EA', '#1E6B2A', 'check'], warn: ['#FFF4D6', '#7A4F00', 'flag'], fail: ['#FDECEA', '#B3261E', 'x'] };
  const body = `${head('Brand kit · Colour', 'Accessible text pairings', 'WCAG 2.2 contrast, computed from the HEX values. Body text needs 4.5:1 (AA); large text (24 px+, or 19 px+ bold) needs 3:1.')}
  <div style="position:absolute;left:88px;top:286px;display:grid;grid-template-columns:repeat(4,${tw}px);gap:24px 28px">
  ${pairs.map(([n, fg, bg, use]) => { const r = contrast(fg, bg); const [v, t] = verdict(r); const [tb, tc, ic] = tone[t];
    return `<div style="height:236px;border-radius:20px;overflow:hidden;border:1.5px solid #E3E6EA;background:#fff">
      <div style="height:118px;background:${bg};padding:16px 22px;color:${fg}"><div style="font:700 40px/1 Poppins">Aa Sell more</div><div style="font:500 22px Inter;margin-top:12px">${n}</div></div>
      <div style="padding:14px 22px;display:flex;flex-direction:column;gap:8px">
        <div style="display:flex;align-items:center;gap:12px"><span style="font:700 30px Poppins;color:${C.ink}">${r.toFixed(1)}:1</span>
        <span style="display:inline-flex;align-items:center;gap:6px;padding:3px 12px 3px 8px;border-radius:999px;background:${tb};color:${tc};font:700 19px Inter">${icon(ic, 18, tc, 3)}${v}</span></div>
        <div style="font:400 20px Inter;color:#5B6570">${use}</div></div></div>`; }).join('')}
  </div>${brandmark({ pos: 'right:88px;top:74px', size: 36 })}`;
  add('colour-accessibility-pairings', 1920, 1080, page({ title: 'contrast', w: 1920, h: 1080, body }));
}

// ---------- typography ----------
{
  const scale = [
    ['Display', 'Poppins 700', 72, 'Receipts and revenue', 'Poppins', 700],
    ['H1', 'Poppins 700', 56, 'Sell where your buyers chat', 'Poppins', 700],
    ['H2', 'Poppins 600', 40, 'Your AI marketing team', 'Poppins', 600],
    ['H3', 'Poppins 600', 30, 'Checkout inside WhatsApp', 'Poppins', 600],
    ['Body', 'Inter 400', 24, 'Plan, create, publish, sell and learn from one workspace.', 'Inter', 400],
    ['Caption', 'Inter 500', 20, 'Priced in ZAR · 14-day free trial, no card required', 'Inter', 500],
  ];
  const body = `${head('Brand kit · Typography', 'Poppins for headlines, Inter for everything else')}
  <div style="position:absolute;left:88px;top:200px;width:840px;height:330px" class="card">
    <div style="position:absolute;left:36px;top:6px;font:700 210px/1 Poppins;color:${C.orange}">Aa</div>
    <div style="position:absolute;left:340px;top:36px;right:30px">
      <div style="font:700 44px Poppins;color:${C.ink}">Poppins</div>
      <div style="font:400 22px/1.45 Inter;color:#5B6570;margin-top:6px">Headlines, numbers, the wordmark’s geometric feel. SemiBold 600 and Bold 700.</div>
      <div style="font:600 26px/1.5 Poppins;color:${C.ink};margin-top:14px">ABCDEFGHIJKLM<br>abcdefghijklm 0123456789 R₦</div>
    </div></div>
  <div style="position:absolute;left:992px;top:200px;width:840px;height:330px" class="card">
    <div style="position:absolute;left:36px;top:6px;font:600 210px/1 Inter;color:${C.slate}">Aa</div>
    <div style="position:absolute;left:340px;top:36px;right:30px">
      <div style="font:700 44px Inter;color:${C.ink}">Inter</div>
      <div style="font:400 22px/1.45 Inter;color:#5B6570;margin-top:6px">Body copy, UI, tables and captions. Regular 400, Medium 500, SemiBold 600.</div>
      <div style="font:400 26px/1.5 Inter;color:${C.ink};margin-top:14px">ABCDEFGHIJKLM<br>abcdefghijklm 0123456789 R₦</div>
    </div></div>
  <div style="position:absolute;left:88px;top:566px;right:88px">
    <div style="font:700 24px Poppins;color:${C.ink};margin-bottom:6px">Slide scale <span style="font:500 21px Inter;color:#5B6570">· 1920×1080 canvas · fallback: Arial</span></div>
    ${scale.map(([n, spec, px, sample, fam, wt]) => `<div style="display:flex;align-items:baseline;gap:24px;border-top:1.5px solid #E3E6EA;padding:${px > 50 ? 2 : 6}px 0">
      <div style="width:350px;flex:none;font:500 21px Inter;color:#5B6570"><b style="color:${C.ink}">${n}</b> · ${spec} · ${px}px</div>
      <div style="font:${wt} ${px}px/1.12 ${fam};color:${C.ink};white-space:nowrap;overflow:hidden">${sample}</div></div>`).join('')}
  </div>${brandmark({ pos: 'right:88px;top:74px', size: 36 })}`;
  add('typography-specimen', 1920, 1080, page({ title: 'typography', w: 1920, h: 1080, body }));
}

// ---------- social avatar 1080 ----------
add('social-avatar-1080', 1080, 1080, page({ title: 'avatar', w: 1080, h: 1080, bg: C.night, dark: true,
  body: `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 46%, rgba(255,106,0,.22), rgba(15,20,25,0) 58%)"></div>
  <img src="${ICON}" style="position:absolute;left:215px;top:215px;width:650px;height:650px">` }), { dpr: 1 });

// ---------- social covers ----------
const cover = (w, h, guides, kind) => {
  const lh = Math.round(h * 0.3);
  const guideSvg = !guides ? '' : kind === 'x'
    ? `<svg style="position:absolute;inset:0" width="${w}" height="${h}"><rect x="30" y="${h - 190}" width="220" height="220" rx="110" fill="rgba(229,57,53,.25)" stroke="#E53935" stroke-width="3" stroke-dasharray="10 8"/>
       <rect x="0" y="0" width="${w}" height="70" fill="rgba(229,57,53,.15)"/><rect x="0" y="${h - 70}" width="${w}" height="70" fill="rgba(229,57,53,.15)"/>
       <text x="40" y="45" fill="#fff" font-family="Inter" font-size="22" font-weight="600">Approx. crop zones: top/bottom may be trimmed on some devices; profile photo overlaps bottom-left</text></svg>`
    : `<svg style="position:absolute;inset:0" width="${w}" height="${h}"><rect x="0" y="0" width="${(w - 1200) / 2}" height="${h}" fill="rgba(229,57,53,.18)"/><rect x="${w - (w - 1200) / 2}" y="0" width="${(w - 1200) / 2}" height="${h}" fill="rgba(229,57,53,.18)"/>
       <rect x="40" y="${h - 230}" width="250" height="250" rx="125" fill="rgba(229,57,53,.25)" stroke="#E53935" stroke-width="3" stroke-dasharray="10 8"/>
       <text x="${(w - 1200) / 2 + 20}" y="40" fill="#fff" font-family="Inter" font-size="22" font-weight="600">Approx. mobile crop: side strips hidden; profile photo overlaps bottom-left on desktop</text></svg>`;
  return page({ title: 'cover', w, h, bg: C.night, dark: true, body: `
    ${netSVG(w, h, { seed: 5, n: 34, color: C.orange, opacity: 0.22, region: [w * 0.72, 10, w - 10, h - 10] })}
    ${netSVG(w, h, { seed: 9, n: 16, color: '#ffffff', opacity: 0.07, region: [10, 10, w * 0.22, h - 10] })}
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:${Math.round(w * 0.03)}px;padding-left:${Math.round(w * 0.12)}px;padding-right:${Math.round(w * 0.08)}px">
      <img src="${DARK}" style="height:${lh}px">
      <div style="width:3px;height:${Math.round(h * 0.42)}px;background:${C.orange};border-radius:2px"></div>
      <div style="color:#F5F6F8">
        <div style="font:700 ${Math.round(h * 0.078)}px/1.15 Poppins">AI Marketing &amp; WhatsApp<br>Commerce for Africa</div>
        <div style="font:500 ${Math.round(h * 0.046)}px Inter;color:#A7B0BA;margin-top:${Math.round(h * 0.025)}px">Plan · Create · Publish · Sell · Learn</div>
        <div class="chip" style="margin-top:${Math.round(h * 0.035)}px;font-size:${Math.round(h * 0.04)}px">14-day free trial · fluxmuse.ai</div>
      </div></div>${guideSvg}` });
};
add('social-cover-1500x500', 1500, 500, cover(1500, 500, false, 'x'), { dpr: 1 });
add('social-cover-1500x500_guides', 1500, 500, cover(1500, 500, true, 'x'), { dpr: 1 });
add('social-cover-1640x624', 1640, 624, cover(1640, 624, false, 'fb'), { dpr: 1 });
add('social-cover-1640x624_guides', 1640, 624, cover(1640, 624, true, 'fb'), { dpr: 1 });

// ---------- WhatsApp Business profile (640×640, circle-safe) ----------
add('whatsapp-business-profile-640', 640, 640, page({ title: 'wa profile', w: 640, h: 640, bg: C.paper,
  body: `<img src="${ICON}" style="position:absolute;left:115px;top:105px;width:410px;height:410px">` }), { dpr: 1 });

// ---------- email signature banner 600×150 (1x and 2x) ----------
const emailBanner = page({ title: 'email banner', w: 600, h: 150, bg: C.paper, body: `
  ${netSVG(600, 150, { seed: 3, n: 14, color: C.orange, opacity: 0.18, region: [470, 8, 592, 142], r: 2 })}
  <div style="position:absolute;left:22px;top:0;bottom:6px;display:flex;align-items:center;gap:18px">
    <img src="${LIGHT}" style="height:66px">
    <div style="width:2px;height:80px;background:${C.orange}"></div>
    <div><div style="font:600 17px/1.25 Poppins;color:${C.ink}">AI marketing team &amp;<br>WhatsApp commerce for African SMBs</div>
    <div style="font:500 13px Inter;color:${C.slate};margin-top:6px">fluxmuse.ai · 14-day free trial, no card required</div></div></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:${C.orange}"></div>` });
add('email-signature-banner-600x150', 600, 150, emailBanner, { dpr: 1 });
add('email-signature-banner-600x150@2x', 600, 150, emailBanner, { dpr: 2 });

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9341 });
