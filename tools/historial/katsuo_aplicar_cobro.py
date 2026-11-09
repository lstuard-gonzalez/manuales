import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
call('account.move', 'write', [[43238], {'ref': 'Reversión de: E002-00016947, Facturada en fiscal: F002-00003845 y F002-00003846 (28/08)'}])
inv = call('account.move.line', 'search_read', [[['move_id', '=', 43251], ['account_id.account_type', '=', 'asset_receivable']]], {'fields': ['id']})[0]['id']
pl = call('account.move.line', 'read', [[138246]], {'fields': ['reconciled', 'amount_residual_currency', 'account_id', 'partner_id']})[0]
assert not pl['reconciled'] and abs(pl['amount_residual_currency'] + 120.31) < .005 and pl['partner_id'][0] == 117
call('account.move.line', 'reconcile', [[inv, 138246]])
for i in (43250, 43251, 43238, 17823):
    print(call('account.move', 'read', [[i]], {'fields': ['name', 'ref', 'payment_state', 'amount_residual', 'amount_total']}))
print(call('account.payment', 'search_read', [[['name', '=', 'PREGB/2026/00251']]], {'fields': ['state']}))
print(call('account.move', 'search_read', [[['journal_id.code', '=', 'EXCH'], ['create_date', '>=', '2026-11-09 18:00:00'], ['line_ids.partner_id', '=', 117]]], {'fields': ['name', 'amount_total']}))
