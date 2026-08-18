"""Construye el informe piloto completo (notebooks/informe_piloto.ipynb).

Versión con el catálogo completo: 36 métricas descriptivas en 5 temas,
las proyecciones calculadas (P1 con validación 2025, P2, P3, P4) y el
contexto demográfico (P6). Estructura estándar heredada de
agente-encuesta-hogares (docs/METODOLOGIA.md, sección 1): introducción,
preparación de datos, un tramo por tema con las cinco partes por
métrica, nota metodológica, resumen analítico y conclusiones. Español
neutro y formal; toda cifra con su fuente.

Las celdas viven en src/piloto_celdas_1.py (introducción y temas 1-3) y
src/piloto_celdas_2.py (temas 4-5, contexto y cierre); los textos citan
únicamente valores verificados en datos_curados/, resultados/ y los
documentos de data/ (ver docs/RELEVAMIENTO_DE_DATOS.md).
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf

sys.path.insert(0, str(Path(__file__).resolve().parent))

from piloto_celdas_1 import CELDAS as CELDAS_1  # noqa: E402
from piloto_celdas_2 import CELDAS as CELDAS_2  # noqa: E402

PROYECTO = Path(__file__).resolve().parent.parent
DESTINO = PROYECTO / "notebooks" / "informe_piloto.ipynb"


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = CELDAS_1 + CELDAS_2
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, DESTINO)
    n_metricas = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Métrica"))
    n_proy = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Proyección"))
    print(f"Notebook escrito en {DESTINO}: {len(nb.cells)} celdas, "
          f"{n_metricas} métricas, {n_proy} proyecciones.")


if __name__ == "__main__":
    main()
