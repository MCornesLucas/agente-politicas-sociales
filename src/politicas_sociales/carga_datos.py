"""Estado y ayudas del paso de datos del flujo guiado.

El formulario de datos (ver `plantillas.plantilla_datos`) se muestra en
TODAS las corridas y ofrece tres acciones cuyo estado depende de lo que
ya exista en `data/` (decisión del dueño, 2026-08-20):

1. **Carga automática** de las fuentes documentales (SIPIAV, INAU,
   ENSANNA, CETI, CONAPEES, INE, UNICEF). Tres estados (decisión del
   dueño, 2026-08-20): sin datos, el botón descarga todo
   (`descarga_fuentes.MANIFIESTO` + biblioteca UNICEF); con los datos ya
   cargados pero la vigilancia de terceros vencida (más de
   `DIAS_ENTRE_REVISIONES` desde la última corrida en esta máquina), el
   botón corre `politicas_sociales.vigilancia` para buscar novedades; con
   datos cargados y revisión al día, queda deshabilitado con su marca de
   listo.
2. **Carga manual de la ECH** — el agente crea las carpetas de año
   vacías en `data/ech_microdatos/` y abre el Explorador; el usuario
   descarga los microdatos del INE (aceptando sus términos él mismo) y
   los copia ahí. Los años esperados son los verificados por el
   pipeline: 2019 y de 2023 al año corriente — la ECH 2020-2022
   (relevamiento telefónico de pandemia) nunca se verificó aquí y no se
   ofrece. El botón queda deshabilitado cuando todos los esperados
   tienen datos de Hogares.
3. **Carga manual de la ENDIS** — igual que la ECH: el agente crea
   `data/endis_microdatos/2023/`, abre el Explorador y el usuario copia
   los microdatos de la ENDIS 2023 (catálogo ANDA, entrada 765) que
   descargó aceptando los términos del INE; al confirmar se recalcula
   la métrica de primera infancia (`metricas_endis`). El botón queda
   deshabilitado cuando la base de niño seleccionado ya está (en esa
   carpeta o como fuente propia registrada). Incorporado el 2026-09-05
   junto con el tema 6.
4. **Otras fuentes** — siempre habilitada: el usuario deja archivos
   propios en `data/usuario/<carpeta>/` para usarlos en métricas a
   medida. Cada fuente se registra con nombre y origen en
   `data/usuario/fuentes.json` para que el informe pueda citarla (regla
   del proyecto: toda cifra con su fuente).
"""

from __future__ import annotations

import datetime
import json
import re
import unicodedata

from . import config, descarga_fuentes, metricas_endis, vigilancia
from .ech import config as ech_config

CARPETA_USUARIO = config.DATA_DIR / "usuario"
REGISTRO_FUENTES_USUARIO = CARPETA_USUARIO / "fuentes.json"

# 2020-2022 quedan afuera a propósito (ECH telefónica de pandemia, nunca
# verificada por este pipeline); el año corriente se ofrece aunque el INE
# publique sus archivos recién avanzado el año siguiente.
_PRIMER_ANIO = 2019
_ANIOS_SIN_VERIFICAR = {2020, 2021, 2022}


def anios_ech_esperados(hoy: datetime.date | None = None) -> list[int]:
    hoy = hoy or datetime.date.today()
    return [a for a in range(_PRIMER_ANIO, hoy.year + 1)
            if a not in _ANIOS_SIN_VERIFICAR]


def anios_ech_cargados() -> list[int]:
    if not ech_config.DATA_DIR.is_dir():
        return []
    return sorted(
        int(p.name) for p in ech_config.DATA_DIR.iterdir()
        if p.is_dir() and p.name.isdigit()
        and ech_config.datos_disponibles(p.name)["hogares"]
    )


def preparar_carpetas_ech(hoy: datetime.date | None = None) -> str:
    """Crea las carpetas de año (vacías si no existían) y devuelve la ruta
    real y absoluta de `data/ech_microdatos/` para abrirla en el
    Explorador — nunca un placeholder ni una ruta relativa (lección de
    una corrida real: se llegó a mostrar una ruta relativa de Unix en vez
    de la ruta de Windows que el usuario necesitaba ver)."""
    for anio in anios_ech_esperados(hoy):
        (ech_config.DATA_DIR / str(anio)).mkdir(parents=True, exist_ok=True)
    return str(ech_config.DATA_DIR)


def endis_cargada() -> bool:
    """La base de niño seleccionado de la ENDIS 2023 está disponible: en
    `data/endis_microdatos/2023/` o como fuente propia registrada (que es
    donde la dejó la carga original del 2026-08-20). Una carpeta vacía no
    cuenta."""
    try:
        metricas_endis.localizar_microdatos()
    except FileNotFoundError:
        return False
    return True


def preparar_carpeta_endis() -> str:
    """Crea `data/endis_microdatos/2023/` (vacía si no existía) y devuelve
    su ruta real y absoluta para abrirla en el Explorador — misma regla
    que la ECH: nunca una ruta relativa ni inventada."""
    metricas_endis.DATOS.mkdir(parents=True, exist_ok=True)
    return str(metricas_endis.DATOS)


# Con los datos cargados, el botón de carga automática pasa a ofrecer la
# revisión de novedades cuando la última corrida de la vigilancia en esta
# máquina tiene más de este plazo (o nunca se corrió). Una vez al mes,
# por decisión del dueño (2026-08-20).
DIAS_ENTRE_REVISIONES = 30


def vigilancia_pendiente(hoy: datetime.date | None = None) -> bool:
    hoy = hoy or datetime.date.today()
    ultima = vigilancia.fecha_ultima_revision()
    return ultima is None or (hoy - ultima).days >= DIAS_ENTRE_REVISIONES


def automaticas_cargadas() -> bool:
    manifiesto_completo = all(
        descarga_fuentes.archivo_valido(config.DATA_DIR / e["destino"], e["tipo"])
        for e in descarga_fuentes.MANIFIESTO
    )
    return manifiesto_completo and bool(descarga_fuentes.ids_unicef_locales(config.DATA_DIR))


def estado_datos(hoy: datetime.date | None = None) -> dict:
    """El estado que consume `plantillas.plantilla_datos`."""
    esperados = anios_ech_esperados(hoy)
    cargados = [a for a in anios_ech_cargados() if a in esperados]
    return {
        "automaticas_listo": automaticas_cargadas(),
        "vigilancia_pendiente": vigilancia_pendiente(hoy),
        "ech_esperados": esperados,
        "ech_cargados": cargados,
        "ech_completo": bool(cargados) and set(esperados) <= set(cargados),
        "endis_listo": endis_cargada(),
    }


def _slug(nombre: str) -> str:
    plano = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
    limpio = re.sub(r"[^a-z0-9]+", "_", plano.lower()).strip("_")
    return limpio or "fuente"


def carpeta_fuente_usuario(nombre: str) -> str:
    """Crea (si hace falta) la carpeta de una fuente del usuario y
    devuelve su ruta real y absoluta para abrirla en el Explorador."""
    carpeta = CARPETA_USUARIO / _slug(nombre)
    carpeta.mkdir(parents=True, exist_ok=True)
    return str(carpeta)


def registrar_fuente_usuario(nombre: str, origen: str) -> list[str]:
    """Registra la fuente en `data/usuario/fuentes.json` y devuelve los
    archivos que el usuario dejó en su carpeta.

    Si la carpeta está vacía devuelve una lista vacía y NO registra nada:
    una fuente sin archivos no existe — el agente se lo dice al usuario
    en lugar de dar el paso por hecho.
    """
    carpeta = CARPETA_USUARIO / _slug(nombre)
    archivos = sorted(p.name for p in carpeta.iterdir() if p.is_file()) if carpeta.is_dir() else []
    if not archivos:
        return []
    registro = fuentes_usuario()
    registro = [f for f in registro if f["carpeta"] != _slug(nombre)]
    registro.append({
        "nombre": nombre.strip(),
        "origen": origen.strip(),
        "carpeta": _slug(nombre),
        "archivos": archivos,
        "fecha": datetime.date.today().isoformat(),
    })
    REGISTRO_FUENTES_USUARIO.parent.mkdir(parents=True, exist_ok=True)
    REGISTRO_FUENTES_USUARIO.write_text(
        json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return archivos


def fuentes_usuario() -> list[dict]:
    if not REGISTRO_FUENTES_USUARIO.is_file():
        return []
    return json.loads(REGISTRO_FUENTES_USUARIO.read_text(encoding="utf-8"))
