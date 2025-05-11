import networkx as nx

def crear_grafo_peru(df_regiones, df_distancias):
    """
    Crear un grafo de las regiones de Perú
    
    Args:
        df_regiones: DataFrame con información de las regiones
        df_distancias: DataFrame con las distancias entre regiones
    
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
        grafo.add_edge(ruta['origen'], ruta['destino'], 
                      weight=ruta['distancia_km'])
    
    return grafo

def encontrar_ruta_mas_corta(grafo, origen, destino):
    """
    Encontrar la ruta más corta entre dos regiones utilizando el algoritmo de Dijkstra
    
    Args:
        grafo: Grafo con las regiones y distancias
        origen: Región de origen
        destino: Región de destino
    
    Returns:
        tuple: (ruta, distancia) donde ruta es una lista de regiones y distancia es el valor en km
    """
    try:
        # Usar algoritmo de Dijkstra para encontrar el camino más corto
        ruta = nx.dijkstra_path(grafo, origen, destino, weight='weight')
        distancia = nx.dijkstra_path_length(grafo, origen, destino, weight='weight')
        
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
        list: Lista de diccionarios con los detalles de cada segmento
    """
    detalles = []
    
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i + 1]
        distancia = grafo[origen][destino]['weight']
        
        detalles.append({
            'origen': origen,
            'destino': destino,
            'distancia_km': distancia
        })
    
    return detalles
