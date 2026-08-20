"""Vigilancia de las fuentes de terceros pendientes.

El proyecto espera publicaciones que no dependen de él (ver
docs/RELEVAMIENTO_DE_DATOS.md): los microdatos de la ENSANNA 2024 en el
catálogo ANDA del INE, las estimaciones retrospectivas de la revisión
2025 de las proyecciones de población, una serie ESNNA oficial nueva de
CONAPEES, el plan del CETI posterior a la ENSANNA y las publicaciones
nuevas de UNICEF Uruguay en su biblioteca digital. Hasta ahora cada
revisión era manual; este módulo la vuelve repetible: descarga cada
fuente, extrae una señal concreta y la compara contra el estado conocido
(el baseline versionado en `datos_curados/vigilancia_baseline.json`).

Reglas de diseño (las mismas de los guardianes del proyecto):

- Ninguna fuente queda "sin novedad" por no poder mirarla: si la página
  no responde, el estado es NO ACCESIBLE, y si responde pero ya no tiene
  la estructura esperada (sitios que se rediseñan: le pasó al de INAU en
  2026), el estado es ILEGIBLE. Verde solo cuando se miró de verdad.
- La señal de cada fuente se calibró contra el contenido real del
  2026-08-20 (direcciones y estructura verificadas ese día):
  el catálogo ANDA vive en www4.ine.gub.uy/Anda5 (el host anterior
  anda.ine.gub.uy dejó de existir) y el sitio de INAU migró a Drupal
  (las páginas /conapees y /sipiav desaparecieron; las noticias viven en
  /sala-de-prensa/noticias con enlaces /noticias/<año>/<titular>).

Uso:

    python -m politicas_sociales.vigilancia
    python -m politicas_sociales.vigilancia --actualizar-baseline

Código de salida: 0 todo sin novedad; 2 hay novedades para revisar;
1 alguna fuente no accesible o ilegible (y ninguna novedad).
`--actualizar-baseline` se corre después de revisar una novedad e
incorporarla al proyecto: deja el estado actual como nuevo punto de
comparación.
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import urllib.request

from . import bitacora, config

BASELINE = config.DATOS_CURADOS / "vigilancia_baseline.json"

# Sin User-Agent de navegador, el sitio nuevo de INAU responde 404 a
# páginas que existen (verificado el 2026-08-20).
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_TIMEOUT_SEGUNDOS = 45


def descargar(url: str) -> str:
    pedido = urllib.request.Request(url, headers={"User-Agent": _UA})
    contexto = ssl.create_default_context()
    with urllib.request.urlopen(pedido, timeout=_TIMEOUT_SEGUNDOS, context=contexto) as r:
        return r.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Análisis por fuente: cada función recibe el texto descargado y el estado
# conocido (baseline) y devuelve un dict con "estado" (sin_novedad /
# novedad / ilegible), "detalle" y "actual" (lo que se guardaría como
# nuevo baseline). Son funciones puras: los tests las ejercitan con
# contenido sintético en las dos direcciones, sin red.
# ---------------------------------------------------------------------------


def analizar_anda(texto: str, conocido: dict) -> dict:
    """Catálogo ANDA (export CSV): ¿apareció la ENSANNA?"""
    primera_linea = texto.splitlines()[0] if texto.splitlines() else ""
    if not {"id", "idno", "title"} <= set(primera_linea.lstrip("﻿").split(",")):
        return {"estado": "ilegible",
                "detalle": "El export CSV del catálogo ya no trae el encabezado esperado (id,idno,title,...)."}
    filas = texto.splitlines()[1:]
    entradas = len(filas)
    con_ensanna = [f for f in filas if re.search(r"ensanna|actividades de ni", f, re.IGNORECASE)]
    actual = {"entradas_catalogo": entradas, "entradas_ensanna": len(con_ensanna)}
    if len(con_ensanna) > conocido.get("entradas_ensanna", 0):
        return {"estado": "novedad", "actual": actual,
                "detalle": ("La ENSANNA apareció en el catálogo ANDA — revisar si publica microdatos: "
                            + "; ".join(f[:120] for f in con_ensanna[:3]))}
    detalle = f"Sin ENSANNA en el catálogo ({entradas} entradas"
    if entradas != conocido.get("entradas_catalogo", entradas):
        detalle += f"; antes {conocido['entradas_catalogo']} — hay entradas nuevas de otros temas"
    return {"estado": "sin_novedad", "actual": actual, "detalle": detalle + ")."}


def analizar_retrospectivas(texto: str, conocido: dict) -> dict:
    """Página de proyecciones rev. 2025 del INE: ¿se publicaron las
    estimaciones retrospectivas (archivos A.*)?"""
    if "royeccion" not in texto:  # cubre Proyeccion/proyección con y sin tilde
        return {"estado": "ilegible",
                "detalle": "La página de proyecciones ya no menciona 'proyecciones' — cambió su estructura."}
    menciones = len(re.findall(r"retrospectiv", texto, re.IGNORECASE))
    actual = {"menciones_retrospectivas": menciones}
    if menciones > conocido.get("menciones_retrospectivas", 0):
        return {"estado": "novedad", "actual": actual,
                "detalle": (f"La página menciona 'retrospectivas' ({menciones} veces): "
                            "revisar si ya están los archivos A.* con las estimaciones 2012-2023.")}
    return {"estado": "sin_novedad", "actual": actual,
            "detalle": "La página sigue sin mencionar estimaciones retrospectivas."}


_PATRON_NOTICIA_INAU = re.compile(r'href="(/noticias/[0-9]{4}/[^"]+)"')
_CLAVES_ESNNA = ("explotacion", "explotaci%C3%B3n", "conapees", "esnna")


def analizar_noticias_inau(texto: str, conocido: dict) -> dict:
    """Noticias de INAU: ¿hay novedades de CONAPEES / explotación sexual
    (la serie ESNNA oficial se anuncia por ahí, típicamente cada 7 de
    diciembre)?"""
    slugs = sorted(set(_PATRON_NOTICIA_INAU.findall(texto)))
    if not slugs:
        return {"estado": "ilegible",
                "detalle": "La página de noticias de INAU no muestra ningún enlace /noticias/<año>/... — cambió su estructura."}
    relevantes = sorted(s for s in slugs if any(c in s.lower() for c in _CLAVES_ESNNA))
    vistas = set(conocido.get("noticias_vistas", []))
    nuevas = [s for s in relevantes if s not in vistas]
    actual = {"noticias_vistas": sorted(set(relevantes) | vistas)}
    if nuevas:
        return {"estado": "novedad", "actual": actual,
                "detalle": "Noticias nuevas de CONAPEES/explotación sexual en INAU: "
                           + "; ".join("https://www.inau.gub.uy" + s for s in nuevas)}
    return {"estado": "sin_novedad", "actual": actual,
            "detalle": f"Sin noticias nuevas de CONAPEES/ESNNA ({len(slugs)} noticias revisadas)."}


_PATRON_CONTENIDO_CETI = re.compile(
    r'href="(/ministerio-trabajo-seguridad-social/comunicacion/(?:noticias|publicaciones)/[^"]+)"')


def analizar_ceti(texto: str, conocido: dict) -> dict:
    """Página del CETI (MTSS): ¿hay contenidos nuevos (el plan posterior a
    la ENSANNA se anunciaría como noticia o publicación de esa página)?"""
    if "Trabajo Infantil" not in texto:
        return {"estado": "ilegible",
                "detalle": "La página del CETI ya no dice 'Trabajo Infantil' — cambió su estructura."}
    enlaces = sorted(set(_PATRON_CONTENIDO_CETI.findall(texto)))
    if not enlaces:
        return {"estado": "ilegible",
                "detalle": "La página del CETI no muestra ningún enlace de noticias/publicaciones — cambió su estructura."}
    vistos = set(conocido.get("enlaces_vistos", []))
    nuevos = [e for e in enlaces if e not in vistos]
    actual = {"enlaces_vistos": sorted(set(enlaces) | vistos)}
    if nuevos:
        return {"estado": "novedad", "actual": actual,
                "detalle": "Contenidos nuevos en la página del CETI: "
                           + "; ".join("https://www.gub.uy" + e for e in nuevos)}
    return {"estado": "sin_novedad", "actual": actual,
            "detalle": f"Sin contenidos nuevos en la página del CETI ({len(enlaces)} enlaces conocidos)."}


_PATRON_NOTICE_UNICEF = re.compile(r"notice_display&(?:amp;)?id=(\d+)")


def analizar_biblioteca_unicef(texto: str, conocido: dict) -> dict:
    """Biblioteca digital de UNICEF Uruguay (catálogo PMB): ¿hay registros
    nuevos en las páginas de tema?"""
    ids = sorted({int(i) for i in _PATRON_NOTICE_UNICEF.findall(texto)})
    if not ids:
        return {"estado": "ilegible",
                "detalle": "Las páginas de tema de la biblioteca UNICEF no muestran ningún registro — cambió su estructura."}
    vistos = set(conocido.get("registros_vistos", []))
    nuevos = [i for i in ids if i not in vistos]
    actual = {"registros_vistos": sorted(set(ids) | vistos)}
    if nuevos:
        return {"estado": "novedad", "actual": actual,
                "detalle": (f"{len(nuevos)} registro(s) nuevo(s) en la biblioteca UNICEF — revisar en "
                            "https://bibliotecaunicef.uy/opac_css/ los id "
                            + ", ".join(str(i) for i in nuevos[:10]))}
    return {"estado": "sin_novedad", "actual": actual,
            "detalle": f"Sin registros nuevos en la biblioteca UNICEF ({len(ids)} registros conocidos a la vista)."}


_URL_UNICEF_TEMAS = "https://bibliotecaunicef.uy/opac_css/index.php?lvl=cmspage&pageid=6&id_rubrique=82"
_URL_UNICEF_TEMA = "https://bibliotecaunicef.uy/opac_css/index.php?lvl=cmspage&pageid=4&id_article={id}"


def obtener_biblioteca_unicef() -> str:
    """Descarga en dos etapas: la portada de TEMAS enumera las páginas de
    tema (id_article) y cada una lista sus registros. Si la portada dejara
    de enumerar temas, se devuelve tal cual y el análisis lo reporta como
    ILEGIBLE (cero registros) en vez de quedar verde sin mirar nada."""
    portada = descargar(_URL_UNICEF_TEMAS)
    ids_articulo = sorted({int(i) for i in re.findall(r"id_article=(\d+)", portada)})
    if not ids_articulo:
        return portada
    return "\n".join(descargar(_URL_UNICEF_TEMA.format(id=i)) for i in ids_articulo)


FUENTES = [
    {
        "clave": "ensanna_microdatos",
        "nombre": "Microdatos ENSANNA 2024 (catálogo ANDA del INE)",
        "url": "https://www4.ine.gub.uy/Anda5/index.php/catalog/export/csv?ps=10000",
        "analizar": analizar_anda,
    },
    {
        "clave": "retrospectivas_ine",
        "nombre": "Estimaciones retrospectivas INE rev. 2025",
        "url": "https://www.gub.uy/instituto-nacional-estadistica/proyeccionesrev2025",
        "analizar": analizar_retrospectivas,
    },
    {
        "clave": "esnna_conapees",
        "nombre": "Serie ESNNA oficial (noticias CONAPEES en INAU)",
        "url": "https://www.inau.gub.uy/sala-de-prensa/noticias",
        "analizar": analizar_noticias_inau,
    },
    {
        "clave": "plan_ceti",
        "nombre": "Plan CETI posterior a la ENSANNA (MTSS)",
        "url": "https://www.gub.uy/ministerio-trabajo-seguridad-social/ceti",
        "analizar": analizar_ceti,
    },
    {
        "clave": "biblioteca_unicef",
        "nombre": "Publicaciones de UNICEF Uruguay (biblioteca digital)",
        "url": _URL_UNICEF_TEMAS,
        "obtener": obtener_biblioteca_unicef,
        "analizar": analizar_biblioteca_unicef,
    },
]


def leer_baseline() -> dict:
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def revisar_fuentes() -> list[dict]:
    baseline = leer_baseline()
    resultados = []
    for fuente in FUENTES:
        conocido = baseline.get(fuente["clave"], {})
        try:
            texto = fuente.get("obtener", lambda u=fuente["url"]: descargar(u))()
        except Exception as e:
            resultado = {"estado": "no_accesible", "detalle": f"No se pudo descargar {fuente['url']}: {e}"}
        else:
            resultado = fuente["analizar"](texto, conocido)
        resultados.append({"clave": fuente["clave"], "nombre": fuente["nombre"], **resultado})
    return resultados


def codigo_de_salida(resultados: list[dict]) -> int:
    estados = {r["estado"] for r in resultados}
    if "novedad" in estados:
        return 2
    if estados & {"no_accesible", "ilegible"}:
        return 1
    return 0


_ETIQUETAS = {
    "sin_novedad": "SIN NOVEDAD",
    "novedad": "NOVEDAD",
    "no_accesible": "NO ACCESIBLE",
    "ilegible": "ILEGIBLE",
}


def main() -> None:
    actualizar = "--actualizar-baseline" in sys.argv[1:]
    resultados = revisar_fuentes()
    for r in resultados:
        print(f"[{_ETIQUETAS[r['estado']]}] {r['nombre']}")
        print(f"    {r['detalle']}")
    bitacora.registrar(
        "vigilancia_fuentes",
        resumen={r["clave"]: r["estado"] for r in resultados},
    )
    if actualizar:
        completos = [r for r in resultados if "actual" in r]
        if len(completos) < len(FUENTES):
            print("\nBaseline SIN actualizar: hay fuentes no accesibles o "
                  "ilegibles y pisar su estado conocido borraría la referencia.")
            sys.exit(1)
        baseline = leer_baseline()
        for r in completos:
            baseline[r["clave"]] = r["actual"]
        BASELINE.write_text(
            json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(f"\nBaseline actualizado: {BASELINE}")
    sys.exit(codigo_de_salida(resultados))


if __name__ == "__main__":
    main()
