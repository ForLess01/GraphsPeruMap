import sys
import os
import subprocess
import pkg_resources

def check_dependencies():
    """Verificar y instalar dependencias requeridas si es necesario"""
    required_packages = [
        'networkx',
        'matplotlib',
        'folium',
        'pandas',
        'PyQt5',
        'PyQtWebEngine'  # Necesario para QWebEngineView
    ]
    
    missing_packages = []
    
    # Verificar qué paquetes faltan
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
    
    # Instalar paquetes faltantes
    if missing_packages:
        print(f"Instalando dependencias faltantes: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("Instalación completa.")
    else:
        print("Todas las dependencias están instaladas correctamente.")

if __name__ == '__main__':
    # Verificar dependencias antes de iniciar la aplicación
    check_dependencies()
    
    try:
        # Importamos aquí después de verificar las dependencias
        from src.app import main
        main()
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Es posible que algunas dependencias no se hayan instalado correctamente.")
        print("Por favor, instala manualmente los paquetes requeridos:")
        print("  pip install networkx matplotlib folium pandas PyQt5 PyQtWebEngine")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)
