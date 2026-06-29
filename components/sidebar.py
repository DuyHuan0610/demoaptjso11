"""
Sidebar: điều khiển mô phỏng và thông tin hệ thống.
Toggle chuyển đổi giữa điều kiện bình thường và cảnh báo AI.
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
    """Render sidebar với toggle mô phỏng và metadata trạm."""
    with st.sidebar:
        st.markdown("### ⚙️ Bảng điều khiển")
        st.markdown("---")

        # Toggle mô phỏng: Normal ↔ AI Alert
        current_mode = get_simulation_mode()
        is_alert = current_mode == "alert"

        st.markdown("**Chế độ mô phỏng**")
        alert_enabled = st.toggle(
            "AI Predicted Salinity Intrusion Alert",
            value=is_alert,
            help="Bật để mô phỏng cảnh báo xâm nhập mặn theo dự báo AI",
            key="simulation_toggle",
        )

        new_mode = "alert" if alert_enabled else "normal"
        if new_mode != current_mode:
            set_simulation_mode(new_mode)
            st.rerun()

        # Hiển thị trạng thái hiện tại
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
