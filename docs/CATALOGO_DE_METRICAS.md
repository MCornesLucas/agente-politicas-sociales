# Catálogo de métricas (borrador de diseño)

Catálogo inicial de métricas candidatas, organizado por tema, con su
fuente y la advertencia de rigor que le corresponde. **Estado: borrador**
— cada métrica se confirma recién cuando se verifica que el dato existe
publicado con la definición esperada (regla: nunca prometer una métrica
cuyo dato no se descargó y miró). Las cinco partes que lleva cada métrica
en un informe (nombre, pregunta, términos, gráfica, justificación) están
definidas en [`METODOLOGIA.md`](METODOLOGIA.md), sección 1.

## Tema 1 — Violencia hacia NNA (fuente: informes anuales SIPIAV)

| # | Métrica | Pregunta que responde | Advertencia |
|---|---|---|---|
| 1 | Situaciones atendidas por año (serie 2013-2024) | ¿Cómo evoluciona la respuesta del sistema? | Casos atendidos ≠ prevalencia; serie válida porque la fuente y la definición son constantes |
| 2 | Casos nuevos vs. arrastre por año | ¿Cuánto de lo atendido es detección nueva? | Definir "situación" vs. "caso nuevo" según el glosario SIPIAV |
| 3 | Distribución por tramo de edad | ¿En qué edades se concentra la detección? | Tramos del informe (0-5, 6-12, 13-17), no re-agrupar |
| 4 | Distribución por tipo de violencia | ¿Qué tipo de violencia se detecta más? | Categorías del informe; violencia sexual desagregada por sexo cuando el informe lo publica |
| 5 | Recurrencia y cronicidad | ¿Se detecta a tiempo? | ~90% recurrente / 75% crónica en 2024 — indicador de detección tardía, así se redacta |

## Tema 2 — Explotación sexual (fuente: CONAPEES)

| # | Métrica | Pregunta que responde | Advertencia |
|---|---|---|---|
| 6 | Situaciones atendidas por año | ¿Cómo evoluciona la detección? | Subregistro reconocido por el comité; resolver primero la discrepancia 285 vs. 456 (ver `FUENTES_DE_DATOS.md`) |
| 7 | Modalidades (incluida la digital) | ¿Qué formas toma y cuánto pesa el entorno digital? | Fuente cualitativa/estudio, no serie — presentar como estado de situación |

## Tema 3 — Trabajo infantil (fuente: ENSANNA 2024, microdatos ANDA)

| # | Métrica | Pregunta que responde | Advertencia |
|---|---|---|---|
| 8 | % de NNA en trabajo infantil (ponderado) | ¿Qué prevalencia tiene el trabajo infantil? | Única familia de métricas con prevalencia real; ponderar siempre |
| 9 | Prevalencia por sexo y tramo de edad | ¿Quiénes están más afectados? | Celdas chicas (n<30): aclarar base muestral |
| 10 | Prevalencia por región/área | ¿Dónde se concentra? | Verificar el nivel de desagregación que soporta el diseño muestral |
| 11 | Asistencia escolar según condición de trabajo | ¿Cómo se relaciona con la escolarización? | Lenguaje observacional, nunca causal |
| 12 | Comparación puntual con ENTI 2009-2010 | ¿Qué cambió en 15 años? | Corte de serie: puntos sueltos + nota de comparabilidad, nunca línea |

## Tema 4 — Protección especial (fuente: INAU, indicadores SIPI)

| # | Métrica | Pregunta que responde | Advertencia |
|---|---|---|---|
| 13 | Cobertura por modalidad de atención | ¿A cuántos NNA atiende INAU y cómo? | Población atendida por INAU, no infancia general |
| 14 | Trayectorias (tiempo en el sistema) | ¿Cuánto duran las intervenciones? | Según dimensión "trayectorias" del reporte SIPI |
| 15 | Adopciones por año | ¿Cómo evoluciona la vía de egreso por adopción? | Números chicos: cuidado con desagregar |

## Tema 5 — Pobreza infantil e inversión (fuente: UNICEF Uruguay + cálculo propio sobre ECH)

| # | Métrica | Pregunta que responde | Advertencia |
|---|---|---|---|
| 16 | Pobreza monetaria en NNA (ponderada, ECH) | ¿Qué % de NNA vive en hogares pobres? | Preferir cálculo propio sobre microdatos ECH (infraestructura ya probada en agente-encuesta-hogares); portal UNICEF como verificación cruzada |
| 17 | Pobreza multidimensional en NNA | ¿Qué privaciones concretas sufren? | Citar la metodología exacta del IPM usado por la fuente |
| 18 | Brecha de pobreza NNA vs. adultos | ¿Está la pobreza infantilizada? | Mismo año, misma línea de pobreza, mismo denominador |

---

**Regla transversal**: los temas 1, 2 y 4 salen de registros
administrativos — ninguna de sus métricas habla de prevalencia. Los temas
3 y 5 salen de encuestas — sus métricas se ponderan siempre. La nota
metodológica del informe explica esta diferencia una vez, en lenguaje
simple.
