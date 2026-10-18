-- Fails if any city has more than one row for the same day
select
    city,
    weather_date,
    count(*) as row_count
from {{ ref('stg_weather_history') }}
group by city, weather_date
having count(*) > 1