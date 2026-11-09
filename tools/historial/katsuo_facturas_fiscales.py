import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
PUENTE, IVA16, IVA8, KATSUO = 2902, 59, 3, 117
FACTS = [
    ('F002-00003845', '00-008318', 426.71, [(152.74, IVA16, '16 %'), (231.05, IVA8, '8 %')]),
    ('F002-00003846', '00-008319', 139.57, [(120.32, IVA16, '16 %')]),
]
assert not call('account.move', 'search', [[['name', 'in', [f[0] for f in FACTS]]]])
ids = []
for name, ctrl, total, bases in FACTS:
    fis = name[-8:]
    vals = {'move_type': 'out_invoice', 'journal_id': 456, 'name': name, 'partner_id': KATSUO, 'date': '2026-09-30', 'invoice_date': '2026-08-28',
            'invoice_payment_term_id': 11, 'invoice_user_id': 10, 'currency_id': 1, 'ref': 'APER0930 CXC FACT 38695', 'nro_ctrl': ctrl, 'tax_today': 791.6667,
            'narration': '<p>Factura fiscal %s, control %s (Profit 38695, nota 16947), 28/08/2026.</p>' % (fis, ctrl),
            'invoice_line_ids': [(0, 0, {'account_id': PUENTE, 'name': 'Factura fiscal %s · FACT 38695 (Profit) · base IVA %s' % (fis, lbl), 'quantity': 1, 'price_unit': b, 'tax_ids': [(6, 0, [t])]}) for b, t, lbl in bases]}
    mid = call('account.move', 'create', [vals])
    m = call('account.move', 'read', [[mid]], {'fields': ['name', 'state', 'amount_untaxed', 'amount_tax', 'amount_total', 'tax_today', 'nro_ctrl', 'invoice_date_due']})[0]
    print('borrador', m)
    if abs(m['amount_total'] - total) > .005 or m['tax_today'] != 791.6667:
        call('account.move', 'unlink', [[mid]]); raise SystemExit('no cuadra, borrador eliminado')
    call('account.move', 'action_post', [[mid]])
    m = call('account.move', 'read', [[mid]], {'fields': ['name', 'state', 'date', 'invoice_date', 'amount_total', 'amount_total_signed', 'payment_state', 'nks_sucursal_id', 'journal_id']})[0]
    print('publicada', m)
    for l in call('account.move.line', 'search_read', [[['move_id', '=', mid]]], {'fields': ['account_id', 'name', 'balance', 'amount_currency', 'tax_line_id']}): print('    ', l['account_id'][1][:28], '|', l['name'], l['balance'], l['amount_currency'])
    assert m['name'] == name and m['state'] == 'posted'
    ids.append(mid)
print('IDS', ids)
