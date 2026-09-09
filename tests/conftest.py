"""Configuración común de la suite.

El autouse redirige la bitácora de los hooks a un archivo temporal en
TODOS los tests, sin que ninguno tenga que acordarse de pedirlo. La
lección viene de un problema real aparecido dos
veces: tests escribiendo en la bitácora real de quien tenga el proyecto
en esa carpeta, con entradas indistinguibles de una corrida suya, justo
en el archivo que existe para reconstruir qué pasó.

El segundo autouse hace lo mismo con el marcador de la última corrida
de la vigilancia (`logs/vigilancia_ultima_revision.json`): un test que
ejercita `vigilancia.main()` con la red simulada caída lo escribía de
verdad, y el paso de datos del flujo pasó a creer que la vigilancia se
había corrido ese día con las cinco fuentes "no accesibles" — así que
dejaba de ofrecerla durante un mes sin haber mirado nada (ocurrió el
2026-08-20 y el 2026-09-05).
"""

import pytest

from politicas_sociales import vigilancia


@pytest.fixture(autouse=True)
def _bitacora_de_hooks_a_archivo_temporal(tmp_path, monkeypatch):
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(tmp_path / "bitacora_hooks.jsonl"))


@pytest.fixture(autouse=True)
def _marcador_de_vigilancia_a_archivo_temporal(tmp_path, monkeypatch):
    monkeypatch.setattr(vigilancia, "ULTIMA_REVISION", tmp_path / "vigilancia_ultima_revision.json")
