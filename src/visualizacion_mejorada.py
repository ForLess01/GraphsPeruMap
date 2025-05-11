import folium
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from folium.plugins import MeasureControl
import io
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import base64

def generar_mapa_base(df_regiones, usar_matplotlib=False):
    """
    Generar un mapa base con todas las regiones de Perú
    
    Args:
        df_regiones: DataFrame con información de las regiones
        usar_matplotlib: Si es True, genera un mapa estático con Matplotlib en lugar de Folium
    
    Returns:
        mapa o imagen según el método utilizado
    """
    if usar_matplotlib:
        return generar_mapa_base_matplotlib(df_regiones)
    else:
        return generar_mapa_base_folium(df_regiones)

def generar_mapa_base_folium(df_regiones):
    """
    Generar un mapa base con Folium
    """
    # Coordenadas centrales de Perú
    peru_center = [-9.1900, -75.0152]
    
    # Crear mapa base con un estilo más atractivo
    mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")
    
    # Añadir control de medición de distancias
    mapa.add_child(MeasureControl())
    
    # Añadir marcadores para cada región con popups mejorados
    for idx, region in df_regiones.iterrows():
        popup_content = f"""
        <div style="font-family: Arial; width: 150px;">
            <h4 style="color: #2c3e50;">{region['region']}</h4>
            <p>Latitud: {region['latitude']:.4f}</p>
            <p>Longitud: {region['longitude']:.4f}</p>
        </div>
        """
        
        folium.Marker(
            location=[region['latitude'], region['longitude']],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=region['region'],  # Muestra el nombre al pasar el cursor
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(mapa)
    
    # Añadir capa de control para cambiar entre diferentes mapas base
    folium.TileLayer('OpenStreetMap').add_to(mapa)
    folium.TileLayer('Stamen Terrain').add_to(mapa)
    folium.TileLayer('Stamen Toner').add_to(mapa)
    folium.LayerControl().add_to(mapa)
    
    return mapa

def generar_mapa_base_matplotlib(df_regiones):
    """
    Generar un mapa base con Matplotlib
    """
    plt.figure(figsize=(10, 8))
    
    # Límites del mapa de Perú (ampliados un poco)
    min_lat, max_lat = -18.5, -0.0  # Sur a Norte
    min_lon, max_lon = -82.0, -68.0  # Oeste a Este
    
    # Fondo azul claro para el océano
    plt.fill_between([min_lon, max_lon], [min_lat, min_lat], [max_lat, max_lat], color='#ADD8E6')
    
    # Dibujar puntos para cada región
    for idx, region in df_regiones.iterrows():
        plt.plot(region['longitude'], region['latitude'], 'bo', markersize=8)
        plt.text(region['longitude']+0.2, region['latitude'], region['region'], 
                fontsize=8, ha='left', va='center')
    
    # Añadir título y etiquetas
    plt.title('Mapa de Regiones del Perú', fontsize=14)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    
    # Establecer los límites del gráfico
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)
    
    # Añadir cuadrícula
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Convertir el gráfico a una imagen
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Crear QPixmap desde los datos del buffer
    image = Image.open(buf)
    return image

def generar_mapa_con_ruta(df_regiones, ruta, distancias=None, usar_matplotlib=False):
    """
    Generar un mapa con la ruta resaltada entre regiones
    
    Args:
        df_regiones: DataFrame con información de las regiones
        ruta: Lista de regiones en la ruta
        distancias: Diccionario con las distancias entre cada par de regiones en la ruta
        usar_matplotlib: Si es True, genera un mapa estático con Matplotlib en lugar de Folium
        
    Returns:
        mapa o imagen según el método utilizado
    """
    if usar_matplotlib:
        return generar_mapa_con_ruta_matplotlib(df_regiones, ruta, distancias)
    else:
        return generar_mapa_con_ruta_folium(df_regiones, ruta, distancias)

def generar_mapa_con_ruta_folium(df_regiones, ruta, distancias=None):
    """
    Generar un mapa con la ruta resaltada usando Folium
    """
    # Coordenadas centrales de Perú
    peru_center = [-9.1900, -75.0152]
    
    # Crear mapa base con un estilo más atractivo
    mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")
    
    # Añadir control de medición de distancias
    mapa.add_child(MeasureControl())
    
    # Añadir marcadores para cada región con popups mejorados
    for idx, region in df_regiones.iterrows():
        # Decidir el color y estilo del marcador
        if region['region'] == ruta[0]:
            color = 'green'
            icon_type = 'play'
            z_index = 1000
        elif region['region'] == ruta[-1]:
            color = 'red'
            icon_type = 'flag-checkered'
            z_index = 1000
        elif region['region'] in ruta:
            color = 'blue'
            icon_type = 'map-marker'
            z_index = 900
        else:
            color = 'gray'
            icon_type = 'circle'
            z_index = 100
        
        # Crear contenido del popup
        popup_content = f"""
        <div style="font-family: Arial; width: 150px;">
            <h4 style="color: #2c3e50;">{region['region']}</h4>
            <p>Latitud: {region['latitude']:.4f}</p>
            <p>Longitud: {region['longitude']:.4f}</p>
        </div>
        """
        
        folium.Marker(
            location=[region['latitude'], region['longitude']],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=region['region'],
            icon=folium.Icon(color=color, icon=icon_type),
            z_index_offset=z_index
        ).add_to(mapa)
    
    # Añadir líneas para la ruta con estilo mejorado y popups para distancias
    puntos_ruta = []
    for i in range(len(ruta)):
        region = df_regiones[df_regiones['region'] == ruta[i]]
        puntos_ruta.append([region['latitude'].values[0], region['longitude'].values[0]])
    
    # Añadir líneas para cada segmento de la ruta
    for i in range(len(ruta) - 1):
        origen_region = df_regiones[df_regiones['region'] == ruta[i]]
        destino_region = df_regiones[df_regiones['region'] == ruta[i + 1]]
        
        origen_coords = [origen_region['latitude'].values[0], origen_region['longitude'].values[0]]
        destino_coords = [destino_region['latitude'].values[0], destino_region['longitude'].values[0]]
        
        # Determinar la distancia para este segmento
        distancia_segmento = "N/A"
        if distancias and (ruta[i], ruta[i + 1]) in distancias:
            distancia_segmento = distancias[(ruta[i], ruta[i + 1])]
        
        # Crear una línea con un popup que muestre la distancia
        line = folium.PolyLine(
            [origen_coords, destino_coords],
            color='#FF6B6B',
            weight=5,
            opacity=0.8,
            tooltip=f"{ruta[i]} → {ruta[i + 1]}: {distancia_segmento} km"
        )
        line.add_to(mapa)
        
        # Añadir un marcador en el punto medio para mayor visibilidad
        mid_lat = (origen_coords[0] + destino_coords[0]) / 2
        mid_lon = (origen_coords[1] + destino_coords[1]) / 2
        
        folium.CircleMarker(
            location=[mid_lat, mid_lon],
            radius=3,
            color='#FF6B6B',
            fill=True,
            fill_color='#FF6B6B'
        ).add_to(mapa)
    
    # Añadir capa de control para cambiar entre diferentes mapas base
    folium.TileLayer('OpenStreetMap').add_to(mapa)
    folium.TileLayer('Stamen Terrain').add_to(mapa)
    folium.TileLayer('Stamen Toner').add_to(mapa)
    folium.LayerControl().add_to(mapa)
    
    return mapa

def generar_mapa_con_ruta_matplotlib(df_regiones, ruta, distancias=None):
    """
    Generar un mapa con la ruta resaltada usando Matplotlib
    """
    plt.figure(figsize=(10, 8))
    
    # Límites del mapa de Perú (ampliados un poco)
    min_lat, max_lat = -18.5, -0.0  # Sur a Norte
    min_lon, max_lon = -82.0, -68.0  # Oeste a Este
    
    # Fondo azul claro para el océano
    plt.fill_between([min_lon, max_lon], [min_lat, min_lat], [max_lat, max_lat], color='#ADD8E6')
    
    # Dibujar puntos para cada región
    for idx, region in df_regiones.iterrows():
        if region['region'] in ruta:
            if region['region'] == ruta[0]:
                # Origen: verde
                plt.plot(region['longitude'], region['latitude'], 'go', markersize=10)
            elif region['region'] == ruta[-1]:
                # Destino: rojo
                plt.plot(region['longitude'], region['latitude'], 'ro', markersize=10)
            else:
                # En la ruta: azul
                plt.plot(region['longitude'], region['latitude'], 'bo', markersize=8)
        else:
            # No está en la ruta: gris
            plt.plot(region['longitude'], region['latitude'], 'o', color='gray', markersize=6)
            
        plt.text(region['longitude']+0.2, region['latitude'], region['region'], 
                fontsize=8, ha='left', va='center')
    
    # Dibujar la ruta
    ruta_lons = []
    ruta_lats = []
    for region_nombre in ruta:
        region = df_regiones[df_regiones['region'] == region_nombre]
        ruta_lons.append(region['longitude'].values[0])
        ruta_lats.append(region['latitude'].values[0])
    
    plt.plot(ruta_lons, ruta_lats, 'r-', linewidth=2.5)
    
    # Añadir título y etiquetas
    plt.title(f'Ruta: {" → ".join(ruta)}', fontsize=14)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    
    # Establecer los límites del gráfico
    plt.xlim(min_lon, max_lon)
    plt.ylim(min_lat, max_lat)
    
    # Añadir cuadrícula
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Convertir el gráfico a una imagen
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Crear imagen desde los datos del buffer
    image = Image.open(buf)
    return image

def guardar_mapa(mapa, ruta_archivo):
    """
    Guardar el mapa en un archivo HTML
    
    Args:
        mapa: Mapa de folium a guardar
        ruta_archivo: Ruta del archivo donde guardar el mapa
    
    Returns:
        str: Ruta absoluta del archivo guardado
    """
    mapa.save(ruta_archivo)
    return os.path.abspath(ruta_archivo)

def convertir_pillow_a_qpixmap(image):
    """
    Convierte una imagen de Pillow a QPixmap para mostrarla en Qt
    """
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()
    
    # Convertir bytes a QImage
    qimg = QImage()
    qimg.loadFromData(byte_arr)
    
    # Convertir QImage a QPixmap
    return QPixmap.fromImage(qimg)
