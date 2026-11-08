"""Save the two main findings as PNG charts for the README and Power BI screenshots."""

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "weather.duckdb"
CHART_DIR = PROJECT_ROOT / "powerbi" / "charts"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CITY_COLOURS = {
    "Lagos": "#1f77b4",
    "London": "#ff7f0e",
    "New York": "#2ca02c",
    "Tokyo": "#d62728",
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No DuckDB file at {DB_PATH}")

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)

    climatology = con.execute(
        """
        select
            city,
            extract(month from month_start)::integer as month_num,
            round(avg(total_rain_mm), 1) as avg_rain_mm
        from monthly_city_weather
        where days_recorded >= 28
        group by city, extract(month from month_start)
        order by city, month_num
        """
    ).fetchall()

    totals = con.execute(
        """
        select
            city,
            round(sum(total_rain_mm), 0) as total_rain_mm
        from monthly_city_weather
        group by city
        order by total_rain_mm desc
        """
    ).fetchall()
    con.close()

    _plot_climatology(climatology)
    _plot_totals(totals)
    _plot_dashboard(climatology, totals)
    print(f"Wrote charts to {CHART_DIR}")


def _plot_climatology(rows):
    by_city = {}
    for city, month_num, avg_rain in rows:
        by_city.setdefault(city, {})[int(month_num)] = float(avg_rain)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = list(range(1, 13))
    for city, month_map in by_city.items():
        y = [month_map.get(m, 0) for m in x]
        linewidth = 2.8 if city == "Lagos" else 1.6
        ax.plot(
            x,
            y,
            label=city,
            color=CITY_COLOURS.get(city, "gray"),
            linewidth=linewidth,
            marker="o",
            markersize=4,
        )

    ax.set_xticks(x, MONTHS)
    ax.set_ylabel("Average rain (mm)")
    ax.set_title("Average monthly rainfall, 2020–2026")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "monthly_rainfall_by_city.png", dpi=140)
    plt.close(fig)


def _plot_totals(rows):
    cities = [row[0] for row in rows]
    values = [float(row[1]) for row in rows]
    colours = [CITY_COLOURS.get(city, "gray") for city in cities]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(cities, values, color=colours)
    ax.set_ylabel("Total rain (mm)")
    ax.set_title("Total rainfall by city, 2020–2026")
    ax.bar_label(bars, fmt="%.0f")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "total_rainfall_by_city.png", dpi=140)
    plt.close(fig)


def _plot_dashboard(climatology, totals):
    by_city = {}
    for city, month_num, avg_rain in climatology:
        by_city.setdefault(city, {})[int(month_num)] = float(avg_rain)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    x = list(range(1, 13))
    for city, month_map in by_city.items():
        y = [month_map.get(m, 0) for m in x]
        axes[0].plot(
            x,
            y,
            label=city,
            color=CITY_COLOURS.get(city, "gray"),
            linewidth=2.6 if city == "Lagos" else 1.5,
            marker="o",
            markersize=4,
        )
    axes[0].set_xticks(x, MONTHS)
    axes[0].set_ylabel("Average rain (mm)")
    axes[0].set_title("Lagos has two rainy seasons")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    cities = [row[0] for row in totals]
    values = [float(row[1]) for row in totals]
    colours = [CITY_COLOURS.get(city, "gray") for city in cities]
    bars = axes[1].bar(cities, values, color=colours)
    axes[1].set_ylabel("Total rain (mm)")
    axes[1].set_title("Tokyo is wetter than Lagos overall")
    axes[1].bar_label(bars, fmt="%.0f")
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("Weather pipeline · rainfall 2020–2026", fontsize=13)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "rainfall_dashboard.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
