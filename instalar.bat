@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================================
echo   Instalador - Agente de Politicas Sociales
echo ================================================
echo.

REM Este instalador cubre el lado Python del proyecto (paquete,
REM dependencias, generador de PDF). Los pasos de Node/Claude Code y la
REM ventana del agente (abrir_agente.bat) llegan con el punto
REM "formularios" de la lista de paridad: hoy este proyecto no tiene
REM flujo de usuario no tecnico que abrir.

REM --- 1. Detectar Python (Anaconda) ---
REM Se prueba primero la ubicacion tipica de Anaconda, sin depender del
REM PATH: Windows trae un "python.exe" falso propio (el alias de Microsoft
REM Store) que aparece en el PATH aunque no haya ningun Python instalado
REM de verdad, asi que "where python" solo no alcanza para confiar en el.
set "PYEXE=C:\Users\%USERNAME%\anaconda3\python.exe"

if not exist "!PYEXE!" (
    set "PYEXE="
    for /f "delims=" %%v in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PYEXE=%%v"

    if "!PYEXE!"=="" (
        echo.
        echo No se encontro una instalacion de Python/Anaconda utilizable.
        echo Instala Anaconda desde https://www.anaconda.com/download y
        echo vuelve a correr este instalador.
        if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
        exit /b 1
    )
)
echo [1/4] Python encontrado: OK

REM --- 2. Verificar el proyecto hermano agente-encuesta-hogares ---
REM Este proyecto importa los loaders de la ECH desde la copia de trabajo
REM del proyecto hermano (ver src/politicas_sociales/config.py): sin el,
REM la extraccion de la ECH y varias metricas no pueden correr. Se acepta
REM la carpeta hermana o la ruta indicada en AGENTE_ECH_RUTA.
set "ECH_RUTA=%~dp0..\agente-encuesta-hogares"
if defined AGENTE_ECH_RUTA set "ECH_RUTA=%AGENTE_ECH_RUTA%"

if not exist "!ECH_RUTA!\src\encuesta_hogares\" (
    echo.
    echo No se encontro el proyecto hermano agente-encuesta-hogares en:
    echo   !ECH_RUTA!
    echo.
    echo Descargalo de https://github.com/testa10/agente-encuesta-hogares
    echo y dejalo como carpeta hermana de esta ^(mismo directorio^), o
    echo define la variable de entorno AGENTE_ECH_RUTA con su ruta, y
    echo vuelve a correr este instalador.
    if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
    exit /b 1
)
echo [2/4] Proyecto hermano agente-encuesta-hogares: OK

REM --- 3. Instalar las dependencias del proyecto ---
echo [3/4] Instalando las dependencias de Python del proyecto...
"!PYEXE!" -m pip install -e ".[dev]" --quiet
if errorlevel 1 (
    echo.
    echo Hubo un problema instalando las dependencias de Python.
    if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
    exit /b 1
)

REM Guardar la ruta exacta de Python para que el agente la use directamente,
REM sin tener que volver a buscarla ni adivinar cada vez que corre un comando.
if not exist ".claude" mkdir ".claude"
> ".claude\python_path.txt" echo !PYEXE!

REM --- 4. Preparar el generador de PDF (descarga Chromium una sola vez) ---
echo [4/4] Preparando el generador de informes PDF, puede tardar unos minutos la primera vez...
"!PYEXE!" -m playwright install chromium
REM Sin este chequeo, si la descarga de Chromium falla (red, proxy,
REM antivirus) el instalador igual diria "Listo" y el problema apareceria
REM mucho despues, al generar el PDF en medio de una corrida real
REM (leccion heredada del instalador del proyecto hermano).
if errorlevel 1 (
    echo.
    echo No se pudo preparar el generador de informes PDF. Revisa tu
    echo conexion a internet y vuelve a correr este instalador.
    if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
    exit /b 1
)

echo.
echo ================================================
echo   Listo. Ya esta todo instalado.
echo ================================================
echo.
echo Los pipelines se ejecutan con run_python.bat, por ejemplo:
echo   run_python.bat -m politicas_sociales.metricas_ech
echo y la suite de tests con:
echo   run_python.bat -m pytest
echo.
if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
