import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
w = call('account.wh.iva', 'read', [[467]], {'fields': ['state', 'total_tax_ret', 'withholding_rate']})[0]
assert w['state'] == 'draft' and abs(w['total_tax_ret'] - 220273.06) < 0.005 and w['withholding_rate'] == 100.0, w
print('confirm ->', call('account.wh.iva', 'confirm_check', [[467]]))
p(call('account.wh.iva', 'read', [[467]], {'fields': ['name', 'number', 'state', 'date_ret', 'withholding_rate', 'total_tax_ret', 'journal_id']}))
l = call('account.wh.iva.line', 'read', [[467]], {'fields': ['supplier_invoice_number', 'nro_ctrl', 'wh_iva_rate', 'amount_tax_ret', 'move_id', 'state']})[0]
p(l)
if l['move_id']:
    p(call('account.move', 'read', [[l['move_id'][0]]], {'fields': ['name', 'state', 'date']}))
    p(call('account.move.line', 'search_read', [[['move_id', '=', l['move_id'][0]]]], {'fields': ['account_id', 'debit', 'credit', 'reconciled']}))
p(call('account.move', 'read', [[37888]], {'fields': ['state', 'ref', 'wh_iva', 'iva_number_asignado', 'nks_retencion_iva', 'payment_state', 'amount_residual']}))
