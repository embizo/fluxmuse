// Infographics 15+ (revision v2, founder decisions 2026-09-11) → ../assets/infographics
// pricing-regional, founding-member-offer(+_pilot), target-segments, market-entry-sequence,
// gauteng-pilot, case-study-template, segment-solo/sme/agency. Usage: node build_infographics3.mjs [nameFilter]
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

// ============ 15. pricing-regional ============
{
  const tiers = [
    ['Starter', ['R499', '₦41,000', 'KSh 3,999', 'GH₵ 339', '$27']],
    ['Growth', ['R1,999', '₦165,000', 'KSh 15,999', 'GH₵ 1,359', '$109']],
    ['Scale', ['R4,999', '₦413,000', 'KSh 39,999', 'GH₵ 3,399', '$269']],
    ['Agency', ['R7,999', '₦662,000', 'KSh 64,499', 'GH₵ 5,439', '$429']],
  ];
  const cur = [['South Africa', 'ZAR'], ['Nigeria', 'NGN'], ['Kenya', 'KES'], ['Ghana', 'GHS'], ['19 other rail-covered countries', 'USD']];
  const notes = [['calendar', 'Annual = 10× monthly'], ['globe', 'USD applies in 19 other rail-covered countries'], ['users', 'Other countries: join the waitlist'], ['refresh', 'Prices reviewed quarterly']];
  variants('pricing-regional', ({ dark, w, h }) => {
    const t = T(dark); const sq = w === 1080;
    const L = sq ? { x: 56, tw: 968, tierW: 150, top: 212, hdH: 110, rowH: 126, vf: 25, nf: 17 } : { x: 88, tw: 1744, tierW: 260, top: 250, hdH: 112, rowH: 130, vf: 42, nf: 22 };
    const cw = (L.tw - L.tierW) / 5;
    const header = `<div style="display:flex;height:${L.hdH}px;align-items:flex-end;border-bottom:2px solid ${t.fg};padding-bottom:12px">
      <div style="width:${L.tierW}px;font:700 ${sq ? 18 : 22}px Inter;color:${t.muted}">Plan, per month</div>
      ${cur.map(([c, code], i) => `<div style="width:${cw}px;padding-left:${sq ? 10 : 18}px;${i === 4 ? `border-left:2px dashed ${t.line}` : ''}"><div style="font:700 ${sq ? 28 : 36}px/1 Poppins;color:${t.accentText}">${code}</div><div style="font:500 ${sq ? 16 : 21}px/1.2 Inter;color:${t.fg};margin-top:6px">${sq && i === 4 ? '19 other countries' : c}</div></div>`).join('')}</div>`;
    const rows = tiers.map(([n, ps]) => { const pop = n === 'Growth'; return `<div style="display:flex;height:${L.rowH}px;align-items:center;border-bottom:1.5px solid ${t.line};${pop ? `background:${tintOf(dark)};` : ''}">
      <div style="width:${L.tierW}px;padding-left:${sq ? 10 : 20}px"><div style="font:700 ${sq ? 25 : 34}px Poppins;color:${t.fg}">${n}</div>${pop ? `<div style="font:600 ${sq ? 14 : 18}px Inter;color:${t.accentText}">Most popular</div>` : ''}</div>
      ${ps.map((p, i) => `<div style="width:${cw}px;padding-left:${sq ? 10 : 18}px;align-self:stretch;display:flex;align-items:center;${i === 4 ? `border-left:2px dashed ${t.line}` : ''}"><span style="font:700 ${L.vf}px/1 Poppins;color:${t.fg};white-space:nowrap">${p}</span></div>`).join('')}</div>`; }).join('');
    const chips = `<div style="display:flex;flex-wrap:wrap;gap:${sq ? '10px' : '14px'}">${notes.map(([ic, s]) => `<span style="display:inline-flex;align-items:center;gap:10px;padding:${sq ? '8px 14px' : '10px 18px'};border-radius:999px;background:${t.card2};font:600 ${sq ? 17 : 21}px Inter;color:${t.fg}">${icon(ic, sq ? 20 : 24, C.orange, 2.2)}${s}</span>`).join('')}</div>`;
    const tableH = L.hdH + 4 * L.rowH;
    const body = `<div style="position:absolute;left:${L.x}px;top:${L.top}px;width:${L.tw}px">${header}${rows}</div>
      <div style="position:absolute;left:${L.x}px;top:${L.top + tableH + (sq ? 26 : 34)}px;width:${L.tw}px">${chips}</div>
      <div style="position:absolute;left:${L.x}px;bottom:${sq ? 34 : 34}px;width:${sq ? 700 : 1400}px;font:400 ${sq ? 17 : 20}px/1.4 Inter;color:${t.muted}">Fixed price points at FX parity with ZAR (early Sept 2026 rates); billed in local currency. 14-day free trial, no card required. Enterprise: talk to us.</div>`;
    return frame({ w, h, dark, eyebrow: 'Pricing by market', title: sq ? 'Regional pricing' : 'One set of plans, priced for each market', sub: sq ? 'Monthly price per plan.' : 'Monthly price per plan. Billed in ZAR, NGN, KES or GHS; USD everywhere else we sell.', mark: 'tr', headW: sq ? 740 : 1400, body });
  }, { square: true });
}

// ============ 16. founding-member-offer (+ _pilot) ============
const badge = (size, dark) => `<div style="flex:none;width:${size}px;height:${size}px;border-radius:50%;background:${C.orange};display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 ${Math.round(size / 18)}px ${dark ? 'rgba(255,106,0,.22)' : C.tint}">
  <div style="width:${size - 22}px;height:${size - 22}px;border-radius:50%;border:3px dashed ${C.night};display:flex;flex-direction:column;align-items:center;justify-content:center;color:${C.night};text-align:center">
    ${icon('sparkles', Math.round(size / 3.6), C.night, 2.4)}<div style="font:800 ${Math.round(size / 11)}px/1.05 Poppins;letter-spacing:.04em;margin-top:4px">FOUNDING<br>MEMBER</div></div></div>`;
variants('founding-member-offer', ({ dark, w, h }) => {
  const t = T(dark); const sq = w === 1080;
  if (!sq) {
    const optCard = (x, ic, kicker, big, line1, line2) => `<div class="card" style="position:absolute;left:${x}px;top:262px;width:446px;height:290px;padding:26px 28px">
      <div style="display:flex;align-items:center;gap:12px">${icon(ic, 30, C.orange, 2.2)}${label(t, kicker, 19)}</div>
      <div style="font:800 64px/1 Poppins;color:${t.accentText};margin-top:22px;white-space:nowrap">${big}</div>
      <div style="font:600 26px/1.3 Inter;color:${t.fg};margin-top:12px">${line1}</div>
      <div style="font:400 21px/1.35 Inter;color:${t.muted};margin-top:6px">${line2}</div></div>`;
    const steps = [['1', 'Start the 14-day free trial', 'No card required'], ['2', 'Subscribe in the launch window', '60 days per market'], ['3', 'Save, and get the perks', 'Badge + priority support']];
    const bars = [[1, 1399, true], [2, 1399, true], [3, 1999, false], [4, 1999, false]];
    const maxH = 290, bx = 1150, by = 910;
    const body = `
    ${optCard(88, 'calendar', 'Monthly plans', '30% off', 'your first 2 monthly bills', 'then the list price')}
    ${optCard(560, 'wallet', 'Annual plans', '+2 months', 'free on annual plans', '14 months for the price of 12')}
    <div style="position:absolute;left:88px;top:586px;width:918px;display:flex;gap:16px">${steps.map(([n, a, b]) => `<div style="flex:1;display:flex;gap:12px;align-items:flex-start;padding:16px 16px;border-radius:18px;background:${t.card2}">
      <span style="flex:none;width:38px;height:38px;border-radius:50%;background:${C.orange};color:${C.night};font:700 20px Poppins;display:flex;align-items:center;justify-content:center">${n}</span>
      <div><div style="font:700 21px/1.2 Poppins;color:${t.fg}">${a}</div><div style="font:400 19px/1.3 Inter;color:${t.muted};margin-top:3px">${b}</div></div></div>`).join('')}</div>
    ${orangeBand(`<div style="display:flex;align-items:center;gap:20px">${icon('flag', 40, C.night, 2.4)}<div><div style="font:700 20px Inter;letter-spacing:.08em;text-transform:uppercase">South Africa launch window</div><div style="font:800 40px/1.1 Poppins;margin-top:4px">1 Dec 2026 – 31 Jan 2027</div></div></div>
      <div style="font:600 21px/1.35 Inter;margin-top:10px">Limited 60-day window. On top of the 14-day free trial.</div>`, 'position:absolute;left:88px;top:748px;width:918px;height:196px;border-radius:22px;padding:24px 30px')}
    <div class="card" style="position:absolute;left:1060px;top:262px;width:772px;height:682px;padding:28px 34px">
      <div style="display:flex;align-items:center;gap:28px">${badge(150, dark)}
        <div><div style="font:700 32px/1.15 Poppins;color:${t.fg}">Founding Member badge + priority support</div><div style="font:500 22px/1.35 Inter;color:${t.muted};margin-top:8px">On Starter, Growth and Scale plans. Agencies: see partner pricing.</div></div></div>
      <div style="border-top:1.5px solid ${t.line};margin:28px 0 18px"></div>
      <div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font:700 26px Poppins;color:${t.fg}">Example: Growth plan</div><div style="font:500 20px Inter;color:${t.muted}">list price R1,999/mo</div></div>
    </div>
    <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}">
      <line x1="${bx - 20}" y1="${by}" x2="${bx + 4 * 160}" y2="${by}" stroke="${t.line}" stroke-width="2"/>
    </svg>
    ${bars.map(([m, v, disc], i) => { const bh = Math.round((v / 1999) * maxH); const x = bx + i * 160; return `
      <div style="position:absolute;left:${x}px;top:${by - bh}px;width:118px;height:${bh}px;border-radius:14px 14px 0 0;background:${disc ? C.orange : t.card2};${disc ? '' : `border:2px solid ${t.line};border-bottom:none`}"></div>
      <div style="position:absolute;left:${x - 20}px;top:${by - bh - 44}px;width:158px;text-align:center;font:700 28px Poppins;color:${t.fg}">${R(v)}</div>
      ${disc ? `<div style="position:absolute;left:${x}px;top:${by - bh + 14}px;width:118px;text-align:center;font:700 20px Inter;color:${C.night}">−30%</div>` : ''}
      <div style="position:absolute;left:${x - 20}px;top:${by + 8}px;width:158px;text-align:center;font:500 20px Inter;color:${t.muted}">Month ${m}</div>`; }).join('')}
    <div style="position:absolute;left:88px;bottom:30px;width:1400px;font:400 20px/1.4 Inter;color:${t.muted}">For sign-ups in the first 60 days of a market launch. South Africa prices shown; Nigeria, Kenya and Ghana: first 60 days after each country’s launch.</div>`;
    return frame({ w, h, dark, eyebrow: 'Launch offer · 60 days only', title: 'Become a Founding Member', sub: 'Join in the launch window and pay less while you get set up.', headW: 1300, body });
  }
  // square social post
  const body = `
  <div class="card" style="position:absolute;left:56px;top:200px;width:968px;height:264px;padding:24px 34px">
    <div style="display:flex;align-items:baseline;gap:22px"><span style="font:800 112px/1 Poppins;color:${t.accentText}">30% off</span><span style="font:700 34px/1.2 Poppins;color:${t.fg}">your first 2<br>monthly bills</span></div>
    <div style="font:500 25px/1.35 Inter;color:${t.muted};margin-top:18px">or <b style="color:${t.fg}">+2 months free</b> on annual plans (14 months for the price of 12)</div></div>
  <div style="position:absolute;left:56px;top:500px;width:968px;display:flex;gap:26px;align-items:center">${badge(132, dark)}
    <div><div style="font:700 30px/1.2 Poppins;color:${t.fg}">Founding Member badge + priority support</div><div style="font:500 22px/1.35 Inter;color:${t.muted};margin-top:6px">On Starter, Growth and Scale. Agencies: see partner pricing.</div></div></div>
  <div style="position:absolute;left:56px;top:668px;width:968px;padding:16px 26px;border-radius:18px;background:${t.card2};display:flex;align-items:center;gap:16px">${icon('trend', 30, C.orange, 2.2)}
    <div style="font:500 24px/1.3 Inter;color:${t.fg}">Growth plan: <b>R1,399</b> × 2 months, then R1,999</div></div>
  ${orangeBand(`<div style="font:700 19px Inter;letter-spacing:.08em;text-transform:uppercase">South Africa · limited 60-day window</div><div style="font:800 44px/1.1 Poppins;margin-top:6px">1 Dec 2026 – 31 Jan 2027</div><div style="font:600 22px Inter;margin-top:8px">On top of the 14-day free trial · fluxmuse.ai</div>`, 'position:absolute;left:56px;top:776px;width:968px;height:206px;border-radius:22px;padding:22px 32px')}
  <div style="position:absolute;left:56px;bottom:26px;width:700px;font:400 17px Inter;color:${t.muted}">For sign-ups in the 60-day launch window. No card needed for the trial.</div>`;
  return frame({ w, h, dark, eyebrow: 'Launch offer', title: 'Become a Founding Member', mark: 'tr', headW: 760, body });
}, { square: true });

{
  const build = ({ dark, w, h }) => {
    const t = T(dark);
    // pilot price points (facts §2): 50% off, rounded down to whole rands, first 2 monthly bills from 1 Dec 2026
    const list = [['Starter', 499, 249], ['Growth', 1999, 999], ['Scale', 4999, 2499], ['Agency', 7999, 3999]];
    const tl = [['Sept 2026', 'Pilot starts', false], ['30 Nov 2026', 'Pilot ends', false], ['1 Dec 2026', '50% off starts', true], ['From bill 3', 'Then list price', false]];
    const body = `
    <div class="card" style="position:absolute;left:88px;top:262px;width:540px;height:300px;padding:26px 30px;border:3px solid ${C.orange}">
      ${label(t, 'Your pilot thank-you', 19)}
      <div style="font:800 96px/1 Poppins;color:${t.accentText};margin-top:14px">50% off</div>
      <div style="font:700 30px/1.2 Poppins;color:${t.fg};margin-top:10px">your first 2 monthly bills</div>
      <div style="font:400 21px/1.35 Inter;color:${t.muted};margin-top:6px">From 1 Dec 2026. Founding Member terms, deepened.</div></div>
    <div class="card" style="position:absolute;left:656px;top:262px;width:520px;height:300px;padding:26px 30px">
      ${label(t, 'In exchange for', 19)}
      ${[['file', 'A case study', 'Built from your real pilot results'], ['sparkles', 'Logo permission', 'So we can show your brand in our materials']].map(([ic, a, b]) => `<div style="display:flex;gap:16px;align-items:flex-start;margin-top:22px"><span style="flex:none;width:52px;height:52px;border-radius:14px;background:${tintOf(dark)};display:flex;align-items:center;justify-content:center">${icon(ic, 28, C.orange, 2.2)}</span><div><div style="font:700 26px/1.2 Poppins;color:${t.fg}">${a}</div><div style="font:400 20px/1.35 Inter;color:${t.muted}">${b}</div></div></div>`).join('')}
      <div style="font:500 18px/1.3 Inter;color:${t.muted};margin-top:18px">Nothing is published without your signed consent.</div></div>
    <div class="card" style="position:absolute;left:1204px;top:262px;width:628px;height:516px;padding:26px 30px">
      <div style="display:flex;align-items:center;gap:22px">${badge(118, dark)}<div><div style="font:700 26px/1.2 Poppins;color:${t.fg}">Founding Member badge + priority support</div><div style="font:500 20px/1.35 Inter;color:${t.muted};margin-top:6px">Plus your pilot prices below.</div></div></div>
      <div style="display:flex;font:700 18px Inter;color:${t.muted};margin-top:26px;padding-bottom:8px;border-bottom:2px solid ${t.fg}"><span style="flex:1">Plan</span><span style="width:170px;text-align:right">List /mo</span><span style="width:210px;text-align:right">First 2 bills</span></div>
      ${list.map(([n, v, p]) => `<div style="display:flex;align-items:center;height:56px;border-bottom:1.5px solid ${t.line};font:500 23px Inter;color:${t.fg}"><span style="flex:1;font:700 24px Poppins">${n}</span><span style="width:170px;text-align:right;color:${t.muted}">${R(v)}</span><span style="width:210px;text-align:right;font:700 25px Poppins;color:${t.accentText}">${R(p)}</span></div>`).join('')}</div>
    <div class="card" style="position:absolute;left:88px;top:590px;width:1088px;height:188px;padding:22px 30px">
      ${label(t, 'Who qualifies', 19)}
      <div style="font:600 26px/1.35 Inter;color:${t.fg};margin-top:10px">The 12 brands in the Gauteng pilot (September to 30 November 2026).</div>
      <div style="font:400 21px/1.4 Inter;color:${t.muted};margin-top:6px">You keep using FluxMuse after the pilot, on any plan, with no gap in service.</div></div>
    <div style="position:absolute;left:88px;top:812px;width:1744px;height:150px">
      <svg style="position:absolute;left:0;top:0" width="1744" height="150"><line x1="120" y1="40" x2="1624" y2="40" stroke="${C.orange}" stroke-width="4"/></svg>
      ${tl.map(([d, s, hi], i) => { const x = 120 + i * (1504 / 3); return `<div style="position:absolute;left:${x - 16}px;top:24px;width:32px;height:32px;border-radius:50%;background:${hi ? C.orange : t.bg};border:4px solid ${C.orange}"></div>
        <div style="position:absolute;left:${x - 160}px;top:70px;width:320px;text-align:center"><div style="font:700 25px Poppins;color:${hi ? t.accentText : t.fg}">${d}</div><div style="font:500 21px Inter;color:${t.muted};margin-top:2px">${s}</div></div>`; }).join('')}</div>
    <div style="position:absolute;left:88px;bottom:30px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">Pilot-brand terms only. Everyone else: Founding Member offer (30% off the first 2 monthly bills) in the 1 Dec 2026 – 31 Jan 2027 window.</div>`;
    return frame({ w, h, dark, eyebrow: 'Gauteng pilot brands', title: 'Founding Member, pilot edition', sub: 'Thank you for building FluxMuse with us.', headW: 1300, body });
  };
  add('founding-member-offer_pilot', 1920, 1080, build({ dark: false, w: 1920, h: 1080 }));
  add('founding-member-offer_pilot_dark', 1920, 1080, build({ dark: true, w: 1920, h: 1080 }));
}

// ============ 17. target-segments ============
const SEGMENTS = [
  { key: 'solo', n: 1, name: 'Solo entrepreneurs', ic: 'users', tier: 'Starter R499', up: '→ Growth',
    who: 'Founder-run businesses of 1–5 people: side hustles, beauty and braiding, fashion resellers, home bakers, coaches, informal retailers selling on Instagram, Facebook and WhatsApp',
    whoShort: '1–5 people: beauty & braiding, fashion resellers, home bakers, coaches, informal retailers',
    pain: 'No time or budget for a marketer; posts inconsistently; loses sales in WhatsApp DMs; payment links drop off',
    promise: 'Your AI marketing team for R499/mo, and you sell right inside WhatsApp',
    motion: 'Self-serve: 14-day trial → Founding Member offer',
    pains: ['No time or budget for a marketer, so posts go out inconsistently', 'Sales get lost in busy WhatsApp DMs', 'Buyers drop off when sent to payment links'],
    answers: ['Creator writes posts in isiZulu, Afrikaans, English and more; Publisher schedules them', 'Chatbot and WhatsApp Flows reply to buyers instantly, even after hours', 'Catalog, cart and checkout inside WhatsApp with Yoco, Ozow or Paystack'],
    price: 499, upNote: 'Upgrade to Growth (R1,999) for e-commerce and WhatsApp commerce' },
  { key: 'sme', n: 2, name: 'SMEs', ic: 'briefcase', tier: 'Growth R1,999', up: '→ Scale R4,999',
    who: '5–200 staff: retail, restaurants and franchises, e-commerce brands, clinics, property, auto dealers, education, professional services',
    whoShort: '5–200 staff: retail, restaurants & franchises, e-commerce, clinics, property, auto, education',
    pain: '6+ disconnected tools; agency retainers of R15k+/mo; no attribution from social to sales; WhatsApp handled manually by staff',
    promise: 'Replace the tool stack, sell and get paid in chat, see what drives revenue',
    motion: 'Trial + guided onboarding call; proposal for multi-brand / Scale',
    pains: ['6+ disconnected tools and agency retainers of R15k+/mo', 'WhatsApp handled manually by staff', 'No attribution from social to sales'],
    answers: ['One platform and AI marketing team: social, WhatsApp, email, SMS, CRM and commerce', 'Chatbots, catalog, cart checkout and order updates run inside WhatsApp', 'Analyst agent, cohort analysis and custom reports connect campaigns to orders'],
    price: 1999, upNote: 'Scale (R4,999; Founding Member R3,499): 10 brands, API access' },
  { key: 'agency', n: 3, name: 'Agencies', ic: 'layers', tier: 'Partner R5,599', up: '/mo, 30% off Agency',
    who: 'Marketing, digital and social media agencies and freelancers managing 5–50 SMB clients',
    whoShort: 'Marketing, digital and social media agencies and freelancers managing 5–50 SMB clients',
    pain: 'Margin squeeze; manual reporting; too many tools per client; clients want WhatsApp commerce and AI',
    promise: 'Serve more clients under your brand: set your own retail price and keep the spread',
    motion: 'Partner programme: demo → pilot client → partner wholesale plan, reseller billing',
    pains: ['Margin squeeze on every client retainer', 'Manual reporting and too many tools per client', 'Clients asking for WhatsApp commerce and AI'],
    answers: ['Partner price R5,599/mo: set your own retail price and keep the spread', 'Full white-label, 50 client sub-accounts and reseller billing on one platform', 'Resell AI agents and checkout in WhatsApp under your own brand'],
    price: 7999, upNote: 'Agency tier list price. 50 client sub-accounts, full white-label, reseller billing' },
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
    <div style="position:absolute;left:88px;bottom:32px;width:1400px;font:400 20px/1.4 Inter;color:${t.muted}">Enterprise is not a launch target: inbound deals only in FY1. Agencies buy the Agency tier at the R5,599/mo partner price (30% off R7,999).</div>`;
  return frame({ w, h, dark, eyebrow: 'Who we sell to', title: 'Three launch segments, South Africa first', sub: 'Gauteng pilot, then national, before Nigeria, Kenya and Ghana.', headW: 1400, body });
});

// ============ 18. market-entry-sequence ============
variants('market-entry-sequence', ({ dark, w, h }) => {
  const t = T(dark);
  const rest = COUNTRIES.map((c) => c[0]).filter((iso) => !['ZA', 'NG', 'KE', 'GH'].includes(iso));
  const steps = [
    { n: '1', title: 'South Africa', tag: 'Home market', hi: (iso) => (iso === 'ZA' ? 'on' : 'off'), billing: 'Billed in ZAR',
      items: ['Gauteng pilot: 12 brands, to 30 Nov 2026', 'Then national, from 1 Dec 2026', 'Founding Member offer: 1 Dec 2026 – 31 Jan 2027'] },
    { n: '2', title: 'Nigeria, Kenya, Ghana', tag: 'First expansion wave', hi: (iso) => (['NG', 'KE', 'GH'].includes(iso) ? 'on' : iso === 'ZA' ? 'soft' : 'off'), billing: 'Local currency: NGN, KES, GHS',
      items: ['Paystack, pawaPay and Fincra in all three', 'Founding Member offer for 60 days after each launch'] },
    { n: '3', title: '19 other rail-covered countries', tag: 'Self-serve', hi: (iso) => (rest.includes(iso) ? 'on' : ['ZA', 'NG', 'KE', 'GH'].includes(iso) ? 'soft' : 'off'), billing: 'Billed in USD',
      items: ["Côte d'Ivoire, Rwanda, Uganda, Tanzania, Zambia, francophone West & Central Africa and more", 'No local team until traction justifies one'] },
    { n: '4', title: 'Botswana & Namibia', tag: 'Coming soon', soon: true, hi: (iso, soon) => (soon ? 'soon' : 'off'), billing: 'Waitlist only',
      items: ['Shown in the region picker', 'Opens once a payment rail covers them'] },
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
    <div><div style="font:700 27px Poppins;color:${t.fg}">Everywhere else: waitlist only (gated)</div><div style="font:400 21px/1.35 Inter;color:${t.muted}">No prices or checkout where no payment rail can collect, including all countries outside Africa.</div></div></div>
  <div style="position:absolute;left:88px;bottom:28px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">South Sudan &amp; Zimbabwe (Fincra payouts only) open for sale once subscription collection is confirmed. Tiles placed roughly by geography.</div>`;
  return frame({ w, h, dark, eyebrow: 'Market entry sequence', title: 'Where we sell, in order', headW: 1300, body });
});

// ============ 19. gauteng-pilot ============
variants('gauteng-pilot', ({ dark, w, h }) => {
  const t = T(dark);
  const segs = [
    ['Solo entrepreneurs', 5, C.orange, ['Braiding & hair studio', 'Home baker / cake studio', 'Fashion reseller / thrift', 'Nail & lash technician', 'Personal trainer / wellness coach']],
    ['SMEs', 5, C.teal, ['Restaurant / shisanyama with WhatsApp orders', 'Online fashion or beauty brand', 'Clinic / dental / optometry practice', 'Car wash / auto services', 'Multi-branch retailer or franchise']],
    ['Agencies', 2, C.violet, ['Social media agency (5–20 clients)', 'Freelance digital marketer']],
  ];
  const kpis = [['users', 'Brands onboarded'], ['chat', 'WhatsApp conversations'], ['bag', 'Orders / GMV'], ['pen', 'Content pieces published'], ['clock', 'Time saved per week'], ['trend', 'Conversion uplift'], ['heart', 'NPS']];
  const tl = [['Sept 2026', 'Pilot starts', 'on'], ['30 Nov 2026', 'Pilot ends', 'on'], ['December 2026', 'Results + first conversions', 'hi']];
  const colW = 282, gx = 18;
  const body = `
  <div style="position:absolute;left:88px;top:250px;width:1744px;height:110px">
    <svg style="position:absolute;left:0;top:0" width="1744" height="110"><line x1="220" y1="30" x2="872" y2="30" stroke="${C.orange}" stroke-width="4"/><line x1="872" y1="30" x2="1524" y2="30" stroke="${C.orange}" stroke-width="4" stroke-dasharray="12 9"/></svg>
    <div style="position:absolute;left:420px;top:-6px;font:600 19px Inter;color:${t.muted}">12 brands live in the pilot</div>
    ${tl.map(([d, s, st], i) => { const x = 220 + i * 652; return `<div style="position:absolute;left:${x - 15}px;top:15px;width:30px;height:30px;border-radius:50%;background:${st === 'hi' ? C.orange : t.bg};border:4px solid ${C.orange}"></div>
      <div style="position:absolute;left:${x - 200}px;top:52px;width:400px;text-align:center"><div style="font:700 24px/1.2 Poppins;color:${st === 'hi' ? t.accentText : t.fg}">${d}</div><div style="font:500 20px/1.3 Inter;color:${t.muted}">${s}</div></div>`; }).join('')}
  </div>
  <div style="position:absolute;left:88px;top:392px;width:${3 * colW + 2 * gx}px">
    <div style="display:flex;align-items:baseline;gap:14px"><span style="font:700 26px Poppins;color:${t.fg}">Suggested segment mix</span><span style="font:500 20px Inter;color:${t.muted}">archetypes, no brand names</span></div>
    <div style="display:flex;gap:${gx}px;margin-top:16px">${segs.map(([name, n, col, arch]) => `<div style="width:${colW}px">
      <div style="display:flex;align-items:center;gap:10px;font:700 21px Inter;color:${t.fg};margin-bottom:10px"><span style="font:800 34px Poppins;color:${t.fg}">${n}</span>${name}</div>
      ${arch.map((a, j) => { const lead = j === 0 && n === 5 && col === C.orange; return `<div style="height:${lead ? 88 : 72}px;margin-bottom:10px;border-radius:14px;background:${lead ? tintOf(dark) : t.card};border:${lead ? `2.5px solid ${C.orange}` : `1.5px solid ${t.line}`};border-left:8px solid ${col};padding:8px 14px;display:flex;flex-direction:column;justify-content:center">
        ${lead ? `<div style="font:700 15px Inter;letter-spacing:.06em;text-transform:uppercase;color:${t.accentText}">★ Lead case study</div>` : ''}<div style="font:${lead ? 700 : 500} 19px/1.25 Inter;color:${t.fg}">${a}</div></div>`; }).join('')}</div>`).join('')}</div></div>
  <div class="card" style="position:absolute;left:1030px;top:392px;width:802px;height:318px;padding:22px 28px">
    <div style="font:700 26px Poppins;color:${t.fg}">KPIs we track</div>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:16px">${kpis.map(([ic, k]) => `<span style="display:inline-flex;align-items:center;gap:10px;padding:10px 18px;border-radius:999px;background:${t.card2};font:600 21px Inter;color:${t.fg}">${icon(ic, 24, C.orange, 2.2)}${k}</span>`).join('')}</div>
    <div style="font:400 19px/1.35 Inter;color:${t.muted};margin-top:16px">Measured per brand and aggregated only with data from 8+ brands.</div></div>
  <div class="card" style="position:absolute;left:1030px;top:730px;width:390px;height:236px;padding:22px 24px">
    ${label(t, 'Lead case study', 17)}
    <div style="font:700 25px/1.2 Poppins;color:${t.fg};margin-top:8px">Braiding &amp; hair studio</div>
    <div style="font:400 19px/1.35 Inter;color:${t.muted};margin-top:6px">Solo entrepreneur on Starter (R499). Owner decides alone, already books on WhatsApp, short booking cycles.</div></div>
  ${orangeBand(`${icon('calendar', 36, C.night, 2.4)}<div style="font:700 19px Inter;letter-spacing:.08em;text-transform:uppercase;margin-top:12px">Results</div><div style="font:800 40px/1.1 Poppins">December 2026</div><div style="font:600 19px/1.35 Inter;margin-top:8px">Pilot brands convert on Founding Member terms from 1 Dec 2026.</div>`, 'position:absolute;left:1440px;top:730px;width:392px;height:236px;border-radius:22px;padding:22px 26px')}
  <div style="position:absolute;left:88px;bottom:30px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">Pilot underway: no results yet. Suggested mix from the case-study plan; replace with the real roster. No brand names or logos without signed consent.</div>`;
  return frame({ w, h, dark, eyebrow: 'Gauteng pilot · underway', title: '12 brands, September to 30 November 2026', headW: 1400, body });
});

// ============ 20. case-study-template ============
{
  const ph = (s, dark, fs) => `<span style="display:inline-block;padding:0 .2em;border-radius:.18em;background:${tintOf(dark)};outline:2px dashed ${dark ? C.glow : '#C24E00'};outline-offset:-2px;color:${dark ? C.glow : '#C24E00'};font-weight:700;${fs ? `font-size:${fs}px;` : ''}line-height:1.15">[[${s}]]</span>`;
  const metrics = [['Bookings via WhatsApp', '+30%'], ['Deposits collected in chat', '60% of bookings'], ['No-show rate', '−40%']];
  const setup = (dark) => ['WhatsApp Business number with a booking chatbot: hours, prices, styles menu', `Catalog of ${ph('N', dark)} styles and a deposit link via ${ph('YOCO / OZOW', dark)}`, 'Reminders 24h and 2h before appointments, plus a rebooking nudge', 'Before/after posts and captions in isiZulu, Sesotho and English', 'wa.me short link + QR code for the salon mirror and flyers'];
  const challenge = (dark) => [`Bookings lost in busy WhatsApp DMs: ${ph("OWNER'S WORDS", dark)}`, `No-shows with no deposit: ${ph('N', dark)} per week`, `Payment before the pilot: ${ph('CASH / SCREENSHOTS', dark)}`];
  const stamp = (dark, size) => `<div style="transform:rotate(-7deg);border:${size > 1 ? 4 : 3}px solid ${dark ? C.glow : '#C24E00'};border-radius:16px;padding:${size > 1 ? '12px 22px' : '9px 16px'};color:${dark ? C.glow : '#C24E00'};text-align:center;background:${dark ? 'rgba(15,20,25,.85)' : 'rgba(255,255,255,.9)'}">
    <div style="font:800 ${size > 1 ? 26 : 21}px/1.1 Poppins;letter-spacing:.05em">PILOT DATA PENDING</div><div style="font:700 ${size > 1 ? 21 : 18}px Inter;margin-top:3px">December 2026</div></div>`;
  variants('case-study-template', ({ dark, w, h }) => {
    const t = T(dark); const sq = w === 1080;
    const bullets = (arr, fs, gap = 10) => arr.map((s) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:${gap}px;font:400 ${fs}px/1.38 Inter;color:${t.fg}"><span style="flex:none;width:8px;height:8px;border-radius:50%;background:${C.orange};margin-top:${Math.round(fs * 0.5)}px"></span><span>${s}</span></div>`).join('');
    const metric = ([k, goal], big, fs) => `<div style="font:800 ${big}px/1 Poppins;color:${t.fg}">${ph(' ', dark)}</div><div style="font:600 ${fs}px/1.25 Inter;color:${t.fg};margin-top:8px">${k}</div><div style="font:500 ${fs - 2}px Inter;color:${t.muted};margin-top:4px">Target (goal): <b style="color:${t.fg}">${goal}</b></div>`;
    if (!sq) {
      const body = `
      <div style="position:absolute;left:1440px;top:64px">${stamp(dark, 2)}</div>
      <div style="position:absolute;left:88px;top:306px;width:560px">
        <div style="display:flex;gap:14px">
          <div style="width:180px;height:180px;border-radius:20px;border:2.5px dashed ${soonC(dark)};display:flex;align-items:center;justify-content:center;text-align:center;font:600 18px/1.3 Inter;color:${t.muted}">[[BRAND LOGO]]<br>with consent</div>
          <div style="flex:1;height:180px;border-radius:20px;border:2.5px dashed ${soonC(dark)};background:${t.card2};display:flex;align-items:center;justify-content:center;text-align:center;font:600 18px/1.3 Inter;color:${t.muted}">[[BEFORE / AFTER PHOTO]]<br>with consent</div></div>
        <div class="card" style="margin-top:20px;height:436px;padding:22px 26px">${label(t, 'The challenge', 18)}${bullets(challenge(dark), 21, 14)}
          <div style="font:400 18px/1.35 Inter;color:${t.muted};margin-top:16px">From the onboarding interview.</div></div></div>
      <div class="card" style="position:absolute;left:676px;top:306px;width:600px;height:636px;padding:22px 26px">
        ${label(t, 'What we set up in week 1', 18)}
        ${setup(dark).map((s, i) => `<div style="display:flex;gap:14px;align-items:flex-start;margin-top:18px"><span style="flex:none;width:36px;height:36px;border-radius:50%;background:${C.orange};color:${C.night};font:700 19px Poppins;display:flex;align-items:center;justify-content:center">${i + 1}</span><span style="font:400 21px/1.4 Inter;color:${t.fg}">${s}</span></div>`).join('')}
        <div style="font:500 19px/1.35 Inter;color:${t.muted};margin-top:20px">Channels: WhatsApp Business, Facebook Page, link-in-bio.</div></div>
      <div style="position:absolute;left:1304px;top:306px;width:528px">
        ${label(t, 'Results in 60 days', 18)}
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:10px">${metrics.map((m) => `<div class="card" style="padding:16px 14px;height:196px">${metric(m, 34, 18)}</div>`).join('')}</div>
        <div class="card" style="margin-top:16px;height:384px;padding:24px 28px;position:relative">
          <div style="font:800 90px/0.7 Poppins;color:${C.orange}">“</div>
          <div style="font:600 28px/1.35 Poppins;color:${t.fg};margin-top:4px">${ph('OWNER QUOTE', dark)}</div>
          <div style="font:500 21px/1.4 Inter;color:${t.muted};margin-top:18px">${ph('OWNER FIRST NAME', dark, 19)}, owner, ${ph('BRAND NAME', dark, 19)}</div>
          <div style="position:absolute;left:28px;right:28px;bottom:22px;border-top:1.5px solid ${t.line};padding-top:14px;font:500 19px/1.35 Inter;color:${t.fg}">Next: converting on Founding Member terms from 1 Dec 2026 → ${ph('TIER', dark, 18)}</div></div></div>
      <div style="position:absolute;left:88px;bottom:28px;width:1400px;font:400 19px/1.4 Inter;color:${t.muted}">Template: replace every [[PLACEHOLDER]] with measured pilot data and signed consent (case study + logo). Targets are goals, not results.</div>`;
      return frame({ w, h, dark, eyebrow: 'Case study · Gauteng braiding &amp; hair studio', title: `${ph('BRAND NAME', dark)} turned WhatsApp chats into ${ph('N', dark)} paid bookings in 60 days`, sub: `Braiding &amp; hair studio in ${ph('TOWNSHIP / SUBURB', dark, 24)}, Gauteng · Starter → ${ph('TIER', dark, 24)} · pilot to 30 Nov 2026`, titleSize: 50, headW: 1320, body });
    }
    const body = `
    <div style="position:absolute;left:790px;top:58px">${stamp(dark, 1)}</div>
    <div class="card" style="position:absolute;left:56px;top:238px;width:470px;height:300px;padding:18px 22px">${label(t, 'The challenge', 16)}${bullets(challenge(dark), 20, 12)}</div>
    <div class="card" style="position:absolute;left:554px;top:238px;width:470px;height:300px;padding:18px 22px">${label(t, 'What we set up', 16)}${bullets([setup(dark)[0], setup(dark)[1], 'Reminders + multilingual before/after posts'], 20, 12)}</div>
    <div style="position:absolute;left:56px;top:564px;width:968px">${label(t, 'Results in 60 days', 16)}
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px">${metrics.map((m) => `<div class="card" style="padding:14px 16px;height:156px">${metric(m, 32, 18)}</div>`).join('')}</div></div>
    <div style="position:absolute;left:56px;top:780px;width:968px;display:flex;gap:14px;align-items:flex-start"><div style="font:800 72px/0.8 Poppins;color:${C.orange}">“</div>
      <div><div style="font:600 25px/1.3 Poppins;color:${t.fg}">${ph('OWNER QUOTE', dark)}</div><div style="font:500 19px Inter;color:${t.muted};margin-top:8px">${ph('OWNER FIRST NAME', dark, 17)}, ${ph('BRAND NAME', dark, 17)}</div></div></div>
    <div style="position:absolute;left:56px;top:920px;width:968px;border-top:1.5px solid ${t.line};padding-top:14px;font:500 20px/1.35 Inter;color:${t.fg}">Next: converting on Founding Member terms from 1 Dec 2026 → ${ph('TIER', dark, 18)}</div>
    <div style="position:absolute;left:56px;bottom:26px;width:700px;font:400 16px/1.35 Inter;color:${t.muted}">Template: replace placeholders with measured pilot data and signed consent. Targets are goals, not results.</div>`;
    return frame({ w, h, dark, eyebrow: 'Case study · Gauteng pilot', title: `${ph('BRAND NAME', dark)}: WhatsApp chats into ${ph('N', dark)} paid bookings`, sub: `Braiding &amp; hair studio, ${ph('AREA', dark, 21)}, Gauteng · Starter`, titleSize: 40, headW: 720, mark: 'br', body });
  }, { square: true });
}

// ============ 21. segment-solo / segment-sme / segment-agency ============
for (const s of SEGMENTS) {
  variants('segment-' + s.key, ({ dark, w, h }) => {
    const t = T(dark);
    const FM = { 499: 349, 1999: 1399, 4999: 3499 }; // Founding Member price points (facts §2), first 2 monthly bills
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
      <div style="font:700 28px/1.2 Poppins;color:${t.fg};margin-top:4px">${s.key === 'agency' ? 'Agency' : s.tier.split(' ')[0]}</div>
      <div style="font:800 50px/1.05 Poppins;color:${t.fg}">${R(s.price)}<span style="font:500 22px Inter;color:${t.muted}"> /mo</span></div>
      <div style="font:400 18px/1.35 Inter;color:${t.muted};margin-top:8px">${s.upNote}</div></div>
    ${orangeBand(s.key === 'agency' ? `<div style="display:flex;align-items:center;gap:10px">${icon('layers', 26, C.night, 2.4)}<span style="font:700 18px Inter;letter-spacing:.08em;text-transform:uppercase">Partner price</span></div>
      <div style="font:800 42px/1.1 Poppins;margin-top:10px">R5,599/mo</div><div style="font:700 21px/1.3 Inter">30% off the Agency tier, ongoing</div>
      <div style="font:600 19px/1.35 Inter;margin-top:8px">Wholesale for partner agencies. Set your own retail price and keep the spread.</div>`
      : `<div style="display:flex;align-items:center;gap:10px">${icon('sparkles', 26, C.night, 2.4)}<span style="font:700 18px Inter;letter-spacing:.08em;text-transform:uppercase">Founding Member</span></div>
      <div style="font:800 42px/1.1 Poppins;margin-top:10px">${R(fm)}/mo</div><div style="font:700 21px/1.3 Inter">for your first 2 bills (30% off)</div>
      <div style="font:600 19px/1.35 Inter;margin-top:8px">Then ${R(s.price)}. Limited 60-day launch window, on top of the 14-day free trial.</div>`, `position:absolute;left:1420px;top:${y0 + 224}px;width:412px;height:${3 * rh + 2 * g - 224}px;border-radius:22px;padding:20px 26px`)}
    <div style="position:absolute;left:88px;bottom:30px;width:1400px;font:400 20px/1.4 Inter;color:${t.muted}"><b style="color:${t.fg}">How they buy:</b> ${s.motion}.${s.key === 'agency' ? ' Your spread depends on the retail price you set and your own costs.' : ''}</div>`;
    return frame({ w, h, dark, eyebrow: `Launch segment ${s.n} of 3 · South Africa first`, title: s.name, sub: s.whoShort, headW: 1400, body });
  });
}

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9346 });
