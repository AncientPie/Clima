import requests
import tkinter as tk
from tkinter import messagebox
import emoji

def obtener_clima(ciudad, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}"
    try:
        response = requests.get(url)
        datos = response.json()

        temperatura = datos['main']['temp'] - 273.15  # Convertir de Kelvin a Celsius
        sensacion_termica = datos['main']['feels_like'] - 273.15
        temp_min = datos['main']['temp_min'] - 273.15
        temp_max = datos['main']['temp_max'] - 273.15
        presion_hpa = datos['main']['pressure']
        presion_atm = presion_hpa / 1013.25  # Convertir de hPa a atm
        humedad = datos['main']['humidity']
        descripcion_clima = datos['weather'][0]['description']
        pais = datos['sys']['country']
        ciudad = datos['name']
        timezone = datos['timezone'] / 3600  # Convertir de segundos a horas

        emoji_clima = obtener_emoji_por_clima(descripcion_clima)

        resultado = (
            f"Temperatura en {ciudad}, {pais}: {temperatura:.2f} °C\n"
            f"Sensación térmica: {sensacion_termica:.2f} °C\n"
            f"Temperatura Mínima: {temp_min:.2f} °C\n"
            f"Temperatura Máxima: {temp_max:.2f} °C\n"
            f"Presión: {presion_atm:.4f} atm\n"
            f"Humedad: {humedad}%\n"
            f"Condiciones: {descripcion_clima} {emoji_clima}\n"
            f"Zona horaria: UTC{timezone:+.2f}\n"
        )

        return resultado
    except Exception as e:
        return f"No se pudo obtener el clima. Error: {e}"

def obtener_emoji_por_clima(descripcion_clima):
    emojis = {
        'few clouds': ':cloud:',
        'clear sky': ':sun:',
        'scattered clouds': ':sun_behind_small_cloud:',
        'broken clouds': ':sun_behind_rain_cloud:',
        'shower rain': ':cloud_with_rain:',
        'rain': ':umbrella_with_rain_drops:',
        'thunderstorm': ':cloud_with_lightning:',
        'snow': ':snowflake:',
        'mist': ':fog:',
        'overcast clouds': ':sun_behind_large_cloud:'
    }
    return emoji.emojize(emojis.get(descripcion_clima, ':question:'))

def mostrar_clima():
    ciudad = ciudad_entry.get()
    resultado = obtener_clima(ciudad, api_key)
    messagebox.showinfo("Clima Actual", resultado)
api_key = 'bc3e5a6a6cbcf6e0fd495c8e49d2689c'

app = tk.Tk()
app.title("Clima en Tiempo Real")
app.geometry("1000x800")

ciudad_label = tk.Label(app, text="Ingrese la ciudad:")
ciudad_label.pack(pady=10)

ciudad_entry = tk.Entry(app)
ciudad_entry.pack(pady=10)

obtener_clima_button = tk.Button(app, text="Obtener Clima", command=mostrar_clima)
obtener_clima_button.pack(pady=20)

app.mainloop()
