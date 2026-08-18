"""Tests del cruce territorial INAU × ECH.

El cruce une dos fuentes por nombre de departamento, y los nombres
difieren en acentos y mayúsculas entre archivos (Río Negro / RIO NEGRO /
Rio Negro). La normalización es el punto único de falla del join: si
falla, un departamento desaparece del cruce en silencio.
"""

import pandas as pd

from politicas_sociales.cruce_inau_ech import clave, metrica_ech, poblacion_ech


def test_clave_normaliza_acentos_mayusculas_y_espacios():
    assert clave("Río Negro") == "RIO NEGRO"
    assert clave("PAYSANDÚ") == "PAYSANDU"
    assert clave(" San José ") == "SAN JOSE"
    assert clave("Montevideo") == "MONTEVIDEO"


def test_metrica_ech_filtra_y_renombra():
    df = pd.DataFrame({
        "metrica": ["pobreza_0a17"] * 3 + ["hacinamiento_hogares_nna"],
        "anio": [2024, 2024, 2025, 2024],
        "categoria": ["departamento=Salto", "total", "departamento=Salto",
                      "departamento=Salto"],
        "valor": [30.0, 20.0, 28.0, 10.0],
        "n_muestral": [100, 500, 90, 100],
    })
    salida = metrica_ech(df, "pobreza_0a17", 2024, "pobreza_pct")
    # Solo la apertura departamental del año y la métrica pedidos; ni el
    # total nacional ni otro año ni otra métrica.
    assert len(salida) == 1
    assert salida.loc[0, "clave"] == "SALTO"
    assert salida.loc[0, "pobreza_pct"] == 30.0
    assert salida.loc[0, "n_muestral_pobreza_pct"] == 100


def test_metrica_ech_colapsa_variantes_de_acentos():
    df = pd.DataFrame({
        "metrica": ["pobreza_0a17"] * 2,
        "anio": [2024, 2024],
        "categoria": ["departamento=Río Negro", "departamento=Rio Negro"],
        "valor": [30.0, 31.0],
        "n_muestral": [100, 100],
    })
    salida = metrica_ech(df, "pobreza_0a17", 2024, "pobreza_pct")
    assert len(salida) == 1
    assert salida.loc[0, "clave"] == "RIO NEGRO"


def test_poblacion_ech_suma_ponderadores_y_cuenta_n(tmp_path):
    carpeta = tmp_path / "2024"
    carpeta.mkdir()
    pd.DataFrame({
        "departamento": ["MONTEVIDEO", "MONTEVIDEO", "Salto"],
        "ponderador_hogar": [100.0, 200.0, 50.0],
    }).to_csv(carpeta / "personas_0a17.csv", index=False)
    salida = poblacion_ech(2024, datos_ech=tmp_path).set_index("clave")
    # Población: suma de ponderadores (estimación expandida); n muestral:
    # cantidad de filas sin ponderar, para la regla de celdas chicas.
    assert salida.loc["MONTEVIDEO", "poblacion_0a17_ech"] == 300.0
    assert salida.loc["MONTEVIDEO", "n_muestral_poblacion"] == 2
    assert salida.loc["SALTO", "poblacion_0a17_ech"] == 50.0
