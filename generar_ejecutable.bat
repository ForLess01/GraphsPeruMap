@echo off
echo ====================================================
echo Generador de Ejecutable para GraphsPeruMap
echo ====================================================
echo.
echo Este script creara un ejecutable standalone de la aplicacion.
echo.

:: Verificar si el entorno virtual existe
if not exist venv\Scripts\activate.bat (
    echo ERROR: El entorno virtual no existe.
    echo Por favor, ejecute primero instalar_ejecutar.bat
    pause
    exit /b 1
)

:: Activar el entorno virtual
call venv\Scripts\activate.bat

:: Instalar PyInstaller si no está instalado
pip show pyinstaller > nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo instalar PyInstaller.
        pause
        exit /b 1
    )
)

:: Crear el ejecutable
echo Generando ejecutable (puede tardar unos minutos)...
pyinstaller --name="GraphsPeruMap" ^
            --windowed ^
            --onedir ^
            --add-data="data;data" ^
            --add-data="resources;resources" ^
            --icon="resources/icono.ico" ^
            main.py

echo.
echo Ejecutable creado en: dist\GraphsPeruMap\GraphsPeruMap.exe
echo.
pause
