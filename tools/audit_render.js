/* Visual + runtime audit harness.
 * Renders the portal at several viewports, captures console output,
 * and reports layout metrics for comparison with mock1.png.
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PAGE = 'file:///K:/Newfolder/index.html';
const OUTDIR = 'K:\\Newfolder\\tools\\shots';

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 1000, dsf: 1 },
  { name: 'tablet',  width: 820,  height: 1180, dsf: 1 },
  { name: 'mobile',  width: 390,  height: 844,  dsf: 2 },
];

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
      '--allow-file-access-from-files', '--force-color-profile=srgb',
      '--font-render-hinting=none',
    ],
  });

  const report = {};

  for (const vp of VIEWPORTS) {
    const page = await browser.newPage();
    const logs = [];
    page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`));
    page.on('pageerror', e => logs.push(`[pageerror] ${e.message}`));
    page.on('requestfailed', r =>
      logs.push(`[requestfailed] ${r.url()} :: ${r.failure() && r.failure().errorText}`));

    await page.setViewport({
      width: vp.width, height: vp.height,
      deviceScaleFactor: vp.dsf, isMobile: vp.width < 768, hasTouch: vp.width < 768,
    });
    await page.goto(PAGE, { waitUntil: 'networkidle0', timeout: 45000 });
    await new Promise(r => setTimeout(r, 1200));

    // force reveal animations to be visible for capture
    await page.evaluate(() => {
      document.querySelectorAll('.reveal').forEach(el => {
        el.classList.add('is-visible');
      });
      window.scrollTo(0, 0);
    });
    await new Promise(r => setTimeout(r, 500));

    const out = path.join(OUTDIR, `${vp.name}.png`);
    await page.screenshot({ path: out, fullPage: true });

    const metrics = await page.evaluate(() => {
      const docH = document.documentElement.scrollHeight;
      const sec = [];
      document.querySelectorAll('section[id],header,footer').forEach(el => {
        const r = el.getBoundingClientRect();
        sec.push({
          tag: el.tagName.toLowerCase(),
          id: el.id || el.className.toString().split(' ')[0],
          top: Math.round(r.top + window.scrollY),
          h: Math.round(r.height),
        });
      });
      // horizontal overflow detection
      const overflow = [];
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width > 0 && (r.right > document.documentElement.clientWidth + 2 || r.left < -2)) {
          const cs = getComputedStyle(el);
          if (cs.position === 'fixed' || cs.display === 'none') return;
          overflow.push({
            sel: el.tagName.toLowerCase() + '.' + el.className.toString().split(' ').slice(0, 2).join('.'),
            left: Math.round(r.left), right: Math.round(r.right),
          });
        }
      });
      return {
        docH,
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
        sections: sec,
        overflow: overflow.slice(0, 20),
        fontLoaded: document.fonts ? document.fonts.status : 'n/a',
      };
    });

    report[vp.name] = { metrics, logs };
    console.log(`\n===== ${vp.name} (${vp.width}x${vp.height}) =====`);
    console.log(`doc height: ${metrics.docH}  scrollW: ${metrics.scrollW}  clientW: ${metrics.clientW}`);
    console.log('sections:');
    metrics.sections.forEach(s =>
      console.log(`  ${String(s.top).padStart(6)} +${String(s.h).padStart(5)}  ${s.tag}.${s.id}`));
    if (metrics.overflow.length) {
      console.log('H-OVERFLOW:');
      metrics.overflow.forEach(o => console.log(`  ${o.sel}  ${o.left}..${o.right}`));
    }
    if (logs.length) {
      console.log('CONSOLE:');
      logs.forEach(l => console.log('  ' + l));
    } else {
      console.log('CONSOLE: (clean)');
    }
    await page.close();
  }

  fs.writeFileSync(path.join(OUTDIR, 'report.json'), JSON.stringify(report, null, 2));
  await browser.close();
  console.log('\nDone. Screenshots in', OUTDIR);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
