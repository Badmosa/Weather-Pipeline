import duckdb
import json
from pathlib import Path

# This file lives in transform/, so go up one level to reach the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "weather.duckdb"
RAW_DATA_DIR = PROJECT_ROOT / "raw_data"

def load_json_to_duckdb():
    con = duckdb.connect(str(DB_PATH))

    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            city VARCHAR,
            load_date VARCHAR,
            date VARCHAR,
            temp_max DOUBLE,
            temp_min DOUBLE,
            precipitation DOUBLE
        )
    """)

    for date_folder in RAW_DATA_DIR.iterdir():
        if not date_folder.is_dir():
            continue
        load_date = date_folder.name

        for json_file in date_folder.glob("*.json"):
            city = json_file.stem.replace("_", " ")

            with open(json_file, "r") as f:
                data = json.load(f)

            daily = data["daily"]
            dates = daily["time"]
            temp_max = daily["temperature_2m_max"]
            temp_min = daily["temperature_2m_min"]
            precipitation = daily["precipitation_sum"]

            for i in range(len(dates)):
                con.execute(
                    "INSERT INTO raw_weather VALUES (?, ?, ?, ?, ?, ?)",
                    [city, load_date, dates[i], temp_max[i], temp_min[i], precipitation[i]]
                )

            print(f"Loaded {city} ({load_date}): {len(dates)} rows")

    con.close()

if __name__ == "__main__":
    load_json_to_duckdb()