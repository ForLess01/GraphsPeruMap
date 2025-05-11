# Algoritmo de Dijkstra - Explicación Teórica

El algoritmo de Dijkstra es un algoritmo de búsqueda de caminos más cortos en un grafo con pesos no negativos, desarrollado por el científico de la computación Edsger W. Dijkstra en 1956 y publicado en 1959.

## Fundamentos Teóricos

El algoritmo de Dijkstra resuelve el problema del camino más corto desde un nodo origen a todos los demás nodos en un grafo con pesos positivos. Utiliza una estrategia voraz (greedy) para encontrar en cada paso el nodo con la distancia mínima acumulada.

### Conceptos Básicos

- **Grafo**: Estructura matemática que consiste en un conjunto de vértices (nodos) y un conjunto de aristas (conexiones entre nodos).
- **Arista ponderada**: Conexión entre dos nodos con un valor numérico asociado (distancia, tiempo, costo, etc.).
- **Camino**: Secuencia de nodos conectados por aristas.
- **Camino más corto**: Camino entre dos nodos tal que la suma de los pesos de las aristas que lo componen es mínima.

## El Algoritmo

### Idea Principal

1. Mantener un conjunto de nodos "visitados" y otro de "no visitados".
2. Para cada nodo, mantener la distancia mínima conocida desde el origen.
3. Inicialmente, asignar distancia infinita a todos los nodos excepto al origen (distancia 0).
4. En cada paso, seleccionar el nodo no visitado con la menor distancia acumulada.
5. Actualizar las distancias de los nodos adyacentes si se encuentra un camino más corto.
6. Repetir hasta que todos los nodos estén visitados o no haya caminos posibles.

### Pseudocódigo

```
función Dijkstra(Grafo, nodoOrigen):
    // Inicialización
    para cada nodo v en Grafo:
        distancia[v] = INFINITO
        visitado[v] = falso
        previo[v] = INDEFINIDO
    
    distancia[nodoOrigen] = 0
    
    // Algoritmo principal
    mientras existan nodos no visitados:
        u = nodo no visitado con menor distancia
        visitado[u] = verdadero
        
        para cada vecino v de u:
            // Relajación de aristas
            alt = distancia[u] + peso(u, v)
            si alt < distancia[v]:
                distancia[v] = alt
                previo[v] = u
    
    return distancia[], previo[]
```

### Reconstrucción del Camino

Para reconstruir el camino más corto desde el nodo origen hasta un nodo destino, se utiliza el arreglo `previo[]` que almacena el nodo anterior en el camino óptimo:

```
función ReconstruirCamino(previo[], destino):
    camino = lista vacía
    u = destino
    
    si previo[u] es indefinido:
        return "No existe camino"
    
    mientras u es definido:
        agregar u al principio de camino
        u = previo[u]
    
    return camino
```

## Complejidad Algorítmica

- **Tiempo**: O(V²) con una implementación básica o O(E + V log V) utilizando un montículo (heap).
- **Espacio**: O(V) para almacenar las distancias y los nodos previos.

Donde:
- V: número de vértices (nodos) en el grafo
- E: número de aristas en el grafo

## Aplicación en el Proyecto

En nuestro proyecto GraphsPeruMap:

1. Los nodos representan las 24 regiones del Perú y la provincia constitucional del Callao.
2. Las aristas representan las conexiones directas entre regiones.
3. Los pesos son las distancias en kilómetros entre las capitales de las regiones.
4. El algoritmo de Dijkstra encuentra la ruta más corta entre la región de origen y la de destino seleccionadas por el usuario.

El algoritmo se implementa mediante la biblioteca NetworkX de Python, que proporciona una implementación eficiente de Dijkstra con la función `nx.dijkstra_path()` y `nx.dijkstra_path_length()`.
