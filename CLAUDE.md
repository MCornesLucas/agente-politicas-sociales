# Instrucciones para Claude Code en este proyecto

Proyecto de análisis de políticas sociales de infancia en Uruguay, hermano
de [agente-encuesta-hogares](https://github.com/testa10/agente-encuesta-hogares)
(misma exigencia de rigor, fuentes distintas: registros administrativos e
informes institucionales además de una encuesta).

## Antes de escribir cualquier análisis o gráfica

1. Leer `docs/METODOLOGIA.md` — las reglas de la sección 2 no son
   negociables. La central: **casos atendidos ≠ prevalencia**. Ningún
   número de SIPIAV/CONAPEES/INAU se redacta ni grafica como prevalencia.
2. Consultar `docs/FUENTES_DE_DATOS.md` antes de usar un número de
   cualquier organismo — la "naturaleza del dato" de cada fuente define
   qué afirmaciones son defendibles.
3. Consultar `docs/BIBLIOGRAFIA.md` antes de buscar una fuente nueva —
   puede que ya esté citada. Toda fuente nueva se agrega ahí (y en
   `FUENTES_DE_DATOS.md` si es fuente de datos).

## Reglas de trabajo

- **Ninguna métrica se da por existente sin ver el dato real.** El
  catálogo (`docs/CATALOGO_DE_METRICAS.md`) es un borrador de diseño:
  cada métrica se confirma descargando el informe o microdato y
  verificando que la definición esperada existe. Lección heredada del
  proyecto original: los guardianes/supuestos sin verificar contra la
  salida real fallan en silencio.
- **Microdatos (ENSANNA, ECH): siempre ponderados.** Nunca `.mean()` /
  `.value_counts()` simple sobre una muestra.
- **Cifras en informes: siempre reales, nunca estimadas ni recordadas.**
  Si un número no está en un archivo descargado en `data/` o en una
  fuente citada, no va.
- **Tema sensible**: redacción según la terminología de los organismos
  ("niñas, niños y adolescentes"/"NNA", "situación de trabajo infantil",
  "situaciones atendidas"). No desagregar números de víctimas más que lo
  que publica el propio organismo.
- `data/` no se versiona (ver `.gitignore`): los datos se descargan de
  las fuentes citadas, no se redistribuyen.

## Mantenimiento

- Una sola copia del proyecto (esta). Desarrollar, probar y commitear
  desde acá; revisar el diff uno mismo antes de commitear, sin pedir
  confirmación en el chat.
- Repositorio: https://github.com/testa10/agente-politicas-sociales
