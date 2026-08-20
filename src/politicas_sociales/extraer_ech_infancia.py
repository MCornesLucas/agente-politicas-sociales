"""Extrae de la ECH todo lo referido a infancia y adolescencia (0-17 años).

Recorre cada año de microdatos disponible en `data/ech_microdatos/` y
exporta, a `data/ech/<año>/`, los bloques filtrados al universo del
proyecto (0-17 años, definición de la CDN — ver
docs/CLASIFICACION_DE_EDADES.md):

- personas_0a17.csv          personas de 0 a 17, con las clasificaciones
                             de edad de cada organismo como columnas
                             derivadas (ley 17.823, tramos SIPIAV, OMS)
                             y el ponderador anual del hogar.
- hogares_con_nna.csv        hogares con al menos una persona de 0-17
                             (vivienda, pobreza, brecha digital,
                             territorio), con conteos de NNA por tramo.
- empleo_14a17.csv           filas del panel mensual de Empleo con edad
                             14-17 (trabajo adolescente; el módulo no
                             releva menores de 14), con mes y ponderador
                             mensual.
- victimizacion_hogares_con_nna.csv
                             respuestas del módulo de victimización de
                             hogares donde viven NNA (el módulo lo
                             responden adultos; el dato es del hogar).
- fies_hogares_con_menores.csv
                             hogares FIES con menores de 18 (la base ya
                             trae el marcador oficial del INE).

Los loaders (politicas_sociales.ech) traen las correcciones de encoding
y las decisiones metodológicas verificadas contra los datos reales
(canasta 2017 vs. 2006, columnas discontinuadas, nombres de archivo
cambiantes del INE).

Regla de rigor aplicable a todo lo exportado: los CSV conservan los
ponderadores — cualquier estadística que se calcule después se pondera,
nunca proporción simple (docs/METODOLOGIA.md, sección 2).
"""

from __future__ import annotations

import pandas as pd

from politicas_sociales import config as config_infancia
from politicas_sociales.ech import config, data_loader

DESTINO = config_infancia.DATA_DIR / "ech"

EDAD_MAX = 17  # universo 0-17: "niño" según la CDN es toda persona menor de 18


def clasificar_edades(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega las clasificaciones de edad de cada organismo como columnas.

    No se fija un rango único (docs/CLASIFICACION_DE_EDADES.md): se
    exporta `edad` cruda más una columna por clasificación, para que
    cualquier análisis posterior corte según la fuente que cruce.
    """
    df = df.copy()
    df["tramo_sipiav"] = pd.cut(
        df["edad"], bins=[-1, 5, 12, 17], labels=["0 a 5", "6 a 12", "13 a 17"]
    )
    # Ley 17.823 (art. 1): niño hasta los 13, adolescente de 13 a 18.
    df["clasificacion_ley_17823"] = pd.cut(
        df["edad"], bins=[-1, 12, 17], labels=["Niño/a", "Adolescente"]
    )
    # OMS/UNICEF: adolescencia 10-19 (acá cortada al universo 0-17).
    df["es_adolescente_oms"] = df["edad"].between(10, EDAD_MAX)
    # Universo ENSANNA/OIT para trabajo infantil: 5 a 17.
    df["en_universo_ensanna"] = df["edad"].between(5, EDAD_MAX)
    return df


def cargar_hogares_personas(anio: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hogares y Personas del año, en el formato que exista (.sav o CSV)."""
    carpeta = config.DATA_DIR / str(anio)
    savs_h = sorted(carpeta.glob("H_*.sav"))
    if savs_h:
        hogares = data_loader.load_hogares(savs_h[0])
        personas = data_loader.load_personas(sorted(carpeta.glob("P_*.sav"))[0])
        return hogares, personas
    return data_loader.load_hogares_personas_csv(anio)


def extraer_anio(anio: int) -> list[str]:
    disponibles = config.datos_disponibles(anio)
    if not disponibles["hogares"]:
        return []
    destino = DESTINO / str(anio)
    destino.mkdir(parents=True, exist_ok=True)
    resumen = []

    hogares, personas = cargar_hogares_personas(anio)

    # --- Personas 0-17, con ponderador del hogar y contexto del hogar ---
    nna = clasificar_edades(personas[personas["edad"] <= EDAD_MAX])
    contexto_hogar = [
        c for c in ["id_hogar", "departamento", "estrato_tipo", "pobre",
                    "indigente", "ponderador_hogar"] if c in hogares.columns
    ]
    nna = nna.merge(hogares[contexto_hogar], on="id_hogar", how="left")
    nna.to_csv(destino / "personas_0a17.csv", index=False, encoding="utf-8")

    total_pond = personas.merge(
        hogares[["id_hogar", "ponderador_hogar"]], on="id_hogar", how="left"
    )
    pct = (
        nna["ponderador_hogar"].sum() / total_pond["ponderador_hogar"].sum() * 100
    )
    resumen.append(
        f"personas_0a17: {len(nna):,} filas ({pct:.1f}% ponderado de la población)"
    )

    # --- Hogares con al menos un NNA, con conteos por tramo ---
    conteos = (
        nna.assign(uno=1)
        .pivot_table(
            index="id_hogar", columns="tramo_sipiav", values="uno",
            aggfunc="sum", fill_value=0, observed=False,
        )
        .rename(columns={"0 a 5": "nna_0a5", "6 a 12": "nna_6a12", "13 a 17": "nna_13a17"})
    )
    conteos["total_nna"] = conteos.sum(axis=1)
    hogares_nna = hogares.merge(conteos, on="id_hogar", how="inner")
    hogares_nna.to_csv(destino / "hogares_con_nna.csv", index=False, encoding="utf-8")
    pct_h = (
        hogares_nna["ponderador_hogar"].sum() / hogares["ponderador_hogar"].sum() * 100
    )
    resumen.append(
        f"hogares_con_nna: {len(hogares_nna):,} de {len(hogares):,} hogares "
        f"({pct_h:.1f}% ponderado)"
    )

    # --- Empleo: panel mensual, adolescentes 14-17 ---
    if disponibles["empleo"]:
        empleo = data_loader.load_empleo(anio)
        adolescentes = clasificar_edades(empleo[empleo["edad"] <= EDAD_MAX])
        adolescentes.to_csv(destino / "empleo_14a17.csv", index=False, encoding="utf-8")
        edades = adolescentes["edad"]
        resumen.append(
            f"empleo_14a17: {len(adolescentes):,} filas-mes "
            f"(edades {int(edades.min())}-{int(edades.max())})"
        )

    # --- Victimización: hogares donde viven NNA ---
    if disponibles["seguridad"]:
        victimizacion = data_loader.load_victimizacion(anio)
        con_nna = victimizacion[victimizacion["id_hogar"].isin(set(nna["id_hogar"]))]
        con_nna = con_nna.merge(conteos, on="id_hogar", how="left")
        con_nna.to_csv(
            destino / "victimizacion_hogares_con_nna.csv", index=False, encoding="utf-8"
        )
        resumen.append(
            f"victimizacion_hogares_con_nna: {len(con_nna):,} de "
            f"{len(victimizacion):,} filas"
        )

    # --- FIES: hogares con menores de 18 (marcador oficial de la base) ---
    if disponibles["fies"]:
        fies = data_loader.load_fies(config.fies_file(anio))
        fies_nna = fies[fies["tiene_menores_18"] == 1]
        fies_nna.to_csv(
            destino / "fies_hogares_con_menores.csv", index=False, encoding="utf-8"
        )
        resumen.append(
            f"fies_hogares_con_menores: {len(fies_nna):,} de {len(fies):,} hogares"
        )

    return resumen


def main() -> None:
    anios = sorted(
        int(p.name) for p in config.DATA_DIR.iterdir()
        if p.is_dir() and p.name.isdigit()
    )
    print(f"Años con carpeta de microdatos de la ECH: {anios}\n")
    for anio in anios:
        lineas = extraer_anio(anio)
        if not lineas:
            print(f"{anio}: sin base de Hogares/Personas — se omite")
            continue
        print(f"{anio}:")
        for linea in lineas:
            print(f"  {linea}")
    print(f"\nExportado a {DESTINO}")


if __name__ == "__main__":
    main()
