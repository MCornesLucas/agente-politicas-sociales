"""P4 — NNA en protección especial cada 1.000 NNA (escenario inercial).

Numerador: NNA de 0 a 17 años atendidos en el Sistema de Protección
Especial (indicador nacional 1.1 de INAU, suma de los tramos 0-2, 3-7,
8-12, 13-15 y 16-17 — la suma de tramos reproduce el total del indicador
en los seis años, verificado). Se usa el recorte 0-17 y no el total del
indicador (que incluye 18-20 y 21+) para que numerador y denominador
midan el mismo universo.

Denominador: población proyectada de 0 a 17 años del INE (revisión 2025,
archivo B.1.1, edad simple, ambos sexos) — **sin modelo propio**, regla
de `METODOLOGIA.md`: los denominadores futuros no se extrapolan en este
proyecto. La revisión 2025 comienza en 2024: la tasa observada solo
existe para 2024 y 2025; los años 2020-2023 del numerador participan del
ajuste pero no tienen tasa (las estimaciones retrospectivas de la
revisión 2025 no estaban publicadas al momento de este cálculo).

Protocolo de `docs/PREDICTIVO_JUSTIFICACION_TECNICA.md`: candidatos
simples (ingenuo, deriva, lineal MCO, log-lineal — conteos, no
proporciones: sin logit), backtest con los últimos 2 puntos, criterios
de aceptación fijados antes de calcular (superar al ingenuo y MAPE de
holdout ≤ 15%), horizonte ≤ 1/3 del largo de la serie (6 puntos → 2
años: 2026-2027), rango de ±2 desviaciones de los residuos del
reajuste completo. La incertidumbre reportada es solo la del numerador;
el denominador es una proyección externa con supuestos propios del INE.
Si ningún candidato supera al ingenuo, no se publica proyección: el
escenario inercial se degrada a lectura descriptiva (precedente: P3,
series estables).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

PROYECTO = Path(__file__).resolve().parent.parent
CURADOS = PROYECTO / "datos_curados"
INE_B11 = (
    PROYECTO
    / "data"
    / "ine"
    / "proyecciones_rev2025"
    / "B11_uruguay_edad_simple_2024_2070.xlsx"
)
SALIDA = PROYECTO / "resultados" / "proyecciones"

HOLDOUT = 2
ANIOS_FUTUROS = [2026, 2027]
MAPE_MAXIMO = 15.0
TRAMOS_0A17 = [
    "tramo=0 a 2 años",
    "tramo=3 a 7 años",
    "tramo=8 a 12 años",
    "tramo=13 a 15 años",
    "tramo=16 a 17 años",
]


def numerador_0a17() -> pd.Series:
    """Serie anual 2020-2025 de NNA 0-17 atendidos en el SPE."""
    df = pd.read_csv(
        CURADOS / "inau_spe_nacional.csv", dtype={"indicador_codigo": str}
    )
    s = df[(df["indicador_codigo"] == "1.1") & (df["apertura"].isin(TRAMOS_0A17))]
    serie = s.groupby("anio")["valor"].sum().sort_index()

    # Guardián: la suma de todos los tramos debe reproducir el total del
    # indicador (verificado contra la salida real, no supuesto).
    todos = df[
        (df["indicador_codigo"] == "1.1")
        & (df["apertura"].str.startswith("tramo="))
    ]
    suma_tramos = todos.groupby("anio")["valor"].sum().sort_index()
    total = (
        df[(df["indicador_codigo"] == "1.1") & (df["apertura"] == "total")]
        .set_index("anio")["valor"]
        .sort_index()
    )
    if not np.allclose(suma_tramos, total):
        raise ValueError("La suma de tramos no reproduce el total del indicador 1.1")
    return serie


def denominador_ine(anios: list[int]) -> dict[int, float]:
    """Población 0-17 proyectada (INE rev. 2025, B.1.1, ambos sexos)."""
    wb = openpyxl.load_workbook(INE_B11, read_only=True)
    filas = list(wb["Uruguay"].iter_rows(values_only=True))
    wb.close()
    encabezado = filas[4]  # fila 5: None, 2024, 2025, ...
    col_por_anio = {a: i for i, a in enumerate(encabezado) if isinstance(a, int)}
    # Bloque "Ambos sexos": fila 6 es la etiqueta; edades 0..17 = filas 7-24.
    if filas[5][0] != "Ambos sexos" or filas[6][0] != 0:
        raise ValueError("La estructura del archivo B.1.1 no es la esperada")
    return {
        a: sum(filas[6 + edad][col_por_anio[a]] for edad in range(18))
        for a in anios
    }


def evaluar(serie: np.ndarray) -> dict:
    """Backtest de los 4 candidatos para conteos. Protocolo: estabilidad
    sobre victoria estrecha; sin logit (no es una proporción)."""
    t = np.arange(len(serie), dtype=float)
    t_train, y_train = t[:-HOLDOUT], serie[:-HOLDOUT]
    t_hold, y_hold = t[-HOLDOUT:], serie[-HOLDOUT:]

    def metricas(pred):
        mae = float(np.abs(pred - y_hold).mean())
        mape = float((np.abs(pred - y_hold) / y_hold).mean() * 100)
        return mae, mape

    resultados = {}
    resultados["ingenuo"] = metricas(np.full(HOLDOUT, y_train[-1]))
    deriva = (y_train[-1] - y_train[0]) / (len(y_train) - 1)
    resultados["deriva"] = metricas(y_train[-1] + deriva * (t_hold - t_train[-1]))
    c_lin = np.polyfit(t_train, y_train, 1)
    resultados["lineal"] = metricas(np.polyval(c_lin, t_hold))
    c_log = np.polyfit(t_train, np.log(y_train), 1)
    resultados["log_lineal"] = metricas(np.exp(np.polyval(c_log, t_hold)))

    mape_ingenuo = resultados["ingenuo"][1]
    elegido = "no_proyectable"
    for candidato in ("lineal", "deriva", "log_lineal"):
        if resultados[candidato][1] < mape_ingenuo and resultados[candidato][1] <= MAPE_MAXIMO:
            elegido = candidato
            break
    return {"modelo": elegido, "backtest": resultados}


def main() -> None:
    serie = numerador_0a17()
    print("Numerador (NNA 0-17 atendidos en el SPE):")
    print(serie.to_string())

    anios_obs = [a for a in serie.index if a >= 2024]
    pob = denominador_ine(anios_obs + ANIOS_FUTUROS)
    print("\nDenominador INE rev. 2025 (población 0-17):")
    for a, v in pob.items():
        print(f"  {a}: {v:,.0f}")

    veredicto = evaluar(serie.to_numpy(dtype=float))
    print("\nBacktest (ajuste 2020-2023, holdout 2024-2025):")
    for m, (mae, mape) in veredicto["backtest"].items():
        print(f"  {m:>10}: MAE {mae:7.1f}  MAPE {mape:5.1f}%")
    print(f"  Modelo elegido: {veredicto['modelo']}")

    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = []
    for a in anios_obs:
        filas.append(
            {
                "anio": a,
                "tipo": "observado",
                "nna_0a17_spe": int(serie[a]),
                "poblacion_0a17_ine": round(pob[a]),
                "tasa_por_mil": round(serie[a] / pob[a] * 1000, 2),
            }
        )

    if veredicto["modelo"] != "no_proyectable":
        # Reajuste con la serie completa y proyección del numerador.
        t = np.arange(len(serie), dtype=float)
        y = serie.to_numpy(dtype=float)
        t_fut = np.arange(len(serie), len(serie) + len(ANIOS_FUTUROS), dtype=float)
        if veredicto["modelo"] == "log_lineal":
            c = np.polyfit(t, np.log(y), 1)
            res = np.log(y) - np.polyval(c, t)
            s = res.std(ddof=2)
            z = np.polyval(c, t_fut)
            centro, bajo, alto = np.exp(z), np.exp(z - 2 * s), np.exp(z + 2 * s)
        else:
            if veredicto["modelo"] == "deriva":
                pendiente = (y[-1] - y[0]) / (len(y) - 1)
                centro = y[-1] + pendiente * (t_fut - t[-1])
                res = np.diff(y) - pendiente
            else:
                c = np.polyfit(t, y, 1)
                centro = np.polyval(c, t_fut)
                res = y - np.polyval(c, t)
            s = res.std(ddof=2)
            bajo, alto = centro - 2 * s, centro + 2 * s
        for a, ctr, b, al in zip(ANIOS_FUTUROS, centro, bajo, alto):
            filas.append(
                {
                    "anio": a,
                    "tipo": "proyectado",
                    "nna_0a17_spe": round(float(ctr)),
                    "poblacion_0a17_ine": round(pob[a]),
                    "tasa_por_mil": round(ctr / pob[a] * 1000, 2),
                    "tasa_rango": f"{b / pob[a] * 1000:.2f}-{al / pob[a] * 1000:.2f}",
                }
            )
    else:
        print(
            "\nNingún candidato supera al ingenuo: no se publica proyección "
            "del numerador. Lectura descriptiva del escenario inercial: el "
            "numerador se mantiene en torno al último valor observado; la "
            "tasa futura queda determinada por el denominador del INE "
            "(se calcula como referencia, sin rango de modelo)."
        )
        ultimo = float(serie.iloc[-1])
        for a in ANIOS_FUTUROS:
            filas.append(
                {
                    "anio": a,
                    "tipo": "referencia_inercial_sin_modelo",
                    "nna_0a17_spe": round(ultimo),
                    "poblacion_0a17_ine": round(pob[a]),
                    "tasa_por_mil": round(ultimo / pob[a] * 1000, 2),
                }
            )

    resultado = pd.DataFrame(filas)
    resultado.to_csv(SALIDA / "p4_tasa_spe.csv", index=False, encoding="utf-8")
    print("\nResultado (resultados/proyecciones/p4_tasa_spe.csv):")
    print(resultado.to_string(index=False))


if __name__ == "__main__":
    main()
