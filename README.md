# TechLAB Global — Kiểm nghiệm & Chứng nhận

Mã nguồn trang landing page **kiemnghiem.techlabglobal.com.vn** — giới thiệu dịch vụ kiểm nghiệm (phòng thử nghiệm ISO/IEC 17025) và chứng nhận của TechLAB Global.

**Hotline:** 0899.551.228 | **Email:** info@techlabglobal.com.vn

## Cấu trúc dự án

```
kiemnghiem-techlab/
├── index.html              # Trang chủ + form báo giá
├── thank-you.html          # Trang cảm ơn sau khi gửi form
├── css/
│   ├── style.css           # CSS chính
│   ├── service-page.css    # Layout trang dịch vụ
│   └── conversion.css      # Sticky CTA, form báo giá
├── js/
│   ├── main.js             # Smooth scroll, FAQ accordion
│   └── conversion.js       # Prefill form, tracking GTM
├── images/
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
- Chỉ deploy: `index.html`, `thank-you.html`, `privacy-policy.html`, `css/`, `js/`, `images/`, `pages/`, `robots.txt`, `sitemap.xml`.

## Deploy

Upload các file production ở trên, trỏ domain `kiemnghiem.techlabglobal.com.vn` (CNAME). Submit `sitemap.xml` lên Google Search Console.
