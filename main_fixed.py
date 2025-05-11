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
        'PyQtWebEngine',  # Necesario para QWebEngineView
        'Pillow'          # Necesario para la visualización con Matplotlib
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

def select_app_version():
    """Permitir al usuario seleccionar la versión de la aplicación a ejecutar"""
    print("\n============== GraphsPeruMap ==============")
    print("1. Versión Estándar (puede requerir atención a errores)")
    print("2. Versión Mejorada (recomendada)")
    print("==========================================\n")
    
    try:
        choice = input("Seleccione una versión (1 o 2, Enter para versión mejorada): ")
        if choice == "1":
            return "standard"
        else:
            return "improved"
    except:
        return "improved"  # Por defecto usar la versión mejorada

if __name__ == '__main__':
    # Verificar dependencias antes de iniciar la aplicación
    check_dependencies()
    
    # Corregir posible error de atribuciones en los mapas
    try:
        print("Verificando y corrigiendo configuración de mapas...")
        # Script para corregir las atribuciones en los archivos de visualización
        fix_script = """
import folium
import os
import pandas as pd

# Corregir visualizacion.py
try:
    with open('src/visualizacion.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Reemplazar la creación del mapa sin atribuciones
    new_content = content.replace('mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', 
                               'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> &copy; <a href=\'http://cartodb.com/attributions\'>CartoDB</a>")')
    
    # Reemplazar capas adicionales
    new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", 
                                  "folium.TileLayer('OpenStreetMap', attr='&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    
    with open('src/visualizacion.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("- Archivo de visualización básica corregido")
except Exception as e:
    print(f"Error al corregir visualizacion.py: {e}")

# Corregir visualizacion_mejorada.py
try:
    with open('src/visualizacion_mejorada.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Reemplazar la creación del mapa sin atribuciones
    new_content = content.replace('mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', 
                               'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> &copy; <a href=\'http://cartodb.com/attributions\'>CartoDB</a>")')
    
    # Reemplazar capas adicionales
    new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", 
                                  "folium.TileLayer('OpenStreetMap', attr='&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)")
    
    with open('src/visualizacion_mejorada.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("- Archivo de visualización mejorada corregido")
except Exception as e:
    print(f"Error al corregir visualizacion_mejorada.py: {e}")

print("Correcciones completadas.")
        """
        
        # Ejecutar el script de corrección
        with open('src/fix_maps.py', 'w') as f:
            f.write(fix_script)
        subprocess.call([sys.executable, 'src/fix_maps.py'])
        
    except Exception as e:
        print(f"ADVERTENCIA: No se pudieron aplicar correcciones automaticas: {e}")
    
    # Seleccionar y ejecutar la versión de la aplicación
    app_version = select_app_version()
    
    try:
        if app_version == "standard":
            # Importamos la versión estándar
            print("\nIniciando versión estándar...\n")
            from src.app import main
            main()
        else:
            # Importamos la versión mejorada
            print("\nIniciando versión mejorada...\n")
            from src.app_mejorada import main
            main()
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Es posible que algunas dependencias no se hayan instalado correctamente.")
        print("Por favor, instala manualmente los paquetes requeridos:")
        print("  pip install networkx matplotlib folium pandas PyQt5 PyQtWebEngine Pillow")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        print("\nIntentando ejecutar la versión alternativa...")
        
        try:
            if app_version == "standard":
                # Si falló la estándar, intentamos con la mejorada
                from src.app_mejorada import main
                main()
            else:
                # Si falló la mejorada, intentamos con la estándar
                from src.app import main
                main() 
        except Exception as e2:
            print(f"Error en la versión alternativa: {e2}")
            print("\nPuede ejecutar manualmente alguna de las siguientes opciones:")
            print("  python src/app.py")
            print("  python src/app_mejorada.py")
            sys.exit(1)
