const { chromium } = require('playwright');
const BASE = 'https://alimentos-monteverde.odoo.com';
async function open() {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1600, height: 1000 }, locale: 'es-VE', storageState: 'state.json' });
  const p = await ctx.newPage();
  return { b, ctx, p };
}
async function go(p, path) {
  await p.goto(BASE + path, { waitUntil: 'load', timeout: 60000 });
  await p.waitForSelector('.o_action_manager .o_action, .o_action_manager > div', { timeout: 60000 });
  await p.waitForTimeout(2500);
}
module.exports = { open, go, BASE };
