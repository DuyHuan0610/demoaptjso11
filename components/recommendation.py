"""
Engine khuyến nghị hành động theo mức rủi ro.
Thay đổi layout và gradient theo trạng thái Safe / Critical.
"""

import streamlit as st

from config.settings import THRESHOLDS
from data.simulation import build_station_snapshot
from state.session_manager import get_active_station_id, get_simulation_mode


# Khuyến nghị theo từng mức rủi ro — dễ mở rộng thêm rule engine
_SAFE_ACTIONS = [
    "Tiếp tục bơm nước ngọt theo lịch trình vận hành.",
    "Duy trì giám sát cảm biến mỗi 15 phút.",
    "Kiểm tra van điều tiết cửa đập — vận hành bình thường.",
    "Cập nhật dữ liệu cho trung tâm điều hành huyện.",
]

_CRITICAL_ACTIONS = [
    "ĐÓNG NGAY tất cả cửa đập và van điều tiết.",
    "Ngừng bơm nước — chuyển sang nguồn dự trữ nội bộ.",
    "Thông báo khẩn cho nông dân trong bán kính 5 km.",
    "Kích hoạt quy trình ứng phó xâm nhập mặn cấp huyện.",
    "Theo dõi liên tục dự báo AI trong 7 ngày tới.",
]


def render_recommendation() -> None:
    """Render thẻ khuyến nghị với styling động theo mức rủi ro."""
    station_id = get_active_station_id()
    mode = get_simulation_mode()
    snapshot = build_station_snapshot(station_id, mode)

    is_critical = snapshot["is_dangerous"]

    if is_critical:
        css_class = "recommendation-critical"
        title_class = "rec-title-critical"
        title = "🔴 CRITICAL: CLOSE SLUICE GATES IMMEDIATELY"
        ai_note = (
            " Dự báo AI xác nhận xu hướng xâm nhập mặn trong 7 ngày tới."
            if mode == "alert"
            else ""
        )
        subtitle = (
            f"Độ mặn hiện tại **{snapshot['salinity_ppt']:.2f} ‰** "
            f"vượt ngưỡng an toàn **{THRESHOLDS['salinity_danger_ppt']} ‰**.{ai_note}"
        )
        actions = _CRITICAL_ACTIONS
    else:
        css_class = "recommendation-safe"
        title_class = "rec-title-safe"
        title = "🟢 SAFE TO PUMP WATER"
        subtitle = (
            f"Độ mặn **{snapshot['salinity_ppt']:.2f} ‰** nằm trong ngưỡng an toàn "
            f"(< {THRESHOLDS['salinity_danger_ppt']} ‰). Hệ thống vận hành bình thường."
        )
        actions = _SAFE_ACTIONS

    actions_html = "".join(f"<li>{a}</li>" for a in actions)

    st.markdown(
        f"""
        <div class="{css_class}">
            <div class="rec-title {title_class}">{title}</div>
            <div class="rec-body">{subtitle}</div>
            <ul class="rec-actions">{actions_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
