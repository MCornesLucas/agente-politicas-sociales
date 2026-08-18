"""Configuración: rutas del proyecto y acceso al proyecto hermano.

El paquete encuesta_hogares (agente-encuesta-hogares) se importa desde la
copia de trabajo del proyecto hermano (su carpeta src/), no desde el
paquete instalado en site-packages: la copia instalada puede quedar
desactualizada respecto del desarrollo (al escribir esto: 0.4.0 instalada
contra 0.13.6 en el repositorio) y los loaders del hermano acumulan
correcciones verificadas contra los datos reales del INE que este
proyecto necesita heredar al día. Anteponer su src/ a sys.path garantiza
que se importe la copia de trabajo aunque exista una versión instalada.

La ruta se resuelve como carpeta hermana (ambos proyectos conviven en el
mismo directorio) y puede sobrescribirse con la variable de entorno
AGENTE_ECH_RUTA.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATOS_CURADOS = PROJECT_ROOT / "datos_curados"
RESULTADOS = PROJECT_ROOT / "resultados"
NOTEBOOKS = PROJECT_ROOT / "notebooks"
DOCS = PROJECT_ROOT / "docs"


def ruta_proyecto_ech() -> Path:
    """Ruta del proyecto hermano agente-encuesta-hogares."""
    definida = os.environ.get("AGENTE_ECH_RUTA")
    if definida:
        return Path(definida)
    return PROJECT_ROOT.parent / "agente-encuesta-hogares"


def preparar_import_ech() -> Path:
    """Antepone el src/ del proyecto hermano a sys.path y devuelve su ruta.

    Lanza ModuleNotFoundError (y no un ImportError genérico al primer uso)
    si el proyecto hermano no está donde se espera: el error dice qué
    falta y cómo indicarlo, en lugar de fallar más tarde con un
    "No module named encuesta_hogares" sin contexto.
    """
    ruta = ruta_proyecto_ech()
    src = ruta / "src"
    if not (src / "encuesta_hogares").is_dir():
        raise ModuleNotFoundError(
            "No se encontró el proyecto hermano agente-encuesta-hogares en "
            f"{ruta}. Clonarlo como carpeta hermana de este proyecto o "
            "definir la variable de entorno AGENTE_ECH_RUTA con su ruta."
        )
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    return ruta
