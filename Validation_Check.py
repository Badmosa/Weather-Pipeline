import duckdb

con = duckdb.connect("weather.duckdb")
print(con.execute("select * from raw_weather limit 5").fetchall())
print(con.execute("select city, count(*) from raw_weather group by city").fetchall())