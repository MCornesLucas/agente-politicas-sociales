"""Cruce territorial INAU × ECH por departamento (cruce 1 del catálogo).

Tasa de NNA en protección especial cada 1.000 NNA por departamento
(numerador: indicador departamental 1 de INAU, segundo semestre de cada
año; denominador: población 0-17 ponderada de la ECH del mismo año y
departamento) contra pobreza infantil y hacinamiento del mismo
departamento (resultados/ech/metricas_ech_0a17.csv).

Reglas aplicadas (docs/METODOLOGIA.md):

- Mismo nivel de agregación en ambos lados del cruce (departamento):
  las conclusiones se redactan a nivel departamento, nunca sobre
  individuos (sin falacia ecológica).
- Lenguaje observacional: asociación, nunca causa.
- Asociación medida con correlación de rangos de Spearman (n = 19
  departamentos): robusta a valores extremos y a no linealidad
  monótona; se reporta para 2024 y 2025 como control de estabilidad.
- Denominador ECH: estimación muestral expandida — los departamentos
  chicos tienen más error de muestreo; el n muestral de cada estimación
  queda en el CSV de salida.
- Carencias de vivienda: sin apertura departamental en los resultados
  curados actuales — queda documentado como extensión pendiente.

Salida: resultados/cruces/cruce_inau_ech_departamental.csv
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

PROYECTO = Path(__file__).resolve().parent.parent
CURADOS = PROYECTO / "datos_curados"
SALIDA = PROYECTO / "resultados" / "cruces"
ANIOS = [2024, 2025]


def clave(nombre: str) -> str:
    """Nombre de departamento normalizado (sin acentos, mayúsculas)."""
    s = unicodedata.normalize("NFKD", nombre)
    return "".join(c for c in s if not unicodedata.combining(c)).upper().strip()


def poblacion_ech(anio: int) -> pd.DataFrame:
    p = pd.read_csv(PROYECTO / "data" / "ech" / str(anio) / "personas_0a17.csv",
                    usecols=["departamento", "ponderador_hogar"])
    g = p.groupby("departamento").agg(
        poblacion_0a17_ech=("ponderador_hogar", "sum"),
        n_muestral_poblacion=("ponderador_hogar", "size"),
    ).reset_index()
    g["clave"] = g["departamento"].map(clave)
    return g[["clave", "poblacion_0a17_ech", "n_muestral_poblacion"]]


def metrica_ech(df: pd.DataFrame, metrica: str, anio: int, nombre: str) -> pd.DataFrame:
    s = df[(df["metrica"] == metrica) & (df["anio"] == anio) &
           (df["categoria"].str.startswith("departamento="))].copy()
    s["clave"] = s["categoria"].str.replace("departamento=", "", regex=False).map(clave)
    s = s.groupby("clave").first().reset_index()  # colapsa variantes de acentos
    return s[["clave", "valor", "n_muestral"]].rename(
        columns={"valor": nombre, "n_muestral": f"n_muestral_{nombre}"})


def main() -> None:
    inau = pd.read_csv(CURADOS / "inau_spe_departamental_totales.csv")
    echm = pd.read_csv(PROYECTO / "resultados" / "ech" / "metricas_ech_0a17.csv")

    filas = []
    for anio in ANIOS:
        num = inau[(inau["indicador_codigo"] == 1) & (inau["periodo"] == f"{anio}-S2")].copy()
        num["clave"] = num["departamento"].map(clave)
        base = num[["clave", "departamento", "valor"]].rename(columns={"valor": "nna_spe_s2"})
        base = base.merge(poblacion_ech(anio), on="clave", validate="1:1")
        base = base.merge(metrica_ech(echm, "pobreza_0a17", anio, "pobreza_0a17_pct"),
                          on="clave", validate="1:1")
        base = base.merge(metrica_ech(echm, "hacinamiento_hogares_nna", anio, "hacinamiento_pct"),
                          on="clave", validate="1:1")
        base["anio"] = anio
        base["tasa_spe_por_mil"] = base["nna_spe_s2"] / base["poblacion_0a17_ech"] * 1000
        filas.append(base)

    todo = pd.concat(filas, ignore_index=True)
    if todo.groupby("anio").size().nunique() != 1 or len(todo) != len(ANIOS) * 19:
        raise ValueError("El cruce no cerró con los 19 departamentos en todos los años")

    SALIDA.mkdir(parents=True, exist_ok=True)
    columnas = ["anio", "departamento", "nna_spe_s2", "poblacion_0a17_ech",
                "n_muestral_poblacion", "tasa_spe_por_mil", "pobreza_0a17_pct",
                "n_muestral_pobreza_0a17_pct", "hacinamiento_pct",
                "n_muestral_hacinamiento_pct"]
    todo = todo[columnas].sort_values(["anio", "departamento"])
    todo["tasa_spe_por_mil"] = todo["tasa_spe_por_mil"].round(2)
    todo["poblacion_0a17_ech"] = todo["poblacion_0a17_ech"].round()
    todo.to_csv(SALIDA / "cruce_inau_ech_departamental.csv", index=False, encoding="utf-8")

    print("Asociaciones (Spearman, n=19 departamentos):")
    for anio in ANIOS:
        t = todo[todo["anio"] == anio]
        for variable in ["pobreza_0a17_pct", "hacinamiento_pct"]:
            rho, pval = spearmanr(t["tasa_spe_por_mil"], t[variable])
            print(f"  {anio} · tasa SPE vs {variable}: rho={rho:+.2f} (p={pval:.3f})")
        extremos = t.nlargest(3, "tasa_spe_por_mil")[["departamento", "tasa_spe_por_mil"]]
        print(f"  {anio} · tasas más altas: " +
              ", ".join(f"{d} {v:.1f}" for d, v in extremos.itertuples(index=False)))


if __name__ == "__main__":
    main()
