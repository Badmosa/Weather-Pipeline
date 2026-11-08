-- Total rainfall and typical daily high rainfall by city over the history window.
select city,
       round(avg(avg_max_temp_c)::numeric, 1) as avg_high_c,
       round(sum(total_rain_mm)::numeric, 0) as total_rain_mm
from monthly_city_weather
group by city
order by total_rain_mm desc;
