@echo off
echo ====================================================
echo Instalacion y Ejecucion de GraphsPeruMap
echo ====================================================
echo.
echo Este script instalara todas las dependencias y ejecutara la aplicacion.
echo.

:: Verificar si Python esta instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado en este sistema.
    echo Por favor, instale Python 3.8 o superior desde https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo [4/4] Ejecutando la aplicacion...
echo.
python main.py

pause
