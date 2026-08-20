"""Cierre de la consola de Claude Code cuando el flujo termina de verdad.

Nació de un problema real observado en corridas del flujo guiado: ni
terminar el informe ni salir del flujo cerraban la ventana de consola que
abre `abrir_agente.bat` — quedaba viva de fondo indefinidamente, una
ventana negra que alguien sin conocimientos técnicos no sabe si puede
cerrar. La causa es de diseño: una sesión interactiva de Claude Code no
termina nunca por sí sola (confirmado contra la documentación oficial de
la CLI), así que este módulo no depende de que termine — cuando el flujo
acaba de verdad, cierra el proceso de Claude Code desde adentro y el
`.bat` recupera el control.

**Solo actúa si `abrir_agente.bat` lo pidió explícitamente** (variables
POLITICAS_SOCIALES_CONSOLA y POLITICAS_SOCIALES_CONSOLA_PID, que solo
ese archivo define, recién después del formulario de arranque). Sin esas
variables no hace absolutamente nada: una sesión de `claude` abierta a
mano y la suite de tests jamás se cierran solas por accidente.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from pathlib import Path

from . import bitacora

VAR_ACTIVA = "POLITICAS_SOCIALES_CONSOLA"
VAR_PID_CONSOLA = "POLITICAS_SOCIALES_CONSOLA_PID"

_PREFIJO_MARCA = "politicas-sociales-cierre-"
_VIDA_UTIL_MARCA_EN_SEGUNDOS = 24 * 60 * 60


def marca_de_cierre(pid_consola: int) -> Path:
    """Archivo que le avisa a `abrir_agente.bat` que el cierre lo pidió
    este proyecto, y no que Claude Code se haya roto.

    Terminar el proceso de Claude Code hace que `claude` salga con código
    de error: sin esta marca, el `.bat` no distingue "el flujo terminó
    bien y pedimos cerrar" de "algo falló de verdad", y mostraría un
    error (con su `pause`) al final de una corrida exitosa. En la
    práctica el `.bat` casi nunca llega a leerla (el cierre suele
    llevarse la consola entera), pero en los entornos donde sí sobrevive
    es lo único que evita ese mensaje.
    """
    return Path(tempfile.gettempdir()) / f"{_PREFIJO_MARCA}{pid_consola}.marker"


def limpiar_marcas_viejas() -> None:
    """Borra marcas de cierre de corridas anteriores que nadie consumió.

    Sin esto se acumula un archivo por corrida en la carpeta temporal,
    para siempre. Nunca deja escapar una excepción: no poder limpiar
    temporales jamás puede impedir que la consola se cierre.
    """
    limite = time.time() - _VIDA_UTIL_MARCA_EN_SEGUNDOS
    try:
        for vieja in Path(tempfile.gettempdir()).glob(f"{_PREFIJO_MARCA}*.marker"):
            try:
                if vieja.stat().st_mtime < limite:
                    vieja.unlink()
            except OSError:
                continue
    except Exception:
        pass


# Sube por la cadena de procesos padre desde este mismo Python hasta el
# hijo directo de la consola que abrió `abrir_agente.bat` — ese es Claude
# Code — y lo termina. Por parentesco y no por nombre de ejecutable: según
# cómo se haya instalado, el proceso puede llamarse "node.exe" (npm) o
# "claude.exe" (instalador nativo). Se termina SOLO ese proceso, no el
# árbol: este Python es descendiente de Claude Code, matar el árbol sería
# matarnos en medio de la operación.
_PLANTILLA_POWERSHELL = """
$objetivo = {pid_consola}
$actual = {pid_python}
while ($actual -ne 0) {{
  $proc = Get-CimInstance Win32_Process -Filter ("ProcessId=" + $actual) -ErrorAction SilentlyContinue
  if (-not $proc) {{ break }}
  if ($proc.ParentProcessId -eq $objetivo) {{
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
    break
  }}
  $actual = $proc.ParentProcessId
}}
"""


def cierre_pedido_por_el_lanzador() -> bool:
    """¿Fue `abrir_agente.bat` quien lanzó esta sesión, y por lo tanto hay
    una consola que cerrar cuando el flujo termine? Falso en cualquier
    otro contexto (tests, `claude` abierto a mano, notebook suelto)."""
    return os.environ.get(VAR_ACTIVA) == "1" and (os.environ.get(VAR_PID_CONSOLA) or "").strip().isdigit()


def cerrar_consola(motivo: str) -> bool:
    """Cierra la sesión de Claude Code que abrió `abrir_agente.bat`, para
    que su ventana se cierre sola. Devuelve True si se intentó el cierre.

    No hace nada (y devuelve False) fuera de ese contexto. Nunca deja
    escapar una excepción: si el cierre falla, el usuario se queda con
    una consola abierta de más (el problema que ya existía), nunca con un
    error en medio de la entrega de su informe.
    """
    if not cierre_pedido_por_el_lanzador():
        return False

    pid_consola = int(os.environ[VAR_PID_CONSOLA].strip())
    script = _PLANTILLA_POWERSHELL.format(pid_consola=pid_consola, pid_python=os.getpid())
    bitacora.registrar("cierre_consola", motivo=motivo, pid_consola=pid_consola)
    limpiar_marcas_viejas()
    try:
        # La marca se deja ANTES de terminar el proceso: después de matar a
        # Claude Code, este Python queda huérfano y no hay garantía de
        # cuánto sigue vivo.
        marca_de_cierre(pid_consola).write_text(motivo, encoding="utf-8")
    except Exception:
        pass
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            check=False,
            capture_output=True,
            timeout=20,
        )
    except Exception as e:  # pragma: no cover - depende del sistema operativo
        bitacora.registrar("cierre_consola_error", motivo=motivo, mensaje=str(e))
        return False
    return True
