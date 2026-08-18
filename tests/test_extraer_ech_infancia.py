"""Tests de las clasificaciones de edad por organismo.

Los cortes de edad son la decisión metodológica central del universo
0-17 (docs/CLASIFICACION_DE_EDADES.md): cada organismo clasifica
distinto y un límite corrido en una unidad cambia a qué tramo se asigna
cada niño en todas las métricas posteriores. Por eso se prueban los
bordes exactos, no valores intermedios.
"""

import pandas as pd
import pytest

# El módulo importa los loaders del proyecto hermano al cargarse; si el
# hermano no está instalado como carpeta hermana, la extracción
# genuinamente no puede correr y estos tests se omiten con la razón.
extraer = pytest.importorskip("politicas_sociales.extraer_ech_infancia")


def _edades(*edades):
    return pd.DataFrame({"edad": list(edades)})


def test_tramos_sipiav_en_los_bordes():
    df = extraer.clasificar_edades(_edades(0, 5, 6, 12, 13, 17))
    assert list(df["tramo_sipiav"].astype(str)) == [
        "0 a 5", "0 a 5", "6 a 12", "6 a 12", "13 a 17", "13 a 17",
    ]


def test_ley_17823_ninio_hasta_los_12_adolescente_desde_los_13():
    df = extraer.clasificar_edades(_edades(12, 13))
    assert list(df["clasificacion_ley_17823"].astype(str)) == ["Niño/a", "Adolescente"]


def test_adolescente_oms_de_10_a_17_dentro_del_universo():
    df = extraer.clasificar_edades(_edades(9, 10, 17))
    assert list(df["es_adolescente_oms"]) == [False, True, True]


def test_universo_ensanna_de_5_a_17():
    df = extraer.clasificar_edades(_edades(4, 5, 17))
    assert list(df["en_universo_ensanna"]) == [False, True, True]


def test_clasificar_edades_no_modifica_el_dataframe_original():
    original = _edades(3, 15)
    extraer.clasificar_edades(original)
    assert list(original.columns) == ["edad"]
