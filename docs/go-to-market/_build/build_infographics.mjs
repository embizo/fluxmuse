// Infographics 1–6 (with _square / _dark / _portrait variants) → ../assets/infographics
// Usage: node build_infographics.mjs [nameFilter]
import { join } from 'node:path';
import { renderJobs, ASSETS } from './lib/page.mjs';
import { frame, markers, ringEdges, T, C, icon } from './lib/ig.mjs';
import { COUNTRIES, SOON, billingOf } from './lib/africa.mjs';

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
    ['Plan', 'Strategist', 'target', 'Goals, channel mix, budget, ROI forecast'],
    ['Create', 'Creator', 'pen', sq ? 'Copy & images in Zulu, Pidgin, Swahili +' : 'Copy & images in Zulu, Pidgin, Swahili, Afrikaans, English +'],
    ['Publish', 'Publisher', 'send', 'Social, WhatsApp, email, SMS, USSD'],
    ['Sell', 'WhatsApp commerce', 'bag', 'Catalog, cart and local payments in chat'],
    ['Learn', 'Analyst', 'chart', 'RAG memory, cohorts, auto-optimisation'],
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
const rails = ['Yoco card', 'Ozow EFT', 'Paystack', 'pawaPay mobile money', 'Fincra'];
const flowNodes = [
  ['Discover', 'megaphone', 'Ad, post, QR code or wa.me short link'],
  ['Chat', 'chat', 'Chatbot and WhatsApp Flows reply instantly'],
  ['Catalog', 'bag', 'Buyers browse products inside the chat'],
  ['Cart', 'cart', 'Items and totals, still in WhatsApp'],
  ['Pay', 'card', null],
  ['Confirmed', 'checkCircle', 'Order confirmed, status updates on WhatsApp'],
  ['Loyalty', 'heart', 'Rewards and retargeting bring buyers back'],
];
variants('whatsapp-commerce-flow', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080;
  const railChips = (fs) => rails.map((r) => `<span class="chip" style="font-size:${fs}px;padding:4px 11px">${r}</span>`).join('');
  const foot = `<div style="position:absolute;left:${sq ? 56 : 88}px;bottom:${sq ? 36 : 40}px;font:400 ${sq ? 19 : 21}px Inter;color:${t.muted};width:${sq ? 740 : 1300}px">All five rails live September 2026 (pawaPay &amp; Fincra from 14 Sept).</div>`;
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
      ${desc ? `<div style="font:400 22px/1.36 Inter;color:${t.muted};margin-top:6px">${desc}</div>` : `<div style="font:400 22px/1.3 Inter;color:${t.muted};margin:4px 0 10px">Local rails, no redirects</div><div style="display:flex;flex-wrap:wrap;gap:8px">${railChips(19)}</div>`}
    </div>`).join('')}
    <div class="chip" style="position:absolute;left:${(cxs[1] + cxs[4]) / 2}px;top:${yb + 104}px;transform:translate(-50%,-50%);font-size:21px;background:${t.bg};border:2px solid ${C.orange};color:${t.fg}">${icon('refresh', 20, C.orange)} Abandoned cart? Automatic recovery message</div>
    <div class="chip" style="position:absolute;left:${(cxs[0] + cxs[6]) / 2}px;top:${yb + 228}px;transform:translate(-50%,-50%);font-size:21px;background:${t.bg};border:2px solid ${t.slateMark};color:${t.fg}">${icon('users', 20, t.slateMark)} Segments and retargeting start the next sale</div>
    ${foot}`;
    return frame({ w, h, dark, eyebrow: 'WhatsApp commerce', title: 'From first tap to repeat order, all inside WhatsApp', headW: 1560, body });
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
  <div style="position:absolute;left:118px;top:${ry(6) + rh + 30}px;font:600 20px Inter;color:${t.fg}">Abandoned-cart recovery</div>
  <div style="position:absolute;left:532px;top:${ry(6) + rh + 30}px;font:600 20px Inter;color:${t.fg}">Retargeting loop</div>
  ${foot}`;
  return frame({ w, h, dark, eyebrow: 'WhatsApp commerce', title: 'From tap to repeat order', mark: 'tr', headW: 760, body });
}, { square: true });

// ============ 3. payment-coverage-map (tile-grid cartogram) ============
const RAMP = { light: ['#FFE9D6', '#FFC08F', '#FF9442', '#FF6A00'], dark: ['#3A2718', '#7A3A0C', '#C24E00', '#FF6A00'] };
const tileText = (dark, n) => (dark ? (n === 4 ? C.night : '#FFFFFF') : C.ink);
variants('payment-coverage-map', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080; const ramp = RAMP[dark ? 'dark' : 'light'];
  const counts = [1, 2, 3, 4].map((k) => COUNTRIES.filter((c) => c[4].length === k).length);
  const ts = sq ? 102 : 124, tg = sq ? 8 : 10, mx = sq ? 56 : 88, my = sq ? 196 : 238;
  const soonBorder = dark ? '#8A96A3' : '#8A949E';
  const tiles = COUNTRIES.map(([iso, name, c, r, rs]) => { const n = rs.length; return `<div style="position:absolute;left:${mx + c * (ts + tg)}px;top:${my + r * (ts + tg)}px;width:${ts}px;height:${ts}px;border-radius:${sq ? 14 : 16}px;background:${ramp[n - 1]};color:${tileText(dark, n)};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4px">
    <div style="font:700 ${sq ? 30 : 36}px/1 Poppins">${iso}</div><div style="font:600 ${sq ? 14 : 17}px/1.12 Inter;margin-top:${sq ? 4 : 6}px">${name}</div></div>`; }).join('')
    + SOON.map(([iso, name, c, r]) => `<div style="position:absolute;left:${mx + c * (ts + tg)}px;top:${my + r * (ts + tg)}px;width:${ts}px;height:${ts}px;border-radius:${sq ? 14 : 16}px;border:${sq ? 2.5 : 3}px dashed ${soonBorder};color:${t.fg};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:2px">
    <div style="font:700 ${sq ? 26 : 32}px/1 Poppins">${iso}</div><div style="font:600 ${sq ? 14 : 17}px/1.12 Inter;margin-top:${sq ? 2 : 4}px">${name}</div><div style="font:700 ${sq ? 12 : 15}px/1.1 Inter;color:${t.muted};margin-top:${sq ? 2 : 4}px;text-transform:uppercase;letter-spacing:.03em;max-width:${sq ? 70 : 100}px">Coming soon</div></div>`).join('');
  const swatch = (fs, k) => k === 0 ? `<span style="flex:none;width:${fs + 8}px;height:${fs + 8}px;border-radius:7px;border:2.5px dashed ${soonBorder};box-sizing:border-box"></span>`
    : `<span style="flex:none;width:${fs + 8}px;height:${fs + 8}px;border-radius:7px;background:${ramp[k - 1]};${k === 1 && !dark ? `border:1.5px solid #F2C9A6` : ''}"></span>`;
  const legend = (fs) => `<div style="display:flex;${sq ? 'flex-wrap:wrap;gap:8px 22px' : 'flex-direction:column;gap:10px'}">${[4, 3, 2, 1, 0].map((k) => `<div style="display:flex;align-items:center;gap:10px;font:500 ${fs}px Inter;color:${t.fg}">${swatch(fs, k)}<b>${k ? `${k} rail${k > 1 ? 's' : ''}` : 'Coming soon'}</b> <span style="color:${t.muted}">· ${k ? `${counts[k - 1]} ${counts[k - 1] === 1 ? 'country' : 'countries'}` : 'Botswana, Namibia'}</span></div>`).join('')}</div>`;
  const stats = [['5', 'live payment rails'], ['23', 'countries covered'], ['+2', 'coming soon'], ['40+', 'mobile money operators']];
  const note = `All five rails live September 2026 (pawaPay &amp; Fincra from 14 Sept). <b>*</b>South Sudan &amp; Zimbabwe: Fincra payouts only; sales open once collection is confirmed.`;
  if (!sq) {
    const body = `${tiles}
    <div style="position:absolute;left:1308px;top:238px;width:524px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
        ${stats.map(([n, l]) => `<div class="card" style="padding:16px 18px"><div style="font:700 48px/1 Poppins;color:${C.orange}">${n}</div><div style="font:500 21px/1.25 Inter;color:${t.fg};margin-top:6px">${l}</div></div>`).join('')}
      </div>
      <div style="font:700 24px Poppins;color:${t.fg};margin:28px 0 12px">Rails per country</div>${legend(22)}
      <div style="font:400 20px/1.4 Inter;color:${t.muted};margin-top:22px">${note}</div>
    </div>`;
    return frame({ w, h, dark, eyebrow: 'Payments coverage', title: 'Local payments in 23 African countries', sub: 'Tiles are placed roughly by geography; every tile is the same size.', body });
  }
  const body = `${tiles}
  <div style="position:absolute;left:56px;top:${my + 3 * (ts + tg) + 8}px;width:520px">${stats.map(([n, l]) => `<div style="margin-bottom:8px;white-space:nowrap"><span style="font:700 40px/1 Poppins;color:${C.orange}">${n}</span> <span style="font:500 21px Inter;color:${t.fg}">${l}</span></div>`).join('')}</div>
  <div style="position:absolute;left:56px;top:${my + 6 * (ts + tg) + 34}px;right:56px">${legend(19)}
  <div style="font:400 18px/1.35 Inter;color:${t.muted};margin-top:10px">${note}</div></div>`;
  return frame({ w, h, dark, eyebrow: 'Payments coverage', title: 'Local payments in 23 countries', mark: 'tr', headW: 760, body });
}, { square: true });

// ============ 4. payment-rails-matrix ============
const REGIONS = [
  ['Southern Africa', [['South Africa', 'ZA', 'ZAR'], ['Zambia', 'ZM', 'ZMW'], ['Malawi', 'MW', 'MWK'], ['Mozambique', 'MZ', 'MZN'], ['Lesotho', 'LS', 'LSL'], ['Zimbabwe', 'ZW', 'USD'], ['Botswana', 'BW', 'BWP', true], ['Namibia', 'NA', 'NAD', true]]],
  ['East Africa', [['Kenya', 'KE', 'KES'], ['Uganda', 'UG', 'UGX'], ['Tanzania', 'TZ', 'TZS'], ['Rwanda', 'RW', 'RWF'], ['Ethiopia', 'ET', 'ETB'], ['South Sudan', 'SS', 'SSP']]],
  ['West Africa', [['Nigeria', 'NG', 'NGN'], ['Ghana', 'GH', 'GHS'], ["Côte d'Ivoire", 'CI', 'XOF'], ['Senegal', 'SN', 'XOF'], ['Benin', 'BJ', 'XOF'], ['Burkina Faso', 'BF', 'XOF'], ['Sierra Leone', 'SL', 'SLE']]],
  ['Central Africa', [['Cameroon', 'CM', 'XAF'], ['Rep. of the Congo', 'CG', 'XAF'], ['Gabon', 'GA', 'XAF'], ['DR Congo', 'CD', 'CDF/USD']]],
];
const RAILS = ['Yoco', 'Ozow', 'Paystack', 'pawaPay', 'Fincra'];
const railsOf = Object.fromEntries(COUNTRIES.map((c) => [c[0], c[4]]));
{
  const build = ({ dark, w, h, portrait }) => {
    const t = T(dark);
    const colW = portrait ? { name: 226, iso: 56, cur: 100, bill: 106, rail: 96 } : { name: 206, iso: 48, cur: 112, bill: 96, rail: 78 };
    const tw = colW.name + colW.iso + colW.cur + colW.bill + 5 * colW.rail;
    const rowH = portrait ? 33 : 44, regH = portrait ? 36 : 44, hdH = portrait ? 58 : 70, fs = portrait ? 20 : 22;
    const soonC = dark ? '#8A96A3' : '#8A949E';
    const mark = (st) => st === 'c' ? `<svg width="${fs + 8}" height="${fs + 8}" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="${C.orange}"/><path d="M9 16.5l4.5 4.5L23 11.5" fill="none" stroke="${C.night}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`
      : st === 'p' ? `<svg width="${fs + 8}" height="${fs + 8}" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12.5" fill="none" stroke="${C.orange}" stroke-width="3"/><text x="16" y="21.5" text-anchor="middle" font-family="Inter" font-weight="700" font-size="15" fill="${t.fg}">P</text></svg>`
      : st === 's' ? `<span style="display:inline-block;width:${fs + 14}px;height:${fs + 4}px;border-radius:7px;border:2.5px dashed ${soonC};box-sizing:border-box"></span>` : `<span style="color:${t.line};font:700 ${fs}px Inter">·</span>`;
    const header = `<div style="display:flex;align-items:flex-end;height:${hdH}px;border-bottom:2px solid ${t.fg};font:700 ${fs - 1}px Inter;color:${t.fg}">
      <div style="width:${colW.name}px">Country</div><div style="width:${colW.iso}px">ISO</div><div style="width:${colW.cur}px">Currency</div>
      <div style="width:${colW.bill}px;line-height:1.1;padding-bottom:3px">Billing<br>currency</div>
      ${RAILS.map((r) => `<div style="width:${colW.rail}px;text-align:center;line-height:1.15;font-size:${fs - (portrait ? 5 : 7)}px">${r}<div style="font:600 ${portrait ? 14 : 15}px/1.1 Inter;color:${dark ? '#7FD18A' : '#1E6B2A'};margin:3px 0 6px">live</div></div>`).join('')}</div>`;
    const billCell = (iso, soon) => {
      if (soon) return `<div style="width:${colW.bill}px;color:${t.muted};font-style:italic">waitlist</div>`;
      const b = billingOf(iso); const local = b !== 'USD';
      return `<div style="width:${colW.bill}px;font-weight:${local ? 700 : 500};color:${local ? t.accentText : t.fg}">${b}${iso === 'SS' || iso === 'ZW' ? '*' : ''}</div>`;
    };
    const table = (regs) => `<div style="width:${tw}px">${header}${regs.map(([rn, list]) => `
      <div style="height:${regH}px;display:flex;align-items:flex-end;padding-bottom:5px;font:700 ${fs}px Poppins;color:${t.accentText};border-bottom:1.5px solid ${t.line}">${rn}</div>
      ${list.map(([name, iso, cur, soon]) => { const rs = railsOf[iso] || []; return `<div style="height:${rowH}px;display:flex;align-items:center;border-bottom:1px solid ${t.line};font:400 ${fs}px Inter;color:${soon ? t.muted : t.fg}">
        <div style="width:${colW.name}px;font-weight:500">${name}</div><div style="width:${colW.iso}px;color:${t.muted}">${iso}</div><div style="width:${colW.cur}px;color:${t.muted}">${cur}</div>${billCell(iso, soon)}
        ${soon ? `<div style="width:${5 * colW.rail}px;display:flex;justify-content:center"><span style="display:inline-flex;align-items:center;height:${rowH - 10}px;padding:0 16px;border-radius:999px;border:2.5px dashed ${soonC};font:700 ${fs - 4}px Inter;color:${t.fg};letter-spacing:.02em">Coming soon · no rail yet</span></div>`
          : RAILS.map((r) => `<div style="width:${colW.rail}px;display:flex;justify-content:center">${mark(rs.includes(r) ? 'c' : rs.includes(r + '*') ? 'p' : '')}</div>`).join('')}</div>`; }).join('')}`).join('')}</div>`;
    const lfs = portrait ? 17 : 20;
    const legend = `<div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 24px;font:500 ${lfs}px Inter;color:${t.fg}">
      <span style="display:flex;align-items:center;gap:8px">${mark('c')} available</span><span style="display:flex;align-items:center;gap:8px">${mark('p')} payouts only</span><span style="display:flex;align-items:center;gap:8px">${mark('s')} coming soon</span></div>
      <div style="font:400 ${lfs}px/1.4 Inter;color:${t.muted};margin-top:8px">All five rails live September 2026 (pawaPay &amp; Fincra from 14 Sept). Billing: <b style="color:${t.fg}">ZAR</b> in South Africa; fixed local prices in <b style="color:${t.fg}">NGN, KES, GHS</b>; <b style="color:${t.fg}">USD</b> in the other 19. *South Sudan &amp; Zimbabwe: Fincra payouts only; sales open once collection is confirmed.</div>`;
    if (portrait) {
      const top = 180;
      const body = `<div style="position:absolute;left:56px;top:${top}px">${table(REGIONS)}</div><div style="position:absolute;left:56px;top:${top + hdH + 4 * regH + 25 * rowH + 14}px;width:968px">${legend}</div>`;
      return frame({ w, h, dark, eyebrow: 'Payment rails', title: '23 countries × 5 rails', mark: 'tr', headW: 760, body });
    }
    const top = 214, gap = 1744 - 2 * tw;
    const body = `<div style="position:absolute;left:88px;top:${top}px">${table(REGIONS.slice(0, 2))}</div>
      <div style="position:absolute;left:${88 + tw + gap}px;top:${top}px">${table(REGIONS.slice(2))}</div>
      <div style="position:absolute;left:${88 + tw + gap}px;top:${top + hdH + 2 * regH + 11 * rowH + 22}px;width:${tw}px">${legend}</div>`;
    return frame({ w, h, dark, eyebrow: 'Payment rails', title: '23 countries × 5 rails, by region', mark: 'tr', body });
  };
  add('payment-rails-matrix', 1920, 1080, build({ dark: false, w: 1920, h: 1080 }));
  add('payment-rails-matrix_dark', 1920, 1080, build({ dark: true, w: 1920, h: 1080 }));
  add('payment-rails-matrix_portrait', 1080, 1350, build({ dark: false, w: 1080, h: 1350, portrait: true }));
  add('payment-rails-matrix_portrait_dark', 1080, 1350, build({ dark: true, w: 1080, h: 1350, portrait: true }));
}

// ============ 5. platform-stack ============
variants('platform-stack', ({ dark, w, h }) => {
  const t = T(dark);
  const layers = [
    ['Channels', 'globe', C.blue, ['WhatsApp Cloud API', 'Facebook Pages', 'Instagram*', 'Messenger', 'Email', 'SMS', 'USSD', 'Website chat widget', 'Link-in-bio']],
    ['AI workforce', 'sparkles', C.violet, ['Strategist', 'Creator', 'Publisher', 'Analyst', '+ 23 specialist Flux agents', 'AI Agent Marketplace']],
    ['Commerce & payments', 'bag', C.orange, ['WhatsApp catalog', 'Cart checkout in chat', 'Orders & status updates', 'Abandoned-cart recovery', '5 live rails: Yoco · Ozow · Paystack · pawaPay · Fincra']],
    ['Growth & CRM', 'trend', C.green, ['Lead scoring', 'CRM deals', 'Segmentation', 'Loyalty programmes', 'Churn-risk scoring', 'Sentiment analysis', 'A/B testing', 'Competitor tracking']],
    ['Integrations', 'plug', C.teal, ['Shopify', 'WooCommerce', 'Takealot', 'HubSpot / CRM sync', 'Accounting sync', 'Slack', 'Zapier', 'Public API & keys']],
    ['Trust', 'shield', dark ? '#8FA3AD' : C.slate, ['POPIA · NDPR · GDPR ready', 'Row-level security on every table', 'Encrypted tokens', 'Audit export', 'Data export & account deletion']],
  ];
  const y0 = 218, lh = 112, g = 14;
  const body = layers.map(([n, ic, col, chips], i) => `<div class="card" style="position:absolute;left:88px;top:${y0 + i * (lh + g)}px;width:1744px;height:${lh}px;display:flex;align-items:center;overflow:hidden">
    <div style="align-self:stretch;width:10px;background:${col}"></div>
    <div style="width:340px;display:flex;align-items:center;gap:14px;padding-left:22px">${icon(ic, 34, col, 2.2)}<span style="font:700 27px/1.1 Poppins;color:${t.fg}">${n}</span></div>
    <div style="flex:1;display:flex;flex-wrap:wrap;gap:10px;padding-right:22px">${chips.map((c) => c === 'Instagram*'
      ? `<span class="chip" style="background:transparent;border:2px dashed ${t.muted};color:${t.fg};font-weight:500">Instagram · in Meta review*</span>`
      : `<span class="chip" style="background:${t.card2};color:${t.fg};font-weight:500">${c}</span>`).join('')}</div></div>`).join('') +
    `<div style="position:absolute;left:88px;bottom:42px;width:1360px;font:400 21px/1.4 Inter;color:${t.muted}">*Instagram publishing, comments and DMs are in Meta App Review, not live yet. Runs on React/Vite, Supabase (Postgres, Auth, 140+ Edge Functions) and Vercel.</div>`;
  return frame({ w, h, dark, eyebrow: 'Platform', title: 'One platform, from channel to checkout', body });
});

// ============ 6. agency-partner-model ============
variants('agency-partner-model', ({ dark, w, h }) => {
  const t = T(dark);
  const clients = 20, retail = 1500, list = 7999, tier = 5599, rev = clients * retail, spread = rev - tier; // partner wholesale = Agency list −30%
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
    <div style="font:400 20px/1.3 Inter;color:${t.muted};margin-top:4px">Platform, AI agents, payments</div></div>
  <div style="position:absolute;left:350px;top:${y + 62}px;width:160px;text-align:center;font:600 20px/1.3 Inter;color:${t.fg}">Partner price<br><span style="color:${t.accentText}">${R(tier)}/mo</span></div>
  <div style="position:absolute;left:350px;top:${y + 166}px;width:160px;text-align:center;font:500 17px/1.3 Inter;color:${t.muted}">30% off the<br>${R(list)} Agency tier</div>
  <div class="card" style="position:absolute;left:514px;top:${y - 20}px;width:330px;height:340px;padding:22px 24px;border:2.5px solid ${C.orange}">
    <div style="display:flex;align-items:center;gap:12px">${icon('briefcase', 34, C.orange)}<span style="font:700 28px Poppins;color:${t.fg}">Your agency</span></div>
    ${['Full white-label: your brand', '50 client sub-accounts', 'Reseller billing', '80 channels · 500,000 AI credits/mo'].map((s) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:14px;font:400 22px/1.3 Inter;color:${t.fg}">${icon('check', 24, C.orange, 3)}<span>${s}</span></div>`).join('')}</div>
  <div style="position:absolute;left:846px;top:${y + 60}px;width:146px;text-align:center;font:600 20px/1.3 Inter;color:${t.fg}">Retail price<br><span style="color:${t.accentText}">you set</span></div>
  <div class="card" style="position:absolute;left:994px;top:${y + 10}px;width:238px;height:280px;padding:20px;text-align:center">
    <div style="display:grid;grid-template-columns:repeat(5,26px);gap:10px;justify-content:center">${Array.from({ length: clients }, (_, i) => `<span style="width:26px;height:26px;border-radius:50%;background:${[C.blue, C.teal, C.green, C.violet, C.magenta][i % 5]};opacity:.9"></span>`).join('')}</div>
    <div style="font:700 26px Poppins;color:${t.fg};margin-top:18px">Your clients</div>
    <div style="font:400 20px/1.3 Inter;color:${t.muted}">One sub-account each</div></div>
  <div style="position:absolute;left:88px;top:${y + 380}px;width:1144px;padding:24px 28px;border-radius:20px;background:${t.chipBg}">
    <div style="font:700 30px Poppins;color:${t.fg}">Set your own retail price and keep the spread.</div>
    <div style="font:400 22px/1.4 Inter;color:${t.fg};margin-top:6px">FluxMuse invoices your agency the partner wholesale price, <b>${R(tier)}/mo</b> (30% off the ${R(list)} Agency tier), for 50 client sub-accounts, full white-label and reseller billing. You bill your clients at a retail price you set.</div></div>

  <div class="card" style="position:absolute;left:1290px;top:236px;width:542px;padding:30px 32px">
    <span class="chip" style="background:${dark ? 'rgba(253,216,53,.14)' : '#FFF6D1'};color:${dark ? '#FDE68A' : '#6B4E00'}">${icon('flag', 18, dark ? '#FDE68A' : '#6B4E00')} Illustrative</span>
    <div style="font:700 30px/1.2 Poppins;color:${t.fg};margin-top:16px">${clients} clients at ${R(retail)}/mo</div>
    <div style="font:400 20px Inter;color:${t.muted};margin-top:2px">retail price set by the partner</div>
    ${[['Billed to clients', `${clients} × ${R(retail)}`, R(rev), t.fg], ['Partner wholesale price', `30% off ${R(list)}`, '− ' + R(tier), t.muted]].map(([a, b, c, col]) => `<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:20px;padding-bottom:14px;border-bottom:1.5px solid ${t.line}"><div><div style="font:600 22px Inter;color:${t.fg}">${a}</div><div style="font:400 20px Inter;color:${t.muted}">${b}</div></div><div style="font:700 30px Poppins;color:${col}">${c}</div></div>`).join('')}
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:18px"><div style="font:700 24px Inter;color:${t.fg}">Gross spread /mo</div><div style="font:700 44px Poppins;color:${t.accentText}">${R(spread)}</div></div>
    <div style="display:flex;height:34px;margin-top:22px;gap:2px"><div style="flex:${tier};background:${t.slateMark};border-radius:6px 0 0 6px"></div><div style="flex:${spread};background:${C.orange};border-radius:0 6px 6px 0"></div></div>
    <div style="display:flex;justify-content:space-between;font:500 19px Inter;color:${t.muted};margin-top:8px"><span>Wholesale ${Math.round((tier / rev) * 100)}%</span><span>Spread ${pct}% of revenue</span></div>
    <div style="font:500 22px/1.4 Inter;color:${t.fg};margin-top:22px">Platform cost per client: about <b>${R(perClient)}</b>/mo.</div>
    <div style="font:400 19px/1.4 Inter;color:${t.muted};margin-top:14px">Illustrative only, not a forecast. Gross spread before the partner’s own costs: delivery team, VAT, payment fees and ad spend. Margin depends on the retail price you set.</div>
  </div>`;
  return frame({ w, h, dark, eyebrow: 'Agency partner model', title: 'Resell FluxMuse under your own brand', headW: 1180, body });
});

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9342 });
