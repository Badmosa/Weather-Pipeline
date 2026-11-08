-- Average rainfall by calendar month for every city.
-- Same grain and complete-month filter as the Lagos query, so the cities are comparable.
select city,
       extract(month from month_start) as month_num,
       round(avg(total_rain_mm)::numeric, 1) as avg_rain_mm,
       round(avg(rainy_days)::numeric, 1) as avg_rainy_days
from monthly_city_weather
where days_recorded >= 28
group by city, extract(month from month_start)
order by city, month_num;
