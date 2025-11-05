"""
aplicacion_radio.py - Aplicación completa de Radio Browser
Este archivo combina la lógica del backend con la aplicación Flask
para proporcionar una interfaz web completa para explorar estaciones de radio.
"""

from flask import Flask, render_template
import requests

# Configuración de la aplicación Flask
app = Flask(__name__)

# Lista de servidores mirror disponibles para Radio Browser API
MIRRORS = ["de1", "nl1", "us1", "gb1", "at1"]
TIMEOUT = 10

def rb_get(path, params=None):
    """
    Intenta obtener datos desde varios mirrors de Radio Browser hasta obtener una respuesta exitosa.
    
    Args:
        path: Ruta del endpoint de la API (ejemplo: "/stations/search")
        params: Parámetros de consulta opcionales
        
    Returns:
        JSON con los datos obtenidos o lista vacía si todos los mirrors fallan
    """
    for mirror in MIRRORS:
        try:
            url = f"https://{mirror}.api.radio-browser.info/json{path}"
            r = requests.get(url, params=params, headers={"Accept": "application/json"}, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return []

def search_by_country(country, limit=10, hidebroken=True):
    """
    Busca estaciones de radio por país.
    
    Args:
        country: Nombre del país
        limit: Número máximo de resultados
        hidebroken: Si es True, oculta estaciones rotas
        
    Returns:
        Lista de estaciones encontradas
    """
    return rb_get(f"/stations/bycountry/{requests.utils.quote(country)}",
                  params={"limit": limit, "hidebroken": str(hidebroken).lower()})

def search_by_tag(tag, limit=10, hidebroken=True):
    """
    Busca estaciones de radio por etiqueta/género.
    
    Args:
        tag: Etiqueta o género musical
        limit: Número máximo de resultados
        hidebroken: Si es True, oculta estaciones rotas
        
    Returns:
        Lista de estaciones encontradas
    """
    return rb_get("/stations/search",
                  params={"tag": tag, "limit": limit, "hidebroken": str(hidebroken).lower()})

def pick_stream(station):
    """
    Devuelve la URL 'buena' del stream de una estación.
    
    Args:
        station: Diccionario con datos de la estación
        
    Returns:
        URL del stream de la estación
    """
    return station.get("url_resolved") or station.get("url")

# Rutas de Flask

@app.route("/dev/<nombre_dev>")
def index_dev(nombre_dev):
    """
    Ruta principal con nombre de desarrollador personalizado.
    
    Args:
        nombre_dev: Nombre del desarrollador a mostrar
        
    Returns:
        Renderiza la página principal con estaciones agrupadas por género
    """
    # Tags más comunes para mostrar
    tags = ["rock", "pop", "jazz", "classical"]
    tag_stations = {}
    
    # Obtener estaciones para cada tag
    for tag in tags:
        data = rb_get("/stations/search", {"tag": tag, "limit": 4, "hidebroken": "true"})
        tag_stations[tag.capitalize()] = data
    
    return render_template("index.html", tag_stations=tag_stations, developer=nombre_dev)

@app.route("/")
def index():
    """
    Ruta principal de la aplicación.
    
    Returns:
        Renderiza la página principal con estaciones agrupadas por género
    """
    # Tags más comunes para mostrar
    tags = ["rock", "pop", "jazz", "classical"]
    tag_stations = {}
    
    # Obtener estaciones para cada tag
    for tag in tags:
        data = rb_get("/stations/search", {"tag": tag, "limit": 4, "hidebroken": "true"})
        tag_stations[tag.capitalize()] = data
    
    return render_template("index.html", tag_stations=tag_stations, developer="Desarrollador")

@app.route("/country/<country_name>")
def stations_by_country(country_name):
    """
    Ruta para buscar estaciones por país.
    
    Args:
        country_name: Nombre del país
        
    Returns:
        Renderiza una página con estaciones del país especificado
    """
    stations = search_by_country(country_name, limit=20)
    return render_template("index.html", 
                         tag_stations={"Estaciones de " + country_name: stations}, 
                         developer="Desarrollador")

@app.route("/tag/<tag_name>")
def stations_by_tag(tag_name):
    """
    Ruta para buscar estaciones por etiqueta.
    
    Args:
        tag_name: Nombre de la etiqueta/género
        
    Returns:
        Renderiza una página con estaciones de la etiqueta especificada
    """
    stations = search_by_tag(tag_name, limit=20)
    return render_template("index.html", 
                         tag_stations={tag_name.capitalize(): stations}, 
                         developer="Desarrollador")

if __name__ == "__main__":
    # Iniciar el servidor de desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
