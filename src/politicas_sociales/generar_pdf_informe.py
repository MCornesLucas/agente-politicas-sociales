"""Genera el PDF del informe a partir del HTML sin código.

Replica el pipeline de agente-encuesta-hogares
(`docs/FLUJO_DE_TRABAJO.md`, sección 2, de ese repositorio): se toma el
HTML sin código, se le antepone una portada, se inyecta la hoja de
estilos de impresión (`docs/informe_estilo.css`, heredada — cada regla
resuelve un problema real de paginación: gráficas que no se cortan entre
páginas, tamaño A4, márgenes) y se imprime con Chromium sin interfaz vía
Playwright. No se usa `nbconvert --to pdf` porque depende de LaTeX
(pesado y frágil en Windows).

Salida: notebooks/Informe_Infancia.pdf + copia en Descargas.
"""

from __future__ import annotations

import datetime
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

from politicas_sociales import config
from politicas_sociales.entrega import respaldar_si_existe

HTML_ORIGEN = config.NOTEBOOKS / "informe_infancia.html"
CSS = config.DOCS / "informe_estilo.css"
HTML_IMPRESION = config.NOTEBOOKS / "_informe_infancia_impresion.html"
PDF_SALIDA = config.NOTEBOOKS / "Informe_Infancia.pdf"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def portada() -> str:
    hoy = datetime.date.today()
    fecha = f"{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"
    return f"""
<div class="portada">
  <h1>Pol&iacute;ticas sociales de infancia en Uruguay &mdash; Informe</h1>
  <div class="subtitulo">M&eacute;tricas descriptivas, proyecciones validadas y cruces entre
  fuentes del cat&aacute;logo del proyecto, con cada cifra respaldada por su fuente</div>
  <div class="meta">Generado el {fecha} &middot;
  Proyecto agente-politicas-sociales</div>
</div>
"""


def main() -> None:
    html = HTML_ORIGEN.read_text(encoding="utf-8")
    estilo = CSS.read_text(encoding="utf-8")

    html = html.replace("</head>", f"<style>\n{estilo}\n</style>\n</head>", 1)
    html = re.sub(r"(<body[^>]*>)", r"\1" + portada(), html, count=1)
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
    # La copia de Descargas no la versiona git: sin respaldo, volver a
    # generar el informe la pisaba sin aviso ni forma de recuperarla.
    respaldar_si_existe(descargas)
    shutil.copy(PDF_SALIDA, descargas)
    print(f"PDF generado: {PDF_SALIDA} ({PDF_SALIDA.stat().st_size / 1e6:.1f} MB)")
    print(f"Copia en Descargas: {descargas}")


if __name__ == "__main__":
    main()
