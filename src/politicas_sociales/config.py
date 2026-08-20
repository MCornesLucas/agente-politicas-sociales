"""Configuración: rutas del proyecto.

Los microdatos de la ECH viven en data/ech_microdatos/{año}/ y se cargan
con el subpaquete politicas_sociales.ech (rutas, columnas y loaders
propios, verificados contra los archivos oficiales del INE).
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATOS_CURADOS = PROJECT_ROOT / "datos_curados"
RESULTADOS = PROJECT_ROOT / "resultados"
NOTEBOOKS = PROJECT_ROOT / "notebooks"
DOCS = PROJECT_ROOT / "docs"
