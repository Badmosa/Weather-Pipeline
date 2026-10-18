import json
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "weather.duckdb"
HISTORY_DIR = PROJECT_ROOT / "raw_history"


def main():
    rows = []
    for json_file in HISTORY_DIR.glob("*.json"):
        city = json_file.stem.replace("_", " ")
        with open(json_file, "r") as f:
            daily = json.load(f)["daily"]
        for i in range(len(daily["time"])):
            rows.append((
                city,
                daily["time"][i],
                daily["temperature_2m_max"][i],
                daily["temperature_2m_min"][i],
                daily["precipitation_sum"][i],
            ))

    con = duckdb.connect(str(DB_PATH))
    # Full refresh each run, so re-running never creates duplicates
    con.execute("DROP TABLE IF EXISTS raw_weather_history")
    con.execute("""
        CREATE TABLE raw_weather_history (
            city VARCHAR,
            weather_date VARCHAR,
            temp_max DOUBLE,
            temp_min DOUBLE,
            precipitation DOUBLE
        )
    """)
    con.executemany("INSERT INTO raw_weather_history VALUES (?, ?, ?, ?, ?)", rows)
    print(f"Loaded {len(rows)} rows into raw_weather_history")
    con.close()


if __name__ == "__main__":
    main()