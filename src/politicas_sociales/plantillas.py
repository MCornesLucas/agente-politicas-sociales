"""Plantillas HTML de los formularios — solo texto, sin servidor.

Heredadas del proyecto hermano (mismo estilo y las mismas decisiones de
usabilidad: botón de salida en cada paso, pantalla de espera tras cada
envío). El servidor y los `mostrar_*` viven en `formularios.py`, que
reexporta estas funciones.
"""

from __future__ import annotations

_ESTILO = """
:root { --rojo: #d1495b; --verde: #66a182; --texto: #24292f; --gris: #57606a; }
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  background: linear-gradient(135deg, #f6f8fa 0%, #eef1f4 100%);
  margin: 0; min-height: 100vh; display: flex; align-items: center;
  justify-content: center; padding: 24px; color: var(--texto);
}
.tarjeta {
  background: white; border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08);
  max-width: 640px; width: 100%; padding: 40px;
}
h1 { font-size: 22px; margin: 0 0 8px; }
.subtitulo { color: var(--gris); font-size: 14px; margin-bottom: 20px; }
.emoji { font-size: 40px; margin-bottom: 8px; }
.valor {
  background: #f0fdf4; border-left: 3px solid var(--verde);
  padding: 12px 16px; border-radius: 6px; margin: 20px 0;
  font-size: 14px;
}
.advertencia {
  background: #f6f8fa; border-left: 3px solid var(--gris);
  padding: 12px 16px; border-radius: 6px; margin: 20px 0;
  font-size: 13px; color: var(--gris); line-height: 1.55;
}
button[type=submit] {
  margin-top: 16px; width: 100%; padding: 14px; font-size: 16px;
  font-weight: 600; color: white; background: var(--verde);
  border: none; border-radius: 8px; cursor: pointer;
}
button[type=submit]:hover { background: #559874; }
.listo { text-align: center; padding: 60px 0; }
.listo .check { font-size: 48px; margin-bottom: 12px; }
.spinner {
  width: 40px; height: 40px; margin: 0 auto 16px;
  border: 4px solid #eef1f4; border-top: 4px solid var(--verde);
  border-radius: 50%; animation: girar 0.8s linear infinite;
}
@keyframes girar { to { transform: rotate(360deg); } }
.boton-accion {
  display: block; width: 100%; text-align: center; text-decoration: none;
  margin-top: 16px; padding: 14px; font-size: 16px; font-weight: 600;
  border: none; border-radius: 8px; cursor: pointer; font-family: inherit;
}
.boton-primario { color: white; background: var(--verde); }
.boton-primario:hover { background: #559874; }
.boton-secundario { color: white; background: var(--gris); }
.boton-secundario:hover { background: #46505a; }
.boton-salir {
  display: block; width: 100%; text-align: center; margin-top: 10px;
  padding: 10px; font-size: 13px; font-weight: 600; color: var(--gris);
  background: none; border: none; cursor: pointer; text-decoration: underline;
  font-family: inherit;
}
.boton-salir:hover { color: var(--rojo); }
.opcion {
  display: block; border: 2px solid #d0d7de; border-radius: 10px;
  padding: 14px 16px; margin-bottom: 12px; cursor: pointer; font-size: 14px;
}
.opcion:hover { border-color: var(--verde); }
.opcion input { margin-right: 10px; }
.opcion .detalle { color: var(--gris); }
.categoria { margin-bottom: 26px; }
.categoria h2 {
  font-size: 14px; color: var(--verde); text-transform: uppercase;
  letter-spacing: 0.03em; border-bottom: 2px solid #eef1f4;
  padding-bottom: 6px; margin-bottom: 10px;
}
.barra-acciones { display: flex; gap: 10px; margin-bottom: 12px; }
.barra-acciones button {
  flex: none; width: auto; padding: 8px 16px; font-size: 13px;
  font-weight: 600; border-radius: 6px; cursor: pointer;
  border: 1px solid #d0d7de; background: #f6f8fa; color: var(--texto);
}
.metrica { display: flex; align-items: flex-start; gap: 10px; padding: 7px 0 2px; cursor: pointer; }
.metrica input { margin-top: 4px; width: 18px; height: 18px; flex: none; cursor: pointer; }
.metrica .texto { font-size: 14px; line-height: 1.5; }
.metrica .explicacion { color: var(--gris); }
.metrica-fila { border-bottom: 1px solid #f0f2f4; }
.metrica-fila:last-child { border-bottom: none; }
.otra { background: #f6f8fa; border-radius: 10px; padding: 16px 20px; margin: 20px 0; }
.problema {
  background: #fef2f2; border-left: 3px solid var(--rojo);
  border-radius: 8px; padding: 14px 18px; font-size: 14px;
  line-height: 1.6; margin-bottom: 16px;
}
.original {
  background: #f6f8fa; border-radius: 8px; padding: 14px 18px;
  font-size: 14px; color: var(--gris); margin-bottom: 16px;
}
label { display: block; font-weight: 600; margin-top: 20px; margin-bottom: 8px; }
textarea {
  width: 100%; padding: 12px 14px; font-size: 15px;
  border: 2px solid #d0d7de; border-radius: 8px; font-family: inherit;
}
textarea:focus { outline: none; border-color: var(--verde); }
.error { color: var(--rojo); font-size: 13px; margin-top: 8px; display: none; }
"""

_SCRIPT_LISTO = """
function mostrarListo() {
  document.getElementById('tarjeta').innerHTML = `
    <div class="listo">
      <div class="spinner"></div>
      <h1>Aguardá un momento...</h1>
      <p>Estamos preparando tu informe. Puede tardar unos minutos; cuando
      esté listo, se va a abrir solo el siguiente paso en una pestaña
      nueva.</p>
    </div>`;
}
"""

# Botón presente en los pasos intermedios para que alguien que no quiere
# seguir pueda salir en el momento, en vez de que el agente quede
# esperando hasta 30 minutos a que la pestaña cerrada llegue al timeout.
_BOTON_SALIR = '<button type="button" class="boton-salir" onclick="salirDelFlujo()">Salir sin generar el informe</button>'

_SCRIPT_SALIR = """
function salirDelFlujo() {
  if (!confirm('¿Seguro que querés salir sin generar el informe?')) return;
  fetch('/', {method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({salir_del_flujo: true})}).then(() => {
    document.getElementById('tarjeta').innerHTML = `
      <div class="listo">
        <div class="check">👋</div>
        <h1>Listo, no se generó ningún informe.</h1>
        <p>Ya podés cerrar esta pestaña.</p>
      </div>`;
  });
}
"""


def plantilla_arranque() -> str:
    """Pantalla de arranque de `abrir_agente.bat`, antes de levantar Claude
    Code: elegir entre empezar o salir con dos botones, sin escribir nada.
    La usa `arranque.py`, no el agente — es lo primero que ve el usuario,
    incluso antes de que exista una conversación."""
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Agente de Políticas Sociales de Infancia</title>
<style>{_ESTILO}</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">👋</div>
  <h1>Bienvenido a tu agente de políticas sociales de infancia</h1>
  <p class="subtitulo">Elegí una opción para continuar.</p>
  <button type="button" class="boton-accion boton-primario" onclick="elegir('empezar')">Empezar</button>
  <button type="button" class="boton-accion boton-secundario" onclick="elegir('salir')">Salir del agente</button>
</div>
<script>
async function elegir(accion) {{
  document.getElementById('tarjeta').innerHTML = `
    <div class="listo">
      <div class="spinner"></div>
      <h1>${{accion === 'empezar' ? 'Iniciando…' : 'Cerrando…'}}</h1>
      <p>${{accion === 'empezar' ? 'Ya te vamos a abrir el primer formulario en una pestaña nueva.' : 'Si esta pestaña no se cierra sola, cerrala vos.'}}</p>
    </div>`;
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{accion: accion}})}});
  if (accion === 'salir') {{
    // Los navegadores solo dejan cerrar por script una pestaña que el
    // propio script abrió; esta "reapertura" es el truco habitual para
    // que igual lo permitan cuando la pestaña la abrió `cmd /c start`.
    window.open('', '_self');
    window.close();
  }}
}}
</script></body></html>"""


def plantilla_bienvenida() -> str:
    """Paso 1 del flujo del agente: qué se va a generar y confirmación."""
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Políticas sociales de infancia — Informe</title>
<style>{_ESTILO}</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">📊</div>
  <h1>Informe de políticas sociales de infancia en Uruguay</h1>
  <p>Soy el agente que convierte los datos oficiales del sistema de
  protección (SIPIAV, INAU, CONAPEES, ENSANNA y la ECH) en un informe
  claro y riguroso.</p>
  <div class="valor">
    El informe incluye las métricas confirmadas del catálogo en cinco
    temas — violencia, explotación sexual, trabajo infantil, protección
    especial y pobreza —, las proyecciones validadas y los cruces entre
    fuentes, cada cifra con su fuente citada.
  </div>
  <div class="advertencia">
    La mayoría de las fuentes son registros administrativos: miden la
    respuesta de los sistemas, no cuántos niños atraviesan cada
    problema. El informe explica esa diferencia en lenguaje simple.
  </div>
  <form id="form">
    <button type="submit">Generar el informe →</button>
  </form>
  {_BOTON_SALIR}
</div>
<script>
{_SCRIPT_LISTO}
{_SCRIPT_SALIR}
document.getElementById('form').addEventListener('submit', async (e) => {{
  e.preventDefault();
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{accion: 'generar'}})}});
  mostrarListo();
}});
</script></body></html>"""


def plantilla_catalogo(bloques: list[dict]) -> str:
    """Paso de selección de bloques: qué temas (y si los cruces) incluye
    esta edición. `bloques` viene de
    `construir_informe.bloques_disponibles()` — los conteos se calculan
    desde las celdas reales, así el formulario nunca promete contenido
    desalineado del informe.

    Ningún bloque viene preseleccionado (decisión del dueño del
    proyecto): elegir es del usuario, no un valor por defecto. El envío
    exige al menos un tema (una edición solo de cruces no es un informe).
    """
    filas = []
    for b in bloques:
        contenido = []
        if b["metricas"]:
            contenido.append(f"{b['metricas']} métricas")
        if b["proyecciones"]:
            contenido.append(f"{b['proyecciones']} proyecciones")
        if b["cruces"]:
            contenido.append(f"{b['cruces']} cruces")
        detalle = " · ".join(contenido)
        filas.append(
            f'<label class="opcion"><input type="checkbox" name="bloque" '
            f'value="{b["clave"]}"> <strong>{b["titulo"]}</strong>'
            f'<span class="detalle"> — {detalle}</span></label>'
        )
    filas_html = "\n".join(filas)
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Contenido del informe</title>
<style>{_ESTILO}</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">🗂️</div>
  <h1>¿Qué temas incluye tu informe?</h1>
  <p class="subtitulo">Marcá los bloques que te interesan. En el paso
  siguiente vas a poder elegir las métricas de cada bloque, una por una.
  El resumen analítico y las conclusiones solo se incluyen en el informe
  completo, porque recorren los cinco temas.</p>
  <form id="form">
    {filas_html}
    <p class="error" id="error">Elegí al menos un tema (los cruces solos no
    alcanzan para armar un informe).</p>
    <button type="submit">Continuar →</button>
  </form>
  {_BOTON_SALIR}
</div>
<script>
{_SCRIPT_LISTO}
{_SCRIPT_SALIR}
document.getElementById('form').addEventListener('submit', async (e) => {{
  e.preventDefault();
  const marcados = Array.from(document.querySelectorAll('input[name=bloque]:checked'))
    .map((c) => c.value);
  if (!marcados.some((v) => v.startsWith('tema_'))) {{
    document.getElementById('error').style.display = 'block';
    return;
  }}
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{bloques: marcados}})}});
  mostrarListo();
}});
</script></body></html>"""


def plantilla_metricas(estructura: list[dict]) -> str:
    """Paso de selección fina: las métricas de los bloques elegidos, cada
    una con su explicación real (la pregunta que responde, extraída de
    las propias celdas del informe por
    `construir_informe.unidades_disponibles(bloques)`). Vienen todas
    marcadas — son lo que el informe imprimirá salvo que el usuario
    destilde — con botones de marcar todas/ninguna por bloque (estilo
    heredado del proyecto hermano).

    Si una unidad declara dependencias (`requiere`), el envío las
    autocompleta y lo avisa: elegir una métrica sin lo que necesita no es
    posible.

    Incluye el campo libre "otra métrica": el usuario puede pedir una
    métrica que no está en el catálogo, y el agente analiza con los datos
    del repositorio si puede calcularse con el rigor del proyecto.
    """
    secciones = []
    for bloque in estructura:
        filas = []
        for u in bloque["unidades"]:
            requiere = ",".join(u.get("requiere", []))
            explicacion = f' <span class="explicacion">— {u["explicacion"]}</span>' if u["explicacion"] else ""
            filas.append(
                f'<div class="metrica-fila"><label class="metrica">'
                f'<input type="checkbox" name="unidad" value="{u["clave"]}" '
                f'data-requiere="{requiere}" checked>'
                f'<span class="texto"><strong>{u["titulo"]}</strong>{explicacion}</span>'
                f"</label></div>"
            )
        secciones.append(
            f'<div class="categoria" data-bloque="{bloque["clave"]}">'
            f'<h2>{bloque["titulo"]}</h2>'
            f'<div class="barra-acciones">'
            f'<button type="button" onclick="marcarBloque(\'{bloque["clave"]}\', true)">Marcar todas</button>'
            f'<button type="button" onclick="marcarBloque(\'{bloque["clave"]}\', false)">Ninguna</button>'
            f"</div>{''.join(filas)}</div>"
        )
    secciones_html = "\n".join(secciones)
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Métricas del informe</title>
<style>{_ESTILO}
.tarjeta {{ max-width: 760px; }}
</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">📋</div>
  <h1>Elegí las métricas de tu informe</h1>
  <p class="subtitulo">Estas son las métricas de los bloques que
  elegiste, todas marcadas: destildá las que no necesites. Cada una se
  imprime con su gráfica, su justificación, su lectura y su fuente.</p>
  <form id="form">
    {secciones_html}
    <div class="otra">
      <label for="otra_metrica">¿Querés agregar una métrica que no está en el catálogo?</label>
      <p class="subtitulo" style="margin-bottom:8px;">Describila con tus
      palabras (qué querés saber, de qué fuente, para qué años). El agente
      va a analizar si puede calcularse con los datos ya verificados del
      proyecto y con sus reglas de rigor; si no puede, te va a explicar
      por qué y ofrecer una opción.</p>
      <textarea id="otra_metrica" name="otra_metrica" rows="3"
        placeholder="Ej.: cómo evolucionó la proporción de situaciones con violencia reiterada respecto del total, 2019-2025"></textarea>
    </div>
    <p class="error" id="error">Elegí al menos una métrica o proyección de
    un tema (los cruces solos no alcanzan para armar un informe).</p>
    <p class="error" id="aviso-requiere"></p>
    <button type="submit">Generar el informe →</button>
  </form>
  {_BOTON_SALIR}
</div>
<script>
{_SCRIPT_LISTO}
{_SCRIPT_SALIR}
function marcarBloque(bloque, estado) {{
  document.querySelectorAll('[data-bloque=' + bloque + '] input[name=unidad]')
    .forEach((c) => {{ c.checked = estado; }});
}}
document.getElementById('form').addEventListener('submit', async (e) => {{
  e.preventDefault();
  const casillas = Array.from(document.querySelectorAll('input[name=unidad]'));
  const marcadas = new Set(casillas.filter((c) => c.checked).map((c) => c.value));
  // Autocompletar dependencias declaradas: una unidad nunca viaja sin lo
  // que necesita (la clausura completa la termina el servidor igual).
  const agregadas = [];
  let cambio = true;
  while (cambio) {{
    cambio = false;
    for (const c of casillas) {{
      if (!marcadas.has(c.value)) continue;
      for (const req of (c.dataset.requiere || '').split(',').filter(Boolean)) {{
        if (!marcadas.has(req)) {{ marcadas.add(req); agregadas.push(req); cambio = true; }}
      }}
    }}
  }}
  if (agregadas.length > 0) {{
    casillas.forEach((c) => {{ if (marcadas.has(c.value)) c.checked = true; }});
    const aviso = document.getElementById('aviso-requiere');
    aviso.textContent = 'Se agregaron métricas que las elegidas necesitan: ' + agregadas.join(', ');
    aviso.style.display = 'block';
  }}
  const esDeTema = (v) => v.startsWith('metrica_') || v.startsWith('proyeccion_');
  if (![...marcadas].some(esDeTema)) {{
    document.getElementById('error').style.display = 'block';
    return;
  }}
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{unidades: [...marcadas],
      otra_metrica: document.getElementById('otra_metrica').value.trim()}})}});
  mostrarListo();
}});
</script></body></html>"""


def plantilla_revision(metrica_pedida: str, problema: str,
                       alternativa: str = "") -> str:
    """Revisión de una métrica pedida que no puede calcularse: explica el
    porqué con los datos y reglas del proyecto y ofrece una opción
    (estilo heredado del proyecto hermano). El usuario decide: usar la
    alternativa propuesta (si existe) o continuar solo con las métricas
    del catálogo que eligió.
    """
    boton_alternativa = (
        '<button type="submit" name="decision" value="alternativa" '
        'class="boton-accion boton-primario">Usar la alternativa propuesta</button>'
        if alternativa else ""
    )
    bloque_alternativa = (
        f'<div class="valor"><strong>Alternativa posible:</strong> {alternativa}</div>'
        if alternativa else ""
    )
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Sobre la métrica que pediste</title>
<style>{_ESTILO}</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">🔍</div>
  <h1>La métrica que pediste no puede calcularse así</h1>
  <div class="original"><strong>Pediste:</strong> {metrica_pedida}</div>
  <div class="problema">{problema}</div>
  {bloque_alternativa}
  <form id="form" style="display:flex; flex-direction:column; gap:10px;">
    {boton_alternativa}
    <button type="submit" name="decision" value="descartar"
      class="boton-accion boton-secundario">Continuar sin la métrica nueva</button>
  </form>
  {_BOTON_SALIR}
</div>
<script>
{_SCRIPT_LISTO}
{_SCRIPT_SALIR}
document.getElementById('form').addEventListener('submit', async (e) => {{
  e.preventDefault();
  const decision = e.submitter ? e.submitter.value : 'descartar';
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{decision: decision}})}});
  mostrarListo();
}});
</script></body></html>"""


def plantilla_finalizacion(pdf_disponible: bool, html_disponible: bool) -> str:
    """Último paso: agradecimiento + botones que abren el/los informe(s)."""
    botones = []
    if pdf_disponible:
        botones.append(
            '<a class="boton-accion boton-primario" href="/informe.pdf" target="_blank">'
            "📄 Abrir el informe en PDF</a>"
        )
    if html_disponible:
        botones.append(
            '<a class="boton-accion boton-primario" href="/informe.html" target="_blank">'
            "🌐 Abrir el informe en el navegador</a>"
        )
    botones_html = "\n".join(botones)
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>Informe listo</title>
<style>{_ESTILO}</style></head><body>
<div class="tarjeta" id="tarjeta">
  <div class="emoji">✅</div>
  <h1>Tu informe fue creado con éxito</h1>
  <p class="subtitulo">Gracias por usar el agente de políticas sociales de
  infancia. Podés abrir tu informe con los botones de abajo, las veces
  que quieras.</p>
  {botones_html}
  <form id="form" style="margin-top:24px; display:flex; flex-direction:column; gap:10px;">
    <button type="submit" name="accion" value="nuevo_informe" class="boton-accion boton-secundario">🔄 Crear un nuevo informe</button>
    <button type="submit" name="accion" value="terminar" class="boton-accion boton-primario">Listo, gracias →</button>
  </form>
</div>
<script>
document.getElementById('form').addEventListener('submit', async (e) => {{
  e.preventDefault();
  const accion = e.submitter ? e.submitter.value : 'terminar';
  await fetch('/', {{method: 'POST', headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{accion: accion}})}});
  const esNuevo = accion === 'nuevo_informe';
  document.getElementById('tarjeta').innerHTML = `
    <div class="listo">
      <div class="check">${{esNuevo ? '🔄' : '🙏'}}</div>
      <h1>${{esNuevo ? 'Preparando un nuevo informe…' : '¡Gracias!'}}</h1>
      <p>${{esNuevo
        ? 'Ya te vamos a abrir el primer formulario en una pestaña nueva.'
        : 'Ya podés cerrar esta pestaña.'}}</p>
    </div>`;
}});
</script></body></html>"""
