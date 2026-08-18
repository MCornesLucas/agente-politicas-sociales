"""Tests del cierre de consola: lo crítico es que NUNCA actúe fuera del
contexto de abrir_agente.bat — una sesión de mantenimiento o la propia
suite jamás pueden cerrarse solas."""

import time

from politicas_sociales import cierre


def test_no_actua_sin_las_variables_del_lanzador(monkeypatch):
    monkeypatch.delenv(cierre.VAR_ACTIVA, raising=False)
    monkeypatch.delenv(cierre.VAR_PID_CONSOLA, raising=False)
    assert cierre.cierre_pedido_por_el_lanzador() is False
    assert cierre.cerrar_consola(motivo="prueba") is False


def test_no_actua_con_un_pid_que_no_es_numero(monkeypatch):
    monkeypatch.setenv(cierre.VAR_ACTIVA, "1")
    monkeypatch.setenv(cierre.VAR_PID_CONSOLA, "no-es-un-pid")
    assert cierre.cierre_pedido_por_el_lanzador() is False


def test_detecta_el_contexto_del_lanzador(monkeypatch):
    monkeypatch.setenv(cierre.VAR_ACTIVA, "1")
    monkeypatch.setenv(cierre.VAR_PID_CONSOLA, "1234")
    assert cierre.cierre_pedido_por_el_lanzador() is True


def test_marca_de_cierre_usa_el_prefijo_del_proyecto():
    marca = cierre.marca_de_cierre(1234)
    assert marca.name == "politicas-sociales-cierre-1234.marker"


def test_limpiar_marcas_viejas_borra_solo_las_vencidas(tmp_path, monkeypatch):
    monkeypatch.setattr(cierre.tempfile, "gettempdir", lambda: str(tmp_path))
    vieja = tmp_path / "politicas-sociales-cierre-1.marker"
    vieja.write_text("x", encoding="utf-8")
    hace_dos_dias = time.time() - 2 * 24 * 3600
    import os
    os.utime(vieja, (hace_dos_dias, hace_dos_dias))
    nueva = tmp_path / "politicas-sociales-cierre-2.marker"
    nueva.write_text("x", encoding="utf-8")
    cierre.limpiar_marcas_viejas()
    assert not vieja.exists()
    assert nueva.exists()
