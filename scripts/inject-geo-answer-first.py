#!/usr/bin/env python3
"""GEO: answer-first + meta description + FAQ HTML + FAQPage/Service JSON-LD."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "scripts" / "geo-answer-first-data.json").read_text(encoding="utf-8"))
PAGES = ROOT / "pages"
BASE = "https://kiemnghiem.techlabglobal.com.vn"
MARKER = 'class="geo-answer-first"'

TRUST_END_RE = re.compile(
    r"(<section class=\"trust-strip\">.*?</section>\s*)",
    re.DOTALL,
)
FAQ_SECTION_RE = re.compile(
    r"(<section class=\"faq\">\s*<div class=\"container\">\s*<h2>.*?</h2>\s*<div class=\"faq-container\">).*?(</div>\s*</div>\s*</section>)",
    re.DOTALL,
)
LD_JSON_RE = re.compile(
    r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',
    re.DOTALL,
)
META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"(<title>.*?</title>)", re.IGNORECASE | re.DOTALL)


def render_answer_first(slug: str) -> str:
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


def render_faq_items(item: dict) -> str:
    parts = []
    for i, faq in enumerate(item.get("faq") or []):
        active = " active" if i == 0 else ""
        parts.append(
            f"""                <div class="faq-item{active}">
                    <div class="faq-question">
                        <h3>{faq["q"]}</h3>
                        <i class="fas fa-chevron-down"></i>
                    </div>
                    <div class="faq-answer">
                        <p>{faq["a"]}</p>
                    </div>
                </div>"""
        )
    return "\n".join(parts)


def upsert_meta_description(text: str, description: str) -> str:
    meta = f'<meta name="description" content="{description}">'
    if META_DESC_RE.search(text):
        return META_DESC_RE.sub(meta, text, count=1)
    m = TITLE_RE.search(text)
    if not m:
        return text
    return text[: m.end()] + "\n    " + meta + text[m.end() :]


def patch_answer_first(text: str, slug: str) -> str:
    if MARKER in text:
        text = re.sub(
            r"\s*<section class=\"geo-answer-first\".*?</section>\s*",
            "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
    m = TRUST_END_RE.search(text)
    if not m:
        return text
    return text[: m.end()] + render_answer_first(slug) + text[m.end() :]


def patch_faq_html(text: str, item: dict) -> str:
    if not item.get("faq"):
        return text
    items = render_faq_items(item)

    def repl(m: re.Match) -> str:
        return m.group(1) + "\n" + items + "\n            " + m.group(2)

    new_text, n = FAQ_SECTION_RE.subn(repl, text, count=1)
    return new_text if n else text


def build_service_nodes(slug: str, item: dict, page_url: str) -> list:
    service_name = item.get("service_name") or slug
    nodes = [
        {
            "@type": "Service",
            "@id": f"{page_url}#service",
            "name": service_name,
            "description": item.get("meta_description") or item.get("lead"),
            "url": page_url,
            "provider": {"@id": f"{BASE}/#localbusiness"},
            "areaServed": [
                {"@type": "City", "name": "Hà Nội"},
                {"@type": "City", "name": "Cần Thơ"},
                {"@type": "City", "name": "Hồ Chí Minh"},
            ],
            "brand": {"@id": "https://techlabglobal.com.vn/#organization"},
        }
    ]
    faqs = item.get("faq") or []
    if faqs:
        nodes.append(
            {
                "@type": "FAQPage",
                "@id": f"{page_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
                    }
                    for f in faqs
                ],
            }
        )
    return nodes


def patch_json_ld(text: str, slug: str, item: dict) -> str:
    page_url = f"{BASE}/pages/{slug}.html"
    m = LD_JSON_RE.search(text)
    if not m:
        return text
    try:
        data = json.loads(m.group(2))
    except json.JSONDecodeError:
        return text

    if isinstance(data, dict) and "@graph" in data:
        graph = [
            node
            for node in data["@graph"]
            if not (
                isinstance(node, dict)
                and node.get("@type") in ("Service", "FAQPage")
            )
        ]
        graph.extend(build_service_nodes(slug, item, page_url))
        data["@graph"] = graph
        payload = json.dumps(data, ensure_ascii=False, indent=2)
        return text[: m.start(2)] + "\n    " + payload.replace("\n", "\n    ") + text[m.end(2) :]
    return text


def patch_file(path: Path) -> bool:
    slug = path.stem
    if slug not in DATA:
        return False
    item = DATA[slug]
    original = path.read_text(encoding="utf-8")
    text = original
    text = patch_answer_first(text, slug)
    if item.get("meta_description"):
        text = upsert_meta_description(text, item["meta_description"])
    text = patch_faq_html(text, item)
    text = patch_json_ld(text, slug, item)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(PAGES.glob("*.html")):
        if patch_file(path):
            changed.append(path.name)
    print(f"GEO patched: {len(changed)} pages")
    for name in changed:
        print(" -", name)


if __name__ == "__main__":
    main()
