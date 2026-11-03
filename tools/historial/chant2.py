import sys
from collections import defaultdict
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
pay = call('account.payment', 'search_read', [[['name', '=', 'PBNK2/2026/00196']]], {'fields': ['move_id', 'partner_id']})[0]
tl = call('account.move.line', 'search_read', [[['move_id', '=', pay['move_id'][0]], ['account_id.code', '=', '1.1.04.001.2']]], {'fields': ['id', 'account_id', 'amount_residual', 'reconciled']})[0]
print(tl)
assert not tl['reconciled'] and abs(tl['amount_residual'] - 0.16) < .005
ref = 'Diferencia cobro PBNK2/2026/00196 vs depósito 52330388'
mid = call('account.move', 'create', [{'move_type': 'entry', 'journal_id': 66, 'date': '2026-10-29', 'ref': ref, 'line_ids': [
    (0, 0, {'account_id': tl['account_id'][0], 'partner_id': pay['partner_id'][0], 'name': ref, 'debit': 0.0, 'credit': 0.16}),
    (0, 0, {'account_id': 253, 'partner_id': pay['partner_id'][0], 'name': ref, 'debit': 0.16, 'credit': 0.0})]}])
call('account.move', 'action_post', [[mid]])
nl = call('account.move.line', 'search_read', [[['move_id', '=', mid], ['account_id', '=', tl['account_id'][0]]]], {'fields': ['id']})[0]['id']
call('account.move.line', 'reconcile', [[tl['id'], nl]])
print(call('account.move', 'read', [[mid]], {'fields': ['name', 'date', 'state']}), call('account.payment', 'read', [[pay['id'] if 'id' in pay else 2964]], {'fields': ['name', 'state']}))
# verificación general
bl = call('account.bank.statement.line', 'search_read', [[['journal_id.code', '=', 'BNK2']]], {'fields': ['date', 'payment_ref', 'amount', 'statement_id']})
g = defaultdict(list)
for b in bl: g[(b['date'], b['payment_ref'], b['amount'])].append(b['statement_id'] and b['statement_id'][1])
print('BNK2 líneas', len(bl), 'repetidas', [(k, v) for k, v in g.items() if len(v) > 1])
ss = call('account.move.line', 'search_read', [[['account_id.code', '=', '1.1.03.001'], ['parent_state', '=', 'posted']]], {'fields': ['balance', 'amount_residual']})
print('1.1.03.001 saldo', round(sum(l['balance'] for l in ss), 2), 'abierto', round(sum(l['amount_residual'] for l in ss), 2))
print('EXCH creados hoy:', call('account.move', 'search_read', [[['journal_id.code', '=', 'EXCH'], ['create_date', '>=', '2026-11-03 00:00:00']]], {'fields': ['name', 'date', 'amount_total', 'create_uid']}))
print('borradores MISC1/APER/OPVAR:', call('account.move', 'search_read', [[['state', '=', 'draft'], ['journal_id.code', 'in', ['MISC1', 'APER', 'OPVAR']]]], {'fields': ['name', 'ref', 'amount_total', 'create_uid']}))
print(call('account.move', 'search_read', [[['name', 'like', 'MISC1/2026/10/']]], {'fields': ['name', 'date', 'state', 'amount_total', 'ref']}))
