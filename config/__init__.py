"""Gói cấu hình toàn cục cho ứng dụng SaltWatch."""

from config.settings import APP_CONFIG, MAP_CONFIG, THRESHOLDS
from config.stations import STATIONS, get_station, get_station_ids

__all__ = [
    "APP_CONFIG",
    "MAP_CONFIG",
    "THRESHOLDS",
    "STATIONS",
    "get_station",
    "get_station_ids",
]
