# Catálogo de métricas construibles — confirmado contra los datos reales

Este catálogo sale de **abrir los archivos** (los 12 PDF de SIPIAV, los
Excel de INAU, el boletín ENSANNA, el informe ENTI 2010, los estudios
CONAPEES y los bloques extraídos de la ECH) y verificar qué cuadros
existen, en qué años y con qué desagregaciones. Reglas de rigor:
[`METODOLOGIA.md`](METODOLOGIA.md); naturaleza de cada fuente:
[`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md); relevamiento:
[`RELEVAMIENTO_DE_DATOS.md`](RELEVAMIENTO_DE_DATOS.md).

**Cómo se organiza** (igual que en
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)):
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

Los 12 informes 2013-2024 tienen texto extraíble; los gráficos son
vectoriales (valores extraíbles) solo en 2016-2019, imagen en el resto.

| # | Métrica | Tipo | Serie real | Estado |
|---|---|---|---|---|
| 1 | Situaciones atendidas por año (absolutos) | Descriptiva | 2011-2022 en texto (2013: 1.319 → 2022: 7.473); 2023 (8.157) y 2024 (8.924) solo en imagen del PDF — confirmables por notas oficiales de Presidencia/INAU | ⚠️ serie completa citando fuente mixta |
| 2 | Distribución por sexo (%) | Descriptiva | 2013-2024, todos los años (~54-56% niñas) | ✅ |
| 3 | Distribución por franja etaria (%) | Descriptiva | 0-3/4-5/6-12/13-17/18+ desde 2014 (2013 agregado; 2022-24 la prosa agrupa 0-5) | ⚠️ |
| 4 | Tipos de violencia (%) | Descriptiva | 2013-2024, con dos quiebres: 2020 aparece "explotación sexual" como 5ª categoría; 2024 fusiona abuso + explotación en "violencias sexuales" | ⚠️ quiebres 2020 y 2024 se marcan, no se interpolan |
| 5 | Tipo de violencia × sexo y × franja etaria | Descriptiva | Todos los años (tabla en imagen 2020-2024) | ⚠️ |
| 6 | Recurrencia (episodio único vs. recurrente) | Descriptiva | 2013-2024; cruce × tipo hasta 2023 | ✅ |
| 7 | Cronicidad (>6 meses) | Descriptiva | 2013-2024; cruce × tramo solo 2019-2020 | ✅ |
| 8 | Vínculo de la persona agresora + convivencia | Descriptiva | 2013-2024 (negligencia excluida del análisis desde 2019) | ✅ |
| 9 | NNA que visualizan la violencia | Descriptiva | 2017-2024 solamente | ✅ serie corta |
| 10 | Inclusión de la familia en la intervención | Descriptiva | 2014-2024 (82% → 58%: serie con lectura sustantiva) | ✅ |
| 11 | Cobertura territorial del sistema (nº de CRL) | Descriptiva | 2014-2024 (24 → 36) + participación sectorial 2015-2024 reconstruible | ✅ |
| P1 | Situaciones que atendería el sistema, 2025-2027 | Predictiva | Sobre la métrica 1 (12 puntos) — ya calculada: 2025 ≈ 9.400 (8.500-10.300); el informe 2025 presentado servirá de validación | ✅ |
| P2 | Inclusión de la familia proyectada | Predictiva | Sobre la métrica 10 (11 puntos); pendiente extraer los puntos intermedios de los PDF | ✅ pendiente de cálculo |
| P5 | Cobertura CRL proyectada | Predictiva | Sobre la métrica 11; curva saturante, valor informativo menor | ⚠️ |
| — | Situaciones por departamento | — | **No existe en ningún año** — la ausencia principal de la fuente | ❌ |
| — | Casos nuevos vs. seguimiento | — | Solo 2021, 2022 (+ 2024-2025 vía prensa) | ❌ como serie |

## Tema 2 — Explotación sexual (CONAPEES; el dato cuantitativo vive en el estudio FLACSO 2023, cap. 6)

| # | Métrica | Tipo | Serie real | Estado |
|---|---|---|---|---|
| 12 | Situaciones ESNNA atendidas (CONAPEES) | Descriptiva | 2018: 386 · 2019: 240 · 2020: 410 · 2021: 494; **con apertura por los 19 departamentos** (tabla 2 del estudio FLACSO) | ✅ 2018-2021; 2022+ pendiente (la discrepancia 285 vs. 456 de prensa sigue sin resolver) |
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
| P3 | Desinternación proyectada, por departamento | Predictiva | Sobre la métrica 21 (12 puntos semestrales); responde "¿a este ritmo, cuándo llegaría el departamento X a tal proporción en familia?" | ✅ pendiente de cálculo |
| P4 | NNA en protección especial cada 1.000 NNA, proyectado | Predictiva | Numerador: métrica 20; denominador futuro: proyecciones oficiales de población del INE | ✅ pendiente de cálculo |

Advertencias documentadas por la exploración: los % del nacional vienen en
decimal (0,068) y los departamentales en escala 10,1 — normalizar antes
de cruzar; el nacional desagrega por 6 regiones INAU (no departamentos);
"atendidos" (SPE) ≠ "vinculaciones" (reportes de abril).

## Tema 5 — Pobreza, vivienda y entorno del hogar (ECH propia, ponderada — data/ech/)

Ya extraído y verificado (2019, 2023, 2024, 2025; universo 0-17 con las
clasificaciones de edad de cada organismo como columnas):

| # | Métrica | Tipo | Detalle | Estado |
|---|---|---|---|---|
| 31 | Pobreza monetaria 0-17 (vs. adultos: brecha de infantilización) | Descriptiva | 28,9% ponderado en 2024 (verificado); por departamento, tramo, sexo; 2019 con metodología vieja — quiebre documentado | ✅ |
| 32 | Hacinamiento en hogares con NNA | Descriptiva | habitaciones/personas, por departamento y tramo | ✅ |
| 33 | Condiciones de vivienda de hogares con NNA | Descriptiva | 12 carencias en 2019 → 4 desde 2024 (quiebre heredado y documentado) | ⚠️ |
| 34 | Brecha digital en hogares con NNA | Descriptiva | internet/PC/tablet Ibirapitá, por estrato y departamento | ✅ |
| 35 | Inseguridad alimentaria en hogares con menores (FIES) | Descriptiva | 2023-2025, con marcador oficial menores18/menores6 | ✅ |
| 36 | Victimización de hogares donde viven NNA | Descriptiva | 2024-2025 (5 tipos de delito, denuncia, violencia) | ✅ |
| P8 | Pobreza infantil proyectada | Predictiva | Solo 3 puntos comparables (2023-2025) | ❌ serie insuficiente — se habilita con 2026 |

## Contexto transversal — demografía de la infancia

| # | Métrica | Tipo | Detalle | Estado |
|---|---|---|---|---|
| P6 | Población 0-17 de Uruguay | Predictiva | Proyecciones oficiales del INE (no se calculan: se citan) — la caída de nacimientos achica el denominador de todas las tasas del proyecto | ✅ — la proyección más firme del catálogo porque es del organismo oficial |

Lo que la parte predictiva **nunca** va a contener, por diseño:
pronósticos de prevalencia de violencia o explotación (no hay serie de
prevalencia: solo registros de detección), y cualquier proyección
presentada sin su supuesto inercial y su rango.

## UNICEF Uruguay (75 publicaciones descargadas)

Rol confirmado: **fuente de contexto y verificación cruzada**, no de
series propias — sus datos citan a ECH/ENSANNA/SIPI. Pendiente puntual de
alto valor: la encuesta de violencia sexual en la infancia citada en
Infancia en Datos ("casi 1 de cada 3 antes de los 18") — si su ficha
técnica es pública, sería la única fuente de **prevalencia** de violencia
del proyecto (todo el Tema 1 es registro administrativo).

---

## Cruces con la ECH (a desarrollar)

Los cruces son análisis **descriptivo** (asociaciones observadas entre
condiciones de la infancia y respuesta institucional — lenguaje
observacional, nunca causal); si alguna asociación resultara estable en
el tiempo, su extensión predictiva se evaluaría con las reglas de la
clasificación predictiva, no antes.

1. **INAU × ECH por departamento** (el más sólido): tasa de NNA en
   protección especial cada 1.000 NNA (INAU semestral × población 0-17
   ECH) contra pobreza infantil, hacinamiento y carencias de vivienda del
   mismo departamento. Mismo nivel de agregación → sin falacia ecológica
   si se redacta a nivel departamento.
2. **CONAPEES/Fiscalía × ECH por departamento** (2018-2021): situaciones
   ESNNA y actuaciones fiscales vs. condiciones socioeconómicas de la
   infancia por departamento.
3. **ENSANNA × ECH por nivel socioeconómico** (solo a nivel agregado: el
   INSE de la ENSANNA no es el estrato de la ECH — se documenta como
   comparación de gradientes, no de valores).
4. **SIPIAV × ECH: solo a nivel nacional y por tramo de edad** — SIPIAV
   no publica desagregación departamental de situaciones (limitación
   estructural, documentada arriba).
