select
    city,
    cast(load_date as date) as load_date,
    cast(date as date) as weather_date,
    temp_max as temp_max_c,
    temp_min as temp_min_c,
    precipitation as precipitation_mm
from {{ source('raw', 'raw_weather') }}