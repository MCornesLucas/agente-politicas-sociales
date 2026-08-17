# Notas de curado — ENSANNA 2024 y ENTI 2009-2010

`ensanna_2024.csv` transcribe la totalidad de los datos publicados en el
boletín oficial de la ENSANNA 2024 (INE/MTSS, con apoyo de OIT y UNICEF):
4 cuadros (tasa y volumen por región, sexo, grupo de edad y nivel
socioeconómico) y 4 gráficos (descomposición en trabajo en la frontera
de producción, TFP, y trabajo no remunerado de servicios, TNRS, por las
mismas cuatro aperturas — solo porcentajes). Archivo fuente descargado:
`data/ensanna/2024/informe_trabajo_infantil_ensanna_2024.html`; los
valores de los gráficos provienen del JSON de plotly embebido en ese
HTML. Verificación por muestreo realizada contra el HTML (6,8 / 40,2 /
10,6 / títulos de cuadros presentes).

Decisiones y advertencias:

- **NSE**: el nivel socioeconómico del Cuadro 4 es el INSE (CINVE), no
  quintiles de ingreso ni el estrato de la ECH — no cruzar con esas
  variables como si fueran equivalentes.
- **Universo**: NNA de 5 a 17 años; todas las tasas tienen ese
  denominador.
- **ENTI 2009-2010**: se transcriben solo las tres cifras de cabecera
  (9,9% FPSCN; 13,4% FGP; 8,5% trabajo peligroso) como referencia. La
  comparación 2010 ↔ 2024 exige elegir definición y declarar la posible
  incomparabilidad (el propio informe 2010 la advierte); nunca graficar
  ambas como serie continua.
- **Lo que el boletín 2024 no publica** (y por lo tanto no está aquí):
  asistencia escolar, horas trabajadas, trabajo peligroso, apertura
  departamental, cruces entre aperturas. Se incorporarán si el INE
  publica los microdatos.
