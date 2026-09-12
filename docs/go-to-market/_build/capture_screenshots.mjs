// Capture logged-out product screenshots of https://fluxmuse.ai via CDP.
// Usage: CDP_UDD=<scratch chrome profile dir> node capture_screenshots.mjs
// Writes PNGs to ../assets/screenshots and records bounding boxes of unverified
// marketing claims to screenshot_regions.json (used by composites to cover them).
import { launch } from './lib/cdp.mjs';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, '..', 'assets', 'screenshots');
const SITE = 'https://fluxmuse.ai';
const regions = {};

const b = await launch({ port: 9335 });
const ls = (reg) => `localStorage.setItem('fluxmuse.cookie.consent','rejected');localStorage.setItem('fm_geo_consent','declined');localStorage.setItem('fluxmuse:geo-consent','declined');localStorage.setItem('fluxmuse:region','${reg}');localStorage.setItem('fm_region','${reg}');localStorage.setItem('fluxmuse-locale','en-${reg}');true`;
const dismiss = `(()=>{for(const re of [/essential only/i,/not now/i]){const e=[...document.querySelectorAll('button')].find(x=>re.test(x.innerText)); if(e) e.click();} return true})()`;
const warm = async () => { // scroll through page to trigger in-view animations / lazy images, then back to top
  const h = await b.evaluate('document.documentElement.scrollHeight');
  for (let y = 0; y < h; y += 500) { await b.evaluate(`window.scrollTo(0,${y})`); await b.sleep(120); }
  await b.evaluate('window.scrollTo(0,0)'); await b.sleep(900);
};
// bounding boxes (document coords, CSS px) of elements whose own text matches unverified claims
const claimBoxes = () => b.evaluate(`(()=>{const res=[]; const pats=[/200\\+ African businesses/,/4\\.9 average rating/,/Stitch ready/,/just bought/,/Lerato's Agency/,/MRR managed/];
  const all=[...document.querySelectorAll('body *')].filter(e=>e.children.length<=3 && e.innerText && e.innerText.length<160);
  for(const p of pats){ const cands=all.filter(e=>p.test(e.innerText)); if(!cands.length) continue; const e=cands.sort((a,b)=>a.innerText.length-b.innerText.length)[0]; const r=e.getBoundingClientRect(); res.push({claim:p.source,x:r.x+scrollX,y:r.y+scrollY,w:r.width,h:r.height}); }
  return res})()`);
const prep = async (path, reg = 'ZA', { w = 1440, h = 900, dpr = 2, mobile = false } = {}) => {
  await b.setViewport(w, h, dpr, mobile);
  await b.goto(SITE + '/', 800);
  await b.evaluate(ls(reg));
  await b.goto(SITE + path, 3500);
  await b.evaluate(dismiss); await b.sleep(400);
  await b.evaluate(`(()=>{const s=document.createElement('style'); s.textContent='[class*=cookie],[id*=cookie]{display:none!important}'; document.head.appendChild(s); return 1})()`);
};
const shot = async (name, opts = {}) => {
  await b.shot(join(OUT, name), opts);
  regions[name] = { dpr: opts.dpr, boxes: await claimBoxes(), scrollY: await b.evaluate('scrollY') };
  console.log('saved', name);
};

// chat container of /demo
const chatRect = `(()=>{const h=[...document.querySelectorAll('*')].find(e=>/FluxMuse Demo Store/.test(e.textContent)&&e.children.length<3&&e.textContent.length<40); let p=h; for(let i=0;i<8&&p;i++){ if(p.getBoundingClientRect().height>500) break; p=p.parentElement;} const r=p.getBoundingClientRect(); return {x:r.x+scrollX,y:r.y+scrollY,w:r.width,h:r.height}})()`;
const click = (re) => b.evaluate(`(()=>{const e=[...document.querySelectorAll('button')].filter(x=>${re}.test(x.innerText)); if(!e.length) throw new Error('no button ${re}'); e[0].click(); return true})()`);
const fill = (ph, val) => b.evaluate(`(()=>{const i=[...document.querySelectorAll('input')].find(x=>x.placeholder===${JSON.stringify(ph)}); const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set; set.call(i,${JSON.stringify(val)}); i.dispatchEvent(new Event('input',{bubbles:true})); return true})()`);

const hideFixed = (on) => `(()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position; if(p==='fixed'||p==='sticky'||e.dataset.fmHidden){ if(${on}){e.dataset.fmHidden='1'; e.style.visibility='hidden';} else {e.style.visibility=''; delete e.dataset.fmHidden;} }} return true})()`;
async function demoFlow(tag, vp) {
  await prep('/demo', 'ZA', vp);
  const steps = [
    ['01-catalog', async () => {}],
    ['02-added-to-cart', async () => { await click('/Shea Butter/'); await b.sleep(500); await click('/Rooibos/'); }],
    ['03-cart', async () => click('/View cart/')],
    ['04-checkout-details', async () => { await click('/^\\s*Checkout/'); await b.sleep(700); await fill('Your name', 'Thandi M.'); await fill('+27 71 234 5678', '+27 71 234 5678'); }],
    ['05-payment-method', async () => click('/Yoco card/')],
    ['06-processing', async () => click('/^Pay R/')],
    ['07-confirmation', async () => b.sleep(1600)],
  ];
  for (const [name, act] of steps) {
    await act(); await b.sleep(name === '06-processing' ? 250 : 900);
    const r = await b.evaluate(chatRect);
    const pad = 0;
    if (tag === 'desktop') {
      // viewport shot with the phone fully in view below the sticky site header (~78px)
      await b.evaluate(`window.scrollTo(0, ${Math.max(0, r.y - 120)})`); await b.sleep(250);
      await b.shot(join(OUT, `demo-step-${name}.png`));
    } else {
      await b.evaluate(`window.scrollTo(0, ${Math.max(0, r.y - 96)})`); await b.sleep(250);
      await b.shot(join(OUT, `demo-step-${name}_mobile.png`));
    }
    // chat-screen-only crop (used for device-framed composites); hide sticky header + floating button meanwhile
    await b.evaluate(hideFixed(true));
    const r2 = await b.evaluate(chatRect);
    await b.shot(join(OUT, 'crops', `demo-step-${name}_chat-${tag}.png`), { clip: { x: r2.x - pad, y: r2.y - pad, width: r2.w + pad * 2, height: r2.h + pad * 2 } });
    await b.evaluate(hideFixed(false));
    console.log('saved demo step', tag, name, JSON.stringify(r2));
  }
}

try {
  const D = { w: 1440, h: 900, dpr: 2 };
  const M = { w: 390, h: 844, dpr: 3, mobile: true };
  // "clean" hero captures: unverified social-proof claims hidden in the DOM (visibility:hidden, layout kept)
  const hideClaims = `(()=>{const hidden=[]; const leaf=(re)=>[...document.querySelectorAll('body *')].filter(e=>re.test(e.innerText||'')).sort((a,b)=>a.innerText.length-b.innerText.length)[0];
    const climb=(e,ok)=>{while(e.parentElement && ok(e.parentElement)) e=e.parentElement; return e};
    const hide=(e,tag)=>{ if(e){ e.style.visibility='hidden'; hidden.push(tag+':'+e.innerText.replace(/\\n/g,' ').slice(0,60)); } };
    hide(climb(leaf(/Stitch ready/), p=>p.innerText.length<60), 'trust-line');
    hide(climb(leaf(/200\\+ African businesses/), p=>p.innerText.length<80 && !/Start free/.test(p.innerText)), 'social-proof');
    const t=leaf(/just bought/); hide(t && climb(t, p=>p.innerText.length<70), 'toast');
    return hidden})()`;
  if (process.env.ONLY === 'clean') {
    for (const [vp, name] of [[D, 'home-hero_clean.png'], [M, 'home_clean_mobile.png']]) {
      await prep('/', 'ZA', vp); await b.sleep(2500);
      console.log(name, await b.evaluate(hideClaims)); await b.sleep(100);
      await b.shot(join(OUT, name));
      console.log('still visible:', JSON.stringify(await claimBoxes()));
    }
  } else if (process.env.ONLY === 'demo') { await demoFlow('desktop', D); await demoFlow('mobile', M); } else {
  await prep('/', 'ZA', D); await b.sleep(2500);
  await shot('home-hero.png');
  await warm(); await shot('home-full.png', { fullPage: true });

  await prep('/features', 'ZA', D); await shot('features-hero.png'); await warm(); await shot('features-full.png', { fullPage: true });
  for (const reg of ['ZA', 'NG', 'KE']) {
    await prep('/pricing', reg, D); await shot(`pricing-${reg.toLowerCase()}.png`);
    if (reg === 'ZA') { await warm(); await shot('pricing-za-full.png', { fullPage: true }); }
  }
  await prep('/for-agencies', 'ZA', D); await shot('for-agencies-hero.png'); await warm(); await shot('for-agencies-full.png', { fullPage: true });
  await prep('/demo', 'ZA', D); await shot('demo.png'); await warm(); await shot('demo-full.png', { fullPage: true });
  await demoFlow('desktop', D);

  await prep('/', 'ZA', M); await b.sleep(2500); await shot('home_mobile.png'); // full-page mobile capture tiles/repeats in headless Chrome, so it is skipped
  await prep('/demo', 'ZA', M); await shot('demo_mobile.png');
  await demoFlow('mobile', M);
  }
} finally {
  if (!process.env.ONLY) writeFileSync(join(HERE, 'screenshot_regions.json'), JSON.stringify(regions, null, 2));
  await b.close();
}
