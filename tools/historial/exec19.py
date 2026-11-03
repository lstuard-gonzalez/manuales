import sys, json
from collections import defaultdict
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
a = call('account.bank.statement.line', 'search_read', [[['journal_id.code', '=', 'BNK2'], ['date', '=', '2026-10-19']]], {'fields': ['payment_ref', 'amount', 'statement_id', 'is_reconciled', 'move_id']})
g = defaultdict(list)
for x in a: g[(x['payment_ref'], x['amount'])].append(x)
drop = []
for k, v in g.items():
    if len(v) != 2: continue
    c35 = [x for x in v if x['statement_id'][0] == 35][0]
    ls = call('account.move.line', 'search_read', [[['move_id', '=', c35['move_id'][0]]]], {'fields': ['matched_debit_ids', 'matched_credit_ids']})
    assert not c35['is_reconciled'] and not any(l['matched_debit_ids'] or l['matched_credit_ids'] for l in ls), c35
    drop.append(c35)
tot = round(sum(x['amount'] for x in drop), 2)
print('borrar', len(drop), tot, [x['move_id'][1] for x in drop])
assert len(drop) == 9
json.dump([(x['id'], x['move_id'][1], x['payment_ref'], x['amount']) for x in drop], open('exec19_log.json', 'w'))
for x in drop:
    call('account.bank.statement.line', 'write', [[x['id']], {'statement_id': False}])
    call('account.bank.statement.line', 'unlink', [[x['id']]])
s = {x['id']: x for x in call('account.bank.statement', 'read', [[35, 41, 42]], {'fields': ['balance_start', 'balance_end']})}
bal = s[35]['balance_start']
for sid in (35, 41, 42):
    t = s[sid]['balance_end'] - s[sid]['balance_start'] if sid != 35 else None
    st = call('account.bank.statement', 'read', [[sid]], {'fields': ['line_ids']})[0]
    t = sum(l['amount'] for l in call('account.bank.statement.line', 'read', [st['line_ids']], {'fields': ['amount']}))
    call('account.bank.statement', 'write', [[sid], {'balance_start': round(bal, 2), 'balance_end_real': round(bal + t, 2)}]); bal += t
for x in call('account.bank.statement', 'read', [[27, 35, 41, 42]], {'fields': ['name', 'balance_start', 'balance_end', 'balance_end_real', 'is_complete', 'is_valid', 'line_ids']}):
    print(x['name'], x['balance_start'], x['balance_end'], x['balance_end_real'], 'completo', x['is_complete'], 'válido', x['is_valid'], len(x['line_ids']))
