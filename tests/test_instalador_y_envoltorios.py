"""Tests del instalador y del envoltorio run_python.bat.

Lección heredada del proyecto hermano: los guardianes y envoltorios sin
test contra la salida real fallan en silencio. run_python.bat se ejecuta
de verdad (con un python_path.txt sintético) y de instalar.bat se fijan
los contratos que el resto del proyecto asume: que escribe
.claude/python_path.txt, que verifica el proyecto hermano y que ninguna
pausa bloquea una corrida no interactiva.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
solo_windows = pytest.mark.skipif(sys.platform != "win32",
                                  reason="los .bat son de Windows")


@solo_windows
def test_run_python_ejecuta_el_python_de_python_path(tmp_path):
    # Copia real del envoltorio + un python_path.txt que apunta al Python
    # de esta corrida: si el .bat deja de leer el archivo o de reenviar
    # los argumentos, este test lo ve en la salida real.
    shutil.copy(RAIZ / "run_python.bat", tmp_path / "run_python.bat")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "python_path.txt").write_text(
        sys.executable + "\n", encoding="ascii")
    # Ruta explícita: en máquinas con NoDefaultCurrentDirectoryInExe,
    # cmd no resuelve un .bat por el directorio actual.
    resultado = subprocess.run(
        ["cmd", "/c", str(tmp_path / "run_python.bat"), "-c",
         "print('envoltorio ok')"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert resultado.returncode == 0
    assert "envoltorio ok" in resultado.stdout


@solo_windows
def test_run_python_sin_instalar_da_mensaje_claro(tmp_path):
    shutil.copy(RAIZ / "run_python.bat", tmp_path / "run_python.bat")
    resultado = subprocess.run(
        ["cmd", "/c", str(tmp_path / "run_python.bat"), "--version"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert resultado.returncode != 0
    assert "instalar.bat" in resultado.stdout


def test_instalar_escribe_python_path_y_verifica_al_hermano():
    contenido = (RAIZ / "instalar.bat").read_text(encoding="ascii")
    # Contratos que asume el resto del proyecto:
    assert ".claude\\python_path.txt" in contenido       # run_python.bat lo lee
    assert "agente-encuesta-hogares" in contenido        # dependencia no declarable en pip
    assert "AGENTE_ECH_RUTA" in contenido                # misma alternativa que config.py
    assert 'pip install -e ".[dev]"' in contenido
    assert "playwright install chromium" in contenido


def test_instalar_no_pausa_en_modo_no_interactivo():
    # Cada "pause" debe estar protegido por la variable de modo no
    # interactivo: una pausa suelta colgaria para siempre una corrida
    # automatizada (tests, agente).
    for linea in (RAIZ / "instalar.bat").read_text(encoding="ascii").splitlines():
        if linea.strip().lower() == "pause":
            pytest.fail(f"pause sin proteger: {linea!r}")
        if "pause" in linea.lower() and "NONINTERACTIVE" not in linea:
            pytest.fail(f"pause sin la variable de modo no interactivo: {linea!r}")
