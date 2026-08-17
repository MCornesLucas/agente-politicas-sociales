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
- **Validación pendiente**: el informe SIPIAV 2025 ya fue presentado
  pero solo se difundió el dato de situaciones *nuevas* (2.536), que no
  es el total — cuando se publique el PDF con el total 2025, se
  contrasta contra el rango 8.500-10.300 antes de tocar el modelo.
- **Advertencia heredada**: la serie tiene cambios de fuente (2018-2019
  incorporan CHPR; 2021 salto pospandemia +43%) documentados en
  `CATALOGO_DE_METRICAS.md` — otra razón para no leer el ajuste fino
  como señal (y para el lenguaje de "respuesta del sistema", nunca
  "violencia futura").

## P2 — Inclusión de la familia en la intervención (pendiente de cálculo)

- **Algoritmo previsto**: tendencia lineal sobre transformación
  **logit** de la proporción. Por qué logit: la serie es un porcentaje
  (82% → 58%); una recta sobre el % crudo puede proyectar valores
  imposibles (<0% o >100%) en horizontes largos, la recta en logit no
  (FPP3, transformaciones).
- **Pendiente**: extraer los 11 puntos 2014-2024 de los PDF (varios años
  están solo en prosa). Métricas del backtest se agregan aquí al
  calcular.

## P3 — Ratio residencial vs. contexto familiar, por departamento (pendiente)

- **Algoritmo previsto**: tendencia lineal sobre logit de la proporción
  en contexto familiar, por departamento (12 puntos semestrales
  2020-2025, INAU). Antes de ajustar: verificar visualmente que no haya
  patrón semestral (si lo hay, promediar el año antes de proyectar).
- **Riesgo documentado**: 12 puntos con quiebre pandémico al inicio de
  la serie — si el backtest no pasa los criterios en un departamento,
  ese departamento se reporta solo descriptivo.

## P4 — NNA en protección especial cada 1.000 NNA (pendiente)

- **Algoritmo previsto**: numerador con el mismo protocolo de P1/P3;
  denominador **sin modelo propio**: proyecciones oficiales de
  población del INE (regla de METODOLOGIA: los denominadores futuros no
  se extrapolan en este proyecto). La incertidumbre reportada es solo la
  del numerador — se anota que el denominador es una proyección externa
  con supuestos propios del INE.

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
