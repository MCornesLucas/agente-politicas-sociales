"""Métrica de primera infancia sobre los microdatos de la ENDIS 2023
(tema 6 de docs/CATALOGO_DE_METRICAS.md, métrica 37).

Calcula la cobertura de centros de primera infancia por tramo de edad y
tipo de prestador a partir de la base de niño seleccionado de la
Encuesta de Nutrición, Desarrollo Infantil y Salud (ENDIS), cohorte 2023,
publicada para terceros por el INE en su catálogo ANDA (entrada 765), y
exporta una tabla ordenada a `resultados/endis/` (versionada: son
agregados ponderados, no microdatos).

Origen de la métrica: fue pedida por un usuario del flujo guiado como
métrica a medida sobre su propia carga de la ENDIS (2026-08-20) y el
dueño decidió incorporarla al catálogo permanente (2026-09-05) porque
cubre el tramo de 0 a 4 años, que ningún otro tema describe.

Variables usadas (verificadas contra el archivo; la base para terceros
no trae etiquetas de variable ni de valor):

- `PEREDADMESES`: edad en meses (0 a 59).
- `E239_recod`: tipo de centro al que asiste, con la etiqueta en el
  propio dato ("Centros de primera infancia INAU", "Centros dependientes
  de ANEP", "Centros privados (colegio, jardín, etc)", "Otro público");
  el código "0" reúne a quienes no tienen centro registrado.
- `E238`: 1 = asiste a un centro (siempre con tipo en E239_recod),
  2 = declara no asistir, 0 = sin dato de asistencia (concentrado en los
  menores de un año). La base no permite separar con seguridad "no
  asiste" de "sin dato" en la mayoría de los casos, así que la métrica
  informa **"sin centro registrado"** (E239_recod == "0"), nunca
  "no asiste" a secas.
- `W`: factor de expansión de la encuesta. Toda estimación se pondera;
  la proporción simple de la muestra no se usa nunca.

Regla de celdas chicas (docs/METODOLOGIA.md): cada estimación va con su
n muestral sin ponderar para que el informe marque las celdas con menos
de 30 casos.

Ubicación de los microdatos: `data/endis_microdatos/2023/` (carga manual
por el usuario, aceptando los términos del INE — nunca descarga
automática). Si esa carpeta no existe, se busca el archivo en las
fuentes propias registradas en `data/usuario/`, que es donde lo dejó la
carga original.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from politicas_sociales import config

ANIO = 2023
ARCHIVO = "base_ninoselecc_endis2023_terceros.csv"
DATOS = config.DATA_DIR / "endis_microdatos" / str(ANIO)
SALIDA = config.RESULTADOS / "endis"
CSV_SALIDA = SALIDA / "cobertura_primera_infancia_2023.csv"

LIMITES_TRAMOS = [-1, 11, 23, 35, 47, 59]
TRAMOS = ["0-11 meses", "12-23 meses", "24-35 meses", "36-47 meses", "48-59 meses"]
TOTAL = "Total 0-59 meses"

SIN_CENTRO = "Sin centro registrado"
PRESTADORES = [
    "Centros de primera infancia INAU",
    "Centros dependientes de ANEP",
    "Centros privados (colegio, jardín, etc)",
    "Otro público",
    SIN_CENTRO,
]


def localizar_microdatos() -> Path:
    """La base de niño seleccionado: en data/endis_microdatos/2023/ o, si
    no está ahí, en alguna fuente propia registrada en data/usuario/."""
    candidata = DATOS / ARCHIVO
    if candidata.is_file():
        return candidata
    usuario = config.DATA_DIR / "usuario"
    if usuario.is_dir():
        for carpeta in sorted(p for p in usuario.iterdir() if p.is_dir()):
            if (carpeta / ARCHIVO).is_file():
                return carpeta / ARCHIVO
    raise FileNotFoundError(
        f"No se encontró {ARCHIVO}: cargarlo en {DATOS} (catálogo ANDA del INE, "
        "entrada 765, aceptando sus términos) o registrarlo como fuente propia.")


def cobertura_por_tramo(base: pd.DataFrame, anio: int = ANIO) -> pd.DataFrame:
    """Tabla larga: una fila por (tramo, prestador) con el porcentaje
    ponderado del tramo y los casos de la muestra, más las filas del total
    0-59 meses. Los porcentajes de cada tramo suman 100."""
    df = base[["PEREDADMESES", "E239_recod", "W"]].copy()
    df["tramo"] = pd.cut(df["PEREDADMESES"], LIMITES_TRAMOS, labels=TRAMOS)
    df["prestador"] = df["E239_recod"].astype(str).replace({"0": SIN_CENTRO})
    desconocidos = set(df["prestador"]) - set(PRESTADORES)
    if desconocidos:
        raise ValueError(f"Categorías de E239_recod no previstas: {sorted(desconocidos)}")

    peso = (pd.crosstab(df["tramo"], df["prestador"], values=df["W"], aggfunc="sum")
            .reindex(index=TRAMOS, columns=PRESTADORES).fillna(0.0))
    casos = (pd.crosstab(df["tramo"], df["prestador"])
             .reindex(index=TRAMOS, columns=PRESTADORES).fillna(0).astype(int))
    peso.loc[TOTAL] = peso.sum(axis=0)
    casos.loc[TOTAL] = casos.sum(axis=0)
    porcentaje = peso.div(peso.sum(axis=1), axis=0) * 100

    filas = []
    for tramo in TRAMOS + [TOTAL]:
        for prestador in PRESTADORES:
            filas.append({
                "anio": anio,
                "tramo": tramo,
                "prestador": prestador,
                "porcentaje": round(float(porcentaje.loc[tramo, prestador]), 1),
                "casos_muestra": int(casos.loc[tramo, prestador]),
                "casos_muestra_tramo": int(casos.loc[tramo].sum()),
            })
    return pd.DataFrame(filas)


def main() -> None:
    origen = localizar_microdatos()
    base = pd.read_csv(origen, low_memory=False)
    tabla = cobertura_por_tramo(base)
    SALIDA.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(CSV_SALIDA, index=False, encoding="utf-8")
    print(f"ENDIS {ANIO}: {len(base)} niñas y niños en la muestra, leídos de {origen}")
    print(f"{len(tabla)} filas escritas en {CSV_SALIDA}")
    ancha = tabla.pivot(index="tramo", columns="prestador", values="porcentaje").reindex(TRAMOS + [TOTAL])
    print(ancha.to_string())


if __name__ == "__main__":
    main()
