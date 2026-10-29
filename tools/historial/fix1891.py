exec(open('po.py').read().split("READ =")[0])
import json
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
l = call('account.move.line', 'read', [[29667]], {'fields': ['amount_residual_currency', 'amount_residual', 'reconciled', 'partner_id', 'account_id']})[0]
assert l['amount_residual_currency'] == -0.015 and l['amount_residual'] == -12.74 and not l['reconciled'], l
acc = call('account.account', 'search_read', [[['code', '=', '8.1.01.0006']]], {'fields': ['id', 'name']})[0]['id']
ref = 'Redondeo pago PZELBI/2026/00135 - FACT 1891 MESAMAR'
mid = call('account.move', 'create', [{'move_type': 'entry', 'journal_id': 66, 'date': '2026-10-29', 'ref': ref, 'line_ids': [
    (0, 0, {'account_id': 71, 'partner_id': 2821, 'name': ref, 'debit': 12.74, 'credit': 0.0, 'currency_id': 1, 'amount_currency': 0.015}),
    (0, 0, {'account_id': acc, 'partner_id': 2821, 'name': ref, 'debit': 0.0, 'credit': 12.74, 'currency_id': 1, 'amount_currency': -0.015}),
]}])
print('move', mid)
call('account.move', 'action_post', [[mid]])
nl = call('account.move.line', 'search_read', [[['move_id', '=', mid], ['account_id', '=', 71]]], {'fields': ['id']})[0]['id']
call('account.move.line', 'reconcile', [[29667, nl]])
p(call('account.move', 'read', [[mid]], {'fields': ['name', 'state', 'date', 'journal_id', 'amount_total']}))
p(call('account.move.line', 'search_read', [[['move_id', '=', mid]]], {'fields': ['account_id', 'debit', 'credit', 'amount_currency', 'reconciled']}))
p(call('account.move', 'read', [[11794]], {'fields': ['name', 'payment_state', 'amount_residual', 'amount_residual_usd']}))
p(call('account.move.line', 'read', [[29667]], {'fields': ['amount_residual_currency', 'amount_residual', 'reconciled', 'full_reconcile_id']}))
