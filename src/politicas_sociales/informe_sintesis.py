"""Síntesis por unidad: el fragmento de resumen y de conclusión de cada
métrica, proyección y cruce del informe.

Idea del dueño del proyecto (2026-08-20): cada métrica es una entidad
completa que también es dueña de lo que el cierre del informe dice de
ella. El Resumen analítico y las Conclusiones se **arman** desde estos
fragmentos con las unidades presentes en la edición — así las secciones
finales no pueden afirmar nada que la edición no muestre, por
construcción. Y sin duplicación (regla explícita del dueño): los
fragmentos NO se imprimen en la sección de la métrica, que conserva sus
cinco partes de siempre; solo se materializan una vez, en el cierre.

Los fragmentos reutilizan frases y cifras de las lecturas ya publicadas
del informe; el guardián de cifras valida las secciones armadas contra
los outputs y los CSV versionados, como a todo el cierre. Los tests
mantienen los mapas alineados con las unidades reales: toda unidad tiene
su fragmento de resumen (obligatorio); el de conclusión es opcional —
solo las unidades con algo conclusivo que aportar lo llevan.

La métrica a medida entra por el mismo mecanismo: el agente del flujo
guiado escribe sus fragmentos rotulados con el título real de la métrica
y los inserta en las secciones armadas (ver
`.claude/agents/politicas-sociales.md`, paso 1d.3).
"""

from __future__ import annotations

from politicas_sociales.informe_base import md

# Etiqueta del párrafo de resumen de cada bloque, en el orden del informe.
ETIQUETAS_BLOQUE = {
    "tema_1": "Violencia (SIPIAV)",
    "tema_2": "Explotación sexual (CONAPEES/Fiscalía)",
    "tema_3": "Trabajo infantil (ENSANNA/ECH)",
    "tema_4": "Protección especial (INAU)",
    "tema_5": "Pobreza y entorno (ECH)",
    "tema_6": "Primera infancia (ENDIS)",
    "cruces": "Cruces entre fuentes (contra la ECH)",
}

# Unidad → bloque, en el orden del informe. Un test lo mantiene alineado
# con la partición real de las celdas.
BLOQUE_DE_UNIDAD = {
    **{f"metrica_{n}": "tema_1" for n in range(1, 12)},
    "proyeccion_p1": "tema_1", "proyeccion_p2": "tema_1", "proyeccion_p5": "tema_1",
    **{f"metrica_{n}": "tema_2" for n in range(12, 16)},
    **{f"metrica_{n}": "tema_3" for n in range(16, 20)},
    **{f"metrica_{n}": "tema_4" for n in range(20, 31)},
    "proyeccion_p3": "tema_4", "proyeccion_p4": "tema_4",
    **{f"metrica_{n}": "tema_5" for n in range(31, 37)},
    "metrica_37": "tema_6",
    **{f"cruce_{n}": "cruces" for n in range(1, 5)},
}

# Fragmento de resumen de cada unidad: una o dos frases con las cifras de
# su propia lectura (ya verificadas contra los archivos del repositorio).
RESUMEN = {
    "metrica_1": "La respuesta del sistema se multiplicó por 7 en doce años (1.319 → 9.178 situaciones).",
    "metrica_2": "Entre 54% y 56% de las situaciones corresponde a niñas y adolescentes mujeres, estable en toda la serie.",
    "metrica_3": "Las edades escolares concentran el registro (72 de cada 100 situaciones entre los 6 y los 17 años en 2025).",
    "metrica_4": "El maltrato emocional encabeza los tipos registrados en toda la serie, con quiebres de clasificación (2020 y 2024) marcados sin interpolar.",
    "metrica_5": "Las violencias sexuales tienen patrón propio: 76% niñas y adolescentes mujeres, 51% concentrado en 13-17 años.",
    "metrica_6": "La mayoría de las situaciones ya eran recurrentes al ser detectadas, en toda la serie comparable.",
    "metrica_7": "La detección sigue siendo tardía: en la serie comparable, alrededor de 9 de cada 10 situaciones ya eran crónicas.",
    "metrica_8": "Alrededor de 9 de cada 10 personas agresoras integran el entorno familiar o de convivencia del NNA.",
    "metrica_9": "Solo alrededor de 4 de cada 10 NNA atendidos visualiza la violencia que sufre.",
    "metrica_10": "La inclusión de la familia en la intervención cayó de 82% a 58% en una década.",
    "metrica_11": "La cobertura territorial llegó a 36 Comités de Recepción Local, con señales de acercarse a su techo.",
    "proyeccion_p1": "La proyección de situaciones publicada para 2025 quedó validada por el dato real.",
    "proyeccion_p2": "De continuar la tendencia, hacia 2027 la familia se incluiría en aproximadamente la mitad de las intervenciones.",
    "proyeccion_p5": "De seguir el ritmo de aperturas, el sistema sumaría unos tres comités hacia 2028.",
    "metrica_12": "Entre 240 y 494 situaciones atendidas por año (2018-2021), sin serie oficial desde 2022.",
    "metrica_13": "86% de las víctimas identificadas son niñas y adolescentes mujeres.",
    "metrica_14": "Desde 2024 la explotación sexual perdió su categoría propia en el registro del SIPIAV.",
    "metrica_15": "Más de 2.000 actuaciones anuales de la Fiscalía por delitos sexuales con víctima NNA.",
    "metrica_16": "6,8% de los NNA de 5 a 17 (40.200) está en situación de trabajo infantil, con gradientes por edad, región y nivel socioeconómico.",
    "metrica_17": "El trabajo no remunerado de servicios ya muestra división sexual (niñas 2,8% frente a varones 1,1%).",
    "metrica_18": "La comparación honesta con 2010 es un rango: el trabajo infantil habría descendido desde entre 9,9% y 13,4% hasta 6,8%.",
    "metrica_19": "El trabajo adolescente que existe es casi todo informal (82-93% de los ocupados de 14-17).",
    "metrica_20": "El sistema creció hasta 2023 y se amesetó (~8.000 atendidos; ~7.000 de 0-17).",
    "metrica_21": "La desinternación avanza: de 50,9% a 62,7% de los NNA del sistema en contexto familiar.",
    "metrica_22": "La demanda nueva domina la puerta de entrada: entre 21% y 26% de los atendidos ingresa por primera vez cada año.",
    "metrica_23": "El sistema egresa cada año a alrededor de un cuarto de su población atendida.",
    "metrica_24": "Entre 25% y 32% de los atendidos pasa cada año de residencia a un entorno familiar.",
    "metrica_25": "Solo entre 15% y 18% de los NNA con condición de adoptabilidad pasa cada año a seguimiento de tenencia.",
    "metrica_26": "56,9% de los casos no tiene registro del contacto familiar: la calidad del registro es el límite del dato.",
    "metrica_27": "Aun dentro del sistema, cerca de 1 de cada 10 NNA de 6 a 17 no está inscripto en educación formal.",
    "metrica_28": "Casi 4 de cada 10 NNA del sistema no tienen los controles médicos al día, y más de 2 de cada 10, las vacunas.",
    "metrica_29": "El acogimiento familiar se apoya sobre todo en la red del propio NNA (familia extensa y por afinidad).",
    "metrica_30": "La fotografía de abril de 2025 muestra que la mayoría de los NNA acompañados vive en entornos familiares.",
    "proyeccion_p3": "De persistir el ritmo, la desinternación llegaría a 66,4% de NNA en contexto familiar hacia 2027.",
    "proyeccion_p4": "La tasa de NNA en protección (9,4 por mil) sube por pura demografía: la población de 0 a 17 cae 2,3% por año.",
    "metrica_31": "27,5% de los NNA en hogares pobres (2025, canasta 2017), con la primera infancia como el grupo más afectado.",
    "metrica_32": "El hacinamiento afecta a entre 3,7% y 4,9% de los hogares con NNA según el año.",
    "metrica_33": "Más de un tercio de los hogares con NNA tiene humedades estructurales.",
    "metrica_34": "La brecha digital se cierra en acceso general pero retrocede en internet fija.",
    "metrica_35": "La inseguridad alimentaria mejora pero alcanza al 15,3% de los hogares con menores.",
    "metrica_36": "2,5% de los hogares con NNA declaró haber sufrido al menos un delito en 2024 — serie nueva, relevada desde ese año.",
    "metrica_37": "En el tramo de 0 a 4 años, 66,9% asiste a algún centro de primera infancia y 33,1% no tiene centro registrado (ENDIS 2023, estimaciones ponderadas); la cobertura pasa de 20,9% entre los menores de 1 año a 97,0% entre los 48 y los 59 meses.",
    "cruce_1": "La tasa departamental de protección especial no está asociada a la pobreza infantil ni al hacinamiento: la distribución territorial de la atención parece responder a la oferta institucional más que al mapa de la necesidad.",
    "cruce_2": "La detección de la explotación sexual tampoco sigue el mapa de las carencias: se registra menos donde el hacinamiento es mayor, en las ocho combinaciones de fuente y año.",
    "cruce_3": "El trabajo infantil declarado atraviesa toda la estructura social, con un gradiente mucho más plano que el de la pobreza y la geografía invertida.",
    "cruce_4": "El perfil etario de la atención del SIPIAV no sigue al tramo más pobre: la primera infancia fue históricamente la menos representada, aunque en 2025 se acercó a la paridad.",
}

# Fragmentos de conclusión, en el orden editorial del informe. Solo las
# unidades con algo conclusivo que aportar; cada texto conserva la
# sangría de lista del informe.
CONCLUSIONES = [
    ("metrica_31", """**La pobreza uruguaya está concentrada en la infancia, y dentro de la
   infancia, en sus edades más tempranas.** 27,5% de los NNA en hogares
   pobres (2025) frente a ~17% en la población general, con incidencia
   máxima en la primera infancia. Es el dato más relevante del informe
   para el diseño de políticas (fuente: elaboración propia sobre ECH,
   INE)."""),
    ("metrica_37", """**La oferta de primera infancia cubre casi por completo el año previo a
   la escolarización obligatoria y es minoritaria en el primer año de
   vida.** 97,0% de las niñas y los niños de 48 a 59 meses asiste a algún
   centro frente a 20,9% de los menores de 1 año, con INAU como principal
   prestador en el tramo intermedio y ANEP desde los 36 meses. La cifra
   describe cobertura observada, no demanda insatisfecha: la encuesta no
   releva si las familias sin centro registrado buscaron un cupo (fuente:
   ENDIS 2023, estimaciones ponderadas)."""),
    ("proyeccion_p4", """**El país tiene sistemas de protección en expansión y una infancia en
   contracción.** La respuesta del SIPIAV se multiplicó por 7; el SPE
   del INAU creció hasta amesetarse en ~8.000 atendidos; y la población
   de 0 a 17 cae 2,3% por año. La combinación produce tasas de
   institucionalización crecientes aun sin crecimiento de los sistemas
   (P4) — leer cualquier tasa de infancia sin su denominador demográfico
   induce a error (fuentes: SIPIAV, INAU, INE)."""),
    ("metrica_10", """**La detección de la violencia llega tarde y la intervención pierde a
   la familia.** En la serie comparable, ~9 de cada 10 situaciones
   detectadas ya eran crónicas, solo 4 de cada 10 NNA visualizan la
   violencia que sufren, y la inclusión familiar en la intervención cayó
   24 puntos en una década (82% → 58%), con escenario inercial en ~50%
   hacia 2027 (fuente: SIPIAV)."""),
    ("metrica_5", """**La violencia sexual hacia NNA es adolescente y de género, y perdió
   visibilidad estadística.** 76% de las violencias sexuales afecta a
   niñas y adolescentes mujeres y 51% se concentra en 13-17 años; la
   explotación sexual no tiene serie oficial desde 2022 y desde 2024
   quedó fusionada dentro de «violencias sexuales» (fuentes: SIPIAV,
   CONAPEES/FLACSO)."""),
    ("metrica_1", """**Uruguay no mide la prevalencia de la violencia hacia NNA.** Toda la
   sección de violencia es registro administrativo. La única aproximación existente —
   una encuesta de 2026 de UNICEF con muestra no probabilística, que
   sugiere que cerca de 3 de cada 10 jóvenes vivió violencia sexual
   antes de los 18 — no sustituye una medición oficial con diseño
   muestral: esa es la brecha de información más importante que este
   informe identifica (fuentes: SIPIAV; UNICEF/Equipos 2026, con su
   diseño declarado)."""),
]

# Cierre transversal de las conclusiones: va en TODA edición, sin número
# (los números de la lista dependen de las unidades presentes).
CONCLUSION_TRANSVERSAL = """**Limitaciones declaradas de este informe**: (a) las cifras de
registros administrativos describen la respuesta de los sistemas, no
la prevalencia; (b) las proyecciones son escenarios inerciales con
supuesto explícito — y donde ningún modelo pasó la validación (P4) no
hay proyección; (c) los microdatos de la ENSANNA aún no son públicos
(la sección de trabajo infantil usa el boletín oficial); (d) el SIPIAV no publica
desagregación departamental, lo que limita el análisis territorial de
la violencia; (e) los cuatro cruces entre fuentes comparten tres
límites estructurales — los numeradores administrativos registran
dónde se atiende o actúa (no dónde reside el NNA), las estimaciones
departamentales de la ECH tienen error muestral mayor en los
departamentos chicos, y toda asociación es observacional — además de
las limitaciones propias declaradas en la sección de cada cruce:
escalas socioeconómicas no comparables y sin errores estándar en la
ENSANNA, porcentajes redondeados y renormalizados en el SIPIAV, y
conteos chicos con condiciones fijadas en 2019 en CONAPEES/Fiscalía."""


def celdas_resumen(unidades: list[str] | None = None) -> list:
    """Las celdas del Resumen analítico armadas para la selección: un
    párrafo por bloque presente, compuesto por los fragmentos de sus
    unidades elegidas, en el orden del informe."""
    seleccion = set(BLOQUE_DE_UNIDAD) if unidades is None else set(unidades)
    celdas = [md("\n## Resumen analítico\n")]
    for bloque, etiqueta in ETIQUETAS_BLOQUE.items():
        fragmentos = [RESUMEN[unidad] for unidad, b in BLOQUE_DE_UNIDAD.items()
                      if b == bloque and unidad in seleccion]
        if fragmentos:
            celdas.append(md(f"\n**{etiqueta}.** " + " ".join(fragmentos) + "\n"))
    return celdas


def celdas_conclusiones(unidades: list[str] | None = None) -> list:
    """Las celdas de las Conclusiones armadas para la selección: los
    fragmentos de las unidades elegidas, numerados en el orden editorial,
    más el cierre transversal de limitaciones (siempre)."""
    seleccion = set(BLOQUE_DE_UNIDAD) if unidades is None else set(unidades)
    celdas = [md("\n## Conclusiones\n")]
    numero = 0
    for clave, texto in CONCLUSIONES:
        if clave in seleccion:
            numero += 1
            celdas.append(md(f"\n{numero}. {texto}\n"))
    celdas.append(md("\n" + CONCLUSION_TRANSVERSAL + "\n"))
    return celdas
