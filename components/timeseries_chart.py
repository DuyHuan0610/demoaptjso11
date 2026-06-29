"""Salinity time-series chart with 7-day history and AI forecast."""

import plotly.graph_objects as go
import streamlit as st

from config.settings import THRESHOLDS
from data.simulation import (
    build_station_snapshot,
    generate_forecast_series,
    generate_historical_series,
)
from state.session_manager import get_active_station_id, get_simulation_mode


def _dark_chart_layout(title: str) -> dict:
    """Shared dark-mode chart layout."""
    return dict(
        title=dict(text=title, font=dict(color="#e2e8f0", size=16)),
        xaxis=dict(
            title="Time",
            color="#94a3b8",
            gridcolor="rgba(148, 163, 184, 0.12)",
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="Salinity (ppt)",
            color="#94a3b8",
            gridcolor="rgba(148, 163, 184, 0.12)",
            showgrid=True,
            zeroline=False,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(color="#cbd5e1"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
        ),
        margin=dict(l=50, r=20, t=50, b=40),
        hovermode="x unified",
    )


def render_timeseries_chart() -> None:
    """Render 7-day historical chart and AI forecast when alert mode is active."""
    station_id = get_active_station_id()
    mode = get_simulation_mode()

    historical = generate_historical_series(station_id, mode)
    snapshot = build_station_snapshot(station_id, mode)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical["timestamp"],
            y=historical["salinity_ppt"],
            mode="lines+markers",
            name="IoT Readings (7 days)",
            line=dict(color="#38bdf8", width=2.5),
            marker=dict(size=6, color="#38bdf8", line=dict(width=1, color="#0ea5e9")),
        )
    )

    fig.add_hline(
        y=THRESHOLDS["salinity_danger_ppt"],
        line_dash="dash",
        line_color="#ef4444",
        line_width=2,
        annotation_text=f"Danger Threshold ({THRESHOLDS['salinity_danger_ppt']} ppt)",
        annotation_position="top right",
        annotation_font_color="#f87171",
    )

    if mode == "alert":
        last_value = float(historical["salinity_ppt"].iloc[-1])
        forecast = generate_forecast_series(station_id, last_value)

        fig.add_trace(
            go.Scatter(
                x=forecast["timestamp"],
                y=forecast["salinity_ppt"],
                mode="lines+markers",
                name="AI Forecast (7-day outlook)",
                line=dict(color="#f97316", width=2.5, dash="dash"),
                marker=dict(
                    size=8,
                    symbol="diamond",
                    color="#ef4444",
                    line=dict(width=1, color="#fbbf24"),
                ),
            )
        )

        peak_idx = forecast["salinity_ppt"].idxmax()
        peak_val = forecast.loc[peak_idx, "salinity_ppt"]
        peak_time = forecast.loc[peak_idx, "timestamp"]
        fig.add_annotation(
            x=peak_time,
            y=peak_val,
            text=f"Forecast peak: {peak_val:.2f} ppt",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#f97316",
            font=dict(color="#fb923c", size=11),
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor="#f97316",
        )

    chart_title = (
        f"Salinity Time Series — {station_id} "
        f"(Current: {snapshot['salinity_ppt']:.2f} ppt)"
    )
    fig.update_layout(**_dark_chart_layout(chart_title), height=420)

    st.plotly_chart(fig, use_container_width=True, key="timeseries_chart")
