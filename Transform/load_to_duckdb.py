import json
from pathlib import Path

import duckdb

# This file lives in Transform/, so go up one level to reach the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "weather.duckdb"
RAW_DATA_DIR = PROJECT_ROOT / "raw_data"


def load_json_to_duckdb():
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"No forecast files found at {RAW_DATA_DIR}. "
            "Run Ingestion/Fetch_Weather.py first."
        )

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
            rows = [
                (
                    city,
                    load_date,
                    daily["time"][i],
                    daily["temperature_2m_max"][i],
                    daily["temperature_2m_min"][i],
                    daily["precipitation_sum"][i],
                )
                for i in range(len(daily["time"]))
            ]

            # Replace this city/load_date so re-running the same files is safe
            con.execute(
                "DELETE FROM raw_weather WHERE city = ? AND load_date = ?",
                [city, load_date],
            )
            con.executemany(
                "INSERT INTO raw_weather VALUES (?, ?, ?, ?, ?, ?)",
                rows,
            )

            print(f"Loaded {city} ({load_date}): {len(rows)} rows")

    con.close()


if __name__ == "__main__":
    load_json_to_duckdb()
