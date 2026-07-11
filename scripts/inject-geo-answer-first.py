#!/usr/bin/env python3
"""Chèn khối GEO answer-first vào 16 trang dịch vụ (sau trust-strip)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "scripts" / "geo-answer-first-data.json").read_text(encoding="utf-8"))
PAGES = ROOT / "pages"
MARKER = 'class="geo-answer-first"'

TRUST_END_RE = re.compile(
    r"(<section class=\"trust-strip\">.*?</section>\s*)",
    re.DOTALL,
)


def render_block(slug: str) -> str:
    item = DATA[slug]
    facts_html = "\n".join(f"                    <li>{f}</li>" for f in item["facts"])
    return f"""
    <section class="geo-answer-first" aria-label="Tóm tắt dịch vụ">
        <div class="container">
            <div class="geo-answer-box">
                <p class="geo-answer-lead">{item["lead"]}</p>
                <ul class="geo-answer-facts">
{facts_html}
                </ul>
                <p class="geo-answer-cite">Xác thực năng lực: <a href="../ho-so-nang-luc.html">Hồ sơ năng lực VALAS 217 (ISO/IEC 17025)</a> · Hotline <a href="tel:0899551228">0899.551.228</a> · HCM <a href="tel:0907616969">0907.61.69.69</a></p>
            </div>
        </div>
    </section>
"""


def patch_file(path: Path) -> bool:
    slug = path.stem
    if slug not in DATA:
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        text = re.sub(
            r"\s*<section class=\"geo-answer-first\".*?</section>\s*",
            "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
    block = render_block(slug)
    m = TRUST_END_RE.search(text)
    if not m:
        return False
    new_text = text[: m.end()] + block + text[m.end() :]
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for path in sorted(PAGES.glob("*.html")):
        if patch_file(path):
            changed.append(path.name)
    print(f"Injected answer-first: {len(changed)} pages")
    for name in changed:
        print(" -", name)


if __name__ == "__main__":
    main()
