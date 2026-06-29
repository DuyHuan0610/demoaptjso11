"""
SaltWatch — Giám sát độ mặn siêu cục bộ & Dự báo AI
Đồng bằng sông Cửu Long, tỉnh Bến Tre, Việt Nam.
"""

import streamlit as st

from components.kpi_grid import render_kpi_grid
from components.map_view import render_map_and_nav
from components.recommendation import render_recommendation
from components.sidebar import render_sidebar
from components.timeseries_chart import render_timeseries_chart
from config.settings import APP_CONFIG
from state.session_manager import init_session_state
from styles.theme import inject_theme, render_app_header

st.set_page_config(
    page_title=f"{APP_CONFIG['name']} | Giám sát độ mặn Bến Tre",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Luồng chính của dashboard."""
    init_session_state()
    inject_theme()
    render_app_header(APP_CONFIG["name"], APP_CONFIG["subtitle"])

    render_sidebar()
    render_kpi_grid()

    st.markdown("---")
    render_recommendation()

    st.markdown("---")
    render_map_and_nav()

    st.markdown("---")
    st.markdown("#### 📈 Phân tích chuỗi thời gian & Dự báo AI")
    render_timeseries_chart()


if __name__ == "__main__":
    main()
