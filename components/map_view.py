"""
Bản đồ tương tác Folium + Carto Dark Matter (miễn phí, không cần API key).
Marker thay đổi kích thước/màu theo trạm đang chọn và trạng thái độ mặn.
"""

import folium
import streamlit as st
from streamlit_folium import st_folium

from config.settings import MAP_CONFIG, THRESHOLDS
from config.stations import STATIONS, get_station_ids
from data.simulation import get_all_stations_snapshots
from state.session_manager import get_active_station_id, get_simulation_mode, set_active_station

# Tile Carto Dark Matter — CDN công khai, không yêu cầu đăng ký hay thẻ tín dụng
CARTO_DARK_TILES = "CartoDB dark_matter"


def _build_folium_map(snapshots: dict, active_id: str) -> folium.Map:
    """Xây dựng bản đồ Folium với marker động và tooltip tùy chỉnh."""
    m = folium.Map(
        location=[MAP_CONFIG["center_lat"], MAP_CONFIG["center_lon"]],
        zoom_start=int(MAP_CONFIG["zoom"]),
        tiles=CARTO_DARK_TILES,
        attr=(
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
            '&copy; <a href="https://carto.com/attributions">CARTO</a>'
        ),
    )

    for sid, station in STATIONS.items():
        snap = snapshots[sid]
        is_active = sid == active_id
        is_danger = snap["salinity_ppt"] >= THRESHOLDS["salinity_danger_ppt"]
        color = "#ef4444" if is_danger else "#22c55e"
        radius = 16 if is_active else 9
        weight = 4 if is_active else 2

        tooltip_html = (
            f"<b>{sid}</b> ({station['name']})<br>"
            f"Độ mặn: {snap['salinity_ppt']:.2f} ‰<br>"
            f"Kết nối: {'Online' if snap['connectivity'] == 'online' else 'Offline'}"
        )
        popup_html = (
            f"<div style='min-width:180px'>"
            f"<b>{sid}</b> — {station['name']}<br>"
            f"📍 {station['location_label']}<br>"
            f"Độ mặn: <b>{snap['salinity_ppt']:.2f} ‰</b><br>"
            f"pH: {snap['ph']:.2f} | "
            f"Nhiệt độ: {snap['temperature_c']:.1f}°C"
            f"</div>"
        )

        # Vòng glow nhẹ cho trạm đang chọn
        if is_active:
            folium.CircleMarker(
                location=[station["latitude"], station["longitude"]],
                radius=radius + 8,
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.18,
            ).add_to(m)

        folium.CircleMarker(
            location=[station["latitude"], station["longitude"]],
            radius=radius,
            color="#ffffff" if is_active else color,
            weight=weight,
            fill=True,
            fill_color=color,
            fill_opacity=0.92,
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
            popup=folium.Popup(popup_html, max_width=280),
        ).add_to(m)

    return m


def _handle_map_click(map_data: dict | None) -> None:
    """Đồng bộ trạm khi người dùng click marker trên bản đồ."""
    if not map_data or not map_data.get("last_object_clicked"):
        return

    clicked = map_data["last_object_clicked"]
    click_lat = clicked.get("lat")
    click_lng = clicked.get("lng")
    if click_lat is None or click_lng is None:
        return

    for sid, station in STATIONS.items():
        if (
            abs(station["latitude"] - click_lat) < 0.002
            and abs(station["longitude"] - click_lng) < 0.002
        ):
            if sid != get_active_station_id():
                set_active_station(sid)
                st.rerun()
            break


def render_map_and_nav() -> None:
    """Render bản đồ và hàng nút chuyển trạm nhanh."""
    mode = get_simulation_mode()
    active_id = get_active_station_id()
    snapshots = get_all_stations_snapshots(mode)

    st.markdown("#### 🗺️ Bản đồ trạm giám sát — Bến Tre")
    st.caption("Bản đồ Carto Dark Matter · OpenStreetMap — miễn phí, không cần API key")

    folium_map = _build_folium_map(snapshots, active_id)
    map_output = st_folium(
        folium_map,
        width=None,
        height=420,
        returned_objects=["last_object_clicked"],
        use_container_width=True,
        key="station_map",
    )
    _handle_map_click(map_output)

    st.markdown("##### Chuyển trạm nhanh")
    station_ids = get_station_ids()
    cols = st.columns(len(station_ids))

    for idx, sid in enumerate(station_ids):
        station = STATIONS[sid]
        snap = snapshots[sid]
        is_active = sid == active_id
        danger_tag = " 🔴" if snap["is_dangerous"] else " 🟢"

        with cols[idx]:
            if st.button(
                f"{sid}{danger_tag}",
                key=f"nav_{sid}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=station["location_label"],
            ):
                set_active_station(sid)
                st.rerun()
