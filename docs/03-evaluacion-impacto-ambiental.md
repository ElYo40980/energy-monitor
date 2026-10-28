# Evaluación del Impacto Ambiental

Análisis del ciclo de vida (LCA) simplificado, siguiendo la estructura de ISO 14040/14044, y estimación de la huella de carbono.

> **Aviso de rigor:** las cifras de energía son **estimaciones** basadas en supuestos explícitos, no mediciones de hardware. Los resultados de `bench.py` sí son mediciones, pero del software en un entorno de desarrollo. Antes de presentar cifras como definitivas deben validarse con las herramientas de la sección 7.

## 1. Objetivo y alcance
- **Objetivo:** estimar el impacto climático de desarrollar, operar y retirar la aplicación y orientar decisiones de diseño.
- **Unidad funcional:** operar la aplicación durante un año para un hogar o un grupo reducido de usuarios.
- **Indicador:** kg CO₂e (cambio climático). No se evalúan otros impactos (agua, materiales, toxicidad).

## 2. Límites del sistema
| Etapa | Incluida | Observación |
|---|---|---|
| Desarrollo y CI | Cualitativa | Energía de equipos y ejecuciones de CI |
| Fabricación del hardware | Excluida | Se asume infraestructura compartida existente |
| Distribución (red) | Cuantificada | Bytes por visita |
| Operación (servidor) | Cuantificada | Etapa dominante |
| Mantenimiento | Cualitativa | Despliegues, actualizaciones, auditorías |
| Fin de vida | Cualitativa | Exportación y borrado de datos |

## 3. Inventario
**Mediciones (`bench.py`, 2,000 lecturas, 200 solicitudes):**

| Métrica | Resultado |
|---|---|
| Latencia media GET / | 2.90 ms |
| Memoria pico de Python | 297 KiB |
| HTML | 6.7 KiB |
| CSS | 1.8 KiB |
| Total por vista | ≈ 8.5 KiB |
| Pruebas | 10 de 10 aprobadas en 0.27 s |

**Supuestos:** servidor virtual pequeño con consumo atribuible entre 5 y 20 W de forma continua (8,760 h/año) y factor eléctrico referencial de 0.438 kg CO₂e/kWh.

## 4. Evaluación del impacto: huella operativa
Emisiones = potencia × 8,760 h × factor.

| Escenario | Potencia atribuible | Energía anual | Emisiones anuales |
|---|---|---|---|
| Optimista | 5 W | 43.8 kWh | ≈ 19.2 kg CO₂e |
| **Base** | **10 W** | **87.6 kWh** | **≈ 38.4 kg CO₂e** |
| Pesimista | 20 W | 175.2 kWh | ≈ 76.7 kg CO₂e |

**Transferencia de datos:** 1,000 visitas × 8.5 KiB ≈ 8.3 MiB, una cantidad despreciable frente al consumo del servidor.

## 5. Interpretación
1. La **operación del servidor domina** el impacto; el peso de la página influye poco en términos absolutos.
2. La principal palanca es **reducir la potencia atribuible**: compartir infraestructura, evitar entornos ociosos y apagar los no productivos.
3. Otra palanca es el **lugar de despliegue**: una región con menor intensidad de carbono reduce las emisiones sin cambiar el código.
4. La incertidumbre es alta (factor de 4 entre escenarios). Por eso la aplicación y los documentos presentan resultados como estimaciones.
5. El diseño ligero reduce el costo por visita y permite usar hardware modesto, lo que alarga la vida útil de los equipos.

## 6. Medidas de mitigación adoptadas
Sin JavaScript ni recursos externos, SQLite en lugar de un servicio de base de datos, consultas indexadas y agregadas en SQL, caché de estáticos de siete días, un solo proceso, CI con cancelación de ejecuciones obsoletas y tiempo límite.

## 7. Herramientas de medición recomendadas
- **CodeCarbon** o **Scaphandre**: consumo energético del proceso en ejecución.
- **Cloud Carbon Footprint**: si se despliega en un proveedor de nube.
- **Website Carbon Calculator**: costo por visita.
- **Lighthouse**: rendimiento y accesibilidad.

## 8. Limitaciones
Alcance limitado a cambio climático, hardware excluido, potencia supuesta y factor referencial (verificar el valor vigente de la autoridad competente).
