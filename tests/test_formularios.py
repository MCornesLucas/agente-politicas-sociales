"""Tests del motor de formularios, contra el servidor real.

El "navegador" se simula monkeypatcheando el subprocess que lo abriría:
la función falsa captura la URL y responde por HTTP en un hilo — el
servidor, la validación de origen y el manejo de cuerpos inválidos se
prueban de verdad, no con dobles.
"""

import json
import subprocess
import threading
import time
import urllib.error
import urllib.request

import pytest

from politicas_sociales import bitacora, formularios


def _navegador_falso(monkeypatch, respondedor):
    """Reemplaza la apertura del navegador por `respondedor(url)` en un hilo."""
    def falso(cmd, **kwargs):
        url = cmd[-1]
        threading.Thread(target=respondedor, args=(url,), daemon=True).start()
        return subprocess.CompletedProcess(cmd, 0)
    monkeypatch.setattr(formularios.subprocess, "run", falso)


def _post(url, datos, origen=None):
    cuerpo = json.dumps(datos).encode("utf-8") if isinstance(datos, (dict, list)) else datos
    encabezados = {"Content-Type": "application/json"}
    if origen:
        encabezados["Origin"] = origen
    req = urllib.request.Request(url, data=cuerpo, headers=encabezados, method="POST")
    return urllib.request.urlopen(req, timeout=10)


def test_mostrar_formulario_devuelve_lo_que_respondio_el_usuario(monkeypatch):
    def responder(url):
        time.sleep(0.1)
        _post(url, {"accion": "empezar"})
    _navegador_falso(monkeypatch, responder)
    respuesta = formularios.mostrar_formulario("<h1>Prueba</h1>", timeout=15)
    assert respuesta == {"accion": "empezar"}


def test_post_de_otro_origen_se_rechaza_con_403(monkeypatch):
    rechazo = {}

    def responder(url):
        time.sleep(0.1)
        # Una página de otro sitio intenta responder el formulario en
        # nombre de la persona: 403 y el formulario sigue esperando.
        try:
            _post(url, {"accion": "empezar"}, origen="http://sitio-ajeno.example")
        except urllib.error.HTTPError as e:
            rechazo["codigo"] = e.code
        _post(url, {"accion": "de_verdad"})

    _navegador_falso(monkeypatch, responder)
    respuesta = formularios.mostrar_formulario("<h1>Prueba</h1>", timeout=15)
    assert rechazo["codigo"] == 403
    assert respuesta == {"accion": "de_verdad"}


def test_cuerpo_que_no_es_un_objeto_json_da_400(monkeypatch):
    rechazo = {}

    def responder(url):
        time.sleep(0.1)
        try:
            _post(url, [1, 2])  # JSON válido pero no un objeto
        except urllib.error.HTTPError as e:
            rechazo["codigo"] = e.code
        _post(url, {"ok": True})

    _navegador_falso(monkeypatch, responder)
    respuesta = formularios.mostrar_formulario("<h1>Prueba</h1>", timeout=15)
    assert rechazo["codigo"] == 400
    assert respuesta == {"ok": True}


def test_timeout_devuelve_salir_del_flujo(monkeypatch):
    _navegador_falso(monkeypatch, lambda url: None)  # nadie responde
    respuesta = formularios.mostrar_formulario("<h1>Prueba</h1>", timeout=0.3)
    # El chequeo estándar tras cualquier formulario cubre así también el
    # timeout, sin KeyError crudo (decisión heredada del hermano).
    assert respuesta["salir_del_flujo"] is True
    assert respuesta["motivo"] == "timeout"
    assert "formulario_timeout" in [e["tipo"] for e in bitacora.leer_eventos()]


def test_la_bitacora_guarda_la_respuesta_completa(monkeypatch):
    def responder(url):
        time.sleep(0.1)
        _post(url, {"accion": "generar"})
    _navegador_falso(monkeypatch, responder)
    formularios.mostrar_formulario("<h1>Con bitácora</h1>", timeout=15)
    respondido = next(e for e in bitacora.leer_eventos()
                      if e["tipo"] == "formulario_respondido")
    assert respondido["nombre"] == "Con bitácora"
    assert respondido["respuesta"] == {"accion": "generar"}


def test_finalizacion_sirve_el_pdf_y_devuelve_la_accion(tmp_path, monkeypatch):
    pdf = tmp_path / "informe.pdf"
    pdf.write_bytes(b"%PDF-falso")
    descargado = {}

    def responder(url):
        time.sleep(0.1)
        with urllib.request.urlopen(url + "informe.pdf", timeout=10) as r:
            descargado["bytes"] = r.read()
            descargado["tipo"] = r.headers["Content-Type"]
        _post(url, {"accion": "terminar"})

    _navegador_falso(monkeypatch, responder)
    respuesta = formularios.mostrar_finalizacion(pdf_path=str(pdf), timeout=15)
    assert respuesta == {"accion": "terminar"}
    assert descargado["bytes"] == b"%PDF-falso"
    assert descargado["tipo"] == "application/pdf"


def test_nombre_desde_html():
    assert formularios._nombre_desde_html("<h1>Hola <b>mundo</b></h1>") == "Hola mundo"
    assert formularios._nombre_desde_html("<p>sin titulo</p>") == "formulario"


@pytest.mark.parametrize("plantilla", [
    formularios.plantilla_arranque(),
    formularios.plantilla_bienvenida(),
    formularios.plantilla_finalizacion(pdf_disponible=True, html_disponible=True),
])
def test_las_plantillas_tienen_h1_para_la_bitacora(plantilla):
    assert formularios._nombre_desde_html(plantilla) != "formulario"
