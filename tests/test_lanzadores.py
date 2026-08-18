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
    # Las corridas del flujo van a notebooks/ediciones/ (no versionada);
    # los informe_infancia.* oficiales no se tocan desde el flujo.
    assert "notebooks/ediciones/" in agente


def test_las_ediciones_de_usuario_no_se_versionan():
    # Hallazgo de la corrida real (2026-08-19): la edición de un usuario
    # pisaba el informe completo versionado del repositorio.
    gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8")
    assert "notebooks/ediciones/" in gitignore


def _html_de_plantilla(nombre_plantilla):
    from politicas_sociales import construir_informe, plantillas
    funcion = getattr(plantillas, nombre_plantilla)
    if nombre_plantilla == "plantilla_finalizacion":
        return funcion(pdf_disponible=True, html_disponible=True)
    if nombre_plantilla == "plantilla_catalogo":
        return funcion(construir_informe.bloques_disponibles())
    if nombre_plantilla == "plantilla_metricas":
        return funcion(construir_informe.unidades_disponibles())
    if nombre_plantilla == "plantilla_revision":
        return funcion(metrica_pedida="una métrica", problema="un problema",
                       alternativa="una alternativa")
    return funcion()


@pytest.mark.skipif(node is None, reason="requiere Node.js")
@pytest.mark.parametrize("nombre_plantilla", ["plantilla_arranque", "plantilla_bienvenida",
                                              "plantilla_catalogo", "plantilla_metricas",
                                              "plantilla_revision", "plantilla_finalizacion"])
def test_el_javascript_de_las_plantillas_es_valido(tmp_path, nombre_plantilla):
    # node --check sobre cada <script>: un error de sintaxis en el JS deja
    # el formulario mudo (el botón no hace nada) sin ningún aviso.
    html = _html_de_plantilla(nombre_plantilla)
    scripts = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
    assert scripts, f"{nombre_plantilla} sin <script>"
    for i, script in enumerate(scripts):
        archivo = tmp_path / f"{nombre_plantilla}_{i}.js"
        archivo.write_text(script, encoding="utf-8")
        resultado = subprocess.run([node, "--check", str(archivo)],
                                   capture_output=True, text=True, timeout=60)
        assert resultado.returncode == 0, resultado.stderr


def test_catalogo_sin_preseleccion_por_decision_del_dueno():
    # 2026-08-19: los bloques NO vienen marcados — elegir es del usuario,
    # no un valor por defecto.
    html = _html_de_plantilla("plantilla_catalogo")
    assert 'name="bloque"' in html
    # Ningún checkbox lleva el atributo checked (el ":checked" del
    # JavaScript es el selector, no el atributo).
    assert " checked>" not in html


def test_metricas_preseleccionadas_con_explicacion_y_campo_libre():
    html = _html_de_plantilla("plantilla_metricas")
    # Las 44 unidades vienen marcadas (son lo que el informe imprimirá
    # salvo que el usuario destilde) y cada una muestra su explicación.
    assert html.count('name="unidad"') == 44
    assert html.count(" checked>") == 44
    assert "¿Qué querés agregar" not in html  # el campo libre tiene su propio texto
    assert 'name="otra_metrica"' in html
    assert "Marcar todas" in html
    # Una explicación real extraída de las celdas, no redactada a mano.
    assert "¿Cómo evolucionó la cantidad de situaciones" in html


def test_revision_sin_alternativa_no_ofrece_el_boton():
    from politicas_sociales import plantillas
    html = plantillas.plantilla_revision(metrica_pedida="x", problema="y")
    assert "Usar la alternativa" not in html
    assert "Continuar sin la métrica nueva" in html
    con = plantillas.plantilla_revision(metrica_pedida="x", problema="y",
                                        alternativa="z")
    assert "Usar la alternativa" in con


_TODAS_LAS_PLANTILLAS = ["plantilla_arranque", "plantilla_bienvenida",
                         "plantilla_catalogo", "plantilla_metricas",
                         "plantilla_revision", "plantilla_finalizacion"]


@pytest.mark.parametrize("nombre_plantilla", _TODAS_LAS_PLANTILLAS)
def test_las_plantillas_no_vosean_ni_usan_regionalismos(nombre_plantilla):
    # Regla del proyecto (2026-08-19): lenguaje neutro y profesional en
    # todo lo que ve el usuario — el hermano vosea y al portar sus
    # plantillas el voseo se coló una vez; este guardián evita la
    # reincidencia.
    voseo = re.compile(
        r"\b(vos|elegí|marcá|hacé|mirá|podés|querés|tenés|sabés|destildá|"
        r"aguardá|acordate|fijate|avisame|contame|acá)\b", re.IGNORECASE)
    encontrados = voseo.findall(_html_de_plantilla(nombre_plantilla))
    assert encontrados == [], f"voseo/regionalismos en {nombre_plantilla}: {encontrados}"


def test_los_pasos_intermedios_permiten_volver():
    # Pedido del dueño (2026-08-19): tiene que existir una forma de
    # corregir una elección ya enviada sin salir del flujo.
    for plantilla in ("plantilla_catalogo", "plantilla_metricas"):
        html = _html_de_plantilla(plantilla)
        assert "Volver al paso anterior" in html, plantilla
        assert "volver: true" in html, plantilla


def test_json_de_ejemplo_del_agente_es_coherente_con_el_paquete():
    # Los imports que el agente copia textualmente tienen que existir.
    from politicas_sociales import formularios
    assert callable(formularios.mostrar_formulario)
    assert callable(formularios.mostrar_finalizacion)
    assert callable(formularios.plantilla_bienvenida)
    assert isinstance(json.loads('{"accion": "terminar"}'), dict)
