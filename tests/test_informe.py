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


def test_el_notebook_versionado_coincide_con_las_celdas():
    # Guardián de sincronía: si alguien edita informe_celdas_*.py y no
    # regenera el notebook (o al revés), el informe versionado deja de
    # ser el que producen los módulos — en silencio.
    from politicas_sociales import config
    versionado = nbf.read(config.NOTEBOOKS / "informe_infancia.ipynb", as_version=4)
    assert [c.source for c in versionado.cells] == \
        [c.source for c in construir_informe.celdas_del_informe(None)]


def test_seleccion_completa_es_identica_al_informe_de_siempre():
    todas = list(construir_informe.SELECCIONABLES)
    assert construir_informe.celdas_del_informe(todas) == CELDAS_1 + CELDAS_2
    assert construir_informe.celdas_del_informe(None) == CELDAS_1 + CELDAS_2


def test_edicion_parcial_incluye_lo_elegido_y_lo_fijo():
    celdas = construir_informe.celdas_del_informe(["tema_1"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    assert "## Tema 1" in texto
    assert "## Preparación de datos" in texto      # infraestructura fija
    assert "## Contexto transversal" in texto      # transversal, siempre
    assert "## Nota metodológica" in texto         # siempre
    assert "## Tema 4" not in texto
    assert "## Cruces entre fuentes" not in texto
    # Resumen y conclusiones son transversales: solo en el completo.
    assert "## Resumen analítico" not in texto
    assert "## Conclusiones" not in texto


def test_edicion_parcial_describe_su_alcance_real_en_la_introduccion():
    celdas = construir_informe.celdas_del_informe(["tema_1", "cruces"])
    intro = celdas[0].source
    assert "selección del catálogo" in intro
    assert "violencia hacia niñas, niños y adolescentes" in intro
    assert "cruces entre fuentes" in intro
    # La promesa del informe completo no puede quedar en una edición parcial.
    assert "cinco\ntemas** (" not in intro


def test_seleccion_invalida_se_rechaza():
    import pytest
    with pytest.raises(ValueError, match="desconocidos"):
        construir_informe.celdas_del_informe(["tema_9"])
    with pytest.raises(ValueError, match="al menos un tema"):
        construir_informe.celdas_del_informe(["cruces"])


def test_bloques_disponibles_cuentan_el_contenido_real():
    bloques = {b["clave"]: b for b in construir_informe.bloques_disponibles()}
    assert sum(b["metricas"] for b in bloques.values()) == 36
    assert sum(b["proyecciones"] for b in bloques.values()) == 4
    assert bloques["cruces"]["cruces"] == 4
    assert all(bloques[t]["metricas"] > 0 for t in
               ("tema_1", "tema_2", "tema_3", "tema_4", "tema_5"))
