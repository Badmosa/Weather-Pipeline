-- A comparison between the 4 four cities
select m as month,
  round(avg(case when city = 'Lagos' then total end)::numeric, 1) as lagos,
  round(avg(case when city = 'London' then total end)::numeric, 1) as london,
  round(avg(case when city = 'New York' then total end)::numeric, 1) as new_york,
  round(avg(case when city = 'Tokyo' then total end)::numeric, 1) as tokyo
from (
  select city,
         extract(year from weather_date) as y,
         extract(month from weather_date) as m,
         sum(precipitation_mm) as total
  from stg_weather_history
  group by 1, 2, 3
) t
group by m
order by m;
