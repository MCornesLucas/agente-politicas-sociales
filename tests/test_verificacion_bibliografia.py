"""Tests de la verificación de bibliografía (regla central del dueño:
toda fuente citada en el informe, con su entrada y su enlace en la
bibliografía del proyecto)."""

from politicas_sociales import verificacion_bibliografia as vb


def test_ningun_enlace_del_informe_queda_sin_respaldo():
    # Contra las celdas REALES del informe: si alguien cita una fuente
    # nueva sin agregarla a docs/BIBLIOGRAFIA.md (o FUENTES_DE_DATOS.md),
    # este test la nombra.
    assert vb.enlaces_sin_respaldo() == {}


def test_el_informe_cita_enlaces_y_la_bibliografia_los_respalda():
    # El chequeo anterior no puede quedar verde por no mirar nada
    # (lección de los guardianes): tiene que haber enlaces reales en
    # ambos lados.
    assert len(vb.enlaces_del_informe()) >= 5
    assert len(vb.enlaces_con_respaldo()) >= 10


def test_extraccion_de_enlaces_limpia_puntuacion_final():
    enlaces = vb._enlaces_de("ver https://ejemplo.uy/pagina, y también "
                             "(https://otro.uy/doc).")
    assert enlaces == {"https://ejemplo.uy/pagina", "https://otro.uy/doc"}


def test_los_repositorios_propios_estan_exentos():
    # La firma del informe enlaza los repos del proyecto: no son fuentes
    # de datos y no corresponde pedirles entrada bibliográfica.
    faltantes = vb.enlaces_sin_respaldo()
    assert not any("github.com/testa10" in enlace for enlace in faltantes)
