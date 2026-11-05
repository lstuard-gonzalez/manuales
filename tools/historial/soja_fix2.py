import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
MID, SUSP, INVL, CXC, GAIN, SOJA = 31615, 135088, 43366, 387, 263, 693
inv = call('account.move.line', 'read', [[INVL]], {'fields': ['balance', 'amount_residual', 'amount_residual_currency', 'reconciled']})[0]
sl = call('account.move.line', 'read', [[SUSP]], {'fields': ['balance', 'account_id', 'reconciled']})[0]
assert not inv['reconciled'] and abs(inv['amount_residual'] - 175162.93) < .005 and abs(inv['amount_residual_currency'] - 203.9) < .005, inv
assert sl['account_id'][0] == 454 and abs(sl['balance'] + 206754.6) < .005, sl
cxc = inv['amount_residual']; gain = round(206754.6 - cxc, 2)
ref = 'FACT 19151 (E001-00017172) pagada a 1.014,00 Bs/$'
call('account.move', 'button_draft', [[MID]])
call('account.move', 'write', [[MID], {'line_ids': [
    (1, SUSP, {'account_id': CXC, 'partner_id': SOJA, 'credit': cxc, 'debit': 0.0, 'amount_currency': -cxc, 'name': ref}),
    (0, 0, {'account_id': GAIN, 'partner_id': SOJA, 'credit': gain, 'debit': 0.0, 'amount_currency': -gain, 'currency_id': 166, 'name': 'Diferencial cambiario: ' + ref})]}])
ls = call('account.move.line', 'search_read', [[['move_id', '=', MID]]], {'fields': ['account_id', 'balance', 'currency_id', 'amount_currency']})
for l in ls: print(l)
assert abs(sum(l['balance'] for l in ls)) < .005 and len(ls) == 3
call('account.move', 'action_post', [[MID]])
cl = [l['id'] for l in ls if l['account_id'][0] == CXC][0]
call('account.move.line', 'reconcile', [[INVL, cl]])
print(call('account.move', 'read', [[MID]], {'fields': ['name', 'state', 'date']}))
print(call('account.bank.statement.line', 'read', [[9592]], {'fields': ['is_reconciled']}))
print('factura:', call('account.move', 'read', [[17611]], {'fields': ['payment_state', 'amount_residual']}))
print(call('account.move.line', 'read', [[INVL, cl]], {'fields': ['reconciled', 'amount_residual', 'amount_residual_currency']}))
print('EXCH nuevos:', call('account.move', 'search_read', [[['journal_id.code', '=', 'EXCH'], ['create_date', '>=', '2026-11-05 00:00:00'], ['line_ids.partner_id', '=', SOJA]]], {'fields': ['name', 'amount_total']}))
