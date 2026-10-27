exec(open('po.py').read().split("READ =")[0])
import json
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
lc = call('stock.landed.cost', 'read', [[120]], {'fields': ['state', 'write_uid', 'amount_total']})[0]
adj = call('stock.valuation.adjustment.lines', 'search_read', [[['cost_id', '=', 120]]], {'fields': ['product_id', 'additional_landed_cost']})
ln = call('stock.landed.cost.lines', 'read', [[293]], {'fields': ['price_unit', 'account_id']})[0]
print(lc, adj, ln)
assert lc['state'] == 'draft' and lc['write_uid'][0] == 2 and abs(lc['amount_total'] - 55015835.14) < 0.005
assert {a['product_id'][0]: a['additional_landed_cost'] for a in adj} == {1321: 9556886.94, 278: 45458948.2}
assert ln['account_id'][0] == 538
print('validate ->', call('stock.landed.cost', 'button_validate', [[120]]))
lc = call('stock.landed.cost', 'read', [[120]], {'fields': ['name', 'state', 'account_move_id', 'amount_total']})[0]
p(lc)
p(call('account.move', 'read', [[lc['account_move_id'][0]]], {'fields': ['name', 'state', 'date', 'journal_id', 'amount_total']}))
p(call('account.move.line', 'search_read', [[['move_id', '=', lc['account_move_id'][0]]]], {'fields': ['account_id', 'product_id', 'debit', 'credit', 'debit_usd', 'credit_usd']}))
p(call('product.product', 'read', [[278, 1321]], {'fields': ['display_name', 'standard_price', 'qty_available']}))
