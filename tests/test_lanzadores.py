"""Tests de coherencia entre los lanzadores y el paquete.

Las piezas del flujo guiado (abrir_agente.bat, cierre.py, el agente y el
instalador) comparten nombres que tienen que coincidir letra por letra:
un prefijo de marca distinto o un modelo desalineado no da ningún error
— simplemente el cierre no encuentra la marca o el informe se genera con
otro modelo, en silencio.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from politicas_sociales import cierre

RAIZ = Path(__file__).resolve().parent.parent
node = shutil.which("node")


def test_abrir_agente_usa_las_variables_y_la_marca_de_cierre():
    contenido = (RAIZ / "abrir_agente.bat").read_text(encoding="ascii")
    assert cierre.VAR_ACTIVA in contenido
    assert cierre.VAR_PID_CONSOLA in contenido
    # El prefijo de la marca del .bat debe ser el mismo que usa cierre.py.
    assert f"{cierre._PREFIJO_MARCA}%{cierre.VAR_PID_CONSOLA}%.marker" in contenido
    assert "run_python.bat arranque.py" in contenido


def test_el_modelo_fijado_coincide_entre_lanzador_y_agente():
    bat = (RAIZ / "abrir_agente.bat").read_text(encoding="ascii")
    agente = (RAIZ / ".claude" / "agents" / "politicas-sociales.md").read_text(encoding="utf-8")
    modelo_bat = re.search(r"claude --model (\S+)", bat).group(1)
    modelo_agente = re.search(r"^model:\s*(\S+)", agente, re.M).group(1)
    assert modelo_bat == modelo_agente


def test_instalar_incluye_node_y_claude_code_fijado():
    contenido = (RAIZ / "instalar.bat").read_text(encoding="ascii")
    assert "where node" in contenido
    # Versión fijada, nunca "latest": un instalador que trae una versión
    # distinta según el día es indiagnosticable a distancia.
    assert re.search(r"@anthropic-ai/claude-code@\d+\.\d+\.\d+", contenido)
    assert "abrir_agente.bat" in contenido


def test_el_agente_existe_y_manda_usar_el_envoltorio():
    agente = (RAIZ / ".claude" / "agents" / "politicas-sociales.md").read_text(encoding="utf-8")
    assert "./run_python.bat" in agente
    assert "plantilla_bienvenida" in agente
    assert "mostrar_finalizacion" in agente
    # El primer paso del flujo es el formulario, nunca construir directo.
    assert "primera acción" in agente


@pytest.mark.skipif(node is None, reason="requiere Node.js")
@pytest.mark.parametrize("nombre_plantilla", ["plantilla_arranque", "plantilla_bienvenida",
                                              "plantilla_catalogo", "plantilla_finalizacion"])
def test_el_javascript_de_las_plantillas_es_valido(tmp_path, nombre_plantilla):
    # node --check sobre cada <script>: un error de sintaxis en el JS deja
    # el formulario mudo (el botón no hace nada) sin ningún aviso.
    from politicas_sociales import construir_informe, plantillas
    funcion = getattr(plantillas, nombre_plantilla)
    if nombre_plantilla == "plantilla_finalizacion":
        html = funcion(pdf_disponible=True, html_disponible=True)
    elif nombre_plantilla == "plantilla_catalogo":
        html = funcion(construir_informe.bloques_disponibles())
    else:
        html = funcion()
    scripts = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
    assert scripts, f"{nombre_plantilla} sin <script>"
    for i, script in enumerate(scripts):
        archivo = tmp_path / f"{nombre_plantilla}_{i}.js"
        archivo.write_text(script, encoding="utf-8")
        resultado = subprocess.run([node, "--check", str(archivo)],
                                   capture_output=True, text=True, timeout=60)
        assert resultado.returncode == 0, resultado.stderr


def test_json_de_ejemplo_del_agente_es_coherente_con_el_paquete():
    # Los imports que el agente copia textualmente tienen que existir.
    from politicas_sociales import formularios
    assert callable(formularios.mostrar_formulario)
    assert callable(formularios.mostrar_finalizacion)
    assert callable(formularios.plantilla_bienvenida)
    assert isinstance(json.loads('{"accion": "terminar"}'), dict)
