# Tracking — TechLAB Kiểm nghiệm (`kiemnghiem.techlabglobal.com.vn`)

> Cập nhật: 25/06/2026  
> Repo: [make-qr/kiemnghiem-techlab](https://github.com/make-qr/kiemnghiem-techlab)

## ID đang dùng

| Công cụ | ID |
|---------|-----|
| **GTM** | `GTM-MRHPPTJ7` |
| **GA4** | `G-4YE334L4TV` |
| **Google Ads** | `AW-18270406607` |
| **Meta Pixel** | `4620520364845904` |
| **Domain** | `kiemnghiem.techlabglobal.com.vn` |

## Trên website (repo)

| File | Vai trò |
|------|---------|
| `js/tracking-bootstrap.js` | `dataLayer`, `gtag`, config `TLG_TRACKING` |
| `js/meta-pixel.js` | Meta Pixel PageView + Lead trên `thank-you.html` |
| `js/conversion.js` | Google Ads conversion: form, thank-you, gọi, Zalo |
| `scripts/apply-tracking.py` | Đồng bộ snippet `<head>` cho mọi trang production |

Chạy lại sau khi sửa template tracking:

```bash
python3 scripts/apply-tracking.py
```

## GTM — cài lại container (domain TechLAB)

Container cũ có thể còn tag/trigger cho `natekvn.com`. Trên site đã gắn **Meta Pixel trực tiếp** (không phụ thuộc GTM).

### Cách A — Giữ `GTM-MRHPPTJ7`, dọn trong UI

1. [tagmanager.google.com](https://tagmanager.google.com) → container `GTM-MRHPPTJ7`
2. Xóa/sửa tag trigger URL `natekvn`
3. Thêm (nếu chưa có):
   - **GA4 Configuration** → `G-4YE334L4TV`
   - **Google Ads Conversion Linker** → domain `kiemnghiem.techlabglobal.com.vn`
4. **Xuất bản**

### Cách B — Container mới (khuyên khi muốn sạch)

1. Tạo container mới: **TechLAB Kiểm nghiệm** → URL `https://kiemnghiem.techlabglobal.com.vn`
2. Import file `scripts/gtm-techlab-container.json` (nếu có) hoặc tạo tag thủ công như trên
3. Đổi `GTM-MRHPPTJ7` → ID mới trong `scripts/apply-tracking.py` → chạy lại script
4. Push repo

### Cách C — GTM API (tự động)

```bash
cd ~/huong-dan/du-an/nas/nas-apps/04-ads-automation
python3 gtm-oauth-once.py   # OAuth 1 lần, cần browser
```

## GA4

1. [analytics.google.com](https://analytics.google.com) → property `G-4YE334L4TV`
2. **Luồng dữ liệu** → stream web → URL: `https://kiemnghiem.techlabglobal.com.vn`

## Meta retarget (Facebook)

1. **Trình quản lý sự kiện** → Pixel `4620520364845904` → **Kiểm tra sự kiện**
2. Mở site → *Lượt xem trang*
3. Gửi form → `thank-you.html` → *Khách hàng tiềm năng*
4. **Đối tượng** → Website 30 ngày; loại trừ Lead 30 ngày

## Test nhanh

- Extension **Meta Pixel Helper** + **Tag Assistant**
- Gửi form test → trang cảm ơn
- `nas "báo cáo meta ads 7 ngày"` (NAS)
