# Bloque predictivo — justificación técnica de algoritmos

**Audiencia: técnicos — analistas de datos, economistas, estadísticos —
que auditen este repositorio.** Es la justificación de qué algoritmo usa
cada proyección del Bloque B y de las métricas de evaluación que
respaldan esa elección. **Nada de esto va al informe ni al usuario
final** (decisión del dueño del proyecto, 2026-08-17): el informe
muestra únicamente el escenario inercial con su rango y su supuesto ("si
la tendencia continúa…"), igual que una gráfica muestra el dato y no el
código que la generó. Las reglas
de rigor del bloque están en [`METODOLOGIA.md`](METODOLOGIA.md), sección
3; las fuentes citadas, en [`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md).

## Protocolo de selección de modelo (aplica a toda proyección)

Fundamento: Hyndman & Athanasopoulos, *Forecasting: Principles and
Practice* (FPP3) — capítulos de métodos simples ("simple forecasting
methods"), evaluación de exactitud ("evaluating forecast accuracy") y
transformaciones; y Shmueli (2010) para la separación
explicar/predecir.

1. **Candidatos fijos, todos simples** (n ≤ 12-24 puntos: más parámetros
   sería sobreajuste): ingenuo (último valor), deriva (último valor +
   pendiente media), tendencia lineal MCO, tendencia log-lineal. Para
   series acotadas (%) se agrega tendencia sobre transformación logit;
   para series saturantes, curva asintótica.

### Por qué no aprendizaje automático ni deep learning

Decisión explícita, no una omisión — con tres fundamentos:

- **Tamaño de los datos.** Las series temporales del proyecto tienen
  entre 3 y 24 puntos (SIPIAV: 12 anuales; INAU: 6 anuales o 12
  semestrales; CONAPEES: 4). Una red neuronal o un ensamble de árboles
  tiene órdenes de magnitud más parámetros que observaciones hay
  disponibles: el resultado sería memorizar la serie, no aprender su
  dinámica (sobreajuste garantizado). La evidencia comparada del área
  (competencias M de Makridakis; Makridakis, Spiliotis & Assimakopoulos,
  2018, *PLOS ONE*, "Statistical and Machine Learning forecasting
  methods: Concerns and ways forward") muestra que en series cortas los
  métodos estadísticos simples superan de forma consistente a los de
  aprendizaje automático.
- **Auditabilidad.** Este proyecto exige que cada proyección sea
  explicable ante público técnico y trazable a su supuesto ("si la
  tendencia continúa"). Una pendiente MCO de +696 situaciones/año es
  auditable a simple vista; una caja negra no, y en un tema sensible
  (infancia, violencia) la opacidad del método es un costo inaceptable.
- **El criterio ya está fijado y es empírico, no ideológico.** El
  protocolo admite cualquier candidato que supere el backtest. Si algún
  día un método más complejo lo supera de forma robusta con los datos
  que haya, entra por la misma puerta que los demás — con su tabla de
  métricas en este documento.

**Dónde sí podría aparecer aprendizaje automático clásico en el
futuro**: si el INE publica los microdatos de la ENSANNA (miles de
observaciones transversales, no una serie corta), sería legítimo evaluar
una regresión logística (u otro clasificador clásico regularizado) para
*perfilar* qué características se asocian al trabajo infantil — como
análisis descriptivo de asociaciones, con lenguaje observacional y
validación cruzada. Nunca para predecir riesgo individual de NNA
concretos: además del límite estadístico, es un uso éticamente
inaceptable de estos datos y queda fuera del alcance del proyecto. El
deep learning queda descartado en todos los horizontes visibles: no hay
ningún volumen de datos en este dominio que lo justifique.
2. **Backtest con los últimos 2 puntos como holdout**: se ajusta con la
   serie sin esos puntos y se mide MAE y MAPE sobre ellos.
3. **Criterios de aceptación** (decisión de este proyecto, fijada antes
   de calcular): el modelo elegido debe (a) superar al modelo ingenuo en
   el backtest — si ningún modelo lo supera, no se publica proyección — y
   (b) tener MAPE de holdout ≤ 15%.
4. **El ganador del backtest no se elige a ciegas**: con 2 puntos de
   holdout, una victoria estrecha puede ser azar. Se prefiere el modelo
   más estable (el que usa toda la serie) cuando pasa los criterios, y
   el ganador puntual queda como análisis de sensibilidad.
5. **Rango**: ±2 desviaciones estándar de los residuos del modelo
   reajustado con la serie completa. Se reporta el rango, no el punto.
6. **R² se reporta pero no decide**: en series con tendencia, R² es alto
   casi por construcción (FPP3) — la decisión es siempre por error de
   predicción fuera de muestra.
7. **Validación fuera de muestra continua**: cuando aparece el dato real
   del primer año proyectado, se contrasta contra el rango publicado
   antes de re-estimar nada.

## P1 — Situaciones atendidas por SIPIAV (calculado, 2026-08-17)

Serie: 2013-2022 en texto de los informes (1.319 → 7.473); 2023 (8.157)
y 2024 (8.924) de notas oficiales (Presidencia/INAU — ver
`RELEVAMIENTO_DE_DATOS.md`). Ajuste con 2013-2022, holdout 2023-2024:

| Modelo | Pred. 2023 | Pred. 2024 | MAE | MAPE | Veredicto |
|---|---|---|---|---|---|
| Ingenuo (último valor) | 7.473 | 7.473 | 1.068 | 12,3% | línea base |
| **Deriva** | 8.157 | 8.841 | **42** | **0,5%** | menor error de backtest |
| **Tendencia lineal MCO** | 7.738 | 8.435 | 454 | 5,3% | **elegido** (estable, usa toda la serie, pasa ambos criterios) |
| Tendencia log-lineal | 9.838 | 11.958 | 2.357 | 27,3% | **descartado**: el crecimiento dejó de ser exponencial; proyectarlo sobreestima de manera notoria |

- **Elección: tendencia lineal** (pendiente ≈ +696 situaciones/año),
  con la deriva como sensibilidad (casi indistinguible: su pendiente
  media 2013-2022 es ≈ +684/año — que dos estimadores independientes de
  la pendiente coincidan refuerza la lectura de crecimiento lineal
  estable). La victoria 0,5% de la deriva sobre 2 puntos no es base
  suficiente para preferirla al MCO (regla 4 del protocolo).
- **Proyección publicable** (modelo lineal reajustado 2013-2024,
  residuos s≈458): 2025: ~9.400 (8.500-10.300) · 2026: ~10.100
  (9.200-11.100) · 2027: ~10.900 (10.000-11.800).
- **Validación fuera de muestra (2026-08-18)**: el informe de gestión
  2025 (PDF descargado y verificado) publica el total 2025 bajo la
  metodología tradicional: **9.178** — dentro del rango proyectado
  8.500-10.300 (punto proyectado ~9.400; error del punto 2,4%). La
  proyección queda validada en su primer año. Advertencia para el
  siguiente ciclo: el informe 2025 introduce en paralelo una nueva
  definición operativa (7.381 en 2025) — si desde 2026 la serie se
  publica solo con la nueva base, la serie tradicional se corta en 2025
  y el modelo deberá re-estimarse sobre la base nueva cuando acumule
  puntos suficientes, no mezclarlas (ver
  `datos_curados/sipiav_notas.md`, quiebre 7).
- **Advertencia heredada**: la serie tiene cambios de fuente (2018-2019
  incorporan CHPR; 2021 salto pospandemia +43%) documentados en
  `CATALOGO_DE_METRICAS.md` — otra razón para no leer el ajuste fino
  como señal (y para el lenguaje de "respuesta del sistema", nunca
  "violencia futura").

## P2 — Inclusión de la familia en la intervención (calculado, 2026-08-17)

Serie: 2014-2024, 11 puntos, completa (curada de los informes SIPIAV —
`datos_curados/sipiav_series.csv`, con respaldo textual por valor; 2015
y 2021 provienen de prosa fraccionaria y están marcados). Ajuste con
2014-2022, holdout 2023-2024:

| Modelo | Pred. 2023 | Pred. 2024 | MAE | MAPE | Veredicto |
|---|---|---|---|---|---|
| Ingenuo (último valor) | 62,0 | 62,0 | 2,50 | 4,3% | línea base |
| Deriva | 59,5 | 57,0 | 1,25 | 2,1% | menor error; queda como sensibilidad |
| Lineal sobre % crudo | 62,7 | 60,6 | 2,14 | 3,6% | pasa, pero puede proyectar valores fuera de [0,100] en horizontes largos |
| **Lineal sobre logit** | 62,1 | 59,5 | 1,29 | 2,2% | **elegido**: pasa ambos criterios, usa toda la serie y respeta las cotas de una proporción por construcción (FPP3, transformaciones) |

- **Proyección publicable** (logit reajustado 2014-2024): 2025: ~56%
  (48-64) · 2026: ~53% (45-61) · 2027: ~50% (42-58). Pendiente
  equivalente en escala cruda: −2,35 puntos porcentuales por año.
- **Lectura para el informe**: si la tendencia continúa, hacia 2027 la
  familia se incluiría en la intervención en aproximadamente la mitad de
  las situaciones — cuando en 2014 se lograba en más de 8 de cada 10.
- **Advertencia**: como toda la serie SIPIAV, describe la práctica del
  sistema (a qué proporción de intervenciones se logra incorporar a la
  familia), con los cambios de base de cálculo documentados en
  `datos_curados/sipiav_notas.md`.
- **Validación fuera de muestra (2026-08-18): no concluyente por cambio
  de base.** El informe 2025 publica inclusión familiar = 45%, pero
  sobre una base que incorpora un 17% de casos «sin información» como
  categoría explícita (hasta 2024 el cálculo era sobre casos válidos).
  El 45% publicado no es comparable con la serie 2014-2024 y cae fuera
  del rango proyectado (48-64); recalculado sobre los casos con dato
  (45/(45+39) = 54%) cae dentro del rango. Ninguna de las dos lecturas
  valida ni refuta limpiamente: la validación queda registrada como no
  concluyente y el modelo no se re-estima con el punto 2025 hasta que
  SIPIAV estabilice la base de cálculo (quiebre 7 de
  `datos_curados/sipiav_notas.md`).

## P3 — Proporción del SPE en contexto familiar, por departamento (calculado, 2026-08-17)

Serie: proporción de NNA del Sistema de Protección Especial que viven en
contexto familiar (indicadores departamentales 6 y 5 de INAU), 12 puntos
semestrales 2020-S1 a 2025-S2, los 19 departamentos + total país.
Backtest con holdout 2025-S1/2025-S2; elegible logit primero, lineal
como alternativa; horizonte 4 semestres (2026-2027). Script:
`src/proyeccion_desinternacion.py`; resultados completos por
departamento en `resultados/proyecciones/p3_desinternacion.csv`.

- **Proyectables: 9 de 20 unidades** (total país y 8 departamentos), en
  todos los casos con lineal-logit superando al ingenuo y MAPE ≤ 15%.
  Total país: 62,7% observado (2025-S2) → **66,4% (63,9-68,8) hacia
  2027-S2** si el ritmo de desinternación persiste. Canelones es el caso
  más firme (MAPE logit 0,43%): 70,1% → 74,8% (73,3-76,3).
- **No proyectables: 11 unidades, por dos motivos distintos y ambos
  documentados en el CSV**: (a) series tan estables que el ingenuo ya
  es casi perfecto (Montevideo: MAPE ingenuo 0,24% — el escenario
  inercial ahí es "se mantiene en torno a 53%", y no requiere modelo:
  se reporta como lectura descriptiva); (b) series erráticas donde
  ningún candidato alcanza los criterios (Paysandú: MAPE 23-46% — no se
  publica proyección).
- **Nota**: no se detectó patrón semestral sistemático que obligara a
  anualizar antes de proyectar (verificado sobre el total país y los
  departamentos proyectables).

## P4 — NNA en protección especial cada 1.000 NNA (calculado, 2026-08-18)

Numerador: NNA de **0 a 17 años** atendidos en el SPE (indicador
nacional 1.1 de INAU, suma de los tramos 0-2 a 16-17 — la suma de todos
los tramos reproduce el total del indicador en los seis años,
verificado; se excluyen los tramos 18-20 y 21+ para que numerador y
denominador midan el mismo universo). Serie 2020-2025: 5.583 → 5.929 →
6.312 → 7.027 → 6.960 → 7.043. Denominador **sin modelo propio**:
población 0-17 proyectada del INE (revisión 2025, archivo B.1.1, edad
simple) — los denominadores futuros no se extrapolan en este proyecto.
Script: `src/proyeccion_p4_tasa_spe.py`; resultado:
`resultados/proyecciones/p4_tasa_spe.csv`.

Ajuste con 2020-2023, holdout 2024-2025 (conteos — candidatos sin
logit):

| Modelo | MAE | MAPE | Veredicto |
|---|---|---|---|
| **Ingenuo (último valor)** | **41,5** | **0,6%** | línea base — imbatible |
| Deriva | 747,5 | 10,7% | descartado |
| Tendencia lineal MCO | 625,8 | 8,9% | descartado |
| Tendencia log-lineal | 762,3 | 10,9% | descartado |

- **Resultado del protocolo: ningún candidato supera al ingenuo → no se
  publica proyección de modelo** (regla 3a). El numerador creció hasta
  2023 y se amesetó (2023-2025: 7.027 → 6.960 → 7.043); proyectar la
  pendiente 2020-2023 hacia adelante sobreestimaría de forma notoria —
  el backtest lo muestra con claridad. Mismo desenlace que las series
  estables de P3: el escenario inercial se reporta como lectura
  descriptiva, sin modelo.
- **Lectura publicable (descriptiva)**: tasa observada de NNA de 0 a 17
  años en el SPE cada 1.000 NNA: **9,05 (2024) y 9,38 (2025)**. Si la
  cantidad de NNA atendidos se mantuviera en torno al último valor
  observado (~7.000), la tasa seguiría subiendo a ~9,6 (2026) y ~9,8
  (2027) por mil **solo por la caída de la población infantil**
  proyectada por el INE (768.969 en 2024 → 715.901 en 2027, −2,3%
  anual). Esta cifra de referencia no lleva rango porque no hay modelo
  del numerador: su única incertidumbre declarada es la de la
  proyección demográfica externa (supuestos propios del INE).
- **Limitación documentada**: la revisión 2025 del INE publica
  proyecciones desde 2024; las estimaciones retrospectivas (2020-2023)
  no estaban publicadas al momento del cálculo, por lo que la tasa
  observada solo existe para 2024-2025. Cuando el INE publique la serie
  retrospectiva de la revisión 2025, se completará 2020-2023 con esos
  denominadores (no con los de la revisión 2013, que la ECH todavía usa
  en sus ponderadores — ver `RELEVAMIENTO_DE_DATOS.md`, sección INE).

## P5 — Cobertura CRL (pendiente, prioridad baja)

- **Algoritmo previsto**: curva saturante (asintótica) — la serie 24→36
  con desaceleración visible y un techo natural (cantidad de localidades
  con masa crítica). Una recta proyectaría crecimiento indefinido sin
  sentido sustantivo. Si el ajuste asintótico no es estable con 11
  puntos, se degrada a lectura descriptiva.

## P6 — Población 0-17 (sin algoritmo propio)

- No se modela nada: se citan las proyecciones oficiales del INE
  (organismo productor, con metodología demográfica propia publicada).
  Rol en el proyecto: contexto y denominadores de P4.

---

**Regla de mantenimiento**: cada proyección que pase de "pendiente" a
"calculada" agrega aquí su tabla de backtest con los números reales, en
el mismo commit que el código que la calcula. Una proyección sin su
tabla en este documento no se publica en ningún informe.
