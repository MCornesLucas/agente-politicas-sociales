"""Tests de las métricas ECH del universo 0-17.

Cada test verifica una regla de rigor concreta contra un valor calculado
a mano: ponderación siempre (nunca proporción simple), umbral estricto
de hacinamiento, exclusión del 99 (sin dato), promedio mensual del panel
de empleo (nunca pool anual) y la fuente con su canasta por año.
"""

import numpy as np
import pandas as pd
import pytest

metricas = pytest.importorskip("politicas_sociales.metricas_ech")


def test_pct_ponderado_pondera_y_cuenta_n_sin_ponderar():
    df = pd.DataFrame({"peso": [3.0, 1.0]})
    flag = pd.Series([True, False])
    valor, n = metricas.pct_ponderado(df, flag, "peso")
    # Ponderado: 3/4 = 75%. Una proporción simple daría 50% — la
    # diferencia es exactamente el sesgo que la regla evita.
    assert valor == 75.0
    assert n == 2


def test_pct_ponderado_excluye_sin_dato_del_denominador():
    df = pd.DataFrame({"peso": [1.0, 1.0, 5.0]})
    flag = pd.Series([True, False, np.nan])
    valor, n = metricas.pct_ponderado(df, flag, "peso")
    assert valor == 50.0
    assert n == 2


def test_pct_ponderado_vacio_devuelve_nan_y_cero():
    df = pd.DataFrame({"peso": []})
    valor, n = metricas.pct_ponderado(df, pd.Series([], dtype=float), "peso")
    assert np.isnan(valor)
    assert n == 0


def test_metrica_pobreza_cita_la_canasta_del_anio():
    personas = pd.DataFrame({
        "pobre": [1.0, 0.0],
        "ponderador_hogar": [1.0, 1.0],
        "tramo_sipiav": ["0 a 5", "0 a 5"],
        "departamento": ["MONTEVIDEO", "MONTEVIDEO"],
    })
    # La serie tiene dos regímenes de canasta (2006 y 2017): la fuente de
    # cada fila debe decir cuál, y un año no verificado no inventa una.
    assert "canasta 2006" in metricas.metrica_pobreza(personas, 2019)[0]["fuente"]
    assert "canasta 2017" in metricas.metrica_pobreza(personas, 2024)[0]["fuente"]
    assert "verificar" in metricas.metrica_pobreza(personas, 2022)[0]["fuente"]


def test_metrica_pobreza_total_ponderado():
    personas = pd.DataFrame({
        "pobre": [1.0, 0.0, 0.0],
        "ponderador_hogar": [2.0, 1.0, 1.0],
        "tramo_sipiav": ["0 a 5"] * 3,
        "departamento": ["MONTEVIDEO"] * 3,
    })
    total = metricas.metrica_pobreza(personas, 2024)[0]
    assert total["categoria"] == "total"
    assert total["valor"] == 50.0
    assert total["n_muestral"] == 3


def test_metrica_hacinamiento_umbral_estricto_mayor_a_2():
    hogares = pd.DataFrame({
        "total_personas": [4.0, 5.0],
        "cantidad_habitaciones": [2.0, 2.0],
        "ponderador_hogar": [1.0, 1.0],
        "departamento": ["MONTEVIDEO", "MONTEVIDEO"],
    })
    total = metricas.metrica_hacinamiento(hogares, 2024)[0]
    # Exactamente 2 personas por cuarto NO es hacinamiento (el umbral
    # INE/CEPAL es estrictamente más de 2): 4/2 no cuenta, 5/2 sí.
    assert total["valor"] == 50.0


def test_metrica_vivienda_solo_columnas_presentes_y_99_excluido():
    hogares = pd.DataFrame({
        "goteras": [1.0, 2.0, 99.0],
        "ponderador_hogar": [1.0, 1.0, 1.0],
    })
    salida = metricas.metrica_vivienda(hogares, 2024)
    # Solo la carencia presente en el archivo genera fila (2019 trae 12,
    # 2024 trae 4, 2023 ninguna); el 99 sale del denominador.
    assert [f["categoria"] for f in salida] == ["carencia=goteras"]
    assert salida[0]["valor"] == 50.0
    assert salida[0]["n_muestral"] == 2


def test_metrica_brecha_digital_total_y_por_estrato():
    hogares = pd.DataFrame({
        "tiene_internet": [1.0, 2.0, 1.0],
        "estrato_tipo": [1.0, 1.0, 2.0],
        "ponderador_hogar": [1.0, 1.0, 1.0],
    })
    salida = metricas.metrica_brecha_digital(hogares, 2024)
    categorias = [f["categoria"] for f in salida]
    assert categorias[0] == "recurso=internet"
    assert "recurso=internet;estrato=1.0" in categorias
    por_estrato_1 = next(f for f in salida if f["categoria"] == "recurso=internet;estrato=1.0")
    assert por_estrato_1["valor"] == 50.0


def test_metrica_fies_umbral_estricto_y_hogares_con_menores_de_6(tmp_path):
    pd.DataFrame({
        "prob_inseguridad_moderada": [0.6, 0.5, 0.4, 0.9],
        "prob_inseguridad_severa": [0.1, 0.1, 0.1, 0.6],
        "ponderador_fies": [1.0, 1.0, 1.0, 1.0],
        "tiene_menores_6": [0, 0, 0, 1],
    }).to_csv(tmp_path / "fies_hogares_con_menores.csv", index=False)
    salida = metricas.metrica_fies(tmp_path, 2024)
    moderada = next(f for f in salida if f["categoria"] == "nivel=moderada_o_severa")
    # Probabilidad exactamente 0,5 no supera el umbral FAO (> 0,5): de 4
    # hogares califican 0,6 y 0,9.
    assert moderada["valor"] == 50.0
    con_chicos = next(f for f in salida
                      if f["categoria"] == "nivel=severa;hogares_con_menores_de_6")
    assert con_chicos["valor"] == 100.0
    assert con_chicos["n_muestral"] == 1


def test_metrica_fies_sin_archivo_no_inventa_filas(tmp_path):
    assert metricas.metrica_fies(tmp_path, 2024) == []


def test_metrica_victimizacion_por_delito_y_al_menos_uno(tmp_path):
    pd.DataFrame({
        "v3": [0, 0], "v4": [0, 0], "v5": [1, 0], "v6": [0, 0], "v7": [0, 0],
        "ponderador_victimizacion": [1.0, 3.0],
    }).to_csv(tmp_path / "victimizacion_hogares_con_nna.csv", index=False)
    salida = metricas.metrica_victimizacion(tmp_path, 2024)
    vivienda = next(f for f in salida if f["categoria"] == "delito=Robo en la vivienda")
    assert vivienda["valor"] == 25.0
    alguno = next(f for f in salida if f["categoria"] == "delito=Al menos uno")
    assert alguno["valor"] == 25.0
    assert len(salida) == len(metricas.TIPOS_DELITO) + 1


def test_metrica_trabajo_adolescente_promedia_meses_no_junta_el_pool(tmp_path):
    # Dos meses con pesos distintos: mes 1 da 50%, mes 2 da 75%. El
    # promedio de meses (regla heredada) es 62,5; juntar todo en un pool
    # daría 66,67 — el test falla si alguien "simplifica" el cálculo.
    pd.DataFrame({
        "edad": [15, 15, 16, 16, 13, 18],
        "mes": [1, 1, 2, 2, 1, 1],
        "condicion_actividad_cod": [2, 1, 2, 1, 2, 2],
        "sexo": [1, 1, 1, 1, 1, 1],
        "ponderador_empleo": [1.0, 1.0, 3.0, 1.0, 9.0, 9.0],
    }).to_csv(tmp_path / "empleo_14a17.csv", index=False)
    salida = metricas.metrica_trabajo_adolescente(tmp_path, 2024)
    total = next(f for f in salida if f["categoria"] == "ocupacion=total")
    assert total["valor"] == 62.5
    # Las filas de 13 y 18 años quedan fuera del universo 14-17.
    assert total["n_muestral"] == 4


def test_metrica_trabajo_adolescente_informalidad_solo_entre_ocupados(tmp_path):
    pd.DataFrame({
        "edad": [15, 15, 16],
        "mes": [1, 1, 1],
        "condicion_actividad_cod": [2, 2, 1],
        "sexo": [1, 1, 1],
        "ponderador_empleo": [1.0, 1.0, 5.0],
        "aporta_seguridad_social": [2.0, 1.0, 2.0],
    }).to_csv(tmp_path / "empleo_14a17.csv", index=False)
    salida = metricas.metrica_trabajo_adolescente(tmp_path, 2024)
    informal = next(f for f in salida if f["categoria"] == "informalidad_entre_ocupados")
    # El desocupado (peso 5) no entra al denominador: 1 de 2 ocupados.
    assert informal["valor"] == 50.0
    assert informal["n_muestral"] == 2


def test_anios_disponibles_lee_solo_carpetas_numericas(tmp_path):
    (tmp_path / "2023").mkdir()
    (tmp_path / "2019").mkdir()
    assert metricas.anios_disponibles(tmp_path) == [2019, 2023]
