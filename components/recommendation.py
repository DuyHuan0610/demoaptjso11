"""Action recommendation engine based on salinity risk level."""

import streamlit as st

from config.settings import THRESHOLDS
from data.simulation import build_station_snapshot
from state.session_manager import get_active_station_id, get_simulation_mode


_SAFE_ACTIONS = [
    "Continue freshwater pumping according to the scheduled operation plan.",
    "Maintain IoT sensor monitoring at 15-minute intervals.",
    "Inspect sluice gate control valves — operating normally.",
    "Report readings to the district operations center.",
]

_CRITICAL_ACTIONS = [
    "CLOSE all sluice gates and control valves immediately.",
    "Stop water pumping — switch to internal reserve supply.",
    "Issue urgent alerts to farmers within a 5 km radius.",
    "Activate district-level salinity intrusion response protocol.",
    "Monitor AI forecast continuously over the next 7 days.",
]


def render_recommendation() -> None:
    """Render the Safe / Critical recommendation card."""
    station_id = get_active_station_id()
    mode = get_simulation_mode()
    snapshot = build_station_snapshot(station_id, mode)

    is_critical = snapshot["is_dangerous"]

    if is_critical:
        css_class = "recommendation-critical"
        title_class = "rec-title-critical"
        title = "🔴 CRITICAL: CLOSE SLUICE GATES IMMEDIATELY"
        ai_note = (
            " AI forecast confirms rising salinity intrusion over the next 7 days."
            if mode == "alert"
            else ""
        )
        subtitle = (
            f"Current salinity **{snapshot['salinity_ppt']:.2f} ppt** exceeds the safe limit of "
            f"**{THRESHOLDS['salinity_danger_ppt']} ppt**.{ai_note}"
        )
        actions = _CRITICAL_ACTIONS
    else:
        css_class = "recommendation-safe"
        title_class = "rec-title-safe"
        title = "🟢 SAFE TO PUMP WATER"
        subtitle = (
            f"Salinity **{snapshot['salinity_ppt']:.2f} ppt** is within the safe operating range "
            f"(< {THRESHOLDS['salinity_danger_ppt']} ppt). System operating normally."
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
