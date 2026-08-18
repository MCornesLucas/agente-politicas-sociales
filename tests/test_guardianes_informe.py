"""Tests de los guardianes del informe (.claude/hooks/*.cjs).

Regla del proyecto: todo guardián se prueba contra la salida real — un
hook que nunca se disparó contra un notebook de verdad puede quedar
verde por no mirar nada (fallo documentado dos veces en el proyecto
hermano). Por eso cada guardián se prueba en las dos direcciones: deja
pasar el informe real del repositorio, y bloquea una copia saboteada.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
HOOKS = RAIZ / ".claude" / "hooks"
INFORME_REAL = RAIZ / "notebooks" / "informe_infancia.ipynb"

node = shutil.which("node")
requiere_node = pytest.mark.skipif(node is None, reason="requiere Node.js")


def correr_hook(nombre, comando):
    entrada = json.dumps({"tool_name": "Bash", "tool_input": {"command": comando}})
    # encoding explícito: node emite UTF-8 y en Windows text=True decodifica
    # con cp1252, convirtiendo "Métrica" en mojibake.
    resultado = subprocess.run([node, str(HOOKS / nombre)], input=entrada,
                               capture_output=True, encoding="utf-8", timeout=120)
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout.strip()


def comando_ejecutar(ruta):
    return f'jupyter nbconvert --to notebook --execute --inplace "{ruta}"'


def celda_md(texto):
    return {"cell_type": "markdown", "metadata": {}, "source": texto}


def celda_code(codigo, outputs=None):
    return {"cell_type": "code", "metadata": {}, "execution_count": 1,
            "source": codigo, "outputs": outputs or []}


def escribir_nb(ruta, celdas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps({"cells": celdas, "metadata": {},
                                "nbformat": 4, "nbformat_minor": 5}),
                    encoding="utf-8")
    return ruta


def _grupo_metrica(n, con_lectura=True):
    md = (f"### Métrica {n}. Ejemplo\n\n**¿Qué pregunta responde?** Algo.\n\n"
          "**Por qué esta gráfica.** Porque sí.\n")
    if con_lectura:
        md += "\n**Lectura**: se lee.\n"
    return [celda_md(md), celda_code('plt.plot(x)\nfuente(fig, "Fuente: X")\nplt.show()')]


# ---------------------------------------------------------------- métrica

@requiere_node
def test_metrica_incompleta_deja_pasar_el_informe_real():
    assert correr_hook("gate-informe-metrica-incompleta.cjs",
                       comando_ejecutar(INFORME_REAL)) == ""


@requiere_node
def test_metrica_incompleta_bloquea_una_metrica_sin_lectura(tmp_path):
    nb = escribir_nb(tmp_path / "nb.ipynb",
                     _grupo_metrica(1) + _grupo_metrica(2, con_lectura=False))
    salida = correr_hook("gate-informe-metrica-incompleta.cjs", comando_ejecutar(nb))
    decision = json.loads(salida)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "Métrica 2" in decision["permissionDecisionReason"]
    assert "sin lectura" in decision["permissionDecisionReason"]


@requiere_node
def test_metrica_incompleta_bloquea_si_no_reconoce_ningun_encabezado(tmp_path):
    # El fallo silencioso del proyecto hermano: si el patrón de encabezados
    # cambia, el hook no debe quedar verde por no encontrar nada que mirar.
    nb = escribir_nb(tmp_path / "nb.ipynb", [celda_md("# Otro documento")])
    salida = correr_hook("gate-informe-metrica-incompleta.cjs", comando_ejecutar(nb))
    decision = json.loads(salida)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "ciego" in decision["permissionDecisionReason"]


@requiere_node
def test_metrica_incompleta_ignora_comandos_sin_nbconvert():
    assert correr_hook("gate-informe-metrica-incompleta.cjs", "git status") == ""


# ----------------------------------------------------------------- cifras

@requiere_node
def test_cifras_deja_pasar_el_informe_real():
    assert correr_hook("gate-informe-cifras-sin-respaldo.cjs",
                       comando_ejecutar(INFORME_REAL)) == ""


def _nb_con_resumen(tmp_path, texto_resumen, csv="valor\n27.48\n8017\n"):
    (tmp_path / "datos_curados").mkdir()
    (tmp_path / "datos_curados" / "datos.csv").write_text(csv, encoding="utf-8")
    return escribir_nb(tmp_path / "notebooks" / "nb.ipynb", [
        celda_code("print(1)", outputs=[{"output_type": "stream", "name": "stdout",
                                         "text": "sin numeros utiles aqui\n"}]),
        celda_md("## Resumen analítico"),
        celda_md(texto_resumen),
    ])


@requiere_node
def test_cifras_acepta_redondeo_honesto_y_magnitud(tmp_path):
    # 27,5% es 27.48 del CSV redondeado; ~8.000 es 8017 a magnitud de miles.
    nb = _nb_con_resumen(tmp_path, "La pobreza es 27,5% y el SPE ~8.000 atendidos.")
    assert correr_hook("gate-informe-cifras-sin-respaldo.cjs", comando_ejecutar(nb)) == ""


@requiere_node
def test_cifras_bloquea_una_cifra_inventada(tmp_path):
    nb = _nb_con_resumen(tmp_path, "La pobreza es 99,9% de los hogares.")
    salida = correr_hook("gate-informe-cifras-sin-respaldo.cjs", comando_ejecutar(nb))
    decision = json.loads(salida)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "99,9" in decision["permissionDecisionReason"]


@requiere_node
def test_cifras_tambien_vigila_las_conclusiones_sin_resumen(tmp_path):
    # Desde 2026-08-19 las conclusiones van en TODAS las ediciones; en
    # una parcial no hay resumen analítico, así que el guardián tiene que
    # arrancar en "## Conclusiones" — si no, las cifras escritas a mano
    # de una edición parcial quedaban sin vigilar.
    (tmp_path / "datos_curados").mkdir()
    (tmp_path / "datos_curados" / "datos.csv").write_text("valor\n27.48\n",
                                                          encoding="utf-8")
    nb = escribir_nb(tmp_path / "notebooks" / "nb.ipynb", [
        celda_code("print(1)", outputs=[{"output_type": "stream", "name": "stdout",
                                         "text": "1\n"}]),
        celda_md("## Conclusiones"),
        celda_md("1. **Algo.** El 88,8% de los hogares."),
    ])
    salida = correr_hook("gate-informe-cifras-sin-respaldo.cjs", comando_ejecutar(nb))
    decision = json.loads(salida)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "deny"
    assert "88,8" in decision["permissionDecisionReason"]


def test_cifras_ignora_anios_y_texto_antes_del_resumen(tmp_path):
    # "2024" es un año y "el 15,0%" está ANTES del encabezado del resumen:
    # ninguno debe bloquear.
    (tmp_path / "datos_curados").mkdir()
    (tmp_path / "datos_curados" / "datos.csv").write_text("valor\n1\n", encoding="utf-8")
    nb = escribir_nb(tmp_path / "notebooks" / "nb.ipynb", [
        celda_code("print(1)", outputs=[{"output_type": "stream", "name": "stdout",
                                         "text": "1\n"}]),
        celda_md("En 2024 el 15,0% de algo."),
        celda_md("## Resumen analítico"),
        celda_md("La serie llega a 2024."),
    ])
    assert correr_hook("gate-informe-cifras-sin-respaldo.cjs", comando_ejecutar(nb)) == ""


# --------------------------------------------------------------- gráficas

@requiere_node
def test_graficas_deja_pasar_el_informe_real_ejecutado():
    assert correr_hook("gate-informe-graficas-faltantes.cjs",
                       comando_ejecutar(INFORME_REAL)) == ""


@requiere_node
def test_graficas_bloquea_un_plt_show_sin_imagen(tmp_path):
    nb = escribir_nb(tmp_path / "nb.ipynb", [
        celda_code("plt.plot(x)\nplt.show()", outputs=[]),
    ])
    salida = correr_hook("gate-informe-graficas-faltantes.cjs", comando_ejecutar(nb))
    respuesta = json.loads(salida)
    assert respuesta["decision"] == "block"
    assert "plt.show()" in respuesta["reason"]


@requiere_node
def test_graficas_acepta_un_plt_show_con_imagen(tmp_path):
    nb = escribir_nb(tmp_path / "nb.ipynb", [
        celda_code("plt.plot(x)\nplt.show()", outputs=[
            {"output_type": "display_data", "metadata": {},
             "data": {"image/png": "iVBORw0KG=="}},
        ]),
    ])
    assert correr_hook("gate-informe-graficas-faltantes.cjs", comando_ejecutar(nb)) == ""


# --------------------------------------------------------------- bitácora

@requiere_node
def test_un_bloqueo_queda_registrado_en_la_bitacora(tmp_path, monkeypatch):
    bitacora = tmp_path / "bitacora.jsonl"
    monkeypatch.setenv("POLITICAS_SOCIALES_BITACORA", str(bitacora))
    nb = escribir_nb(tmp_path / "nb.ipynb", [celda_md("# Otro documento")])
    entrada = json.dumps({"tool_name": "Bash",
                          "tool_input": {"command": comando_ejecutar(nb)}})
    subprocess.run([node, str(HOOKS / "gate-informe-metrica-incompleta.cjs")],
                   input=entrada, capture_output=True, encoding="utf-8", timeout=120)
    contenido = bitacora.read_text(encoding="utf-8")
    evento = json.loads(contenido.splitlines()[0])
    assert evento["tipo"] == "hook_bloqueo"
    assert evento["hook"] == "informe-metrica-incompleta"
