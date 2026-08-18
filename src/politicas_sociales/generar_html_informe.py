"""Genera el HTML sin código del informe, a partir del notebook ejecutado.

Pasos 6-8 del flujo heredado de agente-encuesta-hogares
(`docs/FLUJO_DE_TRABAJO.md` de ese repositorio): verificar que ninguna
celda quedó con error, copiar el notebook filtrando los stderr de
matplotlib (warnings inofensivos, no errores), convertir a HTML con
`--no-input` (para público no técnico) y corregir el `<title>` (por
defecto queda el nombre del archivo).

Este paso vivía en un script de sesión fuera del repositorio — un hueco
real: el flujo del agente no podía reproducirlo. Ahora es un módulo del
paquete como los demás.

Salida: notebooks/informe_infancia.html
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat as nbf

from politicas_sociales import config

NOTEBOOK = config.NOTEBOOKS / "informe_infancia.ipynb"
COPIA = config.NOTEBOOKS / "_informe_infancia_sin_stderr.ipynb"
HTML = config.NOTEBOOKS / "informe_infancia.html"
TITULO = "Políticas sociales de infancia en Uruguay — Informe"


def main(notebook: Path = NOTEBOOK, html: Path = HTML) -> None:
    nb = nbf.read(notebook, as_version=4)

    errores = [o for c in nb.cells if c.cell_type == "code"
               for o in c.get("outputs", []) if o.get("output_type") == "error"]
    if errores:
        raise RuntimeError(
            f"El notebook tiene {len(errores)} celda(s) con error: no se "
            "genera el HTML de un informe roto."
        )

    copia = html.parent / COPIA.name
    for c in nb.cells:
        if c.cell_type == "code":
            c["outputs"] = [o for o in c["outputs"]
                            if not (o.get("output_type") == "stream"
                                    and o.get("name") == "stderr")]
    nbf.write(nb, copia)

    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html",
                    "--no-input", str(copia), "--output", html.stem,
                    "--output-dir", str(html.parent)], check=True)
    copia.unlink()

    contenido = html.read_text(encoding="utf-8")
    inicio = contenido.index("<title>")
    fin = contenido.index("</title>") + len("</title>")
    contenido = contenido[:inicio] + f"<title>{TITULO}</title>" + contenido[fin:]
    html.write_text(contenido, encoding="utf-8")
    print(f"HTML: {html} ({html.stat().st_size / 1e6:.1f} MB), título corregido.")


if __name__ == "__main__":
    argumentos = sys.argv[1:]
    if argumentos:
        notebook_cli = Path(argumentos[0])
        html_cli = (Path(argumentos[1]) if len(argumentos) > 1
                    else notebook_cli.with_suffix(".html"))
        main(notebook_cli, html_cli)
    else:
        main()
