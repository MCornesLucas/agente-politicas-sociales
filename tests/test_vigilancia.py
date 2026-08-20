"""Tests de la vigilancia de fuentes de terceros.

Regla del proyecto: un chequeo que nunca se probó contra contenido que
NO cumple puede quedar verde por no mirar nada. Cada análisis se prueba
en las dos direcciones (deja pasar el estado conocido, reporta la
novedad) y además en su camino de estructura rota (ILEGIBLE) y de fuente
caída (NO ACCESIBLE) — verde solo cuando se miró de verdad.
"""

import json

import pytest

from politicas_sociales import vigilancia


# --- ANDA (microdatos ENSANNA) ---------------------------------------------

_CSV_ANDA = "id,idno,title,nation\n1,URY-INE-ECH-2024,\"Encuesta Continua de Hogares\",Uruguay\n"


def test_anda_sin_ensanna_no_es_novedad():
    r = vigilancia.analizar_anda(_CSV_ANDA, {"entradas_catalogo": 1, "entradas_ensanna": 0})
    assert r["estado"] == "sin_novedad"
    assert r["actual"] == {"entradas_catalogo": 1, "entradas_ensanna": 0}


def test_anda_con_ensanna_es_novedad():
    csv = _CSV_ANDA + "2,URY-INE-ENSANNA-2024,\"ENSANNA 2024\",Uruguay\n"
    r = vigilancia.analizar_anda(csv, {"entradas_catalogo": 1, "entradas_ensanna": 0})
    assert r["estado"] == "novedad"
    assert "ENSANNA" in r["detalle"]


def test_anda_menciona_si_el_catalogo_crecio():
    csv = _CSV_ANDA + "2,URY-INE-OTRA,\"Otra encuesta\",Uruguay\n"
    r = vigilancia.analizar_anda(csv, {"entradas_catalogo": 1, "entradas_ensanna": 0})
    assert r["estado"] == "sin_novedad"
    assert "entradas nuevas" in r["detalle"]


def test_anda_sin_encabezado_es_ilegible():
    r = vigilancia.analizar_anda("<html>mantenimiento</html>", {})
    assert r["estado"] == "ilegible"


# --- INE (estimaciones retrospectivas) --------------------------------------


def test_retrospectivas_ausentes_no_es_novedad():
    r = vigilancia.analizar_retrospectivas(
        "<html>Proyecciones revisión 2025 <a href='B11.xlsx'>B.1.1</a></html>",
        {"menciones_retrospectivas": 0})
    assert r["estado"] == "sin_novedad"


def test_retrospectivas_mencionadas_es_novedad():
    r = vigilancia.analizar_retrospectivas(
        "<html>Proyecciones revisión 2025: estimaciones retrospectivas 2012-2023 <a href='A11.xlsx'>A.1.1</a></html>",
        {"menciones_retrospectivas": 0})
    assert r["estado"] == "novedad"


def test_retrospectivas_pagina_cambiada_es_ilegible():
    r = vigilancia.analizar_retrospectivas("<html>Otra cosa</html>", {})
    assert r["estado"] == "ilegible"


# --- INAU (noticias CONAPEES/ESNNA) -----------------------------------------

_NOTICIA = '<a href="/noticias/2026/{slug}">x</a>'


def test_noticias_inau_sin_claves_no_es_novedad():
    html = _NOTICIA.format(slug="otro-tema")
    r = vigilancia.analizar_noticias_inau(html, {"noticias_vistas": []})
    assert r["estado"] == "sin_novedad"


def test_noticias_inau_con_clave_nueva_es_novedad():
    html = _NOTICIA.format(slug="conapees-presento-cifras")
    r = vigilancia.analizar_noticias_inau(html, {"noticias_vistas": []})
    assert r["estado"] == "novedad"
    assert "conapees-presento-cifras" in r["detalle"]


def test_noticias_inau_con_clave_ya_vista_no_repite_novedad():
    slug = "/noticias/2026/conapees-presento-cifras"
    html = f'<a href="{slug}">x</a>'
    r = vigilancia.analizar_noticias_inau(html, {"noticias_vistas": [slug]})
    assert r["estado"] == "sin_novedad"


def test_noticias_inau_sin_enlaces_es_ilegible():
    r = vigilancia.analizar_noticias_inau("<html>rediseño sin noticias</html>", {})
    assert r["estado"] == "ilegible"


# --- MTSS (página del CETI) --------------------------------------------------

_CETI_BASE = '<html>Comité Nacional para la Erradicación del Trabajo Infantil {cuerpo}</html>'
_ENLACE_CETI = '<a href="/ministerio-trabajo-seguridad-social/comunicacion/noticias/{slug}">x</a>'


def test_ceti_enlace_conocido_no_es_novedad():
    slug = "/ministerio-trabajo-seguridad-social/comunicacion/noticias/vieja"
    html = _CETI_BASE.format(cuerpo=f'<a href="{slug}">x</a>')
    r = vigilancia.analizar_ceti(html, {"enlaces_vistos": [slug]})
    assert r["estado"] == "sin_novedad"


def test_ceti_enlace_nuevo_es_novedad():
    html = _CETI_BASE.format(cuerpo=_ENLACE_CETI.format(slug="plan-de-accion-2026-2030"))
    r = vigilancia.analizar_ceti(html, {"enlaces_vistos": []})
    assert r["estado"] == "novedad"
    assert "plan-de-accion-2026-2030" in r["detalle"]


def test_ceti_sin_titulo_es_ilegible():
    r = vigilancia.analizar_ceti("<html>otra página</html>", {})
    assert r["estado"] == "ilegible"


def test_ceti_sin_enlaces_es_ilegible():
    r = vigilancia.analizar_ceti(_CETI_BASE.format(cuerpo=""), {})
    assert r["estado"] == "ilegible"


# --- UNICEF (biblioteca digital) ---------------------------------------------


def test_unicef_registros_conocidos_no_es_novedad():
    html = 'x notice_display&amp;id=28 y notice_display&amp;id=47'
    r = vigilancia.analizar_biblioteca_unicef(html, {"registros_vistos": [28, 47]})
    assert r["estado"] == "sin_novedad"


def test_unicef_registro_nuevo_es_novedad():
    html = 'x notice_display&amp;id=28 y notice_display&amp;id=999'
    r = vigilancia.analizar_biblioteca_unicef(html, {"registros_vistos": [28]})
    assert r["estado"] == "novedad"
    assert "999" in r["detalle"]


def test_unicef_conserva_en_el_baseline_los_registros_que_dejaron_de_verse():
    # Las páginas de tema muestran una selección: que un registro salga de
    # la vista no lo vuelve "nuevo" la próxima vez que aparezca.
    html = 'x notice_display&amp;id=28'
    r = vigilancia.analizar_biblioteca_unicef(html, {"registros_vistos": [28, 47]})
    assert r["estado"] == "sin_novedad"
    assert r["actual"]["registros_vistos"] == [28, 47]


def test_unicef_sin_registros_es_ilegible():
    r = vigilancia.analizar_biblioteca_unicef("<html>catálogo en mantenimiento</html>", {})
    assert r["estado"] == "ilegible"


# --- Integración: baseline, fuente caída y código de salida ------------------


def test_baseline_versionado_cubre_todas_las_fuentes():
    # Guardián de sincronía: una fuente nueva sin entrada en el baseline
    # (o una clave huérfana) rompe aquí, no en silencio en una corrida.
    baseline = json.loads(vigilancia.BASELINE.read_text(encoding="utf-8"))
    assert set(baseline) == {f["clave"] for f in vigilancia.FUENTES}


def test_fuente_caida_es_no_accesible_y_no_verde(monkeypatch):
    def caida(url):
        raise OSError("sin conexión")
    monkeypatch.setattr(vigilancia, "descargar", caida)
    resultados = vigilancia.revisar_fuentes()
    assert len(resultados) == len(vigilancia.FUENTES)
    assert all(r["estado"] == "no_accesible" for r in resultados)
    assert vigilancia.codigo_de_salida(resultados) == 1


def test_actualizar_baseline_se_niega_si_falta_una_fuente(tmp_path, monkeypatch):
    # Pisar el estado conocido con una corrida incompleta borraría la
    # referencia contra la que se detectan novedades.
    copia = tmp_path / "baseline.json"
    copia.write_text(vigilancia.BASELINE.read_text(encoding="utf-8"), encoding="utf-8")
    antes = copia.read_text(encoding="utf-8")
    monkeypatch.setattr(vigilancia, "BASELINE", copia)
    monkeypatch.setattr(vigilancia, "descargar", lambda url: (_ for _ in ()).throw(OSError("caída")))
    monkeypatch.setattr("sys.argv", ["vigilancia", "--actualizar-baseline"])
    with pytest.raises(SystemExit) as salida:
        vigilancia.main()
    assert salida.value.code == 1
    assert copia.read_text(encoding="utf-8") == antes


def test_codigo_de_salida():
    assert vigilancia.codigo_de_salida([{"estado": "sin_novedad"}]) == 0
    assert vigilancia.codigo_de_salida([{"estado": "sin_novedad"}, {"estado": "ilegible"}]) == 1
    assert vigilancia.codigo_de_salida([{"estado": "no_accesible"}, {"estado": "novedad"}]) == 2
