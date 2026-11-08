-- Lagos average rainfall by calendar month across the history window.
-- Uses complete months only (28+ days) so partial current months do not skew the average.
select extract(month from month_start) as month_num,
       round(avg(total_rain_mm)::numeric, 1) as avg_rain_mm,
       round(avg(rainy_days)::numeric, 1) as avg_rainy_days
from monthly_city_weather
where city = 'Lagos' and days_recorded >= 28
group by 1
order by 1;
