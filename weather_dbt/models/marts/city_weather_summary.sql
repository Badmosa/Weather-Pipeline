select
    city,
    count(*) as days_recorded,
    round(avg(temp_max_c), 1) as avg_max_temp_c,
    round(avg(temp_min_c), 1) as avg_min_temp_c,
    max(temp_max_c) as hottest_day_c,
    min(temp_min_c) as coldest_day_c,
    round(sum(precipitation_mm), 1) as total_rain_mm
from {{ ref('stg_weather') }}
group by city