"""Global session state management via st.session_state."""

from typing import Literal

import streamlit as st

from config.stations import get_station_ids

SimulationMode = Literal["normal", "alert"]


def init_session_state() -> None:
    """Initialize session state with default values."""
    defaults: dict[str, str] = {
        "active_station_id": get_station_ids()[0],
        "simulation_mode": "normal",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_active_station_id() -> str:
    """Return the currently selected station ID."""
    init_session_state()
    return st.session_state.active_station_id


def set_active_station(station_id: str) -> None:
    """Update the active station — all components rerender in sync."""
    init_session_state()
    if station_id in get_station_ids():
        st.session_state.active_station_id = station_id


def get_simulation_mode() -> SimulationMode:
    """Return the current alert mode (normal | alert)."""
    init_session_state()
    return st.session_state.simulation_mode  # type: ignore[return-value]


def set_simulation_mode(mode: SimulationMode) -> None:
    """Switch between normal conditions and AI intrusion alert."""
    init_session_state()
    st.session_state.simulation_mode = mode
