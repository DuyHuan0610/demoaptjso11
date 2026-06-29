"""
Cấu hình toàn cục: ngưỡng cảnh báo, bản đồ, và thông số ứng dụng.
Tập trung hóa các hằng số để dễ bảo trì và kiểm thử.
"""

from typing import TypedDict


class ThresholdConfig(TypedDict):
    """Định nghĩa các ngưỡng đo lường môi trường."""

    salinity_danger_ppt: float
    ph_acidic_max: float
    ph_alkaline_min: float


class MapConfig(TypedDict):
    """Cấu hình bản đồ Folium/Carto cho khu vực Bến Tre."""

    tile_provider: str
    center_lat: float
    center_lon: float
    zoom: float


class AppConfig(TypedDict):
    """Metadata ứng dụng."""

    name: str
    subtitle: str
    region: str


# Ngưỡng độ mặn nguy hiểm theo tiêu chuẩn nông nghiệp ĐBSCL (ppt = ‰)
THRESHOLDS: ThresholdConfig = {
    "salinity_danger_ppt": 2.0,
    "ph_acidic_max": 6.5,
    "ph_alkaline_min": 8.5,
}

# Trung tâm bản đồ: tỉnh Bến Tre — tile Carto Dark Matter (miễn phí, không API key)
MAP_CONFIG: MapConfig = {
    "tile_provider": "CartoDB dark_matter",
    "center_lat": 10.08,
    "center_lon": 106.62,
    "zoom": 9.5,
}

APP_CONFIG: AppConfig = {
    "name": "SaltWatch",
    "subtitle": "Giám sát độ mặn siêu cục bộ & Dự báo AI — Đồng bằng sông Cửu Long",
    "region": "Tỉnh Bến Tre, Việt Nam",
}
