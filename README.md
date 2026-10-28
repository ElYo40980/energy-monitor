# Monitor de Consumo Energético

Aplicación web ligera (Flask + SQLite) para registrar consumo de electricidad y gas LP, estimar la huella de carbono y recibir recomendaciones simples. Proyecto final de Ingeniería de Software Sostenible.

## Documentación

1. [Descripción del Proyecto](docs/01-descripcion-del-proyecto.md)
2. [Manual de Usuario](docs/02-manual-de-usuario.md)
3. [Evaluación del Impacto Ambiental](docs/03-evaluacion-impacto-ambiental.md)
4. [Informe de Mantenimiento](docs/04-informe-de-mantenimiento.md)
5. [Responsabilidad Social](docs/05-responsabilidad-social.md)

## Ejecutar

```bash
pip install -r requirements.txt
export SECRET_KEY="cambia-esto"      # obligatorio en producción
python app.py                        # http://127.0.0.1:5000
# producción: gunicorn -w 1 "app:create_app()"
```

## Pruebas y eficiencia

```bash
pip install pytest
pytest -q          # 10 pruebas
python bench.py    # latencia, memoria pico y tamaño de página
```

## Estructura

| Archivo | Responsabilidad |
|---|---|
| `carbon.py` | Cálculo de CO₂e y recomendaciones (lógica pura, sin E/S) |
| `db.py` | Acceso a SQLite con consultas parametrizadas |
| `app.py` | Rutas, validación, CSRF y cabeceras de seguridad |
| `templates/`, `static/` | HTML accesible y CSS de 1.8 KiB, sin JS ni recursos externos |
| `.github/workflows/ci.yml` | CI: pruebas, benchmark y auditoría de dependencias |

## Configuración

- `DB_PATH`: ruta del archivo SQLite (por defecto `energia.db`).
- `SECRET_KEY`: clave de sesión.
- `FE_ELECTRICIDAD`, `FE_GAS_LP`: factores de emisión (kg CO₂e por kWh / kg). Los valores por defecto son referenciales; verifica el factor vigente publicado por la autoridad competente.

## Decisiones de sostenibilidad

Sin JavaScript ni fuentes externas, agregaciones en SQL, caché de estáticos, un solo proceso, CI con cancelación de ejecuciones obsoletas, sin rastreadores, y exportación y borrado de datos disponibles para la persona usuaria.
