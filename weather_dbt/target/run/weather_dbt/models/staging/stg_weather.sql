
  
  create view "weather"."main"."stg_weather__dbt_tmp" as (
    select
    city,
    cast(load_date as date) as load_date,
    cast(date as date) as weather_date,
    temp_max as temp_max_c,
    temp_min as temp_min_c,
    precipitation as precipitation_mm
from "weather"."main"."raw_weather"
  );
