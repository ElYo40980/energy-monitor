# Manual de Usuario

## 1. Requisitos
- Python 3.10 o superior
- pip
- Un navegador moderno

## 2. Instalación
```bash
git clone <URL-de-tu-repositorio>
cd energy-monitor
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configuración
| Variable | Para qué sirve | Por defecto |
|---|---|---|
| `SECRET_KEY` | Clave de sesión (obligatoria en producción) | Se genera una temporal |
| `DB_PATH` | Ruta del archivo SQLite | `energia.db` |
| `FE_ELECTRICIDAD` | Factor kg CO₂e por kWh | 0.438 |
| `FE_GAS_LP` | Factor kg CO₂e por kg | 2.99 |

Los factores por defecto son referenciales: verifica el valor vigente publicado por la autoridad competente.

```bash
export SECRET_KEY="una-clave-larga-y-aleatoria"
export FE_ELECTRICIDAD=0.438
```

## 4. Ejecución
- Desarrollo: `python app.py` y abrir http://127.0.0.1:5000
- Producción: `gunicorn -w 1 "app:create_app()"`

## 5. Uso
1. **Registrar consumo:** elige el periodo, el tipo (electricidad o gas LP) e ingresa la cantidad que aparece en tu recibo. Pulsa *Guardar lectura*.
2. **Leer el resumen:** la tabla muestra el consumo y los kg CO₂e por mes; la barra indica la proporción respecto al mes más alto.
3. **Variación:** compara cada tipo de consumo con el mes anterior.
4. **Recomendaciones:** se generan con reglas simples según tus tendencias.
5. **Descargar tus datos:** enlace *Descargar mis datos (CSV)*.
6. **Eliminar tus datos:** botón *Eliminar todos mis datos* (no se puede deshacer).

## 6. Mensajes de error comunes
| Mensaje | Causa |
|---|---|
| El periodo debe tener formato AAAA-MM | Fecha mal escrita |
| Selecciona un tipo de consumo válido | Tipo no permitido |
| Ingresa una cantidad numérica válida | Valor negativo, vacío o no numérico |

## 7. Pruebas
```bash
pip install pytest
pytest -q
python bench.py
```

## 8. Solución de problemas
- *El puerto 5000 está ocupado:* ejecuta `flask --app app run --port 5001`.
- *Las sesiones se cierran al reiniciar:* define `SECRET_KEY` de forma fija.
- *Los factores no cambian:* reinicia la aplicación tras modificar las variables de entorno.
