#!/usr/bin/env python3
"""Copy banner ảnh vào images/banners/ và gắn --hero-bg cho từng trang dịch vụ."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
BANNERS = IMAGES / "banners"
PAGES = ROOT / "pages"

# slug trang → file nguồn trong images/
BANNER_MAP = {
    "kiem-nghiem-thuc-pham": "food-testing.jpg",
    "kiem-nghiem-banh-keo": "bakery-testing.jpg",
    "kiem-nghiem-nuoc-giai-khat": "hero-banner-trang-chu.png",
    "kiem-nghiem-my-pham": "cosmetics-testing.jpg",
    "kiem-nghiem-duoc-pham": "pharmaceutical-testing.jpg",
    "kiem-nghiem-dinh-duong": "nutrition-testing.jpg",
    "kiem-nghiem-thuc-an-chan-nuoi": "animal-feed-testing.jpg",
    "dich-vu-kiem-nghiem-khac": "other-testing-services.jpg",
    "quan-trac-moi-truong": "environmental-monitoring.jpg",
    "tu-van-moi-truong": "environmental-consulting.jpg",
    "chung-nhan-vietgap": "vietgap-certificate.jpg",
    "chung-nhan-haccp": "chi-phi-cap-chung-chi-iso-22000.jpg",
    "chung-nhan-iso-22000": "chi-phi-cap-chung-chi-iso-22000.jpg",
    "chung-nhan-organic": "organic-certificate.jpg",
    "chung-nhan-halal": "halal-certificate.jpg",
    "chung-nhan-smeta-sedex": "smeta-sedex-certificate.jpg",
}

# Trang cần căn ảnh lệch phải (ảnh lab / người bên phải)
HERO_POS_RIGHT = {"kiem-nghiem-nuoc-giai-khat"}


def banner_dest(slug: str, src_name: str) -> Path:
    ext = Path(src_name).suffix
    return BANNERS / f"{slug}{ext}"


def hero_attrs(slug: str, dest_name: str) -> str:
    url = f"../images/banners/{dest_name}"
    if slug in HERO_POS_RIGHT:
        return f'style="--hero-bg: url(\'{url}\'); --hero-pos: 72% center"'
    return f'style="--hero-bg: url(\'{url}\')"'


def main():
    BANNERS.mkdir(parents=True, exist_ok=True)
    old_hero = '<section class="service-hero">'

    for slug, src_name in sorted(BANNER_MAP.items()):
        src = IMAGES / src_name
        if not src.exists():
            print("SKIP missing:", src_name)
            continue

        dest = banner_dest(slug, src_name)
        shutil.copy2(src, dest)

        html_path = PAGES / f"{slug}.html"
        if not html_path.exists():
            print("SKIP no page:", html_path.name)
            continue

        text = html_path.read_text(encoding="utf-8")
        new_hero = f'<section class="service-hero" {hero_attrs(slug, dest.name)}>'
        if old_hero not in text and "service-hero" not in text:
            print("SKIP no hero tag:", html_path.name)
            continue

        # Thay hero cũ (có hoặc chưa có style)
        import re
        new_text = re.sub(
            r'<section class="service-hero"[^>]*>',
            new_hero,
            text,
            count=1,
        )
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8")
            print("OK", html_path.name, "→", dest.name)

    print("Done.")


if __name__ == "__main__":
    main()
