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
| Repo de manuales | https://github.com/lstuard-gonzalez/manuales (privado), rama `2026-10-26-amv-costos-destino-importaciones` |

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

### 5. Repositorio de manuales (27/10)
- Pedido: guardar todos los manuales en un repo git llamado `manuales`, en la cuenta personal del usuario (`lstuard-gonzalez`, no en Nikkosoft), con un `.md` de la conversación para retomarla, y **una rama por conversación**.
- La integración de Claude no puede crear repos (403 en Nikkosoft y en la cuenta personal). El usuario creó `lstuard-gonzalez/manuales` vacío e instaló la app de Claude en su cuenta; después se hizo el push.
- Estructura subida:
  - `main`: solo `README.md` con la convención (`AAAA-MM-DD-cliente-tema`) y la tabla de conversaciones.
  - `2026-10-26-amv-costos-destino-importaciones`: este archivo, `manuales/` (HTML + PDF de los dos manuales), `fuentes/` (Excel del salmón) y `tools/`.
- Convención para las próximas conversaciones: crear una rama nueva con el mismo formato, con su `CONVERSACION.md`, y agregar su fila al índice de `main`.
- Los manuales siguen también en el repo del cliente (`Nikkosoft/odoo-alimentos-monteverde`, `docs/manuales/`).

### 6. Pago agrupado a MESAMAR (29/10)
Video de Raquel: al marcar 4 facturas de MESAMAR la lista sumaba US$ 12.829,89, pero el asistente «Pagar» proponía US$ 12.800,095 (el total menos los US$ 29,80 de C003-00002025; la causa no se pudo reproducir porque las facturas ya estaban pagadas). Preguntaba si registrar un solo pago y cruzarlo factura por factura.

- Raquel ya lo había hecho: pago **PZELBI/2026/00135** (US$ 12.829,88, diario CXC JORGE ZELLE-BINANCE (USD), fecha 28/10, tasa 888,1183) cruzado con C003-00002025, C003-00001955, C003-00001933 y FACT 1891.
- Quedó un residuo de **US$ 0,015 (12,74 Bs)** en FACT 1891, porque C003-00001955 tiene tres decimales (3.413,985) y el pago solo dos.
- Con autorización del usuario, Claude registró **OPVAR/2026/10/0176** (diario OPERACIONES VARIAS, 29/10): débito `2.1.02.001` MESAMAR 12,74 Bs (US$ 0,015), crédito `8.1.01.0006 OTROS INGRESOS VARIOS`, y lo concilió con FACT 1891, que quedó saldada.
- FACT 1854 (US$ 237,08) sigue pendiente; no estaba en el pago.

### 7. Validación de la Relación de pagos (29/10)
Danny reenvió «Relación de pagos (33).pdf» (149 pagos del 27/10, creados por Aribel Beltran, BANCO MERCANTIL 0312) para validar los montos contra la base de datos: creía que el reporte traía la tasa BCV en lugar de la tasa que pone la usuaria.

- El reporte coincide con la base de datos en los 149 pagos (tasa = `tax_today`, Importe Bs = `amount_company_currency_signed` = asiento). Versión en producción: `nks_amv_ventas` 1.18.4 (ramas `main`/`staging` del repo del cliente).
- 10 de los 36 pagos en $ están contabilizados con otra tasa (8 a la BCV 887,302 y 2 a otra tasa). Diferencia total: 303.090,52 Bs. En los 10 casos el pago se restableció a borrador, se editó y se reconfirmó: la localización (`account_dual_currency`) recalcula el asiento sin respetar la tasa del pago.
- Número repetido: PMERC1/2026/00253 (un pago anulado de Johana Matute y el vigente de Aribel).
- Entrega: `manuales/validacion-relacion-pagos/` (PDF de 3 páginas para el consultor). Fuente: `fuentes/Relacion_de_pagos_33.pdf`.
- No se corrigió nada: corregir los 10 asientos está pendiente de decisión (9 están conciliados con facturas).

### 8. Retención de IVA de GRUPO FERREIRA 001 (02/11)
El proveedor (J-50792517-0) rechazó el comprobante de retención de IVA 20261000000013 (factura fiscal 00000044, control ZZP0023188, 30/10/2026, total 1.760.500,26 Bs, IVA 220.273,06 Bs): decía factura 00000043 y retención del 75% (165.204,80 Bs); debía ser 00000044 y 100%.

- Causas: la ficha del proveedor tenía «% Retención de IVA» = 75, y el comprobante toma el número de factura del campo **Referencia** de la factura (00000043), no de «Número de factura del proveedor» (00000044).
- El comprobante no se había declarado. Con autorización del usuario, Claude: puso el proveedor al 100%, cambió la Referencia de C003-00001955 a 00000044, canceló el comprobante (id 443; su asiento IVAC/2026/10/0014 quedó cancelado), confirmó la factura y confirmó la retención nueva (id 467).
- Resultado: comprobante **20261000000013** (la localización reutilizó el mismo número), 100%, 220.273,06 Bs, factura 00000044; asiento IVAC/2026/10/0015. Saldo por pagar de la factura: 1.540.227,20 Bs.

### 9. Pagos y cobros de Profit sin contrapartida (02/11)
Pedido: revisar los cobros/pagos cargados desde Profit que deben tener contrapartida en Odoo (contra el saldo inicial de bancos), sin conexión a Profit.
- 1.673 pagos de Profit (OdooBot, 01/10–29/10) en cuentas transitorias. Apertura de bancos y cajas al 30/09 = saldo de libros de Profit contra la puente `3.9.01.001`. Extractos cargados solo para los bancos en Bs (01/10–28/10).
- 1.015 conciliados con extracto; 68 con línea libre en el extracto (25,5 MM Bs); 2 dobles (Banco del Tesoro, ref. 122554603: la línea del extracto se concilió directo contra la CxC de INVERSIONES SUSHI EXPRES GM, saldo a favor falso de −16.336.952 Bs); 486 en cuentas sin extractos (Regions, Zelle-Binance, Efectivo $, Banco de Venezuela, Caja, Mercantil Panamá, Amerant); 99 sin rastro en el extracto de octubre (25,0 MM Bs: candidatos a estar ya en el saldo de apertura).
- Mercantil Panamá y Amerant quedarían en −US$ 181 mil y −US$ 292 mil: faltan los fondeos (de Profit solo se migraron cobros y pagos, no los movimientos de banco).
- Entrega: `manuales/pagos-profit-contrapartida/Pagos-Profit-sin-contrapartida-AMV.xlsx`. Se propuso cómo corregir; no se aplicó nada (pendiente de autorización: Tesoro y los 68).

### 10. Comisiones del 1.er corte de octubre, Odoo contra Profit (02/11)
Reportes de Profit «Comisiones por cobros» 01/10–15/10 de 8 vendedores contra el corte confirmado de Odoo (nks_amv_comisiones).
- Profit US$ 7.273,31 contra Odoo US$ 5.078,79 (−2.194,52). Por tasa −2.313,12: Profit corrió 3% fijo; Odoo paga el adelanto del 2% en el corte del 15 (grupos con escala) y completa al cierre según cumplimiento. Por base +118,40 netos.
- Causas de base: N/DB de diferencial (Profit las comisiona aparte; Odoo aplica todo a la factura con tope), notas de crédito (Profit resta), retenciones de IVA (Profit comisiona), 6 facturas con otro vendedor en Odoo, cobros del 15/10 aplicados el 16/10 en Odoo, 8 documentos de María que Profit no trae.
- Error de Odoo: comisiona AJPM cuyo cliente es el propio vendedor (Albert 11124, Manuel 11120, María 11121).
- Entrega: `manuales/comisiones-1er-corte-octubre/` (PDF de 3 páginas + Excel por documento). No se modificó nada.

## Cambios hechos en producción por Claude

| Fecha | Registro | Cambio |
|---|---|---|
| 26/10 | LC/2026/0119 | Creado por error (borrador vacío) y luego **borrado** con autorización |
| 26/10 | Factura C003-00001942 y asiento STJ/2026/10/0001 | Solo cambió la fecha de modificación al abrirlos (recálculo de la localización); sin cambios de montos |
| 27/10 | LC/2026/0120 | Línea a US$ 62.078,71 y cuenta 5.1.01.007; reparto manual; **validado** |
| 02/11 | GRUPO FERREIRA 001 / C003-00001955 / retención IVA | Proveedor al 100%, Referencia 00000044, comprobante 443 cancelado y nuevo comprobante 20261000000013 al 100% (id 467) |
| 29/10 | OPVAR/2026/10/0176 | Ajuste de redondeo de US$ 0,015 (12,74 Bs) conciliado con FACT 1891 de MESAMAR |

Todo lo demás fue de solo lectura.

## Pendientes

- **H1:** asignar cuenta de gastos `5.1.01.007` al producto 1319 (o a la categoría GASTOS OTROS). LC/2026/0120 ya usó 5.1.01.007 en su línea, pero el producto sigue sin cuenta.
- **H2:** crear el costo en destino de la factura C003-00001942.
- **Planilla en el libro de compras:** los campos Nº planilla / fecha / expediente / «Factura SENIAT» solo aparecen si el proveedor es empresa **PJND**. NANTONG está como persona PNNR y SENIAT como persona PNRE. Probar en staging cómo entra la planilla como «Importación» al libro de compras (o leer el código de `nks_localizacion`).
- Confirmar con Contabilidad que ADEL 1023 y ADEL 1128 son de OC-00916.
- Ahumado: el costeo dice 18,65 pero con US$ 10.783,79 da 18,6568. Para 18,65 exacto el gasto sería US$ 10.750,00 (requiere otro costo en destino negativo por US$ 33,79).
- Un costo en destino validado no se cancela: las correcciones van con otro costo en destino (negativo si hay que restar).

- La empresa no tiene configurado el «Diario Asientos de Redondeo» (Contabilidad › Ajustes). El ajuste de MESAMAR usó OPERACIONES VARIAS y 8.1.01.0006; Contabilidad puede definir un diario y una cuenta propios.

- Corregir los asientos de los 10 pagos con tasa equivocada (relación de pagos del 27/10) y reportar el defecto de reconfirmación a la localización.
- FACT 1854 de MESAMAR (US$ 237,08): registrar el pago cuando se sepa el diario y la fecha.

- Corregir el doble del Banco del Tesoro y conciliar los 68 cobros de Profit con línea libre en el extracto; cargar extractos de las cuentas en $ y registrar los fondeos de Mercantil Panamá y Amerant.
- Comisiones: excluir los AJPM del propio vendedor en nks_amv_comisiones y decidir con el cliente diferencial, retenciones y notas de crédito.

## Lecciones técnicas (Odoo 19 + localización AMV)
- El comprobante de retención de IVA imprime como número de factura el campo **Referencia** de la factura de proveedor. Al cancelar y regenerar una retención, la localización reutiliza el número asignado (`iva_number_asignado`).
- Restablecer a borrador y reconfirmar un pago en $ con tasa propia lo recalcula a la BCV (o a otra tasa): para corregir un pago confirmado, anularlo y crear uno nuevo.
- Facturas con tres decimales en US$ dejan residuos de centavos al pagar (los pagos van a dos decimales); se cierran con un ajuste conciliado.

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
