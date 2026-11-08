--average daily high rainfall by month for each city--
select extract(month from weather_date) as month,
  round((avg(temp_max_c) filter (where city = 'Lagos'))::numeric, 1) as lagos,
  round((avg(temp_max_c) filter (where city = 'London'))::numeric, 1) as london,
  round((avg(temp_max_c) filter (where city = 'New York'))::numeric, 1) as new_york,
  round((avg(temp_max_c) filter (where city = 'Tokyo'))::numeric, 1) as tokyo
from stg_weather_history
group by 1
order by 1;
