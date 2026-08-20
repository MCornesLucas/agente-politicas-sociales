"""Tests de la configuración de rutas del proyecto y de los microdatos ECH."""

from politicas_sociales import config
from politicas_sociales.ech import config as ech_config


def test_project_root_es_la_raiz_del_repositorio():
    # La raíz debe contener las carpetas que definen al proyecto; si el
    # paquete se mueve de nivel, esto falla antes de que cualquier módulo
    # lea datos de una carpeta equivocada.
    assert (config.PROJECT_ROOT / "docs" / "METODOLOGIA.md").exists()
    assert (config.PROJECT_ROOT / "pyproject.toml").exists()
    assert config.DATOS_CURADOS == config.PROJECT_ROOT / "datos_curados"
    assert config.RESULTADOS == config.PROJECT_ROOT / "resultados"


def test_microdatos_ech_viven_dentro_del_proyecto():
    # La independencia del proyecto depende de que los loaders resuelvan
    # los microdatos DENTRO del repositorio, no en ninguna ruta externa.
    assert ech_config.PROJECT_ROOT == config.PROJECT_ROOT
    assert ech_config.DATA_DIR == config.DATA_DIR / "ech_microdatos"


def test_hogares_csv_file_reconoce_los_patrones_reales_del_ine(tmp_path, monkeypatch):
    # Los tres patrones observados en archivos reales: implantación con año
    # al medio (2025), implantación con año al final (2023) y el simple.
    monkeypatch.setattr(ech_config, "DATA_DIR", tmp_path)
    carpeta = tmp_path / "2023"
    carpeta.mkdir()
    assert ech_config.hogares_csv_file(2023) == carpeta / "ECH_2023.csv"
    (carpeta / "ECH_implantacion_2023.csv").touch()
    assert ech_config.hogares_csv_file(2023) == carpeta / "ECH_implantacion_2023.csv"
    (carpeta / "ECH_2023_implantacion.csv").touch()
    assert ech_config.hogares_csv_file(2023) == carpeta / "ECH_2023_implantacion.csv"


def test_empleo_files_prefiere_el_patron_largo_si_existe(tmp_path, monkeypatch):
    monkeypatch.setattr(ech_config, "DATA_DIR", tmp_path)
    carpeta = tmp_path / "2025"
    carpeta.mkdir()
    (carpeta / "ECH_01_2025.csv").touch()
    archivos = ech_config.empleo_files(2025)
    assert archivos[0] == carpeta / "ECH_01_2025.csv"      # existe: patrón largo
    assert archivos[1] == carpeta / "ECH_02_25.csv"        # no existe: cae al corto
    assert len(archivos) == 12


def test_datos_disponibles_sobre_un_anio_vacio(tmp_path, monkeypatch):
    monkeypatch.setattr(ech_config, "DATA_DIR", tmp_path)
    (tmp_path / "2030").mkdir()
    disponibles = ech_config.datos_disponibles(2030)
    assert disponibles == {
        "hogares": False, "fies": False, "empleo": False, "seguridad": False,
    }
