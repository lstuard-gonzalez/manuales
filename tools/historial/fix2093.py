import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
rid = 40756
r = call('account.move', 'read', [[rid]], {'fields': ['date', 'tax_today', 'amount_total']})[0]
assert r['date'] == '2026-11-27'
pay = call('account.payment', 'read', [[3129]], {'fields': ['move_id', 'date', 'amount']})[0]
call('account.move', 'button_draft', [[rid]])
call('account.move', 'write', [[rid], {'invoice_date': '2026-10-27', 'date': '2026-10-27'}])
call('account.move', 'write', [[rid], {'tax_today': r['tax_today']}])
call('account.move', 'action_post', [[rid]])
pl = call('account.move.line', 'search_read', [['|', ['move_id', '=', rid], ['move_id', '=', pay['move_id'][0]], ['account_id.account_type', '=', 'liability_payable'], ['reconciled', '=', False]]], {'fields': ['id']})
if len(pl) == 2: call('account.move.line', 'reconcile', [[l['id'] for l in pl]])
print(call('account.move', 'read', [[rid]], {'fields': ['name', 'date', 'invoice_date', 'state', 'amount_total', 'tax_today', 'payment_state']}))
print(call('account.payment', 'read', [[3129]], {'fields': ['name', 'date', 'state', 'reconciled_bill_ids']}))
