# Responsabilidad Social

## 1. Diseño inclusivo
- HTML semántico, atributo `lang="es"`, enlace «Saltar al contenido» y navegación completa por teclado.
- Etiquetas asociadas a cada campo, texto de ayuda, tablas con encabezados y leyendas, y estado de foco visible.
- Modo claro y oscuro automático, diseño adaptable a móvil y respeto a la preferencia de movimiento reducido.
- Funciona sin JavaScript: utilizable en dispositivos antiguos y con conexiones lentas.
- Pendiente: auditoría con Lighthouse y prueba con un lector de pantalla real.

## 2. Transparencia
La página «Acerca y privacidad» muestra la fórmula de cálculo y los factores usados. Las recomendaciones se basan en reglas simples y explicables, no en modelos opacos. La aplicación comunica que sus cifras son **estimaciones**, no mediciones oficiales.

## 3. Privacidad y datos
- Se recopila solo lo necesario: periodo, tipo y cantidad.
- Sin cuentas, cookies de seguimiento, analítica ni recursos de terceros.
- La persona usuaria puede **descargar** y **eliminar** todos sus datos en cualquier momento.

## 4. Seguridad
| Riesgo | Control |
|---|---|
| Inyección SQL | Consultas parametrizadas y restricciones en la tabla |
| XSS | Escape automático de plantillas y política de seguridad de contenido restrictiva |
| CSRF | Token en formularios que modifican datos |
| Entradas inválidas | Validación estricta de periodo, tipo y rango de cantidad |
| Secretos | `SECRET_KEY` por variable de entorno |
| Dependencias vulnerables | `pip-audit` semanal en CI |

## 5. Responsabilidad ambiental
Toda la aplicación está diseñada para consumir lo mínimo (ver documentos 03 y 04) y su propósito es ayudar a reducir el consumo energético de las personas usuarias.

## 6. Limitaciones y compromisos
- Sin autenticación: apta para uso personal o red local; si se expone a internet debe añadirse acceso controlado y HTTPS.
- Cubre solo electricidad y gas LP.
- Los factores son referenciales y deben actualizarse con fuentes oficiales.
