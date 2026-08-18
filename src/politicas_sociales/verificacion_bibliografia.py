"""Verifica que todo enlace citado en el informe esté respaldado por la
bibliografía del proyecto.

Mecanismo heredado de `verificacion_bibliografia` del proyecto hermano
(allí: autores citados sin conectar a ningún patrón real), adaptado a la
regla de este proyecto que el dueño marcó como la más importante
(2026-08-19): las fuentes con sus enlaces validan los números y las
elecciones de cualquier edición del informe — y toda fuente nueva entra
a `docs/BIBLIOGRAFIA.md` en el mismo commit que la cita. Este módulo
convierte esa regla en un chequeo automático: si una celda del informe
cita un enlace que no está en la bibliografía (ni en
`docs/FUENTES_DE_DATOS.md`), la cita quedó sin respaldo.

No verifica que la cita esté bien aplicada (eso sigue siendo criterio
humano): solo que el enlace exista en los documentos de respaldo — la
señal mínima de que la fuente pasó por la curaduría del proyecto.
"""

from __future__ import annotations

import re

from . import config

_RESPALDOS = [
    config.DOCS / "BIBLIOGRAFIA.md",
    config.DOCS / "FUENTES_DE_DATOS.md",
]

# Enlaces del propio proyecto: no son fuentes de datos, son la firma del
# informe y la referencia a la infraestructura hermana — no corresponde
# pedirles entrada bibliográfica.
_PREFIJOS_EXENTOS = (
    "https://github.com/testa10/",
)

_PATRON_ENLACE = re.compile(r"https?://[^\s\)\]\">]+")


def _enlaces_de(texto: str) -> set[str]:
    return {enlace.rstrip(".,;") for enlace in _PATRON_ENLACE.findall(texto)}


def enlaces_del_informe() -> set[str]:
    """Todos los enlaces citados en las celdas del informe completo."""
    from politicas_sociales.informe_celdas_1 import CELDAS as CELDAS_1
    from politicas_sociales.informe_celdas_2 import CELDAS as CELDAS_2
    enlaces: set[str] = set()
    for celda in CELDAS_1 + CELDAS_2:
        if celda.cell_type == "markdown":
            enlaces |= _enlaces_de(celda.source)
    return enlaces


def enlaces_con_respaldo() -> set[str]:
    """Los enlaces presentes en los documentos de respaldo del proyecto."""
    enlaces: set[str] = set()
    for documento in _RESPALDOS:
        if documento.exists():
            enlaces |= _enlaces_de(documento.read_text(encoding="utf-8"))
    return enlaces


def enlaces_sin_respaldo() -> dict[str, str]:
    """Enlaces citados en el informe que no están en la bibliografía —
    `{enlace: razón}`, vacío si la regla se cumple."""
    respaldo = enlaces_con_respaldo()
    faltantes = {}
    for enlace in sorted(enlaces_del_informe()):
        if enlace.startswith(_PREFIJOS_EXENTOS):
            continue
        if enlace not in respaldo:
            faltantes[enlace] = (
                "citado en el informe pero ausente de docs/BIBLIOGRAFIA.md y "
                "docs/FUENTES_DE_DATOS.md — toda fuente nueva entra a la "
                "bibliografía en el mismo commit que la cita."
            )
    return faltantes
