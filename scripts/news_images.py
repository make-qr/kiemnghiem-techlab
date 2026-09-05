#!/usr/bin/env python3
"""Tạo ảnh hero + inline riêng cho mỗi bài tin (TechLAB — không reuse file)."""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images" / "tin-tuc"
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Palettes theo brand TechLAB (navy / blue / accent đỏ nhẹ)
BASE_PALETTES = [
    ((10, 37, 64), (15, 117, 188)),
    ((11, 94, 149), (39, 146, 221)),
    ((7, 26, 46), (15, 117, 188)),
    ((10, 55, 100), (237, 28, 36)),
    ((8, 70, 120), (20, 140, 200)),
    ((12, 45, 80), (50, 160, 210)),
    ((5, 40, 75), (15, 100, 160)),
    ((20, 60, 110), (180, 40, 50)),
]


def unique_seed(slug: str, role: str) -> int:
    h = hashlib.sha256(f"{slug}|{role}|techlab-news-v1".encode()).hexdigest()
    return int(h[:8], 16)


def make_unique_image(slug: str, role: str, width: int = 960, height: int = 540) -> Path:
    out = IMG_DIR / f"{slug}-{role}.jpg"
    seed = unique_seed(slug, role)
    rng_r = (seed >> 0) & 255
    rng_g = (seed >> 8) & 255
    rng_b = (seed >> 16) & 255
    idx = seed % len(BASE_PALETTES)
    c1, c2 = BASE_PALETTES[idx]
    c1 = tuple(max(0, min(255, c1[i] + ((seed >> (i * 5)) & 31) - 15)) for i in range(3))
    c2 = tuple(max(0, min(255, c2[i] + ((seed >> (i * 7 + 3)) & 31) - 10)) for i in range(3))

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        t = y / max(1, height - 1)
        wave = 0.08 * (((seed % 97) / 97) * 2 - 1)
        tt = min(1.0, max(0.0, t + wave * (y % 40) / 40))
        col = tuple(int(c1[i] * (1 - tt) + c2[i] * tt) for i in range(3))
        draw.line([(0, y), (width, y)], fill=col)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    n_shapes = 14 + (seed % 10)
    for i in range(n_shapes):
        s2 = (seed * (i + 3) * 2654435761) & 0xFFFFFFFF
        x0 = s2 % width
        y0 = (s2 >> 9) % height
        w = 28 + (s2 >> 17) % 120
        h = 22 + (s2 >> 23) % 100
        alpha = 55 + (s2 % 80)
        fill = (rng_r, rng_g, rng_b, alpha) if i % 2 == 0 else (c2[0], c2[1], c2[2], alpha)
        shape = (s2 >> 3) % 4
        if shape == 0:
            od.ellipse([x0 - w // 2, y0 - h // 2, x0 + w // 2, y0 + h // 2], fill=fill)
        elif shape == 1:
            od.rectangle([x0, y0, min(width, x0 + w), min(height, y0 + h)], fill=fill)
        elif shape == 2:
            od.polygon([(x0, y0 + h), (x0 + w // 2, y0), (x0 + w, y0 + h)], fill=fill)
        else:
            od.rounded_rectangle(
                [x0, y0, min(width, x0 + w), min(height, y0 + h)], radius=12, fill=fill
            )

    band_y = (seed % (height - 40)) + 10
    od.rectangle([0, band_y, width, band_y + 18], fill=(255, 255, 255, 22))
    od.ellipse([width - 160, -40, width + 40, 160], fill=(255, 255, 255, 35))
    od.ellipse([-60, height - 140, 140, height + 40], fill=(0, 0, 0, 28))
    # accent stripe (brand red hint)
    stripe_x = 40 + (seed % (width // 3))
    od.rectangle([stripe_x, 0, stripe_x + 6, height], fill=(237, 28, 36, 90))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    img = ImageEnhance.Contrast(img).enhance(1.08)

    px = img.load()
    for i in range(64):
        x = (seed + i * 17) % width
        y = (seed // 3 + i * 29) % height
        r, g, b = px[x, y]
        px[x, y] = ((r + i) % 256, (g + seed % 7) % 256, (b + i * 3) % 256)

    img.save(out, "JPEG", quality=88, optimize=True)
    return out


def ensure_article_images(slug: str) -> tuple[Path, Path]:
    hero = IMG_DIR / f"{slug}-hero.jpg"
    inline = IMG_DIR / f"{slug}-inline.jpg"
    if not hero.is_file():
        make_unique_image(slug, "hero")
    if not inline.is_file():
        make_unique_image(slug, "inline")
    return hero, inline


def verify_unique(paths: list[Path]) -> None:
    hashes: dict[str, str] = {}
    for p in paths:
        h = hashlib.md5(p.read_bytes()).hexdigest()
        if h in hashes:
            raise SystemExit(f"DUPLICATE IMAGE HASH: {p.name} == {hashes[h]}")
        hashes[h] = p.name


def figure_html(slug: str, role: str, title: str, css_v: str, loading: str = "lazy") -> str:
    alt = esc_attr(title if role == "hero" else f"{title} — minh họa")
    return (
        f'<figure class="news-{"featured" if role == "hero" else "inline"}">\n'
        f'  <img src="../images/tin-tuc/{slug}-{role}.jpg?v={css_v}" alt="{alt}" '
        f'width="960" height="540" loading="{loading}">\n'
        f"</figure>"
    )


def esc_attr(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inject_inline_after_first_section(body: str, inline_html: str) -> str:
    """Chèn ảnh inline sau khối nội dung đầu tiên (sau </h2>… đến trước <h2> tiếp)."""
    import re

    if 'class="news-inline"' in body:
        return body
    m = re.search(r"</h2>", body)
    if not m:
        return inline_html + "\n" + body
    pos = m.end()
    m2 = re.search(r"<h2\b", body[pos:])
    if m2:
        insert_at = pos + m2.start()
        return body[:insert_at] + "\n" + inline_html + "\n" + body[insert_at:]
    return body[:pos] + "\n" + inline_html + "\n" + body[pos:]
