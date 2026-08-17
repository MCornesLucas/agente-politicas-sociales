"""Genera el PDF del informe piloto a partir del HTML sin código.

Replica el pipeline de agente-encuesta-hogares
(`docs/FLUJO_DE_TRABAJO.md`, sección 2, de ese repositorio): se toma el
HTML sin código, se le antepone una portada, se inyecta la hoja de
estilos de impresión (`docs/informe_estilo.css`, heredada — cada regla
resuelve un problema real de paginación: gráficas que no se cortan entre
páginas, tamaño A4, márgenes) y se imprime con Chromium sin interfaz vía
Playwright. No se usa `nbconvert --to pdf` porque depende de LaTeX
(pesado y frágil en Windows).

Salida: notebooks/Informe_Piloto_Infancia.pdf + copia en Descargas.
"""

from __future__ import annotations

import datetime
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

PROYECTO = Path(__file__).resolve().parent.parent
HTML_ORIGEN = PROYECTO / "notebooks" / "informe_piloto.html"
CSS = PROYECTO / "docs" / "informe_estilo.css"
HTML_IMPRESION = PROYECTO / "notebooks" / "_informe_piloto_impresion.html"
PDF_SALIDA = PROYECTO / "notebooks" / "Informe_Piloto_Infancia.pdf"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
hoy = datetime.date.today()
fecha = f"{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"

PORTADA = f"""
<div class="portada">
  <h1>Pol&iacute;ticas sociales de infancia en Uruguay &mdash; Informe piloto</h1>
  <div class="subtitulo">Violencia, trabajo infantil y pobreza en ni&ntilde;as,
  ni&ntilde;os y adolescentes: an&aacute;lisis descriptivo y escenario inercial</div>
  <div class="meta">Generado el {fecha} &middot;
  Proyecto agente-politicas-sociales</div>
</div>
"""

html = HTML_ORIGEN.read_text(encoding="utf-8")
estilo = CSS.read_text(encoding="utf-8")

html = html.replace("</head>", f"<style>\n{estilo}\n</style>\n</head>", 1)
html = re.sub(r"(<body[^>]*>)", r"\1" + PORTADA, html, count=1)
HTML_IMPRESION.write_text(html, encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(HTML_IMPRESION.resolve().as_uri())
    page.pdf(
        path=str(PDF_SALIDA),
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template="<span></span>",
        footer_template=(
            '<div style="font-size:8pt; width:100%; text-align:center; '
            'color:#8b949e;">P&aacute;gina <span class="pageNumber"></span> '
            'de <span class="totalPages"></span></div>'
        ),
        margin={"top": "20mm", "bottom": "16mm", "left": "18mm", "right": "18mm"},
    )
    browser.close()

HTML_IMPRESION.unlink(missing_ok=True)
descargas = Path.home() / "Downloads" / PDF_SALIDA.name
shutil.copy(PDF_SALIDA, descargas)
print(f"PDF generado: {PDF_SALIDA} ({PDF_SALIDA.stat().st_size / 1e6:.1f} MB)")
print(f"Copia en Descargas: {descargas}")
