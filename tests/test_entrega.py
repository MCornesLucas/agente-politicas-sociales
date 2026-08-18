"""Tests del respaldo de entrega."""

from politicas_sociales.entrega import respaldar_si_existe


def test_respalda_el_archivo_existente(tmp_path):
    original = tmp_path / "Informe_Infancia.pdf"
    original.write_text("version vieja", encoding="utf-8")
    respaldo = respaldar_si_existe(original)
    assert respaldo == tmp_path / "Informe_Infancia (anterior).pdf"
    assert respaldo.read_text(encoding="utf-8") == "version vieja"
    assert not original.exists()


def test_sin_archivo_no_hace_nada(tmp_path):
    assert respaldar_si_existe(tmp_path / "no_existe.pdf") is None


def test_guarda_una_sola_version_anterior(tmp_path):
    original = tmp_path / "informe.pdf"
    (tmp_path / "informe (anterior).pdf").write_text("antigua", encoding="utf-8")
    original.write_text("reciente", encoding="utf-8")
    respaldar_si_existe(original)
    assert (tmp_path / "informe (anterior).pdf").read_text(encoding="utf-8") == "reciente"
