// Infographics 7–14 → ../assets/infographics. Usage: node build_infographics2.mjs [nameFilter]
import { join } from 'node:path';
import { renderJobs, ASSETS } from './lib/page.mjs';
import { frame, markers, T, C, icon } from './lib/ig.mjs';

const OUT = join(ASSETS, 'infographics');
const jobs = [];
const add = (name, w, h, html) => jobs.push({ name, dir: 'infographics', html, w, h, out: join(OUT, name + '.png') });
const ICON = '../../assets/brand/fluxmuse-icon-512.png';

// ============ 7. brand-engagement-journey ============
{
  const stages = [
    ['Discovery call', 'Week 0', 'chat', 'Goals, audience, products and current channels', 'Goals, audience, products'],
    ['Audit & strategy', 'Week 1', 'search', 'Channel and content audit, pilot plan, KPI goals agreed', 'Audit, pilot plan, KPI goals agreed'],
    ['Setup', 'Weeks 1–2', 'zap', 'WhatsApp Business number, catalog, payment rail, content calendar', 'WABA number, catalog, payment rail, calendar'],
    ['Pilot campaign', 'Up to 90 days', 'megaphone', 'AI agents create, publish and sell; weekly check-ins', 'Agents create, publish, sell; weekly check-ins'],
    ['Report & optimise', 'Monthly', 'chart', 'Progress against KPI goals and what to change next', 'Progress vs KPI goals, next changes'],
    ['Convert to a plan', 'After the pilot', 'trend', 'Founding Member terms; add channels, markets and budget', 'Founding Member terms, then scale'],
  ];
  const kpis = [['Conversations', 'chat'], ['Orders & GMV', 'bag'], ['Content published', 'pen'], ['Time saved', 'clock'], ['Conversion uplift', 'trend'], ['NPS', 'heart']];
  const build = ({ w, h }) => {
    const t = T(false); const sq = w === 1080;
    if (!sq) {
      const cw = 272, g = 22, y = 330;
      const body = `
      <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}"><line x1="${88 + cw / 2}" y1="${y}" x2="${88 + 5 * (cw + g) + cw / 2}" y2="${y}" stroke="${C.orange}" stroke-width="4"/></svg>
      ${stages.map(([n, wk, ic, d], i) => { const x = 88 + i * (cw + g); const hi = i === 3; return `
        <div class="chip" style="position:absolute;left:${x + cw / 2}px;top:${y - 58}px;transform:translateX(-50%);${hi ? `background:${C.orange};color:${C.night}` : ''}">${wk}</div>
        <div style="position:absolute;left:${x + cw / 2 - 24}px;top:${y - 24}px;width:48px;height:48px;border-radius:50%;background:${hi ? C.orange : '#fff'};border:4px solid ${C.orange};font:700 22px Poppins;color:${hi ? C.night : C.ink};display:flex;align-items:center;justify-content:center">${i + 1}</div>
        <div class="card" style="position:absolute;left:${x}px;top:${y + 50}px;width:${cw}px;height:300px;padding:22px 20px;${hi ? `border:2.5px solid ${C.orange};background:${C.tint}` : ''}">
          ${icon(ic, 34, C.orange, 2.2)}
          <div style="font:700 27px/1.15 Poppins;color:${t.fg};margin-top:12px">${n}</div>
          <div style="font:400 22px/1.38 Inter;color:${t.muted};margin-top:8px">${d}</div></div>`; }).join('')}
      <div style="position:absolute;left:88px;top:772px;font:700 26px Poppins;color:${t.fg}">KPIs we track from day one</div>
      <div style="position:absolute;left:88px;top:820px;display:flex;gap:16px">${kpis.map(([k, ic]) => `<div style="display:flex;align-items:center;gap:12px;padding:14px 22px;border-radius:999px;background:${C.mist};font:600 24px Inter;color:${t.fg}">${icon(ic, 28, C.orange, 2.2)}${k}</div>`).join('')}</div>
      <div style="position:absolute;left:88px;bottom:34px;width:1500px;font:400 21px/1.4 Inter;color:${t.muted}">Typical timings. KPI targets are goals agreed with each brand at kickoff, not promised results. Gauteng pilot: runs to 30 Nov 2026; pilot brands convert on Founding Member terms from 1 Dec 2026.</div>`;
      return frame({ w, h, eyebrow: 'Working with FluxMuse', title: 'From first call to scaled campaign', body });
    }
    const y0 = 196, rh = 92, g = 8;
    const body = `
    <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}"><line x1="222" y1="${y0 + rh / 2}" x2="222" y2="${y0 + 5 * (rh + g) + rh / 2}" stroke="${C.orange}" stroke-width="4"/></svg>
    ${stages.map(([n, wk, ic, d, ds], i) => { const y = y0 + i * (rh + g); const hi = i === 3; return `
      <div style="position:absolute;left:56px;top:${y + rh / 2 - 16}px;width:136px;text-align:right;font:600 20px Inter;color:${hi ? '#C24E00' : t.muted}">${wk}</div>
      <div style="position:absolute;left:200px;top:${y + rh / 2 - 22}px;width:44px;height:44px;border-radius:50%;background:${hi ? C.orange : '#fff'};border:4px solid ${C.orange};font:700 20px Poppins;color:${hi ? C.night : C.ink};display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div class="card" style="position:absolute;left:268px;top:${y}px;width:756px;height:${rh}px;padding:14px 20px;display:flex;align-items:center;gap:16px;${hi ? `border:2.5px solid ${C.orange};background:${C.tint}` : ''}">
        ${icon(ic, 32, C.orange, 2.2)}<div><div style="font:700 24px/1.15 Poppins;color:${t.fg}">${n}</div><div style="font:400 20px/1.3 Inter;color:${t.muted}">${ds}</div></div></div>`; }).join('')}
    <div style="position:absolute;left:56px;top:${y0 + 6 * (rh + g) + 8}px;font:700 23px Poppins;color:${t.fg}">KPIs we track</div>
    <div style="position:absolute;left:56px;right:56px;top:${y0 + 6 * (rh + g) + 48}px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px">${kpis.map(([k, ic]) => `<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:999px;background:${C.mist};font:600 20px Inter;color:${t.fg};white-space:nowrap">${icon(ic, 22, C.orange, 2.2)}${k}</div>`).join('')}</div>
    <div style="position:absolute;left:56px;right:56px;top:${y0 + 6 * (rh + g) + 172}px;font:400 18px/1.35 Inter;color:${t.muted}">KPI targets are goals agreed at kickoff, not promised results. Gauteng pilot runs to 30 Nov 2026; brands convert on Founding Member terms from 1 Dec 2026.</div>`;
    return frame({ w, h, eyebrow: 'Working with FluxMuse', title: 'First call to scaled campaign', mark: 'tr', headW: 760, body });
  };
  add('brand-engagement-journey', 1920, 1080, build({ w: 1920, h: 1080 }));
  add('brand-engagement-journey_square', 1080, 1080, build({ w: 1080, h: 1080 }));
}

// ============ 8. pilot-campaign-framework ============
{
  const t = T(false);
  const phases = [
    ['Days 1–30', 'Launch & baseline', '#FFE9D6', [
      ['Objectives', ['Go live on WhatsApp plus one social channel', 'Measure a clean baseline']],
      ['Deliverables', ['WhatsApp Business number and catalog live', 'Payment rail connected', '30-day content calendar', 'Chatbot / FAQ flow', 'Baseline report']],
      ['Metrics tracked', ['Conversations started', 'Catalog views and first orders', 'Content published on schedule']]]],
    ['Days 31–60', 'Optimise conversion', '#FFC08F', [
      ['Objectives', ['Lift chat-to-order conversion', 'Test offers, messages and audiences']],
      ['Deliverables', ['A/B tests on messages and offers', 'Abandoned-cart recovery switched on', 'Segments and broadcast templates', 'Mid-pilot report']],
      ['Metrics tracked', ['Chat-to-order conversion', 'Recovered carts', 'Cost per conversation', 'Response time']]]],
    ['Days 61–90', 'Scale what works', '#FF9442', [
      ['Objectives', ['Double down on winning channels', 'Choose a plan on Founding Member terms']],
      ['Deliverables', ['Add channels: email, SMS or USSD', 'Loyalty programme', 'End-of-pilot report and case study', 'Plan and budget from 1 Dec 2026']],
      ['Metrics tracked', ['Orders and GMV', 'Conversion uplift', 'Repeat purchases', 'Hours saved per week', 'NPS']]]],
  ];
  const cw = (1744 - 2 * 32) / 3;
  const body = phases.map(([d, name, col, secs], i) => `<div class="card" style="position:absolute;left:${88 + i * (cw + 32)}px;top:256px;width:${cw}px;height:690px;overflow:hidden">
    <div style="background:${col};padding:18px 28px"><div style="font:700 22px Inter;letter-spacing:.08em;text-transform:uppercase;color:${C.ink}">${d}</div><div style="font:700 34px Poppins;color:${C.ink};margin-top:2px">${name}</div></div>
    <div style="padding:10px 28px">${secs.map(([s, items]) => `<div style="margin-top:14px"><div style="font:700 21px Inter;letter-spacing:.06em;text-transform:uppercase;color:#C24E00">${s}</div>
      ${items.map((it) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:7px;font:400 22px/1.3 Inter;color:${t.fg}"><span style="flex:none;width:8px;height:8px;border-radius:50%;background:${C.orange};margin-top:11px"></span>${it}</div>`).join('')}</div>`).join('')}</div></div>`).join('')
    + `<div style="position:absolute;left:88px;bottom:30px;width:1744px;font:400 21px/1.4 Inter;color:${t.muted}">Any target for a metric is a goal agreed with the brand at kickoff, not a promised result. Pilot brands convert on Founding Member terms (50% off for 60 days from 1 Dec 2026) in exchange for a case study and logo permission. Results: December 2026.</div>`;
  add('pilot-campaign-framework', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Pilot campaign', title: 'The 30 / 60 / 90-day pilot', sub: 'Gauteng pilot: 12 brands, September to 30 November 2026.', body, mark: 'tr' }));
}

// ============ 9. pricing-tiers ============
{
  const t = T(false);
  const tiers = [
    ['Starter', 'Solo entrepreneurs', 499, 4990, '1', '3', '5,000', ['Community support']],
    ['Growth', 'SMEs selling on social & WhatsApp', 1999, 19990, '3', '15', '25,000', ['E-commerce & WhatsApp commerce', 'USSD', 'Integrations', 'Email support']],
    ['Scale', 'Multi-brand & multi-location SMEs', 4999, 49990, '10', '40', '100,000', ['API access', 'White-label reports', 'Priority support']],
    ['Agency', 'Agencies & resellers', 7999, 79990, 'Unlimited', '80', '500,000', ['Full white-label', '50 sub-accounts', 'Reseller billing', 'Dedicated support']],
  ];
  const cw = (1744 - 3 * 28) / 4;
  const R = (n) => 'R' + n.toLocaleString('en-US');
  const ribbon = `<div style="position:absolute;left:88px;top:238px;width:1744px;height:74px;border-radius:18px;background:${C.orange};display:flex;align-items:center;gap:18px;padding:0 28px;color:${C.night}">
    <span style="flex:none;width:44px;height:44px;border-radius:50%;background:${C.night};display:flex;align-items:center;justify-content:center">${icon('sparkles', 26, C.orange, 2.4)}</span>
    <span style="font:700 28px Poppins">Founding Member:</span><span style="font:600 26px Inter">30% off your first 2 months on Starter, Growth &amp; Scale · annual: +2 months free · 60-day window</span></div>`;
  const body = ribbon + tiers.map(([n, aud, m, a, br, ch, cr, hl], i) => { const pop = n === 'Growth'; return `<div class="card" style="position:absolute;left:${88 + i * (cw + 28)}px;top:350px;width:${cw}px;height:590px;padding:28px 28px;${pop ? `border:3px solid ${C.orange};` : ''}">
    ${pop ? `<div class="chip" style="position:absolute;top:-20px;left:28px;background:${C.orange};color:${C.night}">Most popular</div>` : ''}
    <div style="font:700 34px Poppins;color:${t.fg}">${n}</div><div style="font:400 21px/1.25 Inter;color:${t.muted};height:30px">${aud}</div>
    <div style="font:700 60px/1.05 Poppins;color:${t.fg};margin-top:18px">${R(m)}<span style="font:500 24px Inter;color:${t.muted}"> /mo</span></div>
    <div style="font:400 21px Inter;color:${t.muted};margin-top:6px">or ${R(a)}/yr (2 months free)</div>
    <div style="border-top:1.5px solid ${t.line};margin:20px 0 12px"></div>
    ${[['Brands', br], ['Channels', ch], ['AI credits/mo', cr]].map(([k, v]) => `<div style="display:flex;justify-content:space-between;font:400 22px/1.85 Inter;color:${t.muted}"><span>${k}</span><b style="color:${t.fg};font-weight:700">${v}</b></div>`).join('')}
    <div style="border-top:1.5px solid ${t.line};margin:12px 0 4px"></div>
    ${hl.map((x) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:10px;font:400 22px/1.3 Inter;color:${t.fg}">${icon('check', 22, C.orange, 3)}<span>${x}</span></div>`).join('')}
  </div>`; }).join('') + `<div style="position:absolute;left:88px;top:968px;width:1744px;font:400 21px/1.45 Inter;color:${t.muted}"><b style="color:${t.fg}">Enterprise: talk to us.</b> <b style="color:${t.fg}">Agency partners: R5,599/mo wholesale.</b> Prices for South Africa. Annual = 10× monthly. Nigeria, Kenya and Ghana are billed in local currency; 19 other rail-covered countries in USD (see regional pricing).</div>`;
  add('pricing-tiers', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Pricing', title: 'Four plans, priced in ZAR', sub: '14-day free trial, no card required.', body, mark: 'tr' }));
}

// ============ 10. roadmap-2026-2027 (file name kept; horizon now 2026–2028) ============
{
  const build = (dark) => {
  const t = T(dark);
  // columns (non-linear time axis)
  const cols = [['Sept 2026', 200], ['Oct – Nov 2026', 155], ['Dec 2026 – Jan 2027', 250], ['2027', 345], ['2028', 300], ['Coming soon', 222]];
  const X0 = 360; const cx = []; { let x = X0; cols.forEach(([, wd]) => { cx.push(x); x += wd; }); cx.push(x); }
  const laneY = [[318, 604], [634, 948]];
  const box = (x, y, wd, ht, inner, { hl = false, dashed = false, tint = false } = {}) => `<div style="position:absolute;left:${x}px;top:${y}px;width:${wd}px;height:${ht}px;border-radius:18px;padding:14px 18px;background:${tint ? t.chipBg : t.card};border:${dashed ? `2.5px dashed ${t.ring}` : hl ? `2.5px solid ${C.orange}` : `1.5px solid ${t.line}`};overflow:hidden">${inner}</div>`;
  const h3 = (s, fs = 24) => `<div style="font:700 ${fs}px/1.18 Poppins;color:${t.fg}">${s}</div>`;
  const p = (s, fs = 19) => `<div style="font:400 ${fs}px/1.3 Inter;color:${t.muted};margin-top:5px">${s}</div>`;
  const num = (n) => `<span style="display:inline-flex;width:34px;height:34px;border-radius:50%;background:${C.orange};color:${C.night};font:700 19px Poppins;align-items:center;justify-content:center;margin-right:10px;flex:none">${n}</span>`;
  const check = `<span style="display:inline-flex;width:34px;height:34px;border-radius:50%;background:${C.orange};align-items:center;justify-content:center;margin-bottom:8px">${icon('check', 22, C.night, 3.2)}</span>`;
  const pad = 8;
  // 2028 wave: milestone-gated launch months from the financial model (v2, base case)
  const wave = [['Nigeria', 'NGN', 'Feb 2028'], ['Kenya', 'KES', 'Apr 2028'], ['Ghana', 'GHS', 'Jun 2028']];
  const waveRow = (name, cur, when) => `<div style="display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-top:9px">
    <span style="font:700 21px/1.15 Poppins;color:${t.fg}">${name} <span style="font:500 16px Inter;color:${t.muted}">${cur}</span></span>
    <span style="font:700 19px Inter;color:${t.accentText};white-space:nowrap">${when}</span></div>`;
  const body = `
  <div style="position:absolute;left:${X0}px;top:236px;display:flex">${cols.map(([c, wd], i) => `<div style="width:${wd}px;text-align:center;font:700 ${i === 1 ? 19 : i === 2 ? 20 : 23}px Poppins;white-space:nowrap;color:${i === 5 ? t.muted : t.fg}">${c}</div>`).join('')}</div>
  <svg style="position:absolute;left:0;top:0" width="1920" height="1080">
    <line x1="${X0}" y1="286" x2="${cx[6]}" y2="286" stroke="${C.orange}" stroke-width="4"/>
    ${cx.map((x) => `<line x1="${x}" y1="296" x2="${x}" y2="978" stroke="${t.line}" stroke-width="2"/>`).join('')}
    ${cols.map((_, i) => `<circle cx="${(cx[i] + cx[i + 1]) / 2}" cy="286" r="9" fill="${i === 5 ? t.bg : C.orange}" stroke="${i === 5 ? t.ring : C.orange}" stroke-width="3" ${i === 5 ? 'stroke-dasharray="4 3"' : ''}/>`).join('')}
    <line x1="88" y1="619" x2="1832" y2="619" stroke="${t.line}" stroke-width="2" stroke-dasharray="8 6"/>
  </svg>
  <div style="position:absolute;left:88px;top:${laneY[0][0] + 6}px;width:250px">${icon('globe', 34, C.orange, 2.2)}<div style="font:700 26px/1.15 Poppins;color:${t.fg};margin-top:10px">Markets &amp; payments</div><div style="font:400 19px/1.3 Inter;color:${t.muted};margin-top:6px">Market entry order agreed Sept 2026</div></div>
  <div style="position:absolute;left:88px;top:${laneY[1][0] + 6}px;width:250px">${icon('layers', 34, C.orange, 2.2)}<div style="font:700 26px/1.15 Poppins;color:${t.fg};margin-top:10px">Product</div><div style="font:400 19px/1.3 Inter;color:${t.muted};margin-top:6px">Stages 1–4 in the founder’s agreed order</div></div>

  ${box(cx[0] + pad, 318, cols[0][1] - 2 * pad, 150, `${check}${h3('pawaPay &amp; Fincra live', 20)}${p('All 5 rails', 18)}`, { hl: true })}
  ${box(cx[0] + pad, 482, cx[2] - cx[0] - 2 * pad, 122, `${h3('Gauteng pilot · 12 brands', 22)}${p('September to 30 November 2026', 18)}`, { tint: true, hl: true })}
  ${box(cx[2] + pad, 318, cols[2][1] - 2 * pad, 286, `${icon('flag', 30, C.orange, 2.2)}<div style="margin-top:8px">${h3('South Africa launch')}</div>${p('National, with the Founding Member offer')}<div style="font:600 19px/1.3 Inter;color:${t.accentText};margin-top:10px">1 Dec 2026 – 31 Jan 2027</div>`, { hl: true })}
  ${box(cx[3] + pad, 318, cols[3][1] - 2 * pad, 286, `${h3('Scale South Africa', 22)}${p('No new market launches: each next launch waits on its MRR milestone in the financial model', 18)}`, { dashed: true })}
  ${box(cx[4] + pad, 318, cols[4][1] - 2 * pad, 286, `${h3('Wave 1 · local currency', 21)}${wave.map(([n, c2, w2]) => waveRow(n, c2, w2)).join('')}
    <div style="border-top:1.5px solid ${t.line};margin:14px 0 0"></div>
    <div style="font:700 20px/1.2 Poppins;color:${t.fg};margin-top:12px">Rest of rail-covered Africa <span style="font:700 19px Inter;color:${t.accentText}">· Nov 2028</span></div>
    <div style="font:400 18px/1.25 Inter;color:${t.muted};margin-top:4px">19 countries, USD, self-serve</div>`)}
  ${box(cx[5] + pad, 318, cols[5][1] - 2 * pad, 286, `${h3('Botswana &amp; Namibia', 22)}${p('Coming soon, once a payment rail covers them', 18)}`, { dashed: true })}

  ${box(cx[1] + pad, 634, cx[3] - cx[1] - 2 * pad - 20, 150, `<div style="display:flex;align-items:center">${num(1)}${h3('Meta permissions · Q4 2026')}</div>${p('Instagram, Pages posting, business_management, ads')}`, { tint: true, hl: true })}
  ${[[2, 'Social adapters', 'Instagram Login, Threads, LinkedIn, X, TikTok, YouTube, Pinterest'], [3, 'Business app integrations', 'Commerce, CRM, accounting, email/SMS providers'], [4, 'Flux_Partner programme', 'Referral tracking, white-label, partner-managed workspaces']].map(([n, a, b], i) =>
    box(cx[3] + pad, 634 + i * 114, cx[6] - cx[3] - 2 * pad, 106, `<div style="display:flex;align-items:center">${num(n)}${h3(a, 22)}</div><div style="font:400 18px/1.25 Inter;color:${t.muted};margin-top:6px">${b}</div>`)).join('')}
  <div style="position:absolute;left:88px;bottom:30px;width:1744px;font:400 20px/1.4 Inter;color:${t.muted}">Indicative timeline, not commitments. <b style="color:${t.fg};font-weight:600">Market launch months are milestone-gated in the financial model (v2, base case); dates move with actual revenue.</b> Product timing depends on Meta approvals and team capacity. Everywhere without a payment rail stays waitlist-only. Instagram, TikTok and LinkedIn publishing are not live today.</div>`;
  return frame({ w: 1920, h: 1080, dark, eyebrow: 'Roadmap · indicative', title: 'Roadmap 2026–2028', body, mark: 'tr' });
  };
  add('roadmap-2026-2027', 1920, 1080, build(false));
  add('roadmap-2026-2027_dark', 1920, 1080, build(true));
}

// ============ 11. omnichannel-hub ============
{
  const t = T(false);
  const nodes = [['WhatsApp', 'chat', true], ['Facebook Pages', 'globe', true], ['Instagram', 'sparkles', false], ['Messenger', 'send', true], ['Email', 'mail', true], ['SMS', 'phone', true], ['USSD', 'phone', true], ['Website chat widget', 'chat', true], ['Link-in-bio', 'link', true], ['Landing pages', 'file', true]];
  const cx = 960, cy = 618, rx = 650, ry = 300, nw = 280, nh = 78;
  const pos = nodes.map((_, i) => { const th = ((-90 + i * 36) * Math.PI) / 180; return [cx + rx * Math.cos(th), cy + ry * Math.sin(th)]; });
  const body = `
  <svg style="position:absolute;left:0;top:0" width="1920" height="1080">
    ${pos.map(([x, y], i) => `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${nodes[i][2] ? C.orange : '#9AA5B1'}" stroke-width="3" ${nodes[i][2] ? '' : 'stroke-dasharray="10 8"'}/>`).join('')}
  </svg>
  <div style="position:absolute;left:${cx - 140}px;top:${cy - 140}px;width:280px;height:280px;border-radius:50%;background:#fff;border:3px solid ${C.orange};box-shadow:0 0 0 18px ${C.tint};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <img src="${ICON}" style="width:120px"><div style="font:700 24px/1.2 Poppins;color:${t.fg};margin-top:6px">FluxMuse<br>AI team</div></div>
  ${pos.map(([x, y], i) => { const [n, ic, live] = nodes[i]; return `<div class="card" style="position:absolute;left:${x - nw / 2}px;top:${y - nh / 2}px;width:${nw}px;height:${nh}px;display:flex;align-items:center;gap:14px;padding:0 20px;${live ? '' : `border:2px dashed #9AA5B1`}">
    <span style="flex:none;width:44px;height:44px;border-radius:12px;background:${live ? C.tint : C.mist};display:flex;align-items:center;justify-content:center">${icon(ic, 26, live ? C.orange : '#5B6570', 2.2)}</span>
    <span style="font:600 23px/1.15 Inter;color:${t.fg}">${n}${live ? '' : '<br><span style="font:500 18px Inter;color:#5B6570">in Meta review</span>'}</span></div>`; }).join('')}
  <div style="position:absolute;left:88px;bottom:36px;display:flex;align-items:center;gap:28px;font:500 21px Inter;color:${t.muted}">
    <span style="display:flex;align-items:center;gap:10px"><svg width="46" height="6"><line x1="0" y1="3" x2="46" y2="3" stroke="${C.orange}" stroke-width="4"/></svg>live</span>
    <span style="display:flex;align-items:center;gap:10px"><svg width="46" height="6"><line x1="0" y1="3" x2="46" y2="3" stroke="#9AA5B1" stroke-width="4" stroke-dasharray="10 7"/></svg>in Meta App Review, not live yet</span></div>`;
  add('omnichannel-hub', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Channels', title: 'Every channel your buyers use, one AI team', body, mark: 'tr' }));
}

// ============ 12. problem-solution ============
{
  const t = T(false);
  const today = ['A stack of disconnected tools for posts, chats, email, SMS and payments', 'Agency retainers priced beyond most small-business budgets', 'Buyers drop off when sent to external payment links', 'Checkout that doesn’t offer local ways to pay, like EFT or mobile money'];
  const fm = ['One AI marketing team: Strategist, Creator, Publisher, Analyst', 'Plans from R499/mo, 14-day free trial, no card required', 'Catalog, cart and checkout inside WhatsApp', '5 local payment rails: cards, instant EFT, mobile money, bank transfer'];
  const col = (x, title, items, good) => `<div style="position:absolute;left:${x}px;top:250px;width:790px;height:640px;border-radius:24px;padding:36px 40px;background:${good ? '#fff' : C.mist};border:${good ? `3px solid ${C.orange}` : 'none'}">
    <div style="display:flex;align-items:center;gap:14px">${good ? `<img src="${ICON}" style="height:54px">` : icon('clock', 44, '#5B6570', 2.2)}<span style="font:700 40px Poppins;color:${t.fg}">${title}</span></div>
    ${items.map((s) => `<div style="display:flex;gap:18px;align-items:flex-start;margin-top:34px">
      <span style="flex:none;width:46px;height:46px;border-radius:50%;background:${good ? C.orange : '#DDE1E6'};display:flex;align-items:center;justify-content:center">${icon(good ? 'check' : 'x', 26, good ? C.night : '#5B6570', 3)}</span>
      <span style="font:${good ? 600 : 400} 28px/1.35 Inter;color:${good ? t.fg : '#3E4751'}">${s}</span></div>`).join('')}</div>`;
  const body = col(88, 'Today', today, false) + col(1042, 'With FluxMuse', fm, true) +
    `<div style="position:absolute;left:${88 + 790 + 10}px;top:522px;width:144px;height:96px;display:flex;align-items:center;justify-content:center"><svg width="120" height="60"><line x1="6" y1="30" x2="92" y2="30" stroke="${C.orange}" stroke-width="7" stroke-linecap="round"/><path d="M86 10 L116 30 L86 50z" fill="${C.orange}"/></svg></div>`;
  add('problem-solution', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'The problem we solve', title: 'Marketing and selling, without the patchwork', body, mark: 'tr' }));
}

// ============ 13. why-africa-why-now ============
{
  const t = T(false);
  const stats = [
    ['~44M', 'MSMEs in Sub-Saharan Africa', 'IFC / World Bank est.'],
    ['~2.5–3M', 'SMMEs in South Africa', 'SEDA / Stats SA est.'],
    ['~39M', 'MSMEs in Nigeria', 'SMEDAN est.'],
    ['~7.4M', 'MSMEs in Kenya', 'KNBS est.'],
    ['>90%', 'of internet users in SA and Nigeria use WhatsApp', 'DataReportal 2025 est.'],
    ['~70%', 'of global mobile money value is in Sub-Saharan Africa (>US$1 trillion a year)', 'GSMA State of the Industry 2025 est.'],
  ];
  const cw = (1744 - 2 * 24) / 3;
  const body = stats.map(([n, l, src], i) => `<div class="card" style="position:absolute;left:${88 + (i % 3) * (cw + 24)}px;top:${222 + Math.floor(i / 3) * 250}px;width:${cw}px;height:230px;padding:24px 28px;display:flex;flex-direction:column">
      <div style="font:700 60px/1 Poppins;color:${C.orange}">${n}</div>
      <div style="font:500 25px/1.3 Inter;color:${t.fg};margin-top:10px">${l}</div>
      <div style="margin-top:auto;font:400 19px Inter;color:${t.muted}">Source: ${src}</div></div>`).join('') + `
    <div style="position:absolute;left:88px;top:740px;width:1744px;height:230px;border-radius:24px;background:${C.mist};padding:22px 30px">
      <div style="display:flex;align-items:center;gap:14px"><span style="font:700 26px Poppins;color:${t.fg}">Market we size for</span><span class="chip" style="background:#FFF6D1;color:#6B4E00">planning assumption</span></div>
      <div style="display:flex;align-items:stretch;gap:18px;margin-top:16px">
        ${[['TAM', '44M', 'SSA MSMEs'], ['SAM', '~3.5M', 'digitally active SMBs in the 23 rail-covered countries that sell via social/WhatsApp and can pay ≥US$25/mo'], ['SOM (5-yr)', '~17,500', 'paying workspaces, about 0.5% of SAM']].map(([k, v, d], i) => `${i ? `<div style="display:flex;align-items:center"><svg width="26" height="40"><path d="M6 6 L20 20 L6 34" fill="none" stroke="${C.orange}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>` : ''}<div style="flex:${i === 1 ? 1.6 : 1};background:#fff;border-radius:16px;padding:12px 20px"><div style="font:700 20px Inter;letter-spacing:.08em;color:#C24E00">${k}</div><div style="font:700 36px/1.1 Poppins;color:${t.fg}">${v}</div><div style="font:400 19px/1.3 Inter;color:${t.muted}">${d}</div></div>`).join('')}
      </div></div>
    <div style="position:absolute;left:88px;bottom:30px;font:400 20px Inter;color:${t.muted}">Directional estimates; verify each source before external use.</div>`;
  add('why-africa-why-now', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Why Africa, why now', title: 'Millions of SMBs sell and pay on mobile', body, mark: 'tr', headW: 1520 }));
}

// ============ 14. ai-agent-roster ============
{
  const t = T(false);
  const core = [
    ['Strategist', 'target', ['Goal decomposition', 'Budget allocation', 'ROI forecasting']],
    ['Creator', 'pen', ['Multilingual copy: Zulu, Pidgin, Swahili, Afrikaans, English +', 'Image generation']],
    ['Publisher', 'send', ['Scheduling', 'WhatsApp catalog and checkout flows']],
    ['Analyst', 'chart', ['RAG memory', 'Cohort analysis', 'Auto-optimisation']],
  ];
  const groups = [
    ['Marketing & content', C.violet, ['Content', 'Create', 'Design', 'Ads', 'Growth', 'Discover', 'Community']],
    ['Sales & service', C.teal, ['Nurture', 'Sales', 'Support', 'Commerce', 'Onboarding', 'Personal']],
    ['Business & operations', C.blue, ['Insights', 'Advisor', 'Finance', 'Compliance', 'Ops', 'DevOps', 'Integrate', 'Product', 'Partner', 'Agentic']],
  ];
  const cw = (1744 - 3 * 24) / 4;
  const body = core.map(([n, ic, roles], i) => `<div class="card" style="position:absolute;left:${88 + i * (cw + 24)}px;top:222px;width:${cw}px;height:320px;padding:26px 26px;border-top:6px solid ${C.orange}">
    <div style="display:flex;align-items:center;gap:14px"><span style="width:56px;height:56px;border-radius:16px;background:${C.tint};display:flex;align-items:center;justify-content:center">${icon(ic, 30, C.orange, 2.2)}</span><span style="font:700 34px Poppins;color:${t.fg}">${n}</span></div>
    ${roles.map((r) => `<div style="display:flex;gap:10px;align-items:flex-start;margin-top:14px;font:400 23px/1.3 Inter;color:${t.fg}"><span style="flex:none;width:8px;height:8px;border-radius:50%;background:${C.orange};margin-top:12px"></span>${r}</div>`).join('')}</div>`).join('') + `
  <div style="position:absolute;left:88px;top:578px;display:flex;align-items:center;gap:16px"><span style="font:700 30px Poppins;color:${t.fg}">+ 23 specialist Flux agents</span><span class="chip">AI Agent Marketplace</span></div>
  <div style="position:absolute;left:88px;top:636px;width:1744px">${groups.map(([g, col, names]) => `<div style="display:flex;align-items:flex-start;gap:20px;margin-bottom:22px">
    <div style="flex:none;width:300px;display:flex;align-items:center;gap:12px;font:600 23px Inter;color:${t.fg};padding-top:8px"><span style="width:14px;height:14px;border-radius:4px;background:${col}"></span>${g}</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px">${names.map((n) => `<span style="padding:8px 16px;border-radius:999px;background:${C.mist};font:500 22px Inter;color:${t.fg}">Flux ${n}</span>`).join('')}</div></div>`).join('')}</div>
  <div style="position:absolute;left:88px;bottom:32px;font:400 20px Inter;color:${t.muted}">Specialist agents grouped by name for readability.</div>`;
  add('ai-agent-roster', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'AI workforce', title: 'Four core agents, backed by specialists', body, mark: 'tr' }));
}

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9344 });
