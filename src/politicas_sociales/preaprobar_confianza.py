"""Deja esta carpeta pre-aprobada en Claude Code, para que la primera
corrida de abrir_agente.bat no muestre el dialogo de confianza en la
consola (hallazgo de la primera corrida real, 2026-08-19: el usuario
final no debe ver decisiones en la terminal). El consentimiento es
correr instalar.bat, que invoca este modulo — mismo criterio que
cualquier instalador. La aprobacion vive en ~/.claude.json,
projects.<ruta>.hasTrustDialogAccepted (verificado contra el archivo
real). Cualquier fallo se informa y NO detiene la instalacion."""

from __future__ import annotations

import json
from pathlib import Path

from . import config


def preaprobar(ruta_config: Path | None = None, proyecto: Path | None = None) -> bool:
    ruta_config = ruta_config or Path.home() / ".claude.json"
    proyecto = proyecto or config.PROJECT_ROOT
    clave = proyecto.resolve().as_posix()
    try:
        datos = json.loads(ruta_config.read_text(encoding="utf-8")) if ruta_config.exists() else {}
        if not isinstance(datos, dict):
            raise ValueError("~/.claude.json no contiene un objeto JSON")
        entrada = datos.setdefault("projects", {}).setdefault(clave, {})
        if entrada.get("hasTrustDialogAccepted") is True:
            print(f"La carpeta ya estaba aprobada en Claude Code: {clave}")
            return True
        entrada["hasTrustDialogAccepted"] = True
        temporal = ruta_config.with_suffix(".json.politicas-tmp")
        temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        temporal.replace(ruta_config)
        print(f"Carpeta aprobada en Claude Code: {clave}")
        return True
    except Exception as e:
        print(f"No se pudo pre-aprobar la carpeta en Claude Code ({e}). "
              "No es grave: la primera corrida mostrara el chequeo una unica vez.")
        return False


if __name__ == "__main__":
    preaprobar()
