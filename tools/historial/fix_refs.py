import sys
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
for rev_id in [39871, 39880]:
    r = call('account.move', 'read', [[rev_id]], {'fields': ['reversed_entry_id']})[0]
    call('account.move', 'write', [[rev_id], {'ref': 'Reversión de: %s' % r['reversed_entry_id'][1].split(' ')[0]}])
    print(call('account.move', 'read', [[rev_id]], {'fields': ['name', 'ref', 'date']}))
