"""Tests de la pre-aprobación de la carpeta en Claude Code.

El módulo (creado por el dueño del proyecto — auto-aceptar un diálogo de
seguridad es decisión humana) toca el archivo de configuración de Claude
Code de toda la máquina: lo que se fija acá es que preserve todo lo que
no es suyo, que use el formato de clave que la propia CLI escribe
(barras de avance) y que ningún fallo lance una excepción — lo peor
permitido es que el diálogo aparezca una vez.
"""

import json

from politicas_sociales.preaprobar_confianza import preaprobar


def test_crea_el_archivo_si_no_existe(tmp_path):
    ruta = tmp_path / ".claude.json"
    proyecto = tmp_path / "mi-proyecto"
    proyecto.mkdir()
    assert preaprobar(ruta_config=ruta, proyecto=proyecto) is True
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    clave = proyecto.resolve().as_posix()
    # La clave va con barras de avance, como la escribe la propia CLI.
    assert "\\" not in clave
    assert datos["projects"][clave]["hasTrustDialogAccepted"] is True


def test_preserva_todo_lo_que_no_es_suyo(tmp_path):
    ruta = tmp_path / ".claude.json"
    proyecto = tmp_path / "mi-proyecto"
    proyecto.mkdir()
    existente = {
        "otraConfiguracion": {"tema": "oscuro"},
        "projects": {
            "C:/otro/proyecto": {"hasTrustDialogAccepted": True, "lastCost": 1.5},
        },
    }
    ruta.write_text(json.dumps(existente), encoding="utf-8")
    preaprobar(ruta_config=ruta, proyecto=proyecto)
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos["otraConfiguracion"] == {"tema": "oscuro"}
    assert datos["projects"]["C:/otro/proyecto"]["lastCost"] == 1.5
    assert datos["projects"][proyecto.resolve().as_posix()]["hasTrustDialogAccepted"] is True


def test_es_idempotente_y_no_reescribe_si_ya_estaba(tmp_path):
    ruta = tmp_path / ".claude.json"
    proyecto = tmp_path / "mi-proyecto"
    proyecto.mkdir()
    preaprobar(ruta_config=ruta, proyecto=proyecto)
    primera = ruta.read_text(encoding="utf-8")
    assert preaprobar(ruta_config=ruta, proyecto=proyecto) is True
    assert ruta.read_text(encoding="utf-8") == primera


def test_un_archivo_corrupto_no_lanza_ni_se_pisa(tmp_path):
    ruta = tmp_path / ".claude.json"
    ruta.write_text("{esto no es json", encoding="utf-8")
    proyecto = tmp_path / "mi-proyecto"
    proyecto.mkdir()
    # Falla avisando (False), sin excepción y SIN tocar el archivo: pisar
    # una configuración corrupta con una vacía borraría el resto de los
    # proyectos de la máquina.
    assert preaprobar(ruta_config=ruta, proyecto=proyecto) is False
    assert ruta.read_text(encoding="utf-8") == "{esto no es json"
