import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
NUEVA = '2026-10-29'
def par(orig_name):
    o = call('account.move', 'search_read', [[['name', '=', orig_name]]], {'fields': ['id', 'date', 'reversal_move_ids']})[0]
    assert o['date'] == '2026-11-29' and len(o['reversal_move_ids']) == 1, o
    ids = [o['id'], o['reversal_move_ids'][0]]
    lines = call('account.move.line', 'search_read', [[['move_id', 'in', ids]]], {'fields': ['id', 'account_id', 'balance', 'matched_debit_ids', 'matched_credit_ids', 'account_type' if False else 'reconciled']})
    # solo deben estar conciliadas entre ellas
    rec_lines = [l for l in lines if l['matched_debit_ids'] or l['matched_credit_ids']]
    prs = call('account.partial.reconcile', 'read', [sum([l['matched_debit_ids'] + l['matched_credit_ids'] for l in rec_lines], [])], {'fields': ['debit_move_id', 'credit_move_id', 'exchange_move_id']})
    lids = {l['id'] for l in lines}
    assert all(pr['debit_move_id'][0] in lids and pr['credit_move_id'][0] in lids and not pr['exchange_move_id'] for pr in prs), prs
    rec_ids = [l['id'] for l in rec_lines]
    call('account.move', 'button_draft', [ids])
    call('account.move', 'write', [ids, {'date': NUEVA}])
    call('account.move', 'write', [ids, {'name': '/'}])
    call('account.move', 'action_post', [ids])
    abiertas = [l['id'] for l in call('account.move.line', 'read', [rec_ids], {'fields': ['reconciled']}) if not l['reconciled']]
    if abiertas: call('account.move.line', 'reconcile', [abiertas])
    nuevo = call('account.move', 'read', [[ids[0]]], {'fields': ['name']})[0]['name']
    call('account.move', 'write', [[ids[1]], {'ref': 'Reversión de: %s' % nuevo}])
    r = call('account.move', 'read', [ids], {'fields': ['name', 'date', 'state', 'amount_total']})
    chk = call('account.move.line', 'read', [rec_ids], {'fields': ['reconciled', 'amount_residual']})
    ok = all(x['date'] == NUEVA and x['state'] == 'posted' for x in r) and all(c['reconciled'] and abs(c['amount_residual']) < 0.005 for c in chk)
    print('OK ' if ok else 'REVISAR', orig_name, '->', [(x['name'], x['date'], x['state'], x['amount_total']) for x in r])
    return ok
for n in sys.argv[2:]:
    if not par(n): print('Se detiene.'); break
