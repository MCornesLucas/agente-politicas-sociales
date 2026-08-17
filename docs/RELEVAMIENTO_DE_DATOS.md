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
| SIPIAV | ✅ Serie completa publicada | 12 informes de gestión (2013-2024), PDF |
| INAU | ✅ Datos en Excel | Indicadores SPE 2020-2025 (nacional + 19 deptos) y 3 reportes estadísticos de abril 2025 |
| ENSANNA (INE/MTSS) | ✅ Informe / ⏳ microdatos | Informe de resultados 2024 (HTML con cuadros) + informe ENTI 2010; microdatos aún "en análisis" en el INE |
| CETI (MTSS) | ✅ Documentos de política | Plan Nacional de Erradicación del Trabajo Infantil (PDF, OIT/MTSS) |
| CONAPEES | ⚠️ Parcial | 2 estudios 2023 (UNFPA y FLACSO); el III Plan Nacional no tiene PDF directo publicado |
| UNICEF Uruguay | ⚠️ Acceso verificado, descarga pendiente | Portal Infancia en Datos navegable; Biblioteca Digital (bibliotecaunicef.uy) operativa para selección de publicaciones |

## 1. SIPIAV — 12 informes de gestión, 2013-2024 (serie completa)

`data/sipiav/<año>/informe_gestion_sipiav_<año>.pdf`

Descargados del gestor documental de INAU
(`www.inau.gub.uy/sipiav/informes-de-gestion-sipiav/download/<id>/1494/16`
o `sipiav/download/<id>/978/16`). Mapeo id → año verificado leyendo la
portada de cada PDF:

| Año | id | Año | id |
|---|---|---|---|
| 2013 | 6469 | 2019 | 6475 (=6383) |
| 2014 | 6470 | 2020 | 6846 (=6847) |
| 2015 | 6471 | 2021 | 7641 |
| 2016 | 6472 | 2022 | 10367 |
| 2017 | 6473 | 2023 | 10366 |
| 2018 | 6474 | 2024 | 10368 |

**Pendiente**: informe de gestión 2025 — ya fue presentado (2.536
situaciones nuevas, según
[noticia del Ministerio del Interior](https://www.gub.uy/ministerio-interior/comunicacion/noticias/presencia-del-ministerio-del-interior-sipiav-presento-informe-anual-gestion)),
pero el PDF todavía no aparece en el gestor documental — reintentar.

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

**Pendiente**: III Plan Nacional 2023-2028 — existe formalmente (Decreto
48/025, https://www.impo.com.uy/bases/decretos/48-2025) pero no se
encontró PDF directo del plan; la página del CONAPEES en INAU está caída
por la migración del sitio. Los datos anuales de situaciones atendidas
del CONAPEES aparecen dentro de los informes SIPIAV y en notas de prensa
— resolver ahí la discrepancia 285 vs. 456 ya documentada.

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
- Hallazgo a evaluar (prioridad alta): el artículo "Violencia sexual en
  la infancia y la adolescencia en Uruguay" cita una **encuesta** (casi 1
  de cada 3 personas jóvenes vivió violencia sexual antes de los 18) —
  si su ficha técnica es pública, sería la única fuente de *prevalencia*
  de violencia del proyecto. Buscarla entre lo descargado (hay un PDF
  "encuesta_sobre_378.pdf" en sin_anio) o en la biblioteca.

## 7. ECH — extracción de infancia y adolescencia (proyecto hermano)

`data/ech/<año>/` — generado por `src/extraer_ech_infancia.py`, que
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
