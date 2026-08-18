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

**Selección de contenido** (flujo decidido con el dueño del proyecto):
el usuario elige primero los bloques (temas/cruces, sin preselección) y
después las unidades — cada métrica, proyección o cruce individual — en
un segundo formulario que muestra la explicación real de cada una.
Reglas de una edición parcial:

- La infraestructura no se elige: introducción, preparación de datos,
  contexto demográfico (es transversal), nota metodológica y la sección
  de **fuentes de datos y bibliografía** van siempre — decisión del
  dueño (2026-08-19): las fuentes con sus enlaces validan los números y
  las elecciones de cualquier edición. La presentación de un tema va
  siempre que la edición incluya al menos una unidad del tema.
- Las **conclusiones van siempre**, filtradas por bloque (decisión del
  dueño, 2026-08-19): cada conclusión declara en CONCLUSIONES_BLOQUES de
  qué bloques se alimenta y una edición incluye las de sus bloques (las
  transversales, marcadas "siempre", van en todas). El resumen analítico
  sí queda solo en el informe completo.
- La introducción de una edición parcial describe lo que la edición
  realmente contiene — nunca promete contenido que no está.
- Cada unidad es auto-contenida (sus celdas solo dependen de la
  preparación de datos): los helpers compartidos (serie_sipiav,
  serie_inau, spearmanr) viven en la celda de preparación, verificado
  ejecutando cada unidad sola contra los datos reales. Si alguna vez una
  unidad necesita de otra, se declara en REQUIERE y la selección se
  autocompleta con las requeridas — nunca se permite elegir una unidad
  sin lo que necesita (regla del dueño del proyecto).

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

# Dependencias declaradas entre unidades: unidad -> unidades que necesita.
# Hoy está vacío porque todas las unidades son auto-contenidas (los
# helpers compartidos viven en la preparación de datos, verificado
# ejecutando cada unidad sola). Si una unidad nueva necesitara de otra,
# se declara acá y la selección se autocompleta — elegirla sin su
# requerida no es posible.
REQUIERE: dict[str, set[str]] = {}

# Bloques fijos (nunca se eligen) y bloques que solo van en el completo.
_FIJOS_INICIO = "inicio"          # introducción + preparación de datos
_FIJOS_FIN = ("contexto", "nota")  # contexto demográfico + nota metodológica
_ENCABEZADOS_FIJOS = {
    "## Contexto transversal": "contexto",
    "## Nota metodológica": "nota",
    "## Resumen analítico": "resumen",
    "## Conclusiones": "conclusiones",
    "## Fuentes de datos": "fuentes",
}

# Cada conclusión (celda i-ésima después del encabezado "## Conclusiones")
# declara de qué bloques se alimenta; una edición parcial incluye las de
# sus bloques y las transversales ("siempre"). Un test mantiene este mapa
# alineado con la cantidad real de celdas de conclusión.
CONCLUSIONES_BLOQUES: dict[int, set[str] | str] = {
    0: {"tema_5"},                 # pobreza concentrada en la infancia
    1: {"tema_1", "tema_4"},       # sistemas en expansión, infancia en contracción
    2: {"tema_1"},                 # detección tardía, intervención pierde a la familia
    3: {"tema_1", "tema_2"},       # violencia sexual adolescente y de género
    4: {"tema_1"},                 # Uruguay no mide prevalencia
    5: "siempre",                  # limitaciones declaradas del informe
}

# Una unidad seleccionable dentro de un bloque: métrica, proyección o cruce.
_PATRON_UNIDAD = re.compile(r"^#{2,4}\s*(?:Métrica (\d+)\.|Proyección (P\d+)\.|Cruce (\d+)\.)")
_PATRON_PREGUNTA = re.compile(r"\*\*¿Qué pregunta responde\?\*\*\s*(.+?)(?:\n\n|$)", re.S)


def _clave_de_encabezado(primera_linea: str) -> str | None:
    for clave, (encabezado, _) in SELECCIONABLES.items():
        if primera_linea.startswith(encabezado):
            return clave
    for encabezado, clave in _ENCABEZADOS_FIJOS.items():
        if primera_linea.startswith(encabezado):
            return clave
    return None


def _clave_de_unidad(primera_linea: str) -> str | None:
    m = _PATRON_UNIDAD.match(primera_linea)
    if not m:
        return None
    if m.group(1):
        return f"metrica_{m.group(1)}"
    if m.group(2):
        return f"proyeccion_{m.group(2).lower()}"
    return f"cruce_{m.group(3)}"


def _primera_linea(celda) -> str:
    return next((linea for linea in celda.source.split("\n") if linea.strip()), "")


def _particionar(celdas) -> dict:
    """Reparte las celdas en bloques (por encabezado "## ") y, dentro de
    los bloques seleccionables, en la introducción del bloque y sus
    unidades (por encabezado "### Métrica/Proyección/Cruce")."""
    partes: dict = {_FIJOS_INICIO: []}
    bloque, unidad = _FIJOS_INICIO, None
    for celda in celdas:
        if celda.cell_type == "markdown":
            primera = _primera_linea(celda)
            clave_bloque = _clave_de_encabezado(primera)
            if clave_bloque is not None:
                bloque, unidad = clave_bloque, None
                if clave_bloque in SELECCIONABLES:
                    partes.setdefault(bloque, {"intro": [], "unidades": {}, "orden": []})
                else:
                    partes.setdefault(bloque, [])
            elif bloque in SELECCIONABLES:
                clave_unidad = _clave_de_unidad(primera)
                if clave_unidad is not None:
                    unidad = clave_unidad
                    partes[bloque]["unidades"][unidad] = []
                    partes[bloque]["orden"].append(unidad)
        if bloque in SELECCIONABLES:
            destino = (partes[bloque]["unidades"][unidad] if unidad
                       else partes[bloque]["intro"])
            destino.append(celda)
        else:
            partes[bloque].append(celda)
    return partes


def _titulo_de(celdas_unidad) -> str:
    return _primera_linea(celdas_unidad[0]).lstrip("# ").strip()


def _explicacion_de(celdas_unidad) -> str:
    """La pregunta que responde la unidad, extraída de su propia celda —
    la explicación del formulario nunca puede desalinearse del informe."""
    texto = "\n".join(c.source for c in celdas_unidad if c.cell_type == "markdown")
    m = _PATRON_PREGUNTA.search(texto)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def unidades_disponibles(bloques: list[str] | None = None) -> list[dict]:
    """Los bloques con sus unidades (título, explicación real y
    dependencias declaradas), para el formulario de selección fina."""
    partes = _particionar(CELDAS_1 + CELDAS_2)
    salida = []
    for clave, (_, nombre) in SELECCIONABLES.items():
        if bloques is not None and clave not in bloques:
            continue
        bloque = partes.get(clave)
        if not bloque:
            continue
        titulo = next((_primera_linea(c).lstrip("# ").strip()
                       for c in bloque["intro"] if c.cell_type == "markdown"
                       and _primera_linea(c).startswith("## ")), nombre)
        salida.append({
            "clave": clave,
            "nombre": nombre,
            "titulo": titulo,
            "unidades": [{
                "clave": u,
                "titulo": _titulo_de(bloque["unidades"][u]),
                "explicacion": _explicacion_de(bloque["unidades"][u]),
                "requiere": sorted(REQUIERE.get(u, set())),
            } for u in bloque["orden"]],
        })
    return salida


def bloques_disponibles() -> list[dict]:
    """Los bloques seleccionables con sus conteos reales de contenido."""
    salida = []
    for bloque in unidades_disponibles():
        claves = [u["clave"] for u in bloque["unidades"]]
        salida.append({
            "clave": bloque["clave"],
            "nombre": bloque["nombre"],
            "titulo": bloque["titulo"],
            "metricas": sum(1 for c in claves if c.startswith("metrica_")),
            "proyecciones": sum(1 for c in claves if c.startswith("proyeccion_")),
            "cruces": sum(1 for c in claves if c.startswith("cruce_")),
        })
    return salida


def _todas_las_unidades(partes) -> dict[str, str]:
    """Mapa unidad → bloque, en el orden del informe."""
    mapa = {}
    for clave in SELECCIONABLES:
        for unidad in partes.get(clave, {}).get("orden", []):
            mapa[unidad] = clave
    return mapa


def _cerrar_dependencias(seleccion: set[str]) -> set[str]:
    """Autocompleta la selección con las unidades requeridas (clausura
    transitiva de REQUIERE): elegir una unidad sin lo que necesita no es
    posible — la regla del dueño del proyecto."""
    cerrada = set(seleccion)
    pendientes = list(seleccion)
    while pendientes:
        for requerida in REQUIERE.get(pendientes.pop(), set()):
            if requerida not in cerrada:
                cerrada.add(requerida)
                pendientes.append(requerida)
    return cerrada


def _alcance_parcial(partes, seleccion: set[str]) -> str:
    mapa = _todas_las_unidades(partes)
    bloques_presentes = [c for c in _TEMAS if any(mapa[u] == c for u in seleccion)]
    n_metricas = sum(1 for u in seleccion if u.startswith("metrica_"))
    n_proy = sum(1 for u in seleccion if u.startswith("proyeccion_"))
    n_cruces = sum(1 for u in seleccion if u.startswith("cruce_"))
    contenido = []
    if n_metricas:
        contenido.append(f"{n_metricas} métrica{'s' if n_metricas != 1 else ''}")
    if n_proy:
        contenido.append(f"{n_proy} proyección{'es' if n_proy != 1 else ''}")
    if n_cruces:
        contenido.append(f"{n_cruces} cruce{'s' if n_cruces != 1 else ''} entre fuentes")
    nombres = "; ".join(SELECCIONABLES[c][1] for c in bloques_presentes)
    alcance = (f"una selección del catálogo del proyecto — {', '.join(contenido)} — "
               f"{'en los temas' if len(bloques_presentes) > 1 else 'en el tema'}: {nombres}")
    alcance += (". El catálogo completo comprende cinco temas y cuatro "
                "cruces; esta edición contiene lo elegido al generarla")
    return alcance


def _normalizar_seleccion(partes, bloques, unidades) -> set[str]:
    mapa = _todas_las_unidades(partes)
    seleccion: set[str] = set()
    if bloques is not None:
        desconocidos = set(bloques) - set(SELECCIONABLES)
        if desconocidos:
            raise ValueError(f"Bloques desconocidos: {sorted(desconocidos)}. "
                             f"Válidos: {sorted(SELECCIONABLES)}")
        seleccion |= {u for u, b in mapa.items() if b in set(bloques)}
    if unidades is not None:
        desconocidas = set(unidades) - set(mapa)
        if desconocidas:
            raise ValueError(f"Unidades desconocidas: {sorted(desconocidas)}. "
                             f"Válidas: {sorted(mapa)}")
        seleccion |= set(unidades)
    seleccion = _cerrar_dependencias(seleccion)
    if not any(mapa[u] in _TEMAS for u in seleccion):
        raise ValueError("La selección necesita al menos una métrica o "
                         "proyección de un tema (el informe no puede ser "
                         "solo cruces).")
    return seleccion


def celdas_del_informe(bloques: list[str] | None = None,
                       unidades: list[str] | None = None) -> list:
    """Las celdas del informe para la selección pedida.

    Sin selección devuelve el informe completo, idéntico al de siempre;
    también si la selección cubre todas las unidades. `bloques` suma
    bloques enteros; `unidades` suma métricas, proyecciones o cruces
    individuales (claves de `unidades_disponibles()`); pueden combinarse.
    """
    if bloques is None and unidades is None:
        return CELDAS_1 + CELDAS_2
    partes = _particionar(CELDAS_1 + CELDAS_2)
    seleccion = _normalizar_seleccion(partes, bloques, unidades)
    mapa = _todas_las_unidades(partes)
    if seleccion == set(mapa):
        return CELDAS_1 + CELDAS_2

    celdas = [celda_introduccion(_alcance_parcial(partes, seleccion))]
    celdas += partes[_FIJOS_INICIO][1:]  # preparación de datos, sin la intro original
    for clave in list(_TEMAS) + ["cruces"]:
        bloque = partes.get(clave)
        if not bloque:
            continue
        elegidas = [u for u in bloque["orden"] if u in seleccion]
        if not elegidas:
            continue
        celdas += bloque["intro"]
        for unidad in elegidas:
            celdas += bloque["unidades"][unidad]
    for clave in _FIJOS_FIN:
        celdas += partes.get(clave, [])
    # Conclusiones: siempre, filtradas por los bloques presentes en la
    # edición; las transversales ("siempre") van en todas.
    bloques_presentes = {mapa[u] for u in seleccion}
    conclusiones = partes.get("conclusiones", [])
    if conclusiones:
        celdas.append(conclusiones[0])  # encabezado "## Conclusiones"
        for indice, celda in enumerate(conclusiones[1:]):
            aplica = CONCLUSIONES_BLOQUES.get(indice, "siempre")
            if aplica == "siempre" or aplica & bloques_presentes:
                celdas.append(celda)
    # Fuentes de datos y bibliografía: en toda edición, sin excepción.
    celdas += partes.get("fuentes", [])
    return celdas


def main(destino: Path = DESTINO, bloques: list[str] | None = None,
         unidades: list[str] | None = None) -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = celdas_del_informe(bloques, unidades)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    destino.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, destino)
    n_metricas = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Métrica"))
    n_proy = sum(1 for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### Proyección"))
    completo = bloques is None and unidades is None
    edicion = "completo" if completo else f"parcial {sorted(set(bloques or []) | set(unidades or []))}"
    print(f"Notebook escrito en {destino} ({edicion}): {len(nb.cells)} celdas, "
          f"{n_metricas} métricas, {n_proy} proyecciones.")


def _interpretar_argumentos(argumentos: list[str]) -> tuple[Path, list[str] | None, list[str] | None]:
    """CLI: claves de bloque y/o unidad, más `--destino <ruta>` opcional
    (las ediciones del flujo guiado van a notebooks/ediciones/, nunca
    sobre los informe_infancia.* oficiales del repositorio)."""
    destino = DESTINO
    if "--destino" in argumentos:
        indice = argumentos.index("--destino")
        destino = Path(argumentos[indice + 1])
        argumentos = argumentos[:indice] + argumentos[indice + 2:]
    bloques_cli = [a for a in argumentos if a in SELECCIONABLES] or None
    unidades_cli = [a for a in argumentos if a not in SELECCIONABLES] or None
    return destino, bloques_cli, unidades_cli


if __name__ == "__main__":
    destino_cli, bloques_cli, unidades_cli = _interpretar_argumentos(sys.argv[1:])
    main(destino_cli, bloques=bloques_cli, unidades=unidades_cli)
