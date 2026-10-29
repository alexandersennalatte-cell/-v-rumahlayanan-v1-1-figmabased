/* Print geometry of key hero/header elements at 1440px. */
const puppeteer = require('puppeteer-core');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PAGE = 'file:///K:/Newfolder/index.html';

const SELS = [
  '.topbar', '.topbar__inner', '.header', '.header__inner',
  '.logo', '.logo__mark', '.logo__title', '.nav', '.nav__link',
  '.hero', '.hero__inner', '.hero__copy', '.hero__title', '.hero__lead',
  '.search', '.search__hints', '.hero__actions',
  '.hero__media', '.hero__photo', '.hero__card',
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars',
      '--allow-file-access-from-files', '--force-color-profile=srgb'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1 });
  await page.goto(PAGE, { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 800));

  const out = await page.evaluate((sels) => {
    const res = [];
    for (const s of sels) {
      document.querySelectorAll(s).forEach((el, i) => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        res.push({
          sel: s + (i ? '#' + i : ''),
          x: Math.round(r.left), y: Math.round(r.top + window.scrollY),
          w: Math.round(r.width), h: Math.round(r.height),
          fs: cs.fontSize, lh: cs.lineHeight, ff: cs.fontFamily.split(',')[0].replace(/"/g, ''),
          mt: cs.marginTop, mb: cs.marginBottom, pad: cs.padding,
        });
      });
    }
    return res;
  }, SELS);

  console.log('sel'.padEnd(22), 'x'.padStart(6), 'y'.padStart(6), 'w'.padStart(6), 'h'.padStart(5),
    ' fs'.padStart(8), ' lh'.padStart(7), '  font');
  out.forEach(o => {
    console.log(o.sel.padEnd(22), String(o.x).padStart(6), String(o.y).padStart(6),
      String(o.w).padStart(6), String(o.h).padStart(5),
      o.fs.padStart(8), o.lh.padStart(7), ' ' + o.ff);
  });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
