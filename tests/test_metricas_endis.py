"""Métrica 37 (ENDIS 2023): la lógica pura se prueba con una muestra
sintética donde el resultado ponderado se conoce de antemano, y el CSV
versionado se contrasta con la misma lógica para que el informe nunca
lea una tabla desalineada con el módulo."""

import pandas as pd
import pytest

from politicas_sociales import metricas_endis as me


def _muestra():
    # Dos tramos, pesos desiguales: la proporción simple daría otro número.
    return pd.DataFrame({
        "PEREDADMESES": [3, 5, 50, 52, 55],
        "E239_recod": ["0", "Centros de primera infancia INAU",
                       "Centros dependientes de ANEP", "Centros dependientes de ANEP", "0"],
        "W": [30.0, 10.0, 50.0, 50.0, 100.0],
    })


def test_cobertura_pondera_por_el_factor_de_expansion():
    tabla = me.cobertura_por_tramo(_muestra())
    t0 = tabla[tabla["tramo"] == "0-11 meses"].set_index("prestador")["porcentaje"]
    assert t0[me.SIN_CENTRO] == 75.0                       # 30 / 40, no 1/2
    assert t0["Centros de primera infancia INAU"] == 25.0
    t4 = tabla[tabla["tramo"] == "48-59 meses"].set_index("prestador")["porcentaje"]
    assert t4["Centros dependientes de ANEP"] == 50.0      # 100 / 200, no 2/3
    assert t4[me.SIN_CENTRO] == 50.0


def test_cada_tramo_suma_cien_y_lleva_sus_casos_muestrales():
    tabla = me.cobertura_por_tramo(_muestra())
    sumas = tabla.groupby("tramo")["porcentaje"].sum()
    presentes = tabla.groupby("tramo")["casos_muestra_tramo"].first()
    for tramo in me.TRAMOS + [me.TOTAL]:
        if presentes[tramo] > 0:
            assert abs(sumas[tramo] - 100.0) < 0.2, tramo
    assert presentes["0-11 meses"] == 2
    assert presentes[me.TOTAL] == 5
    # Tramos sin casos quedan en cero, nunca ausentes (el informe los grafica).
    assert presentes["24-35 meses"] == 0
    assert set(tabla["prestador"]) == set(me.PRESTADORES)


def test_categoria_desconocida_detiene_el_calculo():
    base = _muestra()
    base.loc[0, "E239_recod"] = "Centro inventado"
    with pytest.raises(ValueError, match="no previstas"):
        me.cobertura_por_tramo(base)


def test_el_csv_versionado_tiene_la_forma_que_el_informe_espera():
    tabla = pd.read_csv(me.CSV_SALIDA)
    assert list(tabla.columns) == ["anio", "tramo", "prestador", "porcentaje",
                                   "casos_muestra", "casos_muestra_tramo"]
    assert set(tabla["tramo"]) == set(me.TRAMOS + [me.TOTAL])
    assert set(tabla["prestador"]) == set(me.PRESTADORES)
    assert (tabla["anio"] == 2023).all()
    for _, grupo in tabla.groupby("tramo"):
        assert abs(grupo["porcentaje"].sum() - 100.0) < 0.2
    total = tabla[tabla["tramo"] == me.TOTAL]
    assert total["casos_muestra_tramo"].iloc[0] == total["casos_muestra"].sum()
