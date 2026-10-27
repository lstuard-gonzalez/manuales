# Conversación 2026-10-26 · AMV · Costos en destino e importaciones

Resumen para retomar esta conversación. Fechas: 26 y 27/10/2026.

## Contexto

| Dato | Valor |
|---|---|
| Cliente | Alimentos MonteVerde C.A. (AMV) |
| Instancia | https://alimentos-monteverde.odoo.com (producción, Odoo 19 Enterprise) |
| Base de datos | `alimentos-monteverde-main-24467214` |
| Usuario usado | `admin`. **La clave no se guarda aquí**: pedírsela al usuario. Se escribió en el chat el 26/10, así que conviene cambiarla. |
| Repo del cliente | `Nikkosoft/odoo-alimentos-monteverde`, rama `claude/gallant-sagan-qn3idn` (los manuales también están en `docs/manuales/`) |
| Localización | `nks_localizacion` (submódulo, rama 19.0). No hubo acceso a ese repo en la sesión. |
| Módulos clave | `stock_landed_costs` 19.0.1.1, `mrp_landed_costs`, `account_dual_currency` 1.12.20, `nks_importaciones` 1.5.1, `nks_amv_ventas` 1.18.1 |
| Sesión original | https://claude.ai/code/session_012G7rDzCGgXdqyg1cPT8wfi |

Configuración de valuación en AMV: perpetua (al facturar), AVCO, cuenta de inventario `1.1.13.001 INVENTARIO VENTA`, diario `STJ · Valuación de inventario` (id 8). Moneda de la compañía VES; referencia USD.

## Pedidos y entregas, en orden

### 1. Manual de costos en destino (26/10)
- Pedido: «manual de configuración y uso de cuentas de costo en destino con capturas reales».
- Entrega: `manuales/costo-en-destino/` (HTML + PDF de 26 páginas). Artifact: https://claude.ai/artifact/MjyKVsBxzDDiDRm8Whdj7s
- Ejemplo real usado: **LC/2026/0118** (22/10, VAL/IN/00044, NORI, US$ 43.532 × 884,7496 = 38.514.919,59 Bs). El costo del NORI quedó en 43.237,44 Bs/caja.
- Hallazgos que se documentaron (no se corrigieron, los decide Contabilidad):
  - **H1:** el producto «GASTO DE IMPORTACION ORDINARIA» (id 1319) no tiene cuenta de gastos y su categoría GASTOS OTROS tampoco. Las facturas con ese producto van a `5.1.01.001 COSTO DE VENTAS`. Propuesta: asignarle `5.1.01.007 GASTOS DE IMPORTACION`.
  - **H2:** la factura C003-00001942 (CORPORACION 18, ref. 140066) tiene una línea de costo en destino sin costo en destino creado.
  - **H3:** LC/2026/0118 no tiene factura de proveedor enlazada.

### 2. Borrado de LC/2026/0119 (26/10)
- Claude lo creó por error al abrir el formulario «Nuevo» de costos en destino para una captura (Odoo guardó el borrador vacío al salir).
- El usuario autorizó borrarlo. Se borró después de confirmar que estaba vacío.

### 3. Audio del cliente sobre importaciones (26/10)
Transcripción (a «Dani»): reciben contenedores, el precio se acuerda con el proveedor y este no emite factura por ese precio; al nacionalizar declaran un precio menor. Caso NORI: ya tienen la OC, la recepción y la distribución de costo; falta la factura del proveedor. Para el libro de compras usarían la factura de nacionalización, pero al cruzar los pagos les queda un saldo pendiente contra el precio real. ¿Cómo lo manejan?

- Primera respuesta: Claude señaló el riesgo de subvaloración aduanera y recomendó escalar al Director y al asesor tributario. **El usuario pidió explícitamente no dar opinión y entregar el procedimiento.**
- Entrega: `manuales/importacion-precio-acordado/` (HTML + PDF de 16 páginas).
- Procedimiento documentado:
  1. Factura de NANTONG desde OC-00916 (lista de órdenes › «Crear facturas», o «Subir factura» con el PDF) en el diario **GASTOS NO FISCALES** (id 553, `nks_no_fiscal`: se paga y concilia, no entra a libros).
  2. Cruzar los anticipos **ADEL 1023 + ADEL 1128 = US$ 214.500** (saldos iniciales 30/09, cuenta `2.1.02.002`) desde «Débitos pendientes › Agregar». ADEL 1102 (US$ 98.825) y ADEL 1022 (US$ 0,10) quedan abiertos.
  3. Planilla de liquidación a nombre del contacto **SENIAT** (id 2841) en FACTURAS PROVEEDORES, IVA 16% C.
  4. Arancel y gastos como costo en destino nuevo.

### 4. Costeo del salmón (27/10)
Mensaje y audios del cliente: el filet se facturó a US$ 11,25/kg pero el costeo usa el precio actual de US$ 13,10/kg (próximo contenedor). Gasto de importación: filet **US$ 51.294,92** (costo final 14,70 $/kg), ahumado **US$ 10.783,79** (costo final 18,65 $/kg). Excel en `fuentes/`.

- **LC/2026/0120** (borrador de Raquel Zarraga, 26/10) sobre **CEA/IN/00003** (OC-00918, EMPRESAS AQUACHILE, S.A.) tenía US$ 34.587,71; al filet le faltaban los US$ 27.491,00 de diferencia de precio.
- Con autorización del usuario, Claude:
  - cambió la línea a **US$ 62.078,71** (55.015.835,14 Bs, tasa 886,2271) y la cuenta a **`5.1.01.007`**;
  - ejecutó Compute y fijó el reparto: filet 45.458.948,20 Bs (US$ 51.294,92), ahumado 9.556.886,94 Bs (US$ 10.783,79);
  - **validó** LC/2026/0120 → asiento **STJ/2026/10/0010** (55.012.012,39 Bs; el ahumado capitalizó 4.998 de 5.000 kg porque 2 kg ya habían salido).
- Resultado: último costo $ filet **14,7019**, ahumado **18,6568**. Costo promedio filet 12.907,09 Bs/kg (≈ US$ 14,56, mezcla con 1.946 kg anteriores); ahumado 16.534,12 Bs/kg.

## Cambios hechos en producción por Claude

| Fecha | Registro | Cambio |
|---|---|---|
| 26/10 | LC/2026/0119 | Creado por error (borrador vacío) y luego **borrado** con autorización |
| 26/10 | Factura C003-00001942 y asiento STJ/2026/10/0001 | Solo cambió la fecha de modificación al abrirlos (recálculo de la localización); sin cambios de montos |
| 27/10 | LC/2026/0120 | Línea a US$ 62.078,71 y cuenta 5.1.01.007; reparto manual; **validado** |

Todo lo demás fue de solo lectura.

## Pendientes

- **H1:** asignar cuenta de gastos `5.1.01.007` al producto 1319 (o a la categoría GASTOS OTROS). LC/2026/0120 ya usó 5.1.01.007 en su línea, pero el producto sigue sin cuenta.
- **H2:** crear el costo en destino de la factura C003-00001942.
- **Planilla en el libro de compras:** los campos Nº planilla / fecha / expediente / «Factura SENIAT» solo aparecen si el proveedor es empresa **PJND**. NANTONG está como persona PNNR y SENIAT como persona PNRE. Probar en staging cómo entra la planilla como «Importación» al libro de compras (o leer el código de `nks_localizacion`).
- Confirmar con Contabilidad que ADEL 1023 y ADEL 1128 son de OC-00916.
- Ahumado: el costeo dice 18,65 pero con US$ 10.783,79 da 18,6568. Para 18,65 exacto el gasto sería US$ 10.750,00 (requiere otro costo en destino negativo por US$ 33,79).
- Un costo en destino validado no se cancela: las correcciones van con otro costo en destino (negativo si hay que restar).

## Lecciones técnicas (Odoo 19 + localización AMV)

- Abrir un formulario **«Nuevo»** y salir guarda el borrador (pasó con LC/2026/0119). Para capturas, no abrir formularios nuevos.
- Abrir un **asiento o factura registrada** actualiza su fecha de modificación (recálculo de la localización dual) aunque no cambie nada.
- En Odoo 19 la **orden de compra no tiene botón «Crear factura»** en el formulario: está «Subir factura» (con PDF) y, en la lista, «Crear facturas».
- En Odoo 19 la valuación y el método de costo se configuran por empresa en Contabilidad › Ajustes; la categoría puede sobrescribirlos.
- **Compute** en un costo en destino borra los ajustes hechos a mano en «Ajustes de valoración».
- Al validar, solo se capitaliza la parte que sigue en existencia; lo vendido queda en la cuenta de gastos.
- El reporte «último costo $» (`nks_amv_ventas/models/ultimo_costo.py`) = precio del documento en $ + costos en destino validados en $, por entrada de proveedor.
- La localización calcula los campos en $ del costo en destino (`additional_landed_cost_usd`, etc.) desde Bs ÷ tasa; se edita el monto en Bs.

## Herramientas (`tools/`)

| Archivo | Uso |
|---|---|
| `login.js` | Inicia sesión con Playwright y guarda `state.json`. Uso: `U=admin P='<clave>' node login.js`. **Borrar `state.json` al terminar.** |
| `lib.js` | Abre el navegador con la sesión guardada (`open`, `go`). |
| `cap.js` | Capturas con recuadros numerados. Recibe un JSON de pasos: `go`, `tab`, `actions` (click/fill/press), `fields`/`cols`/`texts`/`sels` para resaltar, `shot`. Solo navega. |
| `pdf.js` | Genera el PDF de un manual desde su `index.html` (rutas internas a ajustar). |
| `rpc_lectura.py` | Consultas JSON-RPC de solo lectura. Uso: `DB=alimentos-monteverde-main-24467214 P='<clave>' python3 script.py` con `exec(open('rpc_lectura.py')...)`. |
| `tr.py` | Transcribe audios de WhatsApp con faster-whisper (modelo small, español). Convertir antes con `ffmpeg -i audio.ogg -ar 16000 -ac 1 -f s16le a.raw`. |
| `historial/` | Scripts que escribieron en producción (borrado de LC 119, ajuste y validación de LC 120), para trazabilidad. No reejecutar. |
