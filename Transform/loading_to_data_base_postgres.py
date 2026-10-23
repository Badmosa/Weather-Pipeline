import os
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "weather.duckdb"

# Read the password from an environment variable so it never goes into Git
PG_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# Single quotes in the password would break the ATTACH string
PG_PASSWORD_SQL = PG_PASSWORD.replace("'", "''")

TABLES = ["city_weather_summary", "monthly_city_weather", "stg_weather_history"]

con = duckdb.connect(str(DB_PATH))
con.execute("INSTALL postgres")
con.execute("LOAD postgres")
con.execute(
    f"ATTACH 'host=localhost port=5432 dbname=weather user=postgres "
    f"password={PG_PASSWORD_SQL}' AS pg (TYPE postgres)"
)

for table in TABLES:
    con.execute(f"DROP TABLE IF EXISTS pg.public.{table}")
    con.execute(f"CREATE TABLE pg.public.{table} AS SELECT * FROM weather.main.{table}")
    count = con.execute(f"SELECT count(*) FROM pg.public.{table}").fetchone()[0]
    print(f"Copied {table}: {count} rows")

con.close()