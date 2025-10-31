# pip install requests
import requests

MIRRORS = ["de1", "nl1", "us1", "gb1", "at1"]
TIMEOUT = 10

def rb_get(path, params=None):
    """Intenta contra varios mirrors hasta obtener 200 OK."""
    last_err = None
    for mirror in MIRRORS:
        url = f"https://{mirror}.api.radio-browser.info/json{path}"
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT, headers={"Accept":"application/json"})
            if r.status_code == 200:
                return r.json()
            last_err = f"{r.status_code} {r.text[:200]}"
        except Exception as e:
            last_err = str(e)
    raise RuntimeError(f"RadioBrowser fallo en todos los mirrors. Último error: {last_err}")

def search_by_country(country, limit=10, hidebroken=True):
    return rb_get("/stations/bycountry/" + requests.utils.quote(country),
                  params={"limit": limit, "hidebroken": str(hidebroken).lower()})

def search_by_tag(tag, limit=10, hidebroken=True):
    return rb_get("/stations/search",
                  params={"tag": tag, "limit": limit, "hidebroken": str(hidebroken).lower()})

def pick_stream(station):
    """Devuelve la URL 'buena' del stream."""
    return station.get("url_resolved") or station.get("url")

if __name__ == "__main__":
    # Ejemplo 1: por país (Bolivia)
    stations = search_by_country("Bolivia", limit=10)
    for i, st in enumerate(stations, start=1):
        print(f"{i:02d}. {st['name']}  |  {st.get('country')}  |  {st.get('tags')}")
        print("    stream:", pick_stream(st))
        print("    favicon:", st.get("favicon"))
        print("    stationuuid:", st.get("stationuuid"))
        print()

    # Ejemplo 2: por tag (rock)
    rock = search_by_tag("rock", limit=5)
    print(f"Rock top 5 (ocurre {len(rock)} resultados):")
    for st in rock:
        print("-", st["name"], "->", pick_stream(st))
