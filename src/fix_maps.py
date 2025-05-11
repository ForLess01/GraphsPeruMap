
import folium
import os
import pandas as pd

# Corregir visualizacion.py
try:
    with open('src/visualizacion.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Reemplazar la creación del mapa sin atribuciones
    new_content = content.replace('mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', 
                               'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> &copy; <a href='http://cartodb.com/attributions'>CartoDB</a>")')
    
    # Reemplazar capas adicionales
    new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", 
                                  "folium.TileLayer('OpenStreetMap', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    
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
                               'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> &copy; <a href='http://cartodb.com/attributions'>CartoDB</a>")')
    
    # Reemplazar capas adicionales
    new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", 
                                  "folium.TileLayer('OpenStreetMap', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", 
                                  "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(mapa)")
    
    with open('src/visualizacion_mejorada.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("- Archivo de visualización mejorada corregido")
except Exception as e:
    print(f"Error al corregir visualizacion_mejorada.py: {e}")

print("Correcciones completadas.")
        