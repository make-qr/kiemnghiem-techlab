#!/usr/bin/env python3
"""Thêm liên kết Hub ↔ Spoke (techlabglobal.com.vn ↔ kiemnghiem) vào mọi trang HTML."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINKS = json.loads((ROOT / "scripts" / "site-links.json").read_text(encoding="utf-8"))
MARKER = "footer-hub-network"

HUB_STRIP = f"""    <div class="hub-strip" role="navigation" aria-label="Mạng lưới TechLAB Global">
        <div class="container hub-strip-inner">
            <a href="{LINKS['hub']}">TechLAB Global</a>
            <span class="hub-strip-sep" aria-hidden="true">·</span>
            <a href="{LINKS['hub_news']}">Tin tức &amp; kiến thức</a>
            <span class="hub-strip-sep" aria-hidden="true">·</span>
            <span class="hub-strip-here">Báo giá kiểm nghiệm</span>
        </div>
    </div>
"""

FOOTER_HUB = f"""                <div class="footer-hub-network">
                    <h4>Hệ thống TechLAB Global</h4>
                    <ul>
                        <li><a href="{LINKS['hub']}">Website chính</a></li>
                        <li><a href="{LINKS['hub_news']}">Tin tức kiểm nghiệm</a></li>
                        <li><a href="{LINKS['hub_contact']}">Liên hệ tổng đài</a></li>
                        <li><a href="{LINKS['hub_cert']}">Chứng nhận sản phẩm</a></li>
                    </ul>
                    <p class="footer-hub-note">Cổng <strong>kiểm nghiệm &amp; báo giá nhanh</strong> — một thương hiệu TechLAB Global, phòng lab ISO/IEC 17025.</p>
                </div>
"""

SCHEMA = f"""    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "Organization",
          "@id": "{LINKS['hub']}#organization",
          "name": "TechLAB Global",
          "url": "{LINKS['hub']}",
          "logo": "{LINKS['spoke']}images/logo.png",
          "sameAs": [
            "{LINKS['spoke']}",
            "https://www.facebook.com/profile.php?id=61555675322896&locale=vi_VN"
          ]
        }},
        {{
          "@type": "WebSite",
          "@id": "{LINKS['spoke']}#website",
          "name": "Kiểm nghiệm TechLAB Global",
          "url": "{LINKS['spoke']}",
          "publisher": {{ "@id": "{LINKS['hub']}#organization" }},
          "description": "Báo giá kiểm nghiệm thực phẩm, mỹ phẩm, nước uống — phòng lab ISO/IEC 17025"
        }}
      ]
    }}
    </script>
"""


def depth_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.parent == Path("."):
        return ""
    if rel.parent == Path("pages"):
        return "../"
    return ""


def nav_hub_item(prefix: str) -> str:
    return f'                    <li><a href="{LINKS["hub"]}">TechLAB Global</a></li>\n'


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    changed = False
    prefix = depth_prefix(path)

    if "hub-strip" not in text and "</header>" in text:
        text = text.replace("</header>", "</header>\n" + HUB_STRIP, 1)
        changed = True

    if MARKER not in text and '<div class="footer-links">' in text:
        text = text.replace(
            '<div class="footer-links">',
            FOOTER_HUB + '                <div class="footer-links">',
            1,
        )
        changed = True

    if 'href="' + LINKS["hub"] + '"' not in text and "<nav>" in text and "<ul>" in text:
        text = re.sub(
            r"(<nav>\s*<ul>\s*)",
            r"\1" + nav_hub_item(prefix),
            text,
            count=1,
        )
        changed = True

    old_schema = re.search(
        r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "Organization".*?</script>',
        text,
        re.DOTALL,
    )
    if old_schema:
        text = text[: old_schema.start()] + SCHEMA.strip() + text[old_schema.end() :]
        changed = True
    elif '"@graph"' not in text and "</body>" in text:
        text = text.replace("</body>", SCHEMA + "\n</body>", 1)
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    targets = [ROOT / "index.html", ROOT / "thank-you.html", ROOT / "privacy-policy.html"]
    targets.extend(sorted((ROOT / "pages").glob("*.html")))
    n = sum(1 for p in targets if p.is_file() and patch_file(p))
    print(f"Đã cập nhật {n}/{len(targets)} file HTML")


if __name__ == "__main__":
    main()
