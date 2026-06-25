#!/usr/bin/env python3
"""Chuẩn hóa snippet tracking (GTM + GA4 + Ads + Meta Pixel) trên HTML production."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GTM_ID = "GTM-MRHPPTJ7"
GA4_ID = "G-4YE334L4TV"
ADS_ID = "AW-18270406607"
META_PIXEL = "4620520364845904"
SITE_HOST = "kiemnghiem.techlabglobal.com.vn"

TRACKING_BLOCK_ROOT = f"""    <!-- TechLAB tracking: GA4 + Google Ads + GTM + Meta Pixel -->
    <script src="js/tracking-bootstrap.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={ADS_ID}"></script>
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GTM_ID}');</script>
    <!-- End Google Tag Manager -->
    <script src="js/meta-pixel.js" defer></script>
    <noscript><img height="1" width="1" style="display:none" alt=""
      src="https://www.facebook.com/tr?id={META_PIXEL}&ev=PageView&noscript=1"/></noscript>
    <link rel="icon" href="/images/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/images/favicon-32.png" type="image/png" sizes="32x32">
    <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">"""

TRACKING_BLOCK_PAGES = TRACKING_BLOCK_ROOT.replace('src="js/', 'src="../js/')

GTM_NOSCRIPT_ROOT = f"""    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->"""

GTM_NOSCRIPT_PAGES = GTM_NOSCRIPT_ROOT

PRODUCTION = [
    ROOT / "index.html",
    ROOT / "thank-you.html",
    ROOT / "privacy-policy.html",
    *sorted((ROOT / "pages").glob("*.html")),
]

TRACKING_RE = re.compile(
    r"<!-- Google tag \(gtag\.js\).*?<!-- End Google Tag Manager -->|"
    r"<!-- TechLAB tracking:.*?apple-touch-icon\.png\">",
    re.DOTALL,
)

GTM_NOSCRIPT_RE = re.compile(
    r"<!-- Google Tag Manager \(noscript\).*?<!-- End Google Tag Manager \(noscript\) -->",
    re.DOTALL,
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    original = text
    is_pages = path.parent.name == "pages"
    block = TRACKING_BLOCK_PAGES if is_pages else TRACKING_BLOCK_ROOT
    noscript = GTM_NOSCRIPT_PAGES if is_pages else GTM_NOSCRIPT_ROOT

    if TRACKING_RE.search(text):
        text = TRACKING_RE.sub(block, text, count=1)
    else:
        text = text.replace("</head>", block + "\n</head>", 1)

    text = GTM_NOSCRIPT_RE.sub("", text)

    body_match = re.search(r"<body>\s*", text)
    if body_match:
        snippet = text[body_match.end() : body_match.end() + 300]
        if "googletagmanager.com/ns.html" not in snippet:
            insert_at = body_match.end()
            text = text[:insert_at] + "\n" + noscript + "\n" + text[insert_at:]

    text = text.replace("kiemnghiem.natekvn.com", SITE_HOST)
    text = text.replace("natekvn.com", "techlabglobal.com.vn")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in PRODUCTION:
        if patch_file(path):
            print(f"updated: {path.relative_to(ROOT)}")
            changed += 1
    print(f"Done. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
