"""Métricas de la ECH para el universo 0-17 (temas 3 y 5 del catálogo).

Calcula, para cada año disponible en `data/ech/`, las métricas 19 y
31-36 de `docs/CATALOGO_DE_METRICAS.md` y exporta tablas ordenadas a
`resultados/ech/` (versionadas: son agregados ponderados, no microdatos).

Definiciones reutilizadas del proyecto agente-encuesta-hogares, sin
modificar (misma métrica, misma definición):

- Hacinamiento: más de 2 personas por cuarto (umbral clásico INE/CEPAL;
  `preprocessing.compute_hacinamiento` del proyecto original).
- Victimización: víctima de un delito si la variable del tipo vale 1;
  prevalencia a nivel de persona ponderada por `W_SEM`
  (`preprocessing.prepare_victimizacion` del original).
- FIES: inseguridad alimentaria si la probabilidad del modelo Rasch
  supera 0,5 (umbral estándar FAO; `config.UMBRAL_FIES` del original).
- Empleo: panel rotativo mensual — cada métrica se calcula mes a mes
  ponderada por `W` y luego se promedian los 12 meses, nunca juntando
  los meses en un solo pool (regla del original).

Toda estimación se acompaña de su n muestral sin ponderar, para aplicar
la regla de celdas chicas (n < 30) al momento de graficar.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROYECTO = Path(__file__).resolve().parent.parent
DATOS = PROYECTO / "data" / "ech"
SALIDA = PROYECTO / "resultados" / "ech"

sys.path.insert(0, str(Path(r"C:\Users\estes\Documents\agente-encuesta-hogares") / "src"))
from encuesta_hogares import preprocessing  # noqa: E402  (normalizar_departamento)

UMBRAL_HACINAMIENTO = 2.0   # personas por cuarto (INE/CEPAL, heredado)
UMBRAL_FIES = 0.5           # probabilidad Rasch (FAO, heredado)

CONDICIONES_VIVIENDA = [
    "humedad_techos", "goteras", "muros_agrietados",
    "puertas_ventanas_deterioradas", "grietas_pisos", "caida_revoque",
    "cielorraso_desprendido", "poca_luz_solar", "escasa_ventilacion",
    "se_inunda", "peligro_derrumbe", "humedad_cimientos",
]

TIPOS_DELITO = {
    "v3": "Robo total de vehículo",
    "v4": "Robo de objetos del vehículo",
    "v5": "Robo en la vivienda",
    "v6": "Estafa",
    "v7": "Robo o asalto fuera de la vivienda",
}


def pct_ponderado(df: pd.DataFrame, flag: pd.Series, peso: str) -> tuple[float, int]:
    """Porcentaje ponderado de `flag` y n muestral sin ponderar."""
    validos = df.loc[flag.notna()]
    flag = flag.loc[validos.index]
    if not len(validos):
        return np.nan, 0
    pct = (flag * validos[peso]).sum() / validos[peso].sum() * 100
    return round(float(pct), 2), int(len(validos))


def anios_disponibles() -> list[int]:
    return sorted(int(p.name) for p in DATOS.iterdir() if p.is_dir())


def filas(metrica, anio, categoria, valor, unidad, n, fuente):
    return {
        "metrica": metrica, "anio": anio, "categoria": categoria,
        "valor": valor, "unidad": unidad, "n_muestral": n, "fuente": fuente,
    }


# Metodología de pobreza por año, verificada contra las columnas reales de
# cada archivo del INE (2019 y 2023 solo traen pobre06/indig06 — canasta
# 2006; 2024 trae ambas y el proyecto original prefiere la nueva; 2025 solo
# la nueva). Consecuencia: la serie tiene DOS regímenes y solo 2024-2025
# son comparables entre sí sin nota.
CANASTA_POBREZA = {2019: "2006", 2023: "2006", 2024: "2017", 2025: "2017"}


def metrica_pobreza(personas: pd.DataFrame, anio: int) -> list[dict]:
    """Métrica 31 — pobreza monetaria 0-17: total, por tramo y por
    departamento. La canasta de cada año va en la fuente (dos regímenes:
    ver CANASTA_POBREZA); quien grafique la serie corta donde cambia."""
    canasta = CANASTA_POBREZA.get(anio, "verificar")
    fuente = f"ECH {anio} (INE), microdatos ponderados; pobreza oficial INE, canasta {canasta}"
    salida = []
    v, n = pct_ponderado(personas, personas["pobre"], "ponderador_hogar")
    salida.append(filas("pobreza_0a17", anio, "total", v, "porcentaje", n, fuente))
    for tramo, grupo in personas.groupby("tramo_sipiav", observed=True):
        v, n = pct_ponderado(grupo, grupo["pobre"], "ponderador_hogar")
        salida.append(filas("pobreza_0a17", anio, f"tramo={tramo}", v, "porcentaje", n, fuente))
    for depto, grupo in personas.groupby("departamento"):
        v, n = pct_ponderado(grupo, grupo["pobre"], "ponderador_hogar")
        salida.append(filas("pobreza_0a17", anio, f"departamento={depto}", v, "porcentaje", n, fuente))
    return salida


def metrica_hacinamiento(hogares: pd.DataFrame, anio: int) -> list[dict]:
    """Métrica 32 — hacinamiento en hogares con NNA (>2 personas por
    cuarto, umbral heredado)."""
    fuente = f"ECH {anio} (INE); umbral INE/CEPAL >2 personas por cuarto"
    hacinado = (hogares["total_personas"] / hogares["cantidad_habitaciones"]) > UMBRAL_HACINAMIENTO
    salida = []
    v, n = pct_ponderado(hogares, hacinado, "ponderador_hogar")
    salida.append(filas("hacinamiento_hogares_nna", anio, "total", v, "porcentaje", n, fuente))
    for depto, grupo in hogares.groupby("departamento"):
        v, n = pct_ponderado(grupo, hacinado.loc[grupo.index], "ponderador_hogar")
        salida.append(filas("hacinamiento_hogares_nna", anio, f"departamento={depto}", v, "porcentaje", n, fuente))
    return salida


def metrica_vivienda(hogares: pd.DataFrame, anio: int) -> list[dict]:
    """Métrica 33 — condiciones de la vivienda en hogares con NNA (las
    carencias que el INE relevó ese año: 12 en 2019, 4 desde 2024,
    ninguna en 2023 — quiebre documentado)."""
    fuente = f"ECH {anio} (INE); 1=Sí/2=No, 99 excluido"
    salida = []
    for cond in CONDICIONES_VIVIENDA:
        if cond not in hogares.columns:
            continue
        flag = hogares[cond].map({1: True, 2: False})
        v, n = pct_ponderado(hogares, flag, "ponderador_hogar")
        salida.append(filas("vivienda_hogares_nna", anio, f"carencia={cond}", v, "porcentaje", n, fuente))
    return salida


def metrica_brecha_digital(hogares: pd.DataFrame, anio: int) -> list[dict]:
    """Métrica 34 — acceso digital en hogares con NNA."""
    fuente = f"ECH {anio} (INE); 1=Sí/2=No, 99 excluido"
    salida = []
    for col, nombre in [("tiene_internet", "internet"), ("tiene_pc", "pc"),
                        ("internet_fija", "internet_fija")]:
        if col not in hogares.columns:
            continue
        flag = hogares[col].map({1: True, 2: False})
        v, n = pct_ponderado(hogares, flag, "ponderador_hogar")
        salida.append(filas("brecha_digital_hogares_nna", anio, f"recurso={nombre}", v, "porcentaje", n, fuente))
        for estrato, grupo in hogares.groupby("estrato_tipo"):
            fv, fn = pct_ponderado(grupo, flag.loc[grupo.index], "ponderador_hogar")
            salida.append(filas("brecha_digital_hogares_nna", anio,
                                f"recurso={nombre};estrato={estrato}", fv, "porcentaje", fn, fuente))
    return salida


def metrica_fies(carpeta: Path, anio: int) -> list[dict]:
    """Métrica 35 — inseguridad alimentaria (FIES) en hogares con menores
    de 18 (umbral FAO 0,5, heredado)."""
    archivo = carpeta / "fies_hogares_con_menores.csv"
    if not archivo.exists():
        return []
    fies = pd.read_csv(archivo)
    fuente = f"ECH {anio}, módulo FIES (INE); umbral FAO 0,5"
    salida = []
    for col, nombre in [("prob_inseguridad_moderada", "moderada_o_severa"),
                        ("prob_inseguridad_severa", "severa")]:
        flag = fies[col] > UMBRAL_FIES
        v, n = pct_ponderado(fies, flag, "ponderador_fies")
        salida.append(filas("fies_hogares_menores", anio, f"nivel={nombre}", v, "porcentaje", n, fuente))
        con_chicos = fies[fies["tiene_menores_6"] == 1]
        v6, n6 = pct_ponderado(con_chicos, (con_chicos[col] > UMBRAL_FIES), "ponderador_fies")
        salida.append(filas("fies_hogares_menores", anio,
                            f"nivel={nombre};hogares_con_menores_de_6", v6, "porcentaje", n6, fuente))
    return salida


def metrica_victimizacion(carpeta: Path, anio: int) -> list[dict]:
    """Métrica 36 — victimización en hogares donde viven NNA: prevalencia
    a nivel de persona (definición heredada), por tipo de delito."""
    archivo = carpeta / "victimizacion_hogares_con_nna.csv"
    if not archivo.exists():
        return []
    vic = pd.read_csv(archivo)
    fuente = f"ECH {anio}, módulo victimización 2º semestre (INE)"
    salida = []
    for codigo, nombre in TIPOS_DELITO.items():
        flag = vic[codigo] == 1
        v, n = pct_ponderado(vic, flag, "ponderador_victimizacion")
        salida.append(filas("victimizacion_hogares_nna", anio, f"delito={nombre}", v, "porcentaje", n, fuente))
    alguno = (vic[list(TIPOS_DELITO)] == 1).any(axis=1)
    v, n = pct_ponderado(vic, alguno, "ponderador_victimizacion")
    salida.append(filas("victimizacion_hogares_nna", anio, "delito=Al menos uno", v, "porcentaje", n, fuente))
    return salida


def metrica_trabajo_adolescente(carpeta: Path, anio: int) -> list[dict]:
    """Métrica 19 — trabajo adolescente 14-17 (ECH, panel mensual):
    ocupación promedio de los 12 meses (mes a mes ponderado por W, luego
    promedio — regla heredada) e informalidad entre ocupados (no aporte a
    la seguridad social, f82==2 — criterio del paquete oficial ech de R)."""
    archivo = carpeta / "empleo_14a17.csv"
    if not archivo.exists():
        return []
    emp = pd.read_csv(archivo)
    emp = emp[emp["edad"].between(14, 17)]
    fuente = f"ECH {anio}, panel mensual de empleo (INE); promedio de 12 meses"
    salida = []

    def promedio_mensual(df: pd.DataFrame, flag_col) -> tuple[float, int]:
        valores = []
        for _mes, grupo in df.groupby("mes"):
            v, _ = pct_ponderado(grupo, flag_col(grupo), "ponderador_empleo")
            if not np.isnan(v):
                valores.append(v)
        return (round(float(np.mean(valores)), 2) if valores else np.nan), int(len(df))

    ocupado = lambda g: g["condicion_actividad_cod"] == 2  # noqa: E731
    v, n = promedio_mensual(emp, ocupado)
    salida.append(filas("trabajo_adolescente_14a17", anio, "ocupacion=total", v, "porcentaje", n, fuente))
    for sexo, grupo in emp.groupby("sexo"):
        etiqueta = {1: "Varones", 2: "Mujeres"}.get(sexo, str(sexo))
        v, n = promedio_mensual(grupo, ocupado)
        salida.append(filas("trabajo_adolescente_14a17", anio, f"ocupacion=sexo:{etiqueta}", v, "porcentaje", n, fuente))
    if "aporta_seguridad_social" in emp.columns:
        ocupados = emp[emp["condicion_actividad_cod"] == 2]
        informal = lambda g: g["aporta_seguridad_social"] == 2  # noqa: E731
        v, n = promedio_mensual(ocupados, informal)
        salida.append(filas("trabajo_adolescente_14a17", anio, "informalidad_entre_ocupados", v,
                            "porcentaje", n, fuente + "; f82==2 (no aporta)"))
    return salida


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    todas = []
    for anio in anios_disponibles():
        carpeta = DATOS / str(anio)
        personas = pd.read_csv(carpeta / "personas_0a17.csv")
        hogares = pd.read_csv(carpeta / "hogares_con_nna.csv")
        personas = preprocessing.normalizar_departamento(personas)
        hogares = preprocessing.normalizar_departamento(hogares)

        todas += metrica_pobreza(personas, anio)
        todas += metrica_hacinamiento(hogares, anio)
        todas += metrica_vivienda(hogares, anio)
        todas += metrica_brecha_digital(hogares, anio)
        todas += metrica_fies(carpeta, anio)
        todas += metrica_victimizacion(carpeta, anio)
        todas += metrica_trabajo_adolescente(carpeta, anio)
        print(f"{anio}: acumuladas {len(todas)} filas")

    df = pd.DataFrame(todas)
    df.to_csv(SALIDA / "metricas_ech_0a17.csv", index=False, encoding="utf-8")
    print(f"\n{len(df)} filas → {SALIDA / 'metricas_ech_0a17.csv'}")
    resumen = df[df["categoria"].isin(["total", "ocupacion=total"]) |
                 df["categoria"].str.startswith("nivel=") |
                 (df["categoria"] == "delito=Al menos uno")]
    print(resumen.to_string(index=False, max_colwidth=40))


if __name__ == "__main__":
    main()
