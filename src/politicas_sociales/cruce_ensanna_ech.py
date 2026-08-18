"""Cruce ENSANNA × ECH por gradiente socioeconómico y región (cruce 3).

Contrasta la prevalencia de trabajo infantil de la ENSANNA 2024 (única
fuente de prevalencia del proyecto) con las condiciones socioeconómicas
de la infancia calculadas sobre la ECH 2024, en los dos ejes que el
boletín oficial permite: nivel socioeconómico y región
(Montevideo/Interior). Es una **comparación de gradientes, no de
valores** (decisión del catálogo): se compara la forma de cada gradiente
(monotonía y magnitud relativa entre extremos), nunca los niveles.

Limitaciones que acotan toda lectura:

- **Las escalas socioeconómicas no son la misma variable.** La ENSANNA
  clasifica por INSE (índice de CINVE, nacional, 5 niveles); la ECH
  extraída solo trae un ordenamiento socioeconómico comparable para
  Montevideo (estred13, estratos 1 bajo a 5 alto — los códigos 6-12 son
  estratos geográficos del interior, sin orden socioeconómico). El
  gradiente ECH se calcula entonces solo sobre Montevideo y el de la
  ENSANNA es nacional: por eso jamás se comparan niveles.
- **Universos distintos**: ENSANNA 5-17 (trabajo infantil), ECH 0-17
  (pobreza) y 14-17 (ocupación, el módulo de empleo no releva menores de
  14).
- **El boletín ENSANNA no publica errores estándar** ni microdatos (INE
  los lista "en análisis"): la monotonía del gradiente ENSANNA no puede
  testearse; se toma como está publicada.
- La ENSANNA mide **declaración de actividades** por los hogares:
  posible subdeclaración, y no necesariamente pareja entre niveles
  socioeconómicos.

Salida: resultados/cruces/cruce_ensanna_ech.csv
"""

from __future__ import annotations

import pandas as pd

from politicas_sociales import config
from politicas_sociales.metricas_ech import pct_ponderado

CURADOS = config.DATOS_CURADOS
SALIDA = config.RESULTADOS / "cruces"
ANIO_ECH = 2024  # mismo año de campo que la ENSANNA

ESTRATOS_MONTEVIDEO = {1: "Bajo", 2: "Medio bajo", 3: "Medio",
                       4: "Medio alto", 5: "Alto"}
ORDEN_NSE = ["Bajo", "Medio bajo", "Medio", "Medio alto", "Alto"]


def fila(fuente, dimension, categoria, orden, metrica, valor, n, detalle):
    return {"fuente": fuente, "dimension": dimension, "categoria": categoria,
            "orden": orden, "metrica": metrica, "valor": valor,
            "n_muestral": n, "detalle": detalle}


def gradiente_ensanna(ens: pd.DataFrame, metrica: str, prefijo: str,
                      dimension: str, orden: list[str]) -> list[dict]:
    """Filas del boletín ENSANNA para una métrica y una dimensión."""
    s = ens[(ens["metrica"] == metrica) & (ens["unidad"] == "porcentaje")
            & (ens["categoria"].str.startswith(prefijo))]
    salida = []
    for _, r in s.iterrows():
        categoria = r["categoria"].removeprefix(prefijo)
        salida.append(fila("ensanna_2024", dimension, categoria,
                           orden.index(categoria) if categoria in orden else None,
                           metrica, r["valor"], None, r["fuente"]))
    return salida


def pobreza_por_estrato_montevideo(personas: pd.DataFrame) -> list[dict]:
    """Pobreza 0-17 ponderada por estrato socioeconómico de Montevideo."""
    mvd = personas[personas["departamento"].str.upper().str.strip() == "MONTEVIDEO"]
    salida = []
    for codigo, etiqueta in ESTRATOS_MONTEVIDEO.items():
        grupo = mvd[mvd["estrato_tipo"] == codigo]
        v, n = pct_ponderado(grupo, grupo["pobre"], "ponderador_hogar")
        salida.append(fila("ech_2024", "nse", etiqueta, ORDEN_NSE.index(etiqueta),
                           "pobreza_0a17_montevideo", v, n,
                           f"ECH {ANIO_ECH} (INE); estred13={codigo}, solo Montevideo"))
    return salida


def pobreza_por_region(personas: pd.DataFrame) -> list[dict]:
    """Pobreza 0-17 ponderada, Montevideo contra Interior."""
    es_mvd = personas["departamento"].str.upper().str.strip() == "MONTEVIDEO"
    salida = []
    for region, grupo in [("Montevideo", personas[es_mvd]),
                          ("Interior", personas[~es_mvd])]:
        v, n = pct_ponderado(grupo, grupo["pobre"], "ponderador_hogar")
        salida.append(fila("ech_2024", "region", region, None, "pobreza_0a17",
                           v, n, f"ECH {ANIO_ECH} (INE), microdatos ponderados"))
    return salida


def ocupacion_por_region(empleo: pd.DataFrame) -> list[dict]:
    """Ocupación 14-17 por región: mes a mes ponderado y luego promedio
    de los meses (regla del panel, nunca un solo pool)."""
    emp = empleo[empleo["edad"].between(14, 17)]
    es_mvd = emp["departamento"].str.upper().str.strip() == "MONTEVIDEO"
    salida = []
    for region, grupo in [("Montevideo", emp[es_mvd]), ("Interior", emp[~es_mvd])]:
        valores = []
        for _mes, g in grupo.groupby("mes"):
            v, _ = pct_ponderado(g, g["condicion_actividad_cod"] == 2,
                                 "ponderador_empleo")
            valores.append(v)
        promedio = round(float(pd.Series(valores).mean()), 2)
        salida.append(fila("ech_2024", "region", region, None,
                           "ocupacion_14a17", promedio, len(grupo),
                           f"ECH {ANIO_ECH}, panel mensual; promedio de 12 meses"))
    return salida


def es_monotono_decreciente(valores: list[float]) -> bool:
    return all(a >= b for a, b in zip(valores, valores[1:]))


def main() -> None:
    ens = pd.read_csv(CURADOS / "ensanna_2024.csv")
    personas = pd.read_csv(config.DATA_DIR / "ech" / str(ANIO_ECH) / "personas_0a17.csv")
    empleo = pd.read_csv(config.DATA_DIR / "ech" / str(ANIO_ECH) / "empleo_14a17.csv")

    filas = []
    filas += gradiente_ensanna(ens, "trabajo_infantil", "nse=", "nse", ORDEN_NSE)
    filas += gradiente_ensanna(ens, "trabajo_infantil", "region=", "region", [])
    filas += gradiente_ensanna(ens, "trabajo_frontera_produccion", "region=",
                               "region", [])
    filas += pobreza_por_estrato_montevideo(personas)
    filas += pobreza_por_region(personas)
    filas += ocupacion_por_region(empleo)

    todo = pd.DataFrame(filas)
    SALIDA.mkdir(parents=True, exist_ok=True)
    todo.to_csv(SALIDA / "cruce_ensanna_ech.csv", index=False, encoding="utf-8")
    print(f"{len(todo)} filas → {SALIDA / 'cruce_ensanna_ech.csv'}\n")

    def serie(fuente, dimension, metrica):
        s = todo[(todo["fuente"] == fuente) & (todo["dimension"] == dimension)
                 & (todo["metrica"] == metrica)]
        return s.sort_values("orden") if dimension == "nse" else s

    ens_nse = serie("ensanna_2024", "nse", "trabajo_infantil")
    ech_nse = serie("ech_2024", "nse", "pobreza_0a17_montevideo")
    print("Gradiente socioeconómico (bajo → alto):")
    print(f"  Trabajo infantil 5-17 (ENSANNA, INSE nacional): "
          f"{ens_nse['valor'].tolist()}  monótono decreciente: "
          f"{es_monotono_decreciente(ens_nse['valor'].tolist())}  "
          f"razón extremos: {ens_nse['valor'].iloc[0] / ens_nse['valor'].iloc[-1]:.1f}")
    print(f"  Pobreza 0-17 (ECH, estratos de Montevideo):      "
          f"{ech_nse['valor'].tolist()}  monótono decreciente: "
          f"{es_monotono_decreciente(ech_nse['valor'].tolist())}  "
          f"razón extremos: {ech_nse['valor'].iloc[0] / ech_nse['valor'].iloc[-1]:.1f}")
    print("\nRegión (Montevideo / Interior):")
    for fuente, metrica in [("ensanna_2024", "trabajo_infantil"),
                            ("ensanna_2024", "trabajo_frontera_produccion"),
                            ("ech_2024", "ocupacion_14a17"),
                            ("ech_2024", "pobreza_0a17")]:
        s = serie(fuente, "region", metrica).set_index("categoria")["valor"]
        print(f"  {metrica} ({fuente}): Montevideo {s['Montevideo']} · "
              f"Interior {s['Interior']}")


if __name__ == "__main__":
    main()
