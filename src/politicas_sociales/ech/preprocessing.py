"""Normalizaciones mínimas sobre las tablas cargadas de la ECH."""

from __future__ import annotations

import pandas as pd


def normalizar_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """Deja "departamento" en mayúsculas, consistente entre años — no se
    escribe igual en todos ("MONTEVIDEO" en el .sav de 2019, "Montevideo"
    en el CSV combinado de 2024 en adelante). Sin esto, cruzar dos tablas
    de años distintos por departamento cruza cero filas en vez de fallar
    con un error claro — encontrado en una corrida real comparando 2019
    contra 2024.

    Llamar siempre apenas se carga `hogares` (o cualquier tabla derivada
    que traiga esta columna) y antes de cualquier comparación entre años.
    """
    df = df.copy()
    df["departamento"] = df["departamento"].str.upper()
    return df
