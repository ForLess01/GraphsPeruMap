# GraphsPeruMap - Rutas entre regiones del Perú

Este proyecto implementa un sistema de búsqueda de rutas entre las regiones del Perú utilizando la teoría de grafos y el algoritmo de Dijkstra para encontrar la ruta más corta.

## Características

- Visualización gráfica del mapa de Perú con sus 24 regiones y la provincia constitucional del Callao
- Implementación del algoritmo de Dijkstra para encontrar la ruta más corta entre dos regiones
- Cálculo de distancias en kilómetros entre las capitales de las regiones seleccionadas
- Interfaz gráfica intuitiva desarrollada con PyQt5
- Visualización de rutas en mapa interactivo mediante Folium
- **NUEVO**: Soporte para visualización dual - Folium (interactivo) y Matplotlib (estático)

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio o descargar los archivos:

```bash
git clone <url-del-repositorio>
cd GraphsPeruMap
```

2. Crear un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
```

3. Activar el entorno virtual:

En Windows:
```bash
.\venv\Scripts\activate
```

4. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Existen dos formas de ejecutar la aplicación:

### 1. Usando el script de ejecución (recomendado)

Simplemente ejecute el archivo batch incluido:

```bash
ejecutar_aplicacion.bat
```

Este script le permitirá elegir entre:

- **Versión Estándar** - Implementación original con visualización mediante Folium (puede tener problemas en algunos sistemas)
- **Versión Mejorada** - Implementación con soporte para visualización dual (Folium interactivo y Matplotlib estático)

### 2. Ejecutando directamente los archivos Python

Para ejecutar la versión estándar:
```bash
python src/app.py
```

Para ejecutar la versión mejorada:
```bash
python src/app_mejorada.py
```

## Estructura del Proyecto

```
GraphsPeruMap/
├── data/                   # Datos de regiones y distancias
│   ├── regiones.csv        # Información de las regiones (coordenadas)
│   └── distancias.csv      # Distancias entre regiones conectadas
├── resources/              # Recursos como imágenes, iconos, etc.
├── src/                    # Código fuente
│   ├── app.py              # Aplicación principal con la interfaz gráfica
│   ├── app_mejorada.py     # Versión mejorada con soporte para visualización dual
│   ├── dijkstra.py         # Implementación del algoritmo de Dijkstra
│   └── visualizacion.py    # Funciones para visualización en mapa
├── main.py                 # Punto de entrada principal
└── requirements.txt        # Dependencias del proyecto
```

## Cómo Usar

1. Ejecuta la aplicación
2. Selecciona la región de origen en la lista desplegable
3. Selecciona la región de destino en la lista desplegable
4. Haz clic en "Calcular Ruta"
5. La aplicación mostrará la ruta más corta en el mapa y los detalles de la distancia

## Modos de visualización

La versión mejorada ofrece dos modos de visualización:

### Matplotlib (Compatible)
- **Ventajas**: Mayor compatibilidad con diferentes sistemas y configuraciones
- **Características**: Visualización estática del mapa con las rutas marcadas
- **Recomendado para**: Usuarios con problemas en la visualización con Folium, sistemas sin soporte completo para Qt WebEngine

### Folium (Interactivo)
- **Ventajas**: Mapa interactivo con zoom y desplazamiento
- **Características**: Marcadores interactivos, popups con información detallada, opciones para cambiar el mapa base
- **Recomendado para**: Usuarios con soporte completo para Qt WebEngine

## Solución de problemas

Si experimenta problemas para visualizar el mapa interactivo (Folium), intente los siguientes pasos:

1. Asegúrese de tener instalado PyQt5 WebEngine:
```bash
pip install PyQt5-WebEngine
```

2. Si continúa teniendo problemas, seleccione el modo de visualización "Matplotlib" en la interfaz de la aplicación (solo disponible en la versión mejorada).

3. Si ninguno de los métodos funciona, verifique que todas las dependencias estén correctamente instaladas:
```bash
pip install -r requirements.txt
```

## Desarrollo

El proyecto está desarrollado en Python utilizando las siguientes bibliotecas principales:
- NetworkX: Para la implementación de grafos y algoritmos
- PyQt5: Para la interfaz gráfica de usuario
- Folium: Para la visualización de mapas interactivos
- Pandas: Para el manejo de datos

## Teoría de grafos aplicada

En este proyecto:
- Cada región es un nodo en el grafo
- Las conexiones entre regiones son aristas del grafo
- El peso de cada arista es la distancia en kilómetros entre las regiones
- El algoritmo de Dijkstra encuentra el camino de costo mínimo entre dos nodos