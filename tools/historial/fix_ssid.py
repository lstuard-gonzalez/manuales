import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
SSID, PERD, JRN = 438, 253, 429
casos = {c['st']: c for c in json.load(open('casos.json'))}
def uno(st):
    c = casos[st]
    sl = call('account.move.line', 'read', [[c['ssid_line']['id']]], {'fields': ['amount_residual', 'reconciled']})[0]
    tl = call('account.move.line', 'read', [[c['tr_line']['id']]], {'fields': ['amount_residual', 'amount_residual_currency', 'reconciled', 'currency_id', 'account_id', 'partner_id']})[0]
    assert not sl['reconciled'] and not tl['reconciled'] and abs(sl['amount_residual'] - c['ssid_line']['balance']) < .005 and abs(tl['amount_residual'] - c['tr_line']['balance']) < .005, (sl, tl)
    dep = -sl['amount_residual']          # monto del depósito (Bs)
    cob = tl['amount_residual']           # monto del cobro en la transitoria (Bs)
    dif = round(cob - dep, 2)
    assert 0 <= dif <= 1, dif
    usd = tl['currency_id'][0] == 1
    ref = 'Identificación %s ref. %s - %s' % (st, c['pay_rec']['memo'], c['pay'])
    tr = {'account_id': tl['account_id'][0], 'partner_id': tl['partner_id'][0], 'name': ref, 'debit': 0.0, 'credit': cob}
    if usd: tr.update(currency_id=1, amount_currency=-tl['amount_residual_currency'])
    lines = [(0, 0, {'account_id': SSID, 'name': ref, 'debit': dep, 'credit': 0.0}), (0, 0, tr)]
    if dif: lines.append((0, 0, {'account_id': PERD, 'partner_id': tl['partner_id'][0], 'name': 'Diferencia cobro vs depósito ' + c['pay'], 'debit': dif, 'credit': 0.0}))
    vals = {'move_type': 'entry', 'journal_id': JRN, 'date': c['ssid_line']['date'], 'ref': ref, 'line_ids': lines}
    if usd: vals['tax_today'] = c['pay_rec']['tax_today']
    mid = call('account.move', 'create', [vals])
    chk = call('account.move.line', 'search_read', [[['move_id', '=', mid]]], {'fields': ['account_id', 'debit', 'credit', 'amount_currency', 'currency_id', 'partner_id']})
    exp = {SSID: (dep, 0.0), tl['account_id'][0]: (0.0, cob)}
    if dif: exp[PERD] = (dif, 0.0)
    good = len(chk) == len(exp) and all(abs(l['debit'] - exp[l['account_id'][0]][0]) < .005 and abs(l['credit'] - exp[l['account_id'][0]][1]) < .005 for l in chk)
    if usd: good = good and any(l['currency_id'][0] == 1 and abs(l['amount_currency'] + tl['amount_residual_currency']) < .005 for l in chk)
    if not good:
        call('account.move', 'unlink', [[mid]]); print('BORRADOR NO CUADRA, eliminado', chk); return False
    call('account.move', 'action_post', [[mid]])
    ns = [l['id'] for l in call('account.move.line', 'search_read', [[['move_id', '=', mid], ['account_id', '=', SSID]]], {'fields': ['id']})]
    nt = [l['id'] for l in call('account.move.line', 'search_read', [[['move_id', '=', mid], ['account_id', '=', tl['account_id'][0]]]], {'fields': ['id']})]
    call('account.move.line', 'reconcile', [[c['ssid_line']['id']] + ns])
    call('account.move.line', 'reconcile', [[c['tr_line']['id']] + nt])
    m = call('account.move', 'read', [[mid]], {'fields': ['name', 'date', 'state']})[0]
    r = call('account.move.line', 'read', [[c['ssid_line']['id'], c['tr_line']['id']] + ns + nt], {'fields': ['reconciled', 'amount_residual']})
    p = call('account.payment', 'read', [[c['pay_rec']['id']]], {'fields': ['name', 'state']})[0]
    ok = m['state'] == 'posted' and all(x['reconciled'] for x in r) and p['state'] == 'paid'
    print('OK ' if ok else 'REVISAR', st, '->', m['name'], m['date'], '| depósito', dep, 'cobro', cob, 'dif', dif, '|', p['name'], p['state'])
    return ok
for st in sys.argv[2:]:
    if not uno(st): print('Se detiene.'); break
