"""Celdas del informe — temas 4 y 5, contexto demográfico y cierre."""

from __future__ import annotations

from politicas_sociales.informe_base import code, md

CELDAS = [
    # ==================================================================
    md("""
## Tema 4 — Protección especial (INAU)

Indicadores del Sistema de Protección Especial (SPE) del INAU, con
fuente en el SIPI (Sistema de Información Para la Infancia). Describen a
la **población atendida por el INAU** — los NNA que están en el sistema
de protección — no a la infancia uruguaya en general. Serie anual
2020-2025 a nivel nacional; los mismos indicadores existen por
departamento con frecuencia semestral.

Términos utilizados por la fuente:

- **Cuidado residencial / contexto familiar**: las dos grandes
  modalidades de cuidado; reducir la primera en favor de la segunda
  («desinternación») es el eje declarado de la política.
- **SPE**: incluye también a jóvenes de 18 años y más que permanecen en
  proyectos del sistema; cuando una métrica se restringe a 0-17, se
  indica.
"""),
    md("""
### Métrica 20. NNA atendidos en el Sistema de Protección Especial

**¿Qué pregunta responde?** ¿Cuántas personas atiende el sistema de
protección especial y qué proporción de la población del país
representa?
"""),
    code("""
anios_i, atendidos = serie_inau("1.1")
fig, ax = plt.subplots()
ax.plot(anios_i, atendidos, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 9000)
ax.set_xticks(anios_i)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_title(
    "NNA y jóvenes atendidos en el Sistema de Protección Especial (INAU)\\n"
    "(población atendida por el sistema — no describe a la infancia general)"
)
ax.set_ylabel("Personas atendidas")
anotar_extremos(ax, anios_i, atendidos, COLOR)
fuente(fig, "Fuente: INAU, Indicadores del Sistema de Protección Especial (SIPI), indicador 1.1.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual de conteos: línea con marcadores,
eje desde cero, extremos anotados.

**Lectura**: el sistema pasó de 6.516 personas atendidas en 2020 a 7.988
en 2025, con el máximo en 2023 (8.017) y estabilización posterior.
Restringido a 0-17 años (sumando los tramos de edad del indicador), la
población atendida pasó de 5.583 a 7.043 y también se amesetó desde
2023. Como proporción de la población total del país, el sistema
atiende cerca del 1% (0,77% en 2020 → 0,97% en 2025, indicador 1.3).
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 21. Cuidado residencial frente a contexto familiar

**¿Qué pregunta responde?** ¿Avanza la desinternación — que los NNA del
sistema vivan en contexto familiar y no en residencias?
"""),
    code("""
anios_r, resid = serie_inau("2.1")
_, familia = serie_inau("2.2")
pct_familia = familia / (resid + familia) * 100
fig, ax = plt.subplots()
ax.plot(anios_r, pct_familia, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 100)
ax.set_xticks(anios_r)
ax.set_title(
    "NNA del Sistema de Protección Especial que viven en contexto familiar (%)\\n"
    "(el eje de la política de desinternación; población atendida por el sistema)"
)
ax.set_ylabel("% en contexto familiar")
anotar_extremos(ax, anios_r, pct_familia, COLOR, dec=1)
fuente(fig, "Fuente: elaboración propia sobre INAU (SIPI), indicadores 2.1 (residencia) y 2.2 (contexto familiar).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** La proporción en contexto familiar resume en
una sola serie la relación entre las dos modalidades; eje 0-100 completo
para no exagerar el avance (Healy, 2018).

**Lectura**: la desinternación avanza de forma sostenida: 50,9% de los
NNA del sistema vivía en contexto familiar en 2020 y 62,7% en 2025. En
términos del ratio que publica la fuente, se pasó de prácticamente un
NNA en residencia por cada uno en familia (0,97) a 0,6. El avance es
consistente pero se desacelera en los últimos semestres — la proyección
P3 estima su trayectoria.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 22. Ingresos al sistema: primera vez y reingresos

**¿Qué pregunta responde?** ¿Cuánto de la demanda del sistema es nueva y
cuánta es reincidencia de trayectorias anteriores?
"""),
    code("""
anios_p, primera = serie_inau("3.2")
_, reingreso = serie_inau("4.2")
fig, ax = plt.subplots()
ax.plot(anios_p, primera, marker="o", color=COLOR, linewidth=2, label="Ingresan por primera vez")
ax.plot(anios_p, reingreso, marker="o", color=ACENTO, linewidth=2, label="Ingresan con trayectoria anterior")
ax.set_ylim(0, 35)
ax.set_xticks(anios_p)
ax.set_title(
    "Ingresos al Sistema de Protección Especial como % de los atendidos\\n"
    "(población atendida por el sistema)"
)
ax.set_ylabel("% del total de atendidos")
ax.legend(frameon=False, fontsize=9)
anotar_extremos(ax, anios_p, primera, COLOR, dec=1)
anotar_extremos(ax, anios_p, reingreso, ACENTO, dec=1)
fuente(fig, "Fuente: INAU (SIPI), indicadores 3.2 y 4.2.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos líneas en el mismo plano porque comparten
unidad y denominador (% del total de atendidos); no se apilan porque no
agotan el universo.

**Lectura**: cada año, entre 21% y 26% de los atendidos son ingresos por
primera vez, mientras que los reingresos con trayectoria anterior se
mantienen en torno al 5%. La demanda nueva domina sobre la reincidencia
— la puerta de entrada del sistema sigue muy activa, coherente con el
crecimiento de la métrica 20 hasta 2023.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 23. Egresos del sistema

**¿Qué pregunta responde?** ¿A qué ritmo egresan los NNA del sistema de
protección?
"""),
    code("""
anios_e, egresos = serie_inau("5.4")
fig, ax = plt.subplots()
ax.plot(anios_e, egresos, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 35)
ax.set_xticks(anios_e)
ax.set_title(
    "Egresos del Sistema de Protección Especial como % de los atendidos\\n"
    "(población atendida por el sistema)"
)
ax.set_ylabel("% que egresa en el año")
anotar_extremos(ax, anios_e, egresos, COLOR, dec=1)
fuente(fig, "Fuente: INAU (SIPI), indicador 5.4. Los egresos del segundo semestre de 2020 son estimados "
            "(nota del propio archivo de la fuente).")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual simple: línea con marcadores, eje
desde cero.

**Lectura**: el sistema egresa cada año a alrededor de un cuarto de su
población atendida (23-26%). Combinado con la métrica 22 (más ingresos
que egresos hasta 2023), el saldo explica el crecimiento del stock. Los
tiempos de permanencia — publicados desde 2021 — completan esta lectura
en la fuente.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 24. Tránsito de residencia a familia

**¿Qué pregunta responde?** ¿Cuántos NNA dejan el cuidado residencial
para pasar a vivir con una familia?
"""),
    code("""
anios_t, transito = serie_inau("6.2")
fig, ax = plt.subplots()
ax.plot(anios_t, transito, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 40)
ax.set_xticks(anios_t)
ax.set_title(
    "NNA que pasan de residencia a vivir con una familia, como % de los atendidos\\n"
    "(población atendida por el sistema)"
)
ax.set_ylabel("% del total de atendidos")
anotar_extremos(ax, anios_t, transito, COLOR, dec=1)
fuente(fig, "Fuente: INAU (SIPI), indicador 6.2.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual simple, misma convención que las
anteriores del tema.

**Lectura**: entre 25% y 32% de los atendidos pasa cada año de
residencia a un entorno familiar (28,2% en 2025, con máximo de 31,7% en
2022). Es el flujo que sostiene el avance de la desinternación que
muestra la métrica 21.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 25. Adopciones: condición de adoptabilidad y tenencia

**¿Qué pregunta responde?** ¿Cuántos NNA del sistema tienen condición de
adoptabilidad declarada, y cuántos avanzan a tenencia?
"""),
    code("""
anios_a, adoptables = serie_inau("7.1")
fig, ax = plt.subplots()
ax.plot(anios_a, adoptables, marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 900)
ax.set_xticks(anios_a)
ax.set_title(
    "NNA con condición de adoptabilidad declarada\\n"
    "(población atendida por el sistema)"
)
ax.set_ylabel("Cantidad de NNA")
anotar_extremos(ax, anios_a, adoptables, COLOR)
fuente(fig, "Fuente: INAU (SIPI), indicadores 7.1 y 8.2.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie anual de un conteo; el segundo indicador
del proceso (paso a tenencia) se reporta en la lectura para no
superponer unidades distintas (cantidad y porcentaje) en un mismo eje.

**Lectura**: los NNA con condición de adoptabilidad pasaron de 560
(2020) a 732 (2025), alrededor del 7-8% de los atendidos. De ellos, solo
entre 15% y 18% pasa cada año a seguimiento de tenencia (15,4% en
2025): la distancia entre adoptabilidad declarada y adopción efectiva es
el cuello de botella que la fuente permite dimensionar.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 26. Frecuencia de contacto con la familia o referentes

**¿Qué pregunta responde?** ¿Con qué frecuencia los NNA atendidos
mantienen contacto con sus familias o referentes afectivos?
"""),
    code("""
n91 = INAU[(INAU["indicador_codigo"] == "9.1") & (INAU["anio"] == 2025) &
           (INAU["apertura"].str.match(r"^frecuencia="))].copy()
n91["cat"] = n91["apertura"].str.replace("frecuencia=", "", regex=False)
orden = ["Constante", "Esporádica", "Nula", "Sin datos"]
n91 = n91.set_index("cat").loc[orden]
colores = [COLOR, PALETA[3], ACENTO, "#aaaaaa"]
fig, ax = plt.subplots(figsize=(8, 3.8))
barras = ax.barh(orden[::-1], n91["valor"].to_numpy()[::-1], color=colores[::-1], height=0.55)
ax.bar_label(barras, labels=[pct(v) for v in barras.datavalues], padding=4, fontsize=10)
ax.set_xlim(0, 70)
ax.set_title(
    "Frecuencia del contacto con la familia o referentes, 2025 (%)\\n"
    "(población atendida por el sistema; «Sin datos» = casos sin registro de la variable)"
)
ax.set_xlabel("% de los NNA atendidos")
fuente(fig, "Fuente: INAU (SIPI), indicador 9.1, año 2025.", y=-0.07)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras horizontales para categorías con
nombre, **incluida la categoría de datos faltantes**: ocultar el «sin
datos» haría parecer que el 27,5% con contacto constante es mayoría,
cuando la mayoría real es la falta de registro.

**Lectura**: entre quienes tienen la variable registrada, el contacto
constante domina (27,5% del total) sobre el esporádico (6,9%) y el nulo
(8,7%). Pero el dato principal es otro: **56,9% de los casos no tiene
registro de esta variable** — la calidad del registro es hoy el límite
de lo que esta métrica puede decir, y así se reporta.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 27. Educación de los NNA del sistema

**¿Qué pregunta responde?** ¿Los NNA atendidos por el sistema asisten a
la educación?
"""),
    code("""
anios_11, ed05 = serie_inau("11.1")
anios_12, ed617 = serie_inau("11.2")
fig, ax = plt.subplots()
ax.plot(anios_11, ed05, marker="o", color=COLOR, linewidth=2,
        label="0-5 años en centros de educación y cuidado")
ax.plot(anios_12, ed617, marker="o", color=ACENTO, linewidth=2,
        label="6-17 años en educación formal")
ax.set_ylim(0, 100)
ax.set_xticks(anios_12)
ax.set_title(
    "Inscripción educativa de los NNA del Sistema de Protección Especial (%)\\n"
    "(población atendida por el sistema; sin dato de 2020 para 0-5)"
)
ax.set_ylabel("% inscriptos")
ax.legend(frameon=False, fontsize=9)
anotar_extremos(ax, anios_11, ed05, COLOR, dec=1)
anotar_extremos(ax, anios_12, ed617, ACENTO, dec=1)
fuente(fig, "Fuente: INAU (SIPI), indicadores 11.1 y 11.2. El indicador de educación no formal (13-17) "
            "no publica total nacional en el archivo de la fuente.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos líneas con la misma unidad y universos
declarados por tramo; eje 0-100.

**Lectura**: la inscripción en educación formal de los 6-17 es alta y
creciente (89,3% en 2021 → 91,5% en 2025); la de 0-5 en centros de
educación y cuidado ronda el 78-82%. La contracara: aun dentro del
sistema de protección, cerca de 1 de cada 10 NNA de 6 a 17 no está
inscripto en educación formal.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 28. Salud: controles y vacunas al día

**¿Qué pregunta responde?** ¿Los NNA atendidos tienen su atención básica
de salud al día?
"""),
    code("""
anios_s, controles = serie_inau("12.1")
_, vacunas = serie_inau("13.1")
fig, ax = plt.subplots()
ax.plot(anios_s, controles, marker="o", color=COLOR, linewidth=2, label="Controles médicos al día")
ax.plot(anios_s, vacunas, marker="o", color=ACENTO, linewidth=2, label="Vacunas al día")
ax.set_ylim(0, 100)
ax.set_xticks(anios_s)
ax.set_title(
    "Salud de los NNA del Sistema de Protección Especial (%)\\n"
    "(población atendida por el sistema)"
)
ax.set_ylabel("% al día")
ax.legend(frameon=False, fontsize=9)
anotar_extremos(ax, anios_s, controles, COLOR, dec=1)
anotar_extremos(ax, anios_s, vacunas, ACENTO, dec=1)
fuente(fig, "Fuente: INAU (SIPI), indicadores 12.1 y 13.1.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos líneas de la misma unidad; eje 0-100
completo para que la distancia al 100% — que es el dato — sea visible.

**Lectura**: ambos indicadores mejoran (controles: 49,2% en 2020 → 61,8%
en 2025; vacunas: 74,6% → 78,0%), pero el nivel sigue siendo el
hallazgo: en una población bajo cuidado del Estado, casi 4 de cada 10
NNA no tienen los controles médicos al día y más de 2 de cada 10 no
tienen las vacunas al día.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 29. Acogimiento familiar por tipo de familia (abril 2025)

**¿Qué pregunta responde?** ¿En qué tipo de familias se acogen los NNA
que no viven con su familia de origen?
"""),
    code("""
raf = RAF[(RAF["cuadro"] == "Cuadro 1") & (RAF["departamento"] == "Total país") &
          (RAF["columna"] == "Total general") &
          (RAF["fila"].isin(["Familia Amiga y Alternativa Familiar", "Familia Extensa", "Familia Afinidad"]))]
raf = raf.sort_values("valor")
fig, ax = plt.subplots(figsize=(8, 3.6))
barras = ax.barh(raf["fila"], raf["valor"], color=COLOR, height=0.55)
ax.bar_label(barras, labels=[fmt(v) for v in barras.datavalues], padding=4, fontsize=10)
ax.set_title(
    "NNA en acogimiento familiar por tipo de familia — corte a abril de 2025\\n"
    "(población atendida por el sistema)"
)
ax.set_xlabel("Cantidad de NNA")
fuente(fig, "Fuente: INAU, Reporte de Acogimiento Familiar, abril de 2025 (edición Excel), Cuadro 1.", y=-0.07)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras horizontales ordenadas por magnitud
para categorías con nombres largos (Cleveland y McGill, 1984; orden por
total, Ware).

**Lectura**: el acogimiento se apoya sobre todo en la red del propio
NNA: la familia extensa y la familia por afinidad concentran la mayor
parte de los acogimientos, mientras el programa de familias amigas y
alternativas familiares — captación de familias sin vínculo previo —
aporta el grupo menor. La fuente permite además la apertura por etapa de
desarrollo, sexo y departamento.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 30. Dónde viven los NNA acompañados por el sistema (abril 2025)

**¿Qué pregunta responde?** Considerando a todos los NNA vinculados a
dispositivos de protección, ¿dónde están viviendo?
"""),
    code("""
dvf = DVF[(DVF["cuadro"] == "Cuadro 1") & (DVF["departamento"] == "Total país") &
          (DVF["fila"] == "Total") & (DVF["columna"] != "total")].copy()
dvf["lugar"] = (dvf["columna"].str.replace(r"\\d+$", "", regex=True).str.strip())
dvf = dvf.sort_values("valor")
total_dvf = dvf["valor"].sum()
fig, ax = plt.subplots(figsize=(8.5, 4))
barras = ax.barh(dvf["lugar"], dvf["valor"], color=COLOR, height=0.6)
ax.bar_label(barras, labels=[fmt(v) for v in barras.datavalues], padding=4, fontsize=10)
ax.set_title(
    f"Dónde viven los {fmt(total_dvf)} NNA vinculados a dispositivos de protección — abril de 2025\\n"
    "(población atendida por el sistema)"
)
ax.set_xlabel("Cantidad de NNA")
fuente(fig, "Fuente: INAU, Reporte Derecho a Vivir en Familia, abril de 2025 (edición Excel), Cuadro 1.", y=-0.06)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras horizontales ordenadas por magnitud —
misma convención que la métrica 29, con el total en el título para dar
el denominador de una sola vez.

**Lectura**: la fotografía de abril de 2025 muestra la composición
residencial completa de los NNA acompañados: el cuidado residencial
sigue siendo el destino de una parte sustantiva, pero la mayoría vive en
entornos familiares (familia de origen, contexto familiar propio,
acogimientos y familias adoptivas). Es el corte transversal que
complementa la serie de la métrica 21.
"""),
    # ------------------------------------------------------------------
    md("""
### Proyección P3. Desinternación proyectada por departamento, 2026-2027

**¿Qué pregunta responde?** Si el ritmo de desinternación persiste, ¿qué
proporción de los NNA del sistema vivirá en contexto familiar hacia
fines de 2027, y en qué departamentos?
"""),
    code("""
p3 = P3[P3["modelo"] != "no_proyectable"].sort_values("proy_2027-S2")
fig, ax = plt.subplots(figsize=(8.5, 5))
y_pos = np.arange(len(p3))
ax.barh(y_pos + 0.2, p3["ultimo_observado_2025S2"], height=0.38, color=COLOR,
        label="Observado (2025, segundo semestre)")
ax.barh(y_pos - 0.2, p3["proy_2027-S2"], height=0.38, color=ACENTO,
        label="Escenario inercial (2027, segundo semestre)")
ax.set_yticks(y_pos, p3["unidad_territorial"])
for i, (obs, proy) in enumerate(zip(p3["ultimo_observado_2025S2"], p3["proy_2027-S2"])):
    ax.annotate(pct(obs), (obs + 0.5, i + 0.2), fontsize=8, va="center", color=COLOR)
    ax.annotate(pct(proy), (proy + 0.5, i - 0.2), fontsize=8, va="center", color=ACENTO)
ax.set_xlim(0, 100)
ax.set_title(
    "NNA del sistema en contexto familiar: observado y escenario inercial (%)\\n"
    "(solo las 9 de 20 unidades donde la proyección superó los criterios de validación)"
)
ax.set_xlabel("% en contexto familiar")
ax.legend(frameon=False, fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=2)
fuente(fig, "Fuente: elaboración propia sobre INAU (SIPI), indicadores departamentales 5 y 6, series semestrales "
            "2020-2025. Rangos y unidades no proyectables: resultados/proyecciones/p3_desinternacion.csv.", y=-0.10)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras agrupadas observado/proyectado por
unidad territorial, mostrando **solo** las unidades cuyo modelo superó
el backtest — las 11 restantes no se fuerzan: las estables se reportan
como «se mantiene» y las erráticas como no proyectables (protocolo del
bloque predictivo).

**Lectura**: si el ritmo actual persiste, el total del país pasaría de
62,7% a 66,4% de los NNA del sistema en contexto familiar hacia fines de
2027 (rango 63,9-68,8). Canelones es el caso más firme (70,1% → 74,8%).
Montevideo — no graficado — es un caso distinto: su serie es tan estable
en torno a 53% que el escenario inercial es «se mantiene», sin
necesidad de modelo.
"""),
    # ------------------------------------------------------------------
    md("""
### Proyección P4. NNA en protección especial cada 1.000 NNA

**¿Qué pregunta responde?** ¿Qué proporción de la infancia uruguaya está
en el sistema de protección especial, y hacia dónde va esa tasa?

**Término** — **tasa cada 1.000 NNA**: NNA de 0 a 17 en el SPE dividido
por la población de 0 a 17 del país (proyecciones oficiales del INE,
revisión 2025), por mil.
"""),
    code("""
obs = P4[P4["tipo"] == "observado"]
ref = P4[P4["tipo"] != "observado"]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(obs["anio"], obs["tasa_por_mil"], marker="o", color=COLOR, linewidth=2,
        label="Tasa observada")
ax.plot(np.append(obs["anio"].iloc[-1], ref["anio"]),
        np.append(obs["tasa_por_mil"].iloc[-1], ref["tasa_por_mil"]),
        marker="s", linestyle=":", color="#888888",
        label="Referencia si el numerador se mantiene (~7.000 NNA)")
for _, fila in pd.concat([obs, ref]).iterrows():
    ax.annotate(f"{fila['tasa_por_mil']:.2f}".replace(".", ","), (fila["anio"], fila["tasa_por_mil"]),
                textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9,
                color=COLOR if fila["tipo"] == "observado" else "#888888")
ax.set_ylim(0, 12)
ax.set_xticks(P4["anio"])
ax.set_title(
    "NNA de 0 a 17 años en el Sistema de Protección Especial cada 1.000 NNA\\n"
    "(tasa sobre la población infantil del país; referencia sin modelo — ver texto)"
)
ax.set_ylabel("Por cada 1.000 NNA")
ax.legend(frameon=False, fontsize=8)
fuente(fig, "Fuente: elaboración propia sobre INAU (SIPI, indicador 1.1 por tramos de edad) e INE "
            "(proyecciones de población, revisión 2025). La revisión 2025 publica denominadores desde 2024.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** La referencia 2026-2027 se dibuja punteada,
gris y sin banda: **no es una proyección de modelo**. El protocolo del
bloque predictivo exigía que algún modelo del numerador superara al
ingenuo en el backtest, y ninguno lo hizo (el numerador se amesetó en
torno a 7.000 desde 2023) — en ese caso no se publica proyección y el
escenario inercial se degrada a lectura descriptiva.

**Lectura**: 9,05 de cada 1.000 NNA del país estaban en el sistema de
protección especial en 2024, y 9,38 en 2025. El hallazgo está en la
descomposición: la tasa sube **aunque la cantidad de NNA atendidos ya no
crece**, porque la población infantil del país cae 2,3% por año. Si el
sistema simplemente mantiene su tamaño actual, la tasa llegará a ~9,8
por mil en 2027 solo por efecto demográfico — una advertencia general
para todas las tasas de infancia del país.
"""),
    # ==================================================================
    md("""
## Tema 5 — Pobreza, vivienda y entorno del hogar (ECH)

Cálculo propio sobre los **microdatos de la ECH** (INE), universo 0-17
años, siempre ponderado (2019, 2023, 2024 y 2025; la extracción
reutiliza los procedimientos verificados del proyecto
[agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)).
A diferencia de los temas 1, 2 y 4, estas métricas sí describen a la
infancia uruguaya en general.
"""),
    md("""
### Métrica 31. Pobreza monetaria en la infancia

**¿Qué pregunta responde?** ¿Qué proporción de NNA vive en hogares en
situación de pobreza?

**Advertencia de fuente**: la serie tiene un corte metodológico — 2019 y
2023 se calculan con la canasta 2006 del INE y 2024-2025 con la canasta
2017 (verificado contra los archivos: cada año trae solo su variable).
Los dos regímenes no se unen.
"""),
    code("""
pob = ECHM[(ECHM["metrica"] == "pobreza_0a17") & (ECHM["categoria"] == "total")].sort_values("anio")
r1 = pob[pob["anio"] <= 2023]
r2 = pob[pob["anio"] >= 2024]
fig, ax = plt.subplots()
ax.plot(r1["anio"], r1["valor"], marker="o", color=PALETA[3], linewidth=2,
        label="Canasta 2006 (metodología anterior)")
ax.plot(r2["anio"], r2["valor"], marker="o", color=COLOR, linewidth=2,
        label="Canasta 2017 (metodología vigente)")
for df_r, c in [(r1, PALETA[3]), (r2, COLOR)]:
    anotar_extremos(ax, df_r["anio"].to_numpy(), df_r["valor"].to_numpy(), c, dec=1)
ax.set_ylim(0, 40)
ax.set_xticks(pob["anio"])
ax.set_title(
    "Pobreza monetaria en NNA de 0 a 17 años (% ponderado)\\n"
    "(las dos metodologías del INE no se unen: el salto 2023-2024 es del cambio de canasta)"
)
ax.set_ylabel("% de NNA en hogares pobres")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuente: elaboración propia sobre microdatos de la ECH (INE), universo 0-17, ponderador anual. "
            "Clasificación de pobreza oficial del INE de cada año.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos segmentos con colores distintos y sin
línea entre 2023 y 2024: unir los regímenes inventaría un salto de 10
puntos que es metodológico, no social (convención de cortes de serie).

**Lectura**: con la metodología vigente, 28,9% de los NNA vivía en
hogares pobres en 2024 y 27,5% en 2025. El patrón por edad es regresivo
con la primera infancia (32,2% entre 0 y 5 años frente a 27,5% entre 13
y 17, en 2024) y la comparación con la población general (~17%)
confirma la lectura central del proyecto: la pobreza uruguaya está
concentrada en la infancia.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 32. Hacinamiento en hogares con NNA

**¿Qué pregunta responde?** ¿Qué proporción de los hogares donde viven
NNA está en situación de hacinamiento?
"""),
    code("""
hac = ECHM[(ECHM["metrica"] == "hacinamiento_hogares_nna") & (ECHM["categoria"] == "total")].sort_values("anio")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(hac["anio"], hac["valor"], marker="o", color=COLOR, linewidth=2)
ax.set_ylim(0, 8)
ax.set_xticks(hac["anio"])
ax.set_title("Hogares con NNA en situación de hacinamiento (% ponderado)")
ax.set_ylabel("% de hogares con NNA")
anotar_extremos(ax, hac["anio"].to_numpy(), hac["valor"].to_numpy(), COLOR, dec=1)
fuente(fig, "Fuente: elaboración propia sobre microdatos de la ECH (INE), hogares con al menos un NNA, "
            "ponderador anual (definición operativa en src/metricas_ech.py). Sin microdato 2020-2022 en el proyecto.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Serie de cuatro mediciones reales: línea con
marcadores; los años ausentes son años sin extracción en el proyecto,
no ceros.

**Lectura**: el hacinamiento afecta a entre 3,7% y 4,9% de los hogares
con NNA según el año (3,7% en 2025, el valor más bajo de la serie). Su
apertura por departamento y tramo de edad queda disponible para el
análisis territorial.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 33. Condiciones de la vivienda en hogares con NNA

**¿Qué pregunta responde?** ¿Qué carencias físicas tienen las viviendas
donde crecen los NNA?

**Advertencia de fuente**: la ECH relevó 12 carencias en 2019 y solo 4
desde 2024 (cambio del formulario del INE, heredado y documentado). Se
comparan únicamente las 4 presentes en ambos regímenes.
"""),
    code("""
viv = ECHM[(ECHM["metrica"] == "vivienda_hogares_nna") &
           (ECHM["categoria"].str.startswith("carencia="))].copy()
viv["carencia"] = viv["categoria"].str.replace("carencia=", "", regex=False)
piv = viv.pivot_table(index="carencia", columns="anio", values="valor")
comunes = piv.dropna().sort_values(2025)
etiquetas = {"humedad_cimientos": "Humedades en cimientos", "goteras": "Goteras",
             "se_inunda": "Se inunda", "peligro_derrumbe": "Peligro de derrumbe"}
nombres = [etiquetas.get(c, c) for c in comunes.index]
y_pos = np.arange(len(comunes))
fig, ax = plt.subplots(figsize=(8.5, 4))
for i, (anio, color) in enumerate([(2019, PALETA[3]), (2024, PALETA[2]), (2025, COLOR)]):
    ax.barh(y_pos + 0.25 - i * 0.25, comunes[anio], height=0.23, color=color, label=str(anio))
    for j, v in enumerate(comunes[anio]):
        ax.annotate(pct(v), (v + 0.4, j + 0.25 - i * 0.25), fontsize=8, va="center", color=color)
ax.set_yticks(y_pos, nombres)
ax.set_xlim(0, 45)
ax.set_title("Carencias de la vivienda en hogares con NNA (% ponderado)\\n"
             "(solo las 4 carencias comparables entre el formulario 2019 y el vigente)")
ax.set_xlabel("% de hogares con NNA")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuente: elaboración propia sobre microdatos de la ECH (INE), hogares con al menos un NNA, "
            "ponderador anual.", y=-0.05)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras horizontales agrupadas por año: permite
comparar cada carencia entre años sin encadenar una serie que el cambio
de formulario no sostiene.

**Lectura**: las humedades en los cimientos son la carencia más
extendida (36,8% de los hogares con NNA en 2025, subiendo desde 32,1% en
2019) y las goteras afectan a un cuarto (24,2%). Más de un tercio de la
infancia uruguaya crece en viviendas con problemas de humedad
estructural.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 34. Brecha digital en hogares con NNA

**¿Qué pregunta responde?** ¿Los hogares donde viven NNA tienen acceso a
internet y a dispositivos?
"""),
    code("""
bd = ECHM[(ECHM["metrica"] == "brecha_digital_hogares_nna") &
          (ECHM["categoria"].isin(["recurso=internet", "recurso=internet_fija", "recurso=pc"]))].copy()
bd["recurso"] = bd["categoria"].str.replace("recurso=", "", regex=False)
piv = bd.pivot_table(index="anio", columns="recurso", values="valor")
fig, ax = plt.subplots()
nombres = {"internet": "Acceso a internet (cualquier tipo)", "internet_fija": "Internet fija en la vivienda",
           "pc": "Computadora o tablet"}
for i, col in enumerate(["internet", "internet_fija", "pc"]):
    ax.plot(piv.index, piv[col], marker="o", linewidth=2, color=PALETA[i], label=nombres[col])
    anotar_extremos(ax, piv.index.to_numpy(), piv[col].to_numpy(), PALETA[i], dec=1)
ax.set_ylim(0, 100)
ax.set_xticks(piv.index)
ax.set_title("Acceso digital en hogares con NNA (% ponderado)")
ax.set_ylabel("% de hogares con NNA")
ax.legend(frameon=False, fontsize=9, loc="lower right")
fuente(fig, "Fuente: elaboración propia sobre microdatos de la ECH (INE), hogares con al menos un NNA, "
            "ponderador anual.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Tres líneas de la misma unidad, eje 0-100;
los extremos anotados por recurso.

**Lectura**: el acceso general a internet crece (71,0% en 2019 → 85,7%
en 2025), pero la composición cambia: la internet **fija** en la
vivienda retrocede (88,8% → 82,2% entre los hogares con internet del
formulario de cada año) — consistente con la migración a conexiones
móviles — y la tenencia de computadora está estancada (~80%). La brecha
por estrato queda disponible en la fuente para el análisis
socioeconómico.
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 35. Inseguridad alimentaria en hogares con menores (FIES)

**¿Qué pregunta responde?** ¿Qué proporción de los hogares con menores
de 18 años experimenta inseguridad alimentaria?
"""),
    code("""
fies = ECHM[(ECHM["metrica"] == "fies_hogares_menores") &
            (ECHM["categoria"].isin(["nivel=moderada_o_severa", "nivel=severa"]))].copy()
piv = fies.pivot_table(index="anio", columns="categoria", values="valor")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(piv.index, piv["nivel=moderada_o_severa"], marker="o", color=COLOR, linewidth=2,
        label="Moderada o severa")
ax.plot(piv.index, piv["nivel=severa"], marker="o", color=ACENTO, linewidth=2, label="Severa")
anotar_extremos(ax, piv.index.to_numpy(), piv["nivel=moderada_o_severa"].to_numpy(), COLOR, dec=1)
anotar_extremos(ax, piv.index.to_numpy(), piv["nivel=severa"].to_numpy(), ACENTO, dec=1)
ax.set_ylim(0, 25)
ax.set_xticks(piv.index)
ax.set_title("Inseguridad alimentaria en hogares con menores de 18 años (% ponderado, escala FIES)")
ax.set_ylabel("% de hogares con menores")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuente: elaboración propia sobre el módulo FIES de la ECH (INE), hogares con el marcador "
            "oficial menores18, ponderador del módulo.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos niveles de la misma escala en líneas
separadas (no apiladas: «severa» es subconjunto de «moderada o
severa»).

**Lectura**: la inseguridad alimentaria moderada o severa desciende
(18,3% de los hogares con menores en 2023 → 15,3% en 2025), igual que la
severa (3,4% → 2,0%). Aun con la mejora, en 2025 unos 15 de cada 100
hogares con niños experimentaron inseguridad alimentaria — y en los
hogares con menores de 6 años la incidencia es levemente mayor (17,5%).
"""),
    # ------------------------------------------------------------------
    md("""
### Métrica 36. Victimización de hogares donde viven NNA

**¿Qué pregunta responde?** ¿Qué proporción de los hogares con NNA
sufrió delitos en el último año?
"""),
    code("""
vic = ECHM[(ECHM["metrica"] == "victimizacion_hogares_nna") &
           (ECHM["categoria"].str.startswith("delito="))].copy()
vic["delito"] = vic["categoria"].str.replace("delito=", "", regex=False)
piv = vic.pivot_table(index="delito", columns="anio", values="valor").sort_values(2025)
y_pos = np.arange(len(piv))
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.barh(y_pos + 0.2, piv[2024], height=0.38, color=PALETA[3], label="2024")
ax.barh(y_pos - 0.2, piv[2025], height=0.38, color=COLOR, label="2025")
for i, (v24, v25) in enumerate(zip(piv[2024], piv[2025])):
    ax.annotate(pct(v24), (v24 + 0.05, i + 0.2), fontsize=8, va="center", color=PALETA[3])
    ax.annotate(pct(v25), (v25 + 0.05, i - 0.2), fontsize=8, va="center", color=COLOR)
ax.set_yticks(y_pos, piv.index)
ax.set_xlim(0, 3.2)
ax.set_title("Hogares con NNA que declaran haber sufrido delitos (% ponderado)\\n"
             "(módulo de victimización de la ECH; responden personas adultas del hogar)")
ax.set_xlabel("% de hogares con NNA")
ax.legend(frameon=False, fontsize=9)
fuente(fig, "Fuente: elaboración propia sobre el módulo de victimización de la ECH (INE), hogares con al menos "
            "un NNA, ponderador del módulo.", y=-0.04)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Barras horizontales agrupadas por año,
ordenadas por magnitud, para comparar tipos de delito con nombres
largos entre dos mediciones.

**Lectura**: 2,5% de los hogares con NNA declaró haber sufrido al menos
un delito en 2024, y 1,7% en 2025; el robo o asalto fuera de la
vivienda y la estafa encabezan los tipos. Serie nueva (el módulo se
releva desde 2024): su valor analítico crecerá con los años.
"""),
    # ==================================================================
    md("""
## Cruces entre fuentes — ¿La respuesta institucional sigue el mapa de la necesidad?

Los cuatro cruces del catálogo contrastan la respuesta de los sistemas
de protección (INAU, CONAPEES/Fiscalía, SIPIAV) y la única prevalencia
disponible (ENSANNA) con las condiciones socioeconómicas de la infancia
calculadas sobre la ECH. Reglas comunes a todos: ambos lados de cada
cruce al **mismo nivel de agregación**, lectura observacional
(asociación, nunca causa) y las limitaciones de cada cruce declaradas en
su propia sección — ninguna conclusión describe individuos.
"""),
    md("""
### Cruce 1. ¿La intensidad territorial de la protección especial sigue el mapa de la pobreza infantil?

**¿Qué pregunta responde?** ¿Los departamentos con más pobreza infantil
son también los de mayor tasa de NNA en protección especial?

**Construcción**: tasa = NNA atendidos en proyectos del SPE del
departamento (segundo semestre de cada año) cada 1.000 NNA residentes
(población 0-17 ponderada de la ECH del mismo año). Advertencia
importante del numerador: cuenta dónde se **atiende** al NNA, no de
dónde proviene — un niño derivado a una residencia de otro departamento
cuenta en el departamento de la residencia.
"""),
    code("""
CRUCE = pd.read_csv(RESULTADOS / "cruces" / "cruce_inau_ech_departamental.csv")

c25 = CRUCE[CRUCE["anio"] == 2025]
rho25, _ = spearmanr(c25["tasa_spe_por_mil"], c25["pobreza_0a17_pct"])
c24 = CRUCE[CRUCE["anio"] == 2024]
rho24, _ = spearmanr(c24["tasa_spe_por_mil"], c24["pobreza_0a17_pct"])

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(c25["pobreza_0a17_pct"], c25["tasa_spe_por_mil"], color=COLOR, s=45, zorder=3)
a_la_izquierda = {"Treinta y Tres", "Tacuarembó"}
abajo = {"Montevideo", "Colonia"}
arriba = {"Salto"}
for _, fila in c25.iterrows():
    d = fila["departamento"]
    dx, dy, ha = 5, 4, "left"
    if d in a_la_izquierda:
        dx, ha = -6, "right"
    if d in abajo:
        dy = -12
    if d in arriba:
        dy = 10
    ax.annotate(d, (fila["pobreza_0a17_pct"], fila["tasa_spe_por_mil"]),
                textcoords="offset points", xytext=(dx, dy), ha=ha, fontsize=8, color="#444444")
ax.set_xlim(0, 40)
ax.set_ylim(0, 22)
ax.set_yticks(np.arange(0, 21, 5))
def _rho(v):
    return f"{v:+.2f}".replace(".", ",")
ax.set_title(
    "Tasa de NNA en protección especial y pobreza infantil por departamento, 2025\\n"
    "(cada punto es un departamento; asociación de rangos "
    f"rho = {_rho(rho25)} en 2025 y {_rho(rho24)} en 2024 — sin asociación estable)"
)
ax.set_xlabel("Pobreza monetaria 0-17 (% ponderado, ECH)")
ax.set_ylabel("NNA en el SPE cada 1.000 NNA residentes")
fuente(fig, "Fuente: elaboración propia sobre INAU (SIPI, indicador departamental 1, 2025-S2) y microdatos "
            "de la ECH 2025 (INE). Detalle y n muestrales: resultados/cruces/cruce_inau_ech_departamental.csv.",
       y=-0.02)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dispersión con los dos ejes en sus escalas
reales y cada departamento identificado: para una asociación entre dos
variables a nivel de 19 unidades, el plano completo con etiquetas es más
honesto que un coeficiente solo — el lector ve qué departamentos
sostienen (o desarman) la relación. El coeficiente de rangos (Spearman)
acompaña en el título con su valor en ambos años.

**Lectura**: **la intensidad territorial de la protección especial no
sigue el mapa de la pobreza infantil** (rho = −0,10 en 2025 y +0,02 en
2024: sin asociación, con signo inestable). Las tasas más altas están en
dos departamentos chicos de pobreza baja o media — Florida (19,4 por
mil, con 20,2% de pobreza infantil) y Flores (16,3 por mil, 16,6%) —
mientras que en el otro extremo conviven departamentos de pobreza
infantil alta con tasas bajas: Canelones (3,8 por mil, 23,9% de
pobreza), Paysandú (4,9 y 28,5%) y Rivera, que tiene la pobreza infantil
más alta del país (37,7%) y una tasa de 7,6. Con el hacinamiento el
resultado es el mismo (rho inestable entre −0,28 y +0,19). La interpretación prudente, en lenguaje observacional: la
distribución territorial de la atención parece responder a la
localización histórica de la oferta institucional (dónde hay residencias
y proyectos) y a derivaciones entre departamentos, más que a la
distribución territorial de la necesidad socioeconómica. Dos advertencias
acotan esta lectura: el numerador registra el departamento de atención
(no el de origen del NNA), y las estimaciones departamentales de la ECH
tienen error muestral mayor en los departamentos chicos (n muestrales en
el CSV del cruce). Aun con esas salvedades, la ausencia de correlación
es un hallazgo para la discusión de política territorial — y la pregunta
que abre (¿la oferta está donde está la necesidad?) excede lo que estas
fuentes pueden responder solas.
"""),
    md("""
### Cruce 2. ¿La detección de la explotación sexual sigue el mapa de las carencias?

**¿Qué pregunta responde?** ¿Los departamentos con más pobreza infantil
y hacinamiento son también los de más situaciones de ESNNA atendidas
(CONAPEES) y más actuaciones fiscales por delitos sexuales contra NNA
(Fiscalía General de la Nación), en proporción a su población infantil?

**Construcción**: tasa cada 10.000 NNA = casos del departamento
(2018-2021, tablas 2 y 8 del estudio FLACSO 2023) sobre la población
0-17 ponderada de la ECH 2019 — el único año de la ventana con
microdatos extraídos; el lado socioeconómico (pobreza y hacinamiento)
queda fijo en 2019 por la misma razón, de modo que 2020 y 2021 se cruzan
contra condiciones previas a la pandemia. Tres advertencias mayores
acotan este cruce: los conteos departamentales son chicos (de 0 a 59
situaciones anuales en CONAPEES — una situación mueve la tasa de un
departamento chico), el registro mide detección y atención — nunca
incidencia — y el propio estudio FLACSO advierte que los departamentos
con más actuaciones cada 10.000 NNA posiblemente tienen más recursos y
equipos locales, no más explotación (pp. 46 y 52).
"""),
    code("""
CFE = pd.read_csv(RESULTADOS / "cruces" / "cruce_conapees_fiscalia_ech.csv")

etiquetas_fuente = {"conapees": "CONAPEES (situaciones ESNNA)",
                    "fiscalia": "Fiscalía (actuaciones)"}
rhos = []
for fuente_cruce in ["conapees", "fiscalia"]:
    for anio_cruce in [2018, 2019, 2020, 2021]:
        t = CFE[(CFE["fuente"] == fuente_cruce) & (CFE["anio"] == anio_cruce)]
        for variable, etiqueta_v in [("pobreza_2019_pct", "pobreza"),
                                     ("hacinamiento_2019_pct", "hacinamiento")]:
            rho, _ = spearmanr(t["tasa_por_10mil"], t[variable])
            rhos.append({"fuente": etiquetas_fuente[fuente_cruce],
                         "anio": anio_cruce, "variable": etiqueta_v, "rho": rho})
RHOS = pd.DataFrame(rhos)

fig, ax = plt.subplots(figsize=(9, 4.8))
filas_y = [(f, a) for f in etiquetas_fuente.values() for a in [2018, 2019, 2020, 2021]]
posiciones = {fa: i for i, fa in enumerate(filas_y)}
for variable, color, marcador in [("hacinamiento", COLOR, "o"), ("pobreza", ACENTO, "s")]:
    sub = RHOS[RHOS["variable"] == variable]
    y = [posiciones[(f, a)] for f, a in zip(sub["fuente"], sub["anio"])]
    ax.scatter(sub["rho"], y, color=color, marker=marcador, s=55, zorder=3,
               label=f"tasa vs. {variable}")
ax.axvline(0, color="#999999", linewidth=1)
ax.set_yticks(range(len(filas_y)))
ax.set_yticklabels([f"{f} · {a}" for f, a in filas_y], fontsize=9)
ax.invert_yaxis()
ax.set_xlim(-1, 1)
ax.set_xlabel("Correlación de rangos (Spearman) con la tasa cada 10.000 NNA")
ax.set_title("Asociación departamental de la detección de explotación sexual con pobreza y hacinamiento\\n"
             "(cada punto es un año de una fuente; a la izquierda de 0: más detección donde hay menos carencia)")
ax.legend(frameon=False, loc="lower right")
fuente(fig, "Fuente: elaboración propia sobre FLACSO Uruguay 2023 (tablas 2 y 8; CONAPEES y FGN/SIPPAU 2018-2021) y "
            "microdatos de la ECH 2019 (INE). Detalle y n muestrales: resultados/cruces/cruce_conapees_fiscalia_ech.csv.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Con dos fuentes, cuatro años y dos variables,
mostrar el plano de un solo año sería una selección arbitraria: se
muestra el coeficiente de cada combinación (16 puntos) para exhibir lo
único que este cruce puede afirmar con honestidad — la estabilidad del
signo a través de años y fuentes. El detalle departamental, con sus n
muestrales, queda en el CSV del cruce.

**Lectura**: con la pobreza no hay asociación (rho entre −0,27 y +0,09
según año y fuente, siempre compatible con el azar). Con el hacinamiento
la asociación es **negativa en las ocho combinaciones** (entre −0,22 y
−0,71): los departamentos con más hacinamiento tienden a registrar
*menos* situaciones atendidas y menos actuaciones fiscales cada 10.000
NNA, no más. Leída junto con la advertencia del propio estudio FLACSO —
más actuaciones donde hay más recursos y equipos, no necesariamente más
incidencia — la interpretación observacional prudente es que este cruce
retrata la **geografía de la capacidad de detección, no la del
fenómeno**: donde las carencias habitacionales son mayores, el sistema
registra menos. Advertencias adicionales: el valor de Paysandú 2020 en
la fuente fiscal (1 actuación) es una anomalía interna del estudio — el
resultado se sostiene al excluirlo (rho = −0,66) — y el numerador
registra el departamento de actuación, no el de residencia de la
víctima.
"""),
    md("""
### Cruce 3. ¿El trabajo infantil sigue el gradiente socioeconómico de la pobreza?

**¿Qué pregunta responde?** ¿El trabajo infantil declarado (la única
prevalencia real del proyecto) se concentra en los niveles
socioeconómicos bajos tanto como la pobreza infantil?

**Construcción**: este cruce compara **formas de gradiente, no
valores** — las escalas socioeconómicas de los dos lados no son la misma
variable. La ENSANNA clasifica por INSE (índice de CINVE, nacional,
cinco niveles); la extracción de la ECH solo trae un ordenamiento
socioeconómico comparable para Montevideo (estratos 1 a 5 — los códigos
del interior son geográficos, sin orden socioeconómico). A eso se suman
universos distintos (5-17 contra 0-17) y que el boletín ENSANNA no
publica errores estándar ni microdatos. Por eso los paneles llevan
escalas separadas y ninguna cifra de un lado se compara con el nivel del
otro.
"""),
    code("""
CEE = pd.read_csv(RESULTADOS / "cruces" / "cruce_ensanna_ech.csv")
orden_nse = ["Bajo", "Medio bajo", "Medio", "Medio alto", "Alto"]
ens_nse = (CEE[(CEE["fuente"] == "ensanna_2024") & (CEE["dimension"] == "nse")
               & (CEE["metrica"] == "trabajo_infantil")]
           .set_index("categoria").loc[orden_nse, "valor"])
ech_nse = (CEE[(CEE["fuente"] == "ech_2024") & (CEE["dimension"] == "nse")]
           .set_index("categoria").loc[orden_nse, "valor"])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.4))
for ax, serie, titulo, color in [
    (ax1, ens_nse, "Trabajo infantil 5-17\\n(ENSANNA 2024, INSE nacional)", COLOR),
    (ax2, ech_nse, "Pobreza 0-17\\n(ECH 2024, estratos de Montevideo)", ACENTO),
]:
    ax.barh(range(len(serie)), serie.to_numpy(), color=color)
    ax.set_yticks(range(len(serie)))
    ax.set_yticklabels(serie.index)
    ax.invert_yaxis()
    ax.set_title(titulo, fontsize=10)
    for i, v in enumerate(serie):
        ax.annotate(pct(v), (v, i), textcoords="offset points", xytext=(4, 0),
                    va="center", fontsize=9)
    ax.set_xlim(0, serie.max() * 1.2)
fig.suptitle("Dos gradientes socioeconómicos — comparación de formas, no de niveles (escalas distintas)",
             y=1.04, fontsize=12)
fuente(fig, "Fuente: ENSANNA 2024, Cuadro 4 (INE/MTSS; INSE de CINVE) y elaboración propia sobre microdatos de la "
            "ECH 2024 (INE), solo Montevideo. Detalle y n muestrales: resultados/cruces/cruce_ensanna_ech.csv.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Dos paneles de barras con escalas separadas:
la única comparación defendible entre dos índices socioeconómicos
distintos es la forma del gradiente (¿es monótono? ¿cuánto separa a los
extremos?), y esa forma se ve en los largos relativos de las barras de
cada panel, sin inducir jamás la comparación de niveles entre paneles.

**Lectura**: los dos gradientes son monótonos — a menor nivel
socioeconómico, más trabajo infantil y más pobreza — pero sus pendientes
relativas son muy distintas: la pobreza infantil de Montevideo se
multiplica por 20 entre el estrato alto y el bajo (2,7% a 54,5%),
mientras el trabajo infantil nacional apenas se multiplica por 1,6 (4,8%
a 7,9%). En términos observacionales: **el trabajo infantil declarado
atraviesa toda la estructura social** y su gradiente es mucho más plano
que el de la pobreza. La región refuerza esa disociación con dos fuentes
independientes: el trabajo infantil 5-17 es más frecuente en el interior
que en Montevideo (7,7% contra 5,2%, y el doble en actividades
económicas: 5,9% contra 2,9%), igual que la ocupación adolescente 14-17
medida por la ECH (3,7% contra 1,7%) — pero la pobreza infantil es algo
mayor en Montevideo (30,9% contra 27,8% en 2024). **La geografía del
trabajo infantil no es la geografía de la pobreza infantil**: el
componente rural y de actividades económicas del interior pesa más que
la privación monetaria. Advertencia final: la ENSANNA mide actividades
declaradas por los hogares, y la subdeclaración no es necesariamente
pareja entre niveles socioeconómicos.
"""),
    md("""
### Cruce 4. ¿Las edades atendidas por el SIPIAV reflejan las edades de la población infantil?

**¿Qué pregunta responde?** ¿Qué tramos de edad pesan en las situaciones
de violencia atendidas más de lo que pesan en la población — y ese
sesgo, sigue al tramo más pobre?

**Construcción**: índice de representación = participación del tramo en
las situaciones atendidas (SIPIAV, distribución publicada, renormalizada
al universo 0-17) sobre su participación en la población 0-17 (ECH
ponderada del mismo año). 1 = el tramo pesa en la atención lo mismo que
en la población. Años comparables: 2019 y 2025, los únicos con la
distribución etaria completa y microdatos ECH extraídos. El SIPIAV no
publica apertura departamental, así que este cruce es solo nacional
(limitación estructural del catálogo).
"""),
    code("""
CSE = pd.read_csv(RESULTADOS / "cruces" / "cruce_sipiav_ech_tramos.csv")
tramos_cruce = ["0 a 5", "6 a 12", "13 a 17"]
fig, ax = plt.subplots(figsize=(9, 3.8))
for anio_cruce, color in [(2019, "#999999"), (2025, COLOR)]:
    t = CSE[CSE["anio"] == anio_cruce].set_index("tramo").loc[tramos_cruce]
    ax.scatter(t["indice_representacion"], range(len(tramos_cruce)), s=70,
               color=color, zorder=3, label=str(anio_cruce))
    for i, v in enumerate(t["indice_representacion"]):
        ax.annotate(f"{v:.2f}".replace(".", ","), (v, i),
                    textcoords="offset points", xytext=(0, 9), ha="center",
                    fontsize=9, color=color)
ax.axvline(1, color="#bbbbbb", linewidth=1)
ax.set_yticks(range(len(tramos_cruce)))
ax.set_yticklabels(tramos_cruce)
ax.invert_yaxis()
ax.set_xlim(0.5, 1.4)
ax.set_xlabel("Índice de representación (participación en situaciones / participación en población)")
ax.set_title("Representación de cada tramo de edad en las situaciones atendidas por el SIPIAV\\n"
             "(1 = el tramo pesa en la atención lo mismo que en la población 0-17)")
ax.legend(frameon=False, loc="lower right")
fuente(fig, "Fuente: elaboración propia sobre SIPIAV (informes 2019 y 2025, distribución renormalizada a 0-17) y "
            "microdatos de la ECH (INE). Detalle: resultados/cruces/cruce_sipiav_ech_tramos.csv.", y=-0.08)
plt.show()
"""),
    md("""
**Por qué esta gráfica.** El índice de representación en un eje único
con la línea de paridad marcada: la pregunta del cruce es de desvío
respecto de 1, y esa distancia se lee directamente, con los dos años
como control de estabilidad.

**Lectura**: los adolescentes (13-17) están sobrerrepresentados en las
situaciones atendidas en ambos años (índice 1,20 en 2019 y 1,08 en
2025). El cambio grande es la primera infancia: pasó de una
subrepresentación fuerte en 2019 (0,65) a la casi paridad en 2025
(0,95). El registro no permite distinguir si eso refleja más violencia
hacia la primera infancia o mejor detección temprana — y el informe
SIPIAV 2025 introdujo además una metodología nueva en paralelo, con
quiebres documentados en la serie curada. Lo que el cruce sí permite
afirmar: **el perfil etario de la atención no sigue al de la pobreza** —
la primera infancia es el tramo más pobre en ambos años (29,1% contra
26,5% de los adolescentes en 2025) y aun así fue el tramo históricamente
menos representado en la atención. La sobrerrepresentación adolescente
es coherente con la mayor visibilidad de esa violencia para el sistema
(escolarización, capacidad de denuncia propia), no necesariamente con
mayor incidencia. Advertencias: porcentajes publicados redondeados a
enteros y renormalizados (2019 incluía un 9% de mayores de 18) y quiebre
de tramos en 2020 (0-3/4-5 pasa a 0-5): la comparación usa el agregado
0-5, único comparable.
"""),
    # ==================================================================
    md("""
## Contexto transversal — La demografía detrás de todas las tasas

### P6. Población de 0 a 17 años de Uruguay, proyección oficial

**¿Qué pregunta responde?** ¿Cómo evoluciona el denominador de todas las
tasas de infancia del país?
"""),
    code("""
import openpyxl

wb = openpyxl.load_workbook(DATA / "ine" / "proyecciones_rev2025" / "B11_uruguay_edad_simple_2024_2070.xlsx",
                            read_only=True)
filas = list(wb["Uruguay"].iter_rows(values_only=True))
wb.close()
encabezado = filas[4]
cols = {a: i for i, a in enumerate(encabezado) if isinstance(a, int) and a <= 2040}
anios_ine = sorted(cols)
pob017 = [sum(filas[6 + edad][cols[a]] for edad in range(18)) for a in anios_ine]

fig, ax = plt.subplots()
ax.plot(anios_ine, pob017, marker="o", color=COLOR, linewidth=2, markersize=4)
ax.set_ylim(0, 850000)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: fmt(v)))
ax.set_title("Población proyectada de 0 a 17 años, Uruguay (proyección oficial del INE)")
ax.set_ylabel("Personas de 0 a 17 años")
anotar_extremos(ax, anios_ine, pob017, COLOR)
fuente(fig, "Fuente: INE, proyecciones de población revisión 2025 (Censo 2023), archivo B.1.1, suma de "
            "edades simples 0 a 17. No es un cálculo propio: se cita la proyección del organismo oficial.")
plt.show()
"""),
    md("""
**Por qué esta gráfica.** Línea sobre la proyección del organismo
productor (única proyección del informe que no es propia): se cita, no
se modela.

**Lectura**: la población de 0 a 17 años cae de 768.969 (2024) a menos
de 600.000 hacia 2040 según la revisión 2025 del INE — más de un quinto
menos en una década y media. Toda tasa «cada 1.000 NNA» del país subirá
mecánicamente si su numerador no cae al mismo ritmo (el caso de P4), y
todo servicio dimensionado para la infancia actual operará sobre una
población menguante: es el trasfondo demográfico de todos los temas de
este informe.
"""),
    # ==================================================================
    md("""
## Nota metodológica

**Registros administrativos y prevalencia.** La mayoría de las cifras de
este informe (SIPIAV, CONAPEES, Fiscalía, INAU) cuentan las situaciones
que cada sistema detecta y atiende. No miden cuántos NNA atraviesan cada
problema: un aumento puede reflejar mayor capacidad de detección, más
denuncia o más incidencia, y el registro solo no permite distinguirlo.
Por eso ninguna frase de este informe convierte cifras de registro en
afirmaciones sobre la magnitud del fenómeno. Las únicas fuentes de
prevalencia son la ENSANNA 2024 y los cálculos propios sobre la ECH.

**Qué significa «ponderado».** Las cifras de encuestas no son
porcentajes simples de las personas encuestadas: cada hogar de la
muestra representa a un número distinto de hogares del país. Todos los
porcentajes de encuesta de este informe usan esa expansión.

**Escenarios inerciales.** Las proyecciones describen qué sucedería **si
las condiciones actuales persisten**, siempre con un rango. No son
pronósticos. Cuando ningún modelo simple supera la prueba de validación
(el caso de P4), no se publica proyección — se dice explícitamente. La
justificación técnica de cada método, con sus pruebas, está en el
repositorio (`docs/PREDICTIVO_JUSTIFICACION_TECNICA.md`) y no forma
parte de este informe.

**Quiebres de serie.** Ninguna serie con cambio de definición o de
metodología se presenta empalmada: los quiebres se marcan en la propia
gráfica (tipos de violencia 2020 y 2024, base de cálculo SIPIAV 2025,
canasta de pobreza 2023-2024, formulario de vivienda) y los puntos no
comparables se dibujan sueltos.

**Celdas chicas y datos faltantes.** No se publica ninguna
desagregación por debajo del umbral que publica el propio organismo, y
las categorías de datos faltantes se muestran cuando la fuente las
publica (métrica 26): la calidad del registro es parte del dato.
"""),
    md("""
## Resumen analítico

**Violencia (SIPIAV).** La respuesta del sistema se multiplicó por 7 en
doce años (1.319 → 9.178 situaciones) y la proyección publicada para
2025 quedó validada por el dato real. La detección sigue siendo tardía
(en la serie comparable, ~9 de cada 10 situaciones ya eran crónicas) y
la inclusión de la familia en la intervención cayó de 82% a 58% en una
década. Las violencias sexuales tienen patrón propio: 76% niñas y
adolescentes mujeres, 51% concentrado en 13-17 años.

**Explotación sexual (CONAPEES/Fiscalía).** Entre 240 y 494 situaciones
atendidas por año (2018-2021, 86% niñas y adolescentes mujeres) y más de
2.000 actuaciones anuales de Fiscalía por delitos sexuales con víctima
NNA. El vacío es el dato: no hay serie oficial desde 2022, y desde 2024
la explotación sexual perdió su categoría propia en el registro del
SIPIAV.

**Trabajo infantil (ENSANNA/ECH).** 6,8% de los NNA de 5 a 17 (40.200)
en situación de trabajo infantil, con gradientes por edad, región y
nivel socioeconómico. El trabajo no remunerado de servicios ya muestra
división sexual (niñas 2,8% frente a varones 1,1%). El trabajo
adolescente que existe es casi todo informal (82-93% de los ocupados de
14-17).

**Protección especial (INAU).** El sistema creció hasta 2023 y se
amesetó (~8.000 atendidos; ~7.000 de 0-17). La desinternación avanza
(50,9% → 62,7% en contexto familiar) y llegaría a 66,4% en 2027 si el
ritmo persiste. Las señales de alerta: 56,9% de los casos sin registro
de contacto familiar, casi 4 de cada 10 sin controles médicos al día, y
una tasa de NNA en protección (9,4 por mil) que sube por pura
demografía.

**Pobreza y entorno (ECH).** 27,5% de los NNA en hogares pobres (2025,
canasta 2017), con la primera infancia como el grupo más afectado. Más
de un tercio de los hogares con NNA tiene humedades estructurales; la
inseguridad alimentaria mejora pero alcanza al 15,3% de los hogares con
menores; la brecha digital se cierra en acceso general pero retrocede en
internet fija.

**Cruce territorial (INAU × ECH).** La tasa departamental de NNA en
protección especial no está asociada a la pobreza infantil ni al
hacinamiento del departamento (Spearman sin asociación estable en 2024 y
2025): la distribución territorial de la atención parece responder a la
localización de la oferta institucional y a las derivaciones más que al
mapa de la necesidad — una pregunta abierta para la política
territorial.

**Cruces entre fuentes (CONAPEES/Fiscalía, ENSANNA, SIPIAV × ECH).** La
detección de la explotación sexual tampoco sigue el mapa de las
carencias: la asociación con el hacinamiento es negativa y estable en
las ocho combinaciones de fuente y año — se registra menos donde las
carencias habitacionales son mayores, consistente con que el registro
retrata la capacidad de detección y no el fenómeno. El trabajo infantil
declarado atraviesa toda la estructura social, con un gradiente mucho
más plano que el de la pobreza y la geografía invertida (más frecuente
en el interior, con la pobreza infantil algo mayor en Montevideo). Y el
perfil etario de la atención del SIPIAV no sigue al tramo más pobre: la
primera infancia — la más pobre — fue históricamente la menos
representada en la atención, aunque en 2025 se acercó a la paridad.
"""),
    # ==================================================================
    # Conclusiones: una celda por conclusión, a propósito — las ediciones
    # parciales incluyen las conclusiones de sus bloques (el mapa
    # conclusión → bloques vive en construir_informe.CONCLUSIONES_BLOQUES
    # y un test lo mantiene alineado con estas celdas).
    md("""
## Conclusiones
"""),
    md("""
1. **La pobreza uruguaya está concentrada en la infancia, y dentro de la
   infancia, en sus edades más tempranas.** 27,5% de los NNA en hogares
   pobres (2025) frente a ~17% en la población general, con incidencia
   máxima en la primera infancia. Es el dato más relevante del informe
   para el diseño de políticas (fuente: elaboración propia sobre ECH,
   INE).
"""),
    md("""
2. **El país tiene sistemas de protección en expansión y una infancia en
   contracción.** La respuesta del SIPIAV se multiplicó por 7; el SPE
   del INAU creció hasta amesetarse en ~8.000 atendidos; y la población
   de 0 a 17 cae 2,3% por año. La combinación produce tasas de
   institucionalización crecientes aun sin crecimiento de los sistemas
   (P4) — leer cualquier tasa de infancia sin su denominador demográfico
   induce a error (fuentes: SIPIAV, INAU, INE).
"""),
    md("""
3. **La detección de la violencia llega tarde y la intervención pierde a
   la familia.** En la serie comparable, ~9 de cada 10 situaciones
   detectadas ya eran crónicas, solo 4 de cada 10 NNA visualizan la
   violencia que sufren, y la inclusión familiar en la intervención cayó
   24 puntos en una década (82% → 58%), con escenario inercial en ~50%
   hacia 2027 (fuente: SIPIAV).
"""),
    md("""
4. **La violencia sexual hacia NNA es adolescente y de género, y perdió
   visibilidad estadística.** 76% de las violencias sexuales afecta a
   niñas y adolescentes mujeres y 51% se concentra en 13-17 años; la
   explotación sexual no tiene serie oficial desde 2022 y desde 2024
   quedó fusionada dentro de «violencias sexuales» (fuentes: SIPIAV,
   CONAPEES/FLACSO).
"""),
    md("""
5. **Uruguay no mide la prevalencia de la violencia hacia NNA.** Todo el
   tema 1 es registro administrativo. La única aproximación existente —
   una encuesta de 2026 de UNICEF con muestra no probabilística, que
   sugiere que cerca de 3 de cada 10 jóvenes vivió violencia sexual
   antes de los 18 — no sustituye una medición oficial con diseño
   muestral: esa es la brecha de información más importante que este
   proyecto identifica (fuentes: SIPIAV; UNICEF/Equipos 2026, con su
   diseño declarado).
"""),
    md("""
6. **Limitaciones declaradas de este informe**: (a) las cifras de
   registros administrativos describen la respuesta de los sistemas, no
   la prevalencia; (b) las proyecciones son escenarios inerciales con
   supuesto explícito — y donde ningún modelo pasó la validación (P4) no
   hay proyección; (c) los microdatos de la ENSANNA aún no son públicos
   (el tema 3 usa el boletín oficial); (d) el SIPIAV no publica
   desagregación departamental, lo que limita el análisis territorial de
   la violencia; (e) los cuatro cruces entre fuentes comparten tres
   límites estructurales — los numeradores administrativos registran
   dónde se atiende o actúa (no dónde reside el NNA), las estimaciones
   departamentales de la ECH tienen error muestral mayor en los
   departamentos chicos, y toda asociación es observacional — además de
   las limitaciones propias declaradas en la sección de cada cruce:
   escalas socioeconómicas no comparables y sin errores estándar en la
   ENSANNA, porcentajes redondeados y renormalizados en el SIPIAV, y
   conteos chicos con condiciones fijadas en 2019 en CONAPEES/Fiscalía.
"""),
    # ==================================================================
    # Fuentes: sección fija de TODA edición (total o parcial) — decisión
    # del dueño del proyecto (2026-08-19): las fuentes con sus enlaces
    # validan los números y las elecciones del informe. Los enlaces son
    # los ya citados en docs/BIBLIOGRAFIA.md (fuente única de citas).
    md("""
## Fuentes de datos y bibliografía

Cada cifra de este informe lleva su fuente citada en su propia sección;
esta lista reúne las fuentes de datos del proyecto con sus enlaces
oficiales, para verificación directa.

**Registros administrativos e informes institucionales**

- **SIPIAV — informes de gestión (serie desde 2013)**, INAU y sistema
  interinstitucional: [inau.gub.uy/sipiav](https://www.inau.gub.uy/sipiav).
  Registro administrativo: mide situaciones atendidas, nunca prevalencia.
- **INAU — indicadores del Sistema de Protección Especial (SIPI)**:
  [inau.gub.uy/transparencia](https://inau.gub.uy/transparencia/indicadores-sistema-de-proteccion-especial-inau).
  Registro administrativo nacional y departamental.
- **CONAPEES — explotación sexual de NNA**:
  [inau.gub.uy/conapees](https://www.inau.gub.uy/conapees); serie
  cuantitativa 2018-2021 compilada por el estudio de
  [FLACSO Uruguay (2023)](https://flacso.edu.uy/wp-content/uploads/2023/12/EXPLOTACION-SEXUAL-HACIA-NINAS-NINOS-Y-ADOLESCENTES-COMPLETO.pdf),
  capítulo 6 (incluye las actuaciones de la Fiscalía General de la Nación).
- **CETI — política nacional contra el trabajo infantil (MTSS)**:
  [gub.uy/ministerio-trabajo-seguridad-social](https://www.gub.uy/ministerio-trabajo-seguridad-social/comunicacion/noticias/ceti).

**Encuestas y estadísticas oficiales (INE)**

- **ENSANNA 2024** — Encuesta Nacional sobre las Actividades de Niñas,
  Niños y Adolescentes (INE/MTSS), única fuente de prevalencia de
  trabajo infantil:
  [gub.uy/instituto-nacional-estadistica](https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/encuestas/encuesta-nacional-sobre-actividades-ninas-ninos-adolescentes-ensanna).
- **ECH — Encuesta Continua de Hogares (INE)**, microdatos ponderados
  (pobreza, hacinamiento, vivienda, brecha digital, empleo adolescente,
  FIES, victimización):
  [www4.ine.gub.uy/Anda5](https://www4.ine.gub.uy/Anda5/), procesados
  con la infraestructura verificada de
  [agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares).
- **Proyecciones de población, revisión 2025 (INE, Censo 2023)** — el
  denominador demográfico de todas las tasas:
  [gub.uy/instituto-nacional-estadistica/proyeccionesrev2025](https://www.gub.uy/instituto-nacional-estadistica/proyeccionesrev2025).

**Fuentes secundarias**

- **UNICEF Uruguay — Infancia en Datos** (pobreza infantil, protección):
  [unicef.org/uruguay/infancia-en-datos](https://www.unicef.org/uruguay/infancia-en-datos).

Las citas completas, con la naturaleza de cada dato y sus advertencias
de uso, están en `docs/BIBLIOGRAFIA.md` y `docs/FUENTES_DE_DATOS.md` del
repositorio; el respaldo textual de cada valor de las series curadas, en
`datos_curados/*_notas.md`.

---

*Informe generado por el proyecto*
[agente-politicas-sociales](https://github.com/testa10/agente-politicas-sociales).
"""),
]
