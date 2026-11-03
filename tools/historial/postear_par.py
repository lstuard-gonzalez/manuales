import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
ids = [int(x) for x in sys.argv[2:]]
try:
    call('account.move', 'write', [ids, {'name': '/'}])
    call('account.move', 'action_post', [ids])
    print('con número nuevo')
except SystemExit as e:
    print('no se pudo limpiar el número, se devuelve al 29/11:', str(e)[:160])
    call('account.move', 'write', [ids, {'date': '2026-11-29'}])
    call('account.move', 'action_post', [ids])
rl = call('account.move.line', 'search_read', [[['move_id', 'in', ids], ['account_id.account_type', '=', 'asset_receivable'], ['reconciled', '=', False]]], {'fields': ['id']})
if rl: call('account.move.line', 'reconcile', [[l['id'] for l in rl]])
print(call('account.move', 'read', [ids], {'fields': ['name', 'date', 'state', 'ref']}))
print(call('account.move.line', 'search_read', [[['move_id', 'in', ids], ['account_id.account_type', '=', 'asset_receivable']]], {'fields': ['reconciled', 'amount_residual']}))
