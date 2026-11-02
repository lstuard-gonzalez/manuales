import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
print('post ->', call('account.move', 'action_post', [[37888]]))
b = call('account.move', 'read', [[37888]], {'fields': ['name', 'state', 'ref', 'supplier_invoice_number', 'nro_ctrl', 'amount_total', 'amount_tax', 'wh_iva', 'wh_iva_id', 'iva_number_asignado', 'nks_retencion_iva', 'payment_state', 'amount_residual']})[0]
p(b)
if b['wh_iva_id']:
    p(call('account.wh.iva', 'read', [[b['wh_iva_id'][0]]], {'fields': ['name', 'number', 'state', 'date_ret', 'withholding_rate', 'amount_base_ret', 'total_tax_ret', 'wh_lines']}))
