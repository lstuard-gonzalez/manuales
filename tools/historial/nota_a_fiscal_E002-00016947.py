import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None, ctx=None):
    c = {'lang': 'es_VE', 'tz': 'America/Caracas'}; c.update(ctx or {})
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context=c)})
NOTA, CXL, HOY = 17823, 43790, '2026-11-09'
n = call('account.move', 'read', [[NOTA]], {'fields': ['name', 'state', 'payment_state', 'amount_residual', 'journal_id', 'tax_today']})[0]
l = call('account.move.line', 'read', [[CXL]], {'fields': ['matched_credit_ids']})[0]
prs = call('account.partial.reconcile', 'read', [l['matched_credit_ids']], {'fields': ['credit_move_id', 'debit_amount_currency', 'exchange_move_id']})
print(n, prs)
assert n['name'] == 'E002-00016947' and n['state'] == 'posted' and len(prs) == 1 and 'PREGB/2026/00251' in prs[0]['credit_move_id'][1]
pay_line = prs[0]['credit_move_id'][0]
# 1. desaplicar el cobro de la nota
call('account.move.line', 'remove_move_reconcile', [[CXL]])
# 2. nota de crédito con el asistente, como E002-00005991
wid = call('account.move.reversal', 'create', [{'move_ids': [(6, 0, [NOTA])], 'reason': 'CAMBIO DE NOTA A FACTURA FISCAL', 'journal_id': n['journal_id'][0], 'date': HOY}], ctx={'active_model': 'account.move', 'active_ids': [NOTA]})
res = call('account.move.reversal', 'refund_moves', [[wid]], ctx={'active_model': 'account.move', 'active_ids': [NOTA]})
nc = res.get('res_id') or (res.get('domain') and call('account.move', 'search', [res['domain']])[0])
print('NC borrador', nc)
d = call('account.move', 'read', [[nc]], {'fields': ['name', 'ref', 'journal_id', 'date', 'invoice_date', 'amount_total', 'currency_id', 'tax_today', 'move_type', 'reversed_entry_id', 'state']})[0]
for x in call('account.move.line', 'search_read', [[['move_id', '=', nc]]], {'fields': ['account_id', 'name', 'quantity', 'price_unit', 'balance', 'amount_currency']}): print('   ', x)
print(d)
assert d['state'] == 'draft' and d['move_type'] == 'out_refund' and d['journal_id'][0] == 552 and abs(d['amount_total'] - 566.28) < .005 and d['reversed_entry_id'][0] == NOTA
call('account.move', 'action_post', [[nc]])
rl = call('account.move.line', 'search_read', [[['move_id', 'in', [NOTA, nc]], ['account_id.account_type', '=', 'asset_receivable'], ['reconciled', '=', False]]], {'fields': ['id']})
if len(rl) == 2: call('account.move.line', 'reconcile', [[x['id'] for x in rl]])
print('NC:', call('account.move', 'read', [[nc]], {'fields': ['name', 'ref', 'date', 'state', 'payment_state', 'amount_total', 'tax_today']}))
print('Nota:', call('account.move', 'read', [[NOTA]], {'fields': ['name', 'payment_state', 'amount_residual']}))
pl = call('account.move.line', 'read', [[pay_line]], {'fields': ['move_id', 'reconciled', 'amount_residual', 'amount_residual_currency']})
print('Cobro:', pl, call('account.payment', 'search_read', [[['name', '=', 'PREGB/2026/00251']]], {'fields': ['state', 'amount', 'currency_id']}))
print('EXCH:', call('account.move', 'search_read', [['|', ['name', '=', 'EXCH/2026/11/0576'], ['ref', 'ilike', 'EXCH/2026/11/0576']]], {'fields': ['name', 'state', 'ref', 'amount_total']}))
