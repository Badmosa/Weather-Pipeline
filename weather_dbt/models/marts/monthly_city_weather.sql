select
    city,
    date_trunc('month', weather_date) as month_start,
    count(*) as days_recorded,
    round(avg(temp_max_c), 1) as avg_max_temp_c,
    round(avg(temp_min_c), 1) as avg_min_temp_c,
    round(sum(precipitation_mm), 1) as total_rain_mm,
    count(*) filter (where precipitation_mm >= 1) as rainy_days
from {{ ref('stg_weather_history') }}
group by city, date_trunc('month', weather_date)