"""Tests de la configuración de rutas y del acceso al proyecto hermano."""

import sys

import pytest

from politicas_sociales import config


def test_project_root_es_la_raiz_del_repositorio():
    # La raíz debe contener las carpetas que definen al proyecto; si el
    # paquete se mueve de nivel, esto falla antes de que cualquier módulo
    # lea datos de una carpeta equivocada.
    assert (config.PROJECT_ROOT / "docs" / "METODOLOGIA.md").exists()
    assert (config.PROJECT_ROOT / "pyproject.toml").exists()
    assert config.DATOS_CURADOS == config.PROJECT_ROOT / "datos_curados"
    assert config.RESULTADOS == config.PROJECT_ROOT / "resultados"


def test_ruta_proyecto_ech_respeta_la_variable_de_entorno(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENTE_ECH_RUTA", str(tmp_path))
    assert config.ruta_proyecto_ech() == tmp_path


def test_preparar_import_ech_falla_con_mensaje_claro_si_no_existe(tmp_path, monkeypatch):
    # El error debe ser ModuleNotFoundError (y no un ImportError tardío
    # sin contexto): dice qué falta y cómo indicar la ruta.
    monkeypatch.setenv("AGENTE_ECH_RUTA", str(tmp_path / "no_existe"))
    with pytest.raises(ModuleNotFoundError, match="AGENTE_ECH_RUTA"):
        config.preparar_import_ech()


def test_preparar_import_ech_antepone_el_src_del_hermano(tmp_path, monkeypatch):
    (tmp_path / "src" / "encuesta_hogares").mkdir(parents=True)
    monkeypatch.setenv("AGENTE_ECH_RUTA", str(tmp_path))
    monkeypatch.setattr(sys, "path", list(sys.path))
    ruta = config.preparar_import_ech()
    assert ruta == tmp_path
    assert sys.path[0] == str(tmp_path / "src")
