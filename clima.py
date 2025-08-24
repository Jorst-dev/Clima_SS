from flask import Flask, render_template, request, jsonify
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

@app.route('/buscar_clima', methods=['POST'])
def buscar_clima():
    ciudad = request.form.get('ciudad', '').strip()
    
    if not ciudad:
        return jsonify({'error': 'Por favor ingresa el nombre de una ciudad'})
    
    clima = clima_actual(ciudad)
    
    if clima is None:
        return jsonify({'error': 'No se pudo obtener información del clima. Verifica tu API key o intenta con otra ciudad.'})
    
    if clima.get("cod") != 200:
        return jsonify({'error': f'Ciudad no encontrada: {clima.get("message", "Error desconocido")}'})
    
    # Procesar datos del clima
    datos_clima = {
        'ciudad': clima['name'],
        'pais': clima['sys']['country'],
        'descripcion': clima['weather'][0]['description'].title(),
        'temperatura': round(clima['main']['temp']),
        'sensacion_termica': round(clima['main']['feels_like']),
        'humedad': clima['main']['humidity'],
        'presion': clima['main']['pressure'],
        'viento_velocidad': clima['wind'].get('speed', 0),
        'viento_direccion': clima['wind'].get('deg', 0),
        'visibilidad': round(clima.get('visibility', 0) / 1000, 1) if clima.get('visibility') else 0,
        'icono': obtener_icono_clima(clima['weather'][0]['description']),
        'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'temp_min': round(clima['main']['temp_min']),
        'temp_max': round(clima['main']['temp_max'])
    }
    
    return jsonify(datos_clima)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)