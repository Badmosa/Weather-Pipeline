select *
from city_weather_summary;

select *
from monthly_city_weather;


-- Lagos
select m as month, round(avg(total)::numeric, 1) as avg_rain_mm
from (
  select extract(year from weather_date) as y,
         extract(month from weather_date) as m,
         sum(precipitation_mm) as total
  from stg_weather_history
  where city = 'Lagos'
  group by 1, 2
) t
group by m
order by m;


--London
select m as month, round(avg(total)::numeric, 1) as avg_rain_mm
from (
  select extract(year from weather_date) as y,
         extract(month from weather_date) as m,
         sum(precipitation_mm) as total
  from stg_weather_history
  where city = 'London'
  group by 1, 2
) t
group by m
order by m;


--New York
select m as month, round(avg(total)::numeric, 1) as avg_rain_mm
from (
  select extract(year from weather_date) as y,
         extract(month from weather_date) as m,
         sum(precipitation_mm) as total
  from stg_weather_history
  where city = 'New York'
  group by 1, 2
) t
group by m
order by m;


--Tokyo
select m as month, round(avg(total)::numeric, 1) as avg_rain_mm
from (
  select extract(year from weather_date) as y,
         extract(month from weather_date) as m,
         sum(precipitation_mm) as total
  from stg_weather_history
  where city = 'Tokyo'
  group by 1, 2
) t
group by m
order by m;