exec(open('po.py').read().split("READ =")[0])
import json
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
lc = call('stock.landed.cost', 'read', [[120]], {'fields': ['state', 'write_date']})[0]
assert lc['state'] == 'draft' and lc['write_date'] == '2026-10-26 19:28:50', lc
# 1. línea de costo
call('stock.landed.cost.lines', 'write', [[293], {'currency_price_unit': 62078.71, 'price_unit': 55015835.14, 'account_id': 538}])
# 2. Compute
call('stock.landed.cost', 'compute_landed_cost', [[120]])
adj = call('stock.valuation.adjustment.lines', 'search_read', [[['cost_id', '=', 120]]], {'fields': ['product_id', 'additional_landed_cost']})
p(adj)
# 3. reparto del costeo
monto = {1321: 9556886.94, 278: 45458948.20}
for a in adj:
    call('stock.valuation.adjustment.lines', 'write', [[a['id']], {'additional_landed_cost': monto[a['product_id'][0]]}])
p(call('stock.landed.cost', 'read', [[120]], {'fields': ['name', 'state', 'amount_total', 'currency_id']}))
p(call('stock.landed.cost.lines', 'read', [[293]], {'fields': ['product_id', 'account_id', 'split_method', 'tax_today', 'currency_price_unit', 'price_unit']}))
for a in call('stock.valuation.adjustment.lines', 'search_read', [[['cost_id', '=', 120]]], {'fields': ['product_id', 'quantity', 'former_cost', 'additional_landed_cost', 'final_cost', 'former_cost_usd', 'additional_landed_cost_usd', 'final_cost_usd']}):
    a['costo_usd_kg'] = round(a['final_cost_usd'] / a['quantity'], 4)
    p(a)
