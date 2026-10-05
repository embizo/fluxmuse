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
    ['Discovery call', 'Week 0', 'chat', 'Your goals, products and how customers reach you today', 'Goals, products, how customers reach you'],
    ['Demo on your products', 'Week 0', 'search', 'We build a demo shop from your public photos and show it live', 'A demo shop from your own public photos'],
    ['Set up by hand', 'Week 1', 'zap', 'WhatsApp Business number, catalogue from your photos, shop link', 'WhatsApp number, catalogue, shop link'],
    ['Go live', 'Day 1', 'megaphone', 'Share your link, post weekly; the 30-day lead guarantee starts', 'Share your link; lead guarantee starts'],
    ['Weekly check-ins', 'Weeks 1–4', 'chart', 'What came in, what sold, and what to post next', 'What came in, what to post next'],
    ['Keep growing', 'Month 2+', 'trend', 'Change plan as you grow; add brands and channels', 'Change plan as you grow'],
  ];
  const kpis = [['Qualified leads', 'chat'], ['Orders via your link', 'bag'], ['Posts made', 'pen'], ['Time saved', 'clock']];
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
      <div style="position:absolute;left:88px;top:772px;font:700 26px Poppins;color:${t.fg}">What we measure together</div>
      <div style="position:absolute;left:88px;top:820px;display:flex;gap:16px">${kpis.map(([k, ic]) => `<div style="display:flex;align-items:center;gap:12px;padding:14px 22px;border-radius:999px;background:${C.mist};font:600 24px Inter;color:${t.fg}">${icon(ic, 28, C.orange, 2.2)}${k}</div>`).join('')}</div>
      <div style="position:absolute;left:88px;bottom:34px;width:1500px;font:400 21px/1.4 Inter;color:${t.muted}">Typical timings. Goals are agreed at kickoff, not promised results. Lead guarantee: 3 qualified leads in 30 days of go-live, or we keep supporting you at no extra charge until you get them, as long as you share your link and post weekly. Not a refund.</div>`;
      return frame({ w, h, eyebrow: 'Working with FluxMuse', title: 'From first call to your first orders', body });
    }
    const y0 = 196, rh = 92, g = 8;
    const body = `
    <svg style="position:absolute;left:0;top:0" width="${w}" height="${h}"><line x1="222" y1="${y0 + rh / 2}" x2="222" y2="${y0 + 5 * (rh + g) + rh / 2}" stroke="${C.orange}" stroke-width="4"/></svg>
    ${stages.map(([n, wk, ic, d, ds], i) => { const y = y0 + i * (rh + g); const hi = i === 3; return `
      <div style="position:absolute;left:56px;top:${y + rh / 2 - 16}px;width:136px;text-align:right;font:600 20px Inter;color:${hi ? '#C24E00' : t.muted}">${wk}</div>
      <div style="position:absolute;left:200px;top:${y + rh / 2 - 22}px;width:44px;height:44px;border-radius:50%;background:${hi ? C.orange : '#fff'};border:4px solid ${C.orange};font:700 20px Poppins;color:${hi ? C.night : C.ink};display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div class="card" style="position:absolute;left:268px;top:${y}px;width:756px;height:${rh}px;padding:14px 20px;display:flex;align-items:center;gap:16px;${hi ? `border:2.5px solid ${C.orange};background:${C.tint}` : ''}">
        ${icon(ic, 32, C.orange, 2.2)}<div><div style="font:700 24px/1.15 Poppins;color:${t.fg}">${n}</div><div style="font:400 20px/1.3 Inter;color:${t.muted}">${ds}</div></div></div>`; }).join('')}
    <div style="position:absolute;left:56px;top:${y0 + 6 * (rh + g) + 8}px;font:700 23px Poppins;color:${t.fg}">What we measure</div>
    <div style="position:absolute;left:56px;right:56px;top:${y0 + 6 * (rh + g) + 48}px;display:grid;grid-template-columns:repeat(2,1fr);gap:10px">${kpis.map(([k, ic]) => `<div style="display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:999px;background:${C.mist};font:600 20px Inter;color:${t.fg};white-space:nowrap">${icon(ic, 22, C.orange, 2.2)}${k}</div>`).join('')}</div>
    <div style="position:absolute;left:56px;right:56px;top:${y0 + 6 * (rh + g) + 172}px;font:400 18px/1.35 Inter;color:${t.muted}">Goals agreed at kickoff, not promised results. Lead guarantee: 3 qualified leads in 30 days, or we keep supporting you free until you get them (if you share your link and post weekly).</div>`;
    return frame({ w, h, eyebrow: 'Working with FluxMuse', title: 'First call to first orders', mark: 'tr', headW: 760, body });
  };
  add('brand-engagement-journey', 1920, 1080, build({ w: 1920, h: 1080 }));
  add('brand-engagement-journey_square', 1080, 1080, build({ w: 1080, h: 1080 }));
}

// 8. pilot-campaign-framework: retired 2026-10-05 (there is no pilot).

// ============ 9. pricing-tiers (nine tiers in three bands, CURRENT_OFFER.md §1) ============
{
  const t = T(false);
  const R = (n) => 'R' + n.toLocaleString('en-US');
  const bands = [
    ['Small', 'Side-hustles and solo sellers', [['Free', 0, '1 brand · 1 channel', 'Free forever, no card'], ['Nano', 149, '1 brand · 3 channels', 'Entry paid plan'], ['Micro', 289, '1 brand · 4 channels', '1 WhatsApp number']]],
    ['Medium', 'Growing small businesses', [['Starter', 499, '1 brand · 3 channels', ''], ['Growth', 1999, '3 brands · 15 channels', '+ inbound AI Voice (beta)'], ['Scale', 4999, '10 brands · 40 channels', '+ in & outbound AI Voice (beta)']]],
    ['Enterprise', 'Larger teams and agencies', [['Corporate', 6999, '25 brands · 60 channels', 'Bring your own cloud'], ['Agency', 9999, 'Unlimited brands · 80 channels', 'White-label, multi-client'], ['Custom', null, 'Sized to you', 'By consultation']]],
  ];
  const ribbon = `<div style="position:absolute;left:88px;top:238px;width:1744px;height:74px;border-radius:18px;background:${C.orange};display:flex;align-items:center;gap:18px;padding:0 28px;color:${C.night}">
    <span style="flex:none;width:44px;height:44px;border-radius:50%;background:${C.night};display:flex;align-items:center;justify-content:center">${icon('sparkles', 26, C.orange, 2.4)}</span>
    <span style="font:700 28px Poppins">Founding Member:</span><span style="font:600 26px Inter">30% off your first two monthly bills · South African sign-ups · while it lasts</span></div>`;
  const cw = (1744 - 2 * 28) / 3, rowH = 168;
  const body = ribbon + bands.map(([b, aud, tiers], i) => `<div class="card" style="position:absolute;left:${88 + i * (cw + 28)}px;top:340px;width:${cw}px;height:612px;overflow:hidden">
    <div style="background:${C.mist};padding:14px 26px"><span style="font:700 30px Poppins;color:${t.fg}">${b}</span> <span style="font:500 20px Inter;color:${t.muted}">· ${aud}</span></div>
    ${tiers.map(([n, m, cap, note], k) => `<div style="height:${rowH}px;padding:16px 26px;${k ? `border-top:1.5px solid ${t.line};` : ''}display:flex;justify-content:space-between;align-items:center;gap:16px">
      <div><div style="font:700 30px Poppins;color:${t.fg}">${n}</div><div style="font:500 20px/1.3 Inter;color:${t.muted};margin-top:4px">${cap}</div>${note ? `<div style="font:500 19px/1.3 Inter;color:${t.accentText};margin-top:2px">${note}</div>` : ''}</div>
      <div style="text-align:right;flex:none">${m === null ? `<div style="font:700 34px Poppins;color:${t.fg}">On request</div>` : `<div style="font:700 44px/1 Poppins;color:${t.fg};white-space:nowrap">${R(m)}<span style="font:500 20px Inter;color:${t.muted}"> /mo</span></div>${m ? `<div style="font:400 18px Inter;color:${t.muted};margin-top:6px">or ${R(m * 10)}/yr</div>` : ''}`}</div></div>`).join('')}
  </div>`).join('') + `<div style="position:absolute;left:88px;top:976px;width:1744px;font:400 21px/1.45 Inter;color:${t.muted}">Prices in rands, the amount you pay. Annual = 10× monthly. Every paid plan starts with payment; Free is a permanent plan, not a trial. <b style="color:${t.fg}">Agency partners: R6,999/mo wholesale.</b> AI credit allowances: see the pricing page.</div>`;
  add('pricing-tiers', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Pricing', title: 'Nine plans in three bands, priced in rands', sub: 'Paid plans from R149 a month.', body, mark: 'tr' }));
}

// ============ 10. roadmap-2026-2027 (file name kept; no dates while the model is rebuilt) ============
{
  const build = (dark) => {
    const t = T(dark);
    const cols = [['Now · Oct 2026', 'Live'], ['Next', 'Being switched on'], ['Then', 'Once pending accounts are live'], ['Later', 'Self-serve'], ['Coming soon', '']];
    const X0 = 360, cw = (1832 - X0) / cols.length;
    const laneY = [318, 640];
    const box = (ci, y, ht, inner, { hl = false, dashed = false, tint = false, span = 1 } = {}) => `<div style="position:absolute;left:${X0 + ci * cw + 8}px;top:${y}px;width:${span * cw - 16}px;height:${ht}px;border-radius:18px;padding:14px 18px;background:${tint ? t.chipBg : t.card};border:${dashed ? `2.5px dashed ${t.ring}` : hl ? `2.5px solid ${C.orange}` : `1.5px solid ${t.line}`};overflow:hidden">${inner}</div>`;
    const h3 = (s2, fs = 23) => `<div style="font:700 ${fs}px/1.18 Poppins;color:${t.fg}">${s2}</div>`;
    const p = (s2, fs = 19) => `<div style="font:400 ${fs}px/1.32 Inter;color:${t.muted};margin-top:6px">${s2}</div>`;
    const body = `
    <div style="position:absolute;left:${X0}px;top:228px;display:flex">${cols.map(([c, s2], i) => `<div style="width:${cw}px;text-align:center"><div style="font:700 23px Poppins;color:${i === 4 ? t.muted : t.fg}">${c}</div><div style="font:500 17px Inter;color:${t.muted}">${s2}</div></div>`).join('')}</div>
    <svg style="position:absolute;left:0;top:0" width="1920" height="1080">
      <line x1="${X0}" y1="296" x2="1832" y2="296" stroke="${C.orange}" stroke-width="4"/>
      ${cols.map((_, i) => `<circle cx="${X0 + (i + 0.5) * cw}" cy="296" r="9" fill="${i === 0 ? C.orange : t.bg}" stroke="${i === 4 ? t.ring : C.orange}" stroke-width="3"/>`).join('')}
      <line x1="88" y1="622" x2="1832" y2="622" stroke="${t.line}" stroke-width="2" stroke-dasharray="8 6"/>
    </svg>
    <div style="position:absolute;left:88px;top:${laneY[0] + 6}px;width:250px">${icon('globe', 34, C.orange, 2.2)}<div style="font:700 26px/1.15 Poppins;color:${t.fg};margin-top:10px">Markets &amp; payments</div></div>
    <div style="position:absolute;left:88px;top:${laneY[1] + 6}px;width:250px">${icon('layers', 34, C.orange, 2.2)}<div style="font:700 26px/1.15 Poppins;color:${t.fg};margin-top:10px">Product</div><div style="font:400 19px/1.3 Inter;color:${t.muted};margin-top:6px">In the founder’s agreed order</div></div>
    ${box(0, laneY[0], 290, `${h3('South Africa open')}${p('Paystack live. A small first group of businesses, set up by hand. Founding Member: 30% off the first two bills.')}`, { hl: true, tint: true })}
    ${box(1, laneY[0], 290, `${h3('Checkout through FluxMuse')}${p('Paystack, South Africa. Switched on once tested end to end with real money.')}`)}
    ${box(2, laneY[0], 290, `${h3('Nigeria, Kenya, Ghana')}${p('Priced in NGN, KES and GHS. Opens once Fincra and pawaPay accounts are live and checkout is tested.')}`)}
    ${box(3, laneY[0], 290, `${h3('Other covered markets')}${p('Billed in USD, self-serve. No local team until there is demand.')}`)}
    ${box(4, laneY[0], 290, `${h3('Botswana &amp; Namibia')}${p('Once a provider covers them.')}`, { dashed: true })}
    ${box(0, laneY[1], 300, `${h3('Live, newly launched', 22)}${p('WhatsApp Concierge, shop link, order alerts, POST captions and images, short videos, voice notes, TikTok video posting', 18)}`, { hl: true, tint: true })}
    ${box(1, laneY[1], 300, `${h3('1 · Meta permissions', 22)}${p('Facebook Pages and Instagram auto-publishing, daily digest, ads. AI Voice beta.', 18)}`)}
    ${box(2, laneY[1], 300, `${h3('2 · Social adapters', 22)}${p('Instagram Login, Threads, LinkedIn, X, YouTube, Pinterest', 18)}`)}
    ${box(3, laneY[1], 300, `${h3('3 · Business apps', 22)}${p('Shopify, WooCommerce, Takealot sync; CRM, accounting', 18)}`)}
    ${box(4, laneY[1], 300, `${h3('4 · Partner programme', 22)}${p('Referral tracking, white-label, partner workspaces', 18)}`)}
    <div style="position:absolute;left:88px;bottom:30px;width:1744px;font:400 20px/1.4 Inter;color:${t.muted}">Indicative order, not commitments, and no dates: timing depends on Meta approvals, payment-provider accounts and real-money checkout tests. No paid checkout outside South Africa until then.</div>`;
    return frame({ w: 1920, h: 1080, dark, eyebrow: 'Roadmap · indicative', title: 'What comes next, in order', body, mark: 'tr' });
  };
  add('roadmap-2026-2027', 1920, 1080, build(false));
  add('roadmap-2026-2027_dark', 1920, 1080, build(true));
}

// ============ 11. omnichannel-hub ============
{
  const t = T(false);
  const nodes = [['WhatsApp Business', 'chat', true], ['WhatsApp Status', 'sparkles', true], ['Hosted shop link', 'link', true], ['TikTok video', 'send', true], ['Consented broadcasts', 'mail', true], ['Facebook Pages', 'globe', false], ['Instagram posts', 'sparkles', false], ['WhatsApp ads', 'phone', false], ['Instagram DMs', 'chat', 'na'], ['X posting', 'file', 'na']];
  const cx = 960, cy = 618, rx = 650, ry = 300, nw = 330, nh = 84;
  const pos = nodes.map((_, i) => { const th = ((-90 + i * 36) * Math.PI) / 180; return [cx + rx * Math.cos(th), cy + ry * Math.sin(th)]; });
  const body = `
  <svg style="position:absolute;left:0;top:0" width="1920" height="1080">
    ${pos.map(([x, y], i) => `<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="${nodes[i][2] === true ? C.orange : '#9AA5B1'}" stroke-width="3" ${nodes[i][2] === true ? '' : nodes[i][2] === 'na' ? 'stroke-dasharray="2 10" opacity=".5"' : 'stroke-dasharray="10 8"'}/>`).join('')}
  </svg>
  <div style="position:absolute;left:${cx - 140}px;top:${cy - 140}px;width:280px;height:280px;border-radius:50%;background:#fff;border:3px solid ${C.orange};box-shadow:0 0 0 18px ${C.tint};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <img src="${ICON}" style="width:120px"><div style="font:700 24px/1.2 Poppins;color:${t.fg};margin-top:6px">FluxMuse<br>AI team</div></div>
  ${pos.map(([x, y], i) => { const [n, ic, live] = nodes[i]; return `<div class="card" style="position:absolute;left:${x - nw / 2}px;top:${y - nh / 2}px;width:${nw}px;height:${nh}px;display:flex;align-items:center;gap:14px;padding:0 20px;${live === true ? '' : live === 'na' ? 'opacity:.6' : `border:2px dashed #9AA5B1`}">
    <span style="flex:none;width:44px;height:44px;border-radius:12px;background:${live === true ? C.tint : C.mist};display:flex;align-items:center;justify-content:center">${icon(ic, 26, live === true ? C.orange : '#5B6570', 2.2)}</span>
    <span style="font:600 23px/1.15 Inter;color:${t.fg}">${n}${live === true ? '' : `<br><span style="font:500 18px Inter;color:#5B6570">${live === 'na' ? 'not available' : 'being switched on'}</span>`}</span></div>`; }).join('')}
  <div style="position:absolute;left:88px;bottom:36px;display:flex;align-items:center;gap:28px;font:500 21px Inter;color:${t.muted}">
    <span style="display:flex;align-items:center;gap:10px"><svg width="46" height="6"><line x1="0" y1="3" x2="46" y2="3" stroke="${C.orange}" stroke-width="4"/></svg>live</span>
    <span style="display:flex;align-items:center;gap:10px"><svg width="46" height="6"><line x1="0" y1="3" x2="46" y2="3" stroke="#9AA5B1" stroke-width="4" stroke-dasharray="10 7"/></svg>being switched on</span><span>Faded: not available</span></div>`;
  add('omnichannel-hub', 1920, 1080, frame({ w: 1920, h: 1080, eyebrow: 'Channels', title: 'Where FluxMuse works today', body, mark: 'tr' }));
}

// ============ 12. problem-solution ============
{
  const t = T(false);
  const today = ['A stack of disconnected tools for posts, chats, email, SMS and payments', 'Agency retainers priced beyond most small-business budgets', 'No shop page, so orders get lost in chats', 'After-hours messages go unanswered, and the sale goes cold'];
  const fm = ['An AI marketing team that lives in WhatsApp', 'Paid plans from R149 a month, priced in rands', 'Send product photos, get a catalogue and a shop link', 'The assistant answers in your customer’s language, day and night'];
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
        ${[['TAM', '44M', 'SSA MSMEs'], ['SAM', '~3.5M', 'digitally active SMBs in the markets our contracted payment providers cover, selling via social/WhatsApp, able to pay ≥US$25/mo'], ['SOM (5-yr)', '~17,500', 'paying workspaces, about 0.5% of SAM']].map(([k, v, d], i) => `${i ? `<div style="display:flex;align-items:center"><svg width="26" height="40"><path d="M6 6 L20 20 L6 34" fill="none" stroke="${C.orange}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>` : ''}<div style="flex:${i === 1 ? 1.6 : 1};background:#fff;border-radius:16px;padding:12px 20px"><div style="font:700 20px Inter;letter-spacing:.08em;color:#C24E00">${k}</div><div style="font:700 36px/1.1 Poppins;color:${t.fg}">${v}</div><div style="font:400 19px/1.3 Inter;color:${t.muted}">${d}</div></div>`).join('')}
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
