# TechLAB Global — Kiểm nghiệm & Chứng nhận

Mã nguồn trang landing page **kiemnghiem.techlabglobal.com.vn** — giới thiệu dịch vụ kiểm nghiệm (phòng thử nghiệm ISO/IEC 17025) và chứng nhận của TechLAB Global.

**Hotline:** 0899.551.228 | **Email:** info@techlabglobal.com.vn

## Cấu trúc dự án

```
kiemnghiem-techlab/
├── index.html              # Trang chủ + form báo giá
├── ho-so-nang-luc.html     # Hồ sơ năng lực phòng thử nghiệm online
├── thank-you.html          # Trang cảm ơn sau khi gửi form
├── css/
│   ├── style.css           # CSS chính
│   ├── service-page.css    # Layout trang dịch vụ
│   ├── conversion.css      # Sticky CTA, form báo giá
│   └── ho-so-nang-luc.css  # Hồ sơ năng lực
├── js/
│   ├── main.js             # Smooth scroll, FAQ accordion
│   ├── conversion.js       # Prefill form, Google Ads conversion events
│   ├── ho-so-nang-luc.js   # Lightbox, gallery tabs
│   ├── tracking-bootstrap.js  # dataLayer + gtag config
│   └── meta-pixel.js       # Meta Pixel retarget (4620520364845904)
├── images/
│   ├── ho-so-nang-luc/     # Tài liệu public (chứng nhận, lab, PDF)
│   └── tai-lieu/           # Kho tài liệu gốc (không link trực tiếp)
├── pages/                  # Trang dịch vụ & chứng nhận
├── sitemap.xml
└── robots.txt
```

## Trang ưu tiên chuyển đổi

- Kiểm nghiệm Bánh Trung thu / Bánh các loại
- Kiểm nghiệm Nước sạch / Nước uống
- Kiểm nghiệm Thực phẩm, Mỹ phẩm, Dược phẩm

Mỗi trang có: hero CTA (Gọi + Zalo), form báo giá nhanh, FAQ, sticky bar mobile.

## Form liên hệ

Form gửi qua [FormSubmit](https://formsubmit.co/) — endpoint cấu hình trong HTML. Sau gửi thành công chuyển tới `thank-you.html`.

## Chạy local

Mở `index.html` trong trình duyệt hoặc dùng static server:

```bash
npx serve .
```

## Lưu ý

- Thư mục `pages_template/` chỉ là bản nháp cũ — **không deploy** lên hosting.
- Chỉ deploy: `index.html`, `ho-so-nang-luc.html`, `thank-you.html`, `privacy-policy.html`, `css/`, `js/`, `images/`, `pages/`, `robots.txt`, `sitemap.xml`.
- Thư mục `images/tai-lieu/` là kho gốc — web dùng `images/ho-so-nang-luc/` (đã lọc, đổi tên).

## Tracking (GA4, GTM, Google Ads, Meta Pixel)

Xem **[HUONG-DAN-TRACKING.md](HUONG-DAN-TRACKING.md)**.

Sau khi đổi ID GTM/Pixel:

```bash
python3 scripts/apply-tracking.py
```

## Deploy

Upload các file production ở trên, trỏ domain `kiemnghiem.techlabglobal.com.vn` (CNAME). Submit `sitemap.xml` lên Google Search Console.
