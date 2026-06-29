# SaltWatch

Hệ thống giám sát độ mặn siêu cục bộ và dự báo AI cho Đồng bằng sông Cửu Long — tỉnh Bến Tre, Việt Nam.

## Tính năng

- Giám sát **4 trạm IoT** tại Bình Đại, Ba Tri, Chợ Lách, Thạnh Phú
- **Bản đồ tương tác** với marker theo trạng thái độ mặn
- **KPI thời gian thực**: độ mặn, pH, nhiệt độ, trạng thái kết nối
- **Khuyến nghị vận hành** Safe / Critical
- **Biểu đồ chuỗi thời gian** 7 ngày + dự báo AI 7 ngày
- **Cảnh báo xâm nhập mặn** theo mô hình AI

## Khởi chạy

```powershell
cd saltwatch
pip install -r requirements.txt
streamlit run app.py
```

Truy cập: **http://localhost:8501**

## Yêu cầu hệ thống

- Python 3.10+
- Streamlit · Plotly · Pandas · NumPy · Folium · streamlit-folium

## Trạm giám sát

| ID    | Vị trí                         | Tọa độ (lat, lon)  |
|-------|--------------------------------|--------------------|
| SW-01 | Cửa đập Bình Thới (Bình Đại)  | 10.0684, 106.7128  |
| SW-02 | Sông Hàm Luông (Ba Tri)        | 9.9512, 106.5841   |
| SW-03 | Khu ươm giống (Chợ Lách)       | 10.2236, 106.6187  |
| SW-04 | Đầu nguồn Cổ Chiên (Thạnh Phú) | 10.0819, 106.5213  |

## Ngưỡng vận hành

- Độ mặn nguy hiểm: **≥ 2.0 ‰**
- pH tối ưu: **6.5 – 8.5**
