# Convenciones de gráficas: justificar el tipo elegido, con fundamento

Este proyecto adopta las convenciones de visualización del proyecto
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)
(`docs/CONVENCIONES_DE_GRAFICAS.md` de ese repositorio es la versión
extendida, con la cita concreta de cada patrón). Las citas completas
están en [`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md), sección "Visualización de
datos". Acá se resume lo que aplica igual y se agrega lo específico de
este proyecto.

**Cada gráfica va acompañada de una justificación con fundamento, no solo
una frase intuitiva.** Toda métrica lleva, además de su nombre y su
pregunta guía: la fórmula o definición exacta cuando exista notación
estándar (antes de la gráfica), y por qué ese tipo de gráfica con el
principio que lo respalda (después de la gráfica: primero se ve el dato,
después se entiende por qué está presentado así). No hay métrica
"demasiado simple" como para saltearse la gráfica o la justificación.

## Patrones heredados (resumen)

- **Barras horizontales** para categorías con nombres largos (tipos de
  violencia, dimensiones de protección) — Cleveland & McGill (1984);
  orden por total (Gestalt de continuidad, Ware).
- **Barras agrupadas** para comparar el mismo dato entre grupos, lado a
  lado — Few. Nunca apilar proporciones que no suman 100% entre sí.
- **Líneas con marcadores y eje x en escala temporal real** para series
  de 3+ años (los informes anuales de SIPIAV sí forman serie). Los
  marcadores distinguen "medición real" de "interpolación visual" —
  Cleveland & McGill aplicado al eje temporal.
- **Nunca torta con más de 3-4 categorías** — Cleveland & McGill; Cohen
  et al. (2016).
- **Eje y desde cero, nunca 3D** — Healy (2018).
- **Data-ink ratio**: ningún elemento visual que no aporte información —
  Tufte (1983).

## Específico de este proyecto

- **Toda serie temporal anota el valor de su primer y su último punto**
  (y, si hay proyección, también el punto final proyectado). Le da al
  lector las dos o tres cifras de referencia sin recargar la gráfica —
  equilibrio con el principio de data-ink de Tufte: se anotan los
  extremos que el lector necesita, no todos los puntos. Estandarizado a
  pedido del dueño del proyecto (2026-08-17).

- **Toda gráfica construida desde registros administrativos (SIPIAV,
  CONAPEES, INAU) lleva en el título o subtítulo la aclaración de que
  muestra situaciones atendidas/detectadas por el sistema, no
  prevalencia.** Quien mira solo la gráfica también tiene que poder
  leerla bien — es la regla central de `METODOLOGIA.md` aplicada al
  plano visual.
- **Cortes de serie se dibujan como puntos sueltos, no como línea**
  (caso ENTI 2010 / ENSANNA 2024): si dos mediciones no tienen
  comparabilidad metodológica verificada, una línea que las une inventa
  una tendencia que no se midió.
- **Números chicos de víctimas**: si una desagregación cae por debajo
  del umbral de publicación del propio organismo, no se grafica más
  desagregado que lo que el organismo publica.
