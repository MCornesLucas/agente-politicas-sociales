@echo off
cd /d "%~dp0"
title Agente - Politicas Sociales de Infancia

where claude >nul 2>nul
if errorlevel 1 (
    echo No se encontro Claude Code en esta computadora.
    echo Ejecuta primero instalar.bat, que esta en esta misma carpeta.
    pause
    exit /b 1
)

REM Minimiza esta terminal mientras se responde el formulario de arranque
REM (bienvenida con botones "Empezar" / "Salir"), para que lo primero que
REM se vea sea ese formulario en el navegador, no una consola vacia. Es
REM solo cosmetico: si falla, el arranque sigue igual.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0.claude\arranque\ventana.ps1" -Titulo "Agente - Politicas Sociales de Infancia" -Accion Minimizar >nul 2>nul

set "ACCION="
for /f "delims=" %%A in ('run_python.bat arranque.py') do set "ACCION=%%A"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0.claude\arranque\ventana.ps1" -Titulo "Agente - Politicas Sociales de Infancia" -Accion Restaurar >nul 2>nul

if /i not "%ACCION%"=="EMPEZAR" (
    exit /b 0
)

REM --- Cierre automatico de esta ventana al terminar el flujo ---
REM Una sesion interactiva de Claude Code no termina nunca por si sola, asi
REM que es el propio proyecto quien cierra la sesion cuando el flujo
REM termina de verdad (src/politicas_sociales/cierre.py, llamado desde los
REM formularios). Estas dos variables le avisan que esta corriendo bajo
REM esta ventana y cual es la consola a cerrar; se definen recien aca,
REM despues del formulario de arranque, para que arranque.py no pueda
REM disparar un cierre cuando todavia no hay sesion que cerrar.
REM
REM El PID de esta ventana se averigua con REDIRECCION a archivo y no con
REM `for /f ('...')`: `for /f` corre el comando dentro de un cmd.exe
REM intermedio, asi que el padre de powershell seria ese proceso efimero
REM en vez de esta consola (verificado en el proyecto hermano contra un
REM arbol de procesos real).
set "POLITICAS_SOCIALES_CONSOLA=1"
set "ARCHIVO_PID=%TEMP%\politicas-sociales-pid-%RANDOM%.txt"
powershell -NoProfile -Command "$f = 'ProcessId=' + $PID; $p = Get-CimInstance Win32_Process -Filter $f; $p.ParentProcessId" > "%ARCHIVO_PID%"
set /p POLITICAS_SOCIALES_CONSOLA_PID=<"%ARCHIVO_PID%"
del "%ARCHIVO_PID%" >nul 2>nul

set "MARCA_CIERRE=%TEMP%\politicas-sociales-cierre-%POLITICAS_SOCIALES_CONSOLA_PID%.marker"
if exist "%MARCA_CIERRE%" del "%MARCA_CIERRE%" >nul 2>nul

REM --model se fija a proposito: sin el, la sesion toma el modelo por
REM defecto de la cuenta, que puede cambiar sin que nadie toque el
REM proyecto (mismo criterio que el proyecto hermano; si se actualiza
REM aca, actualizar tambien el frontmatter del agente).
claude --model claude-opus-5 "Quiero el informe de politicas sociales de infancia"

REM Terminar el proceso de Claude Code hace que `claude` salga con codigo
REM de error, asi que el codigo de salida solo no distingue "el flujo
REM termino bien y pedimos cerrar" de "Claude Code se rompio de verdad" -
REM esa diferencia la marca este archivo. Con marca: cierre normal. Sin
REM marca y con error: se avisa y se deja la ventana abierta para ver que
REM paso.
if exist "%MARCA_CIERRE%" (
    del "%MARCA_CIERRE%" >nul 2>nul
    exit /b 0
)

if errorlevel 1 (
    echo.
    echo Hubo un problema y la sesion de Claude Code termino con error.
    pause
    exit /b 1
)

exit /b 0
