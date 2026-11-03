import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
m = call('account.move', 'search_read', [[['name', '=', 'APER/2026/10/0001']]], {'fields': ['id', 'amount_total', 'state', 'line_ids']})[0]
ls = call('account.move.line', 'read', [m['line_ids']], {'fields': ['debit', 'credit', 'matched_debit_ids', 'matched_credit_ids', 'full_reconcile_id']})
assert m['amount_total'] == 0 and all(l['debit'] == 0 and l['credit'] == 0 for l in ls), ls
print('partials:', [(l['matched_debit_ids'], l['matched_credit_ids'], l['full_reconcile_id']) for l in ls])
last = call('account.move', 'search_read', [[['journal_id', '=', call('account.move', 'read', [[m['id']]], {'fields': ['journal_id']})[0]['journal_id'][0]], ['name', 'like', 'APER/2026/10/']]], {'fields': ['name']})
print('APER de octubre:', [x['name'] for x in last])
call('account.move', 'button_draft', [[m['id']]])
try:
    call('account.move', 'unlink', [[m['id']]]); print('eliminado')
except SystemExit as e:
    print('no se pudo eliminar:', str(e)[:200]); call('account.move', 'button_cancel', [[m['id']]])
    print(call('account.move', 'read', [[m['id']]], {'fields': ['name', 'state']}))
