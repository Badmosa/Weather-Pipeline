# Power BI report

Marts are exported as CSV files. 

Open those files in Power BI to build visuals.

The same charts are saved in `powerbi/charts/` for GitHub.

## Data

After a pipeline run:

```bash
python Transform/pipeline_visual.py
```

Then in Power BI Desktop: **Get data → Text/CSV** and load, in this order:

1. `powerbi/data/city_month_climatology.csv` — average rain by month (complete months only)
2. `powerbi/data/monthly_city_weather.csv` — one row per city per month
3. `powerbi/data/city_weather_summary.csv` — latest 7-day forecast

To refresh from Postgres instead: **Get data → PostgreSQL database**, server `localhost`, database `weather`, table `monthly_city_weather`.

## Visuals

**Page 1 — Rainfall 2020–2026**

| Visual | Fields |
|---|---|
| Line chart | Axis: `month_num` (sort by this column, display `month_name`). Values: `avg_rain_mm`. Legend: `city` |
| Clustered bar chart | Axis: `city`. Values: Sum of `total_rain_mm` from `monthly_city_weather.csv` |
| Slicer | `city` |
| Card | Sum of `avg_rain_mm` for Lagos in June (optional) |

Sorted `month_name` by `month_num` so the axis is in calendar order and not alphabetical.

**Page 2 — Forecast**

| Visual | Fields |
|---|---|
| Table | all columns from `city_weather_summary.csv` |
| Clustered bar | Axis: `city`. Values: `total_rain_mm` |
