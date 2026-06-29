"""IoT sensor station data for Ben Tre Province, Vietnam."""

from typing import Any


STATIONS: dict[str, dict[str, Any]] = {
    "SW-01": {
        "id": "SW-01",
        "name": "Binh Dai",
        "location_label": "Binh Thoi Sluice Gate",
        "description": (
            "Monitoring station at Binh Thoi Sluice Gate, Binh Dai District — "
            "primary entry point for saline water intrusion."
        ),
        "latitude": 10.0684,
        "longitude": 106.7128,
        "baseline": {
            "salinity_ppt": 1.2,
            "ph": 7.1,
            "temperature_c": 29.5,
        },
        "connectivity": "online",
    },
    "SW-02": {
        "id": "SW-02",
        "name": "Ba Tri",
        "location_label": "Ham Luong River",
        "description": (
            "Monitoring station on the Ham Luong River, Ba Tri District — "
            "key aquaculture production zone."
        ),
        "latitude": 9.9512,
        "longitude": 106.5841,
        "baseline": {
            "salinity_ppt": 0.8,
            "ph": 7.4,
            "temperature_c": 30.1,
        },
        "connectivity": "online",
    },
    "SW-03": {
        "id": "SW-03",
        "name": "Cho Lach",
        "location_label": "Freshwater Seedling Area",
        "description": (
            "Monitoring station in the freshwater seedling nursery zone, Cho Lach District — "
            "highly sensitive to salinity intrusion."
        ),
        "latitude": 10.2236,
        "longitude": 106.6187,
        "baseline": {
            "salinity_ppt": 0.5,
            "ph": 7.6,
            "temperature_c": 28.8,
        },
        "connectivity": "online",
    },
    "SW-04": {
        "id": "SW-04",
        "name": "Thanh Phu",
        "location_label": "Co Chien River Headwaters",
        "description": (
            "Monitoring station at the Co Chien River headwaters, Thanh Phu District — "
            "freshwater–brackish water transition zone."
        ),
        "latitude": 10.0819,
        "longitude": 106.5213,
        "baseline": {
            "salinity_ppt": 1.5,
            "ph": 7.0,
            "temperature_c": 29.2,
        },
        "connectivity": "online",
    },
}


def get_station_ids() -> list[str]:
    """Return station IDs in display order."""
    return list(STATIONS.keys())


def get_station(station_id: str) -> dict[str, Any]:
    """Return station metadata by ID."""
    if station_id not in STATIONS:
        raise KeyError(f"Station not found: {station_id}")
    return STATIONS[station_id]
