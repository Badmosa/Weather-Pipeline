import requests
import json
from datetime import date
import os

# List of cities with their latitude and longitude
CITIES = {
    "Lagos": {"lat": 6.5244, "lon": 3.3792},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
}

def fetch_weather(city_name, lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_raw(city_name, data):
    today = date.today().isoformat()
    folder = f"raw_data/{today}"
    os.makedirs(folder, exist_ok=True)
    filepath = f"{folder}/{city_name.replace(' ', '_')}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filepath}")

def main():
    for city_name, coords in CITIES.items():
        data = fetch_weather(city_name, coords["lat"], coords["lon"])
        save_raw(city_name, data)

if __name__ == "__main__":
    main()