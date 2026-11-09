# Conversación 2026-10-26 · AMV · Costos en destino, importaciones y soporte contable

Resumen para retomar esta conversación. Fechas: del 26/10 al 03/11/2026.

## Contexto

| Dato | Valor |
|---|---|
| Cliente | Alimentos MonteVerde C.A. (AMV), RIF J-31220183-5 |
| Instancia | https://alimentos-monteverde.odoo.com (producción, Odoo 19 Enterprise) |
| Base de datos | `alimentos-monteverde-main-24467214` |
| Usuario usado | `admin`. **La clave no se guarda aquí**: pedírsela al usuario. Se escribió en el chat el 26/10, así que conviene cambiarla. |
| Repo del cliente | `Nikkosoft/odoo-alimentos-monteverde`, rama `claude/gallant-sagan-qn3idn` (los manuales también están en `docs/manuales/`) |
| Localización | `nks_localizacion` (submódulo, rama 19.0). No hubo acceso a ese repo en la sesión. |
| Módulos clave | `stock_landed_costs` 19.0.1.1, `mrp_landed_costs`, `account_dual_currency` 1.12.20, `nks_importaciones` 1.5.1, `nks_amv_ventas` 1.18.4, `nks_amv_comisiones` 19.0.1.0.0 |
| Sesión original | https://claude.ai/code/session_012G7rDzCGgXdqyg1cPT8wfi |
| Repo de manuales | https://github.com/lstuard-gonzalez/manuales (privado), rama `2026-10-26-amv-costos-destino-importaciones` |

- **Valuación:** perpetua (al facturar), AVCO, cuenta de inventario `1.1.13.001 INVENTARIO VENTA`, diario `STJ · Valuación de inventario` (id 8). La recepción no genera asiento; lo genera la factura del proveedor.
- **Monedas:** compañía en VES; referencia en USD.
- **Compañías y sucursales:** una sola compañía. Las sucursales (Valencia, Caracas, Lecherías, CEALCO) son almacenes (`nks_sucursal_id`).

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
- Estructura:
  - `main`: solo `README.md` con la convención (`AAAA-MM-DD-cliente-tema`) y la tabla de conversaciones.
  - `2026-10-26-amv-costos-destino-importaciones`: este archivo, `manuales/` (cada entrega en su carpeta), `fuentes/` (archivos del cliente) y `tools/`.
- Convención para las próximas conversaciones: crear una rama nueva con el mismo formato, con su `CONVERSACION.md`, y agregar su fila al índice de `main`.
- Los dos primeros manuales siguen también en el repo del cliente (`Nikkosoft/odoo-alimentos-monteverde`, `docs/manuales/`).

### 6. Pago agrupado a MESAMAR (29/10)
Video de Raquel: al marcar 4 facturas de MESAMAR la lista sumaba US$ 12.829,89, pero el asistente «Pagar» proponía US$ 12.800,095 (el total menos los US$ 29,80 de C003-00002025; la causa no se pudo reproducir porque las facturas ya estaban pagadas). Preguntaba si registrar un solo pago y cruzarlo factura por factura.

- Raquel ya lo había hecho: pago **PZELBI/2026/00135** (US$ 12.829,88, diario CXC JORGE ZELLE-BINANCE (USD), fecha 28/10, tasa 888,1183) cruzado con C003-00002025, C003-00001955, C003-00001933 y FACT 1891.
- Quedó un residuo de **US$ 0,015 (12,74 Bs)** en FACT 1891, porque C003-00001955 tiene tres decimales (3.413,985) y el pago solo dos.
- Con autorización del usuario, Claude registró **OPVAR/2026/10/0176** (diario OPERACIONES VARIAS, 29/10): débito `2.1.02.001` MESAMAR 12,74 Bs (US$ 0,015), crédito `8.1.01.0006 OTROS INGRESOS VARIOS`, y lo concilió con FACT 1891, que quedó saldada.
- FACT 1854 (US$ 237,08) sigue pendiente: el usuario pidió pagarla, pero no indicó diario ni fecha.

### 7. Validación de la Relación de pagos (29/10)
Danny reenvió «Relación de pagos (33).pdf» (149 pagos del 27/10, creados por Aribel Beltran, BANCO MERCANTIL 0312) para validar los montos contra la base de datos: creía que el reporte traía la tasa BCV en lugar de la tasa que pone la usuaria.

- El reporte coincide con la base de datos en los 149 pagos (tasa = `tax_today`, Importe Bs = `amount_company_currency_signed` = asiento).
- 10 de los 36 pagos en $ están contabilizados con otra tasa (8 a la BCV 887,302 y 2 a otra tasa). Diferencia total: 303.090,52 Bs. En los 10 casos el pago se restableció a borrador, se editó y se reconfirmó: la localización (`account_dual_currency`) recalcula el asiento sin respetar la tasa del pago.
- Número repetido: PMERC1/2026/00253 (un pago anulado de Johana Matute y el vigente de Aribel).
- Entrega: `manuales/validacion-relacion-pagos/` (PDF de 3 páginas para el consultor). Fuente: `fuentes/Relacion_de_pagos_33.pdf`.
- No se corrigió nada: corregir los 10 asientos está pendiente de decisión (9 están conciliados con facturas).

### 8. Retención de IVA de GRUPO FERREIRA 001 (02/11)
El proveedor (J-50792517-0) rechazó el comprobante de retención de IVA 20261000000013 (factura fiscal 00000044, control ZZP0023188, 30/10/2026, total 1.760.500,26 Bs, IVA 220.273,06 Bs): decía factura 00000043 y retención del 75% (165.204,80 Bs); debía ser 00000044 y 100%.

- Causas: la ficha del proveedor tenía «% Retención de IVA» = 75, y el comprobante toma el número de factura del campo **Referencia** de la factura (00000043), no de «Número de factura del proveedor» (00000044).
- El comprobante no se había declarado. Con autorización del usuario, Claude: puso el proveedor al 100%, cambió la Referencia de C003-00001955 a 00000044, canceló el comprobante (id 443; su asiento IVAC/2026/10/0014 quedó cancelado), confirmó la factura y confirmó la retención nueva (id 467).
- Resultado: comprobante **20261000000013** (la localización reutilizó el mismo número), 100%, 220.273,06 Bs, factura 00000044; asiento IVAC/2026/10/0015. Saldo por pagar de la factura: 1.540.227,20 Bs. Se entregó un mensaje corto para el proveedor.

### 9. Pagos y cobros de Profit sin contrapartida (02/11)
Pedido: revisar los cobros/pagos cargados desde Profit que deben tener contrapartida en Odoo (contra el saldo inicial de bancos), sin conexión a Profit.
- 1.673 pagos de Profit (OdooBot, 01/10–29/10) en cuentas transitorias. Apertura de bancos y cajas al 30/09 = saldo de libros de Profit contra la puente `3.9.01.001`. Extractos cargados solo para los bancos en Bs (01/10–28/10).
- 1.015 conciliados con extracto; 68 con línea libre en el extracto (25,5 MM Bs); 2 dobles (Banco del Tesoro, ref. 122554603: la línea del extracto se concilió directo contra la CxC de INVERSIONES SUSHI EXPRES GM, saldo a favor falso de −16.336.952 Bs); 486 en cuentas sin extractos (Regions, Zelle-Binance, Efectivo $, Banco de Venezuela, Caja, Mercantil Panamá, Amerant); 99 sin rastro en el extracto de octubre (25,0 MM Bs: candidatos a estar ya en el saldo de apertura).
- Mercantil Panamá y Amerant quedarían en −US$ 181 mil y −US$ 292 mil: faltan los fondeos (de Profit solo se migraron cobros y pagos, no los movimientos de banco).
- Entrega: `manuales/pagos-profit-contrapartida/Pagos-Profit-sin-contrapartida-AMV.xlsx` y los pasos para corregir. No se aplicó nada (pendiente de autorización: Tesoro y los 68).

### 10. Comisiones del 1.er corte de octubre, Odoo contra Profit (02/11)
Reportes de Profit «Comisiones por cobros» 01/10–15/10 de 8 vendedores contra el corte confirmado de Odoo (`nks_amv_comisiones`).
- Profit US$ 7.273,31 contra Odoo US$ 5.078,79 (−2.194,52). Por tasa −2.313,12: Profit corrió 3% fijo; Odoo paga el adelanto del 2% en el corte del 15 (grupos con escala) y completa al cierre según cumplimiento. Por base +118,40 netos.
- Causas de base: N/DB de diferencial (Profit las comisiona aparte; Odoo aplica todo a la factura con tope), notas de crédito (Profit resta), retenciones de IVA (Profit comisiona), 6 facturas con otro vendedor en Odoo, cobros del 15/10 aplicados el 16/10 en Odoo, 8 documentos de María que Profit no trae.
- Error de Odoo: comisiona AJPM cuyo cliente es el propio vendedor (Albert 11124, Manuel 11120, María 11121).
- Entrega: `manuales/comisiones-1er-corte-octubre/` (PDF de 3 páginas + Excel por documento). No se modificó nada.

### 11. Línea de extracto de INVERSIONES SOJA (03/11)
Captura de la conciliación bancaria de la línea del 08/10, ref. 20418507667, BANCO MERCANTIL 0312, 206.754,60 Bs.
- El asiento MERC1/2026/00631 quedó mal tras varios intentos de Johana Matute (02/11 y 03/11): además del banco y del pago de la factura E001-00017172 (FACT 19151, US$ 203,90 = 178.357,88 Bs a la BCV del 08/10), tiene un débito de 206.754,60 Bs a la CxC del cliente (deuda falsa) y un crédito de 235.151,32 Bs a la transitoria. La línea sigue sin conciliar.
- Lo correcto: banco 206.754,60 / CxC factura 178.357,88 / diferencia 28.396,72 Bs a `8.1.01.0004` (o a favor del cliente). Se explicaron los pasos (Restablecer, agregar la factura, la diferencia a la cuenta, Validar). No se aplicó: falta que el usuario indique si los 28.396,72 Bs van a diferencial o a favor del cliente.

### 12. Libros fiscales de compras y ventas (03/11)
- «Actualizar libro» no traía nada: los períodos predefinidos («Quincena anterior», «Último mes»…) calculan las fechas en el onchange, pero `period_start`/`period_end` son de solo lectura sin `force_save` y no se guardan. Solución temporal: «Personalizado» con fechas a mano. Incidencia para Eulises: `manuales/incidencias-localizacion/libro-fiscal-periodo-sin-fechas.md` (incluye otros 4 defectos de la localización encontrados en la conversación).
- El libro es global por compañía (RIF). El campo «Diarios» permite libros por sucursal, pero cada factura queda en un solo libro (`fb_id`), así que los libros por sucursal reemplazan al global.
- Estado al 03/11: José Oria creó los libros definitivos de la 2.ª quincena de octubre (compras 19 facturas, ventas 237, «Personalizado» 16–31/10). Sobran el primer libro de compras (15/10–31/10, 1 factura) y el libro de ventas «PRUEBA» (retiene 155 facturas del 01 al 15/10). En el libro de compras, NANTONG y FARMERS salen con RIF «VFalse».
- Entrega: `manuales/libros-fiscales/` (instructivo HTML + PDF de 8 páginas con capturas). No se modificó ningún libro.

### 13. Cobros/pagos con fecha 27/11 en vez de 27/10 (03/11)
- 9 recibos de gasto de Barbara Bernal (GASTOS NO FISCALES, C003-00002080 a 00087 y 00093) y 8 pagos del Banesco (PBNK2/2026/00203 a 00210), todos en Bs, con fecha 27/11/2026.
- Con autorización del usuario, Claude los pasó a borrador, les puso fecha 27/10/2026 (fecha contable y de factura), conservó la tasa que puso la usuaria, los confirmó y volvió a conciliar cada recibo con su pago. El pago del recibo C003-00002093 (PBNK2/2026/00222) ya estaba al 27/10.

### 14. Diferencias en cambio (EXCH) con fecha 29/11 (03/11)
38 asientos EXCH de Aribel con fecha 29/11, de cobros que tuvieron esa fecha antes de corregirse al 29/10. Corregidos con autorización del usuario:
- **EXCH/2026/11/0014 (SUPER D´CARLOS) y 0018 (NUEVO SIGLO), activos:** se rehizo la conciliación del cobro con su factura. Odoo revirtió los del 29/11 y creó EXCH/2026/10/2301 (6.874,68 Bs) y 2300 (84,28 Bs) con fecha 31/10. Con la fecha correcta del cobro (29/10, BCV 888,8909) quedaba un residuo en US$ (0,3161 y 0,0949) que se cerró contra `8.2.01.0007` (OPVAR/2026/10/0178 por 272,99 Bs y 0177 por 84,28 Bs). F001-00004106 y F001-00004357 quedan pagadas.
- **Los 20 pares** (original + reversión, neto 0): pasados al 29/10 con números nuevos EXCH/2026/10/2302 a 2341. Cada reversión apunta en su referencia al número nuevo. Quedan huecos en la secuencia EXCH/2026/11.
- **Verificado:** 0 asientos y 0 pagos con fecha futura; 0 borradores en EXCH.
- Se entregó un resumen corto para el consultor (en el chat).

### 15. Saldos por identificar (03/11)
Pedido: camino y forma de registrar los depósitos sin identificar y sacarlos de la cuenta al identificarlos, con PDF para consultor y usuario. Ejemplo: 02/10/2026, ref. 20400501388, crédito inmediato Cámara de Compensación, 414.562,89 Bs.
- Configuración existente: cuenta **1.1.03.001 SALDOS POR IDENTIFICAR** (conciliable, tipo activo corriente con saldo acreedor) y diario **SIN IDENTIFICAR** (MISC1).
- Camino definido: corto (si se conoce el cliente: «Definir contacto» y conciliar con el cobro) o largo: fase 1 «Establecer cuenta» 1.1.03.001 en la conciliación bancaria; fase 2 asiento en SIN IDENTIFICAR (Dr 1.1.03.001 / Cr CxC cliente); fase 3 conciliar las dos líneas de 1.1.03.001 y aplicar el crédito a las facturas.
- Ejemplo: es de EUROBUILDING INTERNACIONAL; el cobro PMERC1/2026/00429 ya existe y está aplicado al cliente, pero la línea del extracto (MERC1/2026/00167) sigue sin conciliar.
- Pendientes de 1.1.03.001 al 03/11: 39 apuntes, −87.325.309,72 Bs (11 SSID de apertura, 25 Mercantil, 2 Banesco, 1 identificación).
- Hallazgos: MISC1/2026/10/0001 (SOJA, 376.954,19 Bs, ref. 20418369711) identifica un depósito que nunca entró a 1.1.03.001 (su línea de 421.785,00 Bs sigue sin conciliar); borrador sobrante en SIN IDENTIFICAR (5.686,69 Bs, duplica MERC1/2026/01548).
- Recomendaciones: modelo de conciliación «SALDO POR IDENTIFICAR»; revisar el tipo de la cuenta.
- Entrega: `manuales/saldos-por-identificar/` (HTML + PDF de 15 páginas con capturas). No se modificó nada (abrir la factura E001-00018944 solo cambió su fecha de modificación).
- **v2 (pedido: «falta un paso, cuando se registra el pago real…»):** la fase 2 queda en dos pasos con dos responsables:
  - **2.1 Cobranzas registra el cobro real** en el diario del **banco** (fecha del depósito, tasa, referencia). Queda «En proceso»: Dr transitoria de cobros del banco (Mercantil 1.1.04.004.2, Banesco 1.1.04.001.2) / Cr CxC, aplicado a las facturas. Ejemplo: PMERC1/2026/00429 (captura 59).
  - **2.2 Contabilidad reclasifica** en SIN IDENTIFICAR: Dr 1.1.03.001 (sin contacto) / Cr **transitoria de cobros** del banco (con el contacto del cliente), ya no contra la CxC.
  - **Fase 3:** dos conciliaciones: 1.1.03.001 (fase 1 con 2.2) y la transitoria de cobros (2.1 con 2.2); el cobro pasa a «Pagado».
  - Razón: las comisiones (`nks_amv_comisiones`) solo cuentan diarios de banco/caja y APERTURA (`nks_comision_diario_cobro_ids` = [432]). Un crédito hecho en SIN IDENTIFICAR contra la CxC no comisiona ni sale en la relación de pagos; queda solo como excepción (5.3).
  - PDF v2 de 18 páginas.

### 16. Cruce de cobros y pagos contra saldos por identificar (03/11)
Consulta de solo lectura: los 28 apuntes de octubre en 1.1.03.001 (sin contar la apertura SSID de Profit) contra 2.575 pagos, por referencia y por monto.
- **Cobro real ya registrado por cobranzas (Aribel Beltran), con el depósito todavía en 1.1.03.001** (fase 1 hecha por Johana Matute). Falta la fase 2.2 o desconciliar la línea del extracto y conciliarla con el cobro:
  - MERC1/2026/01762, ref. 20400628461, 203.342,18 Bs → PMERC1/2026/00423 A&B BOOKCAFE.
  - MERC1/2026/01813, ref. 82558155741, 230.320,00 Bs → PMERC1/2026/00159 RANZAY INFANTE (US$ 230,32).
  - MERC1/2026/01863, ref. 20419070519, 982.890,00 Bs → PMERC1/2026/00426 SUCE EL VIÑEDO (US$ 978).
  - MERC1/2026/01938, ref. 20445559679, 264.095,97 Bs → PMERC1/2026/00425 JALULA (264.096,57: el cobro tiene 0,60 Bs de más).
  - BNK2/2026/01069, ref. 50319205, 92.279,20 Bs → probable PBNK2/2026/00118 INVERSIONES ENMANUEL. Coincide solo el monto: el memo del cobro es la factura E001-00018401. Hay que confirmarlo.
- **APER/2026/10/0001** (Aribel, 29/10): asiento en 0, ref. 20444471393 (depósito MERC1/2026/01582 de 2.513.273 Bs en 1.1.03.001), con las CxC de 4 empresas CRUDOS. Ningún cobro de CRUDOS lleva esa referencia.
- 20 apuntes (−3.496.840,94 Bs) sin ningún cobro relacionado.
- **Hallazgo aparte: el extracto de Banesco 7128 del 27/10 está cargado dos veces.** El estado 35 lo cargó Johan Olivo el 28/10; el estado 41, «del 2026-10-29», se cargó el 30/10 con 115 líneas del 27/10, de las cuales 106 son gemelas (18.103.210,85 Bs netos de más en el banco).
  - En 5 pares están conciliadas las dos copias. Dos son depósitos aplicados a dos clientes distintos:
    - 940036690, 40.181,54 Bs: EMPRENDIMIENTO MORA (PBNK2/2026/00157) y CALIENTICOS LECHERIA (F003-00001344).
    - 45317892, 1.144.130 Bs: INVERSIONES TOMI (PBNK2/2026/00136) y GARY JOSE ALVAREZ (E002-00018744).
  - Los otros 3 pares son comisiones registradas dos veces.
  - BNK2/2026/01069 (en saldos por identificar) tiene su gemela libre en BNK2/2026/01184.
- No se modificó nada en la revisión.
- **Corrección (autorizada: «corrígelo»):**
  - 5 identificaciones en SIN IDENTIFICAR (Dr 1.1.03.001 / Cr transitoria de cobros del banco, conciliadas): MISC1/2026/10/0002 (A&B BOOKCAFE), 0003 (RANZAY, en US$), 0004 (SUCE EL VIÑEDO, en US$), 0005 (JALULA, con 0,60 Bs a 8.2.01.0007) y 0006 (ENMANUEL). Los 5 cobros pasaron a «Pagado». 1.1.03.001 bajó de −87.325.309,72 a −85.552.382,37 Bs.
  - APER/2026/10/0001 (en 0, CRUDOS) eliminado.
  - Banesco 7128: se borraron 145 líneas duplicadas, por 19.560.805,23 Bs:
    - 135 del 27/10 y del 29/10, que estaban repetidas entre los estados 35/41 y 41/42.
    - 9 del 19/10, repetidas entre los estados 27 y 35.
    - BNK2/2026/01184.
  - En cada par se conservó la copia conciliada. Las 38 que quedaron en un estado que no era el de su fecha se movieron a su estado.
  - CHANTILLY: se deshizo la conciliación de 0,16 Bs con la copia sobrante. Los 0,16 se cerraron con OPVAR/2026/10/0179.
  - Los estados 35, 41 y 42 quedaron encadenados, completos y válidos. Los estados empiezan en 0 el 01/10, así que su saldo no es el del banco.
  - Saldo contable de 1.1.04.001 al 30/10: 20.259.073,59 Bs. Al resolver los 2 pares pendientes quedará en 19.074.762,05 Bs. **Johan debe compararlo con el saldo real de Banesco.**
  - Scripts y registros en `tools/historial/`: fix_ssid.py, fix_aper.py, exec_bnk2.py, exec19.py, chant*.py y *_log.json.
- Se entregó un resumen corto para el consultor (en el chat), en tres partes:
  1. Saldos por identificar: los 5 depósitos sacados y APER/2026/10/0001 eliminado.
  2. Banesco: las 145 líneas duplicadas borradas y el saldo de 1.1.04.001 (20.259.073,59 Bs) para comparar con el banco.
  3. Pendiente: definir el cliente de los depósitos 940036690 y 45317892, y registrar los cobros de CRUDOS por el depósito 20444471393.

### 17. Reposición de arroz Kampos: facturas Profit 10502 y 13259 (05/11)
- Pedido: entregar un arroz Kampos que se le debe al cliente (FACT 10502: el arroz se devolvió dañado y el cliente no se llevó el reemplazo). En la FACT 13259 un arroz se entrega sin facturarlo. Además, validar si Profit le dio salida.
- Ninguna de las dos facturas está en Odoo (solo se migraron los saldos abiertos al 30/09). No hay acceso a Profit.
- Hallazgos de configuración:
  - Las órdenes de entrega no generan asiento: el costo se registra al facturar. Por eso una entrega sin factura no lleva el costo a contabilidad.
  - «Muestras y cortesías» manda a una ubicación virtual con cuenta 6.11.01.0005 y genera el asiento STJ al validar.
  - «Virtual Locations/Scrap» e «Inventory adjustment» no tienen cuenta: los desechos SP/00004 y SP/00005 del 04/11 no generaron asiento.
- Propuesta: poner en Scrap la cuenta 8.2.01.0006 PÉRDIDA EN MERCANCÍA DAÑADA y entregar con la operación «Muestras y cortesías», con destino Scrap, el cliente y la referencia a la factura de Profit. Antes, confirmar en Profit que no se emitió nota de crédito por la devolución.
- Se entregó un resumen para el consultor. **No se modificó nada.** Falta la autorización y los datos: sucursal, cliente, cuál arroz y cantidad.

### 18. INVERSIONES SOJA: MERC1/2026/00631 (05/11)
- Depósito del 08/10, ref. 20418507667, por 206.754,60 Bs. Paga la FACT 19151 (E001-00017172) de US$ 203,90 a 1.014,00 Bs/$ (la BCV del 08/10 era 874,7321).
- Johana Matute dejó la conciliación a medias el 03/11: había un débito falso de 206.754,60 Bs en la cuenta por cobrar de SOJA, el EXCH/2026/10/2215 y 235.151,32 Bs en la transitoria.
- Decisión del usuario: tratar el excedente como diferencial, igual que PMERC1/2026/00124 del 22/10 (pagada a 1.003, con EXCH/2026/10/0579).
- Corrección:
  - Se deshizo la conciliación a medias; el EXCH/2026/10/2215 lo revirtió el EXCH/2026/10/2421.
  - La línea del extracto quedó así: Banco 206.754,60 / cuenta por cobrar de SOJA −175.162,93 Bs (−US$ 203,90) / 8.1.01.0004 BENEFICIO EN DIF. CAMBIARIO −31.591,67.
  - La cuenta por cobrar se concilió con la factura: la factura quedó «Pagada» y la línea del extracto conciliada.
  - Un primer intento en Bs dejó US$ 3,65 abiertos y creó el EXCH/2026/10/2422. Se deshizo, y el EXCH/2026/10/2423 lo revirtió (los dos suman cero).
- Se entregó un resumen corto para el consultor (en el chat), con la recomendación de registrar el cobro con la tasa acordada con el cliente (como el 22/10), para que la conciliación no quede a medias.

### 19. Nota de Profit a factura fiscal: E002-00016947 (09/11)
- Pedido: «cámbiala a factura fiscal», copiando exactamente los precedentes.
- Precedentes encontrados:
  - **E002-00017621 → E002-00005991 + F002-00004263** (27/10, Katherine Montoya). Nota de crédito en el mismo diario de saldos iniciales no fiscales, con la misma línea (cuenta 3.9.01.001), conciliada con la nota. Después, factura fiscal nueva en FACTURAS SUCURSAL CARACAS con los productos de Profit, IVA y la tasa del día.
  - E002-00018324 → ENC002-00000616 + F002-00004341 (05 y 06/11).
  - E002-00016983 → ENC002-00000592, ya facturada en fiscal en Profit.
- La nota E002-00016947 es la FACT 38695 de Inversiones Katsuo (US$ 566,28). Aribel le había aplicado hoy el cobro PREGB/2026/00251 (US$ 120,31).
- Hecho:
  - Se desaplicó ese cobro. El EXCH/2026/11/0576 lo revirtió el EXCH/2026/11/0585.
  - Nota de crédito **E002-00005993** (09/11): mismo diario, referencia «Reversión de: E002-00016947, CAMBIO DE NOTA A FACTURA FISCAL», 1 × 566,28 en la 3.9.01.001, tasa 859,0629. Quedó conciliada y la nota pasó a «Revertida».
- **Pendiente:**
  - Que facturación emita la factura fiscal con los productos, cantidades y precios de la FACT 38695 (no están en Odoo).
  - Después, aplicarle el cobro PREGB/2026/00251 (US$ 120,31), que quedó como saldo a favor de Katsuo.

## Cambios hechos en producción por Claude

| Fecha | Registro | Cambio |
|---|---|---|
| 26/10 | LC/2026/0119 | Creado por error (borrador vacío) y luego **borrado** con autorización |
| 26/10 | Factura C003-00001942 y asiento STJ/2026/10/0001 | Solo cambió la fecha de modificación al abrirlos (recálculo de la localización); sin cambios de montos |
| 27/10 | LC/2026/0120 | Línea a US$ 62.078,71 y cuenta 5.1.01.007; reparto manual; **validado** |
| 29/10 | OPVAR/2026/10/0176 | Ajuste de redondeo de US$ 0,015 (12,74 Bs) conciliado con FACT 1891 de MESAMAR |
| 02/11 | GRUPO FERREIRA 001 / C003-00001955 / retención IVA | Proveedor al 100%, Referencia 00000044, comprobante 443 cancelado y nuevo comprobante 20261000000013 al 100% (id 467) |
| 03/11 | 9 recibos C003-00002080..87 y 00093, pagos PBNK2/2026/00203..00210 | Fecha 27/11 → 27/10, misma tasa, conciliados otra vez |
| 03/11 | EXCH del 29/11 (40 asientos) | Pasados a octubre (EXCH/2026/10/2300–2341); OPVAR/2026/10/0177 y 0178 cierran centavos |
| 03/11 | MISC1/2026/10/0002–0006 | 5 depósitos sacados de 1.1.03.001 y conciliados con sus cobros (PMERC1/00423, 00159, 00426, 00425; PBNK2/00118) |
| 03/11 | APER/2026/10/0001 | Asiento en 0 (CRUDOS) eliminado |
| 03/11 | Banesco 7128 (estados 27, 35, 41, 42) | 145 líneas duplicadas borradas (19.560.805,23 Bs), 38 movidas a su estado, saldos de los estados reencadenados; OPVAR/2026/10/0179 cierra 0,16 Bs de CHANTILLY |
| 05/11 | MERC1/2026/00631 (SOJA) | Conciliación rehecha: FACT 19151 pagada, 31.591,67 Bs a 8.1.01.0004; EXCH/2026/10/2215↔2421 y 2422↔2423 revertidos |
| 09/11 | E002-00016947 (Katsuo) | Cobro PREGB/2026/00251 desaplicado (EXCH 0576↔0585); nota de crédito E002-00005993 «CAMBIO DE NOTA A FACTURA FISCAL» |

Todo lo demás fue de solo lectura.

## Pendientes

**Datos en producción (necesitan decisión o datos del usuario)**
- **FACT 1854 de MESAMAR (US$ 237,08):** registrar el pago cuando se sepa el diario y la fecha.
- **Banco del Tesoro (doble):** restablecer la línea ref. 122554603 y conciliarla con los cobros PTESUS/2026/00001 y 00002.
- **68 cobros de Profit** con línea libre en el extracto: conciliar. Cargar extractos de las cuentas en $ y registrar los fondeos de Mercantil Panamá y Amerant.
- **10 pagos con tasa equivocada** (relación de pagos del 27/10): corregir sus asientos.
- **Libros fiscales:** borrar el primer libro de compras (15/10–31/10) y el libro de ventas «PRUEBA»; corregir los RIF «VFalse» (NANTONG, FARMERS) antes de confirmar; crear los libros de la 1.ª quincena de octubre si se declara desde Odoo.

- **Saldos por identificar:** conciliar 20400501388 con PMERC1/2026/00429 (EUROBUILDING); corregir MISC1/2026/10/0001 (SOJA) y eliminar el borrador sobrante del diario SIN IDENTIFICAR. Los cobros reales de CRUDOS para el depósito 20444471393 (2.513.273 Bs).
- **E002-00016947 (Katsuo):** emitir la factura fiscal de la FACT 38695 y aplicarle el cobro PREGB/2026/00251 (US$ 120,31).
- **Reposición de arroz (FACT Profit 10502 y 13259):** autorizar la cuenta de Scrap y pasar sucursal, cliente, arroz y cantidad.
- **Banesco 7128:** decidir a qué cliente corresponden los depósitos 940036690 (40.181,54: EMPRENDIMIENTO MORA o CALIENTICOS LECHERIA) y 45317892 (1.144.130: INVERSIONES TOMI o GARY JOSE ALVAREZ). Después: deshacer la conciliación equivocada, borrar su copia del estado 41 y reencadenar los saldos. Comparar el saldo contable de 1.1.04.001 con el banco.

**Contabilidad y configuración**
- Crear el modelo de conciliación «SALDO POR IDENTIFICAR» y decidir el tipo de la cuenta 1.1.03.001.
- **H1:** asignar cuenta de gastos `5.1.01.007` al producto 1319 (o a la categoría GASTOS OTROS). LC/2026/0120 ya usó 5.1.01.007 en su línea, pero el producto sigue sin cuenta.
- **H2:** crear el costo en destino de la factura C003-00001942.
- **Planilla en el libro de compras:** los campos Nº planilla / fecha / expediente / «Factura SENIAT» solo aparecen si el proveedor es empresa **PJND**. NANTONG está como persona PNNR y SENIAT como persona PNRE. Probar en staging cómo entra la planilla como «Importación» al libro de compras.
- Confirmar con Contabilidad que ADEL 1023 y ADEL 1128 son de OC-00916.
- Ahumado: el costeo dice 18,65 pero con US$ 10.783,79 da 18,6568. Para 18,65 exacto el gasto sería US$ 10.750,00 (requiere otro costo en destino negativo por US$ 33,79).
- Configurar el «Diario Asientos de Redondeo» (Contabilidad › Ajustes). Los ajustes de centavos usaron OPERACIONES VARIAS (`8.1.01.0006` y `8.2.01.0007`).

**Desarrollo**
- **Localización (Eulises):** `force_save` en el período del libro fiscal; tasa del pago al reconfirmar; número de factura en el comprobante de retención; campos de importación solo con PJND. Ver `manuales/incidencias-localizacion/`.
- **Comisiones:** excluir los AJPM del propio vendedor en `nks_amv_comisiones` y decidir con el cliente diferencial, retenciones y notas de crédito.

## Lecciones técnicas (Odoo 19 + localización AMV)

**Formularios y datos**
- Abrir un formulario **«Nuevo»** y salir guarda el borrador (pasó con LC/2026/0119). Para capturas, no abrir formularios nuevos.
- Abrir un **asiento o factura registrada** actualiza su fecha de modificación (recálculo de la localización dual) aunque no cambie nada.
- Un campo de **solo lectura sin `force_save`** no se guarda aunque un onchange le ponga valor (caso del período del libro fiscal).

**Pagos, conciliación y tasas**
- Restablecer a borrador y reconfirmar un pago en $ con tasa propia lo recalcula a la BCV (o a otra tasa): para corregir un pago confirmado, anularlo y crear uno nuevo. Los pagos en Bs no tienen ese problema (el monto contable no depende de la tasa).
- Rehacer por RPC una conciliación de cobro en Bs con factura en US$ usa la BCV de la fecha del cobro, no la tasa del pago; puede dejar centavos en US$ que hay que cerrar.
- Facturas con tres decimales en US$ dejan residuos de centavos al pagar (los pagos van a dos decimales); se cierran con un ajuste conciliado.
- Un asiento de diferencia en cambio que está referenciado por una conciliación no se puede pasar a borrador; hay que deshacer la conciliación (Odoo lo revierte) y rehacerla.
- Un asiento con número de un mes (EXCH/2026/11/…) no se confirma con fecha de otro mes: hay que limpiar el número (`name = '/'`) en borrador para que tome uno nuevo. Al confirmar un par original/reversión, Odoo los vuelve a conciliar solo.

**Fiscal**
- El comprobante de retención de IVA imprime como número de factura el campo **Referencia** de la factura de proveedor. Al cancelar y regenerar una retención, la localización reutiliza el número asignado (`iva_number_asignado`).
- Cada factura queda en un solo libro fiscal (`fb_id`); un libro de prueba deja vacío al definitivo.

**Inventario y costos en destino**
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
| `historial/` | Scripts que escribieron en producción, para trazabilidad. No reejecutar. LC 119 (`del119.py`), LC 120 (`apply120.py`, `val120.py`), MESAMAR (`fix1891.py`), GRUPO FERREIRA (`fix_ferreira_1..4.py`), fechas 27/11 (`fix2711.py`, `fix2093.py`) y EXCH 29/11 (`fix_exch_activo.py`, `cierre_residuo.py`, `fix_par.py`, `postear_par.py`, `restaurar_par.py`, `fix_refs.py`). |
