-- Fails if a day's low is above its high, or a temperature is impossible
select city, weather_date, temp_min_c, temp_max_c
from {{ ref('stg_weather') }}
where temp_min_c > temp_max_c
   or temp_max_c not between -60 and 60
   or temp_min_c not between -60 and 60

union all

select city, weather_date, temp_min_c, temp_max_c
from {{ ref('stg_weather_history') }}
where temp_min_c > temp_max_c
   or temp_max_c not between -60 and 60
   or temp_min_c not between -60 and 60
