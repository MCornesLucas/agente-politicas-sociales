"""Configuración de los microdatos de la ECH: rutas, archivos y columnas.

Los nombres de columna (HOGARES_COLUMNS, PERSONAS_COLUMNS y sus variantes
_CSV) reflejan los códigos de variable de los archivos oficiales del INE,
verificados contra los diccionarios de datos publicados en el catálogo
ANDA ("Diccionario ECH 2024.pdf", ficha URY-INE-ECH-2024-v02) y contra
los archivos reales descargados. Antes de usar datos de un año nuevo hay
que verificar que esos códigos sigan existiendo y con el mismo
significado; si algo cambió, se actualiza este archivo y se documenta en
docs/METODOLOGIA.md.

Cada año de microdatos vive en su propia subcarpeta:
`data/ech_microdatos/{año}/` (por regla del proyecto los microdatos nunca
se versionan — ver CLAUDE.md).
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Microdatos crudos de la ECH, separados de data/ech/ (que guarda los
# extractos 0-17 que produce extraer_ech_infancia.py a partir de estos).
DATA_DIR = PROJECT_ROOT / "data" / "ech_microdatos"


# No hay ninguna constante "archivo de Hogares por defecto" a propósito:
# desde que el INE pasó al CSV combinado (2023 en adelante), el único año
# con .sav es 2019, y cualquier resolución automática "al más reciente"
# terminaría cargando un año viejo en silencio, sin ningún error — en un
# proyecto donde la fidelidad estadística es lo innegociable. El año se
# elige siempre explícito: `hogares_csv_file(anio)` para 2023+, o los
# `H_*.sav`/`P_*.sav` de `data/ech_microdatos/{año}/` para 2019.


# Columnas relevantes de la base de Hogares (H, formato .sav de 2019) y su
# nombre legible.
HOGARES_COLUMNS = {
    "numero": "id_hogar",
    "nomdpto": "departamento",
    "nombarrio": "barrio",
    "estred13": "estrato_tipo",  # estrato socioeconómico 1 (bajo) a 5 (alto)
    "d25": "total_personas",
    "d21_16": "tiene_internet",       # 1=Sí/2=No/99=Sin dato
    "d21_16_1": "internet_fija",
    "d21_16_2": "internet_movil",
    "d21_15": "tiene_pc",
    "d21_21": "tiene_streaming",
    "pobre06": "pobre",               # 0=No pobre, 1=Pobre
    "indigente06": "indigente",       # 0=No indigente, 1=Indigente
    "YSVL": "ingreso_hogar",          # ingreso del hogar sin valor locativo
    "ht3": "menores_14",
    "ht5": "ocupados_hogar",
    "d9": "cantidad_habitaciones",         # excluye baño y cocina (definición CEPAL de "cuarto")
    "d21_15_5": "tiene_tablet_ibirapita",  # 1=Sí/2=No/99=Sin dato
    # Ponderador anual de expansión muestral (idéntico para todas las
    # personas de un mismo hogar, verificado contra los datos reales). Toda
    # estadística que se calcule sobre estos datos se pondera, nunca
    # proporción simple (docs/METODOLOGIA.md, sección 2).
    "pesoano": "ponderador_hogar",
}

# Variables de estado estructural de la vivienda (todas 1=Sí/2=No/99=Sin dato).
CONDICIONES_VIVIENDA_COLUMNS = {
    "c5_1": "humedad_techos",
    "c5_2": "goteras",
    "c5_3": "muros_agrietados",
    "c5_4": "puertas_ventanas_deterioradas",
    "c5_5": "grietas_pisos",
    "c5_6": "caida_revoque",
    "c5_7": "cielorraso_desprendido",
    "c5_8": "poca_luz_solar",
    "c5_9": "escasa_ventilacion",
    "c5_10": "se_inunda",
    "c5_11": "peligro_derrumbe",
    "c5_12": "humedad_cimientos",
}
HOGARES_COLUMNS.update(CONDICIONES_VIVIENDA_COLUMNS)

# Columnas relevantes de la base de Personas (P, formato .sav de 2019).
PERSONAS_COLUMNS = {
    "numero": "id_hogar",
    "nper": "id_persona",
    "e26": "sexo",
    "e27": "edad",
    "PT1": "ingresos_personales",
    "pobpcoac": "condicion_actividad_cod",
    "e30": "parentesco_jefe",        # relación de parentesco con el jefe/a de hogar
    # OJO: "pesoano" (ponderador) a propósito NO se mapea acá, aunque
    # también está en este archivo con el mismo valor que en Hogares
    # (verificado). Si se mapeara en los dos lados, cualquier merge entre
    # Hogares y Personas por id_hogar duplicaría la columna como
    # "ponderador_hogar_x"/"_y". El ponderador viaja siempre desde el lado
    # de Hogares y llega a las tablas de personas vía merge.
}

# ============================================================================
# Hogares/Personas a partir de un único CSV combinado (formato usado desde
# 2024 en adelante: el INE dejó de publicar H_....sav y P_....sav por
# separado y pasó a publicar un solo archivo ECH_{año}.csv, una fila por
# persona, con las columnas de hogar repetidas para cada persona del mismo
# hogar). Los códigos de columna también cambiaron de nombre en varios
# casos, y algunas variables se discontinuaron — verificado contra el
# diccionario oficial "Diccionario ECH 2024.pdf":
#
# - id_hogar viene en "ID" (antes "numero"); departamento en "nom_dpto"
#   (antes "nomdpto"); estrato en "ESTRED13" (antes "estred13"); indigencia
#   en "indig06" (antes "indigente06"); menores de 14 en "d24" (antes "ht3").
# - "barrio" en este formato es un CÓDIGO NUMÉRICO, no el nombre del barrio.
# - "ocupados_hogar" (antes "ht5") ya no viene precalculado a nivel de
#   hogar: se calcula aparte contando, por hogar, cuántas personas tienen
#   condicion_actividad_cod == 2 (Ocupados) — ver
#   data_loader.load_hogares_personas_csv().
HOGARES_COLUMNS_CSV = {
    "ID": "id_hogar",
    "nom_dpto": "departamento",
    "barrio": "barrio",
    "ESTRED13": "estrato_tipo",
    "d25": "total_personas",
    "d21_16": "tiene_internet",
    "d21_16_1": "internet_fija",
    "d21_16_2": "internet_movil",
    "d21_15": "tiene_pc",
    "d21_21": "tiene_streaming",
    "pobre06": "pobre",
    "indig06": "indigente",
    "YSVL": "ingreso_hogar",
    "d24": "menores_14",
    "d9": "cantidad_habitaciones",
    "d21_15_5": "tiene_tablet_ibirapita",
    "W_ANO": "ponderador_hogar",  # mismo ponderador que "pesoano" en 2019, solo cambia el nombre
    # El INE reemplazó la metodología de pobreza/ingreso (canasta de 2006
    # por la de 2017) — verificado contra los datos reales: 2025 ya no trae
    # pobre06/indig06/YSVL, solo pobre17/indig17/YDA_SVL. 2024 es un año de
    # transición: trae LAS DOS a la vez. Ante esa situación se prefiere la
    # metodología nueva (canasta 2017) también para 2024, porque da
    # comparabilidad hacia adelante entre 2024 y 2025; 2019 y 2023 quedan
    # con la metodología vieja, documentado como diferencia metodológica
    # (docs/METODOLOGIA.md). pobre17/indig17 no son una inferencia propia —
    # son la clasificación de pobreza que ya calcula el INE con la
    # metodología vigente, solo cambió el nombre de la columna. Ver
    # PREFERENCIA_METODOLOGIA_HOGARES y data_loader.load_hogares_personas_csv.
    "pobre17": "pobre",
    "indig17": "indigente",
    "YDA_SVL": "ingreso_hogar",
}

# Cuando un archivo trae las dos variantes de una misma columna a la vez
# (año de transición — pasó de verdad con 2024, ver la nota de arriba),
# `data_loader.load_hogares_personas_csv` descarta la columna vieja (clave)
# y se queda con la nueva (valor) — decisión metodológica explícita, no
# tomada en silencio por el código.
PREFERENCIA_METODOLOGIA_HOGARES = {
    "pobre06": "pobre17",
    "indig06": "indig17",
    "YSVL": "YDA_SVL",
}

# Solo las 4 preguntas de "problemas de la vivienda" (módulo C5) que el INE
# siguió relevando durante todo 2024 — las otras 8 se discontinuaron a
# partir del segundo semestre (marcadas con (*) en el diccionario oficial),
# así que no hay dato completo de año para ellas. Se reutilizan los mismos
# nombres legibles que CONDICIONES_VIVIENDA_COLUMNS.
CONDICIONES_VIVIENDA_COLUMNS_CSV = {
    "c5_2": "goteras",
    "c5_10": "se_inunda",
    "c5_11": "peligro_derrumbe",
    "c5_12": "humedad_cimientos",
}
HOGARES_COLUMNS_CSV.update(CONDICIONES_VIVIENDA_COLUMNS_CSV)

PERSONAS_COLUMNS_CSV = {
    "ID": "id_hogar",
    "nper": "id_persona",
    "e26": "sexo",
    "e27": "edad",
    "PT1": "ingresos_personales",
    "POBPCOAC": "condicion_actividad_cod",
    "e30": "parentesco_jefe",
    # Mismo motivo que en PERSONAS_COLUMNS: W_ANO a propósito no se mapea
    # acá, para no duplicar la columna al mergear con el lado de Hogares.
}


def hogares_csv_file(anio: int | str) -> Path:
    """Ruta al archivo combinado de Hogares/Personas de un año.

    El nombre cambió entre años: hasta 2024 es exactamente `ECH_{año}.csv`;
    desde 2025 el INE lo publica como `ECH_{año}_implantacion.csv` —
    verificado contra los archivos reales, no una suposición. El archivo
    real de 2023 vino además con el orden de palabras invertido
    (`ECH_implantacion_2023.csv`), mismo tipo de inconsistencia de nombres
    del INE que obliga a `empleo_files()` a reconocer dos patrones. Se
    prueban los patrones "implantación" primero y se usa el que exista en
    disco; si ninguno existe, se cae al patrón simple (exista o no
    todavía) — así un año recién creado, sin descargar, sigue mostrando un
    nombre de archivo esperado en vez de romper. `datos_disponibles()`
    reutiliza esta misma función como fuente única de verdad.
    """
    carpeta = DATA_DIR / str(anio)
    for nombre in (f"ECH_{anio}_implantacion.csv", f"ECH_implantacion_{anio}.csv"):
        candidato = carpeta / nombre
        if candidato.exists():
            return candidato
    return carpeta / f"ECH_{anio}.csv"


# Corrige un problema de codificación presente en las etiquetas de barrio
# del archivo .sav original: la 'ñ' puede quedar guardada como '¦' (U+00A6).
MOJIBAKE_FIX = {"¦": "ñ"}

# ============================================================================
# FIES (seguridad alimentaria) — solo disponible para algunos años, y solo
# para una submuestra de hogares (no el total). A diferencia de Hogares y
# Personas, viene en CSV, no en .sav.
# ============================================================================


def fies_file(anio: int | str) -> Path:
    """Ruta al archivo FIES de un año (`data/ech_microdatos/{año}/base_FIES_{año}.csv`).
    No tiene resolución automática al "año más reciente" a propósito: FIES
    no existe para todos los años, así que el año siempre se pasa explícito.
    """
    carpeta = DATA_DIR / str(anio)
    candidatos = sorted(carpeta.glob(f"base_FIES_{anio}.csv"))
    return candidatos[0] if candidatos else carpeta / f"base_FIES_{anio}.csv"


def datos_disponibles(anio: int | str) -> dict:
    """Qué tipos de datos existen para un año determinado. "empleo"
    requiere los 12 archivos mensuales completos, no unos pocos — con menos
    de 12 no se puede promediar el año correctamente.
    """
    carpeta = DATA_DIR / str(anio)
    return {
        "hogares": bool(list(carpeta.glob("H_*.sav")) or hogares_csv_file(anio).exists()),
        "fies": fies_file(anio).exists(),
        "empleo": all(archivo.exists() for archivo in empleo_files(anio)),
        "seguridad": victimizacion_file(anio).exists(),
    }


# Solo las columnas cuyo significado se verificó contra el diccionario de
# datos oficial del INE (catálogo ANDA, ficha URY-INE-ECH-2024-v02,
# archivo base_FIES_2024).
FIES_COLUMNS = {
    "ID": "id_hogar",
    "region": "region_cod",
    "quintiles": "quintil_ingreso",
    "menores18": "tiene_menores_18",   # 0/1: hogar con menores de 18 años
    "menores6": "tiene_menores_6",     # 0/1: hogar con niños de 0 a 5 años
    "prob.mod.h": "prob_inseguridad_moderada",
    "prob.sev.h": "prob_inseguridad_severa",
    "w": "ponderador_fies",
}

# ============================================================================
# Empleo (ECH_seguimiento) — panel rotativo mensual, no un corte anual como
# Hogares. Cada hogar permanece en el panel 6 meses seguidos, así que las
# métricas se calculan mes a mes (ponderadas por `w`) y se promedian entre
# los 12 meses — nunca juntando los 12 CSV en un solo pool antes de
# ponderar (docs/METODOLOGIA.md).
# ============================================================================


def empleo_files(anio: int | str) -> list[Path]:
    """Los 12 archivos mensuales de un año determinado, ordenados de enero
    a diciembre. `anio` es el año completo (ej. 2024).

    El patrón de nombre cambió entre años: hasta 2024 el INE usa los
    últimos dos dígitos del año (`ECH_01_24.csv`); desde 2025 usa el año
    completo (`ECH_01_2025.csv`) — verificado contra los archivos reales.
    Se prueba el patrón largo primero y se usa si existe en disco; si no,
    se cae al patrón corto (exista o no todavía).
    """
    carpeta = DATA_DIR / str(anio)
    sufijo_anio = str(anio)[-2:]
    archivos = []
    for mes in range(1, 13):
        patron_largo = carpeta / f"ECH_{mes:02d}_{anio}.csv"
        patron_corto = carpeta / f"ECH_{mes:02d}_{sufijo_anio}.csv"
        archivos.append(patron_largo if patron_largo.exists() else patron_corto)
    return archivos


# Solo las columnas cuyo significado se verificó contra el diccionario de
# datos oficial del INE (archivo ECH_seguimiento_2024) y/o contra los
# datos reales.
EMPLEO_COLUMNS = {
    "ID": "id_hogar",
    "nper": "id_persona",
    "mes": "mes",
    "nom_dpto": "departamento",
    "e26": "sexo",
    "e27": "edad",
    "POBPCOAC": "condicion_actividad_cod",
    "SIT_OCUP": "situacion_ocupacional",     # ya viene con etiquetas de texto
    "SECTOR_F": "sector_formalidad",         # ya viene con etiquetas de texto
    "NIV_EDU": "nivel_educativo",            # ya viene con etiquetas de texto
    "INFORMAL": "es_informal",               # 0/1 — solo válido si condicion_actividad == "Ocupados"
    "SUBEMPLEO": "es_subempleo",             # 0/1 — solo válido si condicion_actividad == "Ocupados"
    "W": "ponderador_empleo",                # ponderador MENSUAL, no anual
    # INFORMAL, SECTOR_F y SIT_OCUP desaparecieron de los archivos
    # mensuales desde 2025 (verificado contra los datos reales). f82
    # ("aporte a fondo de pensión") sigue estando, y es la variable que usa
    # `employment_restrictions()` del paquete oficial de R para la ECH
    # (autoría conjunta INE, github.com/calcita/ech, archivo
    # R/employment.R) para calcular informalidad — el criterio estándar en
    # la región: no aportar a la seguridad social = informal.
    "f82": "aporta_seguridad_social",        # 1=Sí aporta, 2=No aporta, 0=no aplica
}

# ============================================================================
# Seguridad y Victimización (ECH_VICTIMIZACION_S2). No es un panel rotativo
# mensual — es un corte del segundo semestre, se pondera directo por W_SEM
# sin promediar meses. El archivo no trae departamento propio: hay que
# cruzarlo por ID contra los meses de julio-diciembre del mismo año (ver
# data_loader.load_victimizacion).
# ============================================================================


def victimizacion_file(anio: int | str) -> Path:
    """Ruta al archivo de victimización de un año determinado
    (`data/ech_microdatos/{año}/ECH_VICTIMIZACION_S2_{año}.csv`)."""
    carpeta = DATA_DIR / str(anio)
    candidatos = sorted(carpeta.glob(f"ECH_VICTIMIZACION_S2_{anio}.csv"))
    return candidatos[0] if candidatos else carpeta / f"ECH_VICTIMIZACION_S2_{anio}.csv"


VICTIMIZACION_COLUMNS = {
    "ID": "id_hogar",
    "nper": "id_persona",
    "e26": "sexo",
    "v3": "v3", "v3_4": "v3_4", "v3_6": "v3_6", "v3_8": "v3_8",
    "v4": "v4", "v4_4": "v4_4", "v4_6": "v4_6", "v4_8": "v4_8",
    "v5": "v5", "v5_4": "v5_4", "v5_6": "v5_6", "v5_8": "v5_8",
    "v6": "v6", "v6_2": "v6_2", "v6_4": "v6_4",
    "v7": "v7", "v7_4": "v7_4", "v7_6": "v7_6",
    "W_SEM": "ponderador_victimizacion",
}
