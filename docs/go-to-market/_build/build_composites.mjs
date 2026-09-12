// Device-framed composites of product screenshots → ../assets/screenshots/composites
// Run composites/prep_screens.py first. Usage: node build_composites.mjs [nameFilter]
import { join } from 'node:path';
import { renderJobs, ASSETS, page, netSVG, C } from './lib/page.mjs';

const OUT = join(ASSETS, 'screenshots', 'composites');
const S = '../../assets/screenshots/', WK = 'work/';
const jobs = [];
const add = (name, w, h, html, opts = {}) => jobs.push({ name, dir: 'composites', html, w, h, out: join(OUT, name + '.png'), settle: 700, ...opts });

// ---- frames ----
const browser = (src, url, width, shotH, { crop = 1 } = {}) => {
  const imgH = Math.round(width * 1800 / 2880);
  const viewH = Math.round(imgH * crop);
  return `<div style="width:${width}px;border-radius:16px;overflow:hidden;background:#1B2027;box-shadow:0 40px 80px -20px rgba(15,20,25,.45),0 0 0 1px rgba(255,255,255,.06)">
    <div style="height:48px;display:flex;align-items:center;gap:9px;padding:0 18px;background:#20262E">
      <span style="width:13px;height:13px;border-radius:50%;background:#FF5F57"></span><span style="width:13px;height:13px;border-radius:50%;background:#FEBC2E"></span><span style="width:13px;height:13px;border-radius:50%;background:#28C840"></span>
      <div style="margin-left:22px;flex:1;max-width:520px;height:30px;border-radius:9px;background:#12161B;color:#A7B0BA;font:500 15px Inter;display:flex;align-items:center;padding-left:14px">🔒&nbsp; ${url}</div></div>
    <div style="height:${viewH}px;overflow:hidden"><img src="${src}" style="display:block;width:${width}px;height:${imgH}px"></div></div>`;
};
const laptop = (src, width) => {
  const sw = width - 36, sh = Math.round(sw * 10 / 16);
  return `<div style="width:${width}px;display:flex;flex-direction:column;align-items:center;filter:drop-shadow(0 40px 50px rgba(15,20,25,.35))">
    <div style="width:${width}px;padding:18px 18px 26px;border-radius:26px 26px 0 0;background:#0C0E11;box-shadow:inset 0 0 0 2px #2A2F36">
      <div style="width:${sw}px;height:${sh}px;overflow:hidden;border-radius:4px;background:#000"><img src="${src}" style="display:block;width:${sw}px;height:${sh}px;object-fit:cover;object-position:top"></div></div>
    <div style="width:${Math.round(width * 1.16)}px;height:${Math.round(width * 0.028)}px;background:linear-gradient(#D9DDE2,#9AA3AD);border-radius:0 0 ${Math.round(width * 0.02)}px ${Math.round(width * 0.02)}px;position:relative">
      <div style="position:absolute;left:50%;top:0;transform:translateX(-50%);width:${Math.round(width * 0.16)}px;height:${Math.round(width * 0.011)}px;background:#8C949E;border-radius:0 0 10px 10px"></div></div></div>`;
};
const phone = (src, width) => {
  const pad = Math.round(width * 0.034), sw = width - 2 * pad, statusH = Math.round(sw * 0.112), screenH = Math.round(sw * 826 / 412) + statusH;
  const fs = Math.round(sw * 0.036);
  return `<div style="width:${width}px;padding:${pad}px;border-radius:${Math.round(width * 0.15)}px;background:#0B0D10;box-shadow:inset 0 0 0 2px #2F353D,0 40px 70px -18px rgba(15,20,25,.5)">
    <div style="position:relative;width:${sw}px;height:${screenH}px;border-radius:${Math.round(width * 0.12)}px;overflow:hidden;background:#0B141A">
      <div style="height:${statusH}px;background:#202C33;color:#E9EDEF;display:flex;align-items:center;justify-content:space-between;padding:0 ${Math.round(sw * 0.09)}px;font:600 ${fs}px Inter">
        <span>9:41</span><span style="width:${Math.round(sw * 0.28)}px;height:${Math.round(statusH * 0.52)}px;border-radius:99px;background:#000"></span><span style="letter-spacing:2px">▮▮▮ ◔</span></div>
      <img src="${src}" style="display:block;width:${sw}px;height:${screenH - statusH}px;object-fit:cover;object-position:top">
      <div style="position:absolute;left:50%;bottom:${Math.round(sw * 0.02)}px;transform:translateX(-50%);width:${Math.round(sw * 0.34)}px;height:${Math.max(4, Math.round(sw * 0.012))}px;border-radius:9px;background:rgba(255,255,255,.75)"></div>
    </div></div>`;
};
const phoneH = (width) => { const pad = Math.round(width * 0.034), sw = width - 2 * pad; return Math.round(sw * 826 / 412) + Math.round(sw * 0.112) + 2 * pad; };
const center = (inner, w, h) => page({ title: 'composite', w, h, body: `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${inner}</div>`, css: 'html,body,.canvas{background:transparent!important}' });

// ---- browser & laptop (transparent) ----
const screens = [
  ['home', WK + 'home-hero_clean_nofooter.png', 'fluxmuse.ai'],
  ['pricing', S + 'pricing-za.png', 'fluxmuse.ai/pricing'],
  ['demo', S + 'demo.png', 'fluxmuse.ai/demo'],
];
for (const [n, src, url] of screens) {
  add(`browser-${n}`, 1600, 1040, center(browser(src, url, 1480, 0), 1600, 1040), { transparent: true });
  add(`laptop-${n}`, 1800, 1180, center(laptop(src, 1440), 1800, 1180), { transparent: true });
}

// ---- phones per demo step (transparent) ----
const steps = ['01-catalog', '02-added-to-cart', '03-cart', '04-checkout-details', '05-payment-method', '06-processing', '07-confirmation'];
for (const s of steps) add(`phone-demo-step-${s}`, 560, phoneH(480) + 80, center(phone(`${WK}demo-step-${s}_phone.png`, 480), 560, phoneH(480) + 80), { transparent: true });

// ---- 3-phone checkout strip ----
const strip = (dark) => {
  const pw = 360, ph = phoneH(pw);
  const fg = dark ? '#F5F6F8' : C.ink, muted = dark ? '#A7B0BA' : '#5B6570';
  const items = [['01-catalog', '1', 'Browse the catalog'], ['03-cart', '2', 'Review the cart'], ['07-confirmation', '3', 'Pay locally, get confirmation']];
  return page({ title: 'strip', w: 1920, h: 1080, dark, bg: dark ? C.night : C.mist, body: `
    ${netSVG(1920, 1080, { seed: 8, n: 30, color: dark ? '#fff' : C.slate, opacity: dark ? 0.07 : 0.09 })}
    <div style="position:absolute;left:88px;top:60px"><div style="font:700 22px Inter;letter-spacing:.16em;text-transform:uppercase;color:${dark ? C.glow : '#C24E00'}">WhatsApp checkout</div>
      <div style="font:700 56px Poppins;color:${fg};margin-top:8px">Checkout inside the chat</div></div>
    <div style="position:absolute;right:88px;top:74px;font:500 21px Inter;color:${muted}">Interactive demo store at fluxmuse.ai/demo</div>
    <div style="position:absolute;left:0;right:0;top:${1080 - ph - 108}px;display:flex;justify-content:center;align-items:flex-start;gap:150px">
      ${items.map(([s, n, l], i) => `<div style="position:relative;display:flex;flex-direction:column;align-items:center">${phone(`${WK}demo-step-${s}_phone.png`, pw)}
        <div style="margin-top:22px;display:flex;align-items:center;gap:12px;font:600 26px Inter;color:${fg}"><span style="width:40px;height:40px;border-radius:50%;background:${C.orange};color:${C.night};font:700 22px Poppins;display:flex;align-items:center;justify-content:center">${n}</span>${l}</div>
        ${i < 2 ? `<svg style="position:absolute;right:-126px;top:${ph / 2 - 20}px" width="100" height="40"><line x1="4" y1="20" x2="80" y2="20" stroke="${C.orange}" stroke-width="5" stroke-linecap="round"/><path d="M76 8 L96 20 L76 32 z" fill="${C.orange}"/></svg>` : ''}</div>`).join('')}
    </div>` });
};
add('checkout-in-chat-3-phones', 1920, 1080, strip(false));
add('checkout-in-chat-3-phones_dark', 1920, 1080, strip(true));

// ---- hero composites ----
const hero = (dark) => page({ title: 'hero', w: 1920, h: 1080, dark, bg: dark ? C.night : C.paper, body: `
  <div style="position:absolute;inset:0;background:radial-gradient(circle at 62% 48%, ${dark ? 'rgba(255,106,0,.20)' : 'rgba(255,106,0,.10)'}, transparent 55%)"></div>
  ${netSVG(1920, 1080, { seed: 13, n: 40, color: dark ? '#fff' : C.slate, opacity: dark ? 0.07 : 0.08 })}
  <div style="position:absolute;left:170px;top:120px">${laptop(WK + 'home-hero_clean_nofooter.png', 1300)}</div>
  <div style="position:absolute;left:1380px;top:250px">${phone(WK + 'demo-step-07-confirmation_phone.png', 390)}</div>` });
add('hero-laptop-phone_night', 1920, 1080, hero(true));
add('hero-laptop-phone_white', 1920, 1080, hero(false));

const filter = process.argv[2];
await renderJobs(filter ? jobs.filter((j) => j.name.includes(filter)) : jobs, { port: 9343 });
