"""
Biểu đồ chuỗi thời gian độ mặn 7 ngày + dự báo AI.
Sử dụng plotly.graph_objects với nền dark và đường ngưỡng nguy hiểm.
"""

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
    """Layout chung cho biểu đồ dark-mode."""
    return dict(
        title=dict(text=title, font=dict(color="#e2e8f0", size=16)),
        xaxis=dict(
            title="Thời gian",
            color="#94a3b8",
            gridcolor="rgba(148, 163, 184, 0.12)",
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="Độ mặn (‰)",
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
    """Render biểu đồ lịch sử 7 ngày và dự báo AI (khi ở chế độ alert)."""
    station_id = get_active_station_id()
    mode = get_simulation_mode()

    historical = generate_historical_series(station_id, mode)
    snapshot = build_station_snapshot(station_id, mode)

    fig = go.Figure()

    # ── Dữ liệu lịch sử: đường xanh liền nét + marker ──
    fig.add_trace(
        go.Scatter(
            x=historical["timestamp"],
            y=historical["salinity_ppt"],
            mode="lines+markers",
            name="Dữ liệu IoT (7 ngày)",
            line=dict(color="#38bdf8", width=2.5),
            marker=dict(size=6, color="#38bdf8", line=dict(width=1, color="#0ea5e9")),
        )
    )

    # ── Đường ngưỡng nguy hiểm ──
    fig.add_hline(
        y=THRESHOLDS["salinity_danger_ppt"],
        line_dash="dash",
        line_color="#ef4444",
        line_width=2,
        annotation_text=f"Ngưỡng nguy hiểm ({THRESHOLDS['salinity_danger_ppt']} ‰)",
        annotation_position="top right",
        annotation_font_color="#f87171",
    )

    # ── Dự báo AI: chỉ hiển thị khi chế độ alert ──
    if mode == "alert":
        last_value = float(historical["salinity_ppt"].iloc[-1])
        forecast = generate_forecast_series(station_id, last_value)

        fig.add_trace(
            go.Scatter(
                x=forecast["timestamp"],
                y=forecast["salinity_ppt"],
                mode="lines+markers",
                name="Dự báo AI (7 ngày tới)",
                line=dict(color="#f97316", width=2.5, dash="dash"),
                marker=dict(
                    size=8,
                    symbol="diamond",
                    color="#ef4444",
                    line=dict(width=1, color="#fbbf24"),
                ),
            )
        )

        # Đánh dấu đỉnh dự báo
        peak_idx = forecast["salinity_ppt"].idxmax()
        peak_val = forecast.loc[peak_idx, "salinity_ppt"]
        peak_time = forecast.loc[peak_idx, "timestamp"]
        fig.add_annotation(
            x=peak_time,
            y=peak_val,
            text=f"Đỉnh dự báo: {peak_val:.2f} ‰",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#f97316",
            font=dict(color="#fb923c", size=11),
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor="#f97316",
        )

    chart_title = (
        f"Chuỗi thời gian độ mặn — {station_id} "
        f"(Hiện tại: {snapshot['salinity_ppt']:.2f} ‰)"
    )
    fig.update_layout(**_dark_chart_layout(chart_title), height=420)

    st.plotly_chart(fig, use_container_width=True, key="timeseries_chart")
