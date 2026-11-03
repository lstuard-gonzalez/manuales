import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
s = call('account.bank.statement.line', 'search_read', [[['move_id.name', '=', 'BNK2/2026/01184']]], {'fields': ['id', 'move_id', 'amount', 'is_reconciled', 'statement_id', 'payment_ref']})[0]
print(s)
ls = call('account.move.line', 'search_read', [[['move_id', '=', s['move_id'][0]]]], {'fields': ['matched_debit_ids', 'matched_credit_ids']})
assert not s['is_reconciled'] and s['statement_id'][0] == 41 and s['payment_ref'] == '50319205' and not any(l['matched_debit_ids'] or l['matched_credit_ids'] for l in ls)
call('account.bank.statement.line', 'write', [[s['id']], {'statement_id': False}]); call('account.bank.statement.line', 'unlink', [[s['id']]])
print('quedan:', call('account.bank.statement.line', 'search_count', [[['id', '=', s['id']]]]), call('account.move', 'search_count', [[['id', '=', s['move_id'][0]]]]))
