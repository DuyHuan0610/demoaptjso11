"""
Sidebar — điều khiển cảnh báo AI và thông tin trạm đang giám sát.
"""

import streamlit as st

from config.settings import APP_CONFIG, THRESHOLDS
from config.stations import get_station
from state.session_manager import (
    get_active_station_id,
    get_simulation_mode,
    set_simulation_mode,
)


def render_sidebar() -> None:
    """Render sidebar với toggle cảnh báo AI và metadata trạm."""
    with st.sidebar:
        st.markdown("### ⚙️ Bảng điều khiển")
        st.markdown("---")

        current_mode = get_simulation_mode()
        is_alert = current_mode == "alert"

        st.markdown("**Dự báo xâm nhập mặn**")
        alert_enabled = st.toggle(
            "Kích hoạt cảnh báo AI",
            value=is_alert,
            help="Hiển thị dự báo xâm nhập mặn 7 ngày và khuyến nghị khẩn cấp",
            key="alert_toggle",
        )

        new_mode = "alert" if alert_enabled else "normal"
        if new_mode != current_mode:
            set_simulation_mode(new_mode)
            st.rerun()

        if alert_enabled:
            st.error("🔴 Trạng thái: CẢNH BÁO XÂM NHẬP MẶN")
        else:
            st.success("🟢 Trạng thái: ĐIỀU KIỆN BÌNH THƯỜNG")

        st.markdown("---")
        st.markdown("**Trạm đang chọn**")
        station = get_station(get_active_station_id())
        st.info(
            f"**{station['id']}** ({station['name']})\n\n"
            f"📍 {station['location_label']}"
        )

        st.markdown("---")
        st.markdown("**Ngưỡng cảnh báo**")
        st.caption(
            f"Độ mặn nguy hiểm: **≥ {THRESHOLDS['salinity_danger_ppt']} ‰**\n\n"
            f"pH tối ưu: **{THRESHOLDS['ph_acidic_max']} – {THRESHOLDS['ph_alkaline_min']}**"
        )

        st.markdown("---")
        st.caption(f"© 2026 {APP_CONFIG['name']} — {APP_CONFIG['region']}")
