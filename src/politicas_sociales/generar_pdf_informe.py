"""Genera el PDF del informe a partir del HTML sin código.

Pipeline del PDF: se toma el
HTML sin código, se le antepone una portada, se inyecta la hoja de
estilos de impresión (`docs/informe_estilo.css` — cada regla
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
PDF_SALIDA = config.NOTEBOOKS / "Informe_Infancia.pdf"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


# La portada es texto visible del informe y no pasa por las celdas ni por
# los guardianes: se le aplican las mismas reglas del dueño (nada de
# "catálogo", "proyecto" ni temas numerados) y un test la vigila.
def portada() -> str:
    hoy = datetime.date.today()
    fecha = f"{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"
    return f"""
<div class="portada">
  <h1>Pol&iacute;ticas sociales de infancia en Uruguay &mdash; Informe</h1>
  <div class="subtitulo">M&eacute;tricas descriptivas, proyecciones validadas y cruces entre
  fuentes, con cada cifra respaldada por su fuente</div>
  <div class="meta">Generado el {fecha} con agente-politicas-sociales</div>
</div>
"""


def main(html_origen: Path = HTML_ORIGEN, pdf_salida: Path = PDF_SALIDA) -> None:
    html = html_origen.read_text(encoding="utf-8")
    estilo = CSS.read_text(encoding="utf-8")

    # El HTML intermedio de impresión vive junto al de origen, con nombre
    # derivado: dos ediciones distintas nunca chocan entre sí.
    html_impresion = html_origen.with_name(f"_{html_origen.stem}_impresion.html")
    html = html.replace("</head>", f"<style>\n{estilo}\n</style>\n</head>", 1)
    html = re.sub(r"(<body[^>]*>)", r"\1" + portada(), html, count=1)
    html_impresion.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_impresion.resolve().as_uri())
        page.pdf(
            path=str(pdf_salida),
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

    html_impresion.unlink(missing_ok=True)
    descargas = Path.home() / "Downloads" / pdf_salida.name
    # La copia de Descargas no la versiona git: sin respaldo, volver a
    # generar el informe la pisaba sin aviso ni forma de recuperarla.
    respaldar_si_existe(descargas)
    shutil.copy(pdf_salida, descargas)
    print(f"PDF generado: {pdf_salida} ({pdf_salida.stat().st_size / 1e6:.1f} MB)")
    print(f"Copia en Descargas: {descargas}")


if __name__ == "__main__":
    import sys
    argumentos = sys.argv[1:]
    if argumentos:
        html_cli = Path(argumentos[0])
        pdf_cli = (Path(argumentos[1]) if len(argumentos) > 1
                   else html_cli.with_suffix(".pdf"))
        main(html_cli, pdf_cli)
    else:
        main()
