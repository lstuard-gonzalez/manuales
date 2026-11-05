import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
st = call('account.bank.statement.line', 'read', [[9592]], {'fields': ['move_id', 'amount', 'is_reconciled', 'payment_ref']})[0]
assert st['payment_ref'] == '20418507667' and st['amount'] == 206754.6 and not st['is_reconciled'], st
call('account.bank.statement.line', 'action_undo_reconciliation', [[9592]])
for l in call('account.move.line', 'search_read', [[['move_id', '=', st['move_id'][0]]]], {'fields': ['account_id', 'partner_id', 'balance', 'currency_id', 'reconciled']}): print(l)
print('factura:', call('account.move', 'read', [[17611]], {'fields': ['payment_state', 'amount_residual']}))
print('EXCH 2215:', call('account.move', 'search_read', [['|', ['name', '=', 'EXCH/2026/10/2215'], ['ref', 'ilike', 'EXCH/2026/10/2215']]], {'fields': ['name', 'state', 'date', 'ref', 'reversed_entry_id']}))
