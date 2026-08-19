"""P5 — Cobertura de Comités de Recepción Local proyectada (escenario
inercial).

Serie: cantidad de CRL del SIPIAV a fin de cada año, 2013-2025 (13
puntos, curados del texto de los informes de gestión). El catálogo
anticipa una **curva saturante** — los comités cubren un territorio
finito y la serie se amesetó (35, 36, 36) — así que a los cuatro
candidatos estándar para conteos (ingenuo, deriva, lineal MCO,
log-lineal; reutilizados de P4) se agrega la **curva asintótica** que el
protocolo admite para series saturantes
(`docs/PREDICTIVO_JUSTIFICACION_TECNICA.md`, punto 1):

    y(t) = L - (L - y0) * exp(-k * t)

con y0 fijado en el primer valor observado (2 parámetros libres, L y k:
con 11 puntos de ajuste, más parámetros sería sobreajuste). Criterios de
aceptación fijados antes de calcular: superar al ingenuo en el backtest
(holdout: últimos 2 puntos) y MAPE ≤ 15%; horizonte ≤ 1/3 del largo de
la serie (13 puntos → se proyecta 2026-2028); rango de ±2 desviaciones
de los residuos del reajuste completo. Si ningún candidato supera al
ingenuo, no se publica proyección (precedente: P4).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from politicas_sociales import config
from politicas_sociales.proyeccion_p4_tasa_spe import HOLDOUT, MAPE_MAXIMO, evaluar

CURADOS = config.DATOS_CURADOS
SALIDA = config.RESULTADOS / "proyecciones"

ANIOS_FUTUROS = [2026, 2027, 2028]


def serie_crl(archivo: Path | None = None) -> pd.Series:
    """Serie anual de CRL (metrica crl_cantidad, categoria total).

    Guardián: la serie debe ser de años consecutivos, sin huecos — un
    hueco silencioso correría el eje temporal del ajuste y el backtest
    compararía contra años equivocados. `archivo` existe para poder
    probar el guardián con datos sintéticos.
    """
    df = pd.read_csv(archivo or CURADOS / "sipiav_series.csv")
    s = (df[(df["metrica"] == "crl_cantidad") & (df["categoria"] == "total")]
         .set_index("anio")["valor"].sort_index())
    anios = s.index.to_numpy()
    if len(s) < 6 or (np.diff(anios) != 1).any():
        raise ValueError(
            "La serie de CRL tiene huecos o menos de 6 puntos: el ajuste "
            f"temporal no es válido (años presentes: {list(anios)})"
        )
    return s


def _ajustar_asintotica(t: np.ndarray, y: np.ndarray):
    """Ajusta y(t) = L - (L - y0) * exp(-k t) con y0 fijo en y[0].
    Devuelve (funcion_predictora, (L, k))."""
    y0 = float(y[0])

    def curva(tt, L, k):
        return L - (L - y0) * np.exp(-k * tt)

    # Punto de partida: asíntota apenas por encima del máximo observado.
    parametros, _ = curve_fit(
        curva, t, y, p0=[float(y.max()) + 1.0, 0.2],
        bounds=([float(y.max()), 1e-4], [10.0 * float(y.max()), 5.0]),
        maxfev=10000,
    )
    return (lambda tt: curva(tt, *parametros)), tuple(parametros)


def evaluar_p5(serie: np.ndarray) -> dict:
    """Backtest de los cuatro candidatos estándar (reutilizados de P4)
    más la curva asintótica. Elección según el protocolo: para una serie
    saturante se prefiere la asintótica si pasa ambos criterios (su
    estructura es la del fenómeno: cobertura de un territorio finito);
    si no pasa, decide el veredicto estándar de P4."""
    base = evaluar(serie)

    t = np.arange(len(serie), dtype=float)
    t_train, y_train = t[:-HOLDOUT], serie[:-HOLDOUT]
    t_hold, y_hold = t[-HOLDOUT:], serie[-HOLDOUT:]
    try:
        predictor, _ = _ajustar_asintotica(t_train, y_train)
        pred = predictor(t_hold)
        mae = float(np.abs(pred - y_hold).mean())
        mape = float((np.abs(pred - y_hold) / y_hold).mean() * 100)
        base["backtest"]["asintotica"] = (mae, mape)
        if mape < base["backtest"]["ingenuo"][1] and mape <= MAPE_MAXIMO:
            base["modelo"] = "asintotica"
    except RuntimeError:
        # El ajuste no convergió: la serie no es asintótica en la práctica
        # y quedan los candidatos estándar.
        pass
    return base


def proyectar_asintotica(serie: np.ndarray, n_futuros: int):
    """Reajusta la curva con la serie completa y proyecta con rango de
    ±2 desviaciones de los residuos."""
    t = np.arange(len(serie), dtype=float)
    predictor, parametros = _ajustar_asintotica(t, serie)
    residuos = serie - predictor(t)
    s = residuos.std(ddof=2)
    t_futuro = np.arange(len(serie), len(serie) + n_futuros, dtype=float)
    centro = predictor(t_futuro)
    return centro, centro - 2 * s, centro + 2 * s, parametros


def main() -> None:
    serie = serie_crl()
    print("Serie CRL (fin de cada año):")
    print(serie.to_string())

    veredicto = evaluar_p5(serie.to_numpy(dtype=float))
    print("\nBacktest (ajuste hasta 2023, holdout 2024-2025):")
    for modelo, (mae, mape) in veredicto["backtest"].items():
        print(f"  {modelo:>10}: MAE {mae:6.2f}  MAPE {mape:5.2f}%")
    print(f"  Modelo elegido: {veredicto['modelo']}")

    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = [{"anio": int(a), "tipo": "observado", "crl": int(v)}
             for a, v in serie.items()]

    if veredicto["modelo"] == "asintotica":
        centro, bajo, alto, (L, k) = proyectar_asintotica(
            serie.to_numpy(dtype=float), len(ANIOS_FUTUROS))
        print(f"\nCurva asintótica reajustada: L={L:.1f}, k={k:.3f}")
        for a, c, b, al in zip(ANIOS_FUTUROS, centro, bajo, alto):
            filas.append({"anio": a, "tipo": "proyectado", "crl": round(float(c), 1),
                          "rango": f"{b:.1f}-{al:.1f}"})
    elif veredicto["modelo"] != "no_proyectable":
        # Un candidato estándar pasó y la asintótica no: proyección con
        # el mecanismo de P4 no implementado aquí a propósito — si este
        # caso aparece con datos reales, se decide mirándolos (hoy la
        # serie es saturante y este camino no ocurre).
        raise NotImplementedError(
            f"El candidato elegido fue {veredicto['modelo']}: revisar la "
            "serie antes de proyectar un modelo no asintótico sobre una "
            "cobertura territorial finita."
        )
    else:
        print("\nNingún candidato supera al ingenuo: no se publica "
              "proyección (lectura descriptiva, precedente P4).")
        ultimo = int(serie.iloc[-1])
        for a in ANIOS_FUTUROS:
            filas.append({"anio": a, "tipo": "referencia_inercial_sin_modelo",
                          "crl": ultimo})

    resultado = pd.DataFrame(filas)
    resultado.to_csv(SALIDA / "p5_cobertura_crl.csv", index=False, encoding="utf-8")
    print("\nResultado (resultados/proyecciones/p5_cobertura_crl.csv):")
    print(resultado.to_string(index=False))


if __name__ == "__main__":
    main()
