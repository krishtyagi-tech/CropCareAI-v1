import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


def get_weather_by_city(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }