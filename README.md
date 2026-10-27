# Manuales

Manuales de configuración y uso de Odoo con capturas reales, elaborados en conversaciones con Claude.

## Cómo está organizado

- **Una rama por conversación.** El nombre es `AAAA-MM-DD-cliente-tema` (fecha de inicio de la conversación).
- Cada rama contiene:
  - `CONVERSACION.md`: resumen para retomar la conversación (contexto, pedidos, entregas, cambios hechos en producción, pendientes).
  - `manuales/<tema>/`: cada manual en HTML (`index.html` + `img/`) y en PDF.
  - `fuentes/`: archivos que mandó el cliente (Excel, etc.).
  - `tools/`: scripts usados para capturas, PDF y consultas de solo lectura.
- `main` solo tiene este índice.

**Para retomar una conversación:** abre una sesión nueva con este repo, cambia a la rama de la conversación y pídele a Claude que lea `CONVERSACION.md`.

## Conversaciones

| Rama | Cliente | Temas | Manuales |
|---|---|---|---|
| `2026-10-26-amv-costos-destino-importaciones` | Alimentos MonteVerde C.A. (Odoo 19) | Costos en destino, importaciones con anticipos y nacionalización, costeo del salmón | Costos en destino · Importaciones: factura del proveedor, anticipos y nacionalización |
