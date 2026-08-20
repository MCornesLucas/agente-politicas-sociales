// Hook PreToolUse: cada metrica y cada cruce del informe lleva sus cinco
// partes — pregunta, grafica, justificacion ("Por que esta grafica"),
// lectura y fuente citada en la figura — antes de CUALQUIER ejecucion de
// `jupyter nbconvert --execute` sobre el notebook real.
//
// Es la regla estructural de docs/METODOLOGIA.md (seccion 1) y
// docs/CONVENCIONES_DE_GRAFICAS.md — una regla asi no se cumple en el
// 100% de las celdas de un informe real hasta que un
// hook la verifica contra el notebook generado. Calibrado contra el
// informe real de este proyecto (2026-08-19): 40 grupos (36 metricas + 4
// cruces), los cinco componentes presentes en todos — un cambio en las
// celdas que rompa cualquiera de ellos bloquea aca.
//
// Solo revisa grupos con encabezado "### Metrica N." o "### Cruce N.";
// las secciones fijas (introduccion, temas, proyecciones, contexto,
// resumen, conclusiones) tienen estructura propia y no se numeran asi.
const path = require("path");
const { resolverNotebookEjecutado, fuenteDe } = require("./_lib_notebook_ejecutado.cjs");
const { denegar } = require("./_lib_bitacora.cjs");

const ENCABEZADO_GRUPO = /^#{2,4}\s*(M[ée]trica|Cruce)\s+(\w+)[.\s]/;
// La seccion "## Metrica del usuario" (la metrica creada a pedido en el
// flujo guiado) se vigila como un grupo mas: sus celdas tambien deben
// traer las cinco partes. Sin esto, la metrica creada entraria al
// informe sin control (el encabezado de su unidad es solo el titulo,
// sin rotulo, por regla del dueño 2026-08-20).
const ENCABEZADO_MEDIDA = /^##\s+M[ée]trica del usuario/;
const ENCABEZADO_SECCION = /^##\s+(?!\d)/;
const TIENE_GRAFICA = /plt\.|\.plot\(|\.barh?\(|\.scatter\(/;

let raw = "";
process.stdin.on("data", (chunk) => (raw += chunk));
process.stdin.on("end", () => {
  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.exit(0);
  }

  if (input.tool_name !== "Bash") process.exit(0);
  const resultado = resolverNotebookEjecutado((input.tool_input || {}).command);
  if (!resultado) process.exit(0);
  const { ruta: rutaNotebook, nb } = resultado;

  const grupos = [];
  let actual = null;
  for (const cell of nb.cells || []) {
    if (cell.cell_type === "markdown") {
      const texto = fuenteDe(cell);
      const primera = texto.split("\n").find((l) => l.trim().length > 0) || "";
      // La medida se chequea ANTES que el patron generico: su encabezado
      // "## Metrica del usuario" tambien coincide con "Metrica \w+" y el
      // generico la rotularia "Metrica del".
      if (ENCABEZADO_MEDIDA.test(primera)) {
        if (actual) grupos.push(actual);
        actual = { id: "Métrica del usuario", md: [texto], codigo: [] };
        continue;
      }
      const m = primera.match(ENCABEZADO_GRUPO);
      if (m) {
        if (actual) grupos.push(actual);
        actual = { id: `${m[1]} ${m[2]}`, md: [texto], codigo: [] };
        continue;
      }
      if (ENCABEZADO_SECCION.test(primera)) {
        if (actual) grupos.push(actual);
        actual = null;
        continue;
      }
      if (actual) actual.md.push(texto);
      continue;
    }
    if (cell.cell_type === "code" && actual) {
      actual.codigo.push(fuenteDe(cell));
    }
  }
  if (actual) grupos.push(actual);

  // Un notebook sin ningun grupo reconocible es senal de que el patron de
  // encabezados cambio: mejor bloquear que quedar verde por no mirar nada
  // (fallo real documentado en un hook anterior del mismo estilo).
  if (grupos.length === 0) {
    process.stdout.write(
      denegar(
        "informe-metrica-incompleta",
        `El notebook "${rutaNotebook}" no contiene ningún encabezado "### Métrica N." ni ` +
          `"### Cruce N.": o no es el informe (y este hook no debería estar mirándolo), o el ` +
          `formato de encabezados cambió y este guardián quedó ciego. Verificar el patrón en ` +
          `.claude/hooks/gate-informe-metrica-incompleta.cjs antes de continuar.`,
        { notebook: path.basename(rutaNotebook), grupos: 0 }
      )
    );
    process.exit(0);
  }

  const violaciones = [];
  for (const g of grupos) {
    const md = g.md.join("\n");
    const codigo = g.codigo.join("\n");
    const problemas = [];
    if (!md.includes("¿Qué pregunta responde?")) problemas.push("sin la pregunta que responde");
    if (!TIENE_GRAFICA.test(codigo)) problemas.push("sin ninguna gráfica");
    if (!md.includes("Por qué esta gráfica")) problemas.push('sin la justificación ("Por qué esta gráfica")');
    if (!md.includes("**Lectura**")) problemas.push("sin lectura");
    if (!codigo.includes("fuente(")) problemas.push("sin fuente() en la figura");
    if (problemas.length > 0) violaciones.push(`${g.id}: ${problemas.join(", ")}`);
  }

  if (violaciones.length === 0) process.exit(0);

  process.stdout.write(
    denegar(
      "informe-metrica-incompleta",
      `El notebook "${rutaNotebook}" tiene ${violaciones.length} sección(es) de métrica o cruce ` +
        `incompletas según docs/METODOLOGIA.md (cinco partes por métrica): ${violaciones.join("; ")}. ` +
        `Corregir las celdas en los módulos informe_celdas_*.py y reconstruir el notebook con ` +
        `construir_informe antes de volver a ejecutarlo.`,
      { notebook: path.basename(rutaNotebook), violaciones: violaciones.length }
    )
  );
  process.exit(0);
});
