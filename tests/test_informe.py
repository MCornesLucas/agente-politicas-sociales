"""Tests de la construcción del informe.

La versión actual del informe contiene las 36 métricas confirmadas del
catálogo (docs/CATALOGO_DE_METRICAS.md) y las 4 proyecciones calculadas.
Los tests atan ese contenido al catálogo: si una celda de métrica se
borra o se renumera por accidente, la suite lo detecta. Cuando el
informe pase a construirse con métricas elegidas por el usuario, estos
conteos se ajustan a esa selección.
"""

import nbformat as nbf

from politicas_sociales import construir_informe
from politicas_sociales.informe_base import code, md
from politicas_sociales.informe_celdas_1 import CELDAS as CELDAS_1
from politicas_sociales.informe_celdas_2 import CELDAS as CELDAS_2


def test_md_y_code_crean_celdas_del_tipo_correcto_sin_bordes_en_blanco():
    celda_md = md("\n  # Título\n")
    assert celda_md.cell_type == "markdown"
    assert celda_md.source == "# Título"
    celda_code = code("\nx = 1\n")
    assert celda_code.cell_type == "code"
    assert celda_code.source == "x = 1"


def test_el_informe_contiene_las_36_metricas_confirmadas_y_4_proyecciones():
    celdas = CELDAS_1 + CELDAS_2
    metricas = [c for c in celdas
                if c.cell_type == "markdown" and c.source.startswith("### Métrica")]
    proyecciones = [c for c in celdas
                    if c.cell_type == "markdown" and c.source.startswith("### Proyección")]
    assert len(metricas) == 36
    assert len(proyecciones) == 4


def test_el_informe_ya_no_se_presenta_como_piloto_ni_promete_el_catalogo_completo():
    # Decisión del dueño del proyecto (2026-08-18): el informe no se
    # llama "piloto" y la introducción no anuncia "el catálogo completo"
    # — qué métricas incluye cada versión lo decide quien lo pide.
    introduccion = CELDAS_1[0].source
    assert "piloto" not in introduccion.lower()
    assert "catálogo completo" not in introduccion.lower()


def test_main_escribe_un_notebook_valido_y_completo(tmp_path):
    destino = tmp_path / "informe_infancia.ipynb"
    construir_informe.main(destino)
    nb = nbf.read(destino, as_version=4)
    nbf.validate(nb)
    assert len(nb.cells) == len(CELDAS_1) + len(CELDAS_2)
    assert nb.metadata["kernelspec"]["language"] == "python"
