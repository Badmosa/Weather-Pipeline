import json
from datetime import date, timedelta
from pathlib import Path

import requests

CITIES = {
    "Lagos": {"lat": 6.5244, "lon": 3.3792},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503},
}

START_DATE = "2020-01-01"
# The archive lags a few days behind, so stop a week ago to be safe
END_DATE = (date.today() - timedelta(days=7)).isoformat()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "raw_history"


def fetch_history(lat, lon):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for city, coords in CITIES.items():
        data = fetch_history(coords["lat"], coords["lon"])
        filepath = OUTPUT_DIR / f"{city.replace(' ', '_')}.json"
        with open(filepath, "w") as f:
            json.dump(data, f)
        print(f"Saved {filepath.name}: {len(data['daily']['time'])} days")


if __name__ == "__main__":
    main()