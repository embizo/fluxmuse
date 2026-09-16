// Minimal Chrome DevTools Protocol helper (Node 24: global WebSocket + fetch).
// Launches a private headless Chrome, exposes send(), and renders HTML/URLs to PNG.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { tmpdir } from 'node:os';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function launch({ port = 9333, userDataDir } = {}) {
  const udd = userDataDir || process.env.CDP_UDD || `${tmpdir()}/fm-cdp-${port}`;
  const proc = spawn(CHROME, [
    `--remote-debugging-port=${port}`, '--headless=new', `--user-data-dir=${udd}`,
    '--no-first-run', '--no-default-browser-check', '--hide-scrollbars',
    '--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none',
    'about:blank',
  ], { stdio: 'ignore', detached: false });
  let ver;
  for (let i = 0; i < 80; i++) {
    try { ver = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); break; } catch { await sleep(250); }
  }
  if (!ver) throw new Error('chrome did not start');
  const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const page = targets.find((t) => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  let id = 0; const pending = new Map(); const listeners = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result); }
    else if (m.method) listeners.forEach((l) => l(m));
  };
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Page.enable'); await send('Runtime.enable');
  const waitEvent = (name, timeout = 30000) => new Promise((res) => {
    const t = setTimeout(() => res(null), timeout);
    listeners.push(function l(m) { if (m.method === name) { clearTimeout(t); listeners.splice(listeners.indexOf(l), 1); res(m); } });
  });
  const evaluate = async (expr) => {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || JSON.stringify(r.exceptionDetails));
    return r.result.value;
  };
  const setViewport = (width, height, dpr = 2, mobile = false) =>
    send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: dpr, mobile });
  const goto = async (url, settle = 800) => {
    const load = waitEvent('Page.loadEventFired', 45000);
    await send('Page.navigate', { url }); await load;
    await evaluate('document.fonts ? document.fonts.ready.then(()=>true) : true');
    await sleep(settle);
  };
  const shot = async (out, { fullPage = false, clip } = {}) => {
    const params = { format: 'png', captureBeyondViewport: fullPage };
    if (fullPage) {
      const h = await evaluate('Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)');
      const w = await evaluate('document.documentElement.clientWidth');
      params.clip = { x: 0, y: 0, width: w, height: h, scale: 1 };
    }
    if (clip) params.clip = { scale: 1, ...clip };
    const { data } = await send('Page.captureScreenshot', params);
    mkdirSync(dirname(out), { recursive: true });
    writeFileSync(out, Buffer.from(data, 'base64'));
  };
  const close = async () => { try { await send('Browser.close'); } catch {} ; await sleep(300); try { proc.kill('SIGKILL'); } catch {} };
  return { send, evaluate, setViewport, goto, shot, close, sleep, proc };
}

// Render a local HTML file at W×H (CSS px) and DPR to PNG. transparent=true keeps alpha.
export async function renderFile(b, file, out, { width, height, dpr = 2, transparent = false, fullPage = false, settle = 400 }) {
  await b.setViewport(width, height, dpr);
  await b.send('Emulation.setDefaultBackgroundColorOverride', transparent ? { color: { r: 0, g: 0, b: 0, a: 0 } } : {});
  await b.goto('file://' + file, settle);
  await b.shot(out, fullPage ? { fullPage: true } : { clip: { x: 0, y: 0, width, height } });
}
