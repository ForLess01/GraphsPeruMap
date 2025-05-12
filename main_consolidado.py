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
        'Pillow',         # Necesario para la visualización con Matplotlib
        'geopandas',      # Para posible manejo de datos geográficos
        'shapely'         # Para posible manejo de datos geográficos
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

def fix_folium_maps():
    """Corregir problemas conocidos con los mapas de Folium"""
    print("Verificando y corrigiendo configuración de mapas...")
    
    try:
        # Corregir visualizacion_consolidada.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        vis_path = os.path.join(script_dir, 'src', 'visualizacion_consolidada.py')
        
        # Verificar que el archivo exista
        if not os.path.exists(vis_path):
            print(f"Archivo no encontrado: {vis_path}")
            return False
        
        with open(vis_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya tiene atribuciones
        if 'attr=' in content:
            print("La visualización ya tiene las atribuciones correctas.")
            return True
            
        # Reemplazar la creación del mapa sin atribuciones
        new_content = content.replace(
            'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', 
            'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", ' + 
            'attr="&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> &copy; <a href=\'http://cartodb.com/attributions\'>CartoDB</a>")'
        )
        
        # Reemplazar capas adicionales
        new_content = new_content.replace(
            "folium.TileLayer('OpenStreetMap').add_to(mapa)",
            "folium.TileLayer('OpenStreetMap', attr='&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)"
        )
        new_content = new_content.replace(
            "folium.TileLayer('Stamen Terrain').add_to(mapa)",
            "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)"
        )
        new_content = new_content.replace(
            "folium.TileLayer('Stamen Toner').add_to(mapa)",
            "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)"
        )
        
        # Guardar el archivo modificado
        with open(vis_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Correcciones de mapas aplicadas correctamente.")
        return True
        
    except Exception as e:
        print(f"Error al aplicar correcciones de mapas: {str(e)}")
        return False

if __name__ == '__main__':
    # Verificar dependencias antes de iniciar la aplicación
    check_dependencies()
    
    # Corregir problemas conocidos con Folium
    fix_folium_maps()
    
    try:
        # Importamos la versión consolidada
        from src.app_consolidada import main
        print("\nIniciando GraphsPeruMap (versión consolidada)...\n")
        main()
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Es posible que algunas dependencias no se hayan instalado correctamente.")
        print("Por favor, instala manualmente los paquetes requeridos:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)
