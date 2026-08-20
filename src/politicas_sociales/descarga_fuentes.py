"""Carga automática de las fuentes documentales del proyecto.

Descarga a `data/` los archivos de SIPIAV, INAU, ENSANNA, CETI, CONAPEES
e INE desde las URLs citadas en `docs/RELEVAMIENTO_DE_DATOS.md` (el
manifiesto de abajo es su transcripción ejecutable, verificada contra
los servidores reales el 2026-08-20), y las publicaciones de UNICEF
Uruguay recorriendo su Biblioteca Digital (catálogo PMB: páginas de tema
→ registros → `doc_num.php?explnum_id=N`).

Reglas:

- **Idempotente**: un archivo ya presente y con el formato esperado no
  se vuelve a bajar — el botón "cargar de nuevo" no castiga al usuario
  que ya cargó. Las publicaciones UNICEF ya descargadas se reconocen por
  el id del ejemplar al final del nombre (`*_<id>.pdf`), que la
  curaduría original conservó al renombrar por título.
- **Nada se da por descargado sin verificarlo**: cada archivo se valida
  por su firma de formato (un PDF empieza con %PDF, un XLSX con PK) y un
  tamaño mínimo — una página de error del servidor guardada como si
  fuera el archivo no pasa. La verificación de CONTENIDO (que el
  documento sea el que dice ser) ya se hizo al curar el manifiesto: la
  lección del "plan CETI" que era de Argentina está documentada en
  RELEVAMIENTO_DE_DATOS.md y las URLs de aquí son las corregidas.
- Los microdatos de la ECH quedan EXPLÍCITAMENTE afuera: el INE exige
  aceptar sus términos personalmente, así que esa carga es siempre
  manual (ver el paso de datos del flujo guiado).

Uso:

    python -m politicas_sociales.descarga_fuentes
    python -m politicas_sociales.descarga_fuentes --sin-unicef
    python -m politicas_sociales.descarga_fuentes --destino C:/tmp/data

Código de salida: 0 si todo quedó presente y válido; 1 si algo falló.
"""

from __future__ import annotations

import re
import ssl
import sys
import urllib.request
from pathlib import Path

from . import config

# Mismo User-Agent que vigilancia.py: el sitio de INAU responde 404 a
# clientes sin User-Agent de navegador (verificado 2026-08-20).
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_TIMEOUT_SEGUNDOS = 300

# Firma de formato y tamaño mínimo por tipo: suficiente para distinguir
# el archivo real de una página de error guardada con su nombre.
_FIRMAS = {
    "pdf": (b"%PDF", 10_000),
    "xlsx": (b"PK", 4_000),
    "html": (b"<", 20_000),
}

# --- Manifiesto (transcripción ejecutable de RELEVAMIENTO_DE_DATOS.md) ---

_SIPIAV_IDS = {
    2013: 6469, 2014: 6470, 2015: 6471, 2016: 6472, 2017: 6473,
    2018: 6474, 2019: 6475, 2020: 6846, 2021: 7641, 2022: 10367,
    2023: 10366, 2024: 10368, 2025: 11255,
}

_DEPARTAMENTOS_INAU = [
    "artigas", "canelones", "cerrolargo", "colonia", "durazno", "flores",
    "florida", "lavalleja", "maldonado", "montevideo", "paysandu",
    "rionegro", "rivera", "rocha", "salto", "sanjose", "soriano",
    "tacuarembo", "treintaytres",
]

_MIGRADO = "https://www.inau.gub.uy/sites/default/files/migrado-docs"
_INE_REV2025 = ("https://www5.ine.gub.uy/documents/Demograf%C3%ADayEESS/"
                "SERIES%20Y%20OTROS/Estimaciones%20y%20proyecciones/"
                "Revisi%C3%B3n%202025")


def _entrada(destino: str, url: str, tipo: str) -> dict:
    return {"destino": destino, "url": url, "tipo": tipo}


MANIFIESTO = (
    [
        _entrada(f"sipiav/{anio}/informe_gestion_sipiav_{anio}.pdf",
                 f"https://www.inau.gub.uy/sipiav/download/{id_}/1494/16", "pdf")
        for anio, id_ in _SIPIAV_IDS.items()
    ]
    + [
        _entrada("inau/2020-2025/indicadoresanualesspe-inau2020-2025.xlsx",
                 f"{_MIGRADO}/indicadoresanualesspe-inau2020-2025.xlsx", "xlsx"),
    ]
    + [
        _entrada(f"inau/2020-2025/departamentos/datosspe{depto}-3.xlsx",
                 f"{_MIGRADO}/datosspe{depto}-3.xlsx", "xlsx")
        for depto in _DEPARTAMENTOS_INAU
    ]
    + [
        # Reportes estadísticos de abril 2025 — mapeo id → reporte
        # verificado contra el nombre real que revela cada redirección
        # (10361 → 2025_04_rpp, 10362 → 2025_4_raf, 10363 → 2025_04_rdvf).
        _entrada("inau/2025/reporte_poblacion_y_proyectos_abr2025.xlsx",
                 "https://www.inau.gub.uy/inau/download/10361/1494/16", "xlsx"),
        _entrada("inau/2025/reporte_acogimiento_familiar_abr2025.xlsx",
                 "https://www.inau.gub.uy/inau/download/10362/1494/16", "xlsx"),
        _entrada("inau/2025/reporte_derecho_vivir_en_familia_abr2025.xlsx",
                 "https://www.inau.gub.uy/inau/download/10363/1494/16", "xlsx"),
        _entrada("ensanna/2024/informe_trabajo_infantil_ensanna_2024.html",
                 "https://www5.ine.gub.uy/documents/Demograf%C3%ADayEESS/HTML/ECH/"
                 "ENSANNA/Informe-trabajo-infantil-2024.html", "html"),
        _entrada("ensanna/2010/magnitud_caracteristicas_trabajo_infantil_2010.pdf",
                 "https://www5.ine.gub.uy/documents/Demograf%C3%ADayEESS/PDF/"
                 "Informes%20Demogr%C3%A1ficos/Trabajo%20infantil/"
                 "Magnitud%20y%20Caracter%C3%ADsticas%20del%20Trabajo%20Infantil%20en%20Uruguay.pdf",
                 "pdf"),
        _entrada("ceti/2003-2005/plan_accion_prevencion_erradicacion_trabajo_infantil_2003_2005.pdf",
                 "http://www.annaobserva.org/observatorio/wp-content/uploads/2018/03/"
                 "Plan-de-Acci%C3%B3n-para-la-Prevenci%C3%B3n.pdf", "pdf"),
        _entrada("conapees/2023/estudio_explotacion_sexual_entornos_digitales_unfpa_2023.pdf",
                 "https://uruguay.unfpa.org/sites/default/files/pub-pdf/"
                 "pubexplotacionsexual23web.pdf", "pdf"),
        _entrada("conapees/2023/estudio_explotacion_sexual_flacso_2023.pdf",
                 "https://flacso.edu.uy/wp-content/uploads/2023/12/"
                 "EXPLOTACION-SEXUAL-HACIA-NINAS-NINOS-Y-ADOLESCENTES-COMPLETO.pdf", "pdf"),
        _entrada("conapees/2023-2028/iii_plan_nacional_esnna_2023_2028.pdf",
                 "https://www.inau.gub.uy/conapees/download/10402/1494/16", "pdf"),
        _entrada("ine/proyecciones_rev2025/B11_uruguay_edad_simple_2024_2070.xlsx",
                 f"{_INE_REV2025}/B.1.1%20Uruguay%20(100ymas)2024-2070.xlsx", "xlsx"),
        _entrada("ine/proyecciones_rev2025/B12_departamentos_edad_simple_2024_2045.xlsx",
                 f"{_INE_REV2025}/B.1.2%20Departamentos%20(100ymas)2024-2045.xlsx", "xlsx"),
    ]
)

# --- Biblioteca UNICEF (recorrido dinámico del catálogo PMB) ---

_URL_UNICEF = "https://bibliotecaunicef.uy/opac_css/index.php"
_URL_UNICEF_DOC = "https://bibliotecaunicef.uy/opac_css/doc_num.php?explnum_id={id}"
_CARPETA_UNICEF = "unicef"
# La curaduría original renombró cada PDF por su título conservando el id
# del ejemplar al final (p. ej. el_trabajo_infantil_49.pdf) — ese sufijo
# es la memoria de qué ya se descargó.
_PATRON_ID_LOCAL = re.compile(r"_(\d+)\.pdf$", re.IGNORECASE)


def descargar_bytes(url: str) -> bytes:
    pedido = urllib.request.Request(url, headers={"User-Agent": _UA})
    contexto = ssl.create_default_context()
    with urllib.request.urlopen(pedido, timeout=_TIMEOUT_SEGUNDOS, context=contexto) as r:
        return r.read()


def es_valido(contenido: bytes, tipo: str) -> bool:
    firma, minimo = _FIRMAS[tipo]
    return len(contenido) >= minimo and contenido.lstrip()[:16].lstrip(b"\xef\xbb\xbf").startswith(firma)


def archivo_valido(ruta: Path, tipo: str) -> bool:
    if not ruta.is_file():
        return False
    with ruta.open("rb") as f:
        inicio = f.read(64)
    firma, minimo = _FIRMAS[tipo]
    return ruta.stat().st_size >= minimo and inicio.lstrip()[:16].lstrip(b"\xef\xbb\xbf").startswith(firma)


def descargar_manifiesto(destino_raiz: Path) -> list[dict]:
    """Descarga cada entrada del manifiesto que falte (o esté corrupta) y
    devuelve el resultado por archivo: ya_estaba / descargado / error."""
    resultados = []
    for entrada in MANIFIESTO:
        ruta = destino_raiz / entrada["destino"]
        if archivo_valido(ruta, entrada["tipo"]):
            resultados.append({**entrada, "resultado": "ya_estaba"})
            continue
        try:
            contenido = descargar_bytes(entrada["url"])
            if not es_valido(contenido, entrada["tipo"]):
                raise ValueError(
                    f"lo descargado no tiene formato {entrada['tipo']} "
                    f"({len(contenido)} bytes) — puede ser una página de error")
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(contenido)
            resultados.append({**entrada, "resultado": "descargado"})
        except Exception as e:
            resultados.append({**entrada, "resultado": "error", "detalle": str(e)})
    return resultados


def ids_unicef_locales(destino_raiz: Path) -> set[int]:
    carpeta = destino_raiz / _CARPETA_UNICEF
    if not carpeta.is_dir():
        return set()
    return {
        int(m.group(1))
        for pdf in carpeta.rglob("*.pdf")
        if (m := _PATRON_ID_LOCAL.search(pdf.name))
    }


def ids_unicef_en_catalogo() -> set[int]:
    """Recorre el catálogo: portada de TEMAS → páginas de tema → registros
    → ids de ejemplar descargable (explnum)."""
    portada = descargar_bytes(f"{_URL_UNICEF}?lvl=cmspage&pageid=6&id_rubrique=82").decode("utf-8", "replace")
    articulos = sorted({int(i) for i in re.findall(r"id_article=(\d+)", portada)})
    notices: set[int] = set()
    for articulo in articulos:
        pagina = descargar_bytes(f"{_URL_UNICEF}?lvl=cmspage&pageid=4&id_article={articulo}").decode("utf-8", "replace")
        notices |= {int(i) for i in re.findall(r"notice_display&(?:amp;)?id=(\d+)", pagina)}
    explnums: set[int] = set()
    for notice in sorted(notices):
        detalle = descargar_bytes(f"{_URL_UNICEF}?lvl=notice_display&id={notice}").decode("utf-8", "replace")
        explnums |= {int(i) for i in re.findall(r"explnum_id=(\d+)", detalle)}
    return explnums


def descargar_unicef(destino_raiz: Path, limite: int | None = None) -> list[dict]:
    """Descarga los ejemplares del catálogo que no estén ya en data/unicef.

    Los nuevos quedan en `unicef/biblioteca/explnum_<id>.pdf` — sin
    clasificar por año ni renombrar por título (eso fue curaduría manual,
    documentada en RELEVAMIENTO_DE_DATOS.md, y se hace al usarlos).
    """
    ya_presentes = ids_unicef_locales(destino_raiz)
    resultados = []
    faltantes = sorted(ids_unicef_en_catalogo() - ya_presentes)
    if limite is not None:
        resultados += [{"id": i, "resultado": "omitido_por_limite"} for i in faltantes[limite:]]
        faltantes = faltantes[:limite]
    for id_ in faltantes:
        try:
            contenido = descargar_bytes(_URL_UNICEF_DOC.format(id=id_))
            if not es_valido(contenido, "pdf"):
                raise ValueError(f"el ejemplar {id_} no es un PDF ({len(contenido)} bytes)")
            ruta = destino_raiz / _CARPETA_UNICEF / "biblioteca" / f"explnum_{id_}.pdf"
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(contenido)
            resultados.append({"id": id_, "resultado": "descargado"})
        except Exception as e:
            resultados.append({"id": id_, "resultado": "error", "detalle": str(e)})
    return resultados


def main() -> None:
    argumentos = sys.argv[1:]
    destino = config.DATA_DIR
    if "--destino" in argumentos:
        destino = Path(argumentos[argumentos.index("--destino") + 1])
    limite = None
    if "--limite-unicef" in argumentos:
        limite = int(argumentos[argumentos.index("--limite-unicef") + 1])

    resultados = descargar_manifiesto(destino)
    conteo = {"ya_estaba": 0, "descargado": 0, "error": 0}
    for r in resultados:
        conteo[r["resultado"]] += 1
        if r["resultado"] == "error":
            print(f"[ERROR] {r['destino']}: {r['detalle']}")
        elif r["resultado"] == "descargado":
            print(f"[OK] {r['destino']}")
    print(f"Manifiesto: {conteo['descargado']} descargados, "
          f"{conteo['ya_estaba']} ya estaban, {conteo['error']} con error.")

    errores_unicef = 0
    if "--sin-unicef" not in argumentos:
        unicef = descargar_unicef(destino, limite=limite)
        bajados = sum(1 for r in unicef if r["resultado"] == "descargado")
        errores_unicef = sum(1 for r in unicef if r["resultado"] == "error")
        omitidos = sum(1 for r in unicef if r["resultado"] == "omitido_por_limite")
        for r in unicef:
            if r["resultado"] == "error":
                print(f"[ERROR] unicef explnum {r['id']}: {r['detalle']}")
        print(f"Biblioteca UNICEF: {bajados} ejemplares nuevos descargados, "
              f"{len(ids_unicef_locales(destino))} ya presentes"
              + (f", {omitidos} omitidos por el límite" if omitidos else "")
              + (f", {errores_unicef} con error" if errores_unicef else "") + ".")

    sys.exit(1 if conteo["error"] or errores_unicef else 0)


if __name__ == "__main__":
    main()
