import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
MID, CL, INVL = 31615, 135088, 43366
call('account.move.line', 'remove_move_reconcile', [[CL]])
print('tras deshacer:', call('account.move.line', 'read', [[INVL, CL]], {'fields': ['reconciled', 'amount_residual', 'amount_residual_currency']}))
print('EXCH 2422:', call('account.move', 'search_read', [['|', ['name', '=', 'EXCH/2026/10/2422'], ['ref', 'ilike', 'EXCH/2026/10/2422']]], {'fields': ['name', 'state', 'ref']}))
call('account.move', 'button_draft', [[MID]])
call('account.move', 'write', [[MID], {'line_ids': [(1, CL, {'currency_id': 1, 'amount_currency': -203.9, 'credit': 175162.93, 'debit': 0.0})]}])
ls = call('account.move.line', 'search_read', [[['move_id', '=', MID]]], {'fields': ['account_id', 'balance', 'currency_id', 'amount_currency']})
for l in ls: print(l)
c = [l for l in ls if l['id'] == CL][0]
assert c['currency_id'][0] == 1 and abs(c['amount_currency'] + 203.9) < .005 and abs(c['balance'] + 175162.93) < .005 and abs(sum(l['balance'] for l in ls)) < .005
call('account.move', 'action_post', [[MID]])
call('account.move.line', 'reconcile', [[INVL, CL]])
print(call('account.move', 'read', [[MID]], {'fields': ['name', 'state', 'date']}), call('account.bank.statement.line', 'read', [[9592]], {'fields': ['is_reconciled']}))
print('factura:', call('account.move', 'read', [[17611]], {'fields': ['payment_state', 'amount_residual']}))
print(call('account.move.line', 'read', [[INVL, CL]], {'fields': ['reconciled', 'amount_residual', 'amount_residual_currency']}))
print('EXCH de SOJA creados hoy:', call('account.move', 'search_read', [[['journal_id.code', '=', 'EXCH'], ['create_date', '>=', '2026-11-05 00:00:00'], ['line_ids.partner_id', '=', 693]]], {'fields': ['name', 'amount_total', 'ref', 'state']}))
