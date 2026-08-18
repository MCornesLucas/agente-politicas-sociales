"""Tests del cruce CONAPEES/Fiscalía × ECH.

El guardián de este cruce hereda la verificación de la curaduría (la
suma departamental reproduce el total nacional impreso en el estudio
FLACSO) y la vuelve permanente: un filtro mal escrito que pierda un
departamento o arrastre una fila de texto debe detener la corrida, no
producir tasas con un numerador incompleto.
"""

import pandas as pd
import pytest

from politicas_sociales.cruce_conapees_fiscalia_ech import casos_departamentales

DEPARTAMENTOS = [f"Depto {i}" for i in range(1, 20)]


def _tabla(anio=2020, valores=None, total=None):
    valores = valores if valores is not None else list(range(1, 20))
    filas = [{"anio": anio, "departamento": d, "valor": v, "nota": ""}
             for d, v in zip(DEPARTAMENTOS, valores)]
    filas.append({"anio": anio, "departamento": "Total nacional",
                  "valor": total if total is not None else sum(valores),
                  "nota": ""})
    return pd.DataFrame(filas)


def test_devuelve_los_19_departamentos_con_clave():
    salida = casos_departamentales(_tabla(), 2020)
    assert len(salida) == 19
    assert "Total nacional" not in salida["departamento"].values
    assert salida["clave"].iloc[0] == "DEPTO 1"


def test_guardian_detiene_si_la_suma_no_reproduce_el_total():
    with pytest.raises(ValueError, match="total nacional"):
        casos_departamentales(_tabla(total=999), 2020)


def test_guardian_detiene_si_falta_un_departamento():
    tabla = _tabla()
    tabla = tabla[tabla["departamento"] != "Depto 7"]
    with pytest.raises(ValueError, match="19 departamentos"):
        casos_departamentales(tabla, 2020)


def test_solo_usa_las_filas_del_anio_pedido():
    tabla = pd.concat([_tabla(anio=2019), _tabla(anio=2020)], ignore_index=True)
    salida = casos_departamentales(tabla, 2019)
    assert len(salida) == 19
