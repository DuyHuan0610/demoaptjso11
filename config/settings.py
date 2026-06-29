"""Global configuration: alert thresholds, map settings, and application metadata."""

from typing import TypedDict


class ThresholdConfig(TypedDict):
    """Environmental measurement threshold definitions."""

    salinity_danger_ppt: float
    ph_acidic_max: float
    ph_alkaline_min: float


class MapConfig(TypedDict):
    """Folium/Carto map configuration for Ben Tre Province."""

    tile_provider: str
    center_lat: float
    center_lon: float
    zoom: float


class AppConfig(TypedDict):
    """Application metadata."""

    name: str
    subtitle: str
    region: str


# Salinity danger threshold — Mekong Delta agricultural standard (ppt = parts per thousand)
THRESHOLDS: ThresholdConfig = {
    "salinity_danger_ppt": 2.0,
    "ph_acidic_max": 6.5,
    "ph_alkaline_min": 8.5,
}

MAP_CONFIG: MapConfig = {
    "tile_provider": "CartoDB dark_matter",
    "center_lat": 10.08,
    "center_lon": 106.62,
    "zoom": 9.5,
}

APP_CONFIG: AppConfig = {
    "name": "SaltWatch",
    "subtitle": "Hyper-local Salinity Monitoring & AI Forecasting — Mekong Delta",
    "region": "Ben Tre Province, Vietnam",
}
