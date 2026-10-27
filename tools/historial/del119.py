import json, os, urllib.request, http.cookiejar
BASE = 'https://alimentos-monteverde.odoo.com'
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def post(path, params):
    req = urllib.request.Request(BASE + path, json.dumps({"jsonrpc": "2.0", "method": "call", "params": params}).encode(), {'Content-Type': 'application/json'})
    r = json.load(op.open(req, timeout=60))
    if 'error' in r: raise SystemExit(json.dumps(r['error'])[:800])
    return r['result']
post('/web/session/authenticate', {'db': os.environ['DB'], 'login': 'admin', 'password': os.environ['P']})
kw = lambda m, meth, args, k=None: post('/web/dataset/call_kw', {'model': m, 'method': meth, 'args': args, 'kwargs': k or {}})
rec = kw('stock.landed.cost', 'read', [[119]], {'fields': ['name', 'state', 'create_uid', 'picking_ids', 'cost_lines', 'valuation_adjustment_lines', 'account_move_id', 'vendor_bill_id', 'amount_total']})
print('antes:', rec)
r = rec[0]
assert r['name'] == 'LC/2026/0119' and r['state'] == 'draft' and not r['picking_ids'] and not r['cost_lines'] and not r['valuation_adjustment_lines'] and not r['account_move_id'] and not r['vendor_bill_id'] and r['amount_total'] == 0, 'no coincide, no borro'
print('unlink:', kw('stock.landed.cost', 'unlink', [[119]]))
print('después:', kw('stock.landed.cost', 'search_read', [[]], {'fields': ['name', 'state']}))
post('/web/session/destroy', {})
