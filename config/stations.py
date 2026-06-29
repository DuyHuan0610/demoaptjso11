"""
Dữ liệu trạm IoT thực tế tại tỉnh Bến Tre.
Mỗi trạm bao gồm tọa độ GPS chính xác, mô tả vị trí và tham số cơ sở.
"""

from typing import Any


# Tọa độ tham chiếu từ các điểm quan trắc thực tế tại Bến Tre
STATIONS: dict[str, dict[str, Any]] = {
    "SW-01": {
        "id": "SW-01",
        "name": "Binh Dai",
        "location_label": "Cửa đập Bình Thới",
        "description": "Trạm giám sát tại cửa đập Bình Thới, huyện Bình Đại — cửa ngõ nước mặn đầu tiên.",
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
        "location_label": "Sông Hàm Luông",
        "description": "Trạm đặt trên sông Hàm Luông, huyện Ba Tri — khu vực nuôi trồng thủy sản trọng điểm.",
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
        "location_label": "Khu vực ươm giống nước ngọt",
        "description": "Trạm tại khu ươm giống cây trồng nước ngọt, huyện Chợ Lách — nhạy cảm cao với xâm nhập mặn.",
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
        "location_label": "Đầu nguồn sông Cổ Chiên",
        "description": "Trạm tại đầu nguồn sông Cổ Chiên, huyện Thạnh Phú — ranh giới nước ngọt - nước lợ.",
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
    """Trả về danh sách ID trạm theo thứ tự hiển thị."""
    return list(STATIONS.keys())


def get_station(station_id: str) -> dict[str, Any]:
    """
    Lấy thông tin trạm theo ID.
    Ném KeyError nếu ID không hợp lệ — fail-fast để phát hiện lỗi sớm.
    """
    if station_id not in STATIONS:
        raise KeyError(f"Trạm không tồn tại: {station_id}")
    return STATIONS[station_id]
