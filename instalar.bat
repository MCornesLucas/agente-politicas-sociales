@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================================
echo   Instalador - Agente de Politicas Sociales
echo ================================================
echo.

REM --- 1. Verificar Node.js (lo necesita Claude Code) ---
where node >nul 2>nul
if errorlevel 1 (
    echo [1/5] No se encontro Node.js en esta computadora.
    echo        Se va a abrir la pagina de descarga en tu navegador.
    echo        Instala Node.js con las opciones por defecto y despues
    echo        vuelve a hacer doble clic en este archivo, instalar.bat,
    echo        para continuar donde quedaste.
    echo.
    start https://nodejs.org
    if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
    exit /b 1
)
echo [1/5] Node.js encontrado: OK

REM --- 2. Verificar/instalar Claude Code ---
REM Version FIJADA a proposito, no "lo ultimo que haya hoy": el flujo se
REM prueba de punta a punta con esta version, y un instalador que trae una
REM version distinta segun el dia convierte cualquier cambio de
REM comportamiento en un "no me funciona" indiagnosticable a distancia.
REM Para actualizarla: probar el flujo completo con la version nueva y
REM recien entonces cambiar este numero (misma logica que fijar el modelo
REM en abrir_agente.bat).
where claude >nul 2>nul
if errorlevel 1 (
    echo [2/5] Instalando Claude Code, puede tardar un minuto...
    call npm install -g @anthropic-ai/claude-code@2.1.233
    if errorlevel 1 (
        echo.
        echo No se pudo instalar Claude Code. Revisa tu conexion a
        echo internet y vuelve a intentar.
        if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
        exit /b 1
    )
) else (
    echo [2/5] Claude Code ya estaba instalado: OK
)

REM --- 3. Detectar Python (Anaconda) ---
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
echo [3/5] Python encontrado: OK

REM --- 4. Instalar las dependencias del proyecto ---
echo [4/5] Instalando las dependencias de Python del proyecto...
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

REM Dejar la carpeta pre-aprobada en Claude Code (modulo creado por el
REM dueno del proyecto): sin esto, la primera corrida de abrir_agente.bat
REM muestra un chequeo interactivo de confianza EN LA CONSOLA - justo lo
REM que el usuario final no debe ver (hallazgo de la primera corrida
REM real). El consentimiento es correr este instalador; si falla, no es
REM grave: el chequeo aparece una unica vez.
"!PYEXE!" -m politicas_sociales.preaprobar_confianza

REM --- 5. Preparar el generador de PDF (descarga Chromium una sola vez) ---
echo [5/5] Preparando el generador de informes PDF, puede tardar unos minutos la primera vez...
"!PYEXE!" -m playwright install chromium
REM Sin este chequeo, si la descarga de Chromium falla (red, proxy,
REM antivirus) el instalador igual diria "Listo" y el problema apareceria
REM mucho despues, al generar el PDF en medio de una corrida real
REM (leccion de una corrida real del instalador).
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
echo Para usar el agente, cierra esta ventana y haz doble clic en
echo el archivo "abrir_agente.bat", que esta en esta misma carpeta.
echo.
echo No hace falta escribir ningun comando: el agente te va a ir
echo guiando con formularios que se abren en el navegador.
echo.
if not defined POLITICAS_SOCIALES_NONINTERACTIVE pause
