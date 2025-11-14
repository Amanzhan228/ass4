from prometheus_client import start_http_server, Gauge
import requests
import time

# === API CONFIG ===
CITY = "Astana"
API_KEY = "1d43e377474f167396434961a32efe95"  # вставь свой OpenWeather API ключ
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# === METRICS ===
temperature = Gauge('weather_temperature_celsius', 'Temperature in Celsius')
feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature in Celsius')
humidity = Gauge('weather_humidity_percent', 'Humidity percentage')
pressure = Gauge('weather_pressure_hpa', 'Pressure in hPa')
wind_speed = Gauge('weather_wind_speed', 'Wind speed in m/s')
cloudiness = Gauge('weather_cloudiness_percent', 'Cloudiness percentage')
visibility = Gauge('weather_visibility_m', 'Visibility in meters')
sunrise = Gauge('weather_sunrise_timestamp', 'Sunrise time (timestamp)')
sunset = Gauge('weather_sunset_timestamp', 'Sunset time (timestamp)')

def collect_metrics():
    try:
        response = requests.get(URL)
        data = response.json()

        temperature.set(data["main"]["temp"])
        feels_like.set(data["main"]["feels_like"])
        humidity.set(data["main"]["humidity"])
        pressure.set(data["main"]["pressure"])
        wind_speed.set(data["wind"]["speed"])
        cloudiness.set(data["clouds"]["all"])
        visibility.set(data.get("visibility", 0))
        sunrise.set(data["sys"]["sunrise"])
        sunset.set(data["sys"]["sunset"])

        print(f" Updated weather metrics for {CITY}")
    except Exception as e:
        print(f" Error fetching data: {e}")

if __name__ == "__main__":
    print(" Custom API Exporter started on port 9106 ...")
    start_http_server(9106)
    while True:
        collect_metrics()
        time.sleep(20)
