

## 📁 Estructura del proyecto
```
radio_app/
│
├── LogicaBackend.py
├── app.py
├── static/
│   └── styles.css
└── templates/
    └── index.html
├── requirements.txt
├── respuesta.json
├── tags.json
```
### Instrucciones
## PARTE 1 - FLASK
Completar los siguientes requerimientos en el proyecto
1.  Probar los siguientes puntos de conexion en Postman: 
    1. Por Pais
    [METODO GET](https://de1.api.radio-browser.info/json/stations/bycountry/Bolivia?limit=10&hidebroken=true)

    https://de1.api.radio-browser.info/json/stations/bycountry/Bolivia?limit=10&hidebroken=true

    2. Por Categoria
    [METODO GET](https://de1.api.radio-browser.info/json/stations/search?tag=rock&limit=10&hidebroken=true)

    https://de1.api.radio-browser.info/json/stations/search?tag=rock&limit=10&hidebroken=true
2. Clonar el repositorio radio_app
3. Crear tu entorno virtual
4. Crear tu archivo requirements.txt con las siguientes librerias.
```
Flask
requests
```
5. En el archivo app.py agregar la logica que menciona los comentarios.
6. En el archivo index.html agregar la logica que menciona los comentarios.
7. Cambiar la paleta de colores del archivo style.css
## RESULTADO FINAL
![Resultado Final.](/resultado.png "")
![Resultado Final adjunto.](/resultado2.png "")

## PARTE 2 - PYODBC
8. Crear tu base de datos en el gestor de tu preferencia.
9. Crear tu archivo conexion_db.py y realizar la conexion de tu base de datos mediante pyodbc
10. Crear un CRUD mediante los cursor necesarios.
