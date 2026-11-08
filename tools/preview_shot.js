// Screenshot helper for hwpx_preview.py: node preview_shot.js page.html out.png scale
const { chromium } = require('playwright');

(async () => {
  const [html, out, scale] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: Number(scale) * 0.75, viewport: { width: 820, height: 1200 } });
  await page.goto('file://' + html);
  const info = await page.evaluate(() => {
    const px = 96 / 72;
    const flow = document.getElementById('flow').getBoundingClientRect();
    const pageBox = document.getElementById('page').getBoundingClientRect();
    return { flow_bottom_pt: flow.bottom / px, limit_pt: window.PAGE.limit, height_pt: pageBox.height / px };
  });
  await page.locator('#page').screenshot({ path: out });
  await browser.close();
  process.stdout.write(JSON.stringify(info));
})();
