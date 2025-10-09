# Proyecto: Análisis de Ventas – Tienda Aurelion

---

## Tema, problema y solución

Tema

- Análisis descriptivo de un conjunto de datos de ventas minoristas para la tienda (clientes, productos, ventas y detalle de ventas). Los datos permiten estudiar comportamientos de compra, ingresos por producto y análisis por ciudad y medio de pago.

Problema

- Los archivos entregados están en CSV separados y sin documentación formal. Esto dificulta su reutilización, la verificación de calidad de datos y la reproducibilidad de análisis.
- Preguntas concretas que surgen de los datos:
  - ¿Qué productos generan mayor ingreso total?
  - ¿Cuáles son los productos con mayor volumen (cantidad vendida)?
  - ¿Qué medios de pago son más usados por ciudad?
  - ¿Hay inconsistencias entre precios en `productos.csv` y `detalle_ventas.csv`?

Solución

- Entregar documentación técnica que describa cada dataset, su estructura, tipos y escala de medición. Además, proporcionar un script interactivo en Python (`consulta_documentacion.py`) que permita explorar la documentación y los CSV (esquema y filas de ejemplo), facilitando respuestas rápidas a las preguntas anteriores y sirviendo como base para análisis posteriores.

Los archivos fuente mencionados y su relación con las preguntas anteriores:

- `clientes.csv` — identifica clientes y ciudad de residencia (permite análisis por ciudad y recuento de clientes activos).
- `productos.csv` — catálogo y precios de referencia (permite calcular ingresos totales y detectar discrepancias con precios en `detalle_ventas.csv`).
- `ventas.csv` — cabecera de cada operación (fecha, cliente, medio de pago) — necesario para análisis temporales y por medio de pago.
- `detalle_ventas.csv` — líneas de venta por producto (cantidad, precio_unitario, importe) — usado para calcular ingresos por producto y verificar consistencia de montos.

---

## Dataset de referencia (detalle por archivo: definición, estructura, tipos y escala de medición)

Fuente de datos:

- `clientes.csv`
- `productos.csv`
- `ventas.csv`
- `detalle_ventas.csv`

clientes.csv

- Descripción: registro de clientes.
- Columnas:
  - `id_cliente` — entero — tipo: identificador; escala: nominal (clave única por cliente).
  - `nombre_cliente` — texto — escala: nominal.
  - `email` — texto — escala: nominal (identificación de contacto; puede repetirse o cambiar).
  - `ciudad` — texto — escala: nominal (unidad geográfica).
  - `fecha_alta` — fecha (YYYY-MM-DD) — escala: intervalo/temporal (permite ordenar por antigüedad).

productos.csv

- Descripción: catálogo de productos y precios de referencia.
- Columnas:
  - `id_producto` — entero — identificador (nominal).
  - `nombre_producto` — texto — nominal.
  - `categoria` — texto — nominal (p. ej. Alimentos, Limpieza).
  - `precio_unitario` — entero (moneda en unidad mínima, p. ej., centavos) — escala: razón (ratio).

ventas.csv

- Descripción: cabecera de las ventas (registro por operación).
- Columnas:
  - `id_venta` — entero — identificador (nominal).
  - `fecha` — fecha (YYYY-MM-DD) — escala: intervalo/temporal.
  - `id_cliente` — entero — clave foránea a `clientes.id_cliente` (nominal).
  - `nombre_cliente` — texto — réplica para trazabilidad (nominal).
  - `email` — texto — réplica (nominal).
  - `medio_pago` — texto — nominal (categorías: efectivo, qr, tarjeta, transferencia).

detalle_ventas.csv

- Descripción: detalle de líneas por venta (productos vendidos).
- Columnas:
  - `id_venta` — entero — clave foránea a `ventas.id_venta` (nominal).
  - `id_producto` — entero — clave foránea a `productos.id_producto` (nominal).
  - `nombre_producto` — texto — nominal.
  - `cantidad` — entero — escala: razón (unidades vendidas).
  - `precio_unitario` — entero — escala: razón.
  - `importe` — entero — escala: razón (subtotal por línea; esperado igual a `cantidad * precio_unitario`).

Calidad y notas

- Hay redundancia intencional en las tablas (`nombre_cliente` y `email` aparecen en `ventas.csv`, `nombre_producto` y `precio_unitario` aparecen en `detalle_ventas.csv`). Esta redundancia facilita auditoría pero puede originar inconsistencias si no se sincroniza con el catálogo (`productos.csv`).
- Se observan nombres y emails duplicados en `clientes.csv` (mismo nombre con distinto email), por lo que se recomienda usar `id_cliente` para joins.
- Los precios están en enteros; antes de reportes financieros conviene convertir a formato decimal (dividir por 100 si se trabaja en centavos) o documentar la unidad monetaria.

---

## Información, pasos, pseudocódigo y diagrama del programa

Objetivo del script

- Permitir al usuario consultar la documentación (`DOCUMENTACION.md`) y explorar los CSV disponibles mediante una interfaz de línea de comandos (CLI) segura y robusta.

Pasos de alto nivel

1. Cargar `DOCUMENTACION.md`.
2. Detectar los CSV presentes en la carpeta del script.
3. Permitir acciones del usuario: mostrar secciones de la documentación, listar CSV, mostrar esquema de un CSV, mostrar filas de ejemplo, buscar texto en la documentación.
4. Manejar errores (archivo faltante, CSV corrupto, codificación) y mostrar mensajes de ayuda.

Pseudocódigo (versión final)

```text
Inicio
  Cargar DOCUMENTACION.md en memoria
  Detectar CSV disponibles en la carpeta del proyecto
  Mientras el usuario no seleccione salir:
    Mostrar menú con opciones
    Leer opción
    Si opción == mostrar resumen:
      Imprimir sección "Tema, problema y solución"
    Si opción == listar datasets:
      Imprimir archivos CSV detectados
    Si opción == esquema CSV:
      Pedir nombre de archivo; leer encabezado y tipos inferidos; mostrar
    Si opción == ejemplo CSV:
      Pedir nombre de archivo; mostrar primeras N filas
    Si opción == buscar en doc:
      Pedir palabra clave; buscar y listar líneas encontradas
    Si opción == pseudocódigo/diagrama:
      Mostrar la sección de pseudocódigo y diagrama
  Fin Mientras
Fin
```

Diagrama de componentes (ASCII)

DOCUMENTACION.md <-- archivo principal con secciones
|
+--> script: `consulta_documentacion.py` (lee MD y CSVs)
|
+--> Operaciones: listar CSVs, leer esquema, mostrar ejemplos, búsqueda en doc

Flujo de datos simplificado

CSV files (clientes.csv, productos.csv, ventas.csv, detalle_ventas.csv)
|
+--> `consulta_documentacion.py` (lectura con csv.DictReader)
|
+--> Salida al usuario (CLI): tablas de esquema, muestras de filas, resultados de búsqueda

---

## Sugerencias y mejoras (aplicadas con Copilot, aceptadas y descartadas)

Durante el desarrollo se consultaron sugerencias de Copilot. A continuación se listan las recomendaciones más relevantes y la decisión tomada.

1. Interfaz gráfica (tkinter) para navegar la documentación.

   - Decisión: descartada por ahora.
   - Razón: añade complejidad y dependencias; la entrega requiere un programa interactivo sencillo y portable en CLI.

2. Inferencia automática de tipos y conversión de precios a decimal.

   - Decisión: aceptada parcialmente.
   - Implementación: el script incluye una inferencia básica de tipos (int/float/date/str) y muestra los tipos detectados para cada columna. La conversión a decimal (ej. dividir por 100) se dejó como mejora documentada para evitar suposiciones sobre la unidad monetaria en los CSV.

3. Pruebas unitarias (pytest) para validar lectura de CSVs.

   - Decisión: aceptada como recomendación.
   - Estado: no implementado en esta entrega por restricciones de tiempo; se incluye en `instrucciones_copilot.md` como tarea prioritaria.

4. Exportar reportes (HTML/PDF) desde la documentación.

   - Decisión: descartada en esta entrega (propuesta para fases posteriores).

5. Manejo de CSVs grandes (muestreo y límites).

   - Decisión: aceptada parcialmente.
   - Implementación: el script muestrea las primeras N filas (configurable) en lugar de cargar archivos completos en memoria.

6. Normalizar codificaciones (forzar UTF-8 y manejo de errores de decoding).
   - Decisión: aceptada.
   - Implementación: el programa abre archivos con encoding='utf-8' y captura excepciones para indicar problemas de codificación.

Registro de cambios y mejoras futuras recomendadas

- Añadir pruebas unitarias para `read_csv_schema` y `load_documentation`.
- Añadir opción para convertir y mostrar precios en unidades decimales, con parámetro de configuración (p. ej., 'centavos' true/false).
- Agregar validación cruzada entre `productos.csv` y `detalle_ventas.csv` para detectar discrepancias en `precio_unitario`.
- Implementar paginación y búsqueda avanzada en la CLI.

---

## Contacto

Para más información o mejoras, contactar al responsable del proyecto (repositorio local en la carpeta del entregable).
