// Captura de pantallas SOLO LECTURA: navega, cambia de pestaña y dibuja recuadros en el DOM local.
const { open, go } = require('./lib');
const fs = require('fs');
const COLOR = '#E8501B';
async function overlay(p, rects) {
  await p.evaluate(({ rects, COLOR }) => {
    rects.forEach((r, i) => {
      const d = document.createElement('div');
      d.className = 'nks-hl';
      Object.assign(d.style, { position: 'absolute', left: (r.x - 6 + scrollX) + 'px', top: (r.y - 5 + scrollY) + 'px', width: (r.w + 12) + 'px', height: (r.h + 10) + 'px', border: `3px solid ${COLOR}`, borderRadius: '8px', zIndex: 99999, pointerEvents: 'none', boxShadow: '0 0 0 4px rgba(232,80,27,.18)' });
      if (r.n) {
        const b = document.createElement('div');
        b.textContent = r.n;
        Object.assign(b.style, { position: 'absolute', left: '-16px', top: '-16px', width: '26px', height: '26px', borderRadius: '50%', background: COLOR, color: '#fff', font: '700 14px/26px Inter, Arial, sans-serif', textAlign: 'center' });
        d.appendChild(b);
      }
      document.body.appendChild(d);
    });
  }, { rects, COLOR });
}
async function rectsFor(p, step) {
  return p.evaluate((step) => {
    const vis = (e) => e && e.offsetParent !== null && e.getBoundingClientRect().width > 0;
    const union = (els) => {
      els = els.filter(vis);
      if (!els.length) return null;
      const bs = els.map((e) => e.getBoundingClientRect());
      const x = Math.min(...bs.map((b) => b.left)), y = Math.min(...bs.map((b) => b.top));
      return { x, y, w: Math.max(...bs.map((b) => b.right)) - x, h: Math.max(...bs.map((b) => b.bottom)) - y };
    };
    const out = [];
    (step.fields || []).forEach((f, i) => {
      const [name, n, mode] = Array.isArray(f) ? f : [f, null];
      const w = [...document.querySelectorAll(`.o_form_view div.o_field_widget[name="${name}"], .o_setting_box div.o_field_widget[name="${name}"]`)].find(vis);
      if (!w) { out.push({ miss: name }); return; }
      const cell = mode === 'row' ? (w.closest('.row') || w) : mode === 'w' ? w : (w.closest('.o_cell') || w.closest('.o_setting_box') || w);
      const els = [cell];
      const prev = cell.previousElementSibling;
      if (cell.classList.contains('o_cell') && prev && prev.classList.contains('o_wrap_label')) els.push(prev);
      const r = union(els); if (r) { r.n = n; out.push(r); }
    });
    (step.cols || []).forEach((f) => {
      const [name, n] = Array.isArray(f) ? f : [f, null];
      const ths = [...document.querySelectorAll(`th[data-name="${name}"]`)].filter(vis);
      if (!ths.length) { out.push({ miss: name }); return; }
      const th = ths[0], table = th.closest('table');
      const idx = [...th.parentElement.children].indexOf(th);
      const tds = [...table.querySelectorAll('tbody tr')].map((tr) => tr.children[idx]).filter((td) => td && td.colSpan === 1 && td.textContent.trim());
      const r = union([th, ...tds]); r.n = n; out.push(r);
    });
    (step.texts || []).forEach((f) => {
      const [txt, n, sel] = f;
      const els = [...document.querySelectorAll(sel || 'button, a, .o_setting_box, label, span, div, td')].filter((e) => vis(e) && e.textContent.trim() === txt);
      if (!els.length) { out.push({ miss: txt }); return; }
      const r = union([els[0]]); r.n = n; out.push(r);
    });
    (step.sels || []).forEach((f) => {
      const [sel, n] = f;
      const r = union([...document.querySelectorAll(sel)].filter(vis).slice(0, 1));
      if (!r) { out.push({ miss: sel }); return; }
      r.n = n; out.push(r);
    });
    return out;
  }, step);
}
(async () => {
  const steps = JSON.parse(fs.readFileSync(process.argv[2]));
  const { b, p } = await open();
  for (const s of steps) {
    if (s.go) await go(p, s.go);
    if (s.hideChatter) { await p.addStyleTag({ content: '.o-mail-ChatterContainer, .o-mail-Form-chatter{display:none!important}' }); await p.waitForTimeout(500); }
    if (s.tab) { await p.locator('.o_notebook .nav-link', { hasText: s.tab }).first().click(); await p.waitForTimeout(1200); }
    for (const a of (s.actions || [])) {
      if (a.click) await p.locator(a.click).first().click();
      if (a.clickText) await p.locator(a.clickText[1] || 'body').getByText(a.clickText[0], { exact: true }).first().click();
      if (a.esc) await p.keyboard.press('Escape');
      if (a.fill) await p.locator(a.fill[0]).first().fill(a.fill[1]);
      if (a.press) await p.keyboard.press(a.press);
      await p.waitForTimeout(a.wait || 900);
    }
    if (s.scrollText) { await p.getByText(s.scrollText, { exact: true }).first().scrollIntoViewIfNeeded(); await p.evaluate(() => { const m = document.querySelector('.o_content'); if (m) m.scrollBy(0, -120); }); await p.waitForTimeout(800); }
    if (s.wait) await p.waitForTimeout(s.wait);
    await p.evaluate(() => document.querySelectorAll('.nks-hl').forEach((e) => e.remove()));
    const rects = await rectsFor(p, s);
    const miss = rects.filter((r) => r.miss);
    if (miss.length) console.log('MISS', s.shot, JSON.stringify(miss));
    await overlay(p, rects.filter((r) => !r.miss));
    if (s.shot) {
      const opt = { path: `shots/${s.shot}.png` };
      if (s.clip) opt.clip = s.clip;
      await p.screenshot(opt);
      console.log('OK', s.shot);
    }
    if (s.dump) console.log((await p.locator(s.dump).first().innerText()).slice(0, 2500));
  }
  await b.close();
})();
