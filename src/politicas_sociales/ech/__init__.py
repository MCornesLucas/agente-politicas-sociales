"""Carga de microdatos de la ECH (INE Uruguay).

Subpaquete autocontenido: resuelve rutas, nombres de archivo y columnas de
los microdatos oficiales de la Encuesta Continua de Hogares que viven en
`data/ech_microdatos/{año}/`, y los carga corrigiendo los problemas de
codificación y los cambios de formato que el INE introdujo entre años —
todas decisiones verificadas contra los archivos reales publicados por el
INE (ver docs/RELEVAMIENTO_DE_DATOS.md para las fuentes).
"""
