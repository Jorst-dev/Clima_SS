from flask import Flask, render_template
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Reemplaza esta API key con una válida de OpenWeatherMap
API_KEY = "2f333ff0323e14fb922f71b9c4a92f2f"

def clima_actual(ciudad):
    """Obtiene información del clima actual de una ciudad"""
    if not API_KEY or API_KEY == "TU_API_KEY_AQUI":
        return None
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    try:
        response = requests.get(url)
        if response.status_code == 401:
            return None
        response.raise_for_status()
        return response.json()
    except:
        return None

def obtener_icono_clima(descripcion):
    """Mapea descripciones del clima a iconos de Bootstrap"""
    iconos = {
        'clear sky': 'bi-sun-fill',
        'few clouds': 'bi-cloud-sun-fill',
        'scattered clouds': 'bi-cloud-fill',
        'broken clouds': 'bi-clouds-fill',
        'shower rain': 'bi-cloud-rain-fill',
        'rain': 'bi-cloud-rain-fill',
        'thunderstorm': 'bi-lightning-fill',
        'snow': 'bi-snow',
        'mist': 'bi-cloud-fog-fill',
        'fog': 'bi-cloud-fog-fill',
        'haze': 'bi-cloud-fog-fill',
        'smoke': 'bi-cloud-fog-fill',
        'dust': 'bi-cloud-fog-fill',
        'sand': 'bi-cloud-fog-fill',
        'ash': 'bi-cloud-fog-fill',
        'squall': 'bi-wind',
        'tornado': 'bi-tornado'
    }
    
    desc_lower = descripcion.lower()
    for key, icon in iconos.items():
        if key in desc_lower:
            return icon
    return 'bi-cloud-fill'  # Icono por defecto

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
