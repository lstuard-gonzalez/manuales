const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file:///home/user/odoo-alimentos-monteverde/docs/manuales/costo-en-destino/index.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.querySelectorAll('img[loading]').forEach(i => i.removeAttribute('loading')));
  await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
  await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: 'print', colorScheme: 'light' });
  await p.pdf({
    path: '/home/user/odoo-alimentos-monteverde/docs/manuales/costo-en-destino/Manual-Costos-en-Destino-AMV.pdf',
    format: 'Letter', printBackground: true,
    margin: { top: '18mm', bottom: '16mm', left: '14mm', right: '14mm' },
    displayHeaderFooter: true,
    headerTemplate: '<div style="width:100%;height:4px;background:#ff8c00;margin-top:-18mm;-webkit-print-color-adjust:exact"></div>',
    footerTemplate: '<div style="width:100%;font:8px Arial,sans-serif;color:#898989;padding:0 14mm;display:flex;justify-content:space-between"><span>NIKKOSOFT Consultores C.A. · Costos en destino · Alimentos MonteVerde C.A.</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  await b.close();
})();
