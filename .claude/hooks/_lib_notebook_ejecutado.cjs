// Modulo compartido por los hooks que necesitan saber sobre que notebook
// corre un `jupyter nbconvert --execute` disparado por la herramienta Bash.
//
// Heredado de agente-encuesta-hogares con su bug real documentado: alli
// nbconvert nunca se invocaba suelto, siempre envuelto en un archivo .py
// corrido con run_python.bat, asi que los hooks que buscaban "nbconvert"
// solo en el texto crudo del comando no se disparaban nunca. Por eso, si
// el comando referencia un archivo .py, tambien se lee ese archivo y se
// busca ahi.
const fs = require("fs");
const path = require("path");

function textoRelevante(command) {
  let texto = command;
  const rutasPy = command.match(/[^\s"']+\.py\b/g) || [];
  for (const ruta of rutasPy) {
    try {
      texto += "\n" + fs.readFileSync(ruta, "utf-8");
    } catch {
      // Archivo temporal que ya no existe, o ruta no legible desde aca -
      // no es motivo para tirar el hook abajo, seguir con las demas rutas.
    }
  }
  return texto;
}

// Devuelve { ruta, nb } si el comando (o algun .py que referencia) corre
// `nbconvert --execute` sobre un notebook que existe y se puede parsear
// como JSON; null si no aplica ninguna de esas condiciones.
function resolverNotebookEjecutado(command) {
  if (typeof command !== "string") return null;

  const texto = textoRelevante(command);
  if (!texto.includes("nbconvert") || !texto.includes("--execute")) {
    return null;
  }

  const match = texto.match(/["']?([^"'\s]+\.ipynb)["']?/);
  if (!match) return null;

  let rutaNotebook = match[1];
  if (!path.isAbsolute(rutaNotebook)) {
    rutaNotebook = path.join(process.cwd(), rutaNotebook);
  }
  if (!fs.existsSync(rutaNotebook)) return null;

  try {
    return { ruta: rutaNotebook, nb: JSON.parse(fs.readFileSync(rutaNotebook, "utf-8")) };
  } catch {
    return null;
  }
}

function fuenteDe(cell) {
  return Array.isArray(cell.source) ? cell.source.join("") : cell.source || "";
}

function textoDeOutputs(cell) {
  let texto = "";
  for (const out of cell.outputs || []) {
    if (out.text) texto += Array.isArray(out.text) ? out.text.join("") : out.text;
    const plano = out.data && out.data["text/plain"];
    if (plano) texto += Array.isArray(plano) ? plano.join("") : plano;
  }
  return texto;
}

module.exports = { resolverNotebookEjecutado, fuenteDe, textoDeOutputs };
