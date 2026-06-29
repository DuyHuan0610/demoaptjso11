# SaltWatch

Dashboard giám sát độ mặn siêu cục bộ và dự báo AI cho vùng Đồng bằng sông Cửu Long — tỉnh Bến Tre, Việt Nam.

## Tính năng

- **4 trạm IoT** tại Bình Đại, Ba Tri, Chợ Lách, Thạnh Phú
- **Bản đồ Carto Dark Matter** (OpenStreetMap) — miễn phí, không API key
- **KPI grid** 4 cột: độ mặn, pH, nhiệt độ, metadata trạm
- **Engine khuyến nghị** Safe / Critical với hành động cụ thể
- **Biểu đồ chuỗi thời gian** 7 ngày + dự báo AI 7 ngày (chế độ alert)
- **Toggle mô phỏng** Normal ↔ AI Salinity Intrusion Alert

## Chạy trên máy local (Windows)

### Bước 1 — Mở terminal tại thư mục dự án

```powershell
cd C:\Users\Tom\Projects\saltwatch
```

### Bước 2 — Tạo môi trường ảo (khuyến nghị)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Bước 3 — Cài dependencies

```powershell
pip install -r requirements.txt
```

### Bước 4 — Khởi chạy

```powershell
streamlit run app.py
```

Trình duyệt sẽ mở tại **http://localhost:8501**.

> **Không cần Mapbox token.** Bản đồ dùng tile Carto Dark Matter qua Folium/OpenStreetMap.

---

## Deploy lên internet (miễn phí) — Streamlit Community Cloud

Cách nhanh nhất để “landing” dự án public:

### 1. Đẩy code lên GitHub

```powershell
cd C:\Users\Tom\Projects\saltwatch
git init
git add .
git commit -m "Initial SaltWatch dashboard"
```

Tạo repo mới trên [github.com/new](https://github.com/new) (ví dụ: `saltwatch`), rồi:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/saltwatch.git
git branch -M main
git push -u origin main
```

### 2. Deploy trên Streamlit Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng GitHub.
2. Chọn **New app**.
3. Chọn repo `saltwatch`, branch `main`, main file **`app.py`**.
4. Nhấn **Deploy**.

Sau ~2 phút bạn có URL dạng: `https://saltwatch-xxxxx.streamlit.app`

### 3. Kiểm tra sau deploy

- [ ] Bản đồ hiển thị tile tối Carto
- [ ] 4 nút chuyển trạm hoạt động
- [ ] Toggle AI Alert cập nhật KPI + biểu đồ forecast
- [ ] Không có lỗi trong Streamlit logs

---

## Cấu trúc dự án

```
saltwatch/
├── app.py                 # Entry point
├── requirements.txt
├── .streamlit/config.toml # Theme dark
├── config/                # Cấu hình & dữ liệu trạm
├── state/                 # Quản lý st.session_state
├── data/                  # Mô phỏng IoT & dự báo AI
├── components/            # UI components modular
└── styles/                # CSS dark-mode theme
```

## Yêu cầu

- Python 3.10+
- Streamlit, Plotly, Pandas, NumPy, Folium, streamlit-folium

## Trạm giám sát

| ID    | Vị trí                          | Tọa độ (lat, lon)   |
|-------|---------------------------------|---------------------|
| SW-01 | Cửa đập Bình Thới (Bình Đại)   | 10.0684, 106.7128   |
| SW-02 | Sông Hàm Luông (Ba Tri)         | 9.9512, 106.5841    |
| SW-03 | Khu ươm giống (Chợ Lách)        | 10.2236, 106.6187   |
| SW-04 | Đầu nguồn Cổ Chiên (Thạnh Phú)  | 10.0819, 106.5213   |

## Ghi chú

- Ngưỡng độ mặn nguy hiểm: **≥ 2.0 ‰**
- Bật toggle **AI Predicted Salinity Intrusion Alert** trên sidebar để xem dự báo và cảnh báo Critical

Xem thêm chi tiết deploy: [DEPLOY.md](DEPLOY.md)
