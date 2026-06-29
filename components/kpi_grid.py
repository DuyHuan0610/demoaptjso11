"""Four-column KPI grid: salinity, pH, temperature, and station metadata."""

import streamlit as st

from config.settings import THRESHOLDS
from config.stations import get_station
from data.simulation import build_station_snapshot
from state.session_manager import get_active_station_id, get_simulation_mode


def _salinity_color(value: float) -> str:
    """Return hex color based on salinity level."""
    if value >= THRESHOLDS["salinity_danger_ppt"]:
        return "#f87171"
    if value >= THRESHOLDS["salinity_danger_ppt"] * 0.75:
        return "#fbbf24"
    return "#34d399"


def _ph_label_and_color(ph: float) -> tuple[str, str]:
    """Classify pH as Acidic, Optimal, or Alkaline."""
    if ph < THRESHOLDS["ph_acidic_max"]:
        return "Acidic", "#fbbf24"
    if ph > THRESHOLDS["ph_alkaline_min"]:
        return "Alkaline", "#60a5fa"
    return "Optimal", "#34d399"


def render_kpi_grid() -> None:
    """Render the 4-column KPI metrics for the active station."""
    station_id = get_active_station_id()
    mode = get_simulation_mode()
    station = get_station(station_id)
    snapshot = build_station_snapshot(station_id, mode)

    sal_color = _salinity_color(snapshot["salinity_ppt"])
    ph_label, ph_color = _ph_label_and_color(snapshot["ph"])
    conn_icon = "🟢" if snapshot["connectivity"] == "online" else "🔴"
    conn_text = "Connected" if snapshot["connectivity"] == "online" else "Offline"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Water Salinity",
            value=f"{snapshot['salinity_ppt']:.2f} ppt",
            delta="Above threshold" if snapshot["is_dangerous"] else "Within limit",
            delta_color="inverse" if snapshot["is_dangerous"] else "normal",
        )
        st.markdown(
            f"<p style='color:{sal_color};font-size:0.8rem;margin-top:-0.5rem;'>"
            f"{'⚠ Critical' if snapshot['is_dangerous'] else '✓ Safe'}</p>",
            unsafe_allow_html=True,
        )

    with col2:
        st.metric(
            label="Water pH",
            value=f"{snapshot['ph']:.2f}",
            delta=ph_label,
        )
        st.markdown(
            f"<p style='color:{ph_color};font-size:0.8rem;margin-top:-0.5rem;'>"
            f"{'⚠ Acidic' if ph_label == 'Acidic' else '⚠ Alkaline' if ph_label == 'Alkaline' else '✓ Optimal'}</p>",
            unsafe_allow_html=True,
        )

    with col3:
        st.metric(
            label="Water Temperature",
            value=f"{snapshot['temperature_c']:.1f} °C",
            delta=None,
        )

    with col4:
        st.metric(
            label="Active Station",
            value=station["id"],
            delta=conn_text,
        )
        st.markdown(
            f"<p style='color:#94a3b8;font-size:0.78rem;margin-top:-0.5rem;'>"
            f"{conn_icon} {station['location_label']}</p>",
            unsafe_allow_html=True,
        )
