-- Fails if any city has more than one row for the same month
select
    city,
    month_start,
    count(*) as row_count
from {{ ref('monthly_city_weather') }}
group by city, month_start
having count(*) > 1
