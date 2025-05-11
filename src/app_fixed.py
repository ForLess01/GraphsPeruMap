import sys
import os
import pandas as pd
import networkx as nx
import folium
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFileDialog,
                             QSplitter, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class GraphsPeruMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar datos
        self.cargar_datos()
        
        # Configurar la interfaz gráfica
        self.init_ui()
        
    def cargar_datos(self):
        """Cargar datos de regiones y distancias"""
        try:
            # Rutas de los archivos de datos
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            
            regiones_path = os.path.join(parent_dir, 'data', 'regiones.csv')
            distancias_path = os.path.join(parent_dir, 'data', 'distancias.csv')
            
            # Cargar datos
            self.df_regiones = pd.read_csv(regiones_path)
            self.df_distancias = pd.read_csv(distancias_path)
            
            # Crear el grafo
            self.grafo = nx.Graph()
            
            # Añadir nodos (regiones)
            for idx, region in self.df_regiones.iterrows():
                self.grafo.add_node(region['region'], 
                                    lat=region['latitude'], 
                                    lon=region['longitude'])
            
            # Añadir aristas (conexiones entre regiones)
            for idx, ruta in self.df_distancias.iterrows():
                self.grafo.add_edge(ruta['origen'], ruta['destino'], 
                                    weight=ruta['distancia_km'])
            
            # Lista de regiones para los combobox
            self.regiones_list = list(self.df_regiones['region'])
            
        except Exception as e:
            QMessageBox.critical(self, "Error al cargar datos", f"No se pudieron cargar los datos: {str(e)}")
            sys.exit(1)
    
    def init_ui(self):
        """Inicializar la interfaz gráfica"""
        self.setWindowTitle('Rutas entre Regiones del Perú - Algoritmo de Dijkstra')
        self.setGeometry(100, 100, 1200, 800)
        
        # Estilo CSS para una apariencia más moderna
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333;
                padding: 5px 0px;
            }
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 200px;
                background: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                margin: 10px 0px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        
        # Layout principal
        main_layout = QHBoxLayout()
        
        # Panel izquierdo (controles)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        titulo_label = QLabel("Buscador de Rutas")
        titulo_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; padding: 5px 0px 15px 0px;")
        left_layout.addWidget(titulo_label)
        
        # Grupo: Selección de regiones
        seleccion_group = QGroupBox("Selección de Regiones")
        seleccion_layout = QVBoxLayout()
        
        # Origen
        origen_label = QLabel("Región de Origen:")
        self.origen_combo = QComboBox()
        self.origen_combo.addItems(sorted(self.regiones_list))
        self.origen_combo.setCurrentText("Lima")  # Por defecto: Lima
        
        # Destino
        destino_label = QLabel("Región de Destino:")
        self.destino_combo = QComboBox()
        self.destino_combo.addItems(sorted(self.regiones_list))
        self.destino_combo.setCurrentText("Cusco")  # Por defecto: Cusco
        
        # Añadir widgets al grupo de selección
        seleccion_layout.addWidget(origen_label)
        seleccion_layout.addWidget(self.origen_combo)
        seleccion_layout.addWidget(destino_label)
        seleccion_layout.addWidget(self.destino_combo)
        seleccion_group.setLayout(seleccion_layout)
        left_layout.addWidget(seleccion_group)
        
        # Botones de acción
        botones_widget = QWidget()
        botones_layout = QHBoxLayout(botones_widget)
        
        # Botón para calcular ruta
        calcular_btn = QPushButton("Calcular Ruta")
        calcular_btn.setIcon(QIcon.fromTheme("system-search"))
        calcular_btn.clicked.connect(self.calcular_ruta)
        
        # Botón para resetear el mapa
        reset_btn = QPushButton("Resetear")
        reset_btn.setStyleSheet("background-color: #f44336;")
        reset_btn.clicked.connect(self.generar_mapa_base)
        
        botones_layout.addWidget(calcular_btn)
        botones_layout.addWidget(reset_btn)
        left_layout.addWidget(botones_widget)
        
        # Grupo: Resultados
        resultados_group = QGroupBox("Información de la Ruta")
        resultados_layout = QVBoxLayout()
        
        # Información de la ruta
        self.info_resultado = QLabel("Selecciona origen y destino para ver la ruta")
        self.info_resultado.setWordWrap(True)
        self.info_resultado.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: normal;
        """)
        self.info_resultado.setMinimumHeight(200)
        
        resultados_layout.addWidget(self.info_resultado)
        resultados_group.setLayout(resultados_layout)
        left_layout.addWidget(resultados_group)
        
        # Información sobre el proyecto
        creditos_label = QLabel("Proyecto Rutas del Perú - Algoritmo Dijkstra")
        creditos_label.setStyleSheet("font-size: 10px; color: gray; padding: 10px 0px 0px 0px;")
        creditos_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(creditos_label)
        
        left_layout.addStretch()
        
        # Panel derecho (mapa)
        self.mapa_widget = QWebEngineView()
        
        # Splitter para ajustar tamaños
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.mapa_widget)
        splitter.setSizes([350, 850])
        
        main_layout.addWidget(splitter)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Generar mapa base
        self.generar_mapa_base()
    
    def generar_mapa_base(self):
        """Generar el mapa base de Perú"""
        from src.visualizacion import generar_mapa_base
        
        try:
            # Usar la función mejorada de visualización
            mapa = generar_mapa_base(self.df_regiones)
            
            # Guardar el mapa en HTML temporal
            temp_map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp_map.html')
            mapa.save(temp_map_path)
            
            # Cargar el mapa en el visor
            self.mapa_widget.load(Qt.QUrl.fromLocalFile(os.path.abspath(temp_map_path)))
            
            # Actualizar el mensaje de información
            self.info_resultado.setText("Selecciona origen y destino para calcular la ruta óptima utilizando el algoritmo de Dijkstra")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar el mapa base: {str(e)}")
    
    def calcular_ruta(self):
        """Calcular y mostrar la ruta utilizando el algoritmo de Dijkstra"""
        origen = self.origen_combo.currentText()
        destino = self.destino_combo.currentText()
        
        if origen == destino:
            QMessageBox.warning(self, "Error", "El origen y destino deben ser diferentes")
            return
        
        try:
            # Usar algoritmo de Dijkstra para encontrar el camino más corto
            ruta = nx.dijkstra_path(self.grafo, origen, destino, weight='weight')
            distancia = nx.dijkstra_path_length(self.grafo, origen, destino, weight='weight')
            
            # Obtener detalles de cada segmento de la ruta
            detalles_ruta = []
            distancias_segmentos = {}
            for i in range(len(ruta) - 1):
                origen_seg = ruta[i]
                destino_seg = ruta[i + 1]
                distancia_seg = self.grafo[origen_seg][destino_seg]['weight']
                detalles_ruta.append(f"{origen_seg} → {destino_seg}: {distancia_seg} km")
                distancias_segmentos[(origen_seg, destino_seg)] = distancia_seg
            
            # Mostrar información de la ruta
            info_texto = f"Distancia total: {distancia} km\n\n"
            info_texto += f"Ruta: {' → '.join(ruta)}\n\n"
            info_texto += "Detalles del recorrido:\n"
            info_texto += "\n".join(detalles_ruta)
            
            self.info_resultado.setText(info_texto)
            
            # Actualizar el mapa con la ruta
            self.mostrar_ruta_en_mapa(ruta, distancias_segmentos)
            
        except nx.NetworkXNoPath:
            QMessageBox.warning(self, "Error", "No existe un camino entre las regiones seleccionadas")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular la ruta: {str(e)}")
    
    def mostrar_ruta_en_mapa(self, ruta, distancias_segmentos=None):
        """Mostrar la ruta en el mapa utilizando el módulo de visualización"""
        from src.visualizacion import generar_mapa_con_ruta
        
        try:
            # Generar el mapa con la ruta usando la función mejorada
            mapa = generar_mapa_con_ruta(self.df_regiones, ruta, distancias_segmentos)
            
            # Guardar el mapa en HTML temporal
            temp_map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'temp_map.html')
            mapa.save(temp_map_path)
            
            # Cargar el mapa en el visor
            self.mapa_widget.load(Qt.QUrl.fromLocalFile(os.path.abspath(temp_map_path)))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar la ruta en el mapa: {str(e)}")


def main():
    app = QApplication(sys.argv)
    ex = GraphsPeruMapApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
