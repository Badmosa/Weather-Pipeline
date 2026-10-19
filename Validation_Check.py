import duckdb

con = duckdb.connect("weather.duckdb")
print(con.execute("select * from raw_weather limit 5").fetchall())
print(con.execute("select city, count(*) from raw_weather group by city").fetchall())
print(con.execute("select * from city_weather_summary").fetchall())
print(con.execute("select city, month_start, total_rain_mm, rainy_days from monthly_city_weather where city = 'Lagos' and month_start between '2025-01-01' and '2025-12-01' order by month_start").fetchall())
print(con.execute("select city, round(avg(avg_max_temp_c), 1) as avg_high, round(sum(total_rain_mm), 0) as total_rain from monthly_city_weather group by city order by total_rain desc").fetchall())

# run: python validation_check.py