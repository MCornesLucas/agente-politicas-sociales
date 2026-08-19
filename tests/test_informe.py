"""Tests de la construcción del informe.

La versión actual del informe contiene las 36 métricas confirmadas del
catálogo (docs/CATALOGO_DE_METRICAS.md) y las 5 proyecciones calculadas.
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
    assert len(proyecciones) == 5


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
    # Resumen, conclusiones y fuentes van SIEMPRE (decisión del dueño,
    # 2026-08-19), con resumen y conclusiones filtrados por bloque.
    assert "## Resumen analítico" in texto
    assert "**Violencia (SIPIAV).**" in texto          # párrafo del tema elegido
    assert "**Pobreza y entorno (ECH).**" not in texto  # párrafo de otro tema
    assert "## Conclusiones" in texto
    assert "## Fuentes de datos y bibliografía" in texto
    assert "https://www.inau.gub.uy/sipiav" in texto


def test_la_bibliografia_se_imprime_en_el_informe():
    # Pedido del dueño (2026-08-19): quien recibe el PDF no tiene el
    # repositorio, así que las referencias tienen que estar impresas —
    # no basta con remitir a un archivo local. Modelo: el informe del
    # proyecto hermano, que imprime cada fuente con su dirección completa.
    celdas = construir_informe.celdas_del_informe(["tema_1"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    # Referencias completas de las citas que el informe usa en sus
    # justificaciones de gráfica.
    assert "Cleveland, W.S. & McGill, R. (1984)" in texto
    assert "Journal of the American Statistical Association" in texto
    assert "Healy, K. (2018)" in texto
    # Y las que respaldan el método de las proyecciones.
    assert "Hyndman, R.J. & Athanasopoulos, G." in texto
    assert "Shmueli, G. (2010)" in texto
    # Direcciones completas y visibles (en papel no hay clic).
    assert "<https://www.inau.gub.uy/sipiav>" in texto
    assert "<https://www4.ine.gub.uy/Anda5/>" in texto


def test_las_fuentes_no_remiten_a_rutas_locales_del_repositorio():
    # Decir "ver docs/BIBLIOGRAFIA.md" es inútil para quien solo tiene el
    # PDF: la referencia al material completo va por URL pública.
    celdas = construir_informe.celdas_del_informe(["tema_1"])
    fuentes = [c.source for c in celdas if c.cell_type == "markdown"
               and c.source.lstrip().startswith("## Fuentes de datos")]
    assert len(fuentes) == 1
    assert "docs/BIBLIOGRAFIA.md" not in fuentes[0]
    assert "datos_curados/" not in fuentes[0]
    assert "https://github.com/testa10/agente-politicas-sociales" in fuentes[0]


def test_la_firma_es_celda_propia_y_es_el_ancla_de_la_fuente_a_medida():
    # Decisión del dueño (2026-08-20, punto 3): cuando una edición lleva
    # métrica a medida, el agente inserta la nota de su fuente antes de
    # la celda de la firma. El ancla tiene que existir en TODA edición:
    # una celda propia que comienza con "---" y contiene la firma, última
    # del informe, inmediatamente después de la sección de fuentes.
    for seleccion in (None, ["tema_1"]):
        celdas = construir_informe.celdas_del_informe(seleccion)
        firma = celdas[-1]
        assert firma.cell_type == "markdown"
        assert firma.source.startswith("---"), seleccion
        assert "Informe generado por el proyecto" in firma.source
        # La celda anterior es el cierre de la sección de fuentes.
        assert "bibliografía completa del proyecto" in celdas[-2].source


def test_conclusiones_filtradas_por_bloque():
    # Edición solo de pobreza (tema_5): lleva la conclusión de pobreza y
    # las transversales, pero no las que se alimentan de otros temas.
    celdas = construir_informe.celdas_del_informe(["tema_5"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    assert "La pobreza uruguaya está concentrada en la infancia" in texto
    assert "Limitaciones declaradas de este informe" in texto  # "siempre"
    assert "La detección de la violencia llega tarde" not in texto  # tema_1
    # Edición de violencia (tema_1): al revés.
    celdas = construir_informe.celdas_del_informe(["tema_1"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    assert "La detección de la violencia llega tarde" in texto
    assert "La pobreza uruguaya está concentrada en la infancia" not in texto


def test_los_mapas_de_resumen_y_conclusiones_estan_alineados_con_las_celdas():
    # Si se agrega o quita un párrafo sin actualizar su mapa, una edición
    # parcial incluiría (o perdería) contenido en silencio.
    partes = construir_informe._particionar(CELDAS_1 + CELDAS_2)
    bloques_validos = set(construir_informe.SELECCIONABLES)
    for seccion, mapa in (("resumen", construir_informe.RESUMEN_BLOQUES),
                          ("conclusiones", construir_informe.CONCLUSIONES_BLOQUES)):
        celdas_seccion = partes[seccion][1:]  # sin el encabezado
        assert len(celdas_seccion) == len(mapa), seccion
        for aplica in mapa.values():
            assert aplica == "siempre" or (aplica and aplica <= bloques_validos)


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
    with pytest.raises(ValueError, match="al menos una métrica"):
        construir_informe.celdas_del_informe(["cruces"])


def test_bloques_disponibles_cuentan_el_contenido_real():
    bloques = {b["clave"]: b for b in construir_informe.bloques_disponibles()}
    assert sum(b["metricas"] for b in bloques.values()) == 36
    assert sum(b["proyecciones"] for b in bloques.values()) == 5
    assert bloques["cruces"]["cruces"] == 4
    assert all(bloques[t]["metricas"] > 0 for t in
               ("tema_1", "tema_2", "tema_3", "tema_4", "tema_5"))


def test_unidades_disponibles_con_explicacion_real():
    unidades = [u for b in construir_informe.unidades_disponibles()
                for u in b["unidades"]]
    assert len(unidades) == 45  # 36 métricas + 5 proyecciones + 4 cruces
    # Cada unidad lleva su explicación extraída de las celdas ("¿Qué
    # pregunta responde?"): si una celda pierde la pregunta, esto lo ve.
    sin_explicacion = [u["clave"] for u in unidades if not u["explicacion"]]
    assert sin_explicacion == []
    assert all(isinstance(u["requiere"], list) for u in unidades)


def test_seleccion_por_unidades_arma_solo_lo_elegido():
    celdas = construir_informe.celdas_del_informe(
        unidades=["metrica_1", "proyeccion_p1", "cruce_4"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    assert "### Métrica 1." in texto
    assert "### Proyección P1." in texto
    assert "### Cruce 4." in texto
    assert "### Métrica 2." not in texto      # misma sección, no elegida
    assert "### Cruce 1." not in texto
    assert "## Tema 1" in texto               # presentación del tema presente
    assert "## Tema 4" not in texto
    # La introducción parcial cuenta lo elegido de verdad.
    assert "1 métrica, 1 proyección, 1 cruce entre fuentes" in celdas[0].source


def test_todas_las_unidades_equivalen_al_informe_completo():
    todas = [u["clave"] for b in construir_informe.unidades_disponibles()
             for u in b["unidades"]]
    assert construir_informe.celdas_del_informe(unidades=todas) == CELDAS_1 + CELDAS_2


def test_unidad_desconocida_y_solo_cruces_se_rechazan():
    import pytest
    with pytest.raises(ValueError, match="desconocidas"):
        construir_informe.celdas_del_informe(unidades=["metrica_99"])
    with pytest.raises(ValueError, match="al menos una métrica"):
        construir_informe.celdas_del_informe(unidades=["cruce_1"])


def test_cli_interpreta_destino_bloques_y_unidades():
    destino, bloques, unidades = construir_informe._interpretar_argumentos(
        ["--destino", "notebooks/ediciones/edicion_x.ipynb", "tema_1", "metrica_12"])
    assert destino.name == "edicion_x.ipynb"
    assert bloques == ["tema_1"]
    assert unidades == ["metrica_12"]
    destino, bloques, unidades = construir_informe._interpretar_argumentos([])
    assert destino == construir_informe.DESTINO
    assert bloques is None and unidades is None


def test_las_dependencias_declaradas_se_autocompletan(monkeypatch):
    # Regla del dueño: elegir una unidad sin lo que necesita no es
    # posible — la selección se autocompleta (clausura transitiva).
    monkeypatch.setattr(construir_informe, "REQUIERE",
                        {"metrica_2": {"metrica_1"}, "metrica_3": {"metrica_2"}})
    celdas = construir_informe.celdas_del_informe(unidades=["metrica_3"])
    texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
    assert "### Métrica 1." in texto
    assert "### Métrica 2." in texto
    assert "### Métrica 3." in texto
