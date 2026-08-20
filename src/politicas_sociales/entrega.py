"""Utilidades para la entrega final del informe: no perder en silencio un
informe generado antes cuando se vuelve a correr el flujo.

Los artefactos del repositorio los
versiona git, pero la copia de Descargas no: volver a generar el informe
la pisaba sin aviso ni forma de recuperarla.
"""

from __future__ import annotations

from pathlib import Path


def respaldar_si_existe(ruta: Path | str) -> Path | None:
    """Si ya existe un archivo en `ruta`, lo renombra a "<nombre> (anterior)"
    antes de que el llamador lo sobrescriba. Guarda una sola versión
    anterior (no acumula historial infinito). Devuelve la ruta del
    respaldo, o None si no había nada que respaldar."""
    ruta = Path(ruta)
    if not ruta.exists():
        return None
    respaldo = ruta.with_name(f"{ruta.stem} (anterior){ruta.suffix}")
    respaldo.unlink(missing_ok=True)
    ruta.rename(respaldo)
    return respaldo
