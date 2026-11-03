import sys, json
from collections import defaultdict, Counter
exec(open(sys.argv[1]).read().split("READ =")[0])
DRY = sys.argv[2] == 'dry'
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
ST = {35: ('2026-10-19', '2026-10-27'), 41: ('2026-10-28', '2026-10-29'), 42: ('2026-10-30', '2026-10-30')}
home = lambda d: next(k for k, (a, b) in ST.items() if a <= d <= b)
F = ['date', 'payment_ref', 'amount', 'is_reconciled', 'statement_id', 'move_id']
bl = call('account.bank.statement.line', 'search_read', [[['journal_id.code', '=', 'BNK2'], ['statement_id', 'in', list(ST)]]], {'fields': F})
mv = defaultdict(list)
for l in call('account.move.line', 'search_read', [[['move_id', 'in', [b['move_id'][0] for b in bl]]]], {'fields': ['move_id', 'matched_debit_ids', 'matched_credit_ids']}): mv[l['move_id'][0]].append(l)
hp = lambda b: any(l['matched_debit_ids'] or l['matched_credit_ids'] for l in mv[b['move_id'][0]])
g = defaultdict(list)
for b in bl: g[(b['date'], b['payment_ref'], b['amount'])].append(b)
borrar, quedan, pend = [], [], []
for k, v in g.items():
    if len(v) == 1: quedan.append(v[0]); continue
    h = home(k[0]); e, l = sorted(v, key=lambda x: x['statement_id'][0] != h)
    ra, rb = e['is_reconciled'] or hp(e), l['is_reconciled'] or hp(l)
    if ra and rb:
        if hp(e) and hp(l): pend.append(k); continue
        keep, drop = (l, e) if hp(l) else (e, l)
    elif rb: keep, drop = l, e
    else: keep, drop = e, l
    if hp(drop): pend.append(k); continue
    borrar.append(drop); quedan.append(keep)
mover = [b for b in quedan if b['statement_id'][0] != home(b['date'])]
print('borrar', len(borrar), round(sum(b['amount'] for b in borrar), 2), Counter(b['statement_id'][0] for b in borrar), '| mover', len(mover), Counter((b['statement_id'][0], home(b['date'])) for b in mover), '| pendientes', pend)
s = {x['id']: x for x in call('account.bank.statement', 'read', [list(ST)], {'fields': ['balance_start', 'balance_end_real']})}
final = defaultdict(list)
for b in quedan: final[home(b['date'])].append(b)
for k in pend:
    for b in g[k]: final[b['statement_id'][0]].append(b)
bal = s[35]['balance_start']; plan = {}
for sid in sorted(ST):
    t = round(sum(b['amount'] for b in final[sid]), 2); plan[sid] = (round(bal, 2), round(bal + t, 2)); bal += t
    print(sid, 'inicio', plan[sid][0], 'fin', plan[sid][1], '(real antes %s)' % s[sid]['balance_end_real'], len(final[sid]), 'líneas')
assert abs(plan[35][1] - s[35]['balance_end_real']) < .005, 'el 35 no cuadra con su saldo real'
if DRY: sys.exit()
json.dump({'borrar': [(b['id'], b['move_id'][1], b['date'], b['payment_ref'], b['amount'], b['statement_id'][0]) for b in borrar], 'mover': [(b['id'], b['move_id'][1], home(b['date'])) for b in mover], 'plan': plan}, open('exec_bnk2_log.json', 'w'))
n = 0
for b in borrar:
    call('account.bank.statement.line', 'write', [[b['id']], {'statement_id': False}])
    call('account.bank.statement.line', 'unlink', [[b['id']]]); n += 1
print('borradas', n)
for b in mover: call('account.bank.statement.line', 'write', [[b['id']], {'statement_id': home(b['date'])}])
print('movidas', len(mover))
for sid in sorted(ST):
    call('account.bank.statement', 'write', [[sid], {'balance_start': plan[sid][0], 'balance_end_real': plan[sid][1]}])
for x in call('account.bank.statement', 'read', [list(ST)], {'fields': ['name', 'balance_start', 'balance_end', 'balance_end_real', 'is_complete', 'is_valid', 'line_ids']}):
    print(x['name'], x['balance_start'], x['balance_end'], x['balance_end_real'], 'completo', x['is_complete'], 'válido', x['is_valid'], len(x['line_ids']))
