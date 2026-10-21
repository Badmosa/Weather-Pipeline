import os

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="weather",
    user="postgres",
    password=os.environ["POSTGRES_PASSWORD"],
)

QUERY = """
select extract(month from month_start) as month_num,
       round(avg(total_rain_mm), 1) as avg_rain_mm,
       round(avg(rainy_days), 1) as avg_rainy_days
from monthly_city_weather
where city = 'Lagos' and days_recorded >= 28
group by 1
order by 1;
"""

with conn.cursor() as cur:
    cur.execute(QUERY)
    columns = [col[0] for col in cur.description]
    print(columns)
    for row in cur.fetchall():
        print(row)

conn.close()