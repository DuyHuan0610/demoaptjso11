"""Sidebar — AI alert controls and active station information."""

import streamlit as st

from config.settings import APP_CONFIG, THRESHOLDS
from config.stations import get_station
from state.session_manager import (
    get_active_station_id,
    get_simulation_mode,
    set_simulation_mode,
)


def render_sidebar() -> None:
    """Render the sidebar with alert toggle and station metadata."""
    with st.sidebar:
        st.markdown("### ⚙️ Control Panel")
        st.markdown("---")

        current_mode = get_simulation_mode()
        is_alert = current_mode == "alert"

        st.markdown("**Salinity Intrusion Forecast**")
        alert_enabled = st.toggle(
            "Enable AI Intrusion Alert",
            value=is_alert,
            help="Display 7-day salinity forecast and emergency recommendations",
            key="alert_toggle",
        )

        new_mode = "alert" if alert_enabled else "normal"
        if new_mode != current_mode:
            set_simulation_mode(new_mode)
            st.rerun()

        if alert_enabled:
            st.error("🔴 Status: SALINITY INTRUSION ALERT")
        else:
            st.success("🟢 Status: NORMAL CONDITIONS")

        st.markdown("---")
        st.markdown("**Active Station**")
        station = get_station(get_active_station_id())
        st.info(
            f"**{station['id']}** ({station['name']})\n\n"
            f"📍 {station['location_label']}"
        )

        st.markdown("---")
        st.markdown("**Alert Thresholds**")
        st.caption(
            f"Critical salinity: **≥ {THRESHOLDS['salinity_danger_ppt']} ppt**\n\n"
            f"Optimal pH range: **{THRESHOLDS['ph_acidic_max']} – {THRESHOLDS['ph_alkaline_min']}**"
        )

        st.markdown("---")
        st.caption(f"© 2026 {APP_CONFIG['name']} — {APP_CONFIG['region']}")
