@echo off
echo ====================================================
echo GraphsPeruMap - Version Consolidada Mejorada
echo ====================================================
echo.
echo Este script ejecutara la version consolidada y mejorada
echo de la aplicacion GraphsPeruMap.
echo.

REM Verificar si Python esta instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado en este sistema.
    echo Por favor, instale Python 3.8 o superior desde https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Ejecutando la aplicacion...
echo.

python main_consolidado.py

echo.
pause
