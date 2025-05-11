@echo off
echo Corrigiendo el problema de visualizacion del mapa...
echo.

echo Actualizando archivos de visualizacion...

pushd %~dp0
@echo import folium > src\fix_visualizacion.py
@echo import os >> src\fix_visualizacion.py
@echo import pandas as pd >> src\fix_visualizacion.py
@echo from folium.plugins import MeasureControl >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo # Abrir y leer el archivo de visualizacion original >> src\fix_visualizacion.py
@echo with open('src/visualizacion.py', 'r', encoding='utf-8') as f: >> src\fix_visualizacion.py
@echo     content = f.read() >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo # Reemplazar la creacion del mapa sin atribuciones con una version con atribuciones >> src\fix_visualizacion.py
@echo new_content = content.replace('mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', >> src\fix_visualizacion.py
@echo                             'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> &copy; <a href=\'http://cartodb.com/attributions\'>CartoDB</a>")') >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo # Reemplazar las capas adicionales sin atribuciones >> src\fix_visualizacion.py
@echo new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                "folium.TileLayer('OpenStreetMap', attr='&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo # Guardar el archivo modificado >> src\fix_visualizacion.py
@echo with open('src/visualizacion.py', 'w', encoding='utf-8') as f: >> src\fix_visualizacion.py
@echo     f.write(new_content) >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo # Realizar el mismo proceso para visualizacion_mejorada.py si existe >> src\fix_visualizacion.py
@echo try: >> src\fix_visualizacion.py
@echo     with open('src/visualizacion_mejorada.py', 'r', encoding='utf-8') as f: >> src\fix_visualizacion.py
@echo         content = f.read() >> src\fix_visualizacion.py
@echo     # Reemplazar la creacion del mapa sin atribuciones con una version con atribuciones >> src\fix_visualizacion.py
@echo     new_content = content.replace('mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron")', >> src\fix_visualizacion.py
@echo                               'mapa = folium.Map(location=peru_center, zoom_start=6, tiles="CartoDB positron", attr="&copy; <a href=\'http://www.openstreetmap.org/copyright\'>OpenStreetMap</a> &copy; <a href=\'http://cartodb.com/attributions\'>CartoDB</a>")') >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo     # Reemplazar las capas adicionales sin atribuciones >> src\fix_visualizacion.py
@echo     new_content = new_content.replace("folium.TileLayer('OpenStreetMap').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                  "folium.TileLayer('OpenStreetMap', attr='&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo     new_content = new_content.replace("folium.TileLayer('Stamen Terrain').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                  "folium.TileLayer('Stamen Terrain', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo     new_content = new_content.replace("folium.TileLayer('Stamen Toner').add_to(mapa)", >> src\fix_visualizacion.py
@echo                                  "folium.TileLayer('Stamen Toner', attr='Map tiles by <a href=\"http://stamen.com\">Stamen Design</a>, <a href=\"http://creativecommons.org/licenses/by/3.0\">CC BY 3.0</a> &mdash; Map data &copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a> contributors').add_to(mapa)") >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo     # Guardar el archivo modificado >> src\fix_visualizacion.py
@echo     with open('src/visualizacion_mejorada.py', 'w', encoding='utf-8') as f: >> src\fix_visualizacion.py
@echo         f.write(new_content) >> src\fix_visualizacion.py
@echo     print("Se ha corregido el archivo visualizacion_mejorada.py") >> src\fix_visualizacion.py
@echo except FileNotFoundError: >> src\fix_visualizacion.py
@echo     print("El archivo visualizacion_mejorada.py no existe, no se realizaron cambios en él") >> src\fix_visualizacion.py
@echo. >> src\fix_visualizacion.py
@echo print("¡Archivos de visualizacion corregidos exitosamente!") >> src\fix_visualizacion.py

python src\fix_visualizacion.py

echo.
echo Los archivos de visualizacion han sido corregidos.
echo Ahora la aplicacion deberia funcionar correctamente.
echo.
echo Presiona cualquier tecla para ejecutar la aplicacion mejorada...
pause > nul

echo Ejecutando aplicacion...
python src/app_mejorada.py

popd