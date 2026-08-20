# Instrucciones para Claude Code en este proyecto

Proyecto de análisis de políticas sociales de infancia en Uruguay:
registros administrativos e informes institucionales de los organismos
del área, más los microdatos de la ECH (INE) para el universo 0-17.

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
  verificando que la definición esperada existe. Lección aprendida:
  los guardianes/supuestos sin verificar contra la
  salida real fallan en silencio.
- **Microdatos (ENSANNA, ECH): siempre ponderados.** Nunca `.mean()` /
  `.value_counts()` simple sobre una muestra.
- **Cifras en informes: siempre reales, nunca estimadas ni recordadas.**
  Si un número no está en un archivo descargado en `data/` o en una
  fuente citada, no va.
- **Separación de audiencias en el bloque predictivo**: la elección de
  algoritmos y sus métricas de backtest se documentan en
  `docs/PREDICTIVO_JUSTIFICACION_TECNICA.md` (público técnico:
  analistas, economistas, estadísticos). En el informe y para el usuario
  final va solo el escenario con su rango y su supuesto inercial — nunca
  MAE/MAPE/nombres de modelos. Una proyección sin su tabla de backtest
  en ese documento no se publica.
- **Tema sensible**: redacción según la terminología de los organismos
  ("niñas, niños y adolescentes"/"NNA", "situación de trabajo infantil",
  "situaciones atendidas"). No desagregar números de víctimas más que lo
  que publica el propio organismo.
- `data/` no se versiona (ver `.gitignore`): los datos se descargan de
  las fuentes citadas, no se redistribuyen.

## Código y tests

- El código vive en el paquete `politicas_sociales` (`src/politicas_sociales/`);
  los pipelines se ejecutan como módulos (`python -m politicas_sociales.metricas_ech`),
  nunca como scripts sueltos por ruta.
- En una máquina instalada con `instalar.bat`, invocar Python siempre a
  través de `run_python.bat` (lee la ruta real de `.claude/python_path.txt`),
  nunca por una ruta de Python escrita a mano.
- Las rutas del proyecto se centralizan en `politicas_sociales/config.py`
  (las de los microdatos ECH, en `politicas_sociales/ech/config.py`) —
  ningún módulo escribe rutas absolutas.
- La suite (`python -m pytest`) cubre la lógica pura y los guardianes de
  datos; todo guardián nuevo lleva su test que verifique que realmente
  detiene la corrida con datos que no cumplen (lección heredada:
  los supuestos sin verificar contra la salida real fallan en silencio).
- Los guardianes del informe viven en `.claude/hooks/*.cjs` (calibrados
  contra el notebook real, con tests en ambas direcciones: dejan pasar el
  informe correcto y bloquean uno saboteado) y se registran en
  `.claude/settings.json`, que edita solo el dueño del proyecto.
- El flujo guiado para usuarios no técnicos (`abrir_agente.bat` →
  formularios en el navegador → informe → cierre automático de la
  consola) lo conduce el agente `.claude/agents/politicas-sociales.md`;
  la maquinaria (formularios, bitácora, cierre, entrega) vive en el
  paquete, con sus lecciones documentadas en cada módulo.

## Mantenimiento

- Los pendientes de terceros (microdatos ENSANNA, retrospectivas INE,
  ESNNA/CONAPEES, plan CETI, publicaciones UNICEF) se revisan con
  `python -m politicas_sociales.vigilancia` contra el estado conocido en
  `datos_curados/vigilancia_baseline.json` (ver
  `docs/RELEVAMIENTO_DE_DATOS.md`, sección "Vigilancia").

- **Lenguaje formal y español neutro** en toda la documentación y en los
  informes: sin voseo ni regionalismos coloquiales ("acá", "arrancar",
  "ganarle"); se escribe "aquí", "comenzar", "superar". El modelo de
  estilo son `docs/METODOLOGIA.md` y los informes generados. Los términos
  técnicos de los organismos se conservan tal cual.
- Una sola copia del proyecto (esta). Desarrollar, probar y commitear
  desde aquí; revisar el diff uno mismo antes de commitear, sin pedir
  confirmación en el chat.
- Repositorio: https://github.com/MCornesLucas/agente-politicas-sociales
