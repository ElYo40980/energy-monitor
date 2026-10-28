# Informe de Mantenimiento Sostenible

## 1. Estrategia
Mantener la aplicación con el menor esfuerzo y consumo posibles: poco código, pocas dependencias, verificación automática y una línea base medible para detectar regresiones.

## 2. Prácticas implementadas
| Práctica | Implementación | Evidencia |
|---|---|---|
| Optimización del código | Lógica pura y pequeña; consultas con índice (periodo, tipo); resumen acotado a 12 meses | `carbon.py`, `db.py` |
| Gestión eficiente de recursos | Conexión por solicitud cerrada en `teardown`; un solo worker; caché de estáticos de 7 días | `app.py` |
| Automatización | CI con pruebas, benchmark y `pip-audit` en cada cambio y cada lunes | `.github/workflows/ci.yml` |
| Monitoreo del rendimiento | Ruta `/salud` y `bench.py` como línea base de latencia, memoria y tamaño | `bench.py` |
| Dependencias mínimas | Solo Flask y gunicorn | `requirements.txt` |
| Configuración externa | Factores y rutas por variables de entorno | `carbon.py`, `app.py` |
| Pruebas | 10 pruebas (cálculo, validación, CSRF, escape, exportación, borrado, cabeceras) | `tests/test_app.py` |

## 3. Procedimientos
**Actualizar factores de emisión:** cambiar `FE_ELECTRICIDAD` o `FE_GAS_LP`, reiniciar. Sin tocar código.

**Actualizar dependencias:** revisar el reporte semanal de `pip-audit`, actualizar `requirements.txt`, ejecutar `pytest -q` y `python bench.py`, y comparar con la línea base.

**Detectar regresiones de rendimiento:** ejecutar `bench.py` antes y después de cada cambio relevante. Línea base actual: 2.90 ms por solicitud, 297 KiB de memoria pico, 8.5 KiB por vista.

**Respaldo:** copiar el archivo SQLite (`DB_PATH`) o usar la exportación CSV.

## 4. Eficiencia del propio proceso de desarrollo
El CI cancela ejecuciones obsoletas, usa caché de pip y tiene un límite de 10 minutos para no desperdiciar cómputo. Las pruebas completas tardan 0.27 s.

## 5. Mejoras recomendadas
1. Agregar al CI un umbral de regresión (por ejemplo, fallar si la latencia supera el doble de la línea base).
2. Registrar los resultados de `bench.py` por versión.
3. Medir el consumo real con CodeCarbon y sustituir las estimaciones del documento 03.
4. Añadir respaldos automáticos si se despliega para varias personas.
