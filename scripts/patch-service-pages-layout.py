#!/usr/bin/env python3
"""Cân bố cục 16 trang landing: body class, header CTA, form sau intro, season banner, intro ảnh."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"

SEASON_SLUGS = {
    "kiem-nghiem-thuc-pham",
    "kiem-nghiem-banh-keo",
    "kiem-nghiem-nuoc-giai-khat",
}

CERT_SLUGS = {
    "chung-nhan-vietgap",
    "chung-nhan-haccp",
    "chung-nhan-iso-22000",
    "chung-nhan-organic",
    "chung-nhan-halal",
    "chung-nhan-smeta-sedex",
}

FORM_RE = re.compile(
    r"\n\s*<section id=\"bao-gia\" class=\"quote-form-section\">.*?</section>",
    re.DOTALL,
)

INTRO_RE = re.compile(
    r"(<section class=\"service-intro\">.*?</section>)",
    re.DOTALL,
)

SEASON_RE = re.compile(
    r"\n\s*<div class=\"season-banner\">.*?</div>\s*",
    re.DOTALL,
)

HEADER_ACTIONS_OLD = (
    '<div class="header-actions">\n'
    '                <a href="tel:0899551228" class="header-call-btn"'
)

HEADER_ACTIONS_NEW = (
    '<div class="header-actions">\n'
    '                <a href="#bao-gia" class="header-quote-btn">Báo giá</a>\n'
    '                <a href="tel:0899551228" class="header-call-btn"'
)


def intro_banner_path(slug: str) -> str | None:
    banners = ROOT / "images" / "banners"
    for ext in (".jpg", ".png", ".webp"):
        p = banners / f"{slug}{ext}"
        if p.exists():
            return f"../images/banners/{slug}{ext}"
    return None


def patch_hero_cert(html: str, slug: str) -> str:
    if slug not in CERT_SLUGS:
        return html
    return re.sub(
        r'<section class="service-hero" ',
        '<section class="service-hero service-hero--cert" ',
        html,
        count=1,
    )


def move_form_after_intro(html: str) -> str:
    form_m = FORM_RE.search(html)
    if not form_m:
        return html
    form_block = form_m.group(0)
    html = FORM_RE.sub("", html, count=1)
    intro_m = INTRO_RE.search(html)
    if not intro_m:
        return html + form_block
    pos = intro_m.end()
    return html[:pos] + form_block + html[pos:]


def fix_intro_img_markup(html: str) -> str:
    html = html.replace('loading="lazy"> loading=\\"lazy\\"', 'loading="lazy">')
    html = re.sub(
        r'(<div class="intro-image">\s*<img src="[^"]+" alt="[^"]*")> loading=\\"lazy\\"',
        r'\1 loading="lazy">',
        html,
    )
    return html


def patch_intro_image(html: str, slug: str) -> str:
    banner = intro_banner_path(slug)
    if not banner:
        return fix_intro_img_markup(html)
    html = re.sub(
        r'(<div class="intro-image">\s*<img src=")[^"]+(" alt="[^"]*"(?:\s+loading="lazy")?>)',
        rf"\1{banner}\2",
        html,
        count=1,
    )
    return fix_intro_img_markup(html)


def patch_file(path: Path) -> bool:
    slug = path.stem
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace("<body>", '<body class="service-page">', 1)
    text = text.replace(HEADER_ACTIONS_OLD, HEADER_ACTIONS_NEW, 1)

    if slug not in SEASON_SLUGS:
        text = SEASON_RE.sub("\n", text, count=1)

    text = move_form_after_intro(text)
    text = patch_intro_image(text, slug)
    text = fix_intro_img_markup(text)
    text = patch_hero_cert(text, slug)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    dirs = [PAGES, ROOT / "pages_template"]
    for folder in dirs:
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.html")):
            if patch_file(path):
                changed.append(f"{folder.name}/{path.name}")
    print("Patched:", len(changed), "files")
    for name in changed:
        print(" -", name)


if __name__ == "__main__":
    main()
