// Hook PostToolUse: despues de ejecutar el notebook, ¿alguna celda que
// muestra una grafica (plt.show()) termino sin producir ninguna imagen?
// Eso pasa si la celda se comio una excepcion en silencio o si la figura
// nunca se llego a renderizar — un informe con una grafica "invisible" es
// un fallo real que hasta ahora solo se detectaba a ojo entre ~150
// celdas. Heredado del proyecto hermano (alli el patron era viz.plot_;
// aqui las celdas grafican con matplotlib y cierran con plt.show()).
const path = require("path");
const { resolverNotebookEjecutado, fuenteDe } = require("./_lib_notebook_ejecutado.cjs");
const { registrar } = require("./_lib_bitacora.cjs");

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
  // PostToolUse: el nbconvert --inplace ya termino, asi que se lee el
  // contenido actualizado del notebook.
  const resultado = resolverNotebookEjecutado((input.tool_input || {}).command);
  if (!resultado) process.exit(0);
  const { ruta: rutaNotebook, nb } = resultado;

  const celdasSinImagen = [];
  (nb.cells || []).forEach((cell, i) => {
    if (cell.cell_type !== "code") return;
    if (!/plt\.show\(\)/.test(fuenteDe(cell))) return;
    const tieneImagen = (cell.outputs || []).some(
      (o) => o.output_type !== "error" && o.data && Object.keys(o.data).some((k) => k.startsWith("image/"))
    );
    if (!tieneImagen) celdasSinImagen.push(i);
  });

  if (celdasSinImagen.length === 0) process.exit(0);

  registrar("hook_bloqueo", {
    hook: "informe-graficas-faltantes",
    celdas_sin_imagen: celdasSinImagen.length,
    notebook: path.basename(rutaNotebook),
  });
  process.stdout.write(
    JSON.stringify({
      decision: "block",
      reason:
        `El notebook "${rutaNotebook}" tiene ${celdasSinImagen.length} celda(s) que llaman a ` +
        `plt.show() pero no produjeron ninguna imagen: celdas ${celdasSinImagen.join(", ")}. ` +
        `Esa gráfica quedaría ausente del informe final sin que nadie lo note. Revisar esas ` +
        `celdas (¿una excepción silenciosa? ¿la figura nunca se creó?) antes de continuar.`,
    })
  );
  process.exit(0);
});
