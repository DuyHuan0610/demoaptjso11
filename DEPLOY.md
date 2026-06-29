# Hướng dẫn Landing SaltWatch

Tài liệu này mô tả 3 cách đưa SaltWatch lên môi trường thực tế — từ máy cá nhân đến URL public miễn phí.

---

## Option A — Chạy local (phát triển & demo nội bộ)

**Thời gian:** ~5 phút  
**Chi phí:** Miễn phí  
**Phù hợp:** Demo cho team, kiểm thử trước khi deploy

```powershell
cd C:\Users\Tom\Projects\saltwatch
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Mở trình duyệt: **http://localhost:8501**

### Xử lý lỗi thường gặp

| Lỗi | Cách xử lý |
|-----|------------|
| `streamlit` không nhận lệnh | Dùng `python -m streamlit run app.py` |
| PowerShell chặn Activate.ps1 | Chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Bản đồ trống | Kiểm tra kết nối internet (tile tải từ CDN Carto/OSM) |
| Port 8501 bận | `streamlit run app.py --server.port 8502` |

---

## Option B — Streamlit Community Cloud (khuyến nghị cho landing public)

**Thời gian:** ~15 phút  
**Chi phí:** Miễn phí  
**URL:** `https://your-app.streamlit.app`

### Checklist trước khi deploy

- [ ] File `requirements.txt` đầy đủ
- [ ] Entry point là `app.py` ở root repo
- [ ] Không commit file `.env` chứa secret (dự án này không cần API key bản đồ)
- [ ] Repo public hoặc bạn có quyền kết nối Streamlit Cloud với repo private

### Các bước

1. **Khởi tạo Git** (nếu chưa có):

   ```powershell
   cd C:\Users\Tom\Projects\saltwatch
   git init
   git add .
   git commit -m "SaltWatch production dashboard"
   ```

2. **Tạo GitHub repo** tại https://github.com/new

3. **Push code:**

   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/saltwatch.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy:**
   - https://share.streamlit.io → **Create app**
   - Repository: `YOUR_USERNAME/saltwatch`
   - Branch: `main`
   - Main file path: `app.py`
   - **Deploy!**

5. **Chia sẻ URL** với stakeholders — app tự redeploy khi bạn push lên `main`.

### Cấu hình Streamlit (đã có sẵn)

File `.streamlit/config.toml` đặt theme dark corporate. Streamlit Cloud đọc file này tự động.

---

## Option C — Docker (VPS / server riêng)

**Thời gian:** ~20 phút  
**Chi phí:** VPS từ ~$5/tháng (DigitalOcean, Hetzner, v.v.)  
**Phù hợp:** Production nội bộ, reverse proxy, domain riêng

Tạo `Dockerfile` (nếu cần, thêm vào repo):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

Build & run:

```bash
docker build -t saltwatch .
docker run -p 8501:8501 saltwatch
```

Truy cập: **http://SERVER_IP:8501**

---

## Bản đồ — không cần Mapbox

SaltWatch dùng:

| Thành phần | Nguồn | API key |
|------------|-------|---------|
| Tile nền | Carto Dark Matter | Không |
| Dữ liệu địa lý | OpenStreetMap | Không |
| Thư viện | Folium + streamlit-folium | Không |

Attribution bắt buộc (đã embed trong map): © OpenStreetMap, © CARTO.

---

## Demo flow cho stakeholder

1. Mở app → xem 4 KPI và bản đồ Bến Tre
2. Click **SW-02** → toàn bộ dashboard đồng bộ sang trạm Ba Tri
3. Bật **AI Predicted Salinity Intrusion Alert** → thẻ đỏ Critical + đường forecast cam trên biểu đồ
4. Tắt alert → trở về trạng thái Safe xanh

---

## Bước tiếp theo (production thật)

Khi chuyển từ demo sang hệ thống thật:

1. Thay `data/simulation.py` bằng API MQTT/REST từ cảm biến IoT
2. Lưu lịch sử vào PostgreSQL / TimescaleDB
3. Thay forecast giả lập bằng model ML đã train (Prophet, LSTM, v.v.)
4. Thêm auth (Streamlit-Authenticator hoặc OAuth phía reverse proxy)
