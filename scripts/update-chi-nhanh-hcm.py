#!/usr/bin/env python3
"""Thêm chi nhánh HCM vào footer/contact các trang production."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FOOTER_CT = (
    '<p><i class="fas fa-map-marker-alt"></i> Cần Thơ: Số CC-15, đường số 12, KDC công ty 8, KV2, P. Hưng Thạnh</p>'
)
FOOTER_HCM = """                    <p><i class="fas fa-map-marker-alt"></i> HCM: Lô II-1, Đường số 1, KCN Tân Bình, P. Tây Thạnh</p>
                    <p><i class="fas fa-phone"></i> HCM: <a href="tel:0907616969">0907.61.69.69</a></p>"""

REPLACEMENTS = [
    ("Nhận mẫu Hà Nội &amp; Cần Thơ", "Nhận mẫu HN · CT · HCM"),
    ("Nhận mẫu Hà Nội & Cần Thơ", "Nhận mẫu HN · CT · HCM"),
    ("Hà Nội &amp; Cần Thơ", "HN · CT · HCM"),
    ("Hà Nội và Cần Thơ", "Hà Nội, Cần Thơ &amp; HCM"),
    (
        "Chúng tôi nhận mẫu và tư vấn tại trụ sở Hà Nội (Km11, Quốc Lộ 21) và văn phòng Cần Thơ (KDC công ty 8, P. Hưng Thạnh).",
        "Chúng tôi nhận mẫu và tư vấn tại Hà Nội (Km11, Quốc Lộ 21), Cần Thơ (KDC công ty 8, P. Hưng Thạnh) và chi nhánh HCM (KCN Tân Bình, P. Tây Thạnh). Hotline HCM: <a href=\"tel:0907616969\">0907.61.69.69</a>.",
    ),
    (
        "Nhận mẫu tại Hà Nội, Cần Thơ và HCM (KCN Tân Bình). HCM: <a href=\"tel:0907616969\">0907.61.69.69</a>.",
        "Nhận mẫu tại Hà Nội, Cần Thơ và HCM (KCN Tân Bình). Hotline HCM: 0907.61.69.69.",
    ),
    (
        "Cần Thơ: Số CC-15, đường số 12, KDC công ty 8, KV2, P. Hưng Thạnh<br>\n                Điện thoại:",
        "Cần Thơ: Số CC-15, đường số 12, KDC công ty 8, KV2, P. Hưng Thạnh<br>\n                HCM: Lô II-1, Đường số 1, KCN Tân Bình, P. Tây Thạnh<br>\n                Điện thoại HCM: <a href=\"tel:0907616969\">0907.61.69.69</a><br>\n                Điện thoại:",
    ),
    ("Hà Nội hoặc Cần Thơ", "Hà Nội, Cần Thơ hoặc HCM"),
    ("Hà Nội, Cần Thơ &amp; HCM — liên hệ hotline", "Hà Nội, Cần Thơ &amp; HCM — liên hệ hotline"),
]

GLOB_PATTERNS = [
    "index.html",
    "thank-you.html",
    "privacy-policy.html",
    "ho-so-nang-luc.html",
    "pages/*.html",
]


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if FOOTER_CT in text and 'HCM: Lô II-1' not in text:
        text = text.replace(FOOTER_CT, FOOTER_CT + "\n" + FOOTER_HCM, 1)

    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for pattern in GLOB_PATTERNS:
        for path in sorted(ROOT.glob(pattern)):
            if "pages_template" in str(path):
                continue
            if patch_file(path):
                changed.append(path.relative_to(ROOT))
    print("Updated:", len(changed), "files")
    for p in changed:
        print(" -", p)


if __name__ == "__main__":
    main()
