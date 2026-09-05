# Fuentes de datos: qué publica cada organismo y qué es (y qué no es) cada dato

Catálogo de las fuentes institucionales del proyecto. Antes de usar un
número de cualquiera de estas fuentes, leer la columna "naturaleza del
dato" — es la diferencia entre una afirmación defendible y una incorrecta
(ver la regla central de [`METODOLOGIA.md`](METODOLOGIA.md), sección 2).

Las citas completas para referenciar en informes están en
[`BIBLIOGRAFIA.md`](BIBLIOGRAFIA.md).

## Resumen

| Fuente | Tipo de dato | Nivel | Periodicidad |
|---|---|---|---|
| ENSANNA 2024 (INE/MTSS) | Encuesta con microdatos públicos | Persona/hogar | Puntual (antecedente 2009-2010) |
| SIPIAV | Registro administrativo (informes agregados) | Casos atendidos | Anual (desde 2013) |
| INAU — SIPI | Registro administrativo (indicadores agregados) | Población atendida por INAU | Semestral (anual desde 2026) |
| CONAPEES | Registro administrativo + planes + estudios | Casos atendidos / documentos | Irregular |
| UNICEF Uruguay | Portal de indicadores + publicaciones técnicas | Agregado (reprocesa ECH/ENSANNA/registros) | Continua |
| CETI (MTSS) | Comité interinstitucional: planes y documentos | Documentos de política | Irregular |
| Encuesta violencia sexual NNA 2026 (UNICEF/Equipos) | Encuesta retrospectiva, muestra no probabilística | Personas de 18 a 24 años | Puntual (2026) |
| INE — proyecciones de población (rev. 2025) | Proyección demográfica oficial | Población por sexo y edad | Revisión tras cada censo |
| ENDIS 2023 (INE) | Encuesta con microdatos para terceros | Niñas y niños de 0 a 59 meses | Cohorte 2023 |

## 1. ENSANNA 2024 — Encuesta Nacional sobre las Actividades de Niñas, Niños y Adolescentes (INE/MTSS, con OIT y UNICEF)

- **Qué es**: encuesta a hogares relevada por el INE en el segundo
  semestre de 2024, en convenio con el MTSS y con apoyo de OIT y UNICEF
  Uruguay. Mide trabajo infantil y actividades de NNA. Es la **única
  fuente de este proyecto con microdatos públicos** (portal ANDA del
  INE), y por eso la única donde aplican en pleno las reglas de encuesta
  del proyecto original (ponderación, celdas chicas).
- **Universo**: NNA de **5 a 17 años** (ver
  [`CLASIFICACION_DE_EDADES.md`](CLASIFICACION_DE_EDADES.md)).
- **Resultados centrales publicados**: 6,8% de los NNA de 5 a 17 en
  situación de trabajo infantil (más de 40.000); 4,9% en actividades
  económicas remuneradas y ~2% en tareas no remuneradas; 10,6% en el
  tramo 15-17; interior 7,7% vs. Montevideo 5,2%.
- **Antecedente**: la encuesta anterior sobre el tema es de 2009-2010
  (ENTI/ENANNA, ~68.000 NNA afectados). **No graficar 2010 vs. 2024 como
  serie sin verificar comparabilidad metodológica** (ver
  `METODOLOGIA.md`, sección 2).
- **Dónde**:
  - Página oficial INE: https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/encuestas/encuesta-nacional-sobre-actividades-ninas-ninos-adolescentes-ensanna
  - Página MTSS: https://www.gub.uy/ministerio-trabajo-seguridad-social/politicas-y-gestion/encuesta-nacional-sobre-actividades-ninas-ninos-adolescentes-ensanna-2024
  - Microdatos: catálogo ANDA del INE (https://www4.ine.gub.uy/Anda5/)
- **Naturaleza del dato**: estimación de prevalencia con diseño muestral
  → sí permite afirmaciones del tipo "X% de los NNA...", siempre
  ponderadas.

## 2. SIPIAV — Sistema Integral de Protección a la Infancia y a la Adolescencia contra la Violencia (coordina INAU)

- **Qué es**: sistema interinstitucional (INAU, MIDES, MSP, ANEP, Fiscalía,
  Poder Judicial, entre otros) que registra y atiende situaciones de
  violencia hacia NNA. Publica un **informe anual** con datos del sistema
  (serie desde 2013 aprox.).
- **Cifras 2024 publicadas**: 8.924 situaciones atendidas (promedio 24
  por día), 2.501 casos nuevos; la franja 13-17 años concentra la mayor
  cantidad (38%); 22% violencia sexual, con casi 80% de esos casos en
  niñas y adolescentes mujeres; ~90% de las situaciones detectadas eran
  recurrentes y 75% crónicas.
- **Cifras 2025 publicadas** (informe de gestión 2025, presentado el
  27/04/2026): 9.178 situaciones registradas con la metodología
  tradicional — y 7.381 con la **nueva metodología** que el mismo
  informe introduce (solo violencias activas en el año o cerradas
  explícitamente); 2.536 nuevas situaciones (casi 7 por día). Las
  desagregaciones 2025 incluyen una categoría explícita "sin
  información" (17%) que rompe la comparabilidad de recurrencia,
  cronicidad e inclusión familiar con la serie histórica — quiebres 7 y
  8 de `datos_curados/sipiav_notas.md`.
- **Dónde**: https://www.inau.gub.uy/noticias/2026/sipiav-presento-informe-2025
  (noticia de presentación del último informe; el sitio migrado del INAU
  ya no tiene página institucional del SIPIAV y los informes viven en su
  gestor documental, ver `RELEVAMIENTO_DE_DATOS.md`).
- **Naturaleza del dato**: **registro administrativo de casos detectados
  y atendidos por el sistema — NO es prevalencia**. Un aumento
  interanual puede reflejar mayor capacidad de detección, no
  necesariamente más violencia. Esta distinción es la regla de rigor
  central del proyecto (ver `METODOLOGIA.md`, sección 2, primera regla).

## 3. INAU — SIPI e Indicadores del Sistema de Protección Especial

- **Qué es**: el SIPI (Sistema de Información Para la Infancia, en
  producción desde 2010) registra a toda la población atendida por INAU.
  De ahí salen los **Indicadores del Sistema de Protección Especial**
  publicados en la sección Transparencia, estructurados en dimensiones:
  cobertura, trayectorias, adopciones, cuidados y vínculos, educación y
  salud. Publicación semestral; anunciada como anual desde enero 2026
  (con información 2020-2025).
- **Dónde**:
  - Indicadores: https://inau.gub.uy/transparencia/indicadores-sistema-de-proteccion-especial-inau
  - Memorias anuales: https://www.inau.gub.uy/ (sección institucional)
- **Naturaleza del dato**: registro administrativo de la **población
  atendida por INAU** — describe a quienes están en el sistema de
  protección, no a la infancia uruguaya en general.

## 4. CONAPEES — Comité Nacional para la Erradicación de la Explotación Sexual Comercial y No Comercial de la Niñez y la Adolescencia

- **Qué es**: comité interinstitucional en la órbita de INAU. Produce
  planes nacionales (III Plan Nacional aprobado en julio de 2023),
  informes de situación y estudios (ej. explotación sexual y entornos
  digitales, con UNFPA).
- **Cifras publicadas**: 285 situaciones atendidas en un año (nota de
  Presidencia); 456 casos detectados con aumento de 24% interanual en
  2024 (nota de Facultad de Psicología/UdelaR). **Las dos cifras no son
  comparables entre sí sin verificar año y definición exacta** — caso de
  la regla de "misma métrica, misma definición" de `METODOLOGIA.md`.
- **Dónde**:
  - https://www.inau.gub.uy/noticias/2023/conapees-registro-169-nuevos-casos-de-explotacion-sexual-en-2023
    (noticia con las últimas cifras publicadas; el sitio migrado del
    INAU ya no tiene página institucional del CONAPEES).
  - Estudio entornos digitales (UNFPA): https://uruguay.unfpa.org/es/informe-conapees-explotacion-sexual-nna-entornos-digitales
- **Naturaleza del dato**: registro administrativo de casos detectados —
  mismas precauciones que SIPIAV, agravadas porque la explotación sexual
  tiene un subregistro reconocido por el propio comité.

## 5. UNICEF Uruguay — Infancia en Datos

- **Qué es**: portal de indicadores sobre infancia y adolescencia
  (salud, educación, protección, inclusión social, inversión pública) y
  publicaciones técnicas asociadas (pobreza infantil monetaria y
  multidimensional, trabajo infantil, inversión en infancia).
- **Cifras publicadas**: ~4 de cada 10 niños en situación de pobreza;
  220.000 NNA en hogares con pobreza multidimensional.
- **Dónde**: https://www.unicef.org/uruguay/infancia-en-datos
- **Naturaleza del dato**: **fuente secundaria** — reprocesa ECH, ENSANNA
  y registros administrativos. Al citar un número de este portal,
  identificar y citar también la fuente primaria y su año; si el mismo
  indicador se puede calcular desde microdatos propios (ECH/ENSANNA),
  preferir el cálculo propio y usar el del portal como verificación
  cruzada.

## 6. Encuesta sobre violencia sexual contra NNA, Uruguay 2026 (UNICEF Uruguay / Equipos Consultores)

- **Qué es**: encuesta web autoadministrada a personas de **18 a 24
  años** que viven en Uruguay, sobre experiencias de violencia sexual
  vividas antes de los 18 (medición retrospectiva). Publicada en abril
  de 2026. Archivo:
  `data/unicef/2026/encuesta_violencia_sexual_nna_2026_378.pdf`.
- **Resultados centrales**: 29% reporta haber sufrido violencia sexual
  antes de los 18 años ("casi 1 de cada 3"); 17% abuso sexual; 17%
  situaciones de explotación; 30% de las mujeres jóvenes; 69% de
  quienes sufrieron abuso no lo contó en su momento.
- **Naturaleza del dato**: **estimación de prevalencia retrospectiva con
  muestra no probabilística** (ficha metodológica, anexo 5.1: n = 617,
  reclutamiento por publicidad en redes sociales, calibración rake
  contra la ECH 2024). Es la única fuente de prevalencia de violencia
  del proyecto, pero **no admite margen de error en sentido
  probabilístico ni afirmaciones de representatividad**: se cita como
  orden de magnitud ("aproximadamente 3 de cada 10"), nunca como serie,
  nunca con decimales, y siempre con su diseño declarado. No es
  comparable con los registros SIPIAV (miden cosas distintas: respuesta
  del sistema vs. experiencia reportada).

## 7. CETI — Comité Nacional para la Erradicación del Trabajo Infantil (MTSS)

- **Qué es**: comité interinstitucional (Estado, empresas, sindicatos,
  ONG) que asesora y coordina la política contra el trabajo infantil.
  Con base en la ENSANNA 2024 está elaborando el primer **plan
  estratégico nacional** contra el trabajo infantil.
- **Dónde**: https://www.gub.uy/ministerio-trabajo-seguridad-social/
  (buscar "CETI"); antecedente: Plan Nacional de Erradicación del
  Trabajo Infantil (OIT/MTSS).
- **Naturaleza del dato**: documentos de política, no datos primarios —
  útil para el marco de políticas (qué se propone, con qué metas) contra
  el cual leer los datos de ENSANNA.

## 8. INE — Proyecciones de población, revisión 2025

- **Qué es**: proyecciones oficiales de población de Uruguay por sexo y
  edad, revisadas tras el Censo 2023 (período 2012-2070; archivos de
  proyección publicados desde 2024). Publicadas el 17/07/2025. Es la
  fuente de los denominadores poblacionales del proyecto (P4, P6):
  `data/ine/proyecciones_rev2025/`.
- **Cifras centrales para el proyecto**: población 0-17 = 768.969 en
  2024 (22,0% del total) y cayendo ~2,3% anual (715.901 en 2027) — el
  denominador de toda tasa del proyecto se achica año a año.
- **Naturaleza del dato**: **proyección demográfica del organismo
  productor**, con metodología y supuestos propios (fecundidad,
  mortalidad, migración). No se modela ni se extrapola nada sobre ella:
  se cita. Dos advertencias de uso: (a) los ponderadores de la ECH
  siguen calibrados a la revisión anterior (0-17 = 24,1% en la ECH 2024
  vs. 22,0% en la revisión 2025) — no mezclar bases sin anotarlo; (b)
  el archivo departamental es quinquenal: 0-17 exacto solo existe a
  nivel país (ver `RELEVAMIENTO_DE_DATOS.md`, sección 7).

## 9. ENDIS 2023 — Encuesta de Nutrición, Desarrollo Infantil y Salud (INE)

- **Qué es**: encuesta del INE a niñas y niños de 0 a 59 meses y sus
  hogares (nutrición, desarrollo infantil, salud, cuidados y asistencia
  a centros de primera infancia). La cohorte 2023 publica para terceros
  siete bases con su factor de expansión (`W`) en el catálogo ANDA
  (entrada 765). Incorporada el 2026-09-05 a partir de una métrica a
  medida pedida en el flujo guiado.
- **Universo**: niñas y niños de **0 a 59 meses** (ver
  [`CLASIFICACION_DE_EDADES.md`](CLASIFICACION_DE_EDADES.md)).
- **Resultado usado**: cobertura de centros de primera infancia por
  tramo de edad y tipo de prestador (métrica 37): 66,9% asiste a algún
  centro en el conjunto 0-59 meses; 20,9% entre los menores de un año y
  97,0% entre los 48 y los 59 meses.
- **Dónde**: catálogo ANDA del INE,
  https://www4.ine.gub.uy/Anda5/index.php/catalog/765 (los microdatos
  se descargan aceptando los términos del INE personalmente — nunca de
  forma automática — y se colocan en `data/endis_microdatos/2023/`).
- **Naturaleza del dato**: estimación con diseño muestral → sí permite
  afirmaciones del tipo «X% de las niñas y los niños de 0 a 4 años...»,
  siempre ponderadas y con su n muestral. La base para terceros no
  distingue con seguridad «no asiste» de «sin dato de asistencia»: se
  informa «sin centro registrado».

---

**Cómo agregar una fuente nueva**: incorporarla aquí con su "naturaleza del
dato" explícita, y la cita completa en `BIBLIOGRAFIA.md`. Si la fuente es
un registro administrativo, la primera pregunta a responder por escrito
es: ¿qué población cubre y qué evento registra exactamente?
