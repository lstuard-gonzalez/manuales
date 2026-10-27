import json, os, urllib.request, http.cookiejar
BASE = 'https://alimentos-monteverde.odoo.com'
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def post(path, params):
    req = urllib.request.Request(BASE + path, json.dumps({"jsonrpc": "2.0", "method": "call", "params": params}).encode(), {'Content-Type': 'application/json'})
    r = json.load(op.open(req, timeout=60))
    if 'error' in r: raise SystemExit(json.dumps(r['error'])[:600])
    return r.get('result')
post('/web/session/authenticate', {'db': os.environ['DB'], 'login': 'admin', 'password': os.environ['P']})
READ = {'read', 'search_read', 'fields_get', 'get_views', 'search_count'}
def kw(m, meth, args, k=None):
    assert meth in READ
    return post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': dict(k or {}, context={'lang': 'es_VE'})})
p = lambda x: print(json.dumps(x, ensure_ascii=False, default=str))
po = kw('purchase.order', 'search_read', [[['name', '=', 'OC-00916']]], {'fields': ['name', 'partner_id', 'currency_id', 'amount_untaxed', 'amount_total', 'state', 'invoice_status', 'invoice_ids', 'date_order', 'fiscal_position_id']})
p(po)
p(kw('purchase.order.line', 'search_read', [[['order_id', '=', po[0]['id']]]], {'fields': ['product_id', 'product_qty', 'qty_received', 'qty_invoiced', 'price_unit', 'price_subtotal', 'taxes_id' if False else 'tax_ids']}))
p(kw('nks.import.file', 'fields_get', [], {'attributes': ['string', 'type']}))
