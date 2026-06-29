"""SaltWatch — Hyper-local Salinity Monitoring & AI Forecasting, Mekong Delta."""

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
    page_title=f"{APP_CONFIG['name']} | Salinity Monitoring — Ben Tre",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Main dashboard entry point."""
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
    st.markdown("#### 📈 Time Series Analysis & AI Forecast")
    render_timeseries_chart()


if __name__ == "__main__":
    main()
