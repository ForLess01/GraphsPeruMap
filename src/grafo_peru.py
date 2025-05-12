import networkx as nx
import pandas as pd
import os

def cargar_datos():
    """
    Cargar datos de regiones y distancias desde los archivos CSV
    
    Returns:
        tuple: (df_regiones, df_distancias, grafo) donde:
            - df_regiones: DataFrame con información de las regiones
            - df_distancias: DataFrame con las distancias entre regiones
            - grafo: Grafo de NetworkX con las regiones y distancias
    """
    try:
        # Rutas de los archivos de datos
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        regiones_path = os.path.join(parent_dir, 'data', 'regiones.csv')
        
        # Intentar usar el archivo enriquecido si existe, si no usar el básico
        distancias_enriquecido_path = os.path.join(parent_dir, 'data', 'distancias_regionales_peru_enriquecido.csv')
        distancias_path = os.path.join(parent_dir, 'data', 'distancias.csv')
        
        # Cargar datos de regiones
        df_regiones = pd.read_csv(regiones_path)
        
        # Determinar qué archivo de distancias usar
        if os.path.exists(distancias_enriquecido_path):
            df_distancias = pd.read_csv(distancias_enriquecido_path)
            usar_enriquecido = True
        else:
            df_distancias = pd.read_csv(distancias_path)
            usar_enriquecido = False
            
        # Crear el grafo
        grafo = crear_grafo(df_regiones, df_distancias, usar_enriquecido)
        
        return df_regiones, df_distancias, grafo
        
    except Exception as e:
        raise Exception(f"Error al cargar datos: {str(e)}")

def crear_grafo(df_regiones, df_distancias, usar_enriquecido=False):
    """
    Crear un grafo de NetworkX con las regiones y distancias
    
    Args:
        df_regiones: DataFrame con información de las regiones
        df_distancias: DataFrame con las distancias entre regiones
        usar_enriquecido: Si es True, usar columnas de región_origen y región_destino
    
    Returns:
        networkx.Graph: Grafo con las regiones y distancias
    """
    grafo = nx.Graph()
    
    # Añadir nodos (regiones)
    for idx, region in df_regiones.iterrows():
        grafo.add_node(region['region'], 
                      lat=region['latitude'], 
                      lon=region['longitude'])
    
    # Añadir aristas (conexiones entre regiones)
    for idx, ruta in df_distancias.iterrows():
        origen = ruta['origen']
        destino = ruta['destino']
        
        # Si estamos usando el dataset enriquecido, podemos verificar adyacencia
        if usar_enriquecido:
            region_origen = ruta['region_origen'] 
            region_destino = ruta['region_destino']
            grafo.add_edge(origen, destino, 
                         weight=ruta['distancia_km'],
                         region_origen=region_origen,
                         region_destino=region_destino)
        else:
            grafo.add_edge(origen, destino, 
                         weight=ruta['distancia_km'])
    
    return grafo

def son_adyacentes(df_distancias, origen, destino):
    """
    Verificar si dos regiones son adyacentes geográficamente
    
    Args:
        df_distancias: DataFrame con las distancias entre regiones
        origen: Nombre de la región de origen
        destino: Nombre de la región de destino
    
    Returns:
        bool: True si son adyacentes, False en caso contrario
    """
    # Implementación básica: Verificar si hay una entrada directa en el DataFrame
    filtro = ((df_distancias['origen'] == origen) & (df_distancias['destino'] == destino)) | \
             ((df_distancias['origen'] == destino) & (df_distancias['destino'] == origen))
    
    return filtro.any()

def encontrar_ruta_mas_corta(grafo, origen, destino, solo_adyacentes=False):
    """
    Encontrar la ruta más corta entre dos regiones utilizando el algoritmo de Dijkstra
    
    Args:
        grafo: Grafo con las regiones y distancias
        origen: Región de origen
        destino: Región de destino
        solo_adyacentes: Si es True, verificar que todas las regiones en la ruta sean adyacentes
    
    Returns:
        tuple: (ruta, distancia) donde ruta es una lista de regiones y distancia es el valor en km
    """
    try:
        # Usar algoritmo de Dijkstra para encontrar el camino más corto
        ruta = nx.dijkstra_path(grafo, origen, destino, weight='weight')
        distancia = nx.dijkstra_path_length(grafo, origen, destino, weight='weight')
        
        # Verificar adyacencia si se solicita
        if solo_adyacentes:
            for i in range(len(ruta) - 1):
                region_actual = ruta[i]
                siguiente_region = ruta[i + 1]
                
                # Verificar si las regiones son adyacentes en el grafo
                if not grafo.has_edge(region_actual, siguiente_region):
                    return None, 0
                
                # Si tenemos información enriquecida, podríamos hacer más verificaciones aquí
        
        return ruta, distancia
    except nx.NetworkXNoPath:
        return None, 0
    except Exception as e:
        raise e

def obtener_detalles_ruta(grafo, ruta):
    """
    Obtener los detalles de cada segmento de la ruta
    
    Args:
        grafo: Grafo con las regiones y distancias
        ruta: Lista de regiones en la ruta
    
    Returns:
        dict: Diccionario con detalles de cada segmento de la ruta y distancias
    """
    detalles = []
    distancias_segmentos = {}
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        distancia = grafo[origen][destino]['weight']
        
        detalles.append({
            'origen': origen,
            'destino': destino,
            'distancia_km': distancia
        })
        
        # También guardar las distancias en un formato más simple para la visualización
        distancias_segmentos[(origen, destino)] = distancia
    
    return {
        'detalles': detalles,
        'distancias_segmentos': distancias_segmentos
    }

def verificar_integridad_grafo(grafo):
    """
    Verificar la integridad del grafo: conexidad, aislamiento de nodos, etc.
    
    Args:
        grafo: Grafo de NetworkX a verificar
    
    Returns:
        dict: Diccionario con información de la verificación
    """
    resultado = {
        'es_conexo': nx.is_connected(grafo),
        'num_nodos': grafo.number_of_nodes(),
        'num_aristas': grafo.number_of_edges(),
        'nodos_aislados': list(nx.isolates(grafo)),
        'componentes_conexas': list(nx.connected_components(grafo))
    }
    
    # Convertir componentes_conexas a lista de listas para que sea JSON serializable
    resultado['componentes_conexas'] = [list(comp) for comp in resultado['componentes_conexas']]
    
    return resultado
