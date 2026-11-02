import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
bill = call('account.move', 'read', [[37888]], {'fields': ['state', 'ref', 'supplier_invoice_number', 'wh_iva_id', 'partner_id']})[0]
wh = call('account.wh.iva', 'read', [[443]], {'fields': ['state', 'number', 'total_tax_ret']})[0]
prt = call('res.partner', 'read', [[4691]], {'fields': ['wh_iva_rate']})[0]
p([bill, wh, prt])
assert bill['state'] == 'draft' and bill['ref'] == '00000043' and bill['supplier_invoice_number'] == '00000044' and bill['wh_iva_id'][0] == 443
assert wh['state'] == 'done' and wh['number'] == '20261000000013' and prt['wh_iva_rate'] == 75.0
# 1. proveedor al 100 %
call('res.partner', 'write', [[4691], {'wh_iva_rate': 100.0}])
# 2. referencia de la factura
call('account.move', 'write', [[37888], {'ref': '00000044'}])
p(call('res.partner', 'read', [[4691]], {'fields': ['wh_iva_rate']}))
p(call('account.move', 'read', [[37888]], {'fields': ['state', 'ref', 'supplier_invoice_number']}))
