"""Export DuckDB marts as CSV files Power BI can open without running Postgres."""

from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "weather.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "powerbi" / "data"

MONTH_CASE = """
    case extract(month from month_start)::integer
        when 1 then 'January'
        when 2 then 'February'
        when 3 then 'March'
        when 4 then 'April'
        when 5 then 'May'
        when 6 then 'June'
        when 7 then 'July'
        when 8 then 'August'
        when 9 then 'September'
        when 10 then 'October'
        when 11 then 'November'
        when 12 then 'December'
    end
"""


def _copy(con, sql, path: Path):
    con.execute(f"copy ({sql}) to '{path.as_posix()}' (header, delimiter ',')")


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"No DuckDB file at {DB_PATH}. Run the pipeline and dbt before exporting."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)

    monthly_path = OUTPUT_DIR / "monthly_city_weather.csv"
    _copy(
        con,
        f"""
        select
                city,
            cast(month_start as date) as month_start,
            extract(year from month_start)::integer as year,
            extract(month from month_start)::integer as month_num,
            {MONTH_CASE} as month_name,
            days_recorded,
            avg_max_temp_c,
            avg_min_temp_c,
            total_rain_mm,
            rainy_days,
            days_recorded >= 28 as is_complete_month
        from monthly_city_weather
        order by city, month_start
        """,
        monthly_path,
    )

    summary_path = OUTPUT_DIR / "city_weather_summary.csv"
    _copy(
        con,
        """
        select *
        from city_weather_summary
        order by city
        """,
        summary_path,
    )

    climatology_path = OUTPUT_DIR / "city_month_climatology.csv"
    _copy(
        con,
        f"""
        select
            city,
            extract(month from month_start)::integer as month_num,
            {MONTH_CASE} as month_name,
            round(avg(total_rain_mm), 1) as avg_rain_mm,
            round(avg(rainy_days), 1) as avg_rainy_days,
            round(avg(avg_max_temp_c), 1) as avg_max_temp_c
        from monthly_city_weather
        where days_recorded >= 28
        group by city, extract(month from month_start)
        order by city, month_num
        """,
        climatology_path,
    )
    con.close()
    print(f"Wrote {monthly_path.name}, {summary_path.name}, {climatology_path.name}")


if __name__ == "__main__":
    main()
