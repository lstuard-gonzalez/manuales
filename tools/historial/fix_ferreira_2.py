import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
print('cancel ->', call('account.wh.iva', 'action_cancel', [[443]]))
p(call('account.wh.iva', 'read', [[443]], {'fields': ['state', 'number', 'total_tax_ret']}))
p(call('account.wh.iva.line', 'read', [[443]], {'fields': ['state', 'move_id']}))
p(call('account.move', 'read', [[39361]], {'fields': ['name', 'state', 'reversal_move_ids'] }))
p(call('account.move', 'read', [[37888]], {'fields': ['state', 'ref', 'wh_iva', 'wh_iva_id', 'iva_number_asignado', 'nks_retencion_iva', 'payment_state']}))
