"""Tests del cruce ENSANNA × ECH.

Las decisiones que se prueban: el gradiente ECH se calcula SOLO sobre
Montevideo (los estratos del interior no tienen orden socioeconómico),
la ocupación regional respeta la regla del panel (mes a mes y luego
promedio, nunca un pool), y la monotonía se evalúa como está definida.
"""

import pandas as pd
import pytest

cruce = pytest.importorskip("politicas_sociales.cruce_ensanna_ech")


def test_es_monotono_decreciente():
    assert cruce.es_monotono_decreciente([7.9, 7.5, 6.1, 5.9, 4.8])
    assert cruce.es_monotono_decreciente([3.0, 3.0, 1.0])
    assert not cruce.es_monotono_decreciente([1.0, 2.0])


def test_pobreza_por_estrato_ignora_el_interior():
    personas = pd.DataFrame({
        "departamento": ["MONTEVIDEO", "MONTEVIDEO", "Salto"],
        "estrato_tipo": [1, 1, 6],
        "pobre": [1.0, 0.0, 1.0],
        "ponderador_hogar": [1.0, 1.0, 50.0],
    })
    salida = cruce.pobreza_por_estrato_montevideo(personas)
    bajo = next(f for f in salida if f["categoria"] == "Bajo")
    # El hogar de Salto (estrato 6, peso 50) no debe entrar: 1 de 2.
    assert bajo["valor"] == 50.0
    assert bajo["n_muestral"] == 2
    assert [f["categoria"] for f in salida] == cruce.ORDEN_NSE


def test_ocupacion_por_region_promedia_meses():
    empleo = pd.DataFrame({
        "edad": [15, 15, 16, 16, 12],
        "mes": [1, 1, 2, 2, 1],
        "departamento": ["MONTEVIDEO"] * 5,
        "condicion_actividad_cod": [2, 1, 2, 1, 2],
        "ponderador_empleo": [1.0, 1.0, 3.0, 1.0, 9.0],
    })
    salida = cruce.ocupacion_por_region(empleo)
    mvd = next(f for f in salida if f["categoria"] == "Montevideo")
    # Mes 1: 50%; mes 2: 75%; promedio 62,5 (un pool daría 66,7). El de
    # 12 años queda fuera (el módulo no releva menores de 14).
    assert mvd["valor"] == 62.5
    interior = next(f for f in salida if f["categoria"] == "Interior")
    assert pd.isna(interior["valor"]) or interior["n_muestral"] == 0


def test_gradiente_ensanna_filtra_porcentajes_y_asigna_orden():
    ens = pd.DataFrame({
        "metrica": ["trabajo_infantil"] * 3,
        "categoria": ["nse=Bajo", "nse=Bajo", "region=Interior"],
        "valor": [7.9, 16.3, 7.7],
        "unidad": ["porcentaje", "miles_nna", "porcentaje"],
        "fuente": ["Cuadro 4"] * 3,
    })
    salida = cruce.gradiente_ensanna(ens, "trabajo_infantil", "nse=", "nse",
                                     cruce.ORDEN_NSE)
    # La fila en miles de NNA y la de región no entran al gradiente NSE.
    assert len(salida) == 1
    assert salida[0]["valor"] == 7.9
    assert salida[0]["orden"] == 0
