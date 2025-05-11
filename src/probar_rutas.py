import os
import pandas as pd
import networkx as nx

def main():
    # Rutas de los archivos de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    regiones_path = os.path.join(parent_dir, 'data', 'regiones.csv')
    distancias_path = os.path.join(parent_dir, 'data', 'distancias.csv')
    
    # Cargar datos
    df_regiones = pd.read_csv(regiones_path)
    df_distancias = pd.read_csv(distancias_path)
    
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
    
    # Lista de pruebas origen-destino
    pruebas = [
        ("Lima", "Cusco"),
        ("Lima", "Tacna"),
        ("Lima", "Loreto"),
        ("Tacna", "Tumbes"),
        ("Cusco", "Piura"),
        ("Callao", "Puno")
    ]
    
    # Realizar pruebas
    print("Pruebas de rutas entre regiones:")
    print("=" * 50)
    
    for origen, destino in pruebas:
        try:
            ruta = nx.dijkstra_path(grafo, origen, destino, weight='weight')
            distancia = nx.dijkstra_path_length(grafo, origen, destino, weight='weight')
            print(f"\nRuta más corta de {origen} a {destino}:")
            print(f"Distancia: {distancia} km")
            print(f"Ruta: {' -> '.join(ruta)}")
            
            # Mostrar detalles de cada segmento de la ruta
            print("\nDetalles de la ruta:")
            for i in range(len(ruta) - 1):
                tramo_origen = ruta[i]
                tramo_destino = ruta[i + 1]
                tramo_distancia = grafo[tramo_origen][tramo_destino]['weight']
                print(f"  {tramo_origen} -> {tramo_destino}: {tramo_distancia} km")
            
        except nx.NetworkXNoPath:
            print(f"\nNo existe un camino entre {origen} y {destino}")
        except Exception as e:
            print(f"\nError al calcular la ruta de {origen} a {destino}: {str(e)}")

if __name__ == "__main__":
    main()
