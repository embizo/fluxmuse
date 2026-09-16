// Infographic frame + drawing helpers shared by build_infographics*.mjs
import { page, netSVG, brandmark, C } from './page.mjs';
import { icon } from './icons.mjs';
export { C, icon };

export const T = (dark) => ({
  fg: dark ? '#F5F6F8' : C.ink, muted: dark ? '#A7B0BA' : '#5B6570', card: dark ? '#182028' : '#FFFFFF',
  card2: dark ? '#1E2731' : C.mist, line: dark ? '#2B3540' : '#E3E6EA', bg: dark ? C.night : C.paper,
  accentText: dark ? C.glow : '#C24E00', chipBg: dark ? 'rgba(255,106,0,.16)' : C.tint, chipFg: dark ? '#FFB27A' : '#9A3D00',
  ring: dark ? '#3A4552' : '#CBD2D9', slateMark: dark ? '#8FA3AD' : C.slate,
});

export function frame({ w, h, dark = false, eyebrow, title, sub = '', body, css = '', mark = 'br', titleSize, headW }) {
  const sq = w <= 1080;
  const ts = titleSize || (sq ? 46 : 56);
  const markPos = mark === 'tr' ? `right:${sq ? 48 : 64}px;top:${sq ? 50 : 60}px` : `right:${sq ? 48 : 64}px;bottom:${sq ? 34 : 36}px`;
  const t = T(dark);
  return page({ title: title.replace(/<[^>]+>/g, ''), w, h, dark, bg: t.bg, css: `
    .ey{font:700 ${sq ? 20 : 22}px Inter,Arial;letter-spacing:.16em;text-transform:uppercase;color:${t.accentText}}
    .tt{font:700 ${ts}px/1.08 Poppins,Arial;color:${t.fg};margin-top:10px;letter-spacing:-.01em}
    .sb{font:400 ${sq ? 23 : 26}px/1.4 Inter,Arial;color:${t.muted};margin-top:12px}
    .card{background:${t.card};border:1.5px solid ${t.line};border-radius:22px}
    .chip{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;font:600 20px Inter,Arial;background:${t.chipBg};color:${t.chipFg};white-space:nowrap}
    .muted{color:${t.muted}} .fg{color:${t.fg}}
    ${css}`,
    body: `${netSVG(w, h, { seed: 21, n: 18, color: dark ? '#ffffff' : C.slate, opacity: dark ? 0.09 : 0.1, region: [w - (sq ? 360 : 560), 8, w - 8, sq ? 190 : 230] })}
    <div style="position:absolute;left:${sq ? 56 : 88}px;top:${sq ? 50 : 60}px;width:${headW || (sq ? 800 : 1300)}px">
      <div class="ey">${eyebrow}</div><div class="tt">${title}</div>${sub ? `<div class="sb">${sub}</div>` : ''}</div>
    ${body}
    ${brandmark({ pos: markPos, size: sq ? 36 : 42 })}` });
}

export const markers = (dark) => `<defs>
  <marker id="ah-o" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${C.orange}"/></marker>
  <marker id="ah-s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${dark ? '#8FA3AD' : C.slate}"/></marker>
  <marker id="ah-m" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${dark ? '#6B7785' : '#9AA5B1'}"/></marker>
</defs>`;

// Ellipse ring edges between rectangular nodes, clipped to the gaps. Returns [{d, mid:[x,y], ang}]
export function ringEdges(cx, cy, rx, ry, anglesDeg, rects, pad = 16) {
  const inside = (p, r) => p[0] > r.x - pad && p[0] < r.x + r.w + pad && p[1] > r.y - pad && p[1] < r.y + r.h + pad;
  const n = anglesDeg.length; const out = [];
  for (let i = 0; i < n; i++) {
    const a = anglesDeg[i]; let b = anglesDeg[(i + 1) % n]; if (b <= a) b += 360;
    const pts = [];
    for (let k = 0; k <= 400; k++) {
      const th = ((a + (b - a) * k / 400) * Math.PI) / 180; const p = [cx + rx * Math.cos(th), cy + ry * Math.sin(th)];
      if (!rects.some((r) => inside(p, r))) pts.push(p); else if (pts.length) break;
    }
    const mid = pts[Math.floor(pts.length / 2)] || [cx, cy];
    out.push({ d: 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L'), mid });
  }
  return out;
}

export const fmtR = (n) => 'R' + n.toLocaleString('en-US');
