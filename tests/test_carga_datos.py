"""Tests del paso de datos del flujo guiado (estado, ECH manual, fuentes
del usuario) y de los estados del formulario de datos.

Reglas del dueño fijadas aquí (2026-08-20): el formulario se muestra
siempre; cada botón se deshabilita con su marca de listo cuando su carga
ya está, salvo "Otras fuentes"; con los datos cargados y la revisión
vencida, el botón de carga automática pasa a ofrecer la vigilancia de
terceros; los años ECH ofrecidos son 2019 y 2023 en adelante (la ECH
telefónica 2020-2022 nunca se verificó en este pipeline).
"""

import datetime
import json

from politicas_sociales import carga_datos, plantillas, vigilancia


# --- Años ECH -----------------------------------------------------------------


def test_anios_esperados_excluyen_la_pandemia_e_incluyen_el_corriente():
    hoy = datetime.date(2026, 8, 20)
    assert carga_datos.anios_ech_esperados(hoy) == [2019, 2023, 2024, 2025, 2026]


def test_preparar_carpetas_crea_los_anios_vacios(tmp_path, monkeypatch):
    monkeypatch.setattr(carga_datos.ech_config, "DATA_DIR", tmp_path / "ech_microdatos")
    carpeta = carga_datos.preparar_carpetas_ech(datetime.date(2026, 1, 1))
    assert carpeta == str(tmp_path / "ech_microdatos")
    assert sorted(p.name for p in (tmp_path / "ech_microdatos").iterdir()) == [
        "2019", "2023", "2024", "2025", "2026"]
    # Idempotente: si un año ya tiene datos, no los toca.
    (tmp_path / "ech_microdatos" / "2023" / "ECH_2023.csv").write_text("x")
    carga_datos.preparar_carpetas_ech(datetime.date(2026, 1, 1))
    assert (tmp_path / "ech_microdatos" / "2023" / "ECH_2023.csv").read_text() == "x"


def test_anios_cargados_detecta_solo_anios_con_hogares(tmp_path, monkeypatch):
    monkeypatch.setattr(carga_datos.ech_config, "DATA_DIR", tmp_path)
    (tmp_path / "2019").mkdir()
    (tmp_path / "2019" / "H_2019_Terceros.sav").write_text("")
    (tmp_path / "2024").mkdir()   # carpeta vacía: no cuenta como cargado
    (tmp_path / "2025").mkdir()
    (tmp_path / "2025" / "ECH_2025_implantacion.csv").write_text("")
    assert carga_datos.anios_ech_cargados() == [2019, 2025]


# --- Estado del formulario ----------------------------------------------------


def _con_vigilancia(monkeypatch, tmp_path, hace_dias, hoy):
    marcador = tmp_path / "ultima.json"
    if hace_dias is not None:
        fecha = (hoy - datetime.timedelta(days=hace_dias)).isoformat()
        marcador.write_text(json.dumps({"fecha": fecha, "resumen": {}}), encoding="utf-8")
    monkeypatch.setattr(vigilancia, "ULTIMA_REVISION", marcador)


def test_vigilancia_pendiente_por_plazo_o_por_no_haber_corrido(tmp_path, monkeypatch):
    hoy = datetime.date(2026, 8, 20)
    _con_vigilancia(monkeypatch, tmp_path, None, hoy)
    assert carga_datos.vigilancia_pendiente(hoy)          # nunca corrió
    _con_vigilancia(monkeypatch, tmp_path, 2, hoy)
    assert not carga_datos.vigilancia_pendiente(hoy)      # reciente
    _con_vigilancia(monkeypatch, tmp_path, carga_datos.DIAS_ENTRE_REVISIONES, hoy)
    assert carga_datos.vigilancia_pendiente(hoy)          # plazo cumplido


def test_estado_datos_en_maquina_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr(carga_datos.config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(carga_datos.ech_config, "DATA_DIR", tmp_path / "ech_microdatos")
    _con_vigilancia(monkeypatch, tmp_path, None, datetime.date(2026, 8, 20))
    estado = carga_datos.estado_datos(datetime.date(2026, 8, 20))
    assert estado["automaticas_listo"] is False
    assert estado["ech_cargados"] == []
    assert estado["ech_completo"] is False
    assert estado["vigilancia_pendiente"] is True


# --- Estados del formulario de datos ------------------------------------------


def _estado(**cambios):
    base = {"automaticas_listo": False, "vigilancia_pendiente": False,
            "ech_esperados": [2019, 2023], "ech_cargados": [], "ech_completo": False}
    return {**base, **cambios}


def test_boton_automatica_descarga_cuando_no_hay_datos():
    html = plantillas.plantilla_datos(_estado())
    assert "accion('automatica')" in html
    assert "accion('vigilancia')" not in html


def test_boton_automatica_ofrece_vigilancia_con_datos_y_plazo_vencido():
    html = plantillas.plantilla_datos(_estado(automaticas_listo=True, vigilancia_pendiente=True))
    assert "accion('vigilancia')" in html
    assert "accion('automatica')" not in html
    assert "Revisar novedades" in html


def test_boton_automatica_deshabilitado_con_datos_y_revision_al_dia():
    html = plantillas.plantilla_datos(_estado(automaticas_listo=True, vigilancia_pendiente=False))
    assert "accion('automatica')" not in html
    assert "accion('vigilancia')" not in html
    assert html.count("disabled>") == 1
    assert "✓ Listo" in html


def test_boton_ech_muestra_los_anios_y_se_deshabilita_completo():
    parcial = plantillas.plantilla_datos(_estado(ech_cargados=[2019]))
    assert "accion('ech')" in parcial
    assert "Años cargados: 2019." in parcial
    completo = plantillas.plantilla_datos(
        _estado(ech_cargados=[2019, 2023], ech_completo=True))
    assert "accion('ech')" not in completo
    assert "✓ Listo" in completo


def test_boton_otras_fuentes_siempre_habilitado_y_continuar_presente():
    html = plantillas.plantilla_datos(
        _estado(automaticas_listo=True, ech_completo=True, ech_cargados=[2019, 2023]))
    assert "accion('otras')" in html
    assert "continuar" in html
    assert "salir_del_flujo" in html


def test_el_aviso_se_muestra_solo_si_existe():
    assert "un resultado" in plantillas.plantilla_datos(_estado(), aviso="un resultado")
    assert 'class="advertencia"' not in plantillas.plantilla_datos(_estado())


# --- Fuentes del usuario ------------------------------------------------------


def _fuentes_en(tmp_path, monkeypatch):
    monkeypatch.setattr(carga_datos, "CARPETA_USUARIO", tmp_path / "usuario")
    monkeypatch.setattr(carga_datos, "REGISTRO_FUENTES_USUARIO",
                        tmp_path / "usuario" / "fuentes.json")


def test_carpeta_fuente_usuario_crea_con_slug_seguro(tmp_path, monkeypatch):
    _fuentes_en(tmp_path, monkeypatch)
    carpeta = carga_datos.carpeta_fuente_usuario("Registros del programa Ñandú (2020-2024)")
    assert carpeta == str(tmp_path / "usuario" / "registros_del_programa_nandu_2020_2024")
    assert (tmp_path / "usuario" / "registros_del_programa_nandu_2020_2024").is_dir()


def test_registrar_fuente_vacia_no_registra_nada(tmp_path, monkeypatch):
    _fuentes_en(tmp_path, monkeypatch)
    carga_datos.carpeta_fuente_usuario("Mi fuente")
    assert carga_datos.registrar_fuente_usuario("Mi fuente", "https://ejemplo.uy") == []
    assert carga_datos.fuentes_usuario() == []


def test_registrar_fuente_con_archivos_guarda_nombre_y_origen(tmp_path, monkeypatch):
    _fuentes_en(tmp_path, monkeypatch)
    carpeta = carga_datos.carpeta_fuente_usuario("Mi fuente")
    (tmp_path / "usuario" / "mi_fuente" / "datos.csv").write_text("a,b\n1,2\n")
    archivos = carga_datos.registrar_fuente_usuario("Mi fuente", "https://ejemplo.uy/datos")
    assert archivos == ["datos.csv"]
    (registro,) = carga_datos.fuentes_usuario()
    assert registro["nombre"] == "Mi fuente"
    assert registro["origen"] == "https://ejemplo.uy/datos"
    assert registro["carpeta"] == "mi_fuente"
    assert registro["archivos"] == ["datos.csv"]
    assert carpeta.endswith("mi_fuente")


def test_registrar_dos_veces_reemplaza_sin_duplicar(tmp_path, monkeypatch):
    _fuentes_en(tmp_path, monkeypatch)
    carga_datos.carpeta_fuente_usuario("Mi fuente")
    (tmp_path / "usuario" / "mi_fuente" / "datos.csv").write_text("x")
    carga_datos.registrar_fuente_usuario("Mi fuente", "origen viejo")
    (tmp_path / "usuario" / "mi_fuente" / "extra.csv").write_text("y")
    carga_datos.registrar_fuente_usuario("Mi fuente", "origen nuevo")
    (registro,) = carga_datos.fuentes_usuario()
    assert registro["origen"] == "origen nuevo"
    assert registro["archivos"] == ["datos.csv", "extra.csv"]
