// Deja constancia en la bitacora cuando un hook BLOQUEA una herramienta.
//
// Nacio de un hueco de
// observabilidad real: un notebook ejecutado tres veces en una corrida y
// ningun rastro de si fueron bloqueos de hooks (calidad bien invertida) o
// retrabajo evitable. Sin registro no se puede decidir.
//
// POLITICAS_SOCIALES_BITACORA permite redirigir el log a otro archivo.
// Existe para los tests: sin esto, cualquier test que corra un hook de
// verdad escribe en la bitacora REAL de quien tenga el proyecto en esa
// carpeta (leccion aprendida dos veces en corridas reales). En una
// corrida normal la variable no existe y se usa logs/bitacora.jsonl.
const fs = require("fs");
const path = require("path");

// El .cjs vive en <proyecto>/.claude/hooks/, asi que la raiz esta dos
// niveles arriba. No se usa CLAUDE_PROJECT_DIR como unica fuente a
// proposito: se ha visto esa variable llegar vacia en produccion
// y dejar los hooks sin correr durante dias.
const RAIZ = path.resolve(__dirname, "..", "..");

const LOG = process.env.POLITICAS_SOCIALES_BITACORA || path.join(RAIZ, "logs", "bitacora.jsonl");

function registrar(tipo, detalle) {
  try {
    fs.mkdirSync(path.dirname(LOG), { recursive: true });
    const linea = {
      timestamp: new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00"),
      tipo,
      ...detalle,
    };
    fs.appendFileSync(LOG, JSON.stringify(linea) + "\n", "utf-8");
  } catch {
    // Un fallo al escribir el log nunca puede tirar abajo el flujo real:
    // la bitacora es de apoyo, jamas la causa de un problema nuevo.
  }
}

/** Registra el bloqueo y devuelve el JSON PreToolUse que Claude Code espera. */
function denegar(hook, motivo, detalle = {}) {
  registrar("hook_bloqueo", { hook, ...detalle });
  return JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: motivo,
    },
  });
}

module.exports = { registrar, denegar };
