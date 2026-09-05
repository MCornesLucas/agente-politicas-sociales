"""Celdas del informe — introducción, preparación y temas 1 a 3.

Toda cifra citada en los textos proviene de los archivos curados del
repositorio (datos_curados/, resultados/) o de los documentos
descargados y verificados en data/ — ver docs/RELEVAMIENTO_DE_DATOS.md.
"""

from __future__ import annotations

from politicas_sociales.informe_base import code, md

# El alcance del informe completo. Las ediciones parciales (selección de
# temas por el usuario) reemplazan este texto por uno que describe lo que
# la edición realmente contiene — la introducción nunca promete contenido
# que no está (misma decisión que sacar "el catálogo completo" del texto).
ALCANCE_COMPLETO = """métricas agrupadas en **seis
temas** (violencia hacia niñas, niños y adolescentes; explotación
sexual; trabajo infantil; protección especial; pobreza, vivienda y
entorno del hogar; primera infancia y cuidados), junto con las proyecciones calculadas y validadas
hasta la fecha y los **cuatro cruces entre fuentes** (INAU,
CONAPEES/Fiscalía, ENSANNA y SIPIAV contra la ECH), cada uno con sus
limitaciones declaradas"""


def celda_introduccion(alcance: str = ALCANCE_COMPLETO):
    return md(f"""
# Políticas sociales de infancia en Uruguay — Informe

Este informe presenta {alcance}. Cada métrica se presenta con la pregunta que responde,
su gráfica, la justificación del tipo de gráfica elegido y su lectura,
con la fuente citada en cada caso
([agente-politicas-sociales](https://github.com/MCornesLucas/agente-politicas-sociales)).

El informe integra en cada tema sus métricas **descriptivas** (qué está
pasando) y **predictivas** (qué sucedería si las condiciones actuales
persisten — siempre como escenario inercial con rango, nunca como
pronóstico).

**Advertencia central de lectura**: la mayoría de las fuentes de este
informe son registros administrativos — miden las situaciones que cada
sistema detecta y atiende, no cuántos niños atraviesan cada problema en
el país. La nota metodológica del final explica esta diferencia en
lenguaje simple; cada gráfica la lleva incorporada en su título.
""")


CELDAS = [
    # ==================================================================
    celda_introduccion(),
    # ==================================================================
    md("""
## Preparación de datos

Se cargan las fuentes curadas y documentadas que alimentan este
informe (con inventario de descargas y respaldo textual de cada valor
en sus notas de curaduría):

- **SIPIAV**: series 2013-2025 curadas de los trece informes de gestión
  (INAU), con sus quiebres metodológicos documentados.
- **CONAPEES / Fiscalía**: series 2018-2021 compiladas por el estudio
  FLACSO 2023 (capítulo 6).
- **ENSANNA 2024**: cuadros del boletín oficial (INE/MTSS) y su
  antecedente ENTI 2010.
- **INAU**: indicadores del Sistema de Protección Especial 2020-2025
  (SIPI) y reportes estadísticos de abril de 2025.
- **ECH**: métricas propias ponderadas 2019-2025, universo 0-17 años.
- **ENDIS 2023**: cobertura de centros de primera infancia, estimación
  ponderada sobre los microdatos publicados para terceros (INE), niñas y
  niños de 0 a 59 meses.
- **INE**: proyecciones de población, revisión 2025 (Censo 2023).
"""),
    code("""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# La raíz del proyecto se busca hacia arriba desde el directorio de
# trabajo: el notebook puede ejecutarse desde notebooks/, desde
# notebooks/ediciones/ (las ediciones del flujo guiado) o desde la raíz —
# la heurística anterior ("el padre si estoy en notebooks") fallaba en las
# ediciones, hallazgo de una corrida real del flujo guiado (2026-08-19).
RAIZ = Path.cwd()
while not (RAIZ / "datos_curados").is_dir() and RAIZ != RAIZ.parent:
    RAIZ = RAIZ.parent
CURADOS = RAIZ / "datos_curados"
RESULTADOS = RAIZ / "resultados"
DATA = RAIZ / "data"

SIP = pd.read_csv(CURADOS / "sipiav_series.csv")
CONA = pd.read_csv(CURADOS / "conapees_esnna.csv")
CONA_SEXO = pd.read_csv(CURADOS / "conapees_esnna_sexo.csv")
FISC = pd.read_csv(CURADOS / "fiscalia_delitos_sexuales_nna.csv")
ENS = pd.read_csv(CURADOS / "ensanna_2024.csv")
INAU = pd.read_csv(CURADOS / "inau_spe_nacional.csv", dtype={"indicador_codigo": str})
RAF = pd.read_csv(CURADOS / "inau_abril2025_acogimiento.csv")
DVF = pd.read_csv(CURADOS / "inau_abril2025_dvf.csv")
ECHM = pd.read_csv(RESULTADOS / "ech" / "metricas_ech_0a17.csv")
P3 = pd.read_csv(RESULTADOS / "proyecciones" / "p3_desinternacion.csv")
P4 = pd.read_csv(RESULTADOS / "proyecciones" / "p4_tasa_spe.csv")

COLOR = "#2a5674"
ACENTO = "#c05555"
PALETA = ["#2a5674", "#c05555", "#7a9a6d", "#b08a3e", "#6b5b8e", "#888888"]
plt.rcParams.update({
    "figure.figsize": (9, 4.6),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 12,
    "figure.dpi": 110,
})


def fmt(v):
    return f"{v:,.0f}".replace(",", ".")


def pct(v, dec=1):
    return f"{v:.{dec}f}".replace(".", ",") + "%"


def serie_sipiav(metrica, categoria=None):
    s = SIP[SIP["metrica"] == metrica]
    if categoria is not None:
        s = s[s["categoria"] == categoria]
    s = s.sort_values("anio")
    return s["anio"].to_numpy(), s["valor"].to_numpy(dtype=float)


def serie_inau(codigo):
    s = INAU[(INAU["indicador_codigo"] == codigo) & (INAU["apertura"] == "total")].sort_values("anio")
    return s["anio"].to_numpy(), s["valor"].to_numpy(dtype=float)


def anotar_extremos(ax, x, y, color, dec=0):
    for xi, yi in [(x[0], y[0]), (x[-1], y[-1])]:
        etiqueta = fmt(yi) if dec == 0 else f"{yi:.{dec}f}".replace(".", ",")
        ax.annotate(etiqueta, (xi, yi), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=9, color=color)


def fuente(fig, texto, y=-0.04):
    fig.text(0.125, y, texto, fontsize=8, color="#555555")


def linea_con_huecos(ax, anios_todos, df_pivot, colores=None):
    colores = colores or PALETA
    for i, col in enumerate(df_pivot.columns):
        y = df_pivot[col].reindex(anios_todos)
        ax.plot(anios_todos, y, marker="o", linewidth=1.8,
                color=colores[i % len(colores)], label=col)
"""),
    # ==================================================================
    md("""
## Violencia hacia niñas, niños y adolescentes (SIPIAV)

Este tema mide la **respuesta del sistema de protección**, con datos del
SIPIAV (Sistema Integral de Protección a la Infancia y a la Adolescencia
contra la Violencia, coordinado por INAU e integrado, entre otros, por
MIDES, MSP, ANEP, Fiscalía y Poder Judicial). Serie curada de los trece
informes de gestión 2013-2025, con respaldo textual de cada valor.

Términos utilizados por la fuente:

- **Situación**: cada caso de violencia hacia un NNA detectado,
  registrado e intervenido por el sistema durante el año.
- **Registro administrativo**: la fuente cuenta lo que el sistema
  atiende, no la totalidad de la violencia existente.

**Advertencia 2025**: el informe de gestión 2025 introduce una nueva
metodología de registro en paralelo a la tradicional (7.381 situaciones
bajo la definición nueva frente a 9.178 bajo la tradicional) y presenta
sus desagregaciones con una categoría explícita de datos faltantes
(17% «sin información»). Las series de este tema continúan con la
metodología tradicional — que el propio informe mantiene «para preservar
la comparabilidad longitudinal» — y cada métrica afectada por el cambio
de base lo indica.
"""),
    md("""
### Métrica 1. Situaciones de violencia atendidas por el sistema, 2013-2025

**¿Qué pregunta responde?** ¿Cómo evolucionó la cantidad de situaciones
de violencia hacia NNA que el sistema de protección detecta y atiende
cada año?
"""),
    code("""
anios, valores = serie_sipiav("situaciones_atendidas")
fig, ax = plt.subplots()
ax.plot(anios, valores, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 10500)
ax.set_xticks(anios)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_title(
    "Situaciones de violencia hacia NNA atendidas por el SIPIAV por año\\n"
    "(situaciones detectadas y atendidas por el sistema — no equivale a prevalencia)"
)
ax.set_ylabel("Situaciones atendidas")
anotar_extremos(ax, anios, valores, COLOR)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2025 (INAU), metodología tradicional. "
            "Serie 2011-2025 publicada en texto por el informe 2025.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual de mediciones reales: línea con
marcadores sobre eje temporal en escala real (Cleveland y McGill,
1984), eje vertical desde cero (Healy, 2018) y extremos anotados
(convenciones de gráficas de este informe).

**Lectura**: las situaciones atendidas se multiplicaron por 7 entre 2013
(1.319) y 2025 (9.178). La serie tiene saltos con explicación
documental: la incorporación del hospital Pereira Rossell como fuente
(2018-2019) y el efecto pospandemia (2021, +43%). Desde 2025 convive una
segunda medición con metodología nueva (7.381) que no forma parte de
esta serie. Por tratarse de un registro administrativo, el crecimiento
describe la expansión de la capacidad de detección y atención tanto como
la evolución del fenómeno.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 2. Distribución por sexo de las situaciones, 2013-2025

**¿Qué pregunta responde?** ¿Las situaciones atendidas afectan por igual
a niñas y varones?
"""),
    code("""
anios_f, fem = serie_sipiav("distribucion_sexo", "Femenino")
fig, ax = plt.subplots()
ax.plot(anios_f, fem, marker="o", color=COLOR, linewidth=2, label="Niñas y adolescentes mujeres")
ax.plot(anios_f, 100 - fem, marker="o", color=PALETA[2], linewidth=2, label="Varones")
ax.set_ylim(0, 100)
ax.set_xticks(anios_f)
ax.set_title(
    "Distribución por sexo de las situaciones atendidas por el SIPIAV (%)\\n"
    "(composición del registro del sistema — no equivale a prevalencia)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=9)
anotar_extremos(ax, anios_f, fem, COLOR)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2025 (INAU).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos líneas complementarias con eje 0-100:
mantener la escala completa de un porcentaje evita exagerar
fluctuaciones pequeñas (Healy, 2018 — integridad del eje).

**Lectura**: la composición es estable en todo el período: entre 54% y
56% de las situaciones corresponden a niñas y adolescentes mujeres
(55% en 2025). La brecha por sexo es moderada en el total pero — como
muestra la métrica 5 — se concentra de forma extrema en las violencias
sexuales.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 3. Distribución por franja etaria, 2013-2025

**¿Qué pregunta responde?** ¿En qué edades se concentran las situaciones
que el sistema atiende?

**Advertencia de fuente**: los tramos publicados cambian a lo largo de la
serie (cinco tramos hasta 2019; el agregado 0-5 desde 2020; publicación
parcial en varios años). La gráfica muestra solo lo publicado con cifra
exacta — los huecos son de la fuente y no se interpolan.
"""),
    code("""
ed = SIP[SIP["metrica"] == "distribucion_edad"]
piv = ed.pivot_table(index="anio", columns="categoria", values="valor")
orden = [c for c in ["0-3", "4-5", "0-5", "6-12", "13-17", "18 y más"] if c in piv.columns]
anios_todos = np.arange(int(piv.index.min()), int(piv.index.max()) + 1)
fig, ax = plt.subplots()
linea_con_huecos(ax, anios_todos, piv[orden])
ax.set_ylim(0, 60)
ax.set_xticks(anios_todos)
ax.set_title(
    "Distribución por franja etaria de las situaciones atendidas (%)\\n"
    "(composición del registro del sistema; huecos = años sin cifra exacta publicada)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8, ncol=3)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2025 (INAU). Los tramos siguen la publicación de cada año.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Líneas con marcadores y huecos visibles: el
marcador distingue la medición real, y la ausencia de línea entre años
sin dato evita inventar continuidad que la fuente no publicó
(convención de este informe: los cortes no se interpolan).

**Lectura**: las edades escolares concentran el registro: en 2025, 38%
de las situaciones corresponden al tramo 6-12 y 34% al 13-17 (72 de
cada 100 entre ambos). La primera infancia (0-5) representa 23% en 2025,
con un aumento del tramo 0-3 (de 9% en 2024 a 15%) que el propio informe
atribuye a mayor capacidad de detección en esas edades.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 4. Tipos de violencia registrados, 2013-2025

**¿Qué pregunta responde?** ¿Qué formas de violencia registra el sistema
y en qué proporción?

**Advertencia de fuente**: la clasificación tiene dos quiebres — en 2020
aparece «explotación sexual» como categoría separada, y desde 2024 abuso
y explotación se fusionan en «violencias sexuales». Las categorías se
grafican tal como las publica cada año, sin empalmar.
"""),
    code("""
tv = SIP[SIP["metrica"] == "tipo_violencia"]
piv = tv.pivot_table(index="anio", columns="categoria", values="valor")
orden = [c for c in ["maltrato emocional", "negligencia", "abuso sexual",
                     "maltrato físico", "explotación sexual", "violencias sexuales"]
         if c in piv.columns]
anios_todos = np.arange(int(piv.index.min()), int(piv.index.max()) + 1)
fig, ax = plt.subplots()
linea_con_huecos(ax, anios_todos, piv[orden])
for x_q in [2019.5, 2023.5]:
    ax.axvline(x_q, color="#bbbbbb", linewidth=0.8, linestyle=":")
ax.text(2019.55, 52, "2020: explotación\\nsexual separada", fontsize=7, color="#777777")
ax.text(2023.55, 52, "2024: fusión en\\nviolencias sexuales", fontsize=7, color="#777777")
ax.set_ylim(0, 60)
ax.set_xticks(anios_todos)
ax.set_title(
    "Tipos de violencia en las situaciones atendidas (%)\\n"
    "(composición del registro del sistema; las líneas punteadas marcan cambios de clasificación)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8, ncol=2)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2025 (INAU). Categorías según la publicación de cada año.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Líneas por categoría con los cambios de
clasificación marcados en el propio plano: quien mira solo la gráfica ve
dónde la serie deja de ser comparable (regla central aplicada al plano
visual). Huecos sin interpolar, como en la métrica 3.

**Lectura**: el maltrato emocional es la categoría más frecuente en toda
la serie (entre 32% y 50%; 38% en 2025), seguido por la negligencia
(24% en 2025). Las violencias sexuales representan 18% en 2025 — con la
advertencia de que esa categoría fusiona desde 2024 lo que antes se
publicaba como abuso (20-28%) y explotación (2-3%) por separado.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 5. Tipo de violencia por sexo y franja etaria (2025)

**¿Qué pregunta responde?** ¿Las distintas formas de violencia afectan
igual a niñas y varones, y a las distintas edades?

**Advertencia de fuente**: los cruces tipo × sexo y tipo × edad se
publican como tablas en imagen en los informes 2020-2024; se presentan
aquí los valores 2025, publicados en texto y verificados contra la prosa
del informe.
"""),
    code("""
vs = SIP[SIP["metrica"] == "tipo_violencia_sexo"].copy()
vs["sexo"] = vs["categoria"].str.split("|").str[1]
fig, ax = plt.subplots(figsize=(7.5, 3.4))
barras = ax.barh(["Varones", "Niñas y adolescentes\\nmujeres"],
                 [float(vs[vs["sexo"] == "Masculino"]["valor"].iloc[0]),
                  float(vs[vs["sexo"] == "Femenino"]["valor"].iloc[0])],
                 color=[PALETA[2], ACENTO], height=0.5)
ax.bar_label(barras, labels=[pct(v, 0) for v in barras.datavalues], padding=4, fontsize=11)
ax.set_xlim(0, 100)
ax.set_title(
    "Violencias sexuales registradas por el SIPIAV según sexo, 2025 (%)\\n"
    "(composición del registro del sistema — no equivale a prevalencia)"
)
ax.set_xlabel("% de las situaciones de violencias sexuales")
fuente(fig, "Fuente: informe de gestión SIPIAV 2025 (INAU), p. 52.", y=-0.08)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos barras horizontales bastan: la comparación
de longitudes desde base común es la percepción visual más precisa
(Cleveland y McGill, 1984), y agregar categorías sin cifra exacta
publicada violaría la regla de no consignar valores dudosos.

**Lectura**: de cada cuatro situaciones de violencias sexuales, tres
corresponden a niñas y adolescentes mujeres (76% frente a 24%). Es
además el único tipo de violencia con más de la mitad de los registros
concentrados en una sola franja: 51% en el tramo 13-17. Los otros tres
tipos se reparten de forma pareja por sexo (proporciones cercanas al
50%, según el informe) y son modales en el tramo 6-12 (maltrato
emocional 37%, maltrato físico 38%, negligencia 42%). La violencia
sexual registrada tiene un patrón específico: adolescente y de género.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 6. Recurrencia: episodio único o violencia reiterada

**¿Qué pregunta responde?** ¿El sistema detecta la violencia ante el
primer episodio o cuando ya se repitió?
"""),
    code("""
rec = SIP[(SIP["metrica"] == "recurrencia") & (SIP["categoria"] == "recurrente")].sort_values("anio")
comp = rec[rec["anio"] <= 2024]
p25 = rec[rec["anio"] == 2025]
fig, ax = plt.subplots()
anios_todos = np.arange(2013, 2026)
y = comp.set_index("anio")["valor"].reindex(anios_todos)
ax.plot(anios_todos, y, marker="o", color=COLOR, linewidth=2, label="Situaciones recurrentes (serie comparable)")
if len(p25):
    ax.plot(p25["anio"], p25["valor"], marker="D", color=ACENTO, linestyle="none",
            label="2025 (base nueva con 17% sin información — no comparable)")
ax.set_ylim(0, 100)
ax.set_xticks(anios_todos)
ax.set_title(
    "Situaciones recurrentes entre las atendidas por el SIPIAV (%)\\n"
    "(característica de los casos que el sistema detecta — no equivale a prevalencia)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8)
fuente(fig, "Fuente: informes de gestión SIPIAV (INAU). 2020-2021 y 2023-2024: sin cifra exacta publicada.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Línea para la serie comparable y **punto
suelto con marcador distinto** para 2025: el cambio de base de cálculo
(la fuente incorpora 17% de casos «sin información» a la base) hace que
unirlo con una línea inventaría una caída que no se midió
(convención de este informe: los cortes se dibujan como puntos sueltos).

**Lectura**: en toda la serie comparable, entre 73% y 81% de las
situaciones ya eran recurrentes al ser detectadas — el sistema suele
llegar cuando la violencia ya se repitió. El 70% de 2025 no es
comparable por el cambio de base (sobre los casos con dato equivale a
84%).
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 7. Cronicidad: violencia sostenida en el tiempo

**¿Qué pregunta responde?** ¿Qué proporción de las situaciones
detectadas lleva más de seis meses de violencia sostenida?
"""),
    code("""
cro = SIP[(SIP["metrica"] == "cronicidad") & (SIP["categoria"] == "fase crónica")].sort_values("anio")
comp = cro[cro["anio"] <= 2024]
p25 = cro[cro["anio"] == 2025]
fig, ax = plt.subplots()
anios_todos = np.arange(2013, 2026)
y = comp.set_index("anio")["valor"].reindex(anios_todos)
ax.plot(anios_todos, y, marker="o", color=COLOR, linewidth=2, label="Situaciones en fase crónica (serie comparable)")
if len(p25):
    ax.plot(p25["anio"], p25["valor"], marker="D", color=ACENTO, linestyle="none",
            label="2025 (base nueva con 17% sin información — no comparable)")
ax.set_ylim(0, 100)
ax.set_xticks(anios_todos)
ax.set_title(
    "Situaciones en fase crónica entre las atendidas por el SIPIAV (%)\\n"
    "(característica de los casos que el sistema detecta — no equivale a prevalencia)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8)
fuente(fig, "Fuente: informes de gestión SIPIAV (INAU). 2015 y 2020-2024: sin cifra exacta publicada.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Misma convención que la métrica 6: serie
comparable en línea, punto 2025 suelto por cambio de base.

**Lectura**: en la serie comparable, alrededor de 9 de cada 10
situaciones detectadas ya estaban en fase crónica (87-92%). Junto con la
recurrencia, ambas métricas cuentan la misma historia: la detección
suele ser tardía. El 57% de 2025 no es comparable (base con 17% sin
información y 26% en etapa de inicio — si la mejora en detección
temprana que sugiere se confirma cuando la base se estabilice, sería un
cambio sustantivo).
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 8. Vínculo de la persona agresora con el NNA

**¿Qué pregunta responde?** ¿Quién ejerce la violencia que el sistema
registra?
"""),
    code("""
ag = SIP[SIP["metrica"] == "agresor_vinculo"]
piv = ag.pivot_table(index="anio", columns="categoria", values="valor")
orden = [c for c in ["padre", "madre", "pareja de la madre", "otro familiar", "no familiar"] if c in piv.columns]
anios_todos = np.arange(2013, 2025)
fig, ax = plt.subplots()
linea_con_huecos(ax, anios_todos, piv[orden])
ax.set_ylim(0, 50)
ax.set_xticks(anios_todos)
ax.set_title(
    "Vínculo de la persona agresora con el NNA (%)\\n"
    "(situaciones registradas por el sistema; cobertura de categorías según cada informe)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8, ncol=3)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2024 (INAU). Desde 2019 se excluye del análisis "
            "a las personas agresoras de negligencia (decisión de la fuente).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Líneas por categoría con huecos sin
interpolar: la cobertura de categorías se reduce desde 2020 porque los
gráficos de los informes dejan de ser extraíbles (documentado en las
notas de curaduría de la serie).

**Lectura**: la violencia registrada ocurre dentro del entorno del NNA:
alrededor de 9 de cada 10 personas agresoras son familiares directos o
integran el núcleo de convivencia (91-94% en los años con cifra exacta).
El padre (34-44%) y la madre (21-35%) encabezan la distribución en toda
la serie. Desde 2019 la fuente excluye la negligencia de este análisis,
por lo que los valores posteriores no son estrictamente comparables con
2013-2018.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 9. NNA que visualizan la violencia que sufren

**¿Qué pregunta responde?** ¿Qué proporción de los NNA atendidos
reconoce la situación de violencia que atraviesa?
"""),
    code("""
vis = SIP[(SIP["metrica"] == "visualizacion") & (SIP["categoria"] == "visualiza")].sort_values("anio")
anios_todos = np.arange(2016, 2024)
y = vis.set_index("anio")["valor"].reindex(anios_todos)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(anios_todos, y, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 100)
ax.set_xticks(anios_todos)
ax.set_title(
    "NNA que visualizan la situación de violencia que atraviesan (%)\\n"
    "(entre los casos atendidos por el SIPIAV; huecos = años sin cifra exacta)"
)
ax.set_ylabel("% que visualiza")
ax.annotate(pct(float(y.dropna().iloc[0]), 0), (2016, float(y.dropna().iloc[0])),
            textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, color=COLOR)
ax.annotate(pct(float(y.dropna().iloc[-1]), 0), (2023, float(y.dropna().iloc[-1])),
            textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, color=COLOR)
fuente(fig, "Fuente: informes de gestión SIPIAV (INAU). 2020-2022 y 2024: solo fracciones en prosa, sin cifra exacta.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie corta con huecos de la fuente: línea con
marcadores solo donde hay medición publicada con cifra exacta.

**Lectura**: solo alrededor de 4 de cada 10 NNA atendidos visualiza la
violencia que sufre (38-42% en los años con dato; 38% en 2023). La
naturalización de la violencia por sus propias víctimas es uno de los
obstáculos de detección que la fuente documenta de forma consistente.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 10. Inclusión de la familia en la intervención

**¿Qué pregunta responde?** ¿En qué proporción de las intervenciones se
logra incorporar a la familia como parte del abordaje?
"""),
    code("""
inc = SIP[(SIP["metrica"] == "inclusion_familia") & (SIP["categoria"] == "incluye familia")].sort_values("anio")
comp = inc[inc["anio"] <= 2024]
p25 = inc[inc["anio"] == 2025]
fig, ax = plt.subplots()
ax.plot(comp["anio"], comp["valor"], marker="o", color=COLOR, linewidth=2,
        label="Serie comparable (2014-2024)")
if len(p25):
    ax.plot(p25["anio"], p25["valor"], marker="D", color=ACENTO, linestyle="none",
            label="2025 (base nueva con 17% sin información — no comparable)")
ax.set_ylim(0, 100)
ax.set_xticks(np.arange(2014, 2026))
ax.set_title(
    "Intervenciones del SIPIAV que logran incluir a la familia (%)\\n"
    "(práctica del sistema de protección)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8)
anotar_extremos(ax, comp["anio"].to_numpy(), comp["valor"].to_numpy(), COLOR)
fuente(fig, "Fuente: informes de gestión SIPIAV 2014-2025 (INAU).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie comparable en línea y 2025 como punto
suelto: el informe 2025 calcula esta proporción sobre una base que
incluye 17% de casos sin información, incompatible con la serie
histórica.

**Lectura**: la serie comparable muestra un deterioro sostenido y
sustantivo: la familia se incluía en 82% de las intervenciones en 2014 y
en 58% en 2024 — 24 puntos porcentuales menos en una década. Es la serie
con la lectura más preocupante del tema, porque describe la práctica del
propio sistema, no la demanda que recibe. El 45% publicado para 2025 no
es comparable (sobre los casos con dato equivale a 54%).
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 11. Cobertura territorial: Comités de Recepción Local

**¿Qué pregunta responde?** ¿Con cuántos dispositivos territoriales de
recepción de situaciones cuenta el sistema?
"""),
    code("""
anios_c, crl = serie_sipiav("crl_cantidad")
fig, ax = plt.subplots(figsize=(8.5, 4))
ax.plot(anios_c, crl, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 40)
ax.set_xticks(anios_c)
ax.set_title("Comités de Recepción Local (CRL) del SIPIAV en funcionamiento")
ax.set_ylabel("Cantidad de CRL")
anotar_extremos(ax, anios_c, crl, COLOR)
fuente(fig, "Fuente: informes de gestión SIPIAV 2013-2025 (INAU).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual de un conteo institucional: línea
con marcadores, eje desde cero.

**Lectura**: la red pasó de 24 CRL en 2013 a 36 desde 2024 (estable en
2025). La expansión no fue monótona — 33 en 2019, 32 entre 2020 y
2022 — y muestra desaceleración: la cobertura parece acercarse a su
techo territorial (los 36 CRL cubren las principales localidades del
país) — por eso su proyección (P5, al cierre de este tema) se lee como
orden de magnitud, no como cronograma de aperturas.
"""),
    # ------------------------------------------------------------------
    md("""
### Proyección P1. Situaciones que atendería el sistema, 2026-2027 — con validación 2025

**¿Qué pregunta responde?** Si la tendencia observada continúa, ¿cuántas
situaciones atendería el sistema en los próximos años? ¿Y qué pasó
cuando la primera proyección se contrastó con el dato real?

**Término** — **escenario inercial**: proyección de la continuación de
la tendencia observada, bajo el supuesto explícito de que las
condiciones actuales persisten. No predice cuánta violencia habrá: es la
trayectoria del propio sistema si nada cambia.
"""),
    code("""
# La proyección publicada en la versión anterior del informe se calculó con la serie
# 2013-2024. El informe 2025 (9.178) quedó dentro del rango publicado
# 8.500-10.300: la proyección se muestra junto con el dato real que la
# validó, y se extiende con el mismo método (justificación técnica y
# backtest en docs/PREDICTIVO_JUSTIFICACION_TECNICA.md).
anios, valores = serie_sipiav("situaciones_atendidas")
base = anios <= 2024
coef = np.polyfit(anios[base], valores[base], 1)
residuos = valores[base] - np.polyval(coef, anios[base])
s = residuos.std(ddof=2)
anios_fut = np.arange(2025, 2028)
proy = np.polyval(coef, anios_fut)

fig, ax = plt.subplots()
ax.plot(anios[base], valores[base], marker="o", color=COLOR, linewidth=2,
        label="Observado (2013-2024, base de la proyección)")
ax.plot(np.append(anios[base][-1], anios_fut), np.append(valores[base][-1], proy),
        marker="o", linestyle="--", color=ACENTO,
        label="Escenario inercial (si la tendencia continúa)")
ax.fill_between(anios_fut, proy - 2 * s, proy + 2 * s, color=ACENTO, alpha=0.15,
                label="Rango del escenario")
ax.plot([2025], [valores[anios == 2025][0]], marker="*", markersize=16, color=COLOR,
        linestyle="none", label="Dato real 2025 (9.178): dentro del rango proyectado")
ax.set_ylim(0, 13000)
ax.set_xticks(np.arange(2013, 2028, 2))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_title(
    "Situaciones que atendería el SIPIAV si la tendencia continúa\\n"
    "(escenario inercial sobre la respuesta del sistema — no proyecta la violencia futura)"
)
ax.set_ylabel("Situaciones atendidas")
ax.legend(frameon=False, fontsize=8)
ax.annotate("≈" + fmt(round(proy[-1], -2)), (anios_fut[-1], proy[-1]),
            textcoords="offset points", xytext=(0, 11), ha="center", fontsize=9, color=ACENTO)
fuente(fig, "Fuente: elaboración propia sobre informes de gestión SIPIAV (INAU). Supuesto: condiciones actuales sin cambios.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Proyección como continuación punteada con
banda de rango (nunca un número único), y el dato real 2025 superpuesto
con marcador propio: la validación fuera de muestra se muestra, no solo
se declara (regla metodológica de este informe).

**Lectura**: la proyección publicada antes de conocerse el dato 2025
(entre 8.500 y 10.300 situaciones) quedó **validada**: el real fue
9.178. Si la tendencia continúa, el sistema atendería entre 9.200 y
11.100 situaciones en 2026, y entre 10.000 y 11.800 en 2027. Advertencia
para el próximo ciclo: si SIPIAV migra su serie a la nueva metodología,
esta proyección deberá recalcularse sobre la base nueva.
"""),
    # ------------------------------------------------------------------
    md("""
### Proyección P2. Inclusión de la familia proyectada, 2025-2027

**¿Qué pregunta responde?** Si el deterioro observado en la métrica 10
continúa, ¿a qué proporción llegaría la inclusión familiar?
"""),
    code("""
inc = SIP[(SIP["metrica"] == "inclusion_familia") & (SIP["categoria"] == "incluye familia")].sort_values("anio")
comp = inc[inc["anio"] <= 2024]
t = comp["anio"].to_numpy(dtype=float)
y = comp["valor"].to_numpy(dtype=float)

def logit(p):
    p = np.clip(p / 100, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))

def inv_logit(z):
    return 100 / (1 + np.exp(-z))

c = np.polyfit(t, logit(y), 1)
res = logit(y) - np.polyval(c, t)
s = res.std(ddof=2)
t_fut = np.arange(2025, 2028, dtype=float)
z = np.polyval(c, t_fut)
proy, bajo, alto = inv_logit(z), inv_logit(z - 2 * s), inv_logit(z + 2 * s)

fig, ax = plt.subplots()
ax.plot(t, y, marker="o", color=COLOR, linewidth=2, label="Observado (2014-2024)")
ax.plot(np.append(t[-1], t_fut), np.append(y[-1], proy), marker="o", linestyle="--",
        color=ACENTO, label="Escenario inercial")
ax.fill_between(t_fut, bajo, alto, color=ACENTO, alpha=0.15, label="Rango del escenario")
ax.set_ylim(0, 100)
ax.set_xticks(np.arange(2014, 2028, 2))
ax.set_title(
    "Inclusión de la familia en la intervención si la tendencia continúa (%)\\n"
    "(práctica del sistema — escenario inercial con rango)"
)
ax.set_ylabel("% de las situaciones")
ax.legend(frameon=False, fontsize=8)
ax.annotate("≈" + pct(proy[-1], 0), (t_fut[-1], proy[-1]),
            textcoords="offset points", xytext=(0, 11), ha="center", fontsize=9, color=ACENTO)
fuente(fig, "Fuente: elaboración propia sobre informes de gestión SIPIAV (INAU). "
            "Modelo sobre transformación logit (respeta las cotas de una proporción).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Misma convención que P1. El modelo se ajusta
sobre la transformación logit para que la proyección de una proporción
nunca salga del rango 0-100 (Hyndman y Athanasopoulos, FPP3 —
justificación técnica en el repositorio).

**Lectura**: si la tendencia 2014-2024 continúa, hacia 2027 la familia
se incluiría en aproximadamente la mitad de las intervenciones (50%,
rango 42-58) — cuando en 2014 se lograba en más de 8 de cada 10. La
validación con el dato 2025 quedó **no concluyente** por el cambio de
base de la fuente (el 45% publicado no es comparable; sobre los casos
con dato, 54%, dentro del rango proyectado 48-64): el modelo no se
re-estima hasta que la base se estabilice.
"""),
    # ------------------------------------------------------------------
    md("""
### Proyección P5. Cobertura territorial proyectada, 2026-2028

**¿Qué pregunta responde?** Si el ritmo de aperturas de la métrica 11
continúa, ¿cuántos Comités de Recepción Local tendría el sistema en los
próximos años?
"""),
    code("""
P5C = pd.read_csv(RESULTADOS / "proyecciones" / "p5_cobertura_crl.csv")
obs5 = P5C[P5C["tipo"] == "observado"]
proy5 = P5C[P5C["tipo"] == "proyectado"]
rango5 = proy5["rango"].str.split("-", expand=True).astype(float)

fig, ax = plt.subplots()
ax.plot(obs5["anio"], obs5["crl"], marker="o", color=COLOR, linewidth=2,
        label="Observado (2013-2025)")
ax.plot(np.append(obs5["anio"].iloc[-1], proy5["anio"]),
        np.append(obs5["crl"].iloc[-1], proy5["crl"]), marker="o", linestyle="--",
        color=ACENTO, label="Escenario inercial")
ax.fill_between(proy5["anio"], rango5[0], rango5[1], color=ACENTO, alpha=0.15,
                label="Rango del escenario")
ax.set_ylim(0, 45)
ax.set_xticks(np.arange(2013, 2029, 2))
ax.set_title(
    "Comités de Recepción Local si el ritmo de aperturas continúa\\n"
    "(cobertura territorial del sistema — escenario inercial con rango)"
)
ax.set_ylabel("Cantidad de CRL")
ax.legend(frameon=False, fontsize=8)
ax.annotate("≈" + fmt(proy5["crl"].iloc[-1]), (proy5["anio"].iloc[-1], proy5["crl"].iloc[-1]),
            textcoords="offset points", xytext=(0, 11), ha="center", fontsize=9, color=ACENTO)
fuente(fig, "Fuente: elaboración propia sobre informes de gestión SIPIAV (INAU). "
            "Proyección de crecimiento amortiguado (una cobertura territorial no crece indefinidamente).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Misma convención que P1 y P2: serie observada
en línea continua, escenario inercial punteado con su rango sombreado y
eje desde cero (Healy, 2018). La proyección crece de forma amortiguada —
la cobertura de un territorio finito no crece indefinidamente
(justificación técnica en el repositorio).

**Lectura**: de seguir el ritmo de aperturas, el sistema sumaría unos
tres comités hacia 2028 (39, rango 37-41), sobre los 36 actuales. La
serie crece a saltos administrativos (mesetas de dos o tres años entre
tandas de apertura), así que la lectura útil es el orden de magnitud —
la cobertura seguiría expandiéndose lentamente — y no el año exacto de
cada apertura.
"""),
    # ==================================================================
    md("""
## Explotación sexual de NNA (CONAPEES, Fiscalía)

Registros administrativos con una advertencia adicional: la explotación
sexual tiene un **subregistro reconocido por el propio comité** — las
cifras describen la actividad de los servicios que la detectan, con
mayor distancia aún respecto del fenómeno real. El dato cuantitativo
sistematizado vive en el estudio FLACSO 2023 (capítulo 6), que compila
las cifras oficiales de CONAPEES y Fiscalía.

**Vacío documentado**: no hay serie oficial de situaciones 2022 en
adelante — el III Plan Nacional 2023-2028 (descargado y revisado) no la
trae, y las cifras difundidas por prensa (285 y 456) no son conciliables
entre sí sin conocer año y definición exacta.
"""),
    md("""
### Métrica 12. Situaciones de explotación sexual atendidas (CONAPEES), 2018-2021

**¿Qué pregunta responde?** ¿Cuántas situaciones de explotación sexual
hacia NNA atendió por año el sistema especializado?
"""),
    code("""
tot = CONA[(CONA["departamento"] == "Total nacional") &
           (CONA["nota"].str.contains("total situaciones", na=False))].sort_values("anio")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(tot["anio"], tot["valor"], marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 600)
ax.set_xticks(tot["anio"])
ax.set_title(
    "Situaciones de explotación sexual de NNA atendidas por año\\n"
    "(registro administrativo con subregistro reconocido — no equivale a prevalencia)"
)
ax.set_ylabel("Situaciones atendidas")
anotar_extremos(ax, tot["anio"].to_numpy(), tot["valor"].to_numpy(), COLOR)
fuente(fig, "Fuente: CONAPEES, compilado por FLACSO Uruguay (2023), capítulo 6, tabla 2. "
            "Sin serie oficial 2022 en adelante.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie corta de 4 mediciones reales: línea con
marcadores; no se proyecta (menos de 6 puntos, regla del bloque
predictivo).

**Lectura**: entre 240 y 494 situaciones anuales atendidas (2018-2021),
con caída en 2019 y crecimiento posterior. La fuente incluye la apertura
por los 19 departamentos (todos registran casos, todos los años). La
serie termina en 2021: la ausencia de cifras oficiales posteriores es el
vacío de información principal del tema.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 13. Sexo de las víctimas de explotación sexual, 2020-2021

**¿Qué pregunta responde?** ¿A quiénes afecta la explotación sexual que
el sistema detecta?
"""),
    code("""
ts = CONA_SEXO[CONA_SEXO["departamento"] == "Total nacional"].sort_values("anio")
fig, ax = plt.subplots(figsize=(7, 3.6))
barras = ax.bar([str(a) for a in ts["anio"]], ts["pct_mujeres"], color=ACENTO, width=0.45)
ax.bar_label(barras, labels=[pct(v, 0) for v in ts["pct_mujeres"]], padding=3, fontsize=11)
ax.set_ylim(0, 100)
ax.set_title(
    "Víctimas de explotación sexual que son niñas o adolescentes mujeres (%)\\n"
    "(entre las situaciones detectadas por el sistema)"
)
ax.set_ylabel("% niñas y adolescentes mujeres")
fuente(fig, "Fuente: CONAPEES, compilado por FLACSO Uruguay (2023), capítulo 6, tabla 3.", y=-0.06)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos barras con el valor anotado: para dos
mediciones puntuales, la barra comunica el nivel sin sugerir tendencia.

**Lectura**: 86% de las víctimas identificadas son niñas y adolescentes
mujeres en ambos años con dato. El sesgo de género es aún más marcado
que en las violencias sexuales del SIPIAV (76%) — consistente con la
especificidad de género de este tipo de violencia.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 14. Explotación sexual dentro del registro del SIPIAV

**¿Qué pregunta responde?** ¿Qué lugar ocupa la explotación sexual entre
los tipos de violencia que registra el sistema general de protección?
"""),
    code("""
es = SIP[(SIP["metrica"] == "tipo_violencia") & (SIP["categoria"] == "explotación sexual")].sort_values("anio")
fig, ax = plt.subplots(figsize=(7.5, 3.6))
barras = ax.bar([str(a) for a in es["anio"]], es["valor"], color=COLOR, width=0.5)
ax.bar_label(barras, labels=[pct(v, 0) for v in es["valor"]], padding=3, fontsize=10)
ax.set_ylim(0, 5)
ax.set_title(
    "Explotación sexual como % de las situaciones registradas por el SIPIAV\\n"
    "(categoría separada solo entre 2020 y 2023; desde 2024, fusionada en «violencias sexuales»)"
)
ax.set_ylabel("% de las situaciones")
fuente(fig, "Fuente: informes de gestión SIPIAV 2020-2023 (INAU).", y=-0.06)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras para una ventana corta de 4 años: la
categoría existió como tal solo entre 2020 y 2023, y graficarla como
serie continua sugeriría una historia más larga que la real.

**Lectura**: la explotación sexual representó 2-3% de las situaciones
registradas por el SIPIAV mientras existió como categoría separada — en
valores absolutos, 98 casos en 2020 y 140 en 2021 según la compilación
de FLACSO. Desde 2024 quedó fusionada en «violencias sexuales», por lo
que esta ventana de visibilidad estadística se cerró: hoy ninguna fuente
pública permite seguir la explotación sexual como categoría propia.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 15. Actuaciones de Fiscalía por delitos sexuales con víctima NNA, 2018-2021

**¿Qué pregunta responde?** ¿Cuántas actuaciones penales por delitos
sexuales contra NNA inicia el sistema de justicia por año?

**Precisión de alcance**: son delitos sexuales con víctima NNA en
general (no solo explotación) — se rotula así, siguiendo la regla de
misma métrica, misma definición.
"""),
    code("""
tf = FISC[FISC["departamento"] == "Total nacional"].sort_values("anio")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(tf["anio"], tf["valor"], marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 2600)
ax.set_xticks(tf["anio"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_title(
    "Actuaciones de Fiscalía por delitos sexuales con víctima NNA\\n"
    "(actividad del sistema de justicia — no equivale a prevalencia)"
)
ax.set_ylabel("Actuaciones")
anotar_extremos(ax, tf["anio"].to_numpy(), tf["valor"].to_numpy(), COLOR)
fuente(fig, "Fuente: Fiscalía General de la Nación, compilado por FLACSO Uruguay (2023), capítulo 6, tabla 8. "
            "Disponible por departamento.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie corta de conteos: línea con marcadores,
eje desde cero.

**Lectura**: entre 1.673 (2018) y 2.324 (2021) actuaciones anuales — un
orden de magnitud cuatro veces mayor que las situaciones que atiende el
sistema especializado en explotación (métrica 12), lo que dimensiona
cuánta violencia sexual hacia NNA llega al sistema penal. La fuente
permite la apertura departamental y en tasa cada 10.000 NNA, reservada
para el análisis territorial.
"""),
    # ==================================================================
    md("""
## Trabajo infantil (ENSANNA 2024, ENTI 2010, ECH)

Este tema combina la única fuente de **prevalencia** disponible — la
ENSANNA 2024 (encuesta con diseño muestral del INE/MTSS, con apoyo de
OIT y UNICEF) — con su antecedente 2010 y con el cálculo propio sobre la
ECH para trabajo adolescente.

Términos utilizados:

- **Trabajo infantil**: definición estadística alineada con los
  Convenios 138 y 182 de la OIT (universo ENSANNA: 5 a 17 años).
- **TFP / TNRS**: trabajo en actividades económicas (frontera de
  producción) y trabajo no remunerado de servicios del hogar en
  condiciones no permitidas, respectivamente.
"""),
    md("""
### Métrica 16. Tasa y volumen de trabajo infantil, 2024

**¿Qué pregunta responde?** ¿Qué proporción de NNA está en situación de
trabajo infantil y cómo cambia con la edad?
"""),
    code("""
ed = ENS[(ENS["metrica"] == "trabajo_infantil") & (ENS["unidad"] == "porcentaje") &
         (ENS["categoria"].str.startswith("edad="))].copy()
ed["grupo"] = ed["categoria"].str.replace("edad=", "", regex=False)
total = float(ENS[(ENS["metrica"] == "trabajo_infantil") & (ENS["categoria"] == "total") &
                  (ENS["unidad"] == "porcentaje")]["valor"].iloc[0])
fig, ax = plt.subplots(figsize=(8, 4))
barras = ax.bar(ed["grupo"], ed["valor"], color=COLOR, width=0.55)
ax.axhline(total, color=ACENTO, linewidth=1.2, linestyle="--")
ax.annotate(f"Total 5-17: {pct(total)}", (0.02, total + 0.25), fontsize=9, color=ACENTO)
ax.bar_label(barras, labels=[pct(v) for v in ed["valor"]], padding=3, fontsize=10)
ax.set_ylim(0, 12)
ax.set_title("Trabajo infantil en Uruguay por grupo de edad, 2024 (% de NNA de cada grupo)")
ax.set_ylabel("% en situación de trabajo infantil")
ax.set_xlabel("Grupo de edad (años)")
fuente(fig, "Fuente: ENSANNA 2024, Cuadros 1 y 3 (INE/MTSS, con apoyo de OIT y UNICEF). Estimaciones ponderadas.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras verticales para pocas categorías
ordinales en su orden natural, eje desde cero y línea de referencia del
total (Cleveland y McGill, 1984; Few; Tufte).

**Lectura**: 6,8% de los NNA de 5 a 17 años — 40.200 — está en situación
de trabajo infantil, con tasa creciente con la edad (10,6% entre 15 y
17). El gradiente se repite en las demás aperturas del boletín: interior
7,7% frente a Montevideo 5,2%, y nivel socioeconómico bajo 7,9% frente a
alto 4,8%. A diferencia de la violencia y la explotación sexual
(registros administrativos), estas cifras sí son prevalencia: describen
a la población.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 17. Componentes del trabajo infantil por sexo, 2024

**¿Qué pregunta responde?** ¿El trabajo infantil de niñas y varones es
del mismo tipo?
"""),
    code("""
def valor_ens(metrica, categoria):
    f = ENS[(ENS["metrica"] == metrica) & (ENS["categoria"] == categoria) &
            (ENS["unidad"] == "porcentaje")]
    return float(f["valor"].iloc[0])

grupos = ["Varones", "Mujeres"]
tfp = [valor_ens("trabajo_frontera_produccion", "sexo=Varon"),
       valor_ens("trabajo_frontera_produccion", "sexo=Mujer")]
tnrs = [valor_ens("trabajo_no_remunerado_servicios", "sexo=Varon"),
        valor_ens("trabajo_no_remunerado_servicios", "sexo=Mujer")]
x = np.arange(2)
ancho = 0.35
fig, ax = plt.subplots(figsize=(8, 4))
b1 = ax.bar(x - ancho / 2, tfp, ancho, color=COLOR, label="Actividades económicas (TFP)")
b2 = ax.bar(x + ancho / 2, tnrs, ancho, color=ACENTO, label="Trabajo no remunerado de servicios (TNRS)")
for b in (b1, b2):
    ax.bar_label(b, labels=[pct(v) for v in b.datavalues], padding=3, fontsize=10)
ax.set_xticks(x, grupos)
ax.set_ylim(0, 8)
ax.set_title("Componentes del trabajo infantil por sexo, 2024 (% de NNA de 5 a 17)")
ax.set_ylabel("% de NNA")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuente: ENSANNA 2024, Cuadro 2 (INE/MTSS). Estimaciones ponderadas.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras agrupadas para comparar el mismo dato
entre grupos, lado a lado (Few) — las dos componentes no se apilan
porque cada una tiene su propia definición y no suman una tasa
conjunta interpretable por adición simple.

**Lectura**: el trabajo infantil tiene sexo según su tipo. En
actividades económicas los varones superan a las mujeres (5,5% frente a
4,2%); en el trabajo no remunerado de servicios del hogar la relación se
invierte y más que duplica: 2,8% de las niñas frente a 1,1% de los
varones. La división sexual del trabajo empieza en la infancia.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 18. Comparación puntual 2010 ↔ 2024

**¿Qué pregunta responde?** ¿Qué se puede decir — y qué no — al comparar
la medición 2024 con su antecedente de 2010?

**Advertencia de fuente**: la ENTI 2010 publicó dos definiciones (9,9%
restringida; 13,4% amplia) y su propio informe advierte problemas de
comparabilidad. No hay serie: hay dos mediciones con metodologías
distintas.
"""),
    code("""
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([2010, 2010], [9.9, 13.4], marker="o", linestyle="none", color=PALETA[3],
        label="ENTI 2010 (dos definiciones publicadas)")
ax.plot([2024], [6.8], marker="o", linestyle="none", color=COLOR, markersize=9,
        label="ENSANNA 2024")
for x_p, y_p, et in [(2010, 9.9, "9,9% (FPSCN)"), (2010, 13.4, "13,4% (FGP)"), (2024, 6.8, "6,8%")]:
    ax.annotate(et, (x_p, y_p), textcoords="offset points", xytext=(10, 0), fontsize=9)
ax.set_xlim(2008, 2027)
ax.set_ylim(0, 16)
ax.set_xticks([2010, 2024])
ax.set_title(
    "Trabajo infantil: mediciones puntuales 2010 y 2024 (% de NNA de 5 a 17)\\n"
    "(sin línea entre puntos: las metodologías no son comparables)"
)
ax.set_ylabel("% en situación de trabajo infantil")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuentes: ENTI 2010 (INE) y ENSANNA 2024 (INE/MTSS). La definición elegida en 2010 cambia la conclusión.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Puntos sueltos sin línea que los una — la
convención de este informe para mediciones sin comparabilidad
verificada: una línea inventaría una tendencia que no se midió.

**Lectura**: la lectura honesta es un rango: el trabajo infantil habría
descendido desde entre 9,9% y 13,4% (2010, según la definición) hasta
6,8% (2024). La dirección de la mejora es consistente con cualquiera de
las dos definiciones; su magnitud exacta no es medible con las fuentes
disponibles.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 19. Trabajo adolescente (14-17) — cálculo propio sobre la ECH

**¿Qué pregunta responde?** ¿Qué proporción de adolescentes de 14 a 17
años está ocupada, y en qué condiciones?

**Precisión de alcance**: el módulo de empleo de la ECH comienza a los
14 años — esta métrica cubre trabajo adolescente, no el trabajo
infantil de 5-13 (que solo mide la ENSANNA).
"""),
    code("""
ta = ECHM[ECHM["metrica"] == "trabajo_adolescente_14a17"]
tot = ta[ta["categoria"] == "ocupacion=total"].sort_values("anio")
var = ta[ta["categoria"] == "ocupacion=sexo:Varones"].sort_values("anio")
muj = ta[ta["categoria"] == "ocupacion=sexo:Mujeres"].sort_values("anio")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(tot["anio"], tot["valor"], marker="o", color=COLOR, linewidth=2, label="Total 14-17")
ax.plot(var["anio"], var["valor"], marker="o", color=PALETA[2], linewidth=1.6, label="Varones")
ax.plot(muj["anio"], muj["valor"], marker="o", color=ACENTO, linewidth=1.6, label="Mujeres")
ax.set_ylim(0, 6)
ax.set_xticks(tot["anio"])
ax.set_title("Ocupación de adolescentes de 14 a 17 años (% ponderado, ECH)")
ax.set_ylabel("% ocupados")
ax.legend(frameon=False, fontsize=9)
anotar_extremos(ax, tot["anio"].to_numpy(), tot["valor"].to_numpy(), COLOR, dec=1)
fuente(fig, "Fuente: elaboración propia sobre microdatos de la ECH (INE), panel mensual de empleo 14-17, "
            "ponderador mensual. El módulo de empleo no releva menores de 14 años.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Tres líneas (total y por sexo) sobre una serie
corta de cálculo propio ponderado; eje desde cero.

**Lectura**: alrededor del 3% de los adolescentes de 14 a 17 está
ocupado (3,0% en 2025), con los varones duplicando o cuadruplicando a
las mujeres según el año. El dato más relevante está en la condición: la
informalidad entre los adolescentes ocupados es masiva (82-93% según el
año, frente a ~20% en el conjunto de los ocupados del país) — el trabajo
adolescente que existe ocurre casi todo fuera de la protección de la
seguridad social.
"""),
]
