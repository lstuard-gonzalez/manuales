import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
pay_line, inv_line, exch_name = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
antes = call('account.move', 'search_read', [[['journal_id.name', '=', 'DIFERENCIA EN CAMBIO BENEFICIO']]], {'fields': ['id'], 'order': 'id desc', 'limit': 1})[0]['id']
pl = call('account.move.line', 'read', [[pay_line]], {'fields': ['matched_debit_ids', 'matched_credit_ids']})[0]
prs = call('account.partial.reconcile', 'read', [pl['matched_debit_ids'] + pl['matched_credit_ids']], {'fields': ['debit_move_id', 'credit_move_id', 'exchange_move_id']})
assert all((pr['exchange_move_id'] and pr['exchange_move_id'][1].startswith(exch_name)) or exch_name in (pr['debit_move_id'][1] + pr['credit_move_id'][1]) for pr in prs), prs
call('account.move.line', 'remove_move_reconcile', [[pay_line]])
call('account.move.line', 'reconcile', [[inv_line, pay_line]])
nuevos = call('account.move', 'search_read', [[['id', '>', antes], ['journal_id.name', '=', 'DIFERENCIA EN CAMBIO BENEFICIO']]], {'fields': ['name', 'date', 'ref', 'reversed_entry_id', 'amount_total']})
print('nuevos EXCH:', nuevos)
for lid in (pay_line, inv_line):
    print(call('account.move.line', 'read', [[lid]], {'fields': ['move_id', 'amount_residual', 'amount_residual_currency', 'reconciled']}))
