"""Cruce CONAPEES/Fiscalía × ECH por departamento (cruce 2 del catálogo).

Situaciones de ESNNA atendidas (CONAPEES, tabla 2 del estudio FLACSO
2023) y actuaciones de la Fiscalía en delitos sexuales con víctima NNA
(FGN/SIPPAU, tabla 8 del mismo estudio), 2018-2021, convertidas a tasa
cada 10.000 NNA por departamento y contrastadas con la pobreza infantil
y el hacinamiento del mismo departamento (ECH). Asociación medida con
correlación de rangos de Spearman (n = 19 departamentos), reportada para
cada año 2018-2021 como control de estabilidad.

Limitaciones que acotan toda lectura (docs/METODOLOGIA.md y
datos_curados/conapees_notas.md):

- **Detección ≠ incidencia.** El propio estudio FLACSO advierte (pp. 46
  y 52) que los departamentos con más actuaciones cada 10.000 NNA no
  necesariamente presentan mayor incidencia, sino posiblemente más
  recursos y equipos locales, y que los datos de explotación sexual son
  de los "más frágiles" por subregistro reconocido.
- **Celdas chicas.** Los conteos departamentales de CONAPEES van de 0
  (Lavalleja 2019) a 59: una situación más o menos mueve la tasa de un
  departamento chico; por eso se reporta Spearman (rangos) y ningún
  departamento se lee individualmente.
- **Denominador fijo en la ECH 2019**: es el único año de la ventana
  2018-2021 con microdatos extraídos en este proyecto. La población
  departamental 0-17 cambia lentamente y el error que introduce es menor
  al error muestral departamental; el lado socioeconómico (pobreza,
  hacinamiento) también queda fijo en 2019, por lo que los años 2020 y
  2021 se cruzan contra condiciones pre-pandemia (advertido en la
  lectura).
- **Paysandú 2020 (Fiscalía) = 1** es un valor anómalo interno de la
  fuente (el total impreso solo cierra con él); el Spearman de 2020 se
  reporta además sin Paysandú como control de sensibilidad.
- El numerador registra el departamento de **atención/actuación**, no el
  de residencia de la víctima.

Salida: resultados/cruces/cruce_conapees_fiscalia_ech.csv
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr

from politicas_sociales import config
from politicas_sociales.cruce_inau_ech import clave, metrica_ech, poblacion_ech

CURADOS = config.DATOS_CURADOS
SALIDA = config.RESULTADOS / "cruces"
ANIOS = [2018, 2019, 2020, 2021]
ANIO_ECH = 2019  # único año de la ventana con microdatos ECH extraídos


def casos_departamentales(df: pd.DataFrame, anio: int) -> pd.DataFrame:
    """Filas departamentales del año, verificadas contra el total nacional.

    Guardián heredado de la curaduría: la suma de los 19 departamentos
    debe reproducir la fila "Total nacional" del mismo año (las tablas
    del estudio FLACSO traen el total impreso y la extracción ya lo
    validó; este guardián impide que un filtro mal escrito lo rompa en
    silencio).
    """
    del_anio = df[df["anio"] == anio]
    deptos = del_anio[del_anio["departamento"] != "Total nacional"].copy()
    total = del_anio[del_anio["departamento"] == "Total nacional"]["valor"]
    if len(deptos) != 19:
        raise ValueError(f"{anio}: se esperaban 19 departamentos, hay {len(deptos)}")
    if len(total) != 1 or deptos["valor"].sum() != total.iloc[0]:
        raise ValueError(f"{anio}: la suma departamental no reproduce el total nacional")
    deptos["clave"] = deptos["departamento"].map(clave)
    return deptos[["clave", "departamento", "valor"]]


def main() -> None:
    conapees = pd.read_csv(CURADOS / "conapees_esnna.csv")
    conapees = conapees[conapees["nota"].fillna("").str.contains("tabla 2")]
    fiscalia = pd.read_csv(CURADOS / "fiscalia_delitos_sexuales_nna.csv")

    poblacion = poblacion_ech(ANIO_ECH)
    echm = pd.read_csv(config.RESULTADOS / "ech" / "metricas_ech_0a17.csv")
    pobreza = metrica_ech(echm, "pobreza_0a17", ANIO_ECH, "pobreza_2019_pct")
    hacinamiento = metrica_ech(echm, "hacinamiento_hogares_nna", ANIO_ECH,
                               "hacinamiento_2019_pct")

    filas = []
    for fuente, df, indicador in [
        ("conapees", conapees, "situaciones ESNNA atendidas"),
        ("fiscalia", fiscalia, "actuaciones FGN delitos sexuales NNA"),
    ]:
        for anio in ANIOS:
            base = casos_departamentales(df, anio)
            base = base.merge(poblacion, on="clave", validate="1:1")
            base = base.merge(pobreza, on="clave", validate="1:1")
            base = base.merge(hacinamiento, on="clave", validate="1:1")
            base.insert(0, "fuente", fuente)
            base.insert(1, "indicador", indicador)
            base.insert(2, "anio", anio)
            base["tasa_por_10mil"] = (base["valor"] / base["poblacion_0a17_ech"]
                                      * 10000).round(2)
            filas.append(base)

    todo = pd.concat(filas, ignore_index=True).rename(columns={"valor": "casos"})
    todo["poblacion_0a17_ech"] = todo["poblacion_0a17_ech"].round()
    columnas = ["fuente", "indicador", "anio", "departamento", "casos",
                "poblacion_0a17_ech", "n_muestral_poblacion", "tasa_por_10mil",
                "pobreza_2019_pct", "n_muestral_pobreza_2019_pct",
                "hacinamiento_2019_pct", "n_muestral_hacinamiento_2019_pct"]
    todo = todo[columnas].sort_values(["fuente", "anio", "departamento"])
    SALIDA.mkdir(parents=True, exist_ok=True)
    todo.to_csv(SALIDA / "cruce_conapees_fiscalia_ech.csv", index=False,
                encoding="utf-8")

    print("Asociaciones (Spearman, n=19 departamentos; lado ECH fijo en "
          f"{ANIO_ECH}):")
    for fuente in ("conapees", "fiscalia"):
        for anio in ANIOS:
            t = todo[(todo["fuente"] == fuente) & (todo["anio"] == anio)]
            for variable in ("pobreza_2019_pct", "hacinamiento_2019_pct"):
                rho, pval = spearmanr(t["tasa_por_10mil"], t[variable])
                print(f"  {fuente} {anio} · tasa vs {variable}: "
                      f"rho={rho:+.2f} (p={pval:.3f})")
        print()
    # Sensibilidad: Fiscalía 2020 sin el valor anómalo de Paysandú (=1).
    t = todo[(todo["fuente"] == "fiscalia") & (todo["anio"] == 2020)
             & (todo["departamento"] != "Paysandú")]
    for variable in ("pobreza_2019_pct", "hacinamiento_2019_pct"):
        rho, pval = spearmanr(t["tasa_por_10mil"], t[variable])
        print(f"  fiscalia 2020 sin Paysandú · tasa vs {variable}: "
              f"rho={rho:+.2f} (p={pval:.3f})")


if __name__ == "__main__":
    main()
