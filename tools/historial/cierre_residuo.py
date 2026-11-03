import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
inv_line, fecha, ref = int(sys.argv[2]), sys.argv[3], sys.argv[4]
l = call('account.move.line', 'read', [[inv_line]], {'fields': ['partner_id', 'account_id', 'amount_residual', 'amount_residual_currency', 'currency_id', 'move_id']})[0]
bs, usd = round(l['amount_residual'], 2), round(l['amount_residual_currency'], 4)
assert 0 < bs < 10000 and l['currency_id'][1] == 'USD', l
perd = call('account.account', 'search_read', [[['code', '=', '8.2.01.0007']]], {'fields': ['id']})[0]['id']
mid = call('account.move', 'create', [{'move_type': 'entry', 'journal_id': 66, 'date': fecha, 'ref': ref, 'line_ids': [
    (0, 0, {'account_id': l['account_id'][0], 'partner_id': l['partner_id'][0], 'name': ref, 'debit': 0.0, 'credit': bs, 'currency_id': 1, 'amount_currency': -usd}),
    (0, 0, {'account_id': perd, 'partner_id': l['partner_id'][0], 'name': ref, 'debit': bs, 'credit': 0.0, 'currency_id': 1, 'amount_currency': usd})]}])
call('account.move', 'action_post', [[mid]])
nl = call('account.move.line', 'search_read', [[['move_id', '=', mid], ['account_id', '=', l['account_id'][0]]]], {'fields': ['id']})[0]['id']
call('account.move.line', 'reconcile', [[inv_line, nl]])
print(call('account.move', 'read', [[mid]], {'fields': ['name', 'date', 'state', 'amount_total']}))
print(call('account.move', 'read', [[l['move_id'][0]]], {'fields': ['name', 'payment_state', 'amount_residual', 'amount_residual_usd']}))
