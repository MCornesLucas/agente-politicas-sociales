"""Tests de la construcción del informe piloto.

El informe promete "el catálogo completo: 36 métricas en 5 temas" y las
4 proyecciones — la promesa está impresa en la introducción y en la
portada del PDF. Estos tests atan esa promesa al contenido real: si una
celda de métrica se borra o se renombra, la cifra anunciada deja de ser
cierta y la suite lo detecta.
"""

import nbformat as nbf

from politicas_sociales import construir_informe_piloto
from politicas_sociales.piloto_base import code, md
from politicas_sociales.piloto_celdas_1 import CELDAS as CELDAS_1
from politicas_sociales.piloto_celdas_2 import CELDAS as CELDAS_2


def test_md_y_code_crean_celdas_del_tipo_correcto_sin_bordes_en_blanco():
    celda_md = md("\n  # Título\n")
    assert celda_md.cell_type == "markdown"
    assert celda_md.source == "# Título"
    celda_code = code("\nx = 1\n")
    assert celda_code.cell_type == "code"
    assert celda_code.source == "x = 1"


def test_el_informe_contiene_las_36_metricas_y_4_proyecciones_anunciadas():
    celdas = CELDAS_1 + CELDAS_2
    metricas = [c for c in celdas
                if c.cell_type == "markdown" and c.source.startswith("### Métrica")]
    proyecciones = [c for c in celdas
                    if c.cell_type == "markdown" and c.source.startswith("### Proyección")]
    assert len(metricas) == 36
    assert len(proyecciones) == 4


def test_main_escribe_un_notebook_valido_y_completo(tmp_path):
    destino = tmp_path / "informe_piloto.ipynb"
    construir_informe_piloto.main(destino)
    nb = nbf.read(destino, as_version=4)
    nbf.validate(nb)
    assert len(nb.cells) == len(CELDAS_1) + len(CELDAS_2)
    assert nb.metadata["kernelspec"]["language"] == "python"
