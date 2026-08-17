# Catálogo de métricas construibles — confirmado contra los datos reales

Segunda versión del catálogo: la primera era un borrador de diseño; esta
sale de **abrir los archivos** (los 12 PDF de SIPIAV, los Excel de INAU,
el boletín ENSANNA, el informe ENTI 2010, los estudios CONAPEES y los
bloques extraídos de la ECH) y verificar qué cuadros existen, en qué años
y con qué desagregaciones. Cada métrica indica su serie real y sus
quiebres. Reglas de rigor que gobiernan todas:
[`METODOLOGIA.md`](METODOLOGIA.md); naturaleza de cada fuente:
[`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md); detalle del relevamiento:
[`RELEVAMIENTO_DE_DATOS.md`](RELEVAMIENTO_DE_DATOS.md).

Convención de estado: ✅ construible ya · ⚠️ construible con salvedad
documentada · ❌ no existe en la fuente (documentado para no prometerlo).

**El catálogo se organiza en dos bloques globales**, siguiendo el modelo
de madurez analítica de Gartner (descriptivo: "¿qué pasó?"; predictivo:
"¿qué va a pasar?") y la distinción explicar/predecir de Shmueli (2010)
— citas completas en [`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md), sección
"Marcos de análisis de datos":

- **Bloque A — Análisis descriptivo**: muestra la realidad observada.
  Métricas 1-36, organizadas en 5 temas.
- **Bloque B — Análisis predictivo**: infiere el futuro inercial — "si
  las cosas no cambian, esto es lo que sucederá". Proyecciones P1-P8,
  regidas por las reglas de `METODOLOGIA.md`, sección 3 (solo escenarios
  inerciales, serie mínima de 6 puntos comparables, horizonte ≤ 1/3 del
  largo de la serie, rango en vez de número único, backtesting antes de
  publicar).

---

# Bloque A — Análisis descriptivo (¿qué pasó / qué está pasando?)

## Tema 1 — Violencia hacia NNA (SIPIAV, registros administrativos; nunca prevalencia)

Los 12 informes 2013-2024 tienen texto extraíble; los gráficos son
vectoriales (valores extraíbles) solo en 2016-2019, imagen en el resto.

| # | Métrica | Serie real | Estado |
|---|---|---|---|
| 1 | Situaciones atendidas por año (absolutos) | 2011-2022 en texto (2013: 1.319 → 2022: 7.473); 2023 (8.157) y 2024 (8.924) solo en imagen del PDF — confirmables por notas oficiales de Presidencia/INAU | ⚠️ serie completa citando fuente mixta |
| 2 | Distribución por sexo (%) | 2013-2024, todos los años (~54-56% niñas) | ✅ |
| 3 | Distribución por franja etaria (%) | 0-3/4-5/6-12/13-17/18+ desde 2014 (2013 agregado; 2022-24 la prosa agrupa 0-5) | ⚠️ |
| 4 | Tipos de violencia (%) | 2013-2024, con dos quiebres: 2020 aparece "explotación sexual" como 5ª categoría; 2024 fusiona abuso + explotación en "violencias sexuales" | ⚠️ quiebres 2020 y 2024 se marcan, no se interpolan |
| 5 | Tipo de violencia × sexo y × franja etaria | Todos los años (tabla en imagen 2020-2024) | ⚠️ |
| 6 | Recurrencia (episodio único vs. recurrente) | 2013-2024; cruce × tipo hasta 2023 | ✅ |
| 7 | Cronicidad (>6 meses) | 2013-2024; cruce × tramo solo 2019-2020 | ✅ |
| 8 | Vínculo de la persona agresora + convivencia | 2013-2024 (negligencia excluida del análisis desde 2019) | ✅ |
| 9 | NNA que visualizan la violencia | 2017-2024 solamente | ✅ serie corta |
| 10 | Inclusión de la familia en la intervención | 2014-2024 (82% → 58%: serie con lectura sustantiva) | ✅ |
| 11 | Cobertura territorial del sistema (nº de CRL) | 2014-2024 (24 → 36) + participación sectorial 2015-2024 reconstruible | ✅ |
| — | Situaciones por departamento | **No existe en ningún año** — el gran ausente de SIPIAV | ❌ |
| — | Casos nuevos vs. seguimiento | Solo 2021, 2022 (+ 2024-2025 vía prensa) | ❌ como serie |

## Tema 2 — Explotación sexual (CONAPEES; el dato cuantitativo vive en el estudio FLACSO 2023, cap. 6)

| # | Métrica | Serie real | Estado |
|---|---|---|---|
| 12 | Situaciones ESNNA atendidas (CONAPEES) | 2018: 386 · 2019: 240 · 2020: 410 · 2021: 494; **con apertura por los 19 departamentos** (tabla 2 del estudio FLACSO) | ✅ 2018-2021; 2022+ pendiente (la discrepancia 285 vs. 456 de prensa sigue sin resolver) |
| 13 | Sexo de las víctimas ESNNA | 2020-2021 (86% niñas/adolescentes mujeres) | ✅ corta |
| 14 | ES dentro de SIPIAV | 2020 (98 casos) y 2021 (140); desde 2024 fusionada en "violencias sexuales" | ⚠️ ventana 2020-2023 |
| 15 | Actuaciones de Fiscalía por delitos sexuales con víctima NNA | 2018-2021, por departamento y en tasa cada 10.000 NNA | ✅ (delitos sexuales en general, no solo explotación — así se rotula) |

## Tema 3 — Trabajo infantil (ENSANNA 2024, prevalencia; ENTI 2010; ECH 14-17)

El "informe" ENSANNA es un boletín de 4 cuadros + 4 gráficos — hasta que
el INE publique los microdatos, esto es todo lo construible:

| # | Métrica | Detalle real | Estado |
|---|---|---|---|
| 16 | Tasa y volumen de trabajo infantil 5-17 | 6,8% / 40,2 mil; por región (Mdeo 5,2 / Interior 7,7), sexo (M 7,0 / V 6,6), edad (5-8: 2,0 / 9-14: 7,6 / 15-17: 10,6) y nivel socioeconómico INSE (7,9 bajo → 4,8 alto) | ✅ |
| 17 | Descomposición: actividades económicas (TFP) vs. trabajo no remunerado de servicios (TNRS) | Solo %, por las mismas 4 aperturas; el sesgo de género es visible (TNRS: niñas 2,8 vs. varones 1,1) | ✅ |
| 18 | Comparación puntual 2010 ↔ 2024 | ENTI 2010: 9,9% (FPSCN) o 13,4% (FGP) — la definición elegida cambia la conclusión; el propio informe 2010 advierte incomparabilidad con mediciones previas | ⚠️ puntos sueltos + decisión de definición documentada |
| 19 | Trabajo adolescente 14-17 (ECH propia, ponderada) | data/ech: 2023, 2024, 2025 (panel mensual) — ocupación, formalidad (f82), por sexo/departamento | ✅ anual, cálculo propio |
| — | Asistencia escolar × trabajo, horas, trabajo peligroso, departamento | No publicados en el boletín 2024 (la ENTI 2010 sí los tenía: ~70 cuadros) | ❌ hasta microdatos |

## Tema 4 — Protección especial (INAU, xlsx del SIPI; población atendida, no infancia general)

| # | Métrica | Serie real | Estado |
|---|---|---|---|
| 20 | NNA atendidos en el SPE (y % sobre población país) | 2020-2025 anual nacional; 2020-S1 a 2025-S2 semestral **por los 19 departamentos** | ✅ |
| 21 | Residencial vs. contexto familiar (ratio) | 2020-2025; el eje de la política de desinternación | ✅ |
| 22 | Ingresos por primera vez vs. reingresos | 2020-2025 | ✅ |
| 23 | Egresos y tiempo de permanencia en el sistema | 2020-2025 (tiempos: desde 2021; egresos S2-2020 estimados — nota al pie del propio archivo) | ⚠️ |
| 24 | Tránsito de residencia a familia | 2020-2025 | ✅ |
| 25 | Adopciones: condición de adoptabilidad → tenencia | 2020-2025 | ✅ |
| 26 | Frecuencia de contacto con familia/referentes | 2020-2025 | ✅ |
| 27 | Educación: 0-5 en CAIF/CAPI, 6-17 en formal, 13-17 no formal | 2021-2025 (2020 no disponible) | ⚠️ |
| 28 | Salud: controles y vacunas al día | 2020-2025 | ✅ |
| 29 | Acogimiento familiar: tipo de familia, altas/bajas de familias acogedoras por departamento | Fotografía abril 2025 (RAF) | ✅ corte |
| 30 | Dónde viven los NNA acompañados (familia origen / acogimiento / residencial / adoptiva) | Fotografía abril 2025 (RDVF, ~8.777 NNA) | ✅ corte |

Trampas documentadas por la exploración: los % del nacional vienen en
decimal (0,068) y los departamentales en escala 10,1 — normalizar antes
de cruzar; el nacional desagrega por 6 regiones INAU (no departamentos);
"atendidos" (SPE) ≠ "vinculaciones" (reportes de abril).

## Tema 5 — Pobreza, vivienda y entorno del hogar (ECH propia, ponderada — data/ech/)

Ya extraído y verificado (2019, 2023, 2024, 2025; universo 0-17 con las
clasificaciones de edad de cada organismo como columnas):

| # | Métrica | Detalle | Estado |
|---|---|---|---|
| 31 | Pobreza monetaria 0-17 (vs. adultos: brecha de infantilización) | 28,9% ponderado en 2024 (verificado); por departamento, tramo, sexo; 2019 con metodología vieja — quiebre documentado | ✅ |
| 32 | Hacinamiento en hogares con NNA | habitaciones/personas, por departamento y tramo | ✅ |
| 33 | Condiciones de vivienda de hogares con NNA | 12 carencias en 2019 → 4 desde 2024 (quiebre heredado y documentado) | ⚠️ |
| 34 | Brecha digital en hogares con NNA | internet/PC/tablet Ibirapitá, por estrato y departamento | ✅ |
| 35 | Inseguridad alimentaria en hogares con menores (FIES) | 2023-2025, con marcador oficial menores18/menores6 | ✅ |
| 36 | Victimización de hogares donde viven NNA | 2024-2025 (5 tipos de delito, denuncia, violencia) | ✅ |

## UNICEF Uruguay (75 publicaciones descargadas)

Rol confirmado: **fuente de contexto y verificación cruzada**, no de
series propias — sus datos citan a ECH/ENSANNA/SIPI. Pendiente puntual de
alto valor: la encuesta de violencia sexual en la infancia citada en
Infancia en Datos ("casi 1 de cada 3 antes de los 18") — si su ficha
técnica es pública, sería la única fuente de **prevalencia** de violencia
del proyecto (todo el Tema 1 es registro administrativo).

---

# Bloque B — Análisis predictivo (¿qué sucederá si las cosas no cambian?)

Toda proyección de este bloque es un **escenario inercial** (supuesto
explícito: las condiciones actuales persisten), con rango de
incertidumbre y backtesting — reglas completas y fundamento en
`METODOLOGIA.md`, sección 3 (Gartner; Shmueli 2010; Hyndman &
Athanasopoulos, *FPP3* — ver `BIBLIOGRAFIA.md`). Sobre registros
administrativos se proyecta **la respuesta del sistema, no el
fenómeno**, y así se rotula en cada gráfica.

| # | Proyección | Serie base (fuente) | Horizonte | Estado |
|---|---|---|---|---|
| P1 | Situaciones que atendería el sistema SIPIAV | 2013-2024, 12 puntos anuales (informes de gestión SIPIAV; quiebre de fuentes 2018/2020 documentado) | 2025-2027 | ✅ — el informe 2025 ya presentado (2.536 situaciones nuevas, nota M. Interior) sirve como validación fuera de muestra |
| P2 | Inclusión de la familia en la intervención | 2014-2024, 11 puntos (SIPIAV): cayó de 82% a 58% — proyectar dónde estaría en 2027 si la caída persiste | 2-3 años | ✅ |
| P3 | Ratio cuidado residencial vs. contexto familiar (desinternación) | 2020-2025, 12 puntos semestrales, nacional y por departamento (INAU, indicadores SPE) | 2026-2027 | ✅ — la proyección responde "¿a este ritmo, cuándo llegaría el departamento X a tal proporción en familia?" |
| P4 | NNA atendidos en protección especial cada 1.000 NNA | Numerador: INAU 2020-2025 semestral; denominador futuro: proyecciones oficiales de población del INE | 2026-2027 | ✅ |
| P5 | Cobertura territorial del sistema (CRL) | 2014-2024, 11 puntos (SIPIAV): 24 → 36, tendencia saturante | 2-3 años | ⚠️ — proyectar con curva saturante, no lineal; valor informativo menor |
| P6 | Población 0-17 de Uruguay (contexto demográfico de todo el proyecto) | Proyecciones oficiales del INE (no se calcula: se cita) — la caída de nacimientos achica el denominador de todas las tasas | según INE | ✅ — es la proyección más firme del bloque porque es del organismo oficial |
| P7 | Situaciones ESNNA (CONAPEES) | 2018-2021, 4 puntos (estudio FLACSO 2023, cap. 6) | — | ❌ serie insuficiente (< 6 puntos); se reevalúa si aparecen 2022-2024 oficiales |
| P8 | Pobreza infantil 0-17 | ECH propia: 3 puntos comparables (2023-2025; 2019 quedó con la canasta vieja) | — | ❌ serie insuficiente todavía — se habilita con 2026; mientras, solo lectura descriptiva |

Lo que este bloque **nunca** va a contener, por diseño: pronósticos de
prevalencia de violencia o explotación (no hay serie de prevalencia:
solo registros de detección), y cualquier proyección presentada sin su
supuesto inercial y su rango.

---

## Anticipo de la parte 3 — cruces con la ECH (a desarrollar)

Los cruces son análisis **descriptivo** (asociaciones observadas entre
condiciones de la infancia y respuesta institucional — lenguaje
observacional, nunca causal); si alguna asociación resultara estable en
el tiempo, su extensión predictiva se evaluaría con las reglas del
Bloque B, no antes.

La exploración ya define qué cruces son viables y a qué nivel:

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
