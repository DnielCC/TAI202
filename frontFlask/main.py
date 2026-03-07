from flask import Flask 
import requests

app = Flask(__name__)

@app.route('/ver-datos')
def mostrar_api():
    
    respuesta = requests.get('http://api:5000/token')
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return f"Datos traídos de la API: {datos}"
    return "No se pudo conectar con la API", 500


if __name__ == '__main__':
    app.run(port=8080,debug=True)
