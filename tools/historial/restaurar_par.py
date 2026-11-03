import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
ms = call('account.move', 'search_read', [[['name', 'in', ['EXCH/2026/11/0005', 'EXCH/2026/11/0027']]]], {'fields': ['id', 'name', 'date', 'state']})
print('antes:', ms)
ids = [m['id'] for m in ms if m['state'] == 'draft']
if ids: call('account.move', 'action_post', [ids])
rl = call('account.move.line', 'search_read', [[['move_id', 'in', [m['id'] for m in ms]], ['account_id.account_type', '=', 'asset_receivable'], ['reconciled', '=', False]]], {'fields': ['id']})
if rl: call('account.move.line', 'reconcile', [[l['id'] for l in rl]])
print('después:', call('account.move', 'read', [[m['id'] for m in ms]], {'fields': ['name', 'date', 'state']}), call('account.move.line', 'search_read', [[['move_id', 'in', [m['id'] for m in ms]], ['account_id.account_type', '=', 'asset_receivable']]], {'fields': ['reconciled', 'amount_residual']}))
