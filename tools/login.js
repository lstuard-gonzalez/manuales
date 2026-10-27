const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1600, height: 1000 }, locale: 'es-VE' });
  const p = await ctx.newPage();
  await p.goto('https://alimentos-monteverde.odoo.com/web/login', { waitUntil: 'load' });
  await p.fill('input[name=login]', process.env.U);
  await p.fill('input[name=password]', process.env.P);
  await Promise.all([p.waitForURL(/\/odoo/, { timeout: 60000 }), p.click('button[type=submit]')]);
  await ctx.storageState({ path: 'state.json' });
  console.log('ok', p.url());
  await b.close();
})();
