// Infographics 1–6 (with _square / _dark / _portrait variants) → ../assets/infographics
// Usage: node build_infographics.mjs [nameFilter]
import { join } from 'node:path';
import { renderJobs, ASSETS } from './lib/page.mjs';
import { frame, markers, ringEdges, T, C, icon } from './lib/ig.mjs';
import { COUNTRIES, SOON, billingOf, statusOf } from './lib/africa.mjs';

const OUT = join(ASSETS, 'infographics');
const jobs = [];
const add = (name, w, h, html) => jobs.push({ name, dir: 'infographics', html, w, h, out: join(OUT, name + '.png') });
const variants = (base, fn, { square = false, dark = true } = {}) => {
  add(base, 1920, 1080, fn({ dark: false, w: 1920, h: 1080 }));
  if (dark) add(base + '_dark', 1920, 1080, fn({ dark: true, w: 1920, h: 1080 }));
  if (square) {
    add(base + '_square', 1080, 1080, fn({ dark: false, w: 1080, h: 1080 }));
    if (dark) add(base + '_square_dark', 1080, 1080, fn({ dark: true, w: 1080, h: 1080 }));
  }
};
const ICON = '../../assets/brand/fluxmuse-icon-512.png';

// ============ 1. how-fluxmuse-works ============
variants('how-fluxmuse-works', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080;
  const stages = [
    ['Plan', 'Strategist', 'target', 'Your goals, products and the week ahead'],
    ['Create', 'Creator', 'pen', sq ? 'Captions, images and short clips' : 'Captions, images and short video clips, in your customers’ languages'],
    ['Publish', 'Publisher', 'send', sq ? 'WhatsApp Status, broadcasts, TikTok' : 'WhatsApp Status, consented broadcasts, TikTok'],
    ['Sell', 'WhatsApp shop', 'bag', sq ? 'Shop link and order alerts' : 'Shop link from your photos; every order on WhatsApp'],
    ['Learn', 'Analyst', 'chart', 'What sold, and what to post next'],
  ];
  const edgeLabels = ['brief', 'content', 'chats & clicks', 'orders & data', 'insights'];
  const angles = sq ? [-90, -20, 40, 140, 200] : [-90, -18, 54, 126, 198];
  const G = sq ? { cx: 540, cy: 662, rx: 332, ry: 300, cw: 282, ch: 192 } : { cx: 960, cy: 668, rx: 612, ry: 282, cw: 372, ch: 196 };
  const rects = angles.map((a) => { const th = (a * Math.PI) / 180; const x = G.cx + G.rx * Math.cos(th), y = G.cy + G.ry * Math.sin(th); return { x: x - G.cw / 2, y: y - G.ch / 2, w: G.cw, h: G.ch }; });
  const edges = ringEdges(G.cx, G.cy, G.rx, G.ry, angles, rects, 14);
  const hub = sq ? 200 : 236;
  const body = `
  <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">${markers(dark)}
    ${edges.map((e) => `<path d="${e.d}" fill="none" stroke="${C.orange}" stroke-width="3.5" marker-end="url(#ah-o)"/>`).join('')}
  </svg>
  <div style="position:absolute;left:${G.cx - hub / 2}px;top:${G.cy - hub / 2}px;width:${hub}px;height:${hub}px;border-radius:50%;background:${t.card2};border:1.5px solid ${t.line};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <img src="${ICON}" style="width:${sq ? 78 : 92}px">
    <div style="font:700 ${sq ? 21 : 23}px/1.2 Poppins;color:${t.fg};margin-top:6px">Your AI<br>marketing team</div></div>
  ${edges.map((e, i) => `<div class="chip" style="position:absolute;left:${e.mid[0]}px;top:${e.mid[1]}px;transform:translate(-50%,-50%);font-size:${sq ? 19 : 21}px;background:${t.bg};border:2px solid ${C.orange};color:${t.fg}">${edgeLabels[i]}</div>`).join('')}
  ${stages.map(([s, agent, ic, desc], i) => { const r = rects[i]; return `<div class="card" style="position:absolute;left:${r.x}px;top:${r.y}px;width:${r.w}px;height:${r.h}px;padding:${sq ? '16px 18px' : '18px 22px'}">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:${sq ? 46 : 50}px;height:${sq ? 46 : 50}px;border-radius:14px;background:${t.chipBg};display:flex;align-items:center;justify-content:center">${icon(ic, sq ? 26 : 28, C.orange, 2.2)}</div>
      <div><div style="font:700 ${sq ? 28 : 32}px/1 Poppins;color:${t.fg}">${i + 1}. ${s}</div>
      <div style="font:600 ${sq ? 18 : 20}px Inter;color:${t.accentText};margin-top:5px">${agent}</div></div></div>
    <div style="font:400 ${sq ? 21 : 22}px/1.35 Inter;color:${t.muted};margin-top:12px">${desc}</div></div>`; }).join('')}`;
  return frame({ w, h, dark, eyebrow: 'How FluxMuse works', title: sq ? 'One loop, run by AI agents' : 'One loop, run by your AI marketing team', mark: sq ? 'tr' : 'br', headW: sq ? 760 : 1300, body });
}, { square: true });

// ============ 2. whatsapp-commerce-flow ============
const rails = ['Paystack · South Africa', 'Being switched on'];
const flowNodes = [
  ['Discover', 'megaphone', 'Status post, QR code or your shop link'],
  ['Chat', 'chat', 'The assistant replies in the buyer’s language'],
  ['Catalog', 'bag', 'Your shop, built from your product photos'],
  ['Cart', 'cart', 'Items and totals on your shop page'],
  ['Pay', 'card', null],
  ['Order alert', 'checkCircle', 'Order lands on your WhatsApp; reply SOLD'],
  ['Come back', 'heart', 'Broadcasts to consented contacts'],
];
variants('whatsapp-commerce-flow', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080;
  const railChips = (fs) => rails.map((r) => `<span class="chip" style="font-size:${fs}px;padding:4px 11px">${r}</span>`).join('');
  const foot = `<div style="position:absolute;left:${sq ? 56 : 88}px;bottom:${sq ? 36 : 40}px;font:400 ${sq ? 19 : 21}px Inter;color:${t.muted};width:${sq ? 740 : 1300}px">Checkout through FluxMuse (Paystack, South Africa) is built and being switched on; it has not yet been tested with real money. Until then, orders arrive as a WhatsApp message to your own number.</div>`;
  if (!sq) {
    const y0 = 300, nh = 380, gap = 34, pw = 300, nw = (1744 - pw - 6 * gap) / 6;
    let x = 88; const xs = flowNodes.map(([n]) => { const cur = x; x += (n === 'Pay' ? pw : nw) + gap; return cur; });
    const cxs = flowNodes.map(([n], i) => xs[i] + (n === 'Pay' ? pw : nw) / 2);
    const yb = y0 + nh;
    const arc = (i, j, depth, stroke, mk) => `<path d="M${cxs[i]} ${yb + 8} C ${cxs[i]} ${yb + depth}, ${cxs[j]} ${yb + depth}, ${cxs[j]} ${yb + 8}" fill="none" stroke="${stroke}" stroke-width="3.5" stroke-dasharray="11 9" marker-end="url(#${mk})"/>`;
    const body = `
    <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">${markers(dark)}
      ${xs.slice(0, -1).map((xx, i) => { const x1 = xx + (flowNodes[i][0] === 'Pay' ? pw : nw) + 4, x2 = xs[i + 1] - 4; return `<line x1="${x1}" y1="${y0 + 64}" x2="${x2}" y2="${y0 + 64}" stroke="${C.orange}" stroke-width="3.5" marker-end="url(#ah-o)"/>`; }).join('')}
      ${arc(4, 1, 130, C.orange, 'ah-o')}
      ${arc(6, 0, 300, t.slateMark, 'ah-s')}
    </svg>
    ${flowNodes.map(([n, ic, desc], i) => `<div class="card" style="position:absolute;left:${xs[i]}px;top:${y0}px;width:${n === 'Pay' ? pw : nw}px;height:${nh}px;padding:20px 18px;${n === 'Pay' ? `border:2.5px solid ${C.orange}` : ''}">
      <div style="width:58px;height:58px;border-radius:16px;background:${t.chipBg};display:flex;align-items:center;justify-content:center">${icon(ic, 30, C.orange, 2.2)}</div>
      <div style="font:700 28px Poppins;color:${t.fg};margin-top:14px">${n}</div>
      ${desc ? `<div style="font:400 22px/1.36 Inter;color:${t.muted};margin-top:6px">${desc}</div>` : `<div style="font:400 22px/1.3 Inter;color:${t.muted};margin:4px 0 10px">In South Africa</div><div style="display:flex;flex-wrap:wrap;gap:8px">${railChips(19)}</div>`}
    </div>`).join('')}
    <div class="chip" style="position:absolute;left:${(cxs[1] + cxs[4]) / 2}px;top:${yb + 104}px;transform:translate(-50%,-50%);font-size:21px;background:${t.bg};border:2px solid ${C.orange};color:${t.fg}">${icon('refresh', 20, C.orange)} Questions? The assistant answers, day and night</div>
    <div class="chip" style="position:absolute;left:${(cxs[0] + cxs[6]) / 2}px;top:${yb + 228}px;transform:translate(-50%,-50%);font-size:21px;background:${t.bg};border:2px solid ${t.slateMark};color:${t.fg}">${icon('users', 20, t.slateMark)} A broadcast to consented contacts starts the next sale</div>
    ${foot}`;
    return frame({ w, h, dark, eyebrow: 'WhatsApp commerce', title: 'From first tap to repeat order, on WhatsApp', headW: 1560, body });
  }
  // square: vertical list, loops on the right, loop meaning in a legend
  const x0 = 56, rw = 680, y0 = 196, rh = 86, g = 12, payExtra = 44;
  const ry = (i) => y0 + i * (rh + g) + (i > 4 ? payExtra : 0);
  const rowH = (i) => (flowNodes[i][0] === 'Pay' ? rh + payExtra : rh);
  const mid = (i) => ry(i) + rowH(i) / 2;
  const body = `
  <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">${markers(dark)}
    ${flowNodes.slice(0, -1).map((_, i) => `<line x1="${x0 + 42}" y1="${ry(i) + rowH(i) + 1}" x2="${x0 + 42}" y2="${ry(i + 1) - 1}" stroke="${C.orange}" stroke-width="3" marker-end="url(#ah-o)"/>`).join('')}
    <path d="M${x0 + rw + 6} ${mid(4)} C ${x0 + rw + 90} ${mid(4)}, ${x0 + rw + 90} ${mid(1)}, ${x0 + rw + 12} ${mid(1)}" fill="none" stroke="${C.orange}" stroke-width="3.5" stroke-dasharray="10 8" marker-end="url(#ah-o)"/>
    <path d="M${x0 + rw + 6} ${mid(6)} C ${x0 + rw + 250} ${mid(6)}, ${x0 + rw + 250} ${mid(0)}, ${x0 + rw + 12} ${mid(0)}" fill="none" stroke="${t.slateMark}" stroke-width="3.5" stroke-dasharray="10 8" marker-end="url(#ah-s)"/>
    <line x1="56" y1="${ry(6) + rh + 44}" x2="106" y2="${ry(6) + rh + 44}" stroke="${C.orange}" stroke-width="3.5" stroke-dasharray="10 8"/>
    <line x1="470" y1="${ry(6) + rh + 44}" x2="520" y2="${ry(6) + rh + 44}" stroke="${t.slateMark}" stroke-width="3.5" stroke-dasharray="10 8"/>
  </svg>
  ${flowNodes.map(([n, ic, desc], i) => `<div class="card" style="position:absolute;left:${x0}px;top:${ry(i)}px;width:${rw}px;height:${rowH(i)}px;padding:12px 16px;display:flex;gap:16px;align-items:${n === 'Pay' ? 'flex-start' : 'center'};${n === 'Pay' ? `border:2.5px solid ${C.orange}` : ''}">
    <div style="flex:none;width:52px;height:52px;border-radius:15px;background:${t.chipBg};display:flex;align-items:center;justify-content:center">${icon(ic, 28, C.orange, 2.2)}</div>
    <div><div style="font:700 24px/1.15 Poppins;color:${t.fg}">${n}</div>
    ${desc ? `<div style="font:400 20px/1.3 Inter;color:${t.muted}">${desc}</div>` : `<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px">${railChips(18)}</div>`}</div></div>`).join('')}
  <div style="position:absolute;left:118px;top:${ry(6) + rh + 30}px;font:600 20px Inter;color:${t.fg}">Questions answered</div>
  <div style="position:absolute;left:532px;top:${ry(6) + rh + 30}px;font:600 20px Inter;color:${t.fg}">Repeat orders</div>
  ${foot}`;
  return frame({ w, h, dark, eyebrow: 'WhatsApp commerce', title: 'From tap to repeat order', mark: 'tr', headW: 760, body });
}, { square: true });

// ============ 3. payment-coverage-map (tile-grid cartogram; live vs pending, status 2026-10-05) ============
// live = paid checkout open (South Africa, Paystack). priced = local prices set, not on sale (NG, KE, GH).
// pending = a contracted provider (pawaPay / Fincra) covers it, account pending. soon = no provider yet.
const STAT_STYLE = (dark) => ({
  live: { bg: C.orange, fg: C.night, border: 'none' },
  priced: { bg: dark ? '#3A2718' : '#FFE9D6', fg: dark ? '#FFFFFF' : C.ink, border: `${3}px solid ${C.orange}` },
  pending: { bg: dark ? '#1E2731' : '#F3F4F6', fg: dark ? '#F5F6F8' : C.ink, border: `2px solid ${dark ? '#3A4552' : '#CBD2D9'}` },
});
variants('payment-coverage-map', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080; const S = STAT_STYLE(dark);
  const ts = sq ? 102 : 124, tg = sq ? 8 : 10, mx = sq ? 56 : 88, my = sq ? 196 : 238;
  const soonBorder = dark ? '#8A96A3' : '#8A949E';
  const counts = { live: 0, priced: 0, pending: 0 }; COUNTRIES.forEach((c) => counts[statusOf(c[0])]++);
  const tiles = COUNTRIES.map(([iso, name, c, r]) => { const st = S[statusOf(iso)]; return `<div style="position:absolute;left:${mx + c * (ts + tg)}px;top:${my + r * (ts + tg)}px;width:${ts}px;height:${ts}px;border-radius:${sq ? 14 : 16}px;background:${st.bg};border:${st.border};box-sizing:border-box;color:${st.fg};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4px">
    <div style="font:700 ${sq ? 30 : 36}px/1 Poppins">${iso}</div><div style="font:600 ${sq ? 14 : 17}px/1.12 Inter;margin-top:${sq ? 4 : 6}px">${name.replace('*', '')}</div></div>`; }).join('')
    + SOON.map(([iso, name, c, r]) => `<div style="position:absolute;left:${mx + c * (ts + tg)}px;top:${my + r * (ts + tg)}px;width:${ts}px;height:${ts}px;border-radius:${sq ? 14 : 16}px;border:${sq ? 2.5 : 3}px dashed ${soonBorder};box-sizing:border-box;color:${t.fg};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2px">
    <div style="font:700 ${sq ? 26 : 32}px/1 Poppins">${iso}</div><div style="font:600 ${sq ? 14 : 17}px/1.12 Inter;margin-top:${sq ? 2 : 4}px">${name}</div><div style="font:700 ${sq ? 12 : 15}px/1.1 Inter;color:${t.muted};margin-top:${sq ? 2 : 4}px;text-transform:uppercase;letter-spacing:.03em;max-width:${sq ? 70 : 100}px">Coming soon</div></div>`).join('');
  const swatch = (fs, k) => k === 'soon' ? `<span style="flex:none;width:${fs + 8}px;height:${fs + 8}px;border-radius:7px;border:2.5px dashed ${soonBorder};box-sizing:border-box"></span>`
    : `<span style="flex:none;width:${fs + 8}px;height:${fs + 8}px;border-radius:7px;background:${S[k].bg};border:${S[k].border};box-sizing:border-box"></span>`;
  const rows = [['live', 'Live: paid checkout open', 'South Africa (Paystack)'], ['priced', 'Priced, not yet on sale', 'Nigeria, Kenya, Ghana'], ['pending', 'Provider contracted, account pending', `${counts.pending} countries (pawaPay / Fincra)`], ['soon', 'Coming soon', 'Botswana, Namibia']];
  const legend = (fs) => `<div style="display:flex;flex-direction:column;gap:${sq ? 8 : 12}px">${rows.map(([k, a, b]) => `<div style="display:flex;align-items:flex-start;gap:10px;font:500 ${fs}px/1.3 Inter;color:${t.fg}">${swatch(fs, k)}<span><b>${a}</b> <span style="color:${t.muted}">· ${b}</span></span></div>`).join('')}</div>`;
  const stats = [['1', 'country with live paid checkout'], ['3', 'next markets priced, not on sale'], ['2', 'providers contracted, pending']];
  const note = `Paystack is live in South Africa; FluxMuse checkout through it is being switched on. pawaPay and Fincra are contracted for expansion; accounts pending. No paid checkout outside South Africa yet.`;
  if (!sq) {
    const body = `${tiles}
    <div style="position:absolute;left:1308px;top:238px;width:524px">
      <div style="display:flex;flex-direction:column;gap:12px">
        ${stats.map(([n, l]) => `<div class="card" style="padding:12px 18px;display:flex;align-items:center;gap:16px"><div style="font:700 46px/1 Poppins;color:${t.accentText};width:40px">${n}</div><div style="font:500 21px/1.25 Inter;color:${t.fg}">${l}</div></div>`).join('')}
      </div>
      <div style="font:700 24px Poppins;color:${t.fg};margin:26px 0 12px">Status by country</div>${legend(20)}
      <div style="font:400 19px/1.4 Inter;color:${t.muted};margin-top:20px">${note}</div>
    </div>`;
    return frame({ w, h, dark, eyebrow: 'Payments coverage · October 2026', title: 'Live in South Africa. The rest is pending.', sub: 'Tiles show where contracted providers can reach, placed roughly by geography.', body });
  }
  const body = `${tiles}
  <div style="position:absolute;left:56px;top:${my + 3 * (ts + tg) + 8}px;width:520px">${stats.map(([n, l]) => `<div style="margin-bottom:10px;display:flex;align-items:center;gap:12px"><span style="font:700 38px/1 Poppins;color:${t.accentText}">${n}</span> <span style="font:500 19px/1.2 Inter;color:${t.fg};width:300px">${l}</span></div>`).join('')}</div>
  <div style="position:absolute;left:56px;top:${my + 6 * (ts + tg) + 30}px;right:56px">${legend(18)}
  <div style="font:400 16px/1.35 Inter;color:${t.muted};margin-top:10px">${note}</div></div>`;
  return frame({ w, h, dark, eyebrow: 'Payments · October 2026', title: 'Live in South Africa, the rest pending', mark: 'tr', headW: 760, titleSize: 40, body });
}, { square: true });

// ============ 4. payment-rails-matrix (live vs pending, status 2026-10-05) ============
const REGIONS = [
  ['Southern Africa', [['South Africa', 'ZA', 'ZAR'], ['Zambia', 'ZM', 'ZMW'], ['Malawi', 'MW', 'MWK'], ['Mozambique', 'MZ', 'MZN'], ['Lesotho', 'LS', 'LSL'], ['Zimbabwe', 'ZW', 'USD'], ['Botswana', 'BW', 'BWP', true], ['Namibia', 'NA', 'NAD', true]]],
  ['East Africa', [['Kenya', 'KE', 'KES'], ['Uganda', 'UG', 'UGX'], ['Tanzania', 'TZ', 'TZS'], ['Rwanda', 'RW', 'RWF'], ['Ethiopia', 'ET', 'ETB'], ['South Sudan', 'SS', 'SSP']]],
  ['West Africa', [['Nigeria', 'NG', 'NGN'], ['Ghana', 'GH', 'GHS'], ["Côte d'Ivoire", 'CI', 'XOF'], ['Senegal', 'SN', 'XOF'], ['Benin', 'BJ', 'XOF'], ['Burkina Faso', 'BF', 'XOF'], ['Sierra Leone', 'SL', 'SLE']]],
  ['Central Africa', [['Cameroon', 'CM', 'XAF'], ['Rep. of the Congo', 'CG', 'XAF'], ['Gabon', 'GA', 'XAF'], ['DR Congo', 'CD', 'CDF/USD']]],
];
const RAILS = ['Yoco', 'Ozow', 'Paystack', 'pawaPay', 'Fincra'];
// Header status per rail. Yoco/Ozow: FluxMuse's own subscription billing (SA). Paystack: live in SA only.
const RAIL_STATUS = { Yoco: ['billing', 'live'], Ozow: ['billing', 'live'], Paystack: ['live SA', 'live'], pawaPay: ['pending', 'pending'], Fincra: ['pending', 'pending'] };
const railsOf = Object.fromEntries(COUNTRIES.map((c) => [c[0], c[4]]));
{
  const build = ({ dark, w, h, portrait }) => {
    const t = T(dark);
    const colW = portrait ? { name: 226, iso: 56, cur: 100, bill: 106, rail: 96 } : { name: 206, iso: 48, cur: 112, bill: 96, rail: 78 };
    const tw = colW.name + colW.iso + colW.cur + colW.bill + 5 * colW.rail;
    const rowH = portrait ? 33 : 44, regH = portrait ? 36 : 44, hdH = portrait ? 58 : 70, fs = portrait ? 20 : 22;
    const soonC = dark ? '#8A96A3' : '#8A949E';
    const green = dark ? '#7FD18A' : '#1E6B2A';
    // c = live; p = contracted, account pending (hollow ring); s = coming soon
    const mark = (st) => st === 'c' ? `<svg width="${fs + 8}" height="${fs + 8}" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="${C.orange}"/><path d="M9 16.5l4.5 4.5L23 11.5" fill="none" stroke="${C.night}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`
      : st === 'p' ? `<svg width="${fs + 8}" height="${fs + 8}" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12" fill="none" stroke="${soonC}" stroke-width="2.6" stroke-dasharray="4 3"/></svg>`
      : st === 's' ? `<span style="display:inline-block;width:${fs + 14}px;height:${fs + 4}px;border-radius:7px;border:2.5px dashed ${soonC};box-sizing:border-box"></span>` : `<span style="color:${t.line};font:700 ${fs}px Inter">·</span>`;
    const header = `<div style="display:flex;align-items:flex-end;height:${hdH}px;border-bottom:2px solid ${t.fg};font:700 ${fs - 1}px Inter;color:${t.fg}">
      <div style="width:${colW.name}px">Country</div><div style="width:${colW.iso}px">ISO</div><div style="width:${colW.cur}px">Currency</div>
      <div style="width:${colW.bill}px;line-height:1.1;padding-bottom:3px">Billing<br>status</div>
      ${RAILS.map((r) => { const [lbl, st] = RAIL_STATUS[r]; return `<div style="width:${colW.rail}px;text-align:center;line-height:1.15;font-size:${fs - (portrait ? 5 : 7)}px">${r}<div style="font:600 ${portrait ? 14 : 15}px/1.1 Inter;color:${st === 'live' ? green : t.muted};margin:3px 0 6px">${lbl}</div></div>`; }).join('')}</div>`;
    const billCell = (iso, soon) => {
      if (soon) return `<div style="width:${colW.bill}px;color:${t.muted};font-style:italic">waitlist</div>`;
      const st = statusOf(iso);
      if (st === 'live') return `<div style="width:${colW.bill}px;font-weight:700;color:${t.accentText}">ZAR live</div>`;
      return `<div style="width:${colW.bill}px;color:${t.muted};font-size:${fs - 3}px">${st === 'priced' ? 'priced' : 'closed'}</div>`;
    };
    const cell = (iso, r, rs) => {
      if (iso === 'ZA' && ['Yoco', 'Ozow', 'Paystack'].includes(r)) return mark('c');
      return rs.includes(r) || rs.includes(r + '*') ? mark('p') : mark('');
    };
    const table = (regs) => `<div style="width:${tw}px">${header}${regs.map(([rn, list]) => `
      <div style="height:${regH}px;display:flex;align-items:flex-end;padding-bottom:5px;font:700 ${fs}px Poppins;color:${t.accentText};border-bottom:1.5px solid ${t.line}">${rn}</div>
      ${list.map(([name, iso, cur, soon]) => { const rs = railsOf[iso] || []; return `<div style="height:${rowH}px;display:flex;align-items:center;border-bottom:1px solid ${t.line};font:400 ${fs}px Inter;color:${soon ? t.muted : t.fg};${iso === 'ZA' ? `background:${dark ? 'rgba(255,106,0,.10)' : C.tint};` : ''}">
        <div style="width:${colW.name}px;font-weight:${iso === 'ZA' ? 700 : 500}">${name}</div><div style="width:${colW.iso}px;color:${t.muted}">${iso}</div><div style="width:${colW.cur}px;color:${t.muted}">${cur}</div>${billCell(iso, soon)}
        ${soon ? `<div style="width:${5 * colW.rail}px;display:flex;justify-content:center"><span style="display:inline-flex;align-items:center;height:${rowH - 10}px;padding:0 16px;border-radius:999px;border:2.5px dashed ${soonC};font:700 ${fs - 4}px Inter;color:${t.fg};letter-spacing:.02em">Coming soon · no provider yet</span></div>`
          : RAILS.map((r) => `<div style="width:${colW.rail}px;display:flex;justify-content:center">${cell(iso, r, rs)}</div>`).join('')}</div>`; }).join('')}`).join('')}</div>`;
    const lfs = portrait ? 17 : 20;
    const legend = `<div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 24px;font:500 ${lfs}px Inter;color:${t.fg}">
      <span style="display:flex;align-items:center;gap:8px">${mark('c')} live</span><span style="display:flex;align-items:center;gap:8px">${mark('p')} contracted, account pending</span><span style="display:flex;align-items:center;gap:8px">${mark('s')} coming soon</span></div>
      <div style="font:400 ${lfs}px/1.4 Inter;color:${t.muted};margin-top:8px">Only South Africa is open for paid sign-up. Paystack is live there; Yoco and Ozow run FluxMuse’s own subscription billing. pawaPay and Fincra are contracted for expansion, accounts pending. Nigeria, Kenya and Ghana are priced in local currency but <b style="color:${t.fg}">not yet on sale</b>.</div>`;
    if (portrait) {
      const top = 180;
      const body = `<div style="position:absolute;left:56px;top:${top}px">${table(REGIONS)}</div><div style="position:absolute;left:56px;top:${top + hdH + 4 * regH + 25 * rowH + 14}px;width:968px">${legend}</div>`;
      return frame({ w, h, dark, eyebrow: 'Payment rails · October 2026', title: 'Live in South Africa; the rest pending', mark: 'tr', headW: 760, titleSize: 40, body });
    }
    const top = 214, gap = 1744 - 2 * tw;
    const body = `<div style="position:absolute;left:88px;top:${top}px">${table(REGIONS.slice(0, 2))}</div>
      <div style="position:absolute;left:${88 + tw + gap}px;top:${top}px">${table(REGIONS.slice(2))}</div>
      <div style="position:absolute;left:${88 + tw + gap}px;top:${top + hdH + 2 * regH + 11 * rowH + 22}px;width:${tw}px">${legend}</div>`;
    return frame({ w, h, dark, eyebrow: 'Payment rails · October 2026', title: 'What is live, and what is still pending', mark: 'tr', body });
  };
  add('payment-rails-matrix', 1920, 1080, build({ dark: false, w: 1920, h: 1080 }));
  add('payment-rails-matrix_dark', 1920, 1080, build({ dark: true, w: 1920, h: 1080 }));
  add('payment-rails-matrix_portrait', 1080, 1350, build({ dark: false, w: 1080, h: 1350, portrait: true }));
  add('payment-rails-matrix_portrait_dark', 1080, 1350, build({ dark: true, w: 1080, h: 1350, portrait: true }));
}

// ============ 5. platform-stack ============
variants('platform-stack', ({ dark, w, h }) => {
  const t = T(dark);
  // '*' suffix = in setup (being switched on); '!' suffix = not available. Status per CURRENT_OFFER.md §3.
  const layers = [
    ['Channels', 'globe', C.blue, ['WhatsApp Business', 'WhatsApp Status', 'TikTok video', 'Consented broadcasts', 'Facebook Pages*', 'Instagram posts*', 'Instagram DMs!', 'X posting!']],
    ['AI team', 'sparkles', C.violet, ['Catalogue from photos', 'Captions & images (POST)', 'Short video clips', 'Voice-note transcription', 'Replies in the customer’s language', 'AI Voice (beta)*']],
    ['Shop & orders', 'bag', C.orange, ['Hosted shop link', 'Order alerts on WhatsApp', 'Reply SOLD to mark it', 'Checkout via Paystack, South Africa*']],
    ['Growth', 'trend', C.green, ['Templates & quick replies', 'Broadcasts to consented contacts', 'Daily digest*', 'Click-to-WhatsApp ads*']],
    ['Integrations', 'plug', C.teal, ['Shopify sync*', 'WooCommerce sync*', 'Takealot sync*']],
    ['Trust', 'shield', dark ? '#8FA3AD' : C.slate, ['Verified Meta Tech Provider', 'POPIA-aligned, consent-only broadcasts', 'Row-level security', 'Encrypted tokens', 'Data export & account deletion']],
  ];
  const chip = (c) => c.endsWith('*')
    ? `<span class="chip" style="background:transparent;border:2px dashed ${t.muted};color:${t.fg};font-weight:500">${c.slice(0, -1)} · being switched on</span>`
    : c.endsWith('!') ? `<span class="chip" style="background:transparent;border:1.5px solid ${t.line};color:${t.muted};font-weight:500;text-decoration:line-through">${c.slice(0, -1)}</span><span style="font:500 18px Inter;color:${t.muted};align-self:center;margin-left:-4px">not available</span>`
    : `<span class="chip" style="background:${t.card2};color:${t.fg};font-weight:500">${c}</span>`;
  const y0 = 218, lh = 112, g = 14;
  const body = layers.map(([n, ic, col, chips], i) => `<div class="card" style="position:absolute;left:88px;top:${y0 + i * (lh + g)}px;width:1744px;height:${lh}px;display:flex;align-items:center;overflow:hidden">
    <div style="align-self:stretch;width:10px;background:${col}"></div>
    <div style="width:300px;display:flex;align-items:center;gap:14px;padding-left:22px">${icon(ic, 34, col, 2.2)}<span style="font:700 27px/1.1 Poppins;color:${t.fg}">${n}</span></div>
    <div style="flex:1;display:flex;flex-wrap:wrap;gap:10px;padding-right:22px">${chips.map(chip).join('')}</div></div>`).join('') +
    `<div style="position:absolute;left:88px;bottom:42px;width:1360px;font:400 21px/1.4 Inter;color:${t.muted}">Solid chips are live and newly launched. Dashed chips are being switched on (Meta permissions, real-money checkout tests, beta). Runs on React/Vite, Supabase and Vercel.</div>`;
  return frame({ w, h, dark, eyebrow: 'Platform', title: 'Live today, and being switched on', body });
});

// ============ 6. agency-partner-model ============
variants('agency-partner-model', ({ dark, w, h }) => {
  const t = T(dark);
  const clients = 20, retail = 1500, list = 9999, tier = 6999, rev = clients * retail, spread = rev - tier; // partner wholesale = Agency list −30%
  const pct = Math.round((spread / rev) * 100), perClient = Math.round(tier / clients);
  const R = (n) => 'R' + n.toLocaleString('en-US');
  const y = 330;
  const body = `
  <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">${markers(dark)}
    <line x1="352" y1="${y + 150}" x2="506" y2="${y + 150}" stroke="${C.orange}" stroke-width="4" marker-end="url(#ah-o)"/>
    <line x1="850" y1="${y + 150}" x2="986" y2="${y + 150}" stroke="${C.orange}" stroke-width="4" marker-end="url(#ah-o)"/>
  </svg>
  <div class="card" style="position:absolute;left:88px;top:${y + 40}px;width:256px;height:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:16px">
    <img src="../../assets/brand/fluxmuse-icon-512.png" style="width:86px"><div style="font:700 28px Poppins;color:${t.fg};margin-top:8px">FluxMuse</div>
    <div style="font:400 20px/1.3 Inter;color:${t.muted};margin-top:4px">Platform and AI team</div></div>
  <div style="position:absolute;left:350px;top:${y + 62}px;width:160px;text-align:center;font:600 20px/1.3 Inter;color:${t.fg}">Partner price<br><span style="color:${t.accentText}">${R(tier)}/mo</span></div>
  <div style="position:absolute;left:350px;top:${y + 166}px;width:160px;text-align:center;font:500 17px/1.3 Inter;color:${t.muted}">30% off the<br>${R(list)} Agency tier</div>
  <div class="card" style="position:absolute;left:514px;top:${y - 20}px;width:330px;height:340px;padding:22px 24px;border:2.5px solid ${C.orange}">
    <div style="display:flex;align-items:center;gap:12px">${icon('briefcase', 34, C.orange)}<span style="font:700 28px Poppins;color:${t.fg}">Your agency</span></div>
    ${['White-label: your brand', 'Multi-client, unlimited brands', '80 channels', 'Bring your own cloud'].map((s) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:14px;font:400 22px/1.3 Inter;color:${t.fg}">${icon('check', 24, C.orange, 3)}<span>${s}</span></div>`).join('')}</div>
  <div style="position:absolute;left:846px;top:${y + 60}px;width:146px;text-align:center;font:600 20px/1.3 Inter;color:${t.fg}">Retail price<br><span style="color:${t.accentText}">you set</span></div>
  <div class="card" style="position:absolute;left:994px;top:${y + 10}px;width:238px;height:280px;padding:20px;text-align:center">
    <div style="display:grid;grid-template-columns:repeat(5,26px);gap:10px;justify-content:center">${Array.from({ length: clients }, (_, i) => `<span style="width:26px;height:26px;border-radius:50%;background:${[C.blue, C.teal, C.green, C.violet, C.magenta][i % 5]};opacity:.9"></span>`).join('')}</div>
    <div style="font:700 26px Poppins;color:${t.fg};margin-top:18px">Your clients</div>
    <div style="font:400 20px/1.3 Inter;color:${t.muted}">One sub-account each</div></div>
  <div style="position:absolute;left:88px;top:${y + 380}px;width:1144px;padding:24px 28px;border-radius:20px;background:${t.chipBg}">
    <div style="font:700 30px Poppins;color:${t.fg}">Set your own retail price and keep the spread.</div>
    <div style="font:400 22px/1.4 Inter;color:${t.fg};margin-top:6px">FluxMuse invoices your agency the partner wholesale price, <b>${R(tier)}/mo</b> (30% off the ${R(list)} Agency tier), for multi-client, white-label FluxMuse. You bill your clients at a retail price you set.</div></div>

  <div class="card" style="position:absolute;left:1290px;top:236px;width:542px;padding:30px 32px">
    <span class="chip" style="background:${dark ? 'rgba(253,216,53,.14)' : '#FFF6D1'};color:${dark ? '#FDE68A' : '#6B4E00'}">${icon('flag', 18, dark ? '#FDE68A' : '#6B4E00')} Illustrative</span>
    <div style="font:700 30px/1.2 Poppins;color:${t.fg};margin-top:16px">${clients} clients at ${R(retail)}/mo</div>
    <div style="font:400 20px Inter;color:${t.muted};margin-top:2px">retail price set by the partner</div>
    ${[['Billed to clients', `${clients} × ${R(retail)}`, R(rev), t.fg], ['Partner wholesale price', `30% off ${R(list)}`, '− ' + R(tier), t.muted]].map(([a, b, c, col]) => `<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:20px;padding-bottom:14px;border-bottom:1.5px solid ${t.line}"><div><div style="font:600 22px Inter;color:${t.fg}">${a}</div><div style="font:400 20px Inter;color:${t.muted}">${b}</div></div><div style="font:700 30px Poppins;color:${col}">${c}</div></div>`).join('')}
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:18px"><div style="font:700 24px Inter;color:${t.fg}">Gross spread /mo</div><div style="font:700 44px Poppins;color:${t.accentText}">${R(spread)}</div></div>
    <div style="display:flex;height:34px;margin-top:22px;gap:2px"><div style="flex:${tier};background:${t.slateMark};border-radius:6px 0 0 6px"></div><div style="flex:${spread};background:${C.orange};border-radius:0 6px 6px 0"></div></div>
    <div style="display:flex;justify-content:space-between;font:500 19px Inter;color:${t.muted};margin-top:8px"><span>Wholesale ${Math.round((tier / rev) * 100)}%</span><span>Spread ${pct}% of revenue</span></div>
    <div style="font:500 22px/1.4 Inter;color:${t.fg};margin-top:22px">Platform cost per client: about <b>${R(perClient)}</b>/mo.</div>
    <div style="font:400 19px/1.4 Inter;color:${t.muted};margin-top:14px">Illustrative only, not a forecast. Gross spread before the partner’s own costs: delivery team, payment fees, tax and ad spend. Margin depends on the retail price you set.</div>
  </div>`;
  return frame({ w, h, dark, eyebrow: 'Agency partner model', title: 'Resell FluxMuse under your own brand', headW: 1180, body });
});

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9342 });
