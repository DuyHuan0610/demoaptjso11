"""
Mô phỏng dữ liệu cảm biến IoT và mô hình dự báo AI.
Sử dụng seed cố định theo trạm để đảm bảo dữ liệu nhất quán giữa các lần render.
"""

from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

from config.settings import THRESHOLDS
from config.stations import STATIONS, get_station
from state.session_manager import SimulationMode


def _station_rng(station_id: str, salt: str = "") -> np.random.Generator:
    """Tạo bộ sinh số ngẫu nhiên có seed theo trạm — tái lập được kết quả."""
    seed = sum(ord(c) for c in f"{station_id}{salt}")
    return np.random.default_rng(seed)


def is_salinity_dangerous(salinity_ppt: float) -> bool:
    """Kiểm tra độ mặn có vượt ngưỡng nguy hiểm hay không."""
    return salinity_ppt >= THRESHOLDS["salinity_danger_ppt"]


def build_station_snapshot(station_id: str, mode: SimulationMode) -> dict[str, Any]:
    """
    Tạo snapshot dữ liệu thời gian thực cho một trạm.
    Chế độ 'alert' mô phỏng xâm nhập mặn AI dự báo với giá trị cao hơn baseline.
    """
    station = get_station(station_id)
    baseline = station["baseline"]
    rng = _station_rng(station_id, mode)

    if mode == "alert":
        # Mô phỏng đỉnh xâm nhập mặn theo dự báo AI
        salinity = float(baseline["salinity_ppt"] + rng.uniform(1.2, 2.8))
        ph = float(baseline["ph"] - rng.uniform(0.1, 0.4))
        temperature = float(baseline["temperature_c"] + rng.uniform(0.5, 1.5))
        connectivity = "online"
    else:
        # Dao động tự nhiên quanh giá trị cơ sở
        salinity = float(baseline["salinity_ppt"] + rng.uniform(-0.3, 0.4))
        ph = float(baseline["ph"] + rng.uniform(-0.2, 0.2))
        temperature = float(baseline["temperature_c"] + rng.uniform(-0.8, 0.8))
        connectivity = station["connectivity"]

    salinity = max(0.0, round(salinity, 2))
    ph = round(ph, 2)
    temperature = round(temperature, 1)

    return {
        "station_id": station_id,
        "salinity_ppt": salinity,
        "ph": ph,
        "temperature_c": temperature,
        "connectivity": connectivity,
        "is_dangerous": is_salinity_dangerous(salinity),
        "timestamp": datetime.now(),
    }


def get_all_stations_snapshots(mode: SimulationMode) -> dict[str, dict[str, Any]]:
    """Lấy snapshot cho tất cả trạm — phục vụ bản đồ và so sánh đa trạm."""
    return {sid: build_station_snapshot(sid, mode) for sid in STATIONS}


def generate_historical_series(
    station_id: str,
    mode: SimulationMode,
    days: int = 7,
    points_per_day: int = 4,
) -> pd.DataFrame:
    """
    Sinh chuỗi thời gian lịch sử 7 ngày cho biểu đồ.
    Trả về DataFrame với cột: timestamp, salinity_ppt, series_type.
    """
    station = get_station(station_id)
    baseline = station["baseline"]["salinity_ppt"]
    rng = _station_rng(station_id, f"hist-{mode}")

    total_points = days * points_per_day
    end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=days)

    timestamps = pd.date_range(start=start_time, end=end_time, periods=total_points)

    # Xu hướng tăng nhẹ về phía hiện tại
    trend = np.linspace(-0.2, 0.3 if mode == "normal" else 0.8, total_points)
    noise = rng.normal(0, 0.15, total_points)
    values = np.clip(baseline + trend + noise, 0, None)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "salinity_ppt": np.round(values, 2),
            "series_type": "historical",
        }
    )


def generate_forecast_series(
    station_id: str,
    last_historical_value: float,
    days: int = 7,
    points_per_day: int = 4,
) -> pd.DataFrame:
    """
    Mô phỏng dự báo AI 7 ngày tương lai bằng hồi quy đa thức bậc 2.
    Đường cong dự báo thể hiện đỉnh xâm nhập mặn dự kiến.
    """
    rng = _station_rng(station_id, "forecast")
    total_points = days * points_per_day

    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, periods=total_points)

    # Mô hình hồi quy: tăng dần tới đỉnh rồi giảm nhẹ (mô phỏng AI regression)
    x = np.linspace(0, 1, total_points)
    peak = last_historical_value + rng.uniform(1.5, 3.2)
    # Parabol mở xuống — đỉnh tại x ≈ 0.45
    curve = last_historical_value + (peak - last_historical_value) * (
        -4 * (x - 0.45) ** 2 + 1
    )
    noise = rng.normal(0, 0.08, total_points)
    values = np.clip(curve + noise, 0, None)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "salinity_ppt": np.round(values, 2),
            "series_type": "forecast",
        }
    )
