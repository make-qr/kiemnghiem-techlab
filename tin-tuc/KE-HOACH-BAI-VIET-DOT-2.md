# Kế hoạch tin tức đợt 2 — map Ads KW → `/tin-tuc/`

**Cập nhật:** 24/07/2026  
**Site:** https://kiemnghiem.techlabglobal.com.vn/tin-tuc/  
**Nguồn KW:** `du-an/nas/nas-apps/04-ads-automation/kiemnghiem_services.json`  
**Đợt 1:** 30/30 bài — xem [`KE-HOACH-BAI-VIET.md`](KE-HOACH-BAI-VIET.md)  
**Cách đăng:** sửa `scripts/news-articles.json` → `python3 scripts/generate-news.py`

---

## 1. Map ad group / cụm KW ↔ bài tin hiện có

| Ad group (Ads) | KW chính | Landing | Bài tin cover | Coverage | Ghi chú |
|----------------|----------|---------|---------------|----------|---------|
| Kiểm nghiệm bánh trung thu | kiểm nghiệm bánh trung thu, test bánh trung thu | `kiem-nghiem-banh-keo` | `chi-tieu-kiem-nghiem-banh-trung-thu` | Đủ nền | Thiếu checklist mùa / deadline gửi mẫu |
| Kiểm nghiệm bánh kẹo | kiểm nghiệm bánh kẹo, bánh quy | `kiem-nghiem-banh-keo` | `kiem-nghiem-banh-keo-mat-ong-dau-an` | Đủ | — |
| Kiểm nghiệm nước uống | kiểm nghiệm nước uống, nước đóng chai | `kiem-nghiem-nuoc-giai-khat` | `kiem-nghiem-nuoc-uong-qcvn` | Đủ nền | Thiếu checklist công bố nước chi tiết |
| Kiểm nghiệm nước giải khát | kiểm nghiệm nước giải khát | `kiem-nghiem-nuoc-giai-khat` | `kiem-nghiem-nuoc-uong-qcvn` | Yếu | Gộp chung nước uống |
| Kiểm nghiệm thực phẩm | kiểm nghiệm thực phẩm, phòng lab TP | `kiem-nghiem-thuc-pham` | vi sinh, kim loại, BVTV, challenge… | Đủ rộng | Thiếu góc thủy sản / OCOP / local |
| Kiểm nghiệm mỹ phẩm | kiểm nghiệm mỹ phẩm | `kiem-nghiem-my-pham` | `kiem-nghiem-my-pham-thong-tu-06` | Đủ | — |
| Kiểm nghiệm dược phẩm | kiểm nghiệm dược phẩm | `kiem-nghiem-duoc-pham` | `kiem-nghiem-tpcn-truoc-cong-bo` | Yếu | Chỉ TPCN, chưa bài dược/GMP |
| Kiểm nghiệm thức ăn chăn nuôi | kiểm nghiệm thức ăn chăn nuôi | `kiem-nghiem-thuc-an-chan-nuoi` | `doc-to-vi-nam-aflatoxin` | Yếu | Aflatoxin thôi; thiếu gói chỉ tiêu TACN |
| Kiểm nghiệm dinh dưỡng | kiểm nghiệm dinh dưỡng, phân tích DD | `kiem-nghiem-dinh-duong` | `phan-tich-dinh-duong-ghi-nhan`, TT29 | Đủ | — |
| Dịch vụ kiểm nghiệm khác (paused Ads) | lab uy tín, kiểm nghiệm chuyên biệt | `dich-vu-kiem-nghiem-khac` | bao bì FCM, VALAS… | Một phần | Không ưu tiên KW rộng |
| Chứng nhận VietGAP | chứng nhận vietgap, vietgap là gì | `chung-nhan-vietgap` | `vietgap-organic-halal-overview` | Yếu | Overview gộp 3 CN |
| Chứng nhận Organic | chứng nhận organic / hữu cơ | `chung-nhan-organic` | overview | Yếu | — |
| Chứng nhận Halal | chứng nhận halal | `chung-nhan-halal` | overview | Yếu | — |
| Chứng nhận HACCP | chứng nhận haccp | `chung-nhan-haccp` | `haccp-va-iso-22000-khac-nhau` | Đủ | — |
| Chứng nhận ISO 22000 | chứng nhận iso 22000 | `chung-nhan-iso-22000` | `haccp-va-iso-22000-khac-nhau` | Đủ | — |
| Chứng nhận SMETA SEDEX | chứng nhận smeta, sedex audit | `chung-nhan-smeta-sedex` | `smeta-sedex-nha-may-thuc-pham` | Đủ | — |
| Quan trắc môi trường | quan trắc môi trường, khí thải, nước thải | `quan-trac-moi-truong` | `dang-ky-moi-truong-vs-quan-trac` | Yếu | Gộp; thiếu bài khí thải / nước thải |
| Tư vấn môi trường | tư vấn MT, ĐTM, hồ sơ MT | `tu-van-moi-truong` | `dang-ky-moi-truong-vs-quan-trac` | Yếu | Thiếu checklist ĐTM |
| *(không có ad group)* | chọn lab ISO 17025 / NLCT | `ho-so-nang-luc` | `valas-217-iso-17025-la-gi` | Yếu | Cần bài “cách chọn lab” |
| *(không có ad group)* | OCOP + kiểm nghiệm | `kiem-nghiem-thuc-pham` | — | **THIẾU** | — |
| *(không có ad group)* | kiểm nghiệm thủy sản xuất khẩu | `kiem-nghiem-thuc-pham` | `du-luong-khang-sinh-thuy-san` | Yếu | Chỉ kháng sinh |
| Local SEO | kiểm nghiệm thực phẩm Hà Nội… | form / nhận mẫu | `nhan-mau-ha-noi-can-tho-hcm` | Yếu | 1 bài nhận mẫu; Ads geo Bắc |

**Ưu tiên viết mới:** P0 mùa vụ → P1 tiền (KW Ads đang chạy, cover yếu/thiếu) → P2 chứng nhận/MT → P3 local.

---

## 2. Đợt 2 — 10 bài đề xuất (đã viết ✅)

| # | Status | Ưu tiên | Slug | Tiêu đề | KW chính | Landing | Tag |
|---|--------|---------|------|---------|----------|---------|-----|
| 31 | ✅ | P0 | `checklist-gui-mau-banh-trung-thu-2026` | Checklist gửi mẫu bánh trung thu 2026: thời hạn & chỉ tiêu trước cao điểm | kiểm nghiệm bánh trung thu | `kiem-nghiem-banh-keo` | Bánh trung thu |
| 32 | ✅ | P1 | `chon-phong-lab-iso-17025-nlct` | Cách chọn phòng lab ISO 17025 / đọc NLCT trước khi gửi mẫu | lab kiểm nghiệm uy tín, ISO 17025 | `ho-so-nang-luc` + thực phẩm | Năng lực lab |
| 33 | ✅ | P1 | `kiem-nghiem-thuy-san-xuat-khau` | Kiểm nghiệm thủy sản xuất khẩu: chỉ tiêu doanh nghiệp hay gặp | kiểm nghiệm thủy sản, dư lượng kháng sinh | `kiem-nghiem-thuc-pham` | Thủy sản |
| 34 | ✅ | P1 | `ocop-kiem-nghiem-va-cong-bo` | OCOP và kiểm nghiệm / công bố sản phẩm: hồ sơ cần những gì? | OCOP kiểm nghiệm, công bố sản phẩm | `kiem-nghiem-thuc-pham` | OCOP |
| 35 | ✅ | P3 | `kiem-nghiem-thuc-pham-ha-noi` | Kiểm nghiệm thực phẩm tại Hà Nội: nhận mẫu, thời gian & báo giá | kiểm nghiệm thực phẩm Hà Nội | `kiem-nghiem-thuc-pham` | Local SEO |
| 36 | ✅ | P2 | `quan-trac-khi-thai-nha-may` | Quan trắc khí thải nhà máy: khi nào bắt buộc và chuẩn bị gì? | quan trắc khí thải | `quan-trac-moi-truong` | Môi trường |
| 37 | ✅ | P2 | `quan-trac-nuoc-thai-dinh-ky` | Quan trắc nước thải định kỳ: chỉ tiêu & chu kỳ doanh nghiệp cần biết | quan trắc nước thải | `quan-trac-moi-truong` | Môi trường |
| 38 | ✅ | P2 | `checklist-ho-so-dtm` | Checklist hồ sơ ĐTM / đánh giá tác động môi trường cho dự án mới | báo cáo đánh giá tác động môi trường | `tu-van-moi-truong` | Môi trường |
| 39 | ✅ | P2 | `chung-nhan-vietgap-quy-trinh` | Chứng nhận VietGAP: quy trình, hồ sơ và vai trò kiểm nghiệm | chứng nhận vietgap, đăng ký vietgap | `chung-nhan-vietgap` | Chứng nhận |
| 40 | ✅ | P1 | `kiem-nghiem-duoc-pham-va-gmp` | Kiểm nghiệm dược phẩm & hỗ trợ hồ sơ GMP: doanh nghiệp cần gì? | kiểm nghiệm dược phẩm | `kiem-nghiem-duoc-pham` | Dược phẩm |

**Cadence đề xuất sau publish:** giữ 3 URL “mới”/tuần trên GSC (đã generate cùng đợt; phân phối index theo ngày trong JSON).

---

## 3. Bài đợt 1 — chỉ refresh (không rewrite đợt này)

| Slug | Lý do | Việc sau 2–3 tuần nếu GSC yếu |
|------|-------|-------------------------------|
| `vietgap-organic-halal-overview` | Mỏng, gộp 3 CN | Thêm H2 sâu hoặc link sang bài VietGAP #39 |
| `dang-ky-moi-truong-vs-quan-trac` | Gộp MT | Link sang #36–#38 |
| `valas-217-iso-17025-la-gi` | Brand | Link sang #32 chọn lab |
| `chi-tieu-kiem-nghiem-banh-trung-thu` | Mùa vụ | Link sang checklist #31 |
| `nhan-mau-ha-noi-can-tho-hcm` | Local mỏng | Link sang #35 HN |

---

## 4. Checklist đo lường (sau 2–3 tuần)

Chạy vào khoảng **07–14/08/2026** (hoặc 14–21 ngày sau push đợt 2).

### Google Search Console

- [ ] Lọc page: `kiemnghiem.techlabglobal.com.vn/tin-tuc/` — so sánh impression/click 28 ngày trước vs sau đợt 2
- [ ] Query gắn KW Ads: `kiểm nghiệm bánh trung thu`, `kiểm nghiệm nước uống`, `kiểm nghiệm thực phẩm`, `chứng nhận vietgap`, `quan trắc khí thải`, `kiểm nghiệm dược phẩm`
- [ ] Query local: `kiểm nghiệm thực phẩm Hà Nội`, `lab kiểm nghiệm Hà Nội`
- [ ] Ghi 3–5 query **vị trí 8–20** (gần top) → ưu tiên làm dày / viết bài bổ sung
- [ ] Kiểm index 10 URL mới (URL Inspection)

### Gemini / GEO smoke test

- [ ] Hỏi 5 câu khớp lead bài mới (bánh TT checklist, chọn lab ISO 17025, thủy sản XK, VietGAP, quan trắc khí thải)
- [ ] Ghi có/không cite `kiemnghiem.techlabglobal.com.vn`

### Conversion

- [ ] GA4/GTM: form submit có `Trang_gửi_form` / page path từ `/tin-tuc/*` đợt 2
- [ ] So sánh lead từ tin vs landing Ads (không đổi final URL Ads)

### Quyết định vòng sau

| Kết quả | Hành động |
|---------|-----------|
| Query gần top trên 1 bài | Làm dày H2 + bảng chỉ tiêu + FAQ |
| Impression cao, CTR thấp | Đổi title/meta |
| Cover KW Ads vẫn yếu | Viết thêm long-tail (nước giải khát riêng, Organic/Halal riêng, TACN gói chỉ tiêu) |
| Lead từ tin thấp | Tăng CTA giữa bài + link landing rõ hơn |

---

## 5. Quy trình (giống đợt 1)

```text
1. Viết / sửa scripts/news-articles.json (đầu mảng = mới nhất)
2. python3 scripts/generate-news.py
3. Mở tin-tuc/<slug>.html kiểm tra link/CTA
4. git commit + push (khi anh yêu cầu)
5. Đánh dấu ✅ trong file này
```

---

*Nguồn theo dõi backlog đợt 2. Không mở blog WP hub trong đợt này.*
