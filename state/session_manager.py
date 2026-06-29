"""
Quản lý trạng thái toàn cục qua st.session_state.
Đồng bộ trạm đang chọn và chế độ cảnh báo trên mọi component.
"""

from typing import Literal

import streamlit as st

from config.stations import get_station_ids

SimulationMode = Literal["normal", "alert"]


def init_session_state() -> None:
    """Khởi tạo session state với giá trị mặc định."""
    defaults: dict[str, str] = {
        "active_station_id": get_station_ids()[0],
        "simulation_mode": "normal",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_active_station_id() -> str:
    """Trả về ID trạm đang được chọn."""
    init_session_state()
    return st.session_state.active_station_id


def set_active_station(station_id: str) -> None:
    """Cập nhật trạm hoạt động — tất cả component rerender đồng bộ."""
    init_session_state()
    if station_id in get_station_ids():
        st.session_state.active_station_id = station_id


def get_simulation_mode() -> SimulationMode:
    """Trả về chế độ cảnh báo hiện tại (normal | alert)."""
    init_session_state()
    return st.session_state.simulation_mode  # type: ignore[return-value]


def set_simulation_mode(mode: SimulationMode) -> None:
    """Chuyển đổi giữa điều kiện bình thường và cảnh báo AI."""
    init_session_state()
    st.session_state.simulation_mode = mode
