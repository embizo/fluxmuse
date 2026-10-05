// Infographics 15+ (refreshed 2026-10-05 to CURRENT_OFFER.md) → ../assets/infographics
// pricing-regional, founding-member-offer, target-segments, market-entry-sequence,
// case-study-template, segment-solo/sme/agency. (gauteng-pilot and founding-member-offer_pilot retired.) Usage: node build_infographics3.mjs [nameFilter]
import { join } from 'node:path';
import { renderJobs, ASSETS } from './lib/page.mjs';
import { frame, T, C, icon } from './lib/ig.mjs';
import { COUNTRIES, SOON, miniMap } from './lib/africa.mjs';

const OUT = join(ASSETS, 'infographics');
const jobs = [];
const add = (name, w, h, html) => jobs.push({ name, dir: 'infographics', html, w, h, out: join(OUT, name + '.png') });
// base + _dark (1920×1080); optional light _square (1080×1080)
const variants = (base, fn, { square = false } = {}) => {
  add(base, 1920, 1080, fn({ dark: false, w: 1920, h: 1080 }));
  add(base + '_dark', 1920, 1080, fn({ dark: true, w: 1920, h: 1080 }));
  if (square) add(base + '_square', 1080, 1080, fn({ dark: false, w: 1080, h: 1080 }));
};
const R = (n) => 'R' + n.toLocaleString('en-US');
const tintOf = (dark) => (dark ? 'rgba(255,106,0,.10)' : C.tint);
const soonC = (dark) => (dark ? '#8A96A3' : '#8A949E');
// Orange fill always carries Night text (white on Flux Orange fails WCAG).
const orangeBand = (inner, style = '') => `<div style="background:${C.orange};color:${C.night};${style}">${inner}</div>`;
const label = (t, s, fs = 17) => `<div style="font:700 ${fs}px Inter;letter-spacing:.08em;text-transform:uppercase;color:${t.accentText}">${s}</div>`;

// ============ 15. pricing-regional (tier_regional_prices; outside ZA priced, NOT on sale) ============
{
  const tiers = [
    ['Nano', ['R149', '₦12,000', 'KSh 1,199', 'GH₵ 99', '$8']],
    ['Micro', ['R289', '₦24,000', 'KSh 2,299', 'GH₵ 199', '$16']],
    ['Starter', ['R499', '₦41,000', 'KSh 3,999', 'GH₵ 339', '$27']],
    ['Growth', ['R1,999', '₦165,000', 'KSh 15,999', 'GH₵ 1,359', '$109']],
    ['Scale', ['R4,999', '₦413,000', 'KSh 39,999', 'GH₵ 3,399', '$269']],
    ['Corporate', ['R6,999', '₦579,000', 'KSh 56,999', 'GH₵ 4,799', '$379']],
    ['Agency', ['R9,999', '₦829,000', 'KSh 80,999', 'GH₵ 6,799', '$539']],
  ];
  const cur = [['South Africa', 'ZAR'], ['Nigeria', 'NGN'], ['Kenya', 'KES'], ['Ghana', 'GHS'], ['Other markets', 'USD']];
  variants('pricing-regional', ({ dark, w, h }) => {
    const t = T(dark); const sq = w === 1080;
    const L = sq ? { x: 56, tw: 968, tierW: 150, top: 200, hdH: 116, rowH: 76, vf: 24 } : { x: 88, tw: 1744, tierW: 260, top: 236, hdH: 120, rowH: 78, vf: 36 };
    const cw = (L.tw - L.tierW) / 5;
    const header = `<div style="display:flex;height:${L.hdH}px;align-items:flex-end;border-bottom:2px solid ${t.fg};padding-bottom:10px">
      <div style="width:${L.tierW}px;font:700 ${sq ? 18 : 22}px Inter;color:${t.muted}">Plan, per month</div>
      ${cur.map(([c, code], i) => `<div style="width:${cw}px;padding-left:${sq ? 10 : 18}px;${i === 0 ? '' : `opacity:.95;`}${i === 1 ? `border-left:2px dashed ${t.line}` : ''}"><div style="font:700 ${sq ? 28 : 36}px/1 Poppins;color:${i === 0 ? t.accentText : t.fg}">${code}</div><div style="font:500 ${sq ? 16 : 21}px/1.2 Inter;color:${t.fg};margin-top:6px">${c}</div>
        <div style="display:inline-block;margin-top:6px;padding:2px 10px;border-radius:999px;font:700 ${sq ? 13 : 16}px Inter;${i === 0 ? `background:${C.orange};color:${C.night}` : `border:1.5px dashed ${soonC(dark)};color:${t.muted}`}">${i === 0 ? 'On sale' : 'Not yet on sale'}</div></div>`).join('')}</div>`;
    const rows = tiers.map(([n, ps]) => `<div style="display:flex;height:${L.rowH}px;align-items:center;border-bottom:1.5px solid ${t.line}">
      <div style="width:${L.tierW}px;padding-left:${sq ? 10 : 20}px;font:700 ${sq ? 23 : 30}px Poppins;color:${t.fg}">${n}</div>
      ${ps.map((p, i) => `<div style="width:${cw}px;padding-left:${sq ? 10 : 18}px;align-self:stretch;display:flex;align-items:center;${i === 0 ? `background:${tintOf(dark)};` : ''}${i === 1 ? `border-left:2px dashed ${t.line}` : ''}"><span style="font:700 ${L.vf}px/1 Poppins;color:${i === 0 ? t.fg : t.muted};white-space:nowrap">${p}</span></div>`).join('')}</div>`).join('');
    const body = `<div style="position:absolute;left:${L.x}px;top:${L.top}px;width:${L.tw}px">${header}${rows}</div>
      <div style="position:absolute;left:${L.x}px;bottom:${sq ? 30 : 34}px;width:${sq ? 760 : 1500}px;font:400 ${sq ? 16 : 20}px/1.4 Inter;color:${t.muted}">Free plan R0 everywhere; Custom on request. Annual = 10× monthly. Only South Africa is on sale today: local prices are set, but Nigeria, Kenya, Ghana and USD checkout open only once payment-provider accounts are live and checkout is tested.</div>`;
    return frame({ w, h, dark, eyebrow: 'Pricing by market', title: sq ? 'Regional pricing' : 'One set of plans, priced for each market', sub: sq ? 'On sale in South Africa only.' : 'On sale in South Africa today. Local prices are set for the next markets.', mark: 'tr', headW: sq ? 740 : 1400, body });
  }, { square: true });
}

// ============ 16. founding-member-offer ============
const badge = (size, dark) => `<div style="flex:none;width:${size}px;height:${size}px;border-radius:50%;background:${C.orange};display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 ${Math.round(size / 18)}px ${dark ? 'rgba(255,106,0,.22)' : C.tint}">
  <div style="width:${size - 22}px;height:${size - 22}px;border-radius:50%;border:3px dashed ${C.night};display:flex;flex-direction:column;align-items:center;justify-content:center;color:${C.night};text-align:center">
    ${icon('sparkles', Math.round(size / 3.6), C.night, 2.4)}<div style="font:800 ${Math.round(size / 11)}px/1.05 Poppins;letter-spacing:.04em;margin-top:4px">FOUNDING<br>MEMBER</div></div></div>`;
variants('founding-member-offer', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080;
  const fmList = [['Nano', 149, 104], ['Micro', 289, 202], ['Starter', 499, 349], ['Growth', 1999, 1399], ['Scale', 4999, 3499]];
  if (!sq) {
    const steps = [['1', 'Book a 20-minute call', 'See a demo on your own products'], ['2', 'Choose a paid plan', 'You pay from day one'], ['3', 'Pay 30% less', 'for your first two monthly bills']];
    const bars = [[1, 1399, true], [2, 1399, true], [3, 1999, false], [4, 1999, false]];
    const maxH = 230, bx = 1150, by = 920;
    const body = `
    <div class="card" style="position:absolute;left:88px;top:262px;width:918px;height:290px;padding:26px 32px;display:flex;gap:30px;align-items:center">${badge(190, dark)}
      <div><div style="font:800 96px/1 Poppins;color:${t.accentText};white-space:nowrap">30% off</div>
      <div style="font:700 32px/1.2 Poppins;color:${t.fg};margin-top:10px">your first two monthly bills</div>
      <div style="font:400 22px/1.35 Inter;color:${t.muted};margin-top:6px">Then the normal monthly price.</div></div></div>
    <div style="position:absolute;left:88px;top:586px;width:918px;display:flex;gap:16px">${steps.map(([n, a, b]) => `<div style="flex:1;display:flex;gap:12px;align-items:flex-start;padding:16px 16px;border-radius:18px;background:${t.card2}">
      <span style="flex:none;width:38px;height:38px;border-radius:50%;background:${C.orange};color:${C.night};font:700 20px Poppins;display:flex;align-items:center;justify-content:center">${n}</span>
      <div><div style="font:700 21px/1.2 Poppins;color:${t.fg}">${a}</div><div style="font:400 19px/1.3 Inter;color:${t.muted};margin-top:3px">${b}</div></div></div>`).join('')}</div>
    ${orangeBand(`<div style="display:flex;align-items:center;gap:20px">${icon('flag', 40, C.night, 2.4)}<div><div style="font:700 20px Inter;letter-spacing:.08em;text-transform:uppercase">For South African sign-ups</div><div style="font:800 40px/1.1 Poppins;margin-top:4px">Live now, while it lasts</div></div></div>
      <div style="font:600 21px/1.35 Inter;margin-top:10px">A discount on paid plans, not a free period. Agencies: see partner pricing.</div>`, 'position:absolute;left:88px;top:748px;width:918px;height:196px;border-radius:22px;padding:24px 30px')}
    <div class="card" style="position:absolute;left:1060px;top:262px;width:772px;height:682px;padding:26px 34px">
      <div style="display:flex;font:700 18px Inter;color:${t.muted};padding-bottom:8px;border-bottom:2px solid ${t.fg}"><span style="flex:1">Plan</span><span style="width:170px;text-align:right">Normal /mo</span><span style="width:230px;text-align:right">First two bills</span></div>
      ${fmList.map(([n, v, p]) => `<div style="display:flex;align-items:center;height:48px;border-bottom:1.5px solid ${t.line};font:500 22px Inter;color:${t.fg}"><span style="flex:1;font:700 23px Poppins">${n}</span><span style="width:170px;text-align:right;color:${t.muted}">${R(v)}</span><span style="width:230px;text-align:right;font:700 24px Poppins;color:${t.accentText}">${R(p)}</span></div>`).join('')}
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:22px"><div style="font:700 24px Poppins;color:${t.fg}">Example: Growth plan</div><div style="font:500 19px Inter;color:${t.muted}">R1,999/mo</div></div>
    </div>
    <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">
      <line x1="${bx - 20}" y1="${by}" x2="${bx + 4 * 160}" y2="${by}" stroke="${t.line}" stroke-width="2"/>
    </svg>
    ${bars.map(([m, v, disc], i) => { const bh = Math.round((v / 1999) * maxH); const x = bx + i * 160; return `
      <div style="position:absolute;left:${x}px;top:${by - bh}px;width:118px;height:${bh}px;border-radius:14px 14px 0 0;background:${disc ? C.orange : t.card2};${disc ? '' : `border:2px solid ${t.line};border-bottom:none`}"></div>
      <div style="position:absolute;left:${x - 20}px;top:${by - bh - 40}px;width:158px;text-align:center;font:700 26px Poppins;color:${t.fg}">${R(v)}</div>
      ${disc ? `<div style="position:absolute;left:${x}px;top:${by - bh + 14}px;width:118px;text-align:center;font:700 20px Inter;color:${C.night}">−30%</div>` : ''}
      <div style="position:absolute;left:${x - 20}px;top:${by + 6}px;width:158px;text-align:center;font:500 19px Inter;color:${t.muted}">Bill ${m}</div>`; }).join('')}
    <div style="position:absolute;left:88px;bottom:30px;width:1500px;font:400 20px/1.4 Inter;color:${t.muted}">30% off, rounded down to whole rands, on the first two monthly bills of a paid plan. South African sign-ups only. No end date set yet; it may close at any time.</div>`;
    return frame({ w, h, dark, eyebrow: 'Launch offer · South Africa', title: 'Become a Founding Member', sub: 'Join now and pay less while you get set up.', headW: 1300, body });
  }
  const body = `
  <div class="card" style="position:absolute;left:56px;top:200px;width:968px;height:240px;padding:24px 34px">
    <div style="display:flex;align-items:baseline;gap:22px"><span style="font:800 112px/1 Poppins;color:${t.accentText}">30% off</span><span style="font:700 34px/1.2 Poppins;color:${t.fg}">your first two<br>monthly bills</span></div>
    <div style="font:500 24px/1.35 Inter;color:${t.muted};margin-top:16px">A discount on paid plans, not a free period.</div></div>
  <div style="position:absolute;left:56px;top:470px;width:968px;display:flex;gap:26px;align-items:center">${badge(150, dark)}
    <div style="flex:1">${fmList.slice(0, 4).map(([n, v, p]) => `<div style="display:flex;justify-content:space-between;font:500 23px/1.75 Inter;color:${t.fg};border-bottom:1.5px solid ${t.line}"><b style="font-family:Poppins">${n}</b><span><span style="color:${t.muted}">${R(v)} →</span> <b style="color:${t.accentText}">${R(p)}</b></span></div>`).join('')}</div></div>
  ${orangeBand(`<div style="font:700 19px Inter;letter-spacing:.08em;text-transform:uppercase">South African sign-ups</div><div style="font:800 44px/1.1 Poppins;margin-top:6px">Live now, while it lasts</div><div style="font:600 22px Inter;margin-top:8px">fluxmuse.ai · paid plans from R149 a month</div>`, 'position:absolute;left:56px;top:740px;width:968px;height:206px;border-radius:22px;padding:22px 32px')}
  <div style="position:absolute;left:56px;bottom:26px;width:760px;font:400 17px Inter;color:${t.muted}">First two monthly bills of a paid plan. Agencies: see partner pricing.</div>`;
  return frame({ w, h, dark, eyebrow: 'Launch offer · South Africa', title: 'Become a Founding Member', mark: 'tr', headW: 760, body });
}, { square: true });

// founding-member-offer_pilot: retired 2026-10-05 (there is no pilot).

// ============ 17. target-segments ============
const SEGMENTS = [
  { key: 'solo', n: 1, name: 'Solo entrepreneurs', ic: 'users', tier: 'Nano R149', up: '→ Micro R289 → Starter R499', plan: 'Nano',
    who: 'Founder-run businesses of 1–5 people: side hustles, beauty and braiding, fashion resellers, home bakers, coaches, informal retailers selling on WhatsApp and social',
    whoShort: '1–5 people: beauty & braiding, fashion resellers, home bakers, coaches, informal retailers',
    pain: 'No time or budget for a marketer; DMs answered late; no shop page, so orders get lost in chats',
    promise: 'Send photos, get a shop link. Your marketing team lives in WhatsApp',
    motion: 'Founder-led: a demo on your own products, then a paid plan with Founding Member pricing',
    pains: ['No time or budget for a marketer, so posts go out when they can', 'Messages answered late, after hours or not at all', 'No shop page, so orders get lost in chats'],
    answers: ['Say POST and get a caption and picture, ready for your WhatsApp Status', 'The assistant answers customers in their language, day and night', 'Send product photos, get a shop link; every order arrives on WhatsApp'],
    price: 149, upNote: 'Micro R289 adds a channel and your own WhatsApp number; Starter R499 to grow' },
  { key: 'sme', n: 2, name: 'SMEs', ic: 'briefcase', tier: 'Growth R1,999', up: '→ Scale R4,999', plan: 'Growth',
    who: '5–200 staff: retail, restaurants and franchises, e-commerce brands, clinics, property, auto dealers, education, professional services',
    whoShort: '5–200 staff: retail, restaurants & franchises, e-commerce, clinics, property, auto, education',
    pain: 'Disconnected tools; agency retainers of R15k+/mo; WhatsApp handled by hand; no clear view of what sells',
    promise: 'Answer every customer, post every week, and see every order on WhatsApp',
    motion: 'Discovery call, demo on your products, proposal; set up by hand',
    pains: ['Disconnected tools and agency retainers of R15k+/mo', 'WhatsApp handled by hand by busy staff', 'No clear view of what sells'],
    answers: ['An AI marketing team on WhatsApp: posts, replies, catalogue and shop link', 'The assistant answers customers in their language, day and night', 'An order alert for every sale; reply SOLD to keep track'],
    price: 1999, upNote: 'Scale R4,999: 10 brands, 40 channels. Starter R499 for one brand' },
  { key: 'agency', n: 3, name: 'Agencies', ic: 'layers', tier: 'Partner R6,999', up: '/mo, 30% off Agency', plan: 'Agency',
    who: 'Marketing, digital and social media agencies and freelancers managing 5–50 small-business clients',
    whoShort: 'Marketing, digital and social media agencies and freelancers managing 5–50 small-business clients',
    pain: 'Margin squeeze; manual reporting; too many tools per client; clients asking for WhatsApp selling and AI',
    promise: 'Serve more clients under your brand: set your own retail price and keep the spread',
    motion: 'Partner conversation and demo, then the partner wholesale plan',
    pains: ['Margin squeeze on every client retainer', 'Manual reporting and too many tools per client', 'Clients asking for WhatsApp selling and AI'],
    answers: ['Partner price R6,999/mo: set your own retail price and keep the spread', 'White-label and multi-client, with unlimited brands and 80 channels', 'Offer clients a WhatsApp marketing team under your own brand'],
    price: 9999, upNote: 'Agency tier list price. White-label, multi-client, bring your own cloud' },
];
variants('target-segments', ({ dark, w, h }) => {
  const t = T(dark);
  const cw = (1744 - 2 * 26) / 3;
  const row = (k, v, extra = '') => `<div style="margin-top:16px">${label(t, k, 16)}<div style="font:400 20px/1.36 Inter;color:${t.fg};margin-top:5px;${extra}">${v}</div></div>`;
  const body = SEGMENTS.map((s, i) => `<div class="card" style="position:absolute;left:${88 + i * (cw + 26)}px;top:262px;width:${cw}px;height:652px;overflow:hidden">
    <div style="padding:20px 26px;background:${t.card2};display:flex;align-items:center;gap:14px">
      <span style="flex:none;width:52px;height:52px;border-radius:14px;background:${C.orange};display:flex;align-items:center;justify-content:center">${icon(s.ic, 28, C.night, 2.3)}</span>
      <div><div style="font:600 17px Inter;color:${t.muted}">Segment ${s.n}</div><div style="font:700 30px/1.1 Poppins;color:${t.fg}">${s.name}</div></div></div>
    <div style="padding:0 26px">
      ${row('Who', s.who)}
      <div style="margin-top:16px">${label(t, 'Main tier', 16)}<div style="margin-top:5px;font:700 24px Poppins;color:${t.fg}">${s.tier} <span style="font:500 20px Inter;color:${t.muted}">${s.up}</span></div></div>
      ${row('Pain', s.pain, `color:${t.muted}`)}
      <div style="margin-top:16px">${label(t, 'Promise', 16)}<div style="font:600 22px/1.3 Poppins;color:${t.fg};margin-top:6px;padding-left:14px;border-left:4px solid ${C.orange}">“${s.promise}”</div></div>
      ${row('Buying motion', s.motion)}
    </div></div>`).join('') + `
    <div style="position:absolute;left:88px;bottom:32px;width:1400px;font:400 20px/1.4 Inter;color:${t.muted}">Corporate and Custom are taken inbound only. Agencies buy the Agency tier at the R6,999/mo partner price (30% off R9,999).</div>`;
  return frame({ w, h, dark, eyebrow: 'Who we sell to', title: 'Three launch segments, South Africa first', sub: 'Opening with a small first group of businesses, set up by hand.', headW: 1400, body });
});

// ============ 18. market-entry-sequence ============
variants('market-entry-sequence', ({ dark, w, h }) => {
  const t = T(dark);
  const rest = COUNTRIES.map((c) => c[0]).filter((iso) => !['ZA', 'NG', 'KE', 'GH'].includes(iso));
  const steps = [
    { n: '1', title: 'South Africa', tag: 'Home market', hi: (iso) => (iso === 'ZA' ? 'on' : 'off'), billing: 'Billed in ZAR',
      items: ['Open now: paid plans, Paystack live', 'A small first group of businesses, set up by hand', 'Founding Member: 30% off the first two monthly bills'] },
    { n: '2', title: 'Nigeria, Kenya, Ghana', tag: 'Next · no date set', hi: (iso) => (['NG', 'KE', 'GH'].includes(iso) ? 'on' : iso === 'ZA' ? 'soft' : 'off'), billing: 'Priced in NGN, KES, GHS',
      items: ['Not yet on sale', 'Opens once Fincra and pawaPay accounts are live and checkout is tested'] },
    { n: '3', title: 'Other covered markets', tag: 'Later · self-serve', hi: (iso) => (rest.includes(iso) ? 'on' : ['ZA', 'NG', 'KE', 'GH'].includes(iso) ? 'soft' : 'off'), billing: 'USD, once open',
      items: ["Côte d'Ivoire, Rwanda, Uganda, Tanzania, Zambia, francophone West & Central Africa and more", 'Markets pawaPay and Fincra cover; accounts pending'] },
    { n: '4', title: 'Botswana & Namibia', tag: 'Coming soon', soon: true, hi: (iso, soon) => (soon ? 'soon' : 'off'), billing: 'Waitlist only',
      items: ['Shown in the region picker', 'Opens once a provider covers them'] },
  ];
  const cw = (1744 - 3 * 44) / 4, top = 250, ch = 580;
  const body = `
  <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">
    ${[0, 1, 2].map((i) => { const x = 88 + (i + 1) * cw + i * 44; return `<path d="M${x + 10} ${top + 190} L${x + 34} ${top + 190}" stroke="${C.orange}" stroke-width="5" stroke-linecap="round"/><path d="M${x + 24} ${top + 178} L${x + 36} ${top + 190} L${x + 24} ${top + 202}" fill="none" stroke="${C.orange}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`; }).join('')}
  </svg>
  ${steps.map((s, i) => `<div class="card" style="position:absolute;left:${88 + i * (cw + 44)}px;top:${top}px;width:${cw}px;height:${ch}px;padding:22px 24px;${s.soon ? `border:2.5px dashed ${soonC(dark)}` : i === 0 ? `border:2.5px solid ${C.orange}` : ''}">
    <div style="display:flex;align-items:center;gap:12px">
      <span style="flex:none;width:44px;height:44px;border-radius:50%;${s.soon ? `border:3px dashed ${soonC(dark)};color:${t.fg}` : `background:${C.orange};color:${C.night}`};font:700 22px Poppins;display:flex;align-items:center;justify-content:center;box-sizing:border-box">${s.n}</span>
      <span style="font:700 18px Inter;letter-spacing:.06em;text-transform:uppercase;color:${s.soon ? t.muted : t.accentText}">${s.tag}</span></div>
    <div style="margin:18px 0 0;display:flex;justify-content:center">${miniMap({ ts: 24, tg: 4, dark, hi: s.hi })}</div>
    <div style="font:700 28px/1.15 Poppins;color:${t.fg};margin-top:18px">${s.title}</div>
    <div style="display:inline-block;margin-top:10px;padding:5px 12px;border-radius:999px;background:${s.soon ? t.card2 : tintOf(dark)};font:700 19px Inter;color:${s.soon ? t.muted : t.fg}">${s.billing}</div>
    ${s.items.map((it) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:10px;font:400 20px/1.35 Inter;color:${t.fg}"><span style="flex:none;width:8px;height:8px;border-radius:50%;background:${s.soon ? soonC(dark) : C.orange};margin-top:10px"></span>${it}</div>`).join('')}
  </div>`).join('')}
  <div style="position:absolute;left:88px;top:${top + ch + 24}px;width:1744px;height:112px;border-radius:22px;background:${t.card2};display:flex;align-items:center;gap:22px;padding:0 30px">
    <span style="flex:none;width:60px;height:60px;border-radius:16px;background:${t.card};border:1.5px solid ${t.line};display:flex;align-items:center;justify-content:center">${icon('shield', 32, t.slateMark, 2.2)}</span>
    <div><div style="font:700 27px Poppins;color:${t.fg}">Everywhere else: waitlist only</div><div style="font:400 21px/1.35 Inter;color:${t.muted}">No paid checkout outside South Africa until a provider is live there and checkout is tested.</div></div></div>
  <div style="position:absolute;left:88px;bottom:28px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">Coverage shown is what pawaPay and Fincra contract for; their accounts are pending. Tiles placed roughly by geography.</div>`;
  return frame({ w, h, dark, eyebrow: 'Market entry sequence', title: 'Where we sell, in order', headW: 1300, body });
});

// 19. gauteng-pilot: retired 2026-10-05 (there is no pilot).

// ============ 20. case-study-template ============
{
  const ph = (s, dark, fs) => `<span style="display:inline-block;padding:0 .2em;border-radius:.18em;background:${tintOf(dark)};outline:2px dashed ${dark ? C.glow : '#C24E00'};outline-offset:-2px;color:${dark ? C.glow : '#C24E00'};font-weight:700;${fs ? `font-size:${fs}px;` : ''}line-height:1.15">[[${s}]]</span>`;
  const metrics = [['Qualified leads', '3 in 30 days'], ['Orders via shop link', 'agreed at kickoff'], ['Posts made', 'agreed at kickoff']];
  const setup = (dark) => ['WhatsApp Business number and profile', `Catalogue of ${ph('N', dark)} items, built from product photos`, `Hosted shop link, shared on ${ph('WHERE', dark)}`, 'Order alerts on WhatsApp; reply SOLD to mark it', 'Captions and images for WhatsApp Status (POST)'];
  const challenge = (dark) => [`How customers reach them today: ${ph("OWNER'S WORDS", dark)}`, `What takes the most time: ${ph("OWNER'S WORDS", dark)}`, `How orders are paid today: ${ph('DESCRIBE', dark)}`];
  const stamp = (dark, size) => `<div style="transform:rotate(-7deg);border:${size > 1 ? 4 : 3}px solid ${dark ? C.glow : '#C24E00'};border-radius:16px;padding:${size > 1 ? '12px 22px' : '9px 16px'};color:${dark ? C.glow : '#C24E00'};text-align:center;background:${dark ? 'rgba(15,20,25,.85)' : 'rgba(255,255,255,.9)'}">
    <div style="font:800 ${size > 1 ? 26 : 21}px/1.1 Poppins;letter-spacing:.05em">TEMPLATE · NO DATA YET</div><div style="font:700 ${size > 1 ? 21 : 18}px Inter;margin-top:3px">Consent first</div></div>`;
  variants('case-study-template', ({ dark, w, h }) => {
    const t = T(dark); const sq = w === 1080;
    const bullets = (arr, fs, gap = 10) => arr.map((s) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:${gap}px;font:400 ${fs}px/1.38 Inter;color:${t.fg}"><span style="flex:none;width:8px;height:8px;border-radius:50%;background:${C.orange};margin-top:${Math.round(fs * 0.5)}px"></span><span>${s}</span></div>`).join('');
    const metric = ([k, goal], big, fs) => `<div style="font:800 ${big}px/1 Poppins;color:${t.fg}">${ph(' ', dark)}</div><div style="font:600 ${fs}px/1.25 Inter;color:${t.fg};margin-top:8px">${k}</div><div style="font:500 ${fs - 2}px Inter;color:${t.muted};margin-top:4px">Goal, not a result: <b style="color:${t.fg}">${goal}</b></div>`;
    if (!sq) {
      const body = `
      <div style="position:absolute;left:1440px;top:64px">${stamp(dark, 2)}</div>
      <div style="position:absolute;left:88px;top:306px;width:560px">
        <div style="display:flex;gap:14px">
          <div style="width:180px;height:180px;border-radius:20px;border:2.5px dashed ${soonC(dark)};display:flex;align-items:center;justify-content:center;text-align:center;font:600 18px/1.3 Inter;color:${t.muted}">[[BRAND LOGO]]<br>with consent</div>
          <div style="flex:1;height:180px;border-radius:20px;border:2.5px dashed ${soonC(dark)};background:${t.card2};display:flex;align-items:center;justify-content:center;text-align:center;font:600 18px/1.3 Inter;color:${t.muted}">[[BEFORE / AFTER PHOTO]]<br>with consent</div></div>
        <div class="card" style="margin-top:20px;height:436px;padding:22px 26px">${label(t, 'The challenge', 18)}${bullets(challenge(dark), 21, 14)}
          <div style="font:400 18px/1.35 Inter;color:${t.muted};margin-top:16px">From the onboarding conversation.</div></div></div>
      <div class="card" style="position:absolute;left:676px;top:306px;width:600px;height:636px;padding:22px 26px">
        ${label(t, 'What we set up in week 1', 18)}
        ${setup(dark).map((s, i) => `<div style="display:flex;gap:14px;align-items:flex-start;margin-top:18px"><span style="flex:none;width:36px;height:36px;border-radius:50%;background:${C.orange};color:${C.night};font:700 19px Poppins;display:flex;align-items:center;justify-content:center">${i + 1}</span><span style="font:400 21px/1.4 Inter;color:${t.fg}">${s}</span></div>`).join('')}
        <div style="font:500 19px/1.35 Inter;color:${t.muted};margin-top:20px">Only features that were live for this business.</div></div>
      <div style="position:absolute;left:1304px;top:306px;width:528px">
        ${label(t, 'Measured, period [[FROM–TO]]', 18)}
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:10px">${metrics.map((m) => `<div class="card" style="padding:16px 14px;height:196px">${metric(m, 34, 18)}</div>`).join('')}</div>
        <div class="card" style="margin-top:16px;height:384px;padding:24px 28px;position:relative">
          <div style="font:800 90px/0.7 Poppins;color:${C.orange}">“</div>
          <div style="font:600 28px/1.35 Poppins;color:${t.fg};margin-top:4px">${ph('OWNER QUOTE', dark)}</div>
          <div style="font:500 21px/1.4 Inter;color:${t.muted};margin-top:18px">${ph('OWNER FIRST NAME', dark, 19)}, owner, ${ph('BUSINESS NAME', dark, 19)}</div>
          <div style="position:absolute;left:28px;right:28px;bottom:22px;border-top:1.5px solid ${t.line};padding-top:14px;font:500 19px/1.35 Inter;color:${t.fg}">What we learned: ${ph('INCLUDING WHAT DID NOT WORK', dark, 18)}</div></div></div>
      <div style="position:absolute;left:88px;bottom:28px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">Template only: no case study exists yet. Fill only with measured data and the business’s signed consent. Goals are not results.</div>`;
      return frame({ w, h, dark, eyebrow: 'Case study template · first group of businesses', title: `${ph('BUSINESS NAME', dark)}: ${ph('WHAT CHANGED, MEASURED', dark)}`, sub: `${ph('ARCHETYPE', dark, 24)} in ${ph('AREA', dark, 24)} · ${ph('PLAN', dark, 24)} · ${ph('PERIOD', dark, 24)}`, titleSize: 50, headW: 1320, body });
    }
    const body = `
    <div style="position:absolute;left:790px;top:58px">${stamp(dark, 1)}</div>
    <div class="card" style="position:absolute;left:56px;top:238px;width:470px;height:300px;padding:18px 22px">${label(t, 'The challenge', 16)}${bullets(challenge(dark), 20, 12)}</div>
    <div class="card" style="position:absolute;left:554px;top:238px;width:470px;height:300px;padding:18px 22px">${label(t, 'What we set up', 16)}${bullets([setup(dark)[0], setup(dark)[1], 'Order alerts and Status posts (POST)'], 20, 12)}</div>
    <div style="position:absolute;left:56px;top:564px;width:968px">${label(t, 'Measured, period [[FROM–TO]]', 16)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px">${metrics.map((m) => `<div class="card" style="padding:14px 16px;height:156px">${metric(m, 32, 18)}</div>`).join('')}</div></div>
    <div style="position:absolute;left:56px;top:780px;width:968px;display:flex;gap:14px;align-items:flex-start"><div style="font:800 72px/0.8 Poppins;color:${C.orange}">“</div>
      <div><div style="font:600 25px/1.3 Poppins;color:${t.fg}">${ph('OWNER QUOTE', dark)}</div><div style="font:500 19px Inter;color:${t.muted};margin-top:8px">${ph('OWNER FIRST NAME', dark, 17)}, ${ph('BUSINESS NAME', dark, 17)}</div></div></div>
    <div style="position:absolute;left:56px;top:920px;width:968px;border-top:1.5px solid ${t.line};padding-top:14px;font:500 20px/1.35 Inter;color:${t.fg}">What we learned: ${ph('INCLUDING WHAT DID NOT WORK', dark, 18)}</div>
    <div style="position:absolute;left:56px;bottom:26px;width:700px;font:400 16px/1.35 Inter;color:${t.muted}">Template only. Measured data and signed consent only. Goals are not results.</div>`;
    return frame({ w, h, dark, eyebrow: 'Case study template', title: `${ph('BUSINESS NAME', dark)}: ${ph('WHAT CHANGED', dark)}`, sub: `${ph('ARCHETYPE', dark, 21)}, ${ph('AREA', dark, 21)} · ${ph('PLAN', dark, 21)}`, titleSize: 40, headW: 720, mark: 'br', body });
  }, { square: true });
}

// ============ 21. segment-solo / segment-sme / segment-agency ============
for (const s of SEGMENTS) {
  variants('segment-' + s.key, ({ dark, w, h }) => {
    const t = T(dark);
    const FM = { 149: 104, 289: 202, 499: 349, 1999: 1399, 4999: 3499 }; // Founding Member price points (facts §2), first 2 monthly bills
    const fm = FM[s.price];
    const rh = 140, g = 16, y0 = 456;
    const body = `
    <div style="position:absolute;left:88px;top:262px;width:1744px;padding:6px 0 6px 28px;border-left:8px solid ${C.orange}">
      <div style="font:700 44px/1.2 Poppins;color:${t.fg}">“${s.promise}”</div></div>
    <div style="position:absolute;left:88px;top:${y0 - 44}px;width:560px;display:flex;align-items:center;gap:10px;font:700 20px Inter;letter-spacing:.08em;text-transform:uppercase;color:${t.muted}">${icon('x', 22, t.muted, 3)} Today</div>
    <div style="position:absolute;left:700px;top:${y0 - 44}px;display:flex;align-items:center;gap:10px">${icon('check', 22, C.orange, 3)}${label(t, 'With FluxMuse', 20)}</div>
    ${s.pains.map((p, i) => { const y = y0 + i * (rh + g); return `
      <div style="position:absolute;left:88px;top:${y}px;width:560px;height:${rh}px;border-radius:20px;background:${t.card2};padding:0 26px;display:flex;align-items:center;font:500 24px/1.35 Inter;color:${t.fg}">${p}</div>
      <svg style="position:absolute;left:652px;top:${y + rh / 2 - 20}px" width="44" height="40"><path d="M4 20 H34" stroke="${C.orange}" stroke-width="5" stroke-linecap="round"/><path d="M24 8 L38 20 L24 32" fill="none" stroke="${C.orange}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="card" style="position:absolute;left:700px;top:${y}px;width:680px;height:${rh}px;padding:0 26px;display:flex;align-items:center;gap:18px;border:2px solid ${C.orange}">
        <span style="flex:none;width:44px;height:44px;border-radius:50%;background:${C.orange};display:flex;align-items:center;justify-content:center">${icon('check', 26, C.night, 3)}</span>
        <span style="font:600 24px/1.35 Inter;color:${t.fg}">${s.answers[i]}</span></div>`; }).join('')}
    <div class="card" style="position:absolute;left:1420px;top:${y0}px;width:412px;height:208px;padding:20px 26px">
      ${label(t, 'Main plan', 17)}
      <div style="font:700 28px/1.2 Poppins;color:${t.fg};margin-top:4px">${s.plan}</div>
      <div style="font:800 50px/1.05 Poppins;color:${t.fg}">${R(s.price)}<span style="font:500 22px Inter;color:${t.muted}"> /mo</span></div>
      <div style="font:400 18px/1.35 Inter;color:${t.muted};margin-top:8px">${s.upNote}</div></div>
    ${orangeBand(s.key === 'agency' ? `<div style="display:flex;align-items:center;gap:10px">${icon('layers', 26, C.night, 2.4)}<span style="font:700 18px Inter;letter-spacing:.08em;text-transform:uppercase">Partner price</span></div>
      <div style="font:800 42px/1.1 Poppins;margin-top:10px">R6,999/mo</div><div style="font:700 21px/1.3 Inter">30% off the Agency tier, ongoing</div>
      <div style="font:600 19px/1.35 Inter;margin-top:8px">Wholesale for partner agencies. Set your own retail price and keep the spread.</div>`
      : `<div style="display:flex;align-items:center;gap:10px">${icon('sparkles', 26, C.night, 2.4)}<span style="font:700 18px Inter;letter-spacing:.08em;text-transform:uppercase">Founding Member</span></div>
      <div style="font:800 42px/1.1 Poppins;margin-top:10px">${R(fm)}/mo</div><div style="font:700 21px/1.3 Inter">for your first 2 bills (30% off)</div>
      <div style="font:600 19px/1.35 Inter;margin-top:8px">Then ${R(s.price)}. South African sign-ups, while it lasts.</div>`, `position:absolute;left:1420px;top:${y0 + 224}px;width:412px;height:${3 * rh + 2 * g - 224}px;border-radius:22px;padding:20px 26px`)}
    <div style="position:absolute;left:88px;bottom:30px;width:1400px;font:400 20px/1.4 Inter;color:${t.muted}"><b style="color:${t.fg}">How they buy:</b> ${s.motion}.${s.key === 'agency' ? ' Your spread depends on the retail price you set and your own costs.' : ''}</div>`;
    return frame({ w, h, dark, eyebrow: `Launch segment ${s.n} of 3 · South Africa first`, title: s.name, sub: s.whoShort, headW: 1400, body });
  });
}

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9346 });
