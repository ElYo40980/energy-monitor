# Descripción del Proyecto

## Objetivo
Ofrecer una aplicación web de **bajo impacto ambiental** que ayude a una persona o un hogar a registrar su consumo de electricidad y gas LP, estimar las emisiones asociadas y reducirlas, respetando su privacidad.

## Alcance
**Incluye:** registro mensual de consumo, cálculo de kg CO₂e, comparación con el mes anterior, recomendaciones basadas en reglas, exportación a CSV y borrado total de datos.

**No incluye (limitaciones conocidas):** autenticación y multiusuario (pensada para uso personal o red local), otras fuentes de consumo (agua, combustibles de transporte), medición automática de medidores.

## Características principales
| Característica | Detalle |
|---|---|
| Registro de consumo | Periodo (AAAA-MM), tipo (electricidad kWh, gas LP kg) y cantidad |
| Huella de carbono | consumo × factor de emisión (configurable) |
| Resumen | Últimos 12 meses con datos, variación porcentual y recomendaciones |
| Datos del usuario | Descarga en CSV y eliminación total |
| Transparencia | Página «Acerca y privacidad» con factores y fórmula |
| Accesibilidad | Teclado, etiquetas, contraste, modo oscuro, sin JavaScript |

## Arquitectura
Aplicación monolítica mínima: `carbon.py` (lógica pura), `db.py` (SQLite), `app.py` (rutas, validación, seguridad), plantillas HTML y 1.8 KiB de CSS. Un solo proceso, sin servicios externos.

## Tecnologías
Python 3, Flask, SQLite, pytest, GitHub Actions.

## Principios de sostenibilidad aplicados
Minimizar recursos (página de 8.5 KiB, sin recursos de terceros), simplicidad (pocas dependencias), reutilización (lógica aislada y configurable), ciclo de vida completo (exportación y borrado de datos) y medición continua (`bench.py`). El detalle está en los documentos 03 y 04.
