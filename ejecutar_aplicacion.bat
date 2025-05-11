@echo off
echo Bienvenido a GraphsPeruMap - Aplicacion de Rutas del Peru con Dijkstra
echo.
echo Por favor seleccione la version a ejecutar:
echo 1. Version Estandar (mejor compatibilidad, puede fallar en visualizacion)
echo 2. Version Mejorada (mas robusta, con opciones adicionales)
echo.

set /p opcion="Seleccione una opcion (1 o 2): "

echo.
echo Iniciando aplicacion...
echo.

if "%opcion%"=="1" (
    echo Ejecutando version estandar...
    powershell -Command "Start-Process -FilePath python -ArgumentList 'src/app.py'"
) else if "%opcion%"=="2" (
    echo Ejecutando version mejorada...
    powershell -Command "Start-Process -FilePath python -ArgumentList 'src/app_mejorada.py'"
) else (
    echo Opcion invalida. Se ejecutara la version mejorada por defecto.
    powershell -Command "Start-Process -FilePath python -ArgumentList 'src/app_mejorada.py'"
)

echo.
echo Si se muestra un dialogo de control de cuentas de usuario, por favor aceptelo.
echo.

pause
