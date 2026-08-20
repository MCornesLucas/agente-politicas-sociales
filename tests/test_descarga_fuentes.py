"""Tests de la carga automática de fuentes.

El manifiesto es la transcripción ejecutable de
docs/RELEVAMIENTO_DE_DATOS.md: acá se fija su forma (destinos únicos y
relativos, URLs completas, la ECH afuera) y se prueba la descarga en las
dos direcciones — el archivo bueno queda, la página de error disfrazada
de archivo NO pasa — sin tocar la red.
"""

from politicas_sociales import descarga_fuentes as df


# --- Manifiesto ---------------------------------------------------------------


def test_manifiesto_bien_formado():
    destinos = [e["destino"] for e in df.MANIFIESTO]
    assert len(destinos) == len(set(destinos)), "destinos repetidos"
    for e in df.MANIFIESTO:
        assert not e["destino"].startswith(("/", "\\")) and ".." not in e["destino"]
        assert e["url"].startswith(("https://", "http://"))
        assert e["tipo"] in ("pdf", "xlsx", "html")


def test_manifiesto_cubre_las_seis_entidades_documentales():
    entidades = {e["destino"].split("/")[0] for e in df.MANIFIESTO}
    assert entidades == {"sipiav", "inau", "ensanna", "ceti", "conapees", "ine"}
    # Serie SIPIAV completa y los 19 departamentos de INAU.
    assert sum(1 for e in df.MANIFIESTO if e["destino"].startswith("sipiav/")) == 13
    assert sum(1 for e in df.MANIFIESTO if "departamentos/" in e["destino"]) == 19


def test_los_microdatos_ech_quedan_fuera_del_manifiesto():
    # La carga de la ECH es siempre manual: el INE exige aceptar sus
    # términos personalmente (regla innegociable del flujo).
    assert not any("ech" in e["destino"].split("/")[0] for e in df.MANIFIESTO)


# --- Verificación de formato --------------------------------------------------


def test_es_valido_acepta_el_formato_real_y_rechaza_el_error_disfrazado():
    assert df.es_valido(b"%PDF-1.7" + b"x" * 20_000, "pdf")
    assert df.es_valido(b"PK\x03\x04" + b"x" * 20_000, "xlsx")
    assert df.es_valido(b"<!DOCTYPE html><html>" + b"x" * 30_000, "html")
    # Una página de error del servidor guardada como PDF no pasa.
    assert not df.es_valido(b"<html>404 Not Found</html>" + b"x" * 20_000, "pdf")
    # Un archivo sospechosamente chico tampoco.
    assert not df.es_valido(b"%PDF-1.7 x", "pdf")


def test_archivo_valido_contra_disco(tmp_path):
    bueno = tmp_path / "a.pdf"
    bueno.write_bytes(b"%PDF-1.7" + b"x" * 20_000)
    assert df.archivo_valido(bueno, "pdf")
    malo = tmp_path / "b.pdf"
    malo.write_bytes(b"<html>error</html>" + b"x" * 20_000)
    assert not df.archivo_valido(malo, "pdf")
    assert not df.archivo_valido(tmp_path / "no_existe.pdf", "pdf")


# --- Descarga del manifiesto (sin red) ---------------------------------------


def test_descarga_salta_lo_presente_y_baja_lo_que_falta(tmp_path, monkeypatch):
    primera = df.MANIFIESTO[0]
    ya = tmp_path / primera["destino"]
    ya.parent.mkdir(parents=True)
    ya.write_bytes(b"%PDF-1.4" + b"x" * 20_000)

    pedidas = []

    def falso(url):
        pedidas.append(url)
        return b"%PDF-1.7" + b"y" * 20_000

    monkeypatch.setattr(df, "descargar_bytes", falso)
    resultados = df.descargar_manifiesto(tmp_path)
    por_resultado = {r["destino"]: r["resultado"] for r in resultados}
    assert por_resultado[primera["destino"]] == "ya_estaba"
    assert primera["url"] not in pedidas                      # no se re-baja
    assert ya.read_bytes().startswith(b"%PDF-1.4")            # ni se pisa
    # Los xlsx del manifiesto fallan la firma PDF del descargador falso:
    # quedan como error, no como archivo guardado (verde solo si el
    # formato es el esperado).
    xlsx = next(e for e in df.MANIFIESTO if e["tipo"] == "xlsx")
    assert por_resultado[xlsx["destino"]] == "error"
    assert not (tmp_path / xlsx["destino"]).exists()
    pdf_nuevo = next(e for e in df.MANIFIESTO[1:] if e["tipo"] == "pdf")
    assert por_resultado[pdf_nuevo["destino"]] == "descargado"
    assert (tmp_path / pdf_nuevo["destino"]).read_bytes().startswith(b"%PDF-1.7")


def test_descarga_caida_reporta_error_sin_romper(tmp_path, monkeypatch):
    def caida(url):
        raise OSError("sin conexión")
    monkeypatch.setattr(df, "descargar_bytes", caida)
    resultados = df.descargar_manifiesto(tmp_path)
    assert all(r["resultado"] == "error" for r in resultados)
    assert not list(tmp_path.rglob("*"))


# --- Biblioteca UNICEF --------------------------------------------------------


def test_ids_locales_reconoce_el_sufijo_de_la_curaduria(tmp_path):
    (tmp_path / "unicef" / "2003").mkdir(parents=True)
    (tmp_path / "unicef" / "2003" / "el_trabajo_infantil_49.pdf").write_text("")
    (tmp_path / "unicef" / "biblioteca").mkdir()
    (tmp_path / "unicef" / "biblioteca" / "explnum_120.pdf").write_text("")
    (tmp_path / "unicef" / "2003" / "sin_id.pdf").write_text("")
    assert df.ids_unicef_locales(tmp_path) == {49, 120}
    assert df.ids_unicef_locales(tmp_path / "vacio") == set()


def test_descargar_unicef_baja_solo_los_faltantes(tmp_path, monkeypatch):
    (tmp_path / "unicef" / "x").mkdir(parents=True)
    (tmp_path / "unicef" / "x" / "algo_49.pdf").write_text("")
    monkeypatch.setattr(df, "ids_unicef_en_catalogo", lambda: {49, 50, 51})
    monkeypatch.setattr(df, "descargar_bytes",
                        lambda url: b"%PDF-1.7" + b"z" * 20_000)
    resultados = df.descargar_unicef(tmp_path)
    assert {r["id"]: r["resultado"] for r in resultados} == {
        50: "descargado", 51: "descargado"}
    assert (tmp_path / "unicef" / "biblioteca" / "explnum_50.pdf").exists()


def test_descargar_unicef_respeta_el_limite(tmp_path, monkeypatch):
    monkeypatch.setattr(df, "ids_unicef_en_catalogo", lambda: {1, 2, 3})
    monkeypatch.setattr(df, "descargar_bytes",
                        lambda url: b"%PDF-1.7" + b"z" * 20_000)
    resultados = df.descargar_unicef(tmp_path, limite=1)
    conteo = [r["resultado"] for r in resultados]
    assert conteo.count("descargado") == 1
    assert conteo.count("omitido_por_limite") == 2


def test_descargar_unicef_no_guarda_lo_que_no_es_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(df, "ids_unicef_en_catalogo", lambda: {7})
    monkeypatch.setattr(df, "descargar_bytes",
                        lambda url: b"<html>sesion expirada</html>" + b"x" * 20_000)
    (resultado,) = df.descargar_unicef(tmp_path)
    assert resultado["resultado"] == "error"
    assert not (tmp_path / "unicef" / "biblioteca" / "explnum_7.pdf").exists()
