# Catálogo de métricas construibles — confirmado contra los datos reales

Este catálogo sale de **abrir los archivos** (los 12 PDF de SIPIAV, los
Excel de INAU, el boletín ENSANNA, el informe ENTI 2010, los estudios
CONAPEES y los bloques extraídos de la ECH) y verificar qué cuadros
existen, en qué años y con qué desagregaciones. Reglas de rigor:
[`METODOLOGIA.md`](METODOLOGIA.md); naturaleza de cada fuente:
[`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md); relevamiento:
[`RELEVAMIENTO_DE_DATOS.md`](RELEVAMIENTO_DE_DATOS.md).

**Cómo se organiza**:
los bloques del catálogo — y de todo informe — son **temáticos**. Dentro
de cada tema conviven sus métricas descriptivas y predictivas.

**Clasificación interna** (columna "Tipo" — agrupa métricas para las
reglas que les aplican, no estructura los informes):

- **Descriptiva** — "¿qué pasó?": muestra la realidad observada.
- **Predictiva** — "¿qué sucederá si nada cambia?": escenario inercial
  con rango, regido por `METODOLOGIA.md`, sección 3 (serie mínima de 6
  puntos comparables, horizonte ≤ 1/3 del largo de la serie, backtesting;
  justificación de algoritmos para público técnico en
  [`PREDICTIVO_JUSTIFICACION_TECNICA.md`](PREDICTIVO_JUSTIFICACION_TECNICA.md)
  — nunca en el informe). Fundamento de la distinción: Gartner; Shmueli
  (2010) — ver `BIBLIOGRAFIA.md`.

Convención de estado: ✅ construible ya · ⚠️ construible con salvedad
documentada · ❌ no existe o serie insuficiente (documentado para no
prometerlo).

## Tema 1 — Violencia hacia NNA (SIPIAV, registros administrativos; nunca prevalencia)

Los 13 informes 2013-2025 tienen texto extraíble; los gráficos son
vectoriales (valores extraíbles) solo en 2016-2019 y 2025, imagen en el
resto. **El informe 2025 introduce una nueva metodología en paralelo a
la tradicional** (quiebre 7 de `datos_curados/sipiav_notas.md`): las
series continúan con la tradicional, pero las desagregaciones 2025
incluyen una categoría explícita «sin información» que rompe la
comparabilidad de recurrencia, cronicidad e inclusión familiar.

| # | Métrica | Tipo | Serie real | Estado |
|---|---|---|---|---|
| 1 | Situaciones atendidas por año (absolutos) | Descriptiva | 2011-2025 íntegra en texto: el gráfico retrospectivo del informe 2025 trae los valores en texto (2013: 1.319 → 2025: 9.178) y confirma 2023 (8.157) y 2024 (8.924), antes solo en notas oficiales | ✅ (2016: el retrospectivo 2025 dice 2.547; se mantiene 2.647 del informe del año, discrepancia anotada) |
| 2 | Distribución por sexo (%) | Descriptiva | 2013-2025, todos los años (~54-56% niñas) | ✅ |
| 3 | Distribución por franja etaria (%) | Descriptiva | 0-3/4-5/6-12/13-17/18+ desde 2014 (2013 agregado; 2022-24 la prosa agrupa 0-5; 2025 publica 0-3, 0-5, 6-12 y 13-17) | ⚠️ |
| 4 | Tipos de violencia (%) | Descriptiva | 2013-2025, con dos quiebres: 2020 aparece "explotación sexual" como 5ª categoría; desde 2024 abuso + explotación fusionados en "violencias sexuales" (2025: 18%) | ⚠️ quiebres 2020 y 2024 se marcan, no se interpolan |
| 5 | Tipo de violencia × sexo y × franja etaria | Descriptiva | Todos los años (tabla en imagen 2020-2024; 2025 parcial en prosa) | ⚠️ |
| 6 | Recurrencia (episodio único vs. recurrente) | Descriptiva | 2013-2025; cruce × tipo hasta 2023; 2025 con base no comparable (17% sin información) | ⚠️ desde 2025 |
| 7 | Cronicidad (>6 meses) | Descriptiva | 2013-2025; cruce × tramo solo 2019-2020; 2025 con base no comparable (17% sin información) | ⚠️ desde 2025 |
| 8 | Vínculo de la persona agresora + convivencia | Descriptiva | 2013-2024 (negligencia excluida del análisis desde 2019); 2025 solo publica % de convivencia por tipo | ✅ |
| 9 | NNA que visualizan la violencia | Descriptiva | 2017-2024 solamente | ✅ serie corta |
| 10 | Inclusión de la familia en la intervención | Descriptiva | 2014-2024 (82% → 58%: serie con lectura sustantiva); 2025 (45%) no comparable por cambio de base | ⚠️ serie comparable termina en 2024 |
| 11 | Cobertura territorial del sistema (nº de CRL) | Descriptiva | 2014-2025 (24 → 36; 2025 estable) + participación sectorial 2015-2024 reconstruible | ✅ |
| P1 | Situaciones que atendería el sistema, 2025-2027 | Predictiva | Sobre la métrica 1 (12 puntos) — calculada y **validada**: real 2025 = 9.178, dentro del rango proyectado 8.500-10.300 | ✅ validada en su primer año |
| P2 | Inclusión de la familia proyectada | Predictiva | Sobre la métrica 10 (11 puntos, 2014-2024) — calculada (2027: ~50%, 42-58); validación 2025 no concluyente por el cambio de base de la fuente | ✅ calculada; ⚠️ validación pendiente de base estable |
| P5 | Cobertura CRL proyectada | Predictiva | Sobre la métrica 11 (13 puntos) — calculada (2026-08-20): curva asintótica elegida por backtest (MAPE 1,3%); 2028: ~39 CRL (37-41). Advertencia: la asíntota no está identificada por los datos (régimen casi lineal) — proyección robusta entre candidatos (~+1 CRL/año), ver `PREDICTIVO_JUSTIFICACION_TECNICA.md` | ✅ calculada; valor informativo menor |
| — | Situaciones por departamento | — | **No existe en ningún año** — la ausencia principal de la fuente | ❌ |
| — | Casos nuevos (nuevas situaciones por año) | Descriptiva | Serie oficial 2022-2025 publicada por el informe 2025 (1.643 → 2.536) | ✅ corta (4 puntos; insuficiente para proyectar) |

## Tema 2 — Explotación sexual (CONAPEES; el dato cuantitativo vive en el estudio FLACSO 2023, cap. 6)

| # | Métrica | Tipo | Serie real | Estado |
|---|---|---|---|---|
| 12 | Situaciones ESNNA atendidas (CONAPEES) | Descriptiva | 2018: 386 · 2019: 240 · 2020: 410 · 2021: 494; **con apertura por los 19 departamentos** (tabla 2 del estudio FLACSO) | ✅ 2018-2021; 2022+ pendiente (la discrepancia 285 vs. 456 de prensa sigue sin resolver; el III Plan Nacional 2023-2028, descargado 2026-08-18, no trae serie de casos, y el informe SIPIAV 2025 mantiene ESNNA fusionada en "violencias sexuales") |
| 13 | Sexo de las víctimas ESNNA | Descriptiva | 2020-2021 (86% niñas/adolescentes mujeres) | ✅ corta |
| 14 | ES dentro de SIPIAV | Descriptiva | 2020 (98 casos) y 2021 (140); desde 2024 fusionada en "violencias sexuales" | ⚠️ ventana 2020-2023 |
| 15 | Actuaciones de Fiscalía por delitos sexuales con víctima NNA | Descriptiva | 2018-2021, por departamento y en tasa cada 10.000 NNA | ✅ (delitos sexuales en general, no solo explotación — así se rotula) |
| P7 | Situaciones ESNNA proyectadas | Predictiva | Solo 4 puntos (2018-2021) | ❌ serie insuficiente (< 6 puntos); se reevalúa si aparecen 2022-2024 oficiales |

## Tema 3 — Trabajo infantil (ENSANNA 2024, prevalencia; ENTI 2010; ECH 14-17)

El "informe" ENSANNA es un boletín de 4 cuadros + 4 gráficos — hasta que
el INE publique los microdatos, esto es todo lo construible:

| # | Métrica | Tipo | Detalle real | Estado |
|---|---|---|---|---|
| 16 | Tasa y volumen de trabajo infantil 5-17 | Descriptiva | 6,8% / 40,2 mil; por región (Mdeo 5,2 / Interior 7,7), sexo (M 7,0 / V 6,6), edad (5-8: 2,0 / 9-14: 7,6 / 15-17: 10,6) y nivel socioeconómico INSE (7,9 bajo → 4,8 alto) | ✅ |
| 17 | Descomposición: actividades económicas (TFP) vs. trabajo no remunerado de servicios (TNRS) | Descriptiva | Solo %, por las mismas 4 aperturas; el sesgo de género es visible (TNRS: niñas 2,8 vs. varones 1,1) | ✅ |
| 18 | Comparación puntual 2010 ↔ 2024 | Descriptiva | ENTI 2010: 9,9% (FPSCN) o 13,4% (FGP) — la definición elegida cambia la conclusión; el propio informe 2010 advierte incomparabilidad con mediciones previas | ⚠️ puntos sueltos + decisión de definición documentada |
| 19 | Trabajo adolescente 14-17 (ECH propia, ponderada) | Descriptiva | data/ech: 2023, 2024, 2025 (panel mensual) — ocupación, formalidad (f82), por sexo/departamento | ✅ anual, cálculo propio |
| — | Asistencia escolar × trabajo, horas, trabajo peligroso, departamento | — | No publicados en el boletín 2024 (la ENTI 2010 sí los tenía: ~70 cuadros) | ❌ hasta microdatos |

## Tema 4 — Protección especial (INAU, xlsx del SIPI; población atendida, no infancia general)

| # | Métrica | Tipo | Serie real | Estado |
|---|---|---|---|---|
| 20 | NNA atendidos en el SPE (y % sobre población país) | Descriptiva | 2020-2025 anual nacional; 2020-S1 a 2025-S2 semestral **por los 19 departamentos** | ✅ |
| 21 | Residencial vs. contexto familiar (ratio) | Descriptiva | 2020-2025; el eje de la política de desinternación | ✅ |
| 22 | Ingresos por primera vez vs. reingresos | Descriptiva | 2020-2025 | ✅ |
| 23 | Egresos y tiempo de permanencia en el sistema | Descriptiva | 2020-2025 (tiempos: desde 2021; egresos S2-2020 estimados — nota al pie del propio archivo) | ⚠️ |
| 24 | Tránsito de residencia a familia | Descriptiva | 2020-2025 | ✅ |
| 25 | Adopciones: condición de adoptabilidad → tenencia | Descriptiva | 2020-2025 | ✅ |
| 26 | Frecuencia de contacto con familia/referentes | Descriptiva | 2020-2025 | ✅ |
| 27 | Educación: 0-5 en CAIF/CAPI, 6-17 en formal, 13-17 no formal | Descriptiva | 2021-2025 (2020 no disponible) | ⚠️ |
| 28 | Salud: controles y vacunas al día | Descriptiva | 2020-2025 | ✅ |
| 29 | Acogimiento familiar: tipo de familia, altas/bajas de familias acogedoras por departamento | Descriptiva | Corte transversal a abril de 2025 (RAF) | ✅ corte |
| 30 | Dónde viven los NNA acompañados (familia origen / acogimiento / residencial / adoptiva) | Descriptiva | Corte transversal a abril de 2025 (RDVF, ~8.777 NNA) | ✅ corte |
| P3 | Desinternación proyectada, por departamento | Predictiva | **Calculada**: total país 62,7% → 66,4% (63,9-68,8) en contexto familiar hacia 2027-S2; 9/20 unidades proyectables, el resto estable o errático (documentado) — ver `resultados/proyecciones/p3_desinternacion.csv` | ✅ |
| P4 | NNA en protección especial cada 1.000 NNA | Predictiva → descriptiva | Numerador 0-17 estricto (tramos del indicador 1.1) amesetado desde 2023: ningún candidato supera al ingenuo en el backtest → sin proyección de modelo (protocolo, regla 3a). Tasa observada: 9,05 (2024) y 9,38 (2025) por mil; referencia inercial ~9,8 hacia 2027 solo por caída del denominador INE — ver `resultados/proyecciones/p4_tasa_spe.csv` | ✅ resuelta como lectura descriptiva |

Advertencias documentadas por la exploración: los % del nacional vienen en
decimal (0,068) y los departamentales en escala 10,1 — normalizar antes
de cruzar; el nacional desagrega por 6 regiones INAU (no departamentos);
"atendidos" (SPE) ≠ "vinculaciones" (reportes de abril).

## Tema 5 — Pobreza, vivienda y entorno del hogar (ECH propia, ponderada — data/ech/)

Ya extraído y verificado (2019, 2023, 2024, 2025; universo 0-17 con las
clasificaciones de edad de cada organismo como columnas):

| # | Métrica | Tipo | Detalle | Estado |
|---|---|---|---|---|
| 31 | Pobreza monetaria 0-17 (vs. adultos: brecha de infantilización) | Descriptiva | 28,9% ponderado en 2024 (verificado); por departamento, tramo, sexo. **Dos regímenes verificados contra los archivos**: 2019 y 2023 solo traen canasta 2006 (16,2% y 18,6%); 2024-2025, canasta 2017 (28,9% y 27,5%) — la serie se corta entre 2023 y 2024 | ⚠️ quiebre 2023/2024 |
| 32 | Hacinamiento en hogares con NNA | Descriptiva | habitaciones/personas, por departamento y tramo | ✅ |
| 33 | Condiciones de vivienda de hogares con NNA | Descriptiva | 12 carencias en 2019 → 4 desde 2024 (quiebre heredado y documentado) | ⚠️ |
| 34 | Brecha digital en hogares con NNA | Descriptiva | internet/PC/tablet Ibirapitá, por estrato y departamento | ✅ |
| 35 | Inseguridad alimentaria en hogares con menores (FIES) | Descriptiva | 2023-2025, con marcador oficial menores18/menores6 | ✅ |
| 36 | Victimización de hogares donde viven NNA | Descriptiva | 2024-2025 (5 tipos de delito, denuncia, violencia) | ✅ |
| P8 | Pobreza infantil proyectada | Predictiva | Solo 2 puntos comparables (2024-2025, canasta 2017; 2023 quedó con la canasta 2006 — verificado contra el archivo del INE) | ❌ serie insuficiente |

## Contexto transversal — demografía de la infancia

| # | Métrica | Tipo | Detalle | Estado |
|---|---|---|---|---|
| P6 | Población 0-17 de Uruguay | Predictiva | Proyecciones oficiales del INE, revisión 2025 (Censo 2023), **descargadas y verificadas** (`data/ine/proyecciones_rev2025/`): 0-17 = 768.969 (2024) → 715.901 (2027), −2,3% anual — la caída achica el denominador de todas las tasas del proyecto | ✅ — la proyección más firme del catálogo porque es del organismo oficial |

Lo que la parte predictiva **nunca** va a contener, por diseño:
pronósticos de prevalencia de violencia o explotación (no hay serie de
prevalencia: solo registros de detección), y cualquier proyección
presentada sin su supuesto inercial y su rango.

## UNICEF Uruguay (75 publicaciones descargadas)

Rol confirmado: **fuente de contexto y verificación cruzada**, no de
series propias — sus datos citan a ECH/ENSANNA/SIPI. El pendiente de
alto valor quedó resuelto (2026-08-18): la encuesta citada en Infancia
en Datos es la **"Encuesta sobre violencia sexual contra niños, niñas y
adolescentes, Uruguay 2026"** (UNICEF Uruguay/Equipos Consultores,
abril de 2026), ya estaba entre lo descargado y fue archivada en
`data/unicef/2026/`. Tiene ficha metodológica pública: encuesta web
autoadministrada a personas de 18 a 24 años, **muestra no
probabilística** (n = 617, calibrada por rake contra la ECH 2024).
Resultado central: 29% reporta haber sufrido violencia sexual antes de
los 18 años. Es la única fuente de **prevalencia** de violencia del
proyecto, con advertencia obligatoria: sin marco muestral no hay margen
de error en sentido probabilístico ni representatividad garantizada —
se usa como orden de magnitud, nunca como serie ni con decimales (ver
`FUENTES_DE_DATOS.md`).

---

## Cruces con la ECH (los cuatro desarrollados, 2026-08-18/19)

Los cruces son análisis **descriptivo** (asociaciones observadas entre
condiciones de la infancia y respuesta institucional — lenguaje
observacional, nunca causal); si alguna asociación resultara estable en
el tiempo, su extensión predictiva se evaluaría con las reglas de la
clasificación predictiva, no antes.

1. **INAU × ECH por departamento** — **desarrollado (2026-08-18)**:
   tasa de NNA en protección especial cada 1.000 NNA (INAU 2024-S2 y
   2025-S2 × población 0-17 ponderada de la ECH) contra pobreza infantil
   y hacinamiento del mismo departamento
   (`politicas_sociales/cruce_inau_ech.py` → `resultados/cruces/`). Resultado: **sin
   asociación estable** (Spearman: pobreza −0,10/+0,02; hacinamiento
   −0,28/+0,19) — las tasas altas están en departamentos chicos de
   pobreza baja o media; lectura observacional en el informe.
   Advertencias: el numerador registra el departamento de atención (no
   de origen); carencias de vivienda sin apertura departamental en los
   curados actuales (extensión pendiente).
2. **CONAPEES/Fiscalía × ECH por departamento** — **desarrollado
   (2026-08-19)**: tasas cada 10.000 NNA (situaciones ESNNA 2018-2021 y
   actuaciones FGN; población y condiciones de la ECH 2019, único año de
   la ventana con microdatos) contra pobreza y hacinamiento
   (`politicas_sociales/cruce_conapees_fiscalia_ech.py` →
   `resultados/cruces/`). Resultado: con pobreza sin asociación (rho
   −0,27 a +0,09); con hacinamiento **asociación negativa en las ocho
   combinaciones fuente × año** (rho −0,22 a −0,71) — se registra menos
   donde el hacinamiento es mayor, consistente con la advertencia del
   estudio FLACSO (recursos de detección, no incidencia).
   Advertencias: conteos chicos (0-59), lado ECH fijo en 2019, Paysandú
   2020 (FGN=1) anómalo — el resultado se sostiene al excluirlo.
3. **ENSANNA × ECH por nivel socioeconómico** — **desarrollado
   (2026-08-19)**, como comparación de gradientes, no de valores (el
   INSE de la ENSANNA no es el estrato de la ECH, y el estrato ECH
   ordenado solo existe para Montevideo)
   (`politicas_sociales/cruce_ensanna_ech.py`). Resultado: ambos
   gradientes monótonos, pero el del trabajo infantil es mucho más plano
   (razón extremos 1,6 contra 20 de la pobreza) y la geografía se
   invierte: trabajo infantil mayor en el interior (ENSANNA 7,7 vs. 5,2;
   ocupación ECH 14-17 3,7 vs. 1,7) con pobreza infantil algo mayor en
   Montevideo (30,9 vs. 27,8 en 2024).
4. **SIPIAV × ECH nacional por tramo de edad** — **desarrollado
   (2026-08-19)**; SIPIAV no publica desagregación departamental
   (limitación estructural, documentada arriba)
   (`politicas_sociales/cruce_sipiav_ech.py`). Resultado: índice de
   representación (participación en situaciones / participación en
   población): 13-17 sobrerrepresentado en 2019 y 2025 (1,20 y 1,08);
   0-5 pasó de 0,65 (2019) a 0,95 (2025) — y es el tramo más pobre en
   ambos años: el perfil etario de la atención no sigue al de la
   pobreza. Advertencias: porcentajes publicados redondeados y
   renormalizados a 0-17; quiebre de tramos en 2020.
