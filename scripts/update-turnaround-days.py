#!/usr/bin/env python3
"""Batch-update turnaround day counts on kiemnghiem-techlab site."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Generic footer/boilerplate in news articles
OLD_GENERIC = "Thời gian kết quả thường 5–7 ngày làm việc"
NEW_GENERIC = "KLN/VS: 5–7 ngày; có kiểm nhóm dinh dưỡng: 7–12 ngày làm việc"

# Dinh dưỡng-specific pages/articles
DINH_DUONG_FILES = {
    "tin-tuc/phan-tich-dinh-duong-ghi-nhan.html",
    "tin-tuc/ghi-nhan-dinh-duong-thong-tu-29-2023.html",
}

DINH_DUONG_OLD = "Thời gian kết quả thường 5–7 ngày làm việc"
DINH_DUONG_NEW = "Thời gian kết quả thường 7–12 ngày làm việc"

# Thuc pham ha noi - add exception
THUC_PHAM_HN_OLD = "thường 5–7 ngày làm việc tùy nhóm chỉ tiêu"
THUC_PHAM_HN_NEW = "KLN/VS: 5–7 ngày; có kiểm nhóm dinh dưỡng: 7–12 ngày làm việc"

# Form option in remaining pages
FORM_OLD = 'value="Bình thường (5–7 ngày)" data-slug="binh-thuong">Bình thường (5–7 ngày)'
FORM_NEW = '''value="KLN/VS bình thường (5–7 ngày)" data-slug="binh-thuong">KLN/VS bình thường (5–7 ngày)</option>
                            <option value="Có kiểm nhóm dinh dưỡng (7–12 ngày)" data-slug="dinh-duong">Có kiểm nhóm dinh dưỡng (7–12 ngày)'''

updated = []

for path in ROOT.rglob("*"):
    if path.suffix not in {".html", ".json"}:
        continue
    rel = str(path.relative_to(ROOT))
    if rel.startswith("scripts/update-turnaround"):
        continue

    text = path.read_text(encoding="utf-8")
    orig = text

    if rel in DINH_DUONG_FILES or "dinh-duong" in rel and "kiem-nghiem-dinh-duong" not in rel:
        if DINH_DUONG_OLD in text:
            text = text.replace(DINH_DUONG_OLD, DINH_DUONG_NEW)
        text = text.replace(
            "Thường 5–7 ngày làm việc tùy chỉ tiêu",
            "Thường 7–12 ngày làm việc tùy gói chỉ tiêu dinh dưỡng",
        )

    if "kiem-nghiem-thuc-pham-ha-noi" in rel or rel.endswith("kiem-nghiem-thuc-pham-ha-noi.html"):
        text = text.replace(THUC_PHAM_HN_OLD, THUC_PHAM_HN_NEW)

    if OLD_GENERIC in text and rel not in DINH_DUONG_FILES:
        text = text.replace(OLD_GENERIC, NEW_GENERIC)

    if FORM_OLD in text:
        text = text.replace(FORM_OLD, FORM_NEW)

    # news-articles.json mooncake entries
    if rel == "scripts/news-articles.json":
        text = text.replace(
            "Thời gian kết quả thường 5–7 ngày làm việc",
            "KLN/VS: 5–7 ngày; có kiểm nhóm dinh dưỡng: 7–12 ngày làm việc",
        )
        text = text.replace(
            "<strong>5–7 ngày làm việc</strong> tùy gói",
            "KLN/VS <strong>5–7 ngày</strong>; có kiểm nhóm dinh dưỡng <strong>7–12 ngày</strong> làm việc",
        )
        text = text.replace(
            "Thời gian kết quả thường 5–7 ngày làm việc; báo giá trong ngày. Chi tiết gói bánh kẹo",
            "KLN/VS: 5–7 ngày; có kiểm nhóm dinh dưỡng: 7–12 ngày làm việc; báo giá trong ngày. Chi tiết gói bánh kẹo",
        )
        # dinh duong articles in JSON
        for slug in ["phan-tich-dinh-duong-ghi-nhan", "ghi-nhan-dinh-duong-thong-tu-29-2023"]:
            if slug in text:
                pass  # handled by per-file below if needed

    if text != orig:
        path.write_text(text, encoding="utf-8")
        updated.append(rel)

print(f"Updated {len(updated)} files:")
for u in sorted(updated):
    print(f"  - {u}")
