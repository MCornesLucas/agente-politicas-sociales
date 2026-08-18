"""Configuración común de la suite.

El autouse redirige la bitácora de los hooks a un archivo temporal en
TODOS los tests, sin que ninguno tenga que acordarse de pedirlo. La
lección viene del proyecto hermano, donde el problema apareció dos
veces: tests escribiendo en la bitácora real de quien tenga el proyecto
en esa carpeta, con entradas indistinguibles de una corrida suya, justo
en el archivo que existe para reconstruir qué pasó.
"""

import pytest


@pytest.fixture(autouse=True)
def _bitacora_de_hooks_a_archivo_temporal(tmp_path, monkeypatch):
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(tmp_path / "bitacora_hooks.jsonl"))
