#import namespace necesarias para este proyecto

app = Flask(__name__)
#agrega los servidores disponibles
MIRRORS = []
def rb_get(path, params=None):
    """Obtiene datos desde un mirror válido de RadioBrowser"""
    for mirror in MIRRORS:
        try:
            url = f"https://{mirror}.api.radio-browser.info/json{path}"
            r = requests.get(url, params=params, headers={"Accept": "application/json"}, timeout=10)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return []
#Sobrecargar la funcion index para agregar el nombre del desarrollador por parametro
#ruta -> /dev/<nmbre_dev>
@app.route("/")
def index():
    # Agregar los tags más comunes a tu preferencia
    tags = []
    tag_stations = {}
    for tag in tags:
        data = rb_get("/stations/search", {"tag": tag, "limit": 4, "hidebroken": "true"})
        tag_stations[tag.capitalize()] = data
    #enviar el nombre del dev por parametro para consumir por HTML
    return render_template("index.html", tag_stations=tag_stations)

if __name__ == "__main__":
    app.run(debug=True)
