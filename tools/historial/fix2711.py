import sys, json
exec(open(sys.argv[1]).read().split("READ =")[0])
def call(m, meth, args, k=None):
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE', 'tz': 'America/Caracas'})})
NUEVA = '2026-10-27'
def arreglar(pago_name):
    pay = call('account.payment', 'search_read', [[['name', '=', pago_name]]], {'fields': ['id', 'date', 'state', 'amount', 'tax_today', 'move_id', 'reconciled_bill_ids']})[0]
    assert pay['date'] == '2026-11-27' and len(pay['reconciled_bill_ids']) == 1, pay
    rid = pay['reconciled_bill_ids'][0]
    rec = call('account.move', 'read', [[rid]], {'fields': ['name', 'date', 'invoice_date', 'state', 'amount_total', 'tax_today']})[0]
    assert rec['date'] == '2026-11-27', rec
    # 1. borrador (el pago primero: deshace la conciliación)
    call('account.payment', 'action_draft', [[pay['id']]])
    call('account.move', 'button_draft', [[rid]])
    # 2. fechas, conservando la tasa que puso la usuaria
    call('account.move', 'write', [[rid], {'invoice_date': NUEVA, 'date': NUEVA}])
    call('account.move', 'write', [[rid], {'tax_today': rec['tax_today']}])
    call('account.payment', 'write', [[pay['id']], {'date': NUEVA}])
    call('account.payment', 'write', [[pay['id']], {'tax_today': pay['tax_today']}])
    # 3. confirmar
    call('account.move', 'action_post', [[rid]])
    call('account.payment', 'action_post', [[pay['id']]])
    # 4. volver a conciliar la CxP del recibo con la del pago
    pl = call('account.move.line', 'search_read', [['|', ['move_id', '=', rid], ['move_id', '=', pay['move_id'][0]], ['account_id.account_type', '=', 'liability_payable'], ['reconciled', '=', False]]], {'fields': ['id']})
    call('account.move.line', 'reconcile', [[l['id'] for l in pl]])
    # 5. verificar
    p2 = call('account.payment', 'read', [[pay['id']]], {'fields': ['name', 'date', 'state', 'amount', 'tax_today', 'amount_company_currency_signed', 'reconciled_bill_ids']})[0]
    r2 = call('account.move', 'read', [[rid]], {'fields': ['name', 'date', 'invoice_date', 'state', 'amount_total', 'tax_today', 'payment_state']})[0]
    ok = (p2['date'] == NUEVA and r2['date'] == NUEVA and r2['invoice_date'] == NUEVA and p2['state'] in ('in_process', 'paid') and r2['state'] == 'posted'
          and abs(abs(p2['amount_company_currency_signed']) - pay['amount']) < 0.005 and abs(r2['amount_total'] - rec['amount_total']) < 0.005
          and p2['tax_today'] == pay['tax_today'] and r2['tax_today'] == rec['tax_today'] and r2['payment_state'] in ('in_payment', 'paid') and p2['reconciled_bill_ids'] == [rid])
    print(('OK  ' if ok else 'REVISAR'), p2['name'], p2['date'], p2['state'], p2['amount'], 'tasa', p2['tax_today'], '|', r2['name'], r2['date'], r2['invoice_date'], r2['amount_total'], 'tasa', r2['tax_today'], r2['payment_state'])
    return ok
for name in sys.argv[2:]:
    if not arreglar(name):
        print('Se detiene para revisar.'); break
