# Notas de curación — Indicadores INAU (Sistema de Protección Especial)

Fecha de procesamiento: 2026-08-17.
Fuente: archivos Excel publicados por INAU, copiados en `data/inau/`.
Herramientas: Python (openpyxl, pandas). Codificación de salida: UTF-8 con BOM (`utf-8-sig`), separador coma.

## 1. Mapeo hoja → CSV

| Archivo de origen | Hojas usadas | CSV de salida |
|---|---|---|
| `2020-2025/indicadoresanualesspe-inau2020-2025.xlsx` | 29 hojas `TD.x.y` (tablas de datos) + 29 hojas `FT.x.y` (nombre, dimensión y unidad de cada indicador) | `inau_spe_nacional.csv` |
| `2020-2025/departamentos/datosspe<depto>-3.xlsx` (19 archivos) | Hojas `TD.1` a `TD.24` + `FT.1` a `FT.24` (nombres) | `inau_spe_departamental.csv` |
| `2025/reporte_poblacion_y_proyectos_abr2025.xlsx` | `Cuadro 1` a `Cuadro 10` | `inau_abril2025_poblacion.csv` |
| `2025/reporte_acogimiento_familiar_abr2025.xlsx` | `Cuadro 1` a `Cuadro 7` | `inau_abril2025_acogimiento.csv` |
| `2025/reporte_derecho_vivir_en_familia_abr2025.xlsx` | `Cuadro 1` a `Cuadro 3` | `inau_abril2025_dvf.csv` |

Quedaron fuera en todos los casos: hojas de portada, presentación, índice, glosario, descripciones de propuestas de atención y hojas de gráficos (contenido textual o gráfico, sin datos tabulares nuevos). Las fichas técnicas (`FT.*`) se usaron solo como fuente de metadatos (nombre del indicador, dimensión).

Nota sobre la cantidad de indicadores nacionales: la documentación del INAU habla de 26 indicadores, pero el archivo contiene 29 hojas `TD` (los códigos 1.1–1.5, 2.1–2.3, 3.1–3.2, 4.1–4.2, 5.1–5.4, 6.1–6.2, 7.1–7.2, 8.1–8.2, 9.1, 10.1, 11.1–11.3, 12.1 y 13.1). Se incluyeron las 29 tablas completas, con todas sus aperturas.

## 2. Estructura y convenciones

### `inau_spe_nacional.csv` (8.476 filas)
Columnas: `indicador_codigo`, `indicador_nombre`, `dimension`, `anio` (2020–2025), `apertura`, `valor`, `unidad`.

- `dimension`: Cobertura, Trayectorias, Adopciones, Atención y vínculos, Educación y salud (tomada de la ficha técnica).
- `unidad`: `cantidad`, `porcentaje` o `ratio` (indicador 2.3, que no es porcentaje y se dejó sin transformar).
- `apertura`: `total` para el valor general; en el resto, pares `clave=valor` separados por `|`. Claves usadas: `tramo` (edad), `edad` (edad simple), `sexo`, `region`, `propuesta` (propuesta de atención), `motivo` (motivo de atención), `motivo_permanencia`, `motivo_de_permanencia_en_adopciones`, `oferta` (tipo de oferta educativa), `nivel_educativo`, `propuesta_educativa`, `permanencia` (tiempos de permanencia, indicadores 1.4, 1.5, 5.2, 5.3), `frecuencia` (frecuencia del vínculo, indicador 9.1) y `entorno` (subapertura Contexto familiar / Residencias dentro de los tramos de edad, p. ej. `tramo=0 a 2 años|entorno=Residencias`).

### `inau_spe_departamental.csv` (221.469 filas, 48 MB)
Columnas: `indicador_codigo` (1–24), `indicador_nombre`, `departamento`, `periodo` (`2020-S1` … `2025-S2`), `apertura`, `valor`, `unidad`.

- Se incluyó el detalle completo (todas las aperturas), no solo los totales; los totales por indicador × departamento × período se obtienen filtrando `apertura == "total"`.
- Claves de apertura análogas a las nacionales; `permanencia` corresponde a los indicadores 3, 4, 12 y 13; no hay apertura por región (el departamento ya es la unidad territorial).

### CSVs de abril de 2025 (corte transversal)
Columnas: `cuadro`, `titulo`, `fila`, `departamento`, `columna`, `valor`, `unidad`.

- `fila`: categoría de la fila tal como figura en el cuadro (propuesta de atención, sexo, etc.).
- `departamento`: nombre del departamento cuando la columna del cuadro tiene apertura departamental (cuadros 4, 5, 9 y 10 de población; 4, 5, 6 y 7 de acogimiento); `Total país` en caso contrario o para las columnas de total nacional.
- `columna`: niveles restantes del encabezado de columna separados por `|` (p. ej. `Primera Infancia|Mujeres`, `Centros SPE 24 horas`); `total` cuando la columna es el total; `Total depto` marca la columna de total del departamento en los cuadros que la traen.
- Filas: `inau_abril2025_poblacion.csv` 11.926; `inau_abril2025_acogimiento.csv` 2.208; `inau_abril2025_dvf.csv` 448.

**Precaución al agregar:** tanto en las aperturas (`propuesta=`) como en las filas de los cuadros de abril, coexisten categorías padre y subcategorías que suman al padre (p. ej. `Cuidado residencial` y sus tipos de residencia; `Familia Extensa` y `Extensa`/`Extensa Parcial`). Para sumar sin duplicar hay que usar los totales o quedarse con un solo nivel de la jerarquía.

## 3. Decisiones de normalización

1. **Escala de porcentajes.** En el archivo nacional los porcentajes vienen en formato decimal (0.068 = 6,8 %): se multiplicaron por 100. En los archivos departamentales ya vienen en escala 0–100 (10.1 = 10,1 %): se dejaron tal cual. En el Cuadro 3 del reporte Derecho a Vivir en Familia los valores vienen como texto (`87.3%`): se convirtieron a número en escala 0–100. Resultado: todos los CSV expresan los porcentajes en escala 0–100.
2. **Ratio (indicador nacional 2.3).** No es porcentaje; se conservó el valor original con `unidad = "ratio"`.
3. **Nombres de departamentos.** Se normalizaron con la ortografía correcta: Paysandú, Río Negro, San José, Tacuarembó, Treinta y Tres (los archivos de origen los traen sin tilde en los nombres de archivo y en algunos encabezados).
4. **Error tipográfico de la fuente.** En el Cuadro 2 del reporte de población, el encabezado `Mujereses` se corrigió a `Mujeres`.
5. **Etiquetas de sexo.** Se conservaron tal como vienen en cada fuente: `Mujeres`/`Varones` en el nacional y los reportes, `Niñas`/`Varones` en los departamentales. Unificar requiere un simple reemplazo si se cruzan ambas fuentes.
6. **Celdas combinadas y encabezados de varios niveles.** Los años, semestres y subcategorías de columna se reconstruyeron a partir de las celdas combinadas; en los cuadros de abril algunos encabezados departamentales no estaban combinados y se completaron por arrastre (verificado contra los totales de cada cuadro).

## 4. Datos faltantes conocidos

- Indicadores nacionales **1.4, 1.5, 11.1 y 11.2**: la serie comienza en **2021** (sin dato 2020 en la fuente).
- Indicadores departamentales **3, 4, 20 y 21**: la serie comienza en **2021-S1**.
- Indicador departamental **18** (frecuencia del vínculo familiar): la fuente trae **cero en todas las celdas de los 19 departamentos** (dato no reportado a nivel departamental). Se excluyó del CSV (20.064 filas de ceros) para no inducir a error; el dato nacional equivalente sí existe (indicador 9.1).
- **Egresos del segundo semestre de 2020**: según la fuente, son valores estimados (afecta los indicadores de egresos: 5.x nacional y 11–13 departamentales).
- El reporte Derecho a Vivir en Familia (abril 2025) no tiene apertura departamental; sus tres cuadros son solo a nivel país.

## 5. Verificaciones realizadas

- **(a) Coherencia nacional–departamental:** indicador nacional 1.1, año 2025, `region=Montevideo` = 3.700; indicador departamental 1, Montevideo, `2025-S2`, total = 3.700. Coinciden (el dato anual nacional corresponde al corte del segundo semestre). ✔
- **(b) Porcentajes acotados:** tras la normalización, el máximo es exactamente 100.0 y no hay ningún valor > 100 en ningún CSV. ✔
- **(c) Cobertura territorial:** los 19 departamentos están presentes en `inau_spe_departamental.csv`, con los 12 períodos (2020-S1 a 2025-S2). ✔
- Controles adicionales: la suma por sexo del indicador 1.1 (2020) reproduce el total (6.516); la fila total de Artigas TD.1 se contrastó celda a celda contra el Excel original; en el Cuadro 4 de acogimiento la suma de los totales departamentales (3.250) coincide con el total nacional del Cuadro 3; en el Cuadro 5 de población la suma de proyectos por departamento (3.245) coincide con el total del Cuadro 3; en el Cuadro 2 de población los totales por etapa reproducen la columna de total (58.157 mujeres).

## 6. Qué quedó fuera y por qué

- Hojas metodológicas (presentación, glosario, fichas técnicas, descripciones de propuestas) — texto, no datos.
- Hojas de gráficos — imágenes sin tablas subyacentes adicionales.
- Indicador departamental 18 — todo ceros (ver sección 4).
- Celdas no numéricas dentro de las tablas (vacías o de nota) — se omiten; no se generan filas con valor nulo.
