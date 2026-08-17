# Notas de curación — series SIPIAV 2013-2024

Fuente: textos completos extraídos de los 12 informes de gestión SIPIAV (2013-2024), PDF originales en `data\sipiav\<año>\`. Cada valor de `sipiav_series.csv` fue verificado leyendo el fragmento de texto correspondiente del informe del año indicado en la columna `verificacion`. Regla aplicada: ningún valor sin respaldo textual explícito; los huecos se documentan, no se interpolan.

## Estado de las series

### Completas (todos los años del rango pedido)

| Serie | Rango | Observación |
|---|---|---|
| situaciones_atendidas | 2013-2024 | 2013-2022 extraídas del texto de cada informe; 2023 (8157) y 2024 (8924) provienen de nota oficial Presidencia/INAU (no extraíbles del PDF). Consistencia: ambos informes declaran un aumento del 9 % interanual, coherente con esas cifras. |
| distribucion_sexo | 2013-2024 | Femenino/Masculino, sin huecos. |
| inclusion_familia | 2014-2024 | Serie prioritaria (proyección P2), sin huecos. Dos valores provienen de prosa fraccionaria y están marcados: 2015 = 80 % («en 4 de 5 situaciones») y 2021 = 67 % («2 de cada 3», declarado estable respecto a 2020 = 67 %). |
| crl_cantidad | 2013-2024 | Se agregó 2013 (24 CRL) por mención retrospectiva del informe 2014. La serie no es monótona: 33 CRL en 2019 y 32 en 2020-2022, tal como publican los informes. |

### Con huecos

| Serie | Años con dato | Huecos y motivo |
|---|---|---|
| distribucion_edad | 2016-2019 completos por tramo | 2013-2015: los gráficos de los PDF no contienen texto extraíble; solo hay cifras exactas en prosa para tramos sueltos (2013: 6-12 = 48 %; 2014: 0-3 = 9 %; 2015: 0-3 = 13 %). 2020-2024: la prosa publica el agregado 0-5 y algunos tramos (falta 18 y más en todos; falta 6-12 en 2023 y 2024; falta 13-17 en 2023). |
| tipo_violencia | 2016-2024 completos por categoría | 2013: falta maltrato emocional («la mitad» en prosa; la suma de las demás categorías implicaría 51 %, por lo que no se consignó). 2015: solo abuso sexual (21 %) tiene cifra exacta. |
| recurrencia | 2013-2019 y 2022 | 2020, 2021, 2023, 2024: solo fracciones en prosa («3 de cada 4», «casi 9 de cada 10») sin porcentaje exacto; gráficos no extraíbles. |
| cronicidad | 2013, 2014, 2016-2019 | 2015 y 2020-2024: solo fracciones en prosa («1 de cada 10 en inicio», «casi 9 de 10 crónicas»). |
| visualizacion | 2016-2019 y 2023 | 2020, 2021, 2022, 2024: solo fracciones («1 de cada 3 visualiza», «dos tercios naturalizan»). El informe 2022 sí publica el desglose por sexo (F 39 %, M 26 %) pero no el total. Se incluyó 2016 aunque el pedido indicaba 2017-2024, por estar publicado con cifra exacta. |
| agresor_vinculo | 2013-2024 (parcial) | La cobertura de categorías se reduce desde 2020 porque los gráficos de torta dejan de ser extraíbles: 2020 conserva 5 categorías (prosa), 2021 tres, 2022-2024 solo padre y madre más la constante «9 de cada 10 familiares directos o del núcleo de convivencia» (sin cifra exacta desde 2022). 2014: el padre («casi 4 de cada 10») y el total familiar («más de 3 de cada 4») no tienen cifra exacta. |

## Quiebres de definición detectados

1. **Tipos de violencia, 2020**: aparece por primera vez la categoría «explotación sexual» como tipo separado (2 %), que hasta 2019 estaba subsumida en violencia sexual/abuso. Las categorías 2020-2023 son cinco: maltrato emocional, negligencia, abuso sexual, maltrato físico y explotación sexual.
2. **Tipos de violencia, 2024**: el informe fusiona abuso sexual y explotación sexual en una única categoría «violencias sexuales» (22 %). La serie de abuso sexual puro termina en 2023; no se descompuso el 22 % de 2024.
3. **Tramos de edad**: 2013-2019 publican cinco tramos (0-3, 4-5, 6-12, 13-17, 18 y más); desde 2020 la prosa reporta el agregado «0-5» (primera infancia) y deja de publicar cifras textuales para 18 y más. Se respetó el tramo tal como lo publica cada año, por lo que coexisten filas «0-3»/«4-5» (hasta 2019) y «0-5» (desde 2020).
4. **Base de cálculo**: hasta 2015 los porcentajes de tipos de violencia, recurrencia, cronicidad y agresores se calculan sobre el subconjunto con «información completa» (2013: 891 de 1319; 2014: 1323 de 1728; 2015: 1650 de 1908), mientras que sexo y edad se calculan sobre el total registrado. Desde 2019 los informes indican «porcentajes calculados en base a los casos válidos». Las fuentes también cambian: SIPI solo (2013-2016), +CHPR (2018-2019), SIPI+CRL (2020-2024).
5. **Agresores 2019**: el informe excluye explícitamente del análisis de vínculo a las personas perpetradoras de negligencia por dudas de confiabilidad de esa categoría; los porcentajes de 2019 (y siguientes) no son estrictamente comparables con 2013-2018.
6. **Recurrencia/cronicidad 2024**: el texto del informe 2024 dice «casi 9 de cada 10 recurrentes» y «casi 3 de cada 4 crónicas», invirtiendo la relación histórica (recurrencia ~75-80 %, cronicidad ~90 %). Posible errata del informe; al no haber cifras exactas no se consignó ningún valor.

## Ambigüedades resueltas

- **Abuso sexual 2013 (28 %)**: el informe 2013 solo dice «casi un tercio»; la cifra exacta proviene de las comparaciones retrospectivas de los informes 2014 («22 % frente a 28 %») y 2015 («en 2013 llegaba al 28 %»), coincidentes entre sí. Verificación marcada como retrospectiva.
- **Maltrato emocional 2014 (50 %) y 2022 (36 %)**: prosa no numérica («la mitad», «poco más de un tercio») pero con las demás categorías publicadas con cifra exacta; se consignó el complemento a 100, que coincide con la expresión en prosa. Marcado en `verificacion`.
- **Abuso sexual 2019**: un pasaje en prosa dice 23 % pero el gráfico y el resumen «En suma» del propio informe dicen 24 %; se consignó 24 con la discrepancia anotada.
- **Inclusión familiar 2019**: el informe 2019 publica 79 %; el informe 2020 cita retrospectivamente «del 71 % en 2019 a 67 % en 2020» (probable cambio de base de cálculo). Se consignó 79 (fuente primaria del año) con la discrepancia anotada en la fila.
- **Recurrencia 2014 (75 %)**: el informe 2014 solo dice «3 de cada 4, coincide con 2013»; el informe 2015 confirma «en 2014 eran recurrentes el 75 %».
- **Complementos binarios**: cuando el informe publica solo un lado de una variable binaria (p. ej. recurrente 75 %, visualiza 38 %), el otro lado se consignó por complemento a 100 y así se indica en `verificacion`.
- **Distribución de edad 2022 (6-12 = 36 %, 13-17 = 36 %)**: proviene del informe 2023 («el año anterior ambas franjas llegaron al 36 %»); el informe 2022 no publica las cifras en texto.

## Valores no consignados a propósito

Fracciones en prosa sin porcentaje exacto («casi 9 de 10», «2 de cada 3», «más de 3 de cada 4») no se convirtieron a número, salvo los casos marcados arriba donde otra mención del propio SIPIAV fija la cifra. Es preferible el hueco documentado al dato dudoso.
