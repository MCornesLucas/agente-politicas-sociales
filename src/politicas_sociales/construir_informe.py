"""Construye el informe (notebooks/informe_infancia.ipynb).

Versión actual: las métricas confirmadas del catálogo (hoy 36, en 5
temas), las proyecciones calculadas (P1 con validación 2025, P2, P3, P4)
y el contexto demográfico (P6). El nombre no lleva "piloto" ni el texto
anuncia el catálogo completo: el informe es el producto del proyecto, y
qué métricas incluye cada versión es una decisión de quien lo pide, no
una promesa del título. Estructura estándar heredada de
agente-encuesta-hogares (docs/METODOLOGIA.md, sección 1): introducción,
preparación de datos, un tramo por tema con las cinco partes por
métrica, nota metodológica, resumen analítico y conclusiones. Español
neutro y formal; toda cifra con su fuente.

**Selección de bloques**: el usuario puede elegir qué temas (y si los
cruces) incluye su edición del informe. Las reglas de una edición
parcial, decididas con el dueño del proyecto:

- La infraestructura no se elige: introducción, preparación de datos,
  contexto demográfico (es transversal — "la demografía detrás de todas
  las tasas") y nota metodológica van siempre.
- El resumen analítico y las conclusiones solo van en el informe
  completo: son transversales a los cinco temas y citarían hallazgos de
  secciones que la edición no contiene.
- La introducción de una edición parcial describe lo que la edición
  realmente contiene — nunca promete contenido que no está.

Las celdas viven en informe_celdas_1.py (introducción y temas 1-3) y
informe_celdas_2.py (temas 4-5, cruces, contexto y cierre); los textos
citan únicamente valores verificados en datos_curados/, resultados/ y
los documentos de data/ (ver docs/RELEVAMIENTO_DE_DATOS.md).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat as nbf

from politicas_sociales import config
from politicas_sociales.informe_celdas_1 import CELDAS as CELDAS_1
from politicas_sociales.informe_celdas_1 import celda_introduccion
from politicas_sociales.informe_celdas_2 import CELDAS as CELDAS_2

DESTINO = config.NOTEBOOKS / "informe_infancia.ipynb"

# Los bloques que el usuario puede elegir, con el encabezado "## " que
# abre cada uno en las celdas y el nombre con el que se describe en la
# introducción de una edición parcial.
SELECCIONABLES = {
    "tema_1": ("## Tema 1", "violencia hacia niñas, niños y adolescentes (SIPIAV)"),
    "tema_2": ("## Tema 2", "explotación sexual (CONAPEES, Fiscalía)"),
    "tema_3": ("## Tema 3", "trabajo infantil (ENSANNA, ENTI, ECH)"),
    "tema_4": ("## Tema 4", "protección especial (INAU)"),
    "tema_5": ("## Tema 5", "pobreza, vivienda y entorno del hogar (ECH)"),
    "cruces": ("## Cruces entre fuentes", "los cruces entre fuentes contra la ECH"),
}
_TEMAS = [clave for clave in SELECCIONABLES if clave.startswith("tema_")]

# Bloques fijos (nunca se eligen) y bloques que solo van en el completo.
_FIJOS_INICIO = "inicio"          # introducción + preparación de datos
_FIJOS_FIN = ("contexto", "nota")  # contexto demográfico + nota metodológica
_SOLO_COMPLETO = ("resumen", "conclusiones")
_ENCABEZADOS_FIJOS = {
    "## Contexto transversal": "contexto",
    "## Nota metodológica": "nota",
    "## Resumen analítico": "resumen",
    "## Conclusiones": "conclusiones",
}


def _clave_de_encabezado(primera_linea: str) -> str | None:
    for clave, (encabezado, _) in SELECCIONABLES.items():
        if primera_linea.startswith(encabezado):
            return clave
    for encabezado, clave in _ENCABEZADOS_FIJOS.items():
        if primera_linea.startswith(encabezado):
            return clave
    return None


def _particionar(celdas) -> dict[str, list]:
    """Reparte las celdas en bloques según sus encabezados "## "."""
    partes: dict[str, list] = {_FIJOS_INICIO: []}
    actual = _FIJOS_INICIO
    for celda in celdas:
        if celda.cell_type == "markdown":
            primera = next((linea for linea in celda.source.split("\n") if linea.strip()), "")
            clave = _clave_de_encabezado(primera)
            if clave is not None:
                actual = clave
                partes.setdefault(actual, [])
        partes[actual].append(celda)
    return partes


def bloques_disponibles() -> list[dict]:
    """Los bloques seleccionables con sus conteos reales de contenido,
    contados desde las celdas (fuente única): lo que ofrece el formulario
    de catálogo nunca puede desalinearse de lo que el informe contiene."""
    partes = _particionar(CELDAS_1 + CELDAS_2)
    salida = []
    for clave, (_, nombre) in SELECCIONABLES.items():
        celdas = partes.get(clave, [])
        texto = "\n".join(c.source for c in celdas if c.cell_type == "markdown")
        salida.append({
            "clave": clave,
            "nombre": nombre,
            "titulo": next((linea.lstrip("# ").strip() for c in celdas
                            for linea in c.source.split("\n") if linea.startswith("## ")), nombre),
            "metricas": len(re.findall(r"^### Métrica ", texto, re.M)),
            "proyecciones": len(re.findall(r"^### Proyección ", texto, re.M)),
            "cruces": len(re.findall(r"^### Cruce ", texto, re.M)),
        })
    return salida


def _alcance_parcial(seleccion: set[str]) -> str:
    nombres = [SELECCIONABLES[c][1] for c in _TEMAS if c in seleccion]
    partes = "; ".join(nombres)
    alcance = (f"una selección del catálogo del proyecto — "
               f"{'los temas' if len(nombres) > 1 else 'el tema'}: {partes}")
    if "cruces" in seleccion:
        alcance += " — junto con los cruces entre fuentes contra la ECH, cada uno con sus limitaciones declaradas"
    alcance += (". El catálogo completo comprende cinco temas y cuatro "
                "cruces; esta edición contiene los bloques elegidos al generarla")
    return alcance


def celdas_del_informe(bloques: list[str] | None = None) -> list:
    """Las celdas del informe para la selección pedida.

    `None` (o la selección completa) devuelve el informe completo,
    idéntico al de siempre. Una selección parcial valida las claves,
    exige al menos un tema, reemplaza la introducción por una que
    describe la edición real, y omite el resumen analítico y las
    conclusiones (transversales a los cinco temas).
    """
    if bloques is None:
        return CELDAS_1 + CELDAS_2
    seleccion = set(bloques)
    desconocidos = seleccion - set(SELECCIONABLES)
    if desconocidos:
        raise ValueError(f"Bloques desconocidos: {sorted(desconocidos)}. "
                         f"Válidos: {sorted(SELECCIONABLES)}")
    if not seleccion & set(_TEMAS):
        raise ValueError("La selección necesita al menos un tema (el informe "
                         "no puede ser solo cruces).")
    if seleccion == set(SELECCIONABLES):
        return CELDAS_1 + CELDAS_2

    partes = _particionar(CELDAS_1 + CELDAS_2)
    celdas = [celda_introduccion(_alcance_parcial(seleccion))]
    celdas += partes[_FIJOS_INICIO][1:]  # preparación de datos, sin la intro original
    for clave in list(_TEMAS) + ["cruces"]:
        if clave in seleccion:
            celdas += partes.get(clave, [])
    for clave in _FIJOS_FIN:
        celdas += partes.get(clave, [])
    return celdas


def main(destino: Path = DESTINO, bloques: list[str] | None = None) -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = celdas_del_informe(bloques)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    destino.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, destino)
    n_metricas = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Métrica"))
    n_proy = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Proyección"))
    edicion = "completo" if bloques is None or set(bloques) == set(SELECCIONABLES) else f"parcial {sorted(set(bloques))}"
    print(f"Notebook escrito en {destino} ({edicion}): {len(nb.cells)} celdas, "
          f"{n_metricas} métricas, {n_proy} proyecciones.")


if __name__ == "__main__":
    main(bloques=sys.argv[1:] or None)
