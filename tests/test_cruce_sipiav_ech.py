"""Tests del cruce SIPIAV × ECH por tramo de edad.

Lo delicado de este cruce es la renormalización de porcentajes
publicados: 2019 trae 0-3/4-5 por separado más un 9% de mayores de 18,
2025 trae 0-5 directo y sin fila 18+. Se prueba la aritmética de ambos
formatos contra valores calculados a mano y que el guardián detenga una
distribución incompleta en lugar de renormalizarla en silencio.
"""

import pandas as pd
import pytest

from politicas_sociales.cruce_sipiav_ech import (
    composicion_ech,
    participacion_sipiav,
    pobreza_por_tramo,
)


def _sipiav(filas):
    return pd.DataFrame([
        {"metrica": "distribucion_edad", "anio": anio, "categoria": cat,
         "valor": v} for anio, cat, v in filas
    ])


def test_participacion_formato_2019_suma_tramos_chicos_y_renormaliza():
    sip = _sipiav([(2019, "0-3", 8), (2019, "4-5", 9), (2019, "6-12", 39),
                   (2019, "13-17", 35), (2019, "18 y más", 9)])
    salida = participacion_sipiav(sip, 2019)
    # 0-17 publicado = 91; a mano: 17/91=18,7 · 39/91=42,9 · 35/91=38,5.
    assert salida == {"0 a 5": 18.7, "6 a 12": 42.9, "13 a 17": 38.5}


def test_participacion_formato_2025_usa_0a5_directo():
    sip = _sipiav([(2025, "0-5", 23), (2025, "6-12", 38), (2025, "13-17", 34)])
    salida = participacion_sipiav(sip, 2025)
    assert salida == {"0 a 5": 24.2, "6 a 12": 40.0, "13 a 17": 35.8}


def test_guardian_detiene_distribucion_incompleta():
    # Un año al que la serie curada solo le conoce un tramo no se
    # renormaliza: sumaría 100% sobre datos que faltan.
    sip = _sipiav([(2023, "0-5", 17), (2023, "6-12", 30), (2023, "13-17", 20)])
    with pytest.raises(ValueError, match="incompleta"):
        participacion_sipiav(sip, 2023)


def test_composicion_ech_ponderada():
    personas = pd.DataFrame({
        "tramo_sipiav": ["0 a 5", "0 a 5", "6 a 12", "13 a 17"],
        "ponderador_hogar": [100.0, 100.0, 500.0, 300.0],
    })
    salida = composicion_ech(personas)
    assert salida == {"0 a 5": 20.0, "6 a 12": 50.0, "13 a 17": 30.0}


def test_pobreza_por_tramo_filtra_metrica_y_anio():
    echm = pd.DataFrame({
        "metrica": ["pobreza_0a17", "pobreza_0a17", "hacinamiento_hogares_nna"],
        "anio": [2025, 2024, 2025],
        "categoria": ["tramo=0 a 5", "tramo=0 a 5", "departamento=Salto"],
        "valor": [29.11, 32.19, 4.0],
    })
    assert pobreza_por_tramo(echm, 2025) == {"0 a 5": 29.11}
