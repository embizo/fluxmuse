// Print the preview HTML files (from preview_proposals.py html <dir>) to A4 PDFs with headless Chrome.
// Usage: CDP_UDD=<scratch profile dir> node preview_proposals.mjs <dir>
import { readdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { launch } from '../lib/cdp.mjs';

const dir = resolve(process.argv[2]);
const b = await launch({ port: 9351 });
try {
  for (const f of readdirSync(dir).filter((n) => n.endsWith('.html'))) {
    await b.goto('file://' + join(dir, f), 1500);
    const footer = `<div style="font-family:Arial;font-size:7px;color:#5B6570;width:100%;text-align:center">Fluxmuse Pty Ltd · fluxmuse.ai · Confidential proposal · Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>`;
    const header = `<div style="font-family:Arial;font-size:8px;width:100%;margin:0 2cm;border-bottom:1.5px solid #FF6A00;padding-bottom:3px"><b style="color:#C24E00">FLUX</b><b style="color:#37474F">MUSE</b></div>`;
    const { data } = await b.send('Page.printToPDF', {
      paperWidth: 8.27, paperHeight: 11.69, printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: header, footerTemplate: footer,
    });
    writeFileSync(join(dir, f.replace(/\.html$/, '.pdf')), Buffer.from(data, 'base64'));
    console.log('pdf', f);
  }
} finally {
  await b.close();
}
