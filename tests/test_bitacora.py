"""Tests de la bitácora local de sesiones."""

import json

from politicas_sociales import bitacora


def test_registrar_escribe_una_linea_jsonl(tmp_path, monkeypatch):
    log = tmp_path / "b.jsonl"
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(log))
    bitacora.registrar("prueba", detalle="algo")
    evento = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
    assert evento["tipo"] == "prueba"
    assert evento["detalle"] == "algo"
    assert "timestamp" in evento


def test_registrar_jamas_deja_escapar_una_excepcion(tmp_path, monkeypatch):
    # Una ruta imposible (un archivo donde debería haber una carpeta) no
    # puede tirar abajo el flujo real: la bitácora es de apoyo.
    imposible = tmp_path / "archivo.txt"
    imposible.write_text("x", encoding="utf-8")
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(imposible / "b.jsonl"))
    bitacora.registrar("prueba")  # no debe lanzar


def test_medir_registra_duracion_y_errores(tmp_path, monkeypatch):
    log = tmp_path / "b.jsonl"
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(log))
    with bitacora.medir("paso"):
        pass
    try:
        with bitacora.medir("paso_roto"):
            raise ValueError("falló")
    except ValueError:
        pass
    tipos = [e["tipo"] for e in bitacora.leer_eventos()]
    assert "paso_fin" in tipos
    assert "paso_roto_error" in tipos
    error = next(e for e in bitacora.leer_eventos() if e["tipo"] == "paso_roto_error")
    assert error["mensaje"] == "falló"
    assert "duracion_segundos" in error


def test_leer_eventos_ignora_lineas_corruptas(tmp_path, monkeypatch):
    log = tmp_path / "b.jsonl"
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(log))
    log.write_text('{"tipo": "ok", "timestamp": "t"}\n{corrupta\n', encoding="utf-8")
    eventos = bitacora.leer_eventos()
    assert len(eventos) == 1
    assert eventos[0]["tipo"] == "ok"


def test_rotacion_al_superar_el_tamanio(tmp_path, monkeypatch):
    log = tmp_path / "b.jsonl"
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(log))
    monkeypatch.setattr(bitacora, "_TAMANIO_MAXIMO_EN_BYTES", 50)
    bitacora.registrar("primera", relleno="x" * 100)
    bitacora.registrar("segunda")
    # La primera tanda quedó en ".1" y el log nuevo solo tiene la segunda.
    assert log.with_suffix(".jsonl.1").exists()
    assert [e["tipo"] for e in bitacora.leer_eventos()] == ["segunda"]
