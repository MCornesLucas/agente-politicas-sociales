# Notas de extracción — Capítulo 6, estudio FLACSO Uruguay 2023

**Fuente**: *Explotación sexual hacia niñas, niños y adolescentes* (FLACSO Uruguay, 2023), capítulo 6 «Información cuantitativa: estado de la cuestión» (pp. 43-58).
**Archivo**: `data/conapees/2023/estudio_explotacion_sexual_flacso_2023.pdf` (114 páginas).
**Método**: extracción de texto con pypdf (modos estándar y `layout`); cada tabla se verificó en ambos modos y toda columna con total impreso se validó por suma. Las páginas citadas corresponden a la numeración impresa del documento (la página PDF es la impresa + 1).

## Correspondencia tabla → CSV

| CSV | Tabla del PDF | Página impresa | Contenido |
|---|---|---|---|
| `conapees_esnna.csv` | Tabla 2 + texto de p. 45 | 44-45 | Situaciones de ESNNA atendidas por departamento, 2018-2021 (fuente CONAPEES) |
| `conapees_esnna_sexo.csv` | Tabla 3 | 45 | Víctimas niñas y adolescentes mujeres (cantidad y %), por departamento, 2020-2021 |
| `fiscalia_delitos_sexuales_nna.csv` | Tabla 8 | 50 | Actuaciones de la FGN (SIPPAU) en abuso sexual, atentado violento al pudor y violación con víctima NNA, por departamento, 2018-2021 |
| `sipiav_explotacion_sexual.csv` | Tablas 4, 5, 6 y 7 + texto de p. 48 | 47-48 | Explotación sexual y abuso sexual dentro del registro SIPIAV, 2016-2021 |

## Verificaciones de consistencia realizadas

- **Tabla 2**: la suma de los 19 departamentos coincide exactamente con el total nacional impreso en los cuatro años: 2018 = 386, 2019 = 240, 2020 = 410, 2021 = 494.
- **Tabla 3**: la suma de víctimas mujeres por departamento coincide con el total impreso (2020 = 354; 2021 = 425). Además, cada porcentaje departamental se recalculó como víctimas mujeres / situaciones de la tabla 2 y coincide con el impreso (±1 punto por redondeo) en los 38 casos. Totales: 354/410 = 86 % y 425/494 = 86 %, como imprime la tabla.
- **Tabla 8**: la suma por departamento coincide con el total impreso en los cuatro años: 2018 = 1673, 2019 = 2201, 2020 = 2065, 2021 = 2324.
- **Tablas 4-7 y texto de p. 48**: 98 ≈ 2 % de 4911 (2020) y 140 ≈ 2 % de 7035 (2021); 94 ≈ 96 % de 98 casos crónicos (2020) y 130 ≈ 93 % de 140 (2021). Las cifras absolutas del texto son coherentes con los porcentajes de las tablas.

## Ambigüedades y decisiones

1. **Paysandú 2020 en la tabla 8 (FGN): valor 1.** El PDF imprime «1», valor anómalo frente a la serie del departamento (74 en 2018, 74 en 2019, 86 en 2021). Se conservó porque el total nacional impreso (2065) solo cierra con ese valor, es decir, la anomalía es interna a la fuente y no un error de extracción. Se dejó constancia en la columna `nota` del CSV. Cualquier uso analítico de la serie de Paysandú debe tratar ese dato con cautela (posible error tipográfico del propio estudio).
2. **Tasa cada 10.000 NNA (figuras 5 y 6, pp. 51-52)**: las figuras son imágenes rasterizadas sin texto extraíble; no fue posible obtener valores numéricos verificables, por lo que la columna `tasa_cada_10000_nna` no se incluyó. El texto solo permite afirmar cualitativamente que Artigas, Soriano, Flores y Rocha encabezan las actuaciones cada 10.000 NNA en 2021.
3. **Casos nuevos**: el estudio solo informa situaciones nuevas para 2018 (175 de 386) y 2019 (129 de 240); declara expresamente que no hay dato para 2020 y 2021 (p. 45). Se registraron como filas de «Total nacional» con nota, sin apertura departamental porque la fuente no la trae.
4. **Datos específicos de 2021**: 422 de 494 situaciones corresponden a adolescentes de 12 a 18 años y 364 de 494 se judicializaron (texto, p. 45). Son cifras de texto, no de tabla; se incluyeron con nota que lo indica.
5. **Explotación sexual en SIPIAV**: la tipología «explotación sexual» solo se desagrega desde 2020; hasta 2019 las situaciones de ESNNA quedan incluidas dentro de «abuso sexual» (p. 46). Los años sin dato («s/d» en el PDF) se omitieron en el CSV en lugar de imputarse.
6. **Formato largo del CSV de SIPIAV**: las tablas 4-7 mezclan totales, porcentajes y dos tipologías (AS y ES); se optó por formato largo (`anio, indicador, valor, unidad, tabla_fuente, nota`) para no forzar una estructura tabular ambigua. Se incluyeron también los indicadores de abuso sexual porque las tablas los traen y contextualizan la serie de ES.
7. **Cierre anual de los datos del CONAPEES**: el conteo anual cierra en noviembre, dado que el Comité presenta sus informes el 7 de diciembre de cada año (p. 44).

## Advertencias del propio estudio (aplican a todo uso de estos datos)

- **Las cifras reflejan detección y atención, no incidencia.** El estudio subraya que el aumento de las cifras se relaciona con mayor detección, registro e intervención, y que no puede afirmarse que el fenómeno haya aumentado ni lo contrario, «a la luz de la escasez de evidencia» (p. 46). Para la tabla 8, señala explícitamente que los departamentos con más actuaciones cada 10.000 NNA no necesariamente presentan mayor incidencia, sino posiblemente más recursos y equipos locales (p. 52).
- **Subregistro reconocido.** Las entrevistas citadas (personal de dirección del INAU) constatan reticencia a ingresar datos sensibles al SIPI y califican los datos de explotación sexual como de los «más frágiles» (p. 54).
- **Fragmentación y falta de sistematización.** El CONAPEES no posee cometido específico de registro; sus datos surgen de organizaciones conveniantes con el INAU, el programa Travesía y su equipo técnico (p. 44). El estudio advierte que la fragmentación impide valorar la evolución temporal de las cifras (p. 46).
- **Cobertura y comparabilidad.** No existe información pública en línea de los organismos vinculados; Uruguay no figura en los datos estadísticos de ANNA Observa (IIN-OEA) ni en el índice Out of the Shadows 2020 (pp. 48, 55-56). La única estimación con diseño estadístico (Gurises Unidos - IESTA, 2015: proyección de 650 casos, 390 identificados con certeza) no se ha reiterado y no permite comparación (pp. 54-55).
