"""Tests de P5: guardián de la serie y protocolo con curva asintótica.

La curva asintótica es el candidato que el protocolo admite para series
saturantes; lo delicado es que un ajuste puede "ganar" el backtest
degenerando a casi-lineal (asíntota lejana). Los tests fijan la
mecánica; la lectura de identificabilidad queda documentada en
docs/PREDICTIVO_JUSTIFICACION_TECNICA.md.
"""

import numpy as np
import pandas as pd
import pytest

from politicas_sociales.proyeccion_p5_cobertura_crl import (
    evaluar_p5,
    proyectar_asintotica,
    serie_crl,
)


def _csv_crl(tmp_path, anios, valores):
    archivo = tmp_path / "sipiav_series.csv"
    pd.DataFrame({
        "metrica": ["crl_cantidad"] * len(anios) + ["situaciones_atendidas"],
        "anio": list(anios) + [2020],
        "categoria": ["total"] * (len(anios) + 1),
        "valor": list(valores) + [4911],
    }).to_csv(archivo, index=False)
    return archivo


def test_serie_crl_lee_solo_la_metrica_y_ordena(tmp_path):
    archivo = _csv_crl(tmp_path, [2015, 2013, 2014, 2016, 2017, 2018],
                       [26, 24, 25, 27, 28, 29])
    serie = serie_crl(archivo)
    assert list(serie.index) == [2013, 2014, 2015, 2016, 2017, 2018]
    assert serie[2013] == 24


def test_guardian_detiene_series_con_huecos(tmp_path):
    # Un hueco correría el eje temporal del ajuste en silencio.
    archivo = _csv_crl(tmp_path, [2013, 2014, 2016, 2017, 2018, 2019],
                       [24, 25, 27, 28, 29, 30])
    with pytest.raises(ValueError, match="huecos"):
        serie_crl(archivo)


def test_guardian_detiene_series_demasiado_cortas(tmp_path):
    archivo = _csv_crl(tmp_path, [2020, 2021, 2022], [30, 31, 32])
    with pytest.raises(ValueError, match="6 puntos"):
        serie_crl(archivo)


def test_serie_saturante_elige_la_asintotica():
    # Serie sintética genuinamente saturante hacia L=40, todavía en
    # ascenso en el holdout (si ya llegó a la meseta, el ingenuo tiene
    # error cero y nada puede superarlo — ese caso lo cubre el test de
    # la serie amesetada).
    t = np.arange(13, dtype=float)
    serie = 40 - 16 * np.exp(-0.25 * t)
    veredicto = evaluar_p5(serie)
    assert veredicto["modelo"] == "asintotica"
    assert "asintotica" in veredicto["backtest"]
    assert veredicto["backtest"]["asintotica"][1] < veredicto["backtest"]["ingenuo"][1]


def test_serie_amesetada_no_se_proyecta():
    # Plana: el ingenuo es imbatible; la asintótica no puede superarlo y
    # el protocolo degrada a lectura descriptiva.
    veredicto = evaluar_p5(np.full(13, 36.0))
    assert veredicto["modelo"] == "no_proyectable"


def test_proyectar_asintotica_respeta_la_asintota_y_el_rango():
    t = np.arange(13, dtype=float)
    serie = 40 - 16 * np.exp(-0.35 * t)
    centro, bajo, alto, (L, k) = proyectar_asintotica(serie, 3)
    assert len(centro) == 3
    assert (bajo <= centro).all() and (centro <= alto).all()
    # La proyección crece hacia la asíntota sin superarla.
    assert (np.diff(centro) > 0).all()
    assert (centro < L).all()
    assert L == pytest.approx(40, abs=1.0)
