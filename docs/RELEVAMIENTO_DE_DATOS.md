# Relevamiento de datos: qué se consiguió de cada entidad

Resultado del relevamiento y descarga inicial (agosto 2026). Los archivos
viven en `data/<entidad>/<año>/` — **no se versionan** (ver
`.gitignore`): este documento registra qué hay y de dónde salió cada
archivo, para poder re-descargarlo. La naturaleza de cada dato (registro
administrativo vs. encuesta) está en
[`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md).

## Resumen del estado

| Entidad | ¿Datos conseguidos? | Qué se descargó |
|---|---|---|
| SIPIAV | ✅ Serie completa publicada | 13 informes de gestión (2013-2025), PDF |
| INAU | ✅ Datos en Excel | Indicadores SPE 2020-2025 (nacional + 19 deptos) y 3 reportes estadísticos de abril 2025 |
| ENSANNA (INE/MTSS) | ✅ Informe / ⏳ microdatos | Informe de resultados 2024 (HTML con cuadros) + informe ENTI 2010; microdatos aún "en análisis" en el INE |
| CETI (MTSS) | ✅ Documentos de política | Plan Nacional de Erradicación del Trabajo Infantil (PDF, OIT/MTSS) |
| CONAPEES | ✅ Planes y estudios | 2 estudios 2023 (UNFPA y FLACSO) + III Plan Nacional 2023-2028 (PDF, gestor documental de INAU) |
| UNICEF Uruguay | ✅ 75 publicaciones | Biblioteca Digital (bibliotecaunicef.uy); incluye la Encuesta sobre violencia sexual contra NNA 2026 (única fuente de prevalencia de violencia) |
| INE — proyecciones de población | ✅ Revisión 2025 | B.1.1 (total país, edad simple, 2024-2070) y B.1.2 (departamentos, quinquenal, 2024-2045) — denominadores de P4/P6 |

## 1. SIPIAV — 13 informes de gestión, 2013-2025 (serie completa)

`data/sipiav/<año>/informe_gestion_sipiav_<año>.pdf`

Descargados del gestor documental de INAU
(`www.inau.gub.uy/sipiav/informes-de-gestion-sipiav/download/<id>/1494/16`
o `sipiav/download/<id>/978/16`). Mapeo id → año verificado leyendo la
portada de cada PDF:

| Año | id | Año | id |
|---|---|---|---|
| 2013 | 6469 | 2020 | 6846 (=6847) |
| 2014 | 6470 | 2021 | 7641 |
| 2015 | 6471 | 2022 | 10367 |
| 2016 | 6472 | 2023 | 10366 |
| 2017 | 6473 | 2024 | 10368 |
| 2018 | 6474 | 2025 | 11255 |
| 2019 | 6475 (=6383) | | |

**Informe 2025** (descargado 2026-08-18, id 11255, portada verificada):
presentado el 27/04/2026 ([noticia del Ministerio del Interior](https://www.gub.uy/ministerio-interior/comunicacion/noticias/presencia-del-ministerio-del-interior-sipiav-presento-informe-anual-gestion)).
Introduce una nueva metodología en paralelo a la tradicional y publica
por primera vez en texto la serie completa 2011-2025 y la serie de
nuevas situaciones 2022-2025 — detalles y quiebres en
`datos_curados/sipiav_notas.md` (quiebres 7 y 8).

Nota de contexto: el sitio de INAU está a medio migrar — las páginas de
sección (`/sipiav`, `/conapees`) dan 404, pero el gestor documental y las
noticias siguen operativos; `web.inau.gub.uy` (el host nuevo indexado por
Google) no resuelve DNS desde esta red.

## 2. INAU — Indicadores del Sistema de Protección Especial + reportes estadísticos

- `data/inau/2020-2025/indicadoresanualesspe-inau2020-2025.xlsx` —
  indicadores anuales nacionales, dimensiones: cobertura, trayectorias,
  adopciones, atención y vínculos, educación y salud.
- `data/inau/2020-2025/departamentos/datosspe<depto>-3.xlsx` — los mismos
  indicadores por departamento (19 archivos, todos los departamentos).
  **Clave para el cruce territorial con la ECH.**
- `data/inau/2025/` — tres reportes estadísticos de abril 2025 (edición
  Excel): Reporte de Población y Proyectos (RPP), Reporte de Acogimiento
  Familiar (RAF), Reporte Derecho a Vivir en Familia (RDVF).

Origen: [página de Transparencia de INAU](https://inau.gub.uy/transparencia/indicadores-sistema-de-proteccion-especial-inau)
(`inau.gub.uy/sites/default/files/migrado-docs/*.xlsx`); los reportes
RPP/RAF/RDVF, del gestor documental (ids 10361-10363).

## 3. ENSANNA / trabajo infantil — informes 2024 y 2010

- `data/ensanna/2024/informe_trabajo_infantil_ensanna_2024.html` —
  informe oficial de resultados con cuadros (INE, publicado 09/2025):
  https://www5.ine.gub.uy/documents/Demograf%C3%ADayEESS/HTML/ECH/ENSANNA/Informe-trabajo-infantil-2024.html
- `data/ensanna/2010/magnitud_caracteristicas_trabajo_infantil_2010.pdf`
  — "Magnitud y características del trabajo infantil en Uruguay 2010"
  (ENTI, antecedente):
  https://www5.ine.gub.uy/documents/Demograf%C3%ADayEESS/PDF/Informes%20Demogr%C3%A1ficos/Trabajo%20infantil/Magnitud%20y%20Caracter%C3%ADsticas%20del%20Trabajo%20Infantil%20en%20Uruguay.pdf

**Pendiente**: microdatos ENSANNA — [la página del INE](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/encuestas/encuesta-nacional-sobre-actividades-ninas-ninos-adolescentes-ensanna)
la lista "en análisis"; cuando pasen al catálogo ANDA
(https://www4.ine.gub.uy/Anda5/), descargarlos (ese día este proyecto
incorporará su segunda fuente de prevalencia). Revisar periódicamente.
Última revisión: 2026-08-18 — el catálogo ANDA (390 entradas, exportado
completo) sigue sin la ENSANNA.

## 4. CETI — Plan de Acción 2003-2005

- `data/ceti/2003-2005/plan_accion_prevencion_erradicacion_trabajo_infantil_2003_2005.pdf`
  — "Plan de Acción para la Prevención y Erradicación del Trabajo
  Infantil en el Uruguay 2003-2005" (CETI/Inspección General del
  Trabajo), verificado leyendo el contenido:
  http://www.annaobserva.org/observatorio/wp-content/uploads/2018/03/Plan-de-Acci%C3%B3n-para-la-Prevenci%C3%B3n.pdf

**Corrección registrada**: el primer PDF descargado como "plan CETI"
(desde webapps.ilo.org, ruta buenos-aires) resultó ser el plan de
**Argentina** (CONAETI 2011-2015) — mal catalogado en el sitio de la OIT;
"Uruguay" no aparece ni una vez en su texto. Se eliminó. Lección
aplicada: todo PDF descargado se verifica leyendo su contenido, no por el
nombre del archivo ni el sitio que lo aloja.

**Pendiente**: el primer plan estratégico nacional basado en la ENSANNA
2024 está en elaboración — monitorear la
[página del CETI en MTSS](https://www.gub.uy/ministerio-trabajo-seguridad-social/comunicacion/noticias/ceti).

## 5. CONAPEES — estudios 2023

- `data/conapees/2023/estudio_explotacion_sexual_entornos_digitales_unfpa_2023.pdf`
  (CONAPEES/UNFPA):
  https://uruguay.unfpa.org/sites/default/files/pub-pdf/pubexplotacionsexual23web.pdf
- `data/conapees/2023/estudio_explotacion_sexual_flacso_2023.pdf`
  (FLACSO Uruguay):
  https://flacso.edu.uy/wp-content/uploads/2023/12/EXPLOTACION-SEXUAL-HACIA-NINAS-NINOS-Y-ADOLESCENTES-COMPLETO.pdf

- `data/conapees/2023-2028/iii_plan_nacional_esnna_2023_2028.pdf` —
  **III Plan Nacional 2023-2028, descargado 2026-08-18** del gestor
  documental de INAU (id 10402:
  `https://www.inau.gub.uy/sites/default/files/migrado-docs/iiiplannacionalconapees.pdf`),
  verificado leyendo el contenido (58 páginas, CONAPEES, instituciones
  integrantes en portada). Formalizado por Decreto 48/025
  (https://www.impo.com.uy/bases/decretos/48-2025). **No trae serie de
  casos atendidos** — es un documento de política (ejes, metas,
  responsables).

**Pendiente**: los datos anuales de situaciones atendidas del CONAPEES
2022+ siguen sin fuente oficial: el III Plan no los trae, el informe
SIPIAV 2025 mantiene la explotación sexual fusionada en "violencias
sexuales", y la discrepancia 285 vs. 456 de prensa sigue sin resolver.

## 6. UNICEF Uruguay — 75 publicaciones descargadas de la Biblioteca Digital

- `data/unicef/<año>/` — **75 PDFs (~207 MB)** descargados de la
  [Biblioteca Digital](https://bibliotecaunicef.uy/) (catálogo PMB,
  descarga directa vía `doc_num.php?explnum_id=N`), recorriendo las
  categorías temáticas relevantes (pobreza, violencia, explotación,
  educación, protección, justicia penal, etc.). Cada PDF se renombró con
  el título leído del propio documento y se archivó por el año detectado
  en su contenido; los que no declaran año quedaron en
  `data/unicef/sin_anio/` (clasificarlos a mano cuando se usen).
- El portal [Infancia en Datos](https://www.unicef.org/uruguay/infancia-en-datos)
  (unicef.org) bloquea clientes automatizados — se navega con navegador;
  sus artículos citan como fuentes primarias a ECH/ENSANNA/SIPI, así que
  su rol es contexto y verificación cruzada, no series propias.
- **Hallazgo resuelto (2026-08-18)**: la encuesta citada en "Violencia
  sexual en la infancia y la adolescencia en Uruguay" es la **"Encuesta
  sobre violencia sexual contra niños, niñas y adolescentes, Uruguay
  2026"** (UNICEF Uruguay / Equipos Consultores, Montevideo, abril de
  2026) — era el PDF "encuesta_sobre_378.pdf" de `sin_anio/`,
  reclasificado a
  `data/unicef/2026/encuesta_violencia_sexual_nna_2026_378.pdf`. Ficha
  metodológica pública (anexo 5.1): encuesta web autoadministrada a
  personas de 18 a 24 años, **muestra no probabilística** (n = 617,
  calibración rake contra la ECH 2024). Resultado central: 29% reporta
  violencia sexual antes de los 18 años; 17% abuso sexual; 17%
  explotación. Única fuente de *prevalencia* de violencia del proyecto,
  con la advertencia de diseño registrada en `FUENTES_DE_DATOS.md`.

## 7. INE — Proyecciones de población, revisión 2025 (denominadores de P4/P6)

`data/ine/proyecciones_rev2025/` — descargadas 2026-08-18 de la página
oficial (https://www.gub.uy/instituto-nacional-estadistica/proyeccionesrev2025),
revisión basada en el Censo 2023, publicada el 17/07/2025:

- `B11_uruguay_edad_simple_2024_2070.xlsx` — total país por sexo y
  **edad simple**, 2024-2070 (archivo original: "B.1.1 Uruguay
  (100ymas)2024-2070.xlsx"). Verificado: población 0-17 = 768.969 en
  2024 (22,0% del total) → 715.901 en 2027.
- `B12_departamentos_edad_simple_2024_2045.xlsx` — departamentos por
  sexo y **grupo quinquenal** (no edad simple, pese al nombre del
  archivo local), 2024-2045. **Limitación**: 0-17 exacto no es
  construible por departamento (el grupo 15-19 incluye 18 y 19 años) —
  toda tasa departamental por 1.000 NNA queda condicionada a que el INE
  publique edad simple departamental, no se aproxima.

Advertencias documentadas:

- **La revisión 2025 no es la base de los ponderadores de la ECH**: la
  ECH 2024 ponderada da 0-17 = 24,1% del total, la revisión 2025 da
  22,0% (el Censo 2023 rebajó la población). Un cociente entre un
  numerador ECH y un denominador de la revisión 2025 mezcla bases — no
  hacerlo sin anotarlo.
- Las **estimaciones retrospectivas** (2012-2023) de la revisión 2025
  no estaban publicadas al 2026-08-18 (solo los archivos B de
  proyección; se verificó además que los archivos "A.\*" no existen aún
  en el servidor). Cuando se publiquen, completar los denominadores
  2020-2023 de P4.

## 8. ECH — extracción de infancia y adolescencia (proyecto hermano)

`data/ech/<año>/` — generado por `politicas_sociales/extraer_ech_infancia.py`, que
reutiliza los loaders de
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)
(hereda sus correcciones de encoding y decisiones metodológicas
verificadas). Universo: **0-17 años** (CDN), con las clasificaciones de
cada organismo como columnas derivadas (`tramo_sipiav` 0-5/6-12/13-17,
`clasificacion_ley_17823` niño/adolescente con corte a los 13,
`es_adolescente_oms` 10+, `en_universo_ensanna` 5-17) — cada análisis
posterior corta por la que corresponda a la fuente que cruce, sin volver
a los microdatos.

Bloques por año (todos conservan su ponderador — nada se calcula sin
ponderar):

| Año | personas_0a17 | hogares_con_nna | empleo_14a17 | victimización | FIES |
|---|---|---|---|---|---|
| 2019 | 24.389 (24,8% pond.) | 14.550 (40,9% pond.) | — | — | — |
| 2023 | 11.424 (24,1%) | 7.100 (40,6%) | 15.131 filas-mes | — | 2.245 hogares |
| 2024 | 11.482 (24,1%) | 7.157 (40,1%) | 15.291 filas-mes | 9.162 filas | 2.186 hogares |
| 2025 | 10.826 (24,1%) | 6.913 (41,1%) | 14.915 filas-mes | 8.598 filas | 2.022 hogares |

- `personas_0a17.csv`: personas 0-17 con contexto del hogar
  (departamento, estrato, pobreza) y ponderador anual.
- `hogares_con_nna.csv`: hogares con al menos un NNA — vivienda, brecha
  digital, pobreza, territorio — con conteos de NNA por tramo SIPIAV.
- `empleo_14a17.csv`: panel mensual de Empleo, edades 14-17 (el módulo
  no releva menores de 14), con mes y ponderador mensual.
- `victimizacion_hogares_con_nna.csv`: módulo de victimización (lo
  responden adultos) restringido a hogares donde viven NNA.
- `fies_hogares_con_menores.csv`: hogares FIES con el marcador oficial
  `menores18 == 1` del INE.

Verificación de plausibilidad realizada: pobreza ponderada 0-17 en 2024
= 28,9% (consistente con lo publicado por el INE con metodología 2017,
frente a ~17% en la población general); población 0-17 ≈ 24% del total
ponderado en los cuatro años.

Nota: el módulo de Empleo comienza a los 14 años — para trabajo infantil de
5-13 la única fuente es la ENSANNA; la ECH solo cubre trabajo
adolescente (14-17). Es un caso concreto de la regla "misma métrica,
misma definición" al cruzar con CETI/ENSANNA.

---

**Cómo re-descargar todo**: cada archivo tiene su URL en esta página; la
estructura de carpetas es `data/<entidad>/<año o rango>/`. Si un enlace
de INAU muere, buscar el documento por título en el gestor documental
(`/download/<id>/...`) — los ids están en la tabla de arriba.
