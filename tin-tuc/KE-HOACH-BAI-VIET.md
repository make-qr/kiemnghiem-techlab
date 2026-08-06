# Kế hoạch viết tin tức — kiemnghiem.techlabglobal.com.vn

**Cập nhật:** 20/07/2026  
**Mục tiêu:** Đủ cụm kiến thức kiểm nghiệm để SEO + GEO (Gemini), dẫn về form báo giá / landing dịch vụ.  
**Cách đăng:** sửa `scripts/news-articles.json` → chạy `python3 scripts/generate-news.py` → commit/push.

---

## 1. Đã đăng (P0) — 6/6 ✅

| # | Slug | Tiêu đề | Ngày |
|---|------|---------|------|
| 1 | `vi-sao-kiem-nghiem-bao-bi-tiep-xuc-thuc-pham` | Vì sao phải kiểm nghiệm bao bì tiếp xúc thực phẩm | 20/07 |
| 2 | `chi-tieu-kiem-nghiem-banh-trung-thu` | Chỉ tiêu kiểm nghiệm bánh trung thu mùa cao điểm | 20/07 |
| 3 | `ghi-nhan-dinh-duong-thong-tu-29-2023` | Ghi nhãn dinh dưỡng theo TT 29/2023 | 19/07 |
| 4 | `valas-217-iso-17025-la-gi` | VALAS 217 / ISO 17025 là gì? | 19/07 |
| 5 | `cong-bo-hop-nhua-dung-thuc-pham` | Công bố hộp nhựa đựng thực phẩm | 18/07 |
| 6 | `tu-cong-bo-san-pham-va-phieu-kiem-nghiem` | Tự công bố & phiếu kiểm nghiệm | 18/07 |

**URL mục lục:** https://kiemnghiem.techlabglobal.com.vn/tin-tuc/


> **Cập nhật 20/07/2026:** Đã viết và publish toàn bộ 24 bài còn lại trong một đợt.

---

## 2. Nguyên tắc viết (áp dụng mọi bài)

| Hạng mục | Quy ước |
|----------|---------|
| Độ dài | 800–1.200 chữ (lead 2–3 câu trả lời thẳng) |
| Cấu trúc | Lead → H2 giải thích → bảng/list chỉ tiêu → TechLAB hỗ trợ → CTA |
| Cite bắt buộc | ISO/IEC 17025, VALAS 217, hotline 0899.551.228, HN·CT·HCM |
| Internal link | ≥1 link tới landing `pages/*.html` liên quan |
| CTA | Form báo giá + gọi điện |
| Không | Copy Eurofins / đối thủ; không hứa chỉ tiêu ngoài năng lực lab |
| GEO | Câu đầu trả lời đúng câu hỏi Gemini; FAQ-friendly H2 |

**Template H2 gợi ý:**  
1) [Chủ đề] là gì / vì sao cần?  
2) Chỉ tiêu / quy chuẩn thường gặp  
3) Doanh nghiệp chuẩn bị gì khi gửi mẫu?  
4) TechLAB hỗ trợ thế nào?

---

## 3. Toàn bộ backlog — đã đăng đủ (24/24) ✅

### Đợt B — P1 cốt lõi SEO/lead (10 bài) · ưu tiên cao

| # | Status | Slug đề xuất | Tiêu đề | Tag | Link landing | Tuần dự kiến |
|---|--------|--------------|---------|-----|--------------|--------------|
| 7 | ✅ | `kiem-nghiem-vi-sinh-thuc-pham` | Vi sinh thực phẩm: Coliform, E. coli, Salmonella — đọc kết quả thế nào? | Vi sinh | `kiem-nghiem-thuc-pham` | T28 (21–25/07) |
| 8 | ✅ | `kim-loai-nang-trong-thuc-pham` | Kim loại nặng trong thực phẩm (Pb, Cd, As, Hg): khi nào bắt buộc kiểm? | Hóa lý | `kiem-nghiem-thuc-pham` | T28 |
| 9 | `du-luong-thuoc-bvtv-rau-cu` | Dư lượng thuốc BVTV trên rau củ quả | Nông sản | `kiem-nghiem-thuc-pham` | T28 |
| 10 | ✅ | `doc-to-vi-nam-aflatoxin` | Độc tố vi nấm (aflatoxin) trong ngũ cốc, hạt, thức ăn chăn nuôi | Mycotoxin | `kiem-nghiem-thuc-an-chan-nuoi` | T29 |
| 11 | ✅ | `du-luong-khang-sinh-thuy-san` | Dư lượng kháng sinh / thuốc thú y trong thịt, thủy sản, sữa | An toàn TP | `kiem-nghiem-thuc-pham` | T29 |
| 12 | ✅ | `phan-tich-dinh-duong-ghi-nhan` | Phân tích dinh dưỡng để ghi nhãn: protein, lipid, carb, năng lượng | Dinh dưỡng | `kiem-nghiem-dinh-duong` | T29 |
| 13 | ✅ | `challenge-test-va-han-su-dung` | Challenge test & đánh giá hạn sử dụng — khác kiểm nghiệm thường chỗ nào? | Shelf-life | `kiem-nghiem-thuc-pham` | T30 |
| 14 | ✅ | `kiem-nghiem-tpcn-truoc-cong-bo` | Kiểm nghiệm TPCN / thực phẩm chức năng trước công bố | TPCN | `kiem-nghiem-duoc-pham` | T30 |
| 15 | ✅ | `kiem-nghiem-banh-keo-mat-ong-dau-an` | Kiểm nghiệm bánh kẹo, mật ong, dầu ăn: chỉ tiêu cần biết | Thực phẩm | `kiem-nghiem-banh-keo` + thực phẩm | T30 |
| 16 | ✅ | `haccp-va-iso-22000-khac-nhau` | HACCP vs ISO 22000: doanh nghiệp thực phẩm chọn gì? | Chứng nhận | `chung-nhan-haccp` / `iso-22000` | T31 |

### Đợt C — Dịch vụ & môi trường (6 bài)

| # | Status | Slug đề xuất | Tiêu đề | Tag | Link landing | Tuần |
|---|--------|--------------|---------|-----|--------------|------|
| 17 | ✅ | `kiem-nghiem-nuoc-uong-qcvn` | Kiểm nghiệm nước uống đóng chai theo QCVN: chỉ tiêu & thời gian KQ | Nước | `kiem-nghiem-nuoc-giai-khat` | T31 |
| 18 | ✅ | `kiem-nghiem-my-pham-thong-tu-06` | Kiểm nghiệm mỹ phẩm theo Thông tư 06: chỉ tiêu doanh nghiệp hay hỏi | Mỹ phẩm | `kiem-nghiem-my-pham` | T31 |
| 19 | ✅ | `dang-ky-moi-truong-vs-quan-trac` | Đăng ký môi trường vs quan trắc định kỳ — khác nhau thế nào? | Môi trường | `quan-trac` + `tu-van-moi-truong` | T32 |
| 20 | ✅ | `chai-nhua-dung-nuoc-uong-thoi-nhiem` | Kiểm nghiệm chai nhựa đựng nước uống: thôi nhiễm & an toàn bao bì | Bao bì FCM | `dich-vu-kiem-nghiem-khac` | T32 |
| 21 | ✅ | `vietgap-organic-halal-overview` | VietGAP, Organic, Halal: chứng nhận nào phù hợp doanh nghiệp của bạn? | Chứng nhận | các trang `chung-nhan-*` | T32 |
| 22 | ✅ | `smeta-sedex-nha-may-thuc-pham` | SMETA / Sedex: nhà máy thực phẩm xuất khẩu cần chuẩn bị gì? | Assurance | `chung-nhan-smeta-sedex` | T33 |

### Đợt D — Trend / xuất khẩu (5 bài) · viết sau khi xác nhận năng lực lab

| # | Status | Slug đề xuất | Tiêu đề | Ghi chú | Tuần |
|---|--------|--------------|---------|---------|------|
| 23 | ✅ | `pfas-trong-thuc-pham-bao-bi` | PFAS trong thực phẩm & bao bì: doanh nghiệp cần biết gì? | Chỉ đăng nếu lab/tư vấn được | T33 |
| 24 | ✅ | `vi-nhua-trong-thuc-pham` | Vi nhựa trong thực phẩm và nước uống | Trend GEO | T34 |
| 25 | ✅ | `cronobacter-sua-bot` | Cronobacter sakazakii và rủi ro với sữa bột / dinh dưỡng | Niche | T34 |
| 26 | ✅ | `eu-10-2011-bao-bi-xuat-khau` | EU 10/2011 & xuất khẩu bao bì sang châu Âu | Xuất khẩu | T34 |
| 27 | ✅ | `qcvn-vs-fda-gb4806-bao-bi` | So sánh yêu cầu bao bì VN (QCVN) vs FDA / GB 4806 | So sánh | T35 |

### Đợt E — Bổ sung theo mùa / conversion (3 bài)

| # | Status | Slug đề xuất | Tiêu đề | Ghi chú | Tuần |
|---|--------|--------------|---------|---------|------|
| 28 | ✅ | `gui-mau-kiem-nghiem-can-chuan-bi-gi` | Gửi mẫu kiểm nghiệm: checklist doanh nghiệp | Evergreen CTA | T35 |
| 29 | ✅ | `bao-gia-kiem-nghiem-gom-nhung-gi` | Báo giá kiểm nghiệm gồm những gì? Cách tối ưu chi phí chỉ tiêu | Conversion | T36 |
| 30 | ✅ | `nhan-mau-ha-noi-can-tho-hcm` | Nhận mẫu kiểm nghiệm Hà Nội – Cần Thơ – HCM: quy trình nhanh | Local SEO | T36 |

**Đã hoàn thành:** 30/30 bài trên `/tin-tuc/` (cập nhật 20/07/2026).

**Đợt 2 (map Ads KW + 10 bài mới):** xem [`KE-HOACH-BAI-VIET-DOT-2.md`](KE-HOACH-BAI-VIET-DOT-2.md) — tổng **40** bài (cập nhật 24/07/2026).

---

## 4. Lịch xuất bản đề xuất

| Nhịp | Chi tiết |
|------|----------|
| Tần suất | **3 bài / tuần** (T2 / T4 / T6) |
| Giờ đăng | Sau khi push; không cần giờ cố định (site tĩnh) |
| Thời gian hoàn thành backlog | ~**8 tuần** (T28 → T36/2026) nếu giữ 3 bài/tuần |
| Sprint gần nhất | **Tuần 28 (21–25/07):** bài #7, #8, #9 |

**Ai làm:** Agent viết draft → anh duyệt nhanh (đặc biệt Đợt D: năng lực lab) → generate + push.

---

## 5. Quy trình vận hành (1 bài)

```text
1. Chọn dòng ✅ trong bảng → viết vào scripts/news-articles.json (đầu mảng = mới nhất)
2. python3 scripts/generate-news.py
3. Mở tin-tuc/<slug>.html kiểm tra link/CTA
4. git commit + push
5. Đánh dấu ✅ trong file kế hoạch này
```

---

## 6. Đo lường sau 4–8 tuần

- Search Console: impression/click cụm “kiểm nghiệm…”, “VALAS 217”, “bao bì thực phẩm”
- Gemini: thử 5–10 câu hỏi đã liệt kê trước đó — có cite domain không
- Form: UTM hoặc `Trang_gửi_form` từ bài tin → lead
- Trang yếu (bounce cao): viết lại lead + thêm bảng chỉ tiêu

---

## 7. Quyết định cần anh xác nhận

1. **Giữ nhịp 3 bài/tuần** hay chậm lại 2 bài/tuần?  
2. **Đợt D (PFAS, vi nhựa…):** lab TechLAB có nhận / tư vấn được không, hay chỉ viết “kiến thức + liên hệ tư vấn”?  
3. Bắt đầu **sprint T28 (#7–#9)** ngay trong chat này?

---

*File này là nguồn theo dõi backlog tin tức site kiểm nghiệm. Cập nhật status khi đăng xong từng bài.*
