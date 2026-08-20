// Hook PreToolUse: ninguna cifra del "Resumen analitico" ni de las
// "Conclusiones" puede estar escrita a mano sin respaldo — toda tiene que
// existir en un output ejecutado del notebook o en un CSV versionado del
// proyecto (datos_curados/ o resultados/).
//
// Calibrado con una adaptacion medida contra el
// informe real de este proyecto (2026-08-19): aqui casi todas las cifras
// viven dentro de las graficas (imagenes) y en los CSV curados, no en
// outputs de texto — solo 135 numeros en outputs contra ~1,4 millones en
// los CSV. Chequear solo outputs bloqueaba un informe correcto, asi que
// el pool de "numeros reales" son ambos, que es ademas la regla textual
// de CLAUDE.md: si un numero no esta en un archivo del repositorio o en
// una fuente citada, no va.
//
// Redondeo aceptado (buena redaccion, no error): una cifra coincide si
// algun numero real, redondeado a los mismos decimales, da igual; y una
// cifra entera terminada en ceros ("~8.000") coincide si algun numero
// real redondeado a esa magnitud da igual (8.017 → 8.000). Se ignoran
// años (1900-2100) y enteros sueltos sin % (referencias, no
// estadisticas). El separador de miles uruguayo ("8.017") se interpreta
// como entero, no como decimal.
const fs = require("fs");
const path = require("path");
const { resolverNotebookEjecutado, fuenteDe, textoDeOutputs } = require("./_lib_notebook_ejecutado.cjs");
const { denegar } = require("./_lib_bitacora.cjs");

// El chequeo arranca en el Resumen analítico o, si la edición no lo
// tiene (las parciales), en las Conclusiones — que desde 2026-08-19 van
// en TODAS las ediciones, filtradas por bloque, y también se escriben a
// mano.
const ENCABEZADO_RESUMEN = /resumen anal[ií]tico|^##\s+Conclusiones/im;
const MILES = /^\d{1,3}(?:\.\d{3})+$/;

function valoresDe(texto) {
  const valores = [];
  const patron = /\d{1,3}(?:\.\d{3})+|\d+(?:[.,]\d+)?/g;
  let m;
  while ((m = patron.exec(texto)) !== null) {
    const crudo = m[0];
    const v = MILES.test(crudo) ? Number(crudo.replace(/\./g, "")) : Number(crudo.replace(",", "."));
    if (Number.isFinite(v)) valores.push(v);
  }
  return valores;
}

function cifrasDe(texto) {
  const encontradas = [];
  // Cifras "de estadistica": con decimales, con % pegado, o enteros con
  // separador de miles (magnitudes del informe).
  const patron = /(\d{1,3}(?:\.\d{3})+|\d+(?:[.,]\d+)?)\s*%|(\d{1,3}(?:\.\d{3})+)|(\d+[.,]\d+)/g;
  let m;
  while ((m = patron.exec(texto)) !== null) {
    const crudo = m[1] !== undefined ? m[1] : m[2] !== undefined ? m[2] : m[3];
    let valor, decimales, magnitud;
    if (MILES.test(crudo)) {
      valor = Number(crudo.replace(/\./g, ""));
      decimales = 0;
      const ceros = (String(valor).match(/0+$/) || [""])[0].length;
      magnitud = ceros > 0 ? 10 ** ceros : 1;
    } else {
      const normal = crudo.replace(",", ".");
      valor = Number(normal);
      decimales = normal.includes(".") ? normal.split(".")[1].length : 0;
      magnitud = 1;
    }
    if (!Number.isFinite(valor)) continue;
    if (Number.isInteger(valor) && valor >= 1900 && valor <= 2100) continue; // años
    encontradas.push({ texto: m[0].trim(), valor, decimales, magnitud });
  }
  return encontradas;
}

function redondear(valor, decimales) {
  const factor = 10 ** decimales;
  return Math.round(valor * factor) / factor;
}

// Las direcciones web no contienen cifras estadísticas: el DOI
// "10.1371/journal.pone.0194889" de una referencia bibliográfica no es
// un conteo que deba coincidir con ningún dato. Se quitan antes de
// buscar cifras (detectado al imprimir la bibliografía en el informe,
// 2026-08-19: el guardián marcaba "10.137" y "10.121" de dos DOI).
function sinEnlaces(texto) {
  return texto.replace(/<?https?:\/\/[^\s>)\]]+>?/g, " ");
}

function csvsBajo(carpeta) {
  const rutas = [];
  let entradas = [];
  try {
    entradas = fs.readdirSync(carpeta, { withFileTypes: true });
  } catch {
    return rutas;
  }
  for (const e of entradas) {
    const ruta = path.join(carpeta, e.name);
    if (e.isDirectory()) rutas.push(...csvsBajo(ruta));
    else if (e.name.endsWith(".csv")) rutas.push(ruta);
  }
  return rutas;
}

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

  // Numeros reales: outputs ya ejecutados + CSV versionados del proyecto
  // (el informe vive en <raiz>/notebooks/, asi que la raiz es el padre).
  const reales = [];
  for (const cell of nb.cells || []) {
    if (cell.cell_type === "code") reales.push(...valoresDe(textoDeOutputs(cell)));
  }
  const raiz = path.dirname(path.dirname(rutaNotebook));
  for (const carpeta of ["datos_curados", "resultados"]) {
    for (const csv of csvsBajo(path.join(raiz, carpeta))) {
      try {
        reales.push(...valoresDe(fs.readFileSync(csv, "utf-8")));
      } catch {
        // Un CSV ilegible no tira el hook abajo; el pool sigue con el resto.
      }
    }
  }
  if (reales.length === 0) process.exit(0); // sin datos todavia: nada que contrastar

  let dentroDelResumen = false;
  const sospechosas = [];
  for (const cell of nb.cells || []) {
    if (cell.cell_type !== "markdown") continue;
    const texto = fuenteDe(cell);
    if (ENCABEZADO_RESUMEN.test(texto)) {
      dentroDelResumen = true;
      continue;
    }
    if (!dentroDelResumen) continue;
    for (const cifra of cifrasDe(sinEnlaces(texto))) {
      // Para los enteros con separador de miles se acepta también la
      // equivalencia de escala x1000: varias fuentes publican conteos en
      // miles (la ENSANNA publica 40,2 miles de NNA y el texto escribe
      // "40.200") — el mismo número en otra unidad, no una cifra
      // distinta. Detectado al separar el resumen analítico en celdas
      // (2026-08-19): hasta entonces esos párrafos compartían celda con
      // el encabezado y quedaban exentos por accidente.
      const existe = reales.some((real) =>
        cifra.magnitud > 1
          ? Math.round(real / cifra.magnitud) * cifra.magnitud === cifra.valor
            || Math.round((real * 1000) / cifra.magnitud) * cifra.magnitud === cifra.valor
          : redondear(real, cifra.decimales) === cifra.valor
      );
      if (!existe) sospechosas.push(cifra.texto);
    }
  }

  if (sospechosas.length === 0) process.exit(0);

  const lista = [...new Set(sospechosas)].join(", ");
  process.stdout.write(
    denegar(
      "informe-cifras-sin-respaldo",
      `El "Resumen analítico" o las "Conclusiones" citan cifras que no aparecen en ningún ` +
        `output ejecutado del notebook ni en los CSV versionados del proyecto: ${lista}. ` +
        `Son las únicas secciones donde los números se escriben a mano, así que un error de ` +
        `transcripción ahí no lo detecta nada más. Sacar cada número del dato real (con ` +
        `Python, no de memoria) y reescribir esa parte en informe_celdas_2.py — un redondeo ` +
        `honesto coincide al redondear; una cifra recordada, no.`,
      { notebook: path.basename(rutaNotebook), cifras: [...new Set(sospechosas)] }
    )
  );
  process.exit(0);
});
