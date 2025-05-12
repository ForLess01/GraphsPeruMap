# GraphsPeruMap - Rutas entre regiones del Perú (Versión Consolidada)

Este proyecto implementa un sistema de búsqueda de rutas entre las regiones del Perú utilizando la teoría de grafos y el algoritmo de Dijkstra para encontrar la ruta más corta.

## Características Principales

- Visualización gráfica del mapa de Perú con sus regiones y la provincia constitucional del Callao
- Implementación del algoritmo de Dijkstra para encontrar la ruta más corta entre dos regiones
- Cálculo de distancias en kilómetros entre las capitales de las regiones seleccionadas
- Interfaz gráfica intuitiva desarrollada con PyQt5
- Visualización dual: interactiva con Folium o estática con Matplotlib
- Soporte para restricciones de adyacencia física entre regiones

## Mejoras en la Versión Consolidada

- Código modular y mantenible separado en módulos especializados
- Soporte para detección de regiones físicamente adyacentes
- Visualización mejorada de rutas con colores para mostrar dirección
- Corrección de errores conocidos con Folium y sus atribuciones
- Unificación de las versiones anteriores en una sola aplicación mejorada

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`:
  - networkx
  - matplotlib
  - folium
  - pandas
  - PyQt5
  - PyQtWebEngine
  - Pillow
  - geopandas
  - shapely

## Instalación

1. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

### Método 1: Script de ejecución

Simplemente ejecute el archivo batch incluido:

```bash
ejecutar_consolidado.bat
```

### Método 2: Ejecución directa

```bash
python main_consolidado.py
```

## Estructura del Proyecto

```
GraphsPeruMap/
├── data/                           # Datos de regiones y distancias
│   ├── regiones.csv                # Información de las regiones (coordenadas)
│   ├── distancias.csv              # Distancias entre regiones básicas
│   └── distancias_regionales_peru_enriquecido.csv  # Distancias con información de regiones
├── src/                            # Código fuente
│   ├── app_consolidada.py          # Aplicación principal con la interfaz gráfica
│   ├── grafo_peru.py               # Funciones para manejar el grafo y algoritmo de Dijkstra
│   └── visualizacion_consolidada.py # Funciones para visualización en mapa
├── main_consolidado.py             # Punto de entrada principal
├── ejecutar_consolidado.bat        # Script para ejecutar la aplicación
└── requirements.txt                # Dependencias del proyecto
```

## Cómo Usar

1. Seleccione el **Método de Visualización** preferido:
   - **Matplotlib (Compatible)**: Mapa estático, mejor compatibilidad
   - **Folium (Interactivo)**: Mapa interactivo, requiere soporte para WebEngine

2. Decida si desea utilizar la opción **"Solo considerar regiones adyacentes"**:
   - **Activado**: Solo permite rutas entre regiones que comparten fronteras físicas
   - **Desactivado**: Permite cualquier ruta entre regiones, aunque no sean adyacentes

3. Seleccione la **Región de Origen** y **Región de Destino** entre las que desea encontrar la ruta.

4. Haga clic en **Calcular Ruta** para encontrar la ruta más corta entre las regiones seleccionadas.

5. El resultado se mostrará tanto en el mapa como en el panel de información.

## Solución de problemas

Si experimenta problemas para visualizar el mapa interactivo (Folium), intente los siguientes pasos:

1. Seleccione el modo de visualización "Matplotlib (Compatible)" en la interfaz.

2. Asegúrese de tener instalado PyQt5 WebEngine:
```bash
pip install PyQt5-WebEngine
```

3. Verifique que todas las dependencias estén correctamente instaladas:
```bash
pip install -r requirements.txt
```

## Teoría de grafos aplicada

En este proyecto:
- Cada región es un nodo en el grafo
- Las conexiones entre regiones son aristas del grafo
- El peso de cada arista es la distancia en kilómetros entre las regiones
- El algoritmo de Dijkstra encuentra el camino de costo mínimo entre dos nodos
- La opción de adyacencia restringe las rutas a regiones que comparten fronteras
