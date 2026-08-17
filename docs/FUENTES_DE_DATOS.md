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

## 1. ENSANNA 2024 — Encuesta Nacional sobre las Actividades de Niñas, Niños y Adolescentes (INE/MTSS, con OIT y UNICEF)

- **Qué es**: encuesta a hogares relevada por el INE en el segundo
  semestre de 2024, en convenio con el MTSS y con apoyo de OIT y UNICEF
  Uruguay. Mide trabajo infantil y actividades de NNA. Es la **única
  fuente de este proyecto con microdatos públicos** (portal ANDA del
  INE), y por eso la única donde aplican en pleno las reglas de encuesta
  del proyecto original (ponderación, celdas chicas).
- **Resultado central publicado**: más de 40.000 NNA en situación de
  trabajo infantil.
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
- **Dónde**: https://www.inau.gub.uy/sipiav (informes descargables).
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
  - https://www.inau.gub.uy/conapees
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

## 6. CETI — Comité Nacional para la Erradicación del Trabajo Infantil (MTSS)

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

---

**Cómo agregar una fuente nueva**: sumarla acá con su "naturaleza del
dato" explícita, y la cita completa en `BIBLIOGRAFIA.md`. Si la fuente es
un registro administrativo, la primera pregunta a responder por escrito
es: ¿qué población cubre y qué evento registra exactamente?
