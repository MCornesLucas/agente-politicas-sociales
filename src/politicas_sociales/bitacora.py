"""Bitácora local de sesiones: qué formularios se mostraron, cuánto tardó
cada paso pesado, y si algo falló — todo en la propia computadora del
usuario, sin salir a internet.

Nació de un punto ciego real:
cuando algo sale mal para alguien sin conocimientos técnicos, la única
forma de enterarse era que esa persona lo describiera de memoria. Con la
bitácora, el dueño del proyecto pide un solo archivo
(`logs/bitacora.jsonl`) y reconstruye qué pasó con datos objetivos.
Nunca se sube a git (ver .gitignore) y nunca sale de la computadora.

Regla de contenido: se registran las respuestas completas de los
formularios — seguro HOY porque ninguno pide datos personales (botones y
opciones). Si algún día un formulario pidiera un nombre o un mail, ese
registro pasa a guardar solo los campos inocuos, elegidos a mano.

La variable de entorno POLITICAS_SOCIALES_BITACORA redirige el archivo:
es la misma que usan los hooks de .claude/hooks y la usa la suite de
tests para no escribir jamás en la bitácora real (lección aprendida dos
veces en corridas reales). Se consulta en cada escritura, no al
importar, para que la redirección de un test llegue siempre a tiempo.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import traceback
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from . import config

# La bitácora crece indefinidamente en una instalación que se use seguido.
# Al llegar a este tamaño se guarda como ".1" y se arranca de nuevo: una
# sola tanda anterior alcanza para diagnosticar (importa lo reciente).
_TAMANIO_MAXIMO_EN_BYTES = 2_000_000


def ruta_log() -> Path:
    definida = os.environ.get("POLITICAS_SOCIALES_BITACORA")
    if definida:
        return Path(definida)
    return config.PROJECT_ROOT / "logs" / "bitacora.jsonl"


def _rotar_si_hace_falta(log: Path) -> None:
    try:
        if log.exists() and log.stat().st_size >= _TAMANIO_MAXIMO_EN_BYTES:
            anterior = log.with_suffix(log.suffix + ".1")
            anterior.unlink(missing_ok=True)
            log.rename(anterior)
    except OSError:
        pass


def registrar(tipo: str, **detalle) -> None:
    """Agrega una línea al log. Nunca deja escapar una excepción: un fallo
    al escribir (disco lleno, carpeta sin permisos) no puede tirar abajo
    el flujo real de la persona — la bitácora es de apoyo, jamás la causa
    de un problema nuevo."""
    try:
        log = ruta_log()
        log.parent.mkdir(parents=True, exist_ok=True)
        _rotar_si_hace_falta(log)
        linea = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tipo": tipo,
            **detalle,
        }
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    except Exception:
        pass


@contextmanager
def medir(nombre: str, **detalle):
    """Cronometra un bloque de código Python y lo registra. Si el bloque
    lanza una excepción, igual se registra la duración hasta ese punto,
    junto con el error."""
    inicio = time.monotonic()
    try:
        yield
    except Exception as e:
        registrar(
            f"{nombre}_error",
            duracion_segundos=round(time.monotonic() - inicio, 1),
            mensaje=str(e),
            traceback=traceback.format_exc(),
        )
        raise
    else:
        registrar(f"{nombre}_fin", duracion_segundos=round(time.monotonic() - inicio, 1), **detalle)


def sugerir_catalogo(metrica: str, motivo: str) -> None:
    """Registra que una métrica a medida parece lo bastante reusable como
    para valer la pena incorporarla al catálogo permanente — para que el
    dueño del proyecto la vea después revisando la bitácora.

    A propósito NO es una pregunta interactiva al
    usuario: la consola corre en segundo plano para quien usa el flujo
    guiado, y el proceso puede cerrarse apenas la persona termina. Quedar
    en un archivo que sobrevive al cierre es la única forma confiable de
    que no se pierda.
    """
    registrar("sugerencia_catalogo", metrica=metrica, motivo=motivo)


def medir_comando(nombre: str, comando: list[str]) -> subprocess.CompletedProcess:
    """Corre un comando externo (ej. `jupyter nbconvert`) cronometrando
    cuánto tarda, y lo registra. Para los pasos pesados que el agente
    invoca como subproceso en vez de código Python directo."""
    inicio = time.monotonic()
    try:
        resultado = subprocess.run(comando, check=True)
    except Exception as e:
        registrar(f"{nombre}_error", duracion_segundos=round(time.monotonic() - inicio, 1), mensaje=str(e))
        raise
    registrar(f"{nombre}_fin", duracion_segundos=round(time.monotonic() - inicio, 1))
    return resultado


def leer_eventos() -> list[dict]:
    """Lee todos los eventos registrados. Ignora líneas corruptas en vez de
    fallar la lectura entera — un log puede quedar a medio escribir si el
    proceso se cortó en el momento justo."""
    log = ruta_log()
    if not log.exists():
        return []
    eventos = []
    for linea in log.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            eventos.append(json.loads(linea))
        except json.JSONDecodeError:
            continue
    return eventos
