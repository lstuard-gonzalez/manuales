import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
s = call('account.bank.statement.line', 'search_read', [[['move_id.name', '=', 'BNK2/2026/01331']]], {'fields': ['id', 'statement_id', 'amount', 'payment_ref']})[0]
assert s['statement_id'][0] == 41 and s['payment_ref'] == '52330388'
call('account.bank.statement.line', 'action_undo_reconciliation', [[s['id']]])
for l in call('account.move.line', 'search_read', [[['move_id.name', '=', 'BNK2/2026/01331']]], {'fields': ['account_id', 'balance', 'matched_debit_ids', 'matched_credit_ids']}): print(l)
print(call('account.payment', 'search_read', [[['name', '=', 'PBNK2/2026/00196']]], {'fields': ['state']}))
