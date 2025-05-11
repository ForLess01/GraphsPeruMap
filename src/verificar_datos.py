import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main():
    # Rutas de los archivos de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    regiones_path = os.path.join(parent_dir, 'data', 'regiones.csv')
    distancias_path = os.path.join(parent_dir, 'data', 'distancias.csv')
    
    # Cargar datos
    df_regiones = pd.read_csv(regiones_path)
    df_distancias = pd.read_csv(distancias_path)
    
    print(f"Número de regiones: {len(df_regiones)}")
    print(f"Número de conexiones: {len(df_distancias)}")
    
    # Crear el grafo
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
    
    print(f"Número de nodos en el grafo: {grafo.number_of_nodes()}")
    print(f"Número de aristas en el grafo: {grafo.number_of_edges()}")
    
    # Verificar que el grafo esté conectado (todas las regiones tengan al menos una conexión)
    isolated_nodes = list(nx.isolates(grafo))
    if isolated_nodes:
        print(f"¡Advertencia! Las siguientes regiones no tienen conexiones: {isolated_nodes}")
    else:
        print("Todas las regiones tienen al menos una conexión.")
    
    # Verificar si el grafo es conexo (existe un camino entre cada par de nodos)
    if nx.is_connected(grafo):
        print("El grafo es conexo. Hay un camino entre cualquier par de regiones.")
    else:
        print("¡Advertencia! El grafo no es conexo.")
        componentes = list(nx.connected_components(grafo))
        print(f"Hay {len(componentes)} componentes conexas:")
        for i, comp in enumerate(componentes, 1):
            print(f"Componente {i}: {list(comp)}")
    
    # Probar el algoritmo de Dijkstra con un par de regiones
    origen = "Lima"
    destino = "Cusco"
    try:
        ruta = nx.dijkstra_path(grafo, origen, destino, weight='weight')
        distancia = nx.dijkstra_path_length(grafo, origen, destino, weight='weight')
        print(f"\nRuta más corta de {origen} a {destino}:")
        print(f"Distancia: {distancia} km")
        print(f"Ruta: {' -> '.join(ruta)}")
    except nx.NetworkXNoPath:
        print(f"No existe un camino entre {origen} y {destino}")
    except Exception as e:
        print(f"Error al calcular la ruta: {str(e)}")
    
    # Visualizar el grafo (versión muy básica)
    plt.figure(figsize=(10, 8))
    pos = {node: (grafo.nodes[node]['lon'], grafo.nodes[node]['lat']) for node in grafo.nodes()}
    nx.draw(grafo, pos, with_labels=True, node_size=300, node_color="skyblue")
    plt.title("Grafo de Regiones del Perú")
    plt.savefig("grafo_peru.png")
    print("\nSe ha guardado una visualización básica del grafo como 'grafo_peru.png'")

if __name__ == "__main__":
    main()
