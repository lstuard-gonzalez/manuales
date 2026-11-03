# Libro fiscal: «Quincena anterior» no guarda las fechas del período

**Para:** Eulises (nks_localizacion)
**Cliente:** Alimentos MonteVerde C.A. · producción `alimentos-monteverde.odoo.com` · Odoo 19
**Módulo:** el que define `account.fiscal.book` (libros de compra y venta)
**Fecha:** 03/11/2026
**Severidad:** alta. Los libros creados con un período predefinido quedan sin fechas y no traen documentos.

## Síntoma

Al crear un libro fiscal y elegir **Período = «Quincena anterior»** (o cualquier período que no sea «Personalizado»), el formulario muestra las fechas. Al guardar, **«Período Inicio» y «Período Fin» quedan vacíos**, y «Actualizar libro» no trae ninguna línea.

Caso en producción: `account.fiscal.book` id **18** («PRUEBA», libro de compra, `time_period = last_fortnight`), creado el 03/11 a las 09:43. Tiene `period_start` y `period_end` vacíos y 0 líneas.

## Causa

El cálculo está bien: el onchange de `time_period` devuelve las fechas correctas. Lo probé por RPC sin guardar, con «hoy» = 03/11/2026:

| `time_period` | `period_start` | `period_end` |
|---|---|---|
| `last_fortnight` | 2026-10-16 | 2026-10-31 |
| `this_fortnight` | 2026-11-01 | 2026-11-15 |
| `last_month` | 2026-10-01 | 2026-10-31 |
| `this_month` | 2026-11-01 | 2026-11-30 |

El problema es la vista del formulario:

```xml
<field name="period_start" class="oe_inline" readonly="time_period != 'custom' or state != 'draft'"/>
<field name="period_end"   class="oe_inline" readonly="time_period != 'custom' or state != 'draft'"/>
```

En Odoo 17, 18 y 19 el cliente web **no envía al guardar los campos que están en solo lectura**, aunque un onchange les haya puesto valor, salvo que la vista los marque con `force_save="1"`. Como los dos campos son de solo lectura en todos los períodos menos «Personalizado», el valor calculado se pierde al guardar. Son campos almacenados y no calculados (`store=True`, sin `depends`), así que nada los vuelve a llenar.

## Corrección propuesta

Agregar `force_save="1"` a los dos campos en la vista del formulario de `account.fiscal.book`:

```xml
<field name="period_start" class="oe_inline" force_save="1"
       readonly="time_period != 'custom' or state != 'draft'"/>
<field name="period_end" class="oe_inline" force_save="1"
       readonly="time_period != 'custom' or state != 'draft'"/>
```

Es compatible con Odoo 18 y 19: `force_save` existe y funciona igual en las dos versiones.

Una alternativa más robusta es calcular las fechas en el servidor, con un `compute` almacenado y `readonly=False` que dependa de `time_period`. Así también quedan bien los libros creados por código o importados, que no pasan por el onchange.

## Prueba sugerida

`Form` simula el cliente web, así que reproduce el defecto: falla sin `force_save` y pasa con él. Hay que ajustar los campos obligatorios del modelo si hay más que estos.

```python
# -*- coding: utf-8 -*-
from freezegun import freeze_time

from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLibroFiscalPeriodo(TransactionCase):
    """El período predefinido de un libro fiscal debe quedar guardado."""

    @freeze_time('2026-11-03')
    def test_quincena_anterior_guarda_fechas(self):
        """«Quincena anterior» guarda del 16 al fin del mes anterior."""
        form = Form(self.env['account.fiscal.book'])
        form.name = 'Prueba quincena anterior'
        form.type = 'purchase'
        form.time_period = 'last_fortnight'
        libro = form.save()
        self.assertEqual(str(libro.period_start), '2026-10-16')
        self.assertEqual(str(libro.period_end), '2026-10-31')

    @freeze_time('2026-11-03')
    def test_mes_anterior_guarda_fechas(self):
        """«Último mes» guarda el mes completo anterior."""
        form = Form(self.env['account.fiscal.book'])
        form.name = 'Prueba mes anterior'
        form.type = 'sale'
        form.time_period = 'last_month'
        libro = form.save()
        self.assertEqual(str(libro.period_start), '2026-10-01')
        self.assertEqual(str(libro.period_end), '2026-10-31')
```

## Mientras se corrige

En el libro, elegir **«Personalizado»**, escribir las fechas a mano, guardar y pulsar «Actualizar libro». Con «Personalizado» los campos son editables y sí se guardan.

## Relacionado (datos en producción, sin tocar)

- **Libro id 16** («Libro de Compras 2da Quin Octubre», José Oria): `time_period = last_fortnight`, pero quedó del **15/10** al 31/10. Probablemente se escribió en «Personalizado» y luego se cambió el período. Incluye la factura C003-00001933 (MESAMAR, del 15/10), que es de la primera quincena.
- **Cada factura queda ligada a un solo libro** (`account.move.fb_id`). Un segundo libro del mismo tipo y período sale vacío aunque tenga fechas: los libros «PRUEBA» (id 17 de venta, id 18 de compra) no van a traer nada mientras exista el libro 16. Conviene borrarlos.

## Otros defectos de la localización encontrados en AMV (para la misma revisión)

1. **Pago reconfirmado pierde la tasa del pago** (`account_dual_currency`). Si se restablece a borrador un pago en $ con tasa propia, se edita y se vuelve a confirmar, el asiento se recalcula a la BCV de la fecha (o a otra tasa) y no a `tax_today`. Hay 10 casos en la relación de pagos del 27/10 de Aribel Beltran (PMERC1/2026/00153, 00163, 00164, 00179, 00192, 00193, 00209, 00231, 00271, 00286), con una diferencia de 303.090,52 Bs.
2. **Comprobante de retención de IVA:** imprime como número de factura el campo **Referencia** de la factura (`ref`), no `supplier_invoice_number`. Caso GRUPO FERREIRA 001: salía 00000043 con la factura 00000044. Al cancelar y regenerar la retención se reutiliza el número (`iva_number_asignado`), y el comprobante cancelado conserva el mismo número.
3. **Campos de importación de la factura de proveedor** (Nº de planilla, fecha, Nº de expediente, «Factura SENIAT»): solo aparecen con proveedores **empresa PJND**. Hay proveedores del exterior cargados como persona (NANTONG SAILING está como PNNR), y con ellos no se pueden usar.
4. **Opción «Diario Asientos de Redondeo»** (`nikko_rounding_journal_id`): está vacía en AMV.
