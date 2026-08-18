"""Tests del protocolo de backtest de P3 (desinternación).

El protocolo (docs/PREDICTIVO_JUSTIFICACION_TECNICA.md) fija los
criterios antes de calcular: superar al ingenuo y MAPE ≤ 15%, o no se
proyecta. Los tests verifican que el código honra ese contrato en los
dos extremos: una serie estable no se fuerza a proyectar, y una serie
con tendencia clara sí pasa.
"""

import numpy as np

from politicas_sociales.proyeccion_desinternacion import (
    SEMESTRES_FUTUROS,
    evaluar,
    inv_logit,
    logit,
    proyectar,
)


def test_logit_e_inv_logit_son_inversas_en_porcentajes():
    valores = np.array([10.0, 50.0, 90.0])
    assert np.allclose(inv_logit(logit(valores)), valores)


def test_logit_acota_los_extremos_sin_infinitos():
    assert np.isfinite(logit(np.array([0.0, 100.0]))).all()


def test_serie_estable_no_se_proyecta():
    # Serie plana: el ingenuo es imbatible (error cero) y ningún
    # candidato lo supera estrictamente — el protocolo exige degradar a
    # lectura descriptiva, no forzar un modelo.
    serie = np.full(12, 60.0)
    assert evaluar(serie)["modelo"] == "no_proyectable"


def test_serie_con_tendencia_clara_pasa_el_backtest():
    serie = 40.0 + 1.5 * np.arange(12)
    veredicto = evaluar(serie)
    assert veredicto["modelo"] in ("logit", "lineal")
    assert veredicto["mape_lineal"] < veredicto["mape_ingenuo"]


def test_proyectar_lineal_devuelve_4_semestres_con_rango_ordenado():
    serie = 40.0 + 1.5 * np.arange(12)
    centro, bajo, alto = proyectar(serie, "lineal")
    assert len(centro) == len(SEMESTRES_FUTUROS) == 4
    assert (bajo <= centro).all() and (centro <= alto).all()
    # La tendencia continúa: el primer punto proyectado supera al último observado.
    assert centro[0] > serie[-1]


def test_proyectar_logit_respeta_las_cotas_de_una_proporcion():
    serie = np.linspace(80.0, 95.0, 12)
    centro, bajo, alto = proyectar(serie, "logit")
    assert (centro > 0).all() and (centro < 100).all()
    assert (alto < 100).all() and (bajo > 0).all()
