"""P3 — Desinternación proyectada por departamento (escenario inercial).

Genera además la versión compacta versionable del departamental de INAU
(`datos_curados/inau_spe_departamental_totales.csv`, solo
apertura=="total": la conversión completa de 48 MB no se versiona — ver
.gitignore).

Serie por departamento: proporción de NNA del Sistema de Protección
Especial que viven en contexto familiar — indicadores departamentales 6
(contexto familiar) y 5 (residencia), 12 puntos semestrales 2020-S1 a
2025-S2. Protocolo de `docs/PREDICTIVO_JUSTIFICACION_TECNICA.md`:
candidatos simples, backtest con los últimos 2 puntos, criterios de
aceptación fijados antes de calcular (superar al ingenuo y MAPE ≤ 15%),
horizonte ≤ 1/3 del largo de la serie (12 puntos → 4 semestres:
2026-2027), rango de ±2 desviaciones de los residuos. Los departamentos
cuyo backtest no pasa los criterios quedan como solo descriptivos, no se
fuerzan.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROYECTO = Path(__file__).resolve().parent.parent
CURADOS = PROYECTO / "datos_curados"
SALIDA = PROYECTO / "resultados" / "proyecciones"

HOLDOUT = 2
SEMESTRES_FUTUROS = ["2026-S1", "2026-S2", "2027-S1", "2027-S2"]
MAPE_MAXIMO = 15.0


def logit(p: np.ndarray) -> np.ndarray:
    p = np.clip(p / 100, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def inv_logit(z: np.ndarray) -> np.ndarray:
    return 100 / (1 + np.exp(-z))


def evaluar(serie: np.ndarray) -> dict:
    """Backtest de los 4 candidatos sobre una serie semestral (índice
    temporal 0..n-1). Devuelve métricas y el modelo elegido según el
    protocolo (estabilidad sobre victoria estrecha)."""
    t = np.arange(len(serie), dtype=float)
    t_train, y_train = t[:-HOLDOUT], serie[:-HOLDOUT]
    t_hold, y_hold = t[-HOLDOUT:], serie[-HOLDOUT:]

    def mape(pred):
        return float((np.abs(pred - y_hold) / y_hold).mean() * 100)

    resultados = {}
    resultados["ingenuo"] = mape(np.full(HOLDOUT, y_train[-1]))
    deriva = (y_train[-1] - y_train[0]) / (len(y_train) - 1)
    resultados["deriva"] = mape(y_train[-1] + deriva * (t_hold - t_train[-1]))
    c_raw = np.polyfit(t_train, y_train, 1)
    resultados["lineal"] = mape(np.polyval(c_raw, t_hold))
    c_log = np.polyfit(t_train, logit(y_train), 1)
    resultados["logit"] = mape(inv_logit(np.polyval(c_log, t_hold)))

    # Elección: logit si pasa los criterios (usa toda la serie y respeta
    # las cotas de una proporción); si no, lineal; si ninguno pasa, no se
    # proyecta.
    for candidato in ("logit", "lineal"):
        if resultados[candidato] < resultados["ingenuo"] and resultados[candidato] <= MAPE_MAXIMO:
            return {"modelo": candidato, **{f"mape_{k}": round(v, 2) for k, v in resultados.items()}}
    return {"modelo": "no_proyectable", **{f"mape_{k}": round(v, 2) for k, v in resultados.items()}}


def proyectar(serie: np.ndarray, modelo: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Reajusta con la serie completa y proyecta 4 semestres con rango."""
    t = np.arange(len(serie), dtype=float)
    t_fut = np.arange(len(serie), len(serie) + len(SEMESTRES_FUTUROS), dtype=float)
    if modelo == "logit":
        c = np.polyfit(t, logit(serie), 1)
        res = logit(serie) - np.polyval(c, t)
        s = res.std(ddof=2)
        z = np.polyval(c, t_fut)
        return inv_logit(z), inv_logit(z - 2 * s), inv_logit(z + 2 * s)
    c = np.polyfit(t, serie, 1)
    res = serie - np.polyval(c, t)
    s = res.std(ddof=2)
    p = np.polyval(c, t_fut)
    return p, p - 2 * s, p + 2 * s


def main() -> None:
    completo = pd.read_csv(CURADOS / "inau_spe_departamental.csv")
    totales = completo[completo["apertura"] == "total"].copy()
    totales.to_csv(CURADOS / "inau_spe_departamental_totales.csv", index=False, encoding="utf-8")
    print(f"Compacto versionable: {len(totales):,} filas → inau_spe_departamental_totales.csv")

    base = totales[totales["indicador_codigo"].isin([5, 6])].pivot_table(
        index=["departamento", "periodo"], columns="indicador_codigo", values="valor"
    )
    base["pct_familia"] = base[6] / (base[5] + base[6]) * 100

    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = []
    series = {"Total país": base.groupby("periodo").sum()}
    series["Total país"]["pct_familia"] = (
        series["Total país"][6] / (series["Total país"][5] + series["Total país"][6]) * 100
    )
    for depto in base.index.get_level_values(0).unique():
        series[depto] = base.loc[depto]

    for nombre, df in series.items():
        df = df.sort_index()
        serie = df["pct_familia"].to_numpy()
        veredicto = evaluar(serie)
        fila = {
            "unidad_territorial": nombre,
            "ultimo_observado_2025S2": round(float(serie[-1]), 1),
            **veredicto,
        }
        if veredicto["modelo"] != "no_proyectable":
            centro, bajo, alto = proyectar(serie, veredicto["modelo"])
            for sem, c, b, a in zip(SEMESTRES_FUTUROS, centro, bajo, alto):
                fila[f"proy_{sem}"] = round(float(c), 1)
                fila[f"rango_{sem}"] = f"{b:.1f}-{a:.1f}"
        filas.append(fila)

    resultado = pd.DataFrame(filas)
    resultado.to_csv(SALIDA / "p3_desinternacion.csv", index=False, encoding="utf-8")
    proyectables = resultado[resultado["modelo"] != "no_proyectable"]
    print(f"\nUnidades proyectables: {len(proyectables)}/{len(resultado)}")
    cols = ["unidad_territorial", "ultimo_observado_2025S2", "modelo",
            "mape_ingenuo", "mape_logit", "proy_2027-S2", "rango_2027-S2"]
    print(resultado[[c for c in cols if c in resultado.columns]].to_string(index=False))


if __name__ == "__main__":
    main()
