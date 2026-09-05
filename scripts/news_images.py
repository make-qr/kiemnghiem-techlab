#!/usr/bin/env python3
"""Ảnh tin tức TechLAB — hero/inline khớp chủ đề.

Ảnh nằm trong images/tin-tuc/{slug}-hero.jpg và {slug}-inline.jpg
(đã curate: GenerateImage theo prompt chuyên môn + ảnh brand lab/certificate).

Không tự tải stock lệch chủ đề. Chỉ kiểm tra file tồn tại khi generate HTML.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images" / "tin-tuc"


def ensure_article_images(slug: str) -> tuple[Path, Path]:
    hero = IMG_DIR / f"{slug}-hero.jpg"
    inline = IMG_DIR / f"{slug}-inline.jpg"
    if not hero.is_file() or not inline.is_file():
        raise FileNotFoundError(
            f"Thiếu ảnh cho {slug}. Cần {hero.name} và {inline.name} trong images/tin-tuc/"
        )
    return hero, inline


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


def verify_unique(paths: list[Path]) -> None:
    import hashlib

    hashes: dict[str, str] = {}
    for p in paths:
        h = hashlib.md5(p.read_bytes()).hexdigest()
        if h in hashes:
            raise SystemExit(f"DUPLICATE IMAGE HASH: {p.name} == {hashes[h]}")
        hashes[h] = p.name
