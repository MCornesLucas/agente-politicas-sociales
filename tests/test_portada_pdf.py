"""La portada del PDF es texto visible del informe que no pasa por las
celdas ni por los guardianes del notebook: el 2026-09-05 siguió diciendo
"catálogo del proyecto" después de haber limpiado todas las celdas.
Estas reglas del dueño se verifican aquí sobre la portada real."""

import html
import re

from politicas_sociales import generar_pdf_informe


def _texto_portada() -> str:
    # Sin etiquetas, con las entidades resueltas y los saltos de línea del
    # HTML colapsados: lo que ve el lector.
    texto = html.unescape(re.sub(r"<[^>]+>", " ", generar_pdf_informe.portada()))
    return re.sub(r"\s+", " ", texto)


def test_la_portada_no_remite_a_catalogo_proyecto_ni_temas_numerados():
    texto = _texto_portada()
    patron = re.compile(r"catálogo(?!\s+ANDA)|\bproyecto\b|\btemas?\s+\d", re.IGNORECASE)
    assert patron.search(texto) is None, texto


def test_la_portada_lleva_titulo_subtitulo_y_fecha():
    texto = _texto_portada()
    assert "Políticas sociales de infancia en Uruguay — Informe" in texto
    assert "cruces entre fuentes, con cada cifra respaldada por su fuente" in texto
    assert re.search(r"Generado el \d{1,2} de [a-z]+ de \d{4} con agente-politicas-sociales", texto)
