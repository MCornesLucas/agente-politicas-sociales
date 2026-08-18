# Agente de Políticas Sociales de Infancia — Uruguay

Análisis con rigor estadístico de las políticas sociales de infancia en
Uruguay, a partir de datos oficiales de los organismos del sistema de
protección: **SIPIAV, INAU, CONAPEES, CETI, UNICEF Uruguay** y la
**ENSANNA 2024** (Encuesta Nacional sobre las Actividades de Niñas, Niños
y Adolescentes, INE/MTSS).

Es el proyecto hermano de
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares):
hereda su marco metodológico (reglas de rigor no negociables,
bibliografía auditada, justificación con fundamento de cada gráfica) y lo
aplica a un problema nuevo — y más difícil: aquí la mayoría de las fuentes
no son encuestas, son **registros administrativos**, donde la pregunta
"¿qué mide realmente este número?" es la diferencia entre un análisis
serio y uno equivocado.

## Idea base

El proyecto avanza en dos etapas:

1. **Recabar y sistematizar** la mayor cantidad posible de estudios,
   informes y datos de políticas sociales de infancia de los organismos
   del sistema de protección uruguayo, con la naturaleza de cada dato
   documentada.
2. **Cruzar** esos hallazgos con los indicadores de infancia y
   adolescencia calculables desde los microdatos de la ECH (pobreza,
   hacinamiento, condiciones de vivienda, brecha digital) con la
   infraestructura ya probada de agente-encuesta-hogares — la ECH se
   adapta al rango de edad de cada fuente, no al revés.

El universo es **0 a 17 años** (la definición de la Convención sobre los
Derechos del Niño), sin fijar un rango más angosto a priori: cada
organismo clasifica distinto y cada métrica usa el rango de su fuente —
ver [`docs/CLASIFICACION_DE_EDADES.md`](docs/CLASIFICACION_DE_EDADES.md).

## La regla que define el proyecto

> **Casos atendidos ≠ prevalencia.** Cuando SIPIAV informa 8.924
> situaciones de violencia atendidas en 2024 (24 por día), ese número
> mide la respuesta del sistema de protección — no cuántos niños sufren
> violencia en Uruguay. Un aumento interanual puede significar mejor
> detección, más denuncia, o más violencia: el registro solo no permite
> distinguirlo. Este proyecto redacta y grafica cada dato respetando esa
> diferencia.

Las demás reglas (comparabilidad de definiciones y denominadores, cortes
de serie que no se interpolan, ponderación de microdatos, celdas chicas,
lenguaje observacional, integridad visual) están en
[`docs/METODOLOGIA.md`](docs/METODOLOGIA.md).

## Fuentes de datos

| Organismo | Qué aporta | Naturaleza |
|---|---|---|
| [SIPIAV](https://www.inau.gub.uy/sipiav) | Informes anuales de violencia hacia NNA (serie desde 2013) | Registro administrativo |
| [INAU — SIPI](https://inau.gub.uy/transparencia/indicadores-sistema-de-proteccion-especial-inau) | Indicadores del Sistema de Protección Especial | Registro administrativo |
| [CONAPEES](https://www.inau.gub.uy/conapees) | Planes nacionales y datos de explotación sexual de NNA | Registro + documentos |
| [CETI (MTSS)](https://www.gub.uy/ministerio-trabajo-seguridad-social/comunicacion/noticias/ceti) | Política nacional contra el trabajo infantil | Documentos de política |
| [UNICEF Uruguay](https://www.unicef.org/uruguay/infancia-en-datos) | Portal Infancia en Datos, pobreza infantil, inversión | Fuente secundaria |
| [ENSANNA 2024 (INE)](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/encuestas/encuesta-nacional-sobre-actividades-ninas-ninos-adolescentes-ensanna) | Microdatos públicos de trabajo infantil | Encuesta (prevalencia) |

El detalle de qué publica cada uno, con sus advertencias de uso, está en
[`docs/FUENTES_DE_DATOS.md`](docs/FUENTES_DE_DATOS.md).

## Estructura del repositorio

```
docs/
  METODOLOGIA.md              Reglas de rigor estadístico y terminología (no negociables)
  FUENTES_DE_DATOS.md         Qué publica cada organismo y qué es (y qué no es) cada dato
  BIBLIOGRAFIA.md             Índice único de fuentes, por tema
  CATALOGO_DE_METRICAS.md     Métricas candidatas por tema, con su advertencia de rigor
  CONVENCIONES_DE_GRAFICAS.md Justificación con fundamento del tipo de gráfica
data/                         Datos descargados de las fuentes (no versionados)
datos_curados/                Series curadas con respaldo textual por valor
notebooks/                    Informes generados
resultados/                   Agregados calculados (ponderados, versionables)
src/politicas_sociales/       Paquete Python: extracción, métricas, cruces,
                              proyecciones y construcción del informe
tests/                        Suite de la lógica del paquete y sus guardianes
```

## Instalación y ejecución

Requiere Python 3.10 o superior y el proyecto hermano
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)
como carpeta hermana (o su ruta en la variable de entorno
`AGENTE_ECH_RUTA`): los loaders de la ECH se importan desde su copia de
trabajo para heredar las correcciones al día.

**Instalación rápida (Windows)**: doble clic en `instalar.bat` — detecta
Python (Anaconda), verifica el proyecto hermano, instala el paquete con
sus dependencias y prepara el generador de PDF. Deja la ruta de Python
en `.claude/python_path.txt`, que `run_python.bat` usa para ejecutar
cualquier comando sin depender del PATH de cada máquina:

```bash
run_python.bat -m politicas_sociales.metricas_ech
```

**Instalación manual** (cualquier sistema):

```bash
python -m pip install -e ".[dev]"
```

Los pipelines se ejecutan como módulos del paquete — por ejemplo
`python -m politicas_sociales.metricas_ech` — y la suite con
`python -m pytest`.

## Estado

**Fase de análisis (v0.2)**: catálogo de 36 métricas descriptivas en 5
temas, confirmado métrica por métrica contra los archivos reales
(`docs/CATALOGO_DE_METRICAS.md`); series SIPIAV 2013-2025 curadas con
respaldo textual por valor (`datos_curados/`); bloque predictivo con
protocolo de backtest aplicado: P1 calculada y validada con el dato real
2025, P2 y P3 calculadas, P4 resuelta como lectura descriptiva (el
numerador se amesetó y ningún modelo supera al ingenuo), P6 citada del
INE (revisión 2025 descargada); los cuatro cruces entre fuentes del
catálogo calculados, cada uno con sus limitaciones declaradas
(`resultados/cruces/`). Informe en `notebooks/`.

Pendientes que dependen de terceros: microdatos ENSANNA (INE los lista
"en análisis"), serie ESNNA 2022+ oficial (CONAPEES), estimaciones
retrospectivas de la revisión 2025 del INE, plan estratégico del CETI
basado en la ENSANNA. El detalle vive en
`docs/RELEVAMIENTO_DE_DATOS.md`.

## Licencia

[PolyForm Noncommercial 1.0.0](LICENSE) — uso no comercial.
