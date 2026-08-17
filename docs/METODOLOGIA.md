# Metodología: reglas de rigor para analizar políticas sociales de infancia

Este proyecto hereda el marco metodológico de
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)
(reglas de rigor estadístico, terminología y visualización probadas sobre
la ECH) y lo adapta a un problema distinto: aquí la mayoría de las fuentes
**no son encuestas con microdatos, son registros administrativos e
informes institucionales** (SIPIAV, INAU, CONAPEES), con una sola encuesta
con microdatos públicos (ENSANNA 2024). Esa diferencia cambia qué
afirmaciones son defendibles y cuáles no.

Qué publica cada organismo y qué es cada dato: ver
[`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md). Citas completas:
[`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md). Justificación del tipo de gráfica
de cada métrica: [`CONVENCIONES_DE_GRAFICAS.md`](CONVENCIONES_DE_GRAFICAS.md).

## 1. Estructura estándar del análisis

Igual que en el proyecto original, la estructura de cualquier informe es
fija, no la improvisa el modelo en cada corrida:

1. **Introducción**: qué se analizó, de dónde salen los datos y una
   advertencia de una línea sobre la diferencia entre casos atendidos y
   prevalencia (la regla central de la sección 2), con referencia a la
   nota metodológica final.
2. **Un tramo por tema** (Violencia hacia NNA, Explotación sexual,
   Trabajo infantil, Protección especial, Pobreza infantil e inversión —
   ver `CATALOGO_DE_METRICAS.md`), cada uno abriendo con qué mide, de qué
   fuente sale y qué significan los términos del organismo que usan sus
   métricas.
3. **Nota metodológica** al final: qué es un registro administrativo, qué
   es una estimación ponderada de encuesta, y por qué no se comparan
   entre sí sin aclaración.
4. **Resumen analítico final** con cifras reales (nunca estimadas),
   redactado para un lector no técnico.

Cada métrica lleva las mismas cinco partes del proyecto original, en este
orden: nombre, qué pregunta responde, términos propios (si el tema no los
explicó ya), la gráfica, y por qué esa gráfica con su referencia
bibliográfica.

## 2. Reglas de rigor estadístico (no negociables)

Las primeras cuatro son nuevas de este proyecto (nacen de trabajar con
registros administrativos); las siguientes se heredan del proyecto
original y siguen aplicando en pleno.

- **Casos atendidos ≠ prevalencia — la regla central de este proyecto.**
  SIPIAV, CONAPEES e INAU registran situaciones **detectadas y atendidas
  por el sistema**, no cuántos NNA sufren violencia/explotación en el
  país. Un aumento interanual (ej. 8.157 → 8.924 situaciones SIPIAV entre
  2023 y 2024) puede reflejar mayor capacidad de detección del sistema,
  más denuncia, o más violencia — con el registro solo, no se puede
  distinguir. Redacción correcta: "situaciones atendidas por el sistema
  aumentaron"; redacción prohibida: "la violencia hacia NNA aumentó" o
  "X% de los niños sufren violencia" calculado desde un registro. La
  única fuente de este proyecto que permite hablar de prevalencia es la
  ENSANNA (encuesta con diseño muestral). Esta aclaración va **en el
  texto y en el título o subtítulo de cada gráfica de registros**, no
  solo en la nota metodológica.
- **Misma métrica, misma definición, mismo denominador.** Antes de
  comparar dos números (entre años, entre fuentes, o entre informes del
  mismo organismo) verificar por escrito: rango de edad (0-17, 5-17,
  13-17 varían entre fuentes — la tabla comparativa completa de cómo
  clasifica cada organismo está en
  [`CLASIFICACION_DE_EDADES.md`](CLASIFICACION_DE_EDADES.md); el
  universo del proyecto es 0-17 según la CDN, y en los cruces con la ECH
  es la ECH la que se adapta al rango de la fuente), definición del
  evento (ej. "trabajo
  infantil" de ENSANNA vs. "actividades económicas"; "casos nuevos" vs.
  "situaciones atendidas" de SIPIAV, que incluyen arrastre de años
  anteriores), y cobertura (nacional vs. Montevideo). Caso concreto ya
  detectado: sobre explotación sexual circulan "285 situaciones
  atendidas" y "456 casos detectados, +24%" — no son la misma métrica y
  no se grafican juntas sin resolver qué mide cada una.
- **Cortes de serie se marcan, no se interpolan.** La encuesta de trabajo
  infantil anterior a la ENSANNA 2024 es de 2009-2010 (ENTI, ~68.000 NNA)
  y su comparabilidad metodológica con la ENSANNA no está establecida en
  este proyecto. Hasta verificarla contra la documentación de ambas, los
  dos puntos no forman una serie: si se muestran juntos, con eje x en
  escala temporal real (regla heredada) y una nota explícita de posible
  incomparabilidad. Nunca una línea que sugiera una tendencia continua
  2010→2024.
- **Tasas con denominador citado.** Todo número absoluto de NNA que se
  convierta en tasa ("X por cada 1.000 NNA") lleva como denominador las
  proyecciones de población del INE, citando año y fuente del
  denominador. Nunca mezclar denominadores de años distintos al numerador
  sin aclararlo.
- **Ponderación por muestreo** (hereda del original, aplica a ENSANNA y a
  todo cálculo propio sobre ECH): toda estimación desde microdatos se
  calcula con el ponderador de la encuesta, nunca como proporción simple
  de la muestra. En el proyecto original la diferencia llegaba a 1.1
  puntos porcentuales en pobreza — suficiente para cambiar una
  conclusión.
- **Celdas chicas** (hereda del original): grupos con menos de n=30 casos
  muestrales no sostienen una comparación — aclarar la poca base muestral
  en el texto. En registros administrativos el problema es otro pero la
  regla es análoga: desagregaciones con números muy chicos de víctimas no
  se publican si permiten identificar personas — seguir el criterio de
  desagregación del propio organismo, nunca desagregar más que él.
- **Falacia ecológica** (hereda del original): no sacar conclusiones
  sobre NNA individuales desde datos de un territorio, ni viceversa. Si
  se cruzan niveles (NNA vs. departamento), aclararlo en texto y título.
- **Correlación vs. causación** (hereda del original): lenguaje siempre
  observacional. Con registros administrativos esto es aún más
  restrictivo: ni siquiera hay diseño muestral, así que ninguna
  asociación observada en ellos sostiene lenguaje causal ("la pobreza
  provoca...") ni inferencial ("significativamente mayor").
- **Sin intervalos de confianza que no se puedan respaldar** (hereda del
  original): si la documentación de la ENSANNA no publica variables de
  diseño muestral (conglomerado/estrato), no se calculan errores
  estándar asumiendo muestreo aleatorio simple — estimación puntual
  ponderada y nada más. Verificar qué publica ANDA antes de decidir.
- **Integridad visual del eje y la escala** (hereda del original): eje y
  de barras siempre desde cero, nunca 3D, nunca apilar proporciones que
  no suman 100% entre sí.

## 3. Reglas del bloque predictivo (proyecciones inerciales)

El proyecto se organiza en dos bloques globales (ver
`CATALOGO_DE_METRICAS.md`): **descriptivo** ("¿qué pasó?") y
**predictivo** ("¿qué va a pasar si nada cambia?"), siguiendo el modelo
de madurez analítica de Gartner y la distinción formal entre modelar
para explicar y modelar para predecir de Shmueli (2010) — citas en
`BIBLIOGRAFIA.md`. Todo lo predictivo de este proyecto se rige por estas
reglas:

- **Solo escenarios inerciales, nunca pronósticos causales.** Lo que se
  proyecta es la continuación de una tendencia observada bajo el
  supuesto explícito de que las condiciones actuales persisten
  ("escenario si nada cambia"). Redacción correcta: "si la tendencia
  2013-2024 continúa, el sistema atendería ~X situaciones en 2027";
  prohibido: "la violencia va a aumentar" o cualquier forma que suene a
  ley natural o a causa identificada.
- **Sobre registros administrativos se proyecta la respuesta del
  sistema, no el fenómeno.** Una proyección de la serie SIPIAV proyecta
  cuántas situaciones va a *atender* el sistema — no cuánta violencia va
  a *haber*. La regla central del proyecto (casos atendidos ≠
  prevalencia) se hereda intacta hacia el futuro proyectado, y va en el
  título de la gráfica proyectada.
- **Serie mínima y horizonte máximo.** No se proyecta ninguna serie con
  menos de 6 puntos comparables (sin quiebre de definición en el
  medio), y el horizonte no supera un tercio del largo de la serie
  (regla práctica del forecasting — Hyndman & Athanasopoulos): 12
  puntos anuales → proyectar a lo sumo 3-4 años. Series de 4 puntos
  (CONAPEES, Fiscalía) se declaran insuficientes, no se fuerzan.
- **Modelos simples y a la vista.** Tendencia lineal o log-lineal (o
  deriva simple), estimada sobre la serie completa comparable. Con n <
  15 no se usan modelos complejos ni aprendizaje automático: más
  parámetros que datos es sobreajuste garantizado.
- **Toda proyección lleva rango, nunca un número único.** El intervalo
  sale de los residuos del modelo sobre la serie observada (esto es
  legítimo y distinto del caso "sin variables de diseño muestral" de la
  sección 2: aquí la incertidumbre es del modelo de tendencia, no del
  diseño de una encuesta, y se declara como tal).
- **Backtesting antes de publicar.** Ajustar el modelo dejando fuera los
  últimos 2 puntos de la serie y verificar que los predice
  razonablemente; si no los predice, la proyección no se publica. Cuando
  exista un dato nuevo real (ej. el informe SIPIAV 2025 ya presentado),
  se usa como validación fuera de muestra antes que como punto más.
- **Denominadores futuros: proyecciones oficiales del INE.** Toda tasa
  proyectada ("cada 1.000 NNA en 2027") usa las proyecciones de
  población publicadas por el INE como denominador, citadas — nunca un
  denominador extrapolado por este proyecto.
- **Los quiebres cortan la serie también hacia adelante.** Una serie con
  cambio de definición (tipos de violencia 2020/2024, canasta de
  pobreza 2019→2023) solo se proyecta desde el último tramo homogéneo.

## 4. Reglas de terminología y claridad

- **Usar los términos de cada organismo y definirlos la primera vez.**
  "Situación" (SIPIAV) no es "caso nuevo" ni "denuncia"; "trabajo
  infantil" (ENSANNA/OIT) tiene definición normativa precisa (Convenios
  OIT 138 y 182) que no coincide con "NNA que realiza alguna actividad".
  Nunca renombrar una variable de forma que sugiera algo que no mide
  (lección heredada del caso "nivel de ingreso"/"nivel económico" del
  proyecto original).
- **El tema es sensible: precisión también en la redacción.** Se escribe
  "niñas, niños y adolescentes" o "NNA" (la forma de los organismos),
  "situación de trabajo infantil" (no "niños trabajadores"), "víctima de
  explotación" (no formas que desplacen responsabilidad). El lenguaje de
  los informes de SIPIAV/CONAPEES es la referencia.
- **Cada gráfica necesita una razón de ser** (hereda del original): si no
  se puede explicar en una frase qué pregunta responde, no se incluye.
- **Nunca imprimir estructuras crudas de Python/pandas en un output que
  sobrevive al informe** (hereda del original): números en prosa
  formateada o en la gráfica, nunca un dict o una Series al desnudo.
- **No dejar huecos de numeración ni referencias colgando** al borrar o
  renombrar secciones (hereda del original).
