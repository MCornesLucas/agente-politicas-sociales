"""Formularios locales en el navegador: la forma en que el agente le
"pregunta" cosas al usuario, en vez de hacerlo por chat.

Todo corre en la propia computadora del usuario — no hay ninguna cuenta
de por medio, no sale a internet, no depende de servicios de terceros.
`mostrar_formulario()` levanta un servidor mínimo en localhost, abre el
navegador con el HTML del paso que corresponda, y bloquea hasta que el
usuario lo completa — devuelve la respuesta como un diccionario.

Motor con decisiones de seguridad aprendidas en
corridas reales (validación de Origin, tope de tamaño del
cuerpo, POST malformado que no mata el hilo). El HTML de cada paso vive
en `plantillas.py` y se reexporta desde acá: `formularios.plantilla_*`
es la cara pública.
"""

from __future__ import annotations

import http.server
import json
import re
import subprocess
import threading
import traceback
from pathlib import Path

from . import bitacora, cierre
from .plantillas import (  # noqa: F401 — reexports: la cara pública es formularios.plantilla_*
    plantilla_arranque,
    plantilla_bienvenida,
    plantilla_catalogo,
    plantilla_datos,
    plantilla_datos_ech,
    plantilla_datos_otras,
    plantilla_datos_otras_confirmacion,
    plantilla_finalizacion,
    plantilla_metricas,
    plantilla_revision,
)


def _origen_es_propio(handler) -> bool:
    """¿La respuesta que llega viene de la página que sirve este mismo
    servidor, o de otro sitio?

    El servidor escucha en 127.0.0.1 con un puerto al azar, pero eso solo
    no alcanza: cualquier página web abierta en el navegador puede probar
    puertos de localhost y responder al formulario en nombre de la
    persona. El navegador manda `Origin` en todo POST, así que alcanza
    con exigir que sea el nuestro. Si no viene `Origin` (un cliente que
    no es un navegador, ej. los tests), se acepta: el riesgo que se
    cierra es específicamente el de una página de otro sitio.
    """
    origen = handler.headers.get("Origin")
    if origen is None:
        return True
    puerto = handler.server.server_address[1]
    return origen in (f"http://127.0.0.1:{puerto}", f"http://localhost:{puerto}")


def _rechazar_origen_ajeno(handler) -> bool:
    """Corta la respuesta con 403 si vino de otro sitio. Devuelve True si
    ya se respondió y quien llama tiene que abandonar el pedido."""
    if _origen_es_propio(handler):
        return False
    bitacora.registrar("formulario_origen_rechazado", origen=handler.headers.get("Origin"))
    handler.send_response(403)
    handler.send_header("Content-Length", "0")
    handler.end_headers()
    return True


# Las respuestas de estos formularios son unos pocos cientos de bytes. Un
# tope generoso evita que un `Content-Length` enorme —malformado o
# malicioso— haga que el proceso intente reservar esa memoria de una.
_MAXIMO_CUERPO_EN_BYTES = 1_000_000


def _leer_cuerpo(handler) -> bytes | None:
    """Lee el cuerpo del POST validando su tamaño. Devuelve None (y ya
    respondió) si el pedido no sirve."""
    crudo = handler.headers.get("Content-Length", "0")
    try:
        largo = int(crudo)
    except (TypeError, ValueError):
        largo = -1
    if largo < 0 or largo > _MAXIMO_CUERPO_EN_BYTES:
        handler.send_response(400)
        handler.send_header("Content-Length", "0")
        handler.end_headers()
        return None
    return handler.rfile.read(largo)


def _decodificar_respuesta(handler, cuerpo: bytes) -> dict | None:
    """Convierte el cuerpo del POST en el dict que espera el formulario.
    Devuelve None (y ya respondió 400) si no sirve. Sin esto, un cuerpo
    que no fuera JSON —o que fuera JSON pero no un objeto— tiraba una
    excepción sin manejar dentro del hilo del servidor y la bitácora
    quedaba ciega justo en el caso raro."""
    try:
        datos = json.loads(cuerpo)
    except (json.JSONDecodeError, UnicodeDecodeError):
        datos = None
    if not isinstance(datos, dict):
        bitacora.registrar("formulario_post_invalido", largo_cuerpo=len(cuerpo))
        handler.send_response(400)
        handler.send_header("Content-Length", "0")
        handler.end_headers()
        return None
    return datos


def _nombre_desde_html(html: str) -> str:
    """Extrae el texto del primer <h1> del HTML para identificar el
    formulario en la bitácora."""
    coincidencia = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if not coincidencia:
        return "formulario"
    texto = re.sub(r"<[^>]+>", "", coincidencia.group(1)).strip()
    return texto[:60] if texto else "formulario"


def _servir_html(handler, html_bytes: bytes) -> None:
    handler.send_response(200)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(html_bytes)))
    handler.end_headers()
    handler.wfile.write(html_bytes)


def _responder_post(handler, resultado: dict, evento: threading.Event) -> None:
    """El do_POST completo de cualquiera de los dos servidores: validación
    de origen, de tamaño y de formato — recién si todo eso pasa, la
    respuesta se guarda en `resultado` y se despierta a quien espera."""
    if _rechazar_origen_ajeno(handler):
        return
    cuerpo = _leer_cuerpo(handler)
    if cuerpo is None:
        return
    datos = _decodificar_respuesta(handler, cuerpo)
    if datos is None:
        return
    resultado.update(datos)
    respuesta = b'{"ok": true}'
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(respuesta)))
    handler.end_headers()
    handler.wfile.write(respuesta)
    evento.set()


def _servir_y_esperar(handler_cls, evento: threading.Event, timeout: float | None, evento_error: str, **detalle_error) -> bool:
    """Levanta el servidor en un puerto al azar de 127.0.0.1, abre el
    navegador, y bloquea hasta que llegue la respuesta o venza el timeout.
    Devuelve si hubo respuesta; si el servidor en sí falla, lo registra
    como `evento_error` y relanza."""
    try:
        # ThreadingHTTPServer: el navegador puede abrir más de una conexión
        # a la vez; un servidor de una sola conexión se traba en ese caso
        # (visto en la práctica).
        with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler_cls) as httpd:
            puerto = httpd.server_address[1]
            hilo = threading.Thread(target=httpd.serve_forever, daemon=True)
            hilo.start()
            url = f"http://127.0.0.1:{puerto}/"
            # os.startfile()/webbrowser.open() resultaron poco confiables en
            # algunos entornos; "cmd /c start" es lo más robusto en Windows.
            subprocess.run(["cmd", "/c", "start", "", url], check=False)
            completado = evento.wait(timeout=timeout)
            httpd.shutdown()
    except Exception as e:
        bitacora.registrar(evento_error, mensaje=str(e), traceback=traceback.format_exc(), **detalle_error)
        raise
    return completado


def mostrar_formulario(html: str, timeout: float | None = 1800) -> dict:
    """Sirve `html` en localhost, abre el navegador, y bloquea hasta que el
    usuario lo completa. Devuelve lo que haya mandado el formulario."""
    nombre = _nombre_desde_html(html)
    resultado: dict = {}
    evento = threading.Event()
    html_bytes = html.encode("utf-8")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/favicon"):
                self.send_response(204)
                self.end_headers()
                return
            _servir_html(self, html_bytes)

        def do_POST(self):
            _responder_post(self, resultado, evento)

        def log_message(self, format, *args):
            pass

    bitacora.registrar("formulario_mostrado", nombre=nombre)
    completado = _servir_y_esperar(Handler, evento, timeout, "formulario_error", nombre=nombre)

    # Se guarda también lo que la persona respondió de verdad (no solo que
    # respondió): un desajuste entre lo que alguien cree haber marcado y lo
    # que termina en el informe es indiagnosticable si la bitácora solo
    # dice "se respondió".
    if completado:
        bitacora.registrar("formulario_respondido", nombre=nombre, respuesta=resultado)
    else:
        bitacora.registrar("formulario_timeout", nombre=nombre)

    if not completado:
        # Devolver {} era un riesgo real: el chequeo estándar que sigue es
        # `respuesta.get("salir_del_flujo")`, que con un dict vacío no
        # dispara la salida prolija y el siguiente acceso a un campo
        # esperado tiraba un KeyError crudo. Devolver salir_del_flujo=True
        # hace que el mismo chequeo cubra también el timeout.
        cierre.cerrar_consola(motivo="timeout_formulario")
        return {"salir_del_flujo": True, "motivo": "timeout"}

    # Salir sin generar el informe: acá se termina la conversación, así que
    # también se cierra la consola. Se hace acá y no en las instrucciones
    # del agente a propósito (mismo criterio que los hooks): una regla que
    # depende de que el modelo se acuerde no se cumple siempre.
    if resultado.get("salir_del_flujo"):
        cierre.cerrar_consola(motivo="salir_del_flujo")

    return resultado


def mostrar_finalizacion(pdf_path: str = "", html_path: str = "", timeout: float | None = 1800) -> dict:
    """Último paso: pantalla de agradecimiento con links que abren el PDF
    y/o el HTML del informe, servidos por este mismo servidor local (más
    confiable que `start` desde la terminal). Bloquea hasta que el usuario
    elige una opción. El resultado trae `{"accion": "terminar"}` o
    `{"accion": "nuevo_informe"}` — este último significa que el agente
    reinicia el flujo desde el paso 1, no que termina la conversación."""
    resultado: dict = {}
    evento = threading.Event()
    html = plantilla_finalizacion(pdf_disponible=bool(pdf_path), html_disponible=bool(html_path))
    html_bytes = html.encode("utf-8")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/favicon"):
                self.send_response(204)
                self.end_headers()
                return
            if self.path == "/informe.pdf" and pdf_path:
                self._servir_archivo(pdf_path, "application/pdf")
                return
            if self.path == "/informe.html" and html_path:
                self._servir_archivo(html_path, "text/html; charset=utf-8")
                return
            _servir_html(self, html_bytes)

        def _servir_archivo(self, ruta: str, content_type: str):
            # El archivo puede haber desaparecido entre que se generó y el
            # click (movido a mano, borrado por un antivirus). Sin esto, la
            # excepción moría en el hilo del servidor y el click no hacía
            # nada, sin registro de por qué.
            try:
                datos = Path(ruta).read_bytes()
            except OSError as e:
                bitacora.registrar("finalizacion_archivo_ilegible", ruta=ruta, mensaje=str(e))
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(datos)))
            self.send_header("Content-Disposition", f'inline; filename="{Path(ruta).name}"')
            self.end_headers()
            self.wfile.write(datos)

        def do_POST(self):
            _responder_post(self, resultado, evento)

        def log_message(self, format, *args):
            pass

    bitacora.registrar("finalizacion_mostrada", pdf_disponible=bool(pdf_path), html_disponible=bool(html_path))
    completado = _servir_y_esperar(Handler, evento, timeout, "finalizacion_error")

    if completado:
        bitacora.registrar("finalizacion_respondida", respuesta=resultado)
    else:
        bitacora.registrar("finalizacion_timeout")

    if not completado:
        # Acá no existe "salir_del_flujo" (esta pantalla ya es el final):
        # el equivalente seguro es tratarlo como "terminar".
        cierre.cerrar_consola(motivo="timeout_finalizacion")
        return {"accion": "terminar", "motivo": "timeout"}

    # "terminar" es el final real del flujo. "nuevo_informe" NO cierra
    # nada: el agente reinicia desde el paso 1 en la misma conversación.
    if resultado.get("accion") == "terminar":
        cierre.cerrar_consola(motivo="terminar")

    return resultado
