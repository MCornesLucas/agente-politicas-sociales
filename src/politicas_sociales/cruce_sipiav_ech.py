"""Cruce SIPIAV × ECH nacional por tramo de edad (cruce 4 del catálogo).

El SIPIAV no publica desagregación departamental de situaciones
(limitación estructural documentada en el catálogo), así que este cruce
es **solo nacional y por tramo de edad**: compara la composición etaria
de las situaciones de violencia atendidas (SIPIAV) con la composición
etaria de la población 0-17 (ECH ponderada) y con la pobreza de cada
tramo. El estadístico es el índice de representación de cada tramo:
participación en las situaciones atendidas / participación en la
población (1 = el tramo pesa en la atención lo mismo que en la
población; >1 = sobrerrepresentado).

Años emparejados: 2019 y 2025 — los únicos con la distribución etaria
SIPIAV completa y microdatos ECH extraídos en este proyecto (control de
estabilidad en dos puntos, como el cruce INAU × ECH).

Limitaciones que acotan toda lectura:

- **Composición de la detección, no de la prevalencia.** Un tramo puede
  estar sobrerrepresentado porque sufre más violencia o porque su
  violencia es más visible para el sistema (la escolarización hace más
  detectable a 6-17 que a 0-5); el registro no permite distinguirlo.
- **Porcentajes publicados redondeados a enteros** y con universos
  distintos por año: 2019 incluye "18 y más" (9%) y publica 0-3/4-5 por
  separado; 2025 publica 0-5 directo y sin fila 18+. Ambos años se
  renormalizan sobre los tramos 0-17 (guardián de rango de suma antes de
  renormalizar); la renormalización arrastra el error de redondeo.
- **Quiebre de tramos en 2020** (0-3/4-5 → 0-5): la comparación usa el
  agregado 0-5, único comparable entre 2019 y 2025.
- La pobreza por tramo (ECH) cruza dos regímenes de canasta (2019:
  canasta 2006; 2025: canasta 2017) — se compara la forma del gradiente
  etario dentro de cada año, nunca los niveles entre años.

Salida: resultados/cruces/cruce_sipiav_ech_tramos.csv
"""

from __future__ import annotations

import pandas as pd

from politicas_sociales import config

CURADOS = config.DATOS_CURADOS
SALIDA = config.RESULTADOS / "cruces"
ANIOS = [2019, 2025]
TRAMOS = ["0 a 5", "6 a 12", "13 a 17"]


def participacion_sipiav(sipiav: pd.DataFrame, anio: int) -> dict[str, float]:
    """Participación de cada tramo 0-17 en las situaciones atendidas,
    renormalizada sobre los tres tramos.

    Guardián: los porcentajes publicados del año (incluido "18 y más" si
    existe) deben sumar entre 95 y 105 (son enteros redondeados) — si la
    serie curada trae un año incompleto, la corrida se detiene en lugar
    de renormalizar sobre tramos que faltan.
    """
    s = sipiav[(sipiav["metrica"] == "distribucion_edad")
               & (sipiav["anio"] == anio)].set_index("categoria")["valor"]
    partes = {}
    partes["0 a 5"] = float(s["0-5"]) if "0-5" in s else float(s["0-3"] + s["4-5"])
    partes["6 a 12"] = float(s["6-12"])
    partes["13 a 17"] = float(s["13-17"])
    publicado = sum(partes.values()) + float(s.get("18 y más", 0))
    if not 95 <= publicado <= 105:
        raise ValueError(
            f"{anio}: los porcentajes publicados suman {publicado} — "
            "distribución incompleta en la serie curada, no se renormaliza"
        )
    total = sum(partes.values())
    return {t: round(v / total * 100, 1) for t, v in partes.items()}


def composicion_ech(personas: pd.DataFrame) -> dict[str, float]:
    """Participación ponderada de cada tramo en la población 0-17."""
    pesos = personas.groupby("tramo_sipiav", observed=True)["ponderador_hogar"].sum()
    total = pesos.sum()
    return {t: round(float(pesos[t] / total * 100), 1) for t in TRAMOS}


def pobreza_por_tramo(echm: pd.DataFrame, anio: int) -> dict[str, float]:
    s = echm[(echm["metrica"] == "pobreza_0a17") & (echm["anio"] == anio)
             & (echm["categoria"].str.startswith("tramo="))]
    return {r["categoria"].removeprefix("tramo="): r["valor"]
            for _, r in s.iterrows()}


def main() -> None:
    sipiav = pd.read_csv(CURADOS / "sipiav_series.csv")
    echm = pd.read_csv(config.RESULTADOS / "ech" / "metricas_ech_0a17.csv")

    filas = []
    for anio in ANIOS:
        personas = pd.read_csv(
            config.DATA_DIR / "ech" / str(anio) / "personas_0a17.csv",
            usecols=["tramo_sipiav", "ponderador_hogar"],
        )
        situaciones = participacion_sipiav(sipiav, anio)
        poblacion = composicion_ech(personas)
        pobreza = pobreza_por_tramo(echm, anio)
        for tramo in TRAMOS:
            filas.append({
                "anio": anio,
                "tramo": tramo,
                "pct_situaciones_sipiav": situaciones[tramo],
                "pct_poblacion_0a17_ech": poblacion[tramo],
                "indice_representacion": round(
                    situaciones[tramo] / poblacion[tramo], 2),
                "pobreza_tramo_pct": pobreza[tramo],
                "fuente": (f"SIPIAV informe {anio} (distribución publicada, "
                           f"renormalizada a 0-17); ECH {anio} (INE), ponderada"),
            })

    todo = pd.DataFrame(filas)
    SALIDA.mkdir(parents=True, exist_ok=True)
    todo.to_csv(SALIDA / "cruce_sipiav_ech_tramos.csv", index=False,
                encoding="utf-8")
    print(todo.drop(columns="fuente").to_string(index=False))


if __name__ == "__main__":
    main()
