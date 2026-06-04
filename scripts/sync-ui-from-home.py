#!/usr/bin/env python3
"""Sync subpage UI shell (header, footer, CSS, season banner) with index.html baseline."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "pages"

SEASON_BANNER = """    <div class="season-banner">
        <strong>Ưu tiên mùa cao điểm:</strong> Nhận mẫu kiểm nghiệm Bánh Trung thu &amp; Nước uống — báo giá trong ngày | Hotline <strong>0899.551.228</strong>
    </div>
"""

NAV_BLOCK = """            <nav>
                <ul>
                    <li><a href="../index.html">Trang chủ</a></li>
                    <li><a href="../index.html#dich-vu-noi-bat">Ưu tiên</a></li>
                    <li><a href="#bao-gia">Báo giá</a></li>
                    <li><a href="../index.html#dich-vu">Dịch vụ</a></li>
                    <li><a href="../index.html#chung-nhan">Chứng nhận</a></li>
                    <li><a href="../index.html#lien-he">Liên hệ</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <a href="tel:0899551228" class="header-call-btn" aria-label="Gọi 0899.551.228"><i class="fas fa-phone"></i></a>
                <button type="button" class="nav-toggle" aria-label="Mở menu" aria-expanded="false"><span></span><span></span><span></span></button>
            </div>"""

FOOTER_LINKS = """                <div class="footer-links">
                    <h4>Liên kết nhanh</h4>
                    <ul>
                        <li><a href="../index.html">Trang chủ</a></li>
                        <li><a href="../index.html#bao-gia">Báo giá</a></li>
                        <li><a href="../index.html#dich-vu">Dịch vụ</a></li>
                        <li><a href="../index.html#chung-nhan">Chứng nhận</a></li>
                        <li><a href="../index.html#gioi-thieu">Giới thiệu</a></li>
                        <li><a href="../index.html#lien-he">Liên hệ</a></li>
                        <li><a href="../privacy-policy.html">Chính sách bảo mật</a></li>
                    </ul>
                </div>"""

FOOTER_SERVICES = """                <div class="footer-services">
                    <h4>Dịch vụ</h4>
                    <ul>
                        <li><a href="kiem-nghiem-thuc-pham.html">Kiểm nghiệm Thực phẩm</a></li>
                        <li><a href="kiem-nghiem-duoc-pham.html">Kiểm nghiệm Dược phẩm</a></li>
                        <li><a href="chung-nhan-vietgap.html">Chứng nhận VietGAP</a></li>
                        <li><a href="chung-nhan-haccp.html">Chứng nhận HACCP</a></li>
                        <li><a href="chung-nhan-iso-22000.html">Chứng nhận ISO 22000</a></li>
                        <li><a href="quan-trac-moi-truong.html">Quan trắc Môi trường</a></li>
                    </ul>
                </div>"""

FOOTER_CONTACT = """                <div class="footer-contact">
                    <h4>Thông tin liên hệ</h4>
                    <p><i class="fas fa-map-marker-alt"></i> Hà Nội: Tòa nhà 9 tầng, Km11, Quốc Lộ 21</p>
                    <p><i class="fas fa-map-marker-alt"></i> Cần Thơ: Số CC-15, đường số 12, KDC công ty 8, KV2, P. Hưng Thạnh</p>
                    <p><i class="fas fa-phone"></i> <a href="tel:0899551228">0899.551.228</a></p>
                    <p><i class="fas fa-envelope"></i> <a href="mailto:info@techlabglobal.com.vn">info@techlabglobal.com.vn</a></p>
                </div>"""

CSS_LINKS = """    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/conversion.css">
    <link rel="stylesheet" href="../css/service-page.css">"""

HERO_CTA_OLD = re.compile(
    r'(<a href="tel:0899551228" class="btn btn-hero-primary">[^<]*(?:<[^>]+>[^<]*)*</a>\s*)'
    r'(<a href="https://zalo\.me/2097486021894945291" class="btn btn-hero-secondary"[^>]*>Chat Zalo[^<]*</a>)',
    re.DOTALL,
)

HERO_CTA_NEW = (
    r'\1<a href="#bao-gia" class="btn btn-hero-secondary">Gửi yêu cầu báo giá</a>\n                '
    r'<a href="https://zalo.me/2097486021894945291" class="btn btn-hero-secondary btn-hero-zalo" target="_blank" rel="noopener">Chat Zalo</a>'
)


def remove_inline_chat_styles(html: str) -> str:
    """Remove <style> blocks that define chat widget (now in style.css)."""
    def strip_style(match: re.Match) -> str:
        block = match.group(0)
        if "chat-widget-container" in block or ".chat-button" in block:
            return ""
        return block

    return re.sub(r"<style>.*?</style>\s*", strip_style, html, flags=re.DOTALL)


def fix_css_links(html: str) -> str:
    html = re.sub(
        r'<link rel="stylesheet" href="\.\./css/style\.css">\s*'
        r'<link rel="stylesheet" href="\.\./css/service-page\.css">\s*'
        r'<link rel="stylesheet" href="\.\./css/conversion\.css">',
        CSS_LINKS,
        html,
    )
    # Ensure all three exist if any service page css is present
    if "../css/service-page.css" in html and "../css/conversion.css" not in html:
        html = html.replace(
            '../css/service-page.css">',
            '../css/conversion.css">\n    <link rel="stylesheet" href="../css/service-page.css">',
        )
    return html


def fix_nav(html: str) -> str:
    html = re.sub(
        r"<nav>\s*<ul>.*?</ul>\s*</nav>\s*(?:<div class=\"header-actions\">.*?</div>\s*)?",
        NAV_BLOCK + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def add_season_banner(html: str) -> str:
    if "season-banner" in html:
        return html
    return html.replace(
        "    </header>\n\n    <section",
        "    </header>\n\n" + SEASON_BANNER + "\n    <section",
        1,
    )


def fix_footer(html: str) -> str:
    html = re.sub(
        r"<div class=\"footer-links\">.*?</div>\s*",
        FOOTER_LINKS + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<div class=\"footer-services\">.*?</div>\s*",
        FOOTER_SERVICES + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<div class=\"footer-contact\">.*?</div>\s*",
        FOOTER_CONTACT + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def fix_hero_cta(html: str) -> str:
    if 'href="#bao-gia" class="btn btn-hero-secondary">Gửi yêu cầu báo giá' in html:
        return html
    if 'id="bao-gia"' not in html:
        return html
    return HERO_CTA_OLD.sub(HERO_CTA_NEW, html, count=1)


def fix_bottom_scripts(html: str) -> str:
    """Ensure order: chat widget -> sticky bar -> scripts (match homepage)."""
    sticky = re.search(
        r'(\s*<div class="sticky-cta-bar" id="sticky-cta">.*?</div>)',
        html,
        flags=re.DOTALL,
    )
    scripts = re.search(
        r'(\s*<script src="\.\./js/main\.js"></script>\s*<script src="\.\./js/conversion\.js"></script>)',
        html,
    )
    chat = re.search(
        r'(\s*<!-- Chat Widget Container -->.*?</div>\s*<!-- End Chat Widget Container -->)',
        html,
        flags=re.DOTALL,
    )
    if not sticky or not scripts:
        return html

    sticky_block = sticky.group(1)
    scripts_block = scripts.group(1)
    chat_block = chat.group(1) if chat else ""

    # Remove existing blocks
    html = html.replace(sticky_block, "")
    html = html.replace(scripts_block, "")
    if chat_block:
        html = html.replace(chat_block, "")

    gtm_noscript = ""
    gtm_match = re.search(
        r'(\s*<!-- Google Tag Manager \(noscript\) -->.*?</noscript>\s*<!-- End Google Tag Manager \(noscript\) -->)',
        html,
        flags=re.DOTALL,
    )
    if gtm_match:
        gtm_noscript = gtm_match.group(1)
        html = html.replace(gtm_noscript, "")

    insert = ""
    if chat_block:
        insert += chat_block
    insert += sticky_block
    insert += scripts_block
    insert += gtm_noscript

    return html.replace("</body>", insert + "\n</body>", 1)


def fix_indent(html: str) -> str:
    html = html.replace("                        <nav>", "            <nav>")
    html = re.sub(
        r"(</button>\s*</div>)\n</div>\n(\s*</header>)",
        r"\1\n        </div>\n\2",
        html,
    )
    html = html.replace('                                <div class="footer-links">', '                <div class="footer-links">')
    html = html.replace('                                <div class="footer-services">', '                <div class="footer-services">')
    html = html.replace('                                <div class="footer-contact">', '                <div class="footer-contact">')
    return html


def process_file(path: Path) -> list[str]:
    changes = []
    html = path.read_text(encoding="utf-8")
    original = html

    html = remove_inline_chat_styles(html)
    html = fix_css_links(html)
    html = fix_nav(html)
    html = add_season_banner(html)
    html = fix_footer(html)
    html = fix_hero_cta(html)
    html = fix_bottom_scripts(html)
    html = fix_indent(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        changes.append(path.name)
    return changes


def main():
    skip = {"my-pham-template.html"}
    updated = []
    for path in sorted(PAGES_DIR.glob("*.html")):
        if path.name in skip:
            continue
        updated.extend(process_file(path))

    print(f"Updated {len(updated)} pages:")
    for name in updated:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
