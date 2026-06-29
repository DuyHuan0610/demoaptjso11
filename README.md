# SaltWatch

Hyper-local salinity monitoring and AI forecasting dashboard for the Mekong Delta — Ben Tre Province, Vietnam.

## Features

- **4 IoT sensor stations** across Binh Dai, Ba Tri, Cho Lach, and Thanh Phu
- **Interactive monitoring map** with salinity-based marker status
- **Real-time KPIs**: salinity, pH, water temperature, and connectivity
- **Operational recommendations** — Safe / Critical action cards
- **7-day time series** with AI salinity intrusion forecast
- **AI intrusion alert mode** for predictive scenario analysis

## Quick Start

```powershell
cd saltwatch
pip install -r requirements.txt
streamlit run app.py
```

Open: **http://localhost:8501**

## Requirements

- Python 3.10+
- Streamlit · Plotly · Pandas · NumPy · Folium · streamlit-folium

## Monitoring Stations

| ID    | Location                       | Coordinates (lat, lon) |
|-------|--------------------------------|------------------------|
| SW-01 | Binh Thoi Sluice Gate (Binh Dai) | 10.0684, 106.7128  |
| SW-02 | Ham Luong River (Ba Tri)       | 9.9512, 106.5841       |
| SW-03 | Freshwater Seedling Area (Cho Lach) | 10.2236, 106.6187 |
| SW-04 | Co Chien River Headwaters (Thanh Phu) | 10.0819, 106.5213 |

## Operating Thresholds

- Critical salinity: **≥ 2.0 ppt** (parts per thousand)
- Optimal pH range: **6.5 – 8.5**
