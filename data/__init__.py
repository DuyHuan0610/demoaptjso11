"""IoT sensor data processing and AI forecasting."""

from data.simulation import (
    build_station_snapshot,
    generate_forecast_series,
    generate_historical_series,
    get_all_stations_snapshots,
    is_salinity_dangerous,
)

__all__ = [
    "build_station_snapshot",
    "generate_forecast_series",
    "generate_historical_series",
    "get_all_stations_snapshots",
    "is_salinity_dangerous",
]
