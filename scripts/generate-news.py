#!/usr/bin/env python3
"""Sinh trang tin tức từ scripts/news-articles.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "scripts" / "news-articles.json").read_text(encoding="utf-8"))
OUT = ROOT / "tin-tuc"
BASE = "https://kiemnghiem.techlabglobal.com.vn"

COMMON_HEAD = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta}">
    <title>{title} | TechLAB Global</title>
    <link rel="canonical" href="{canonical}">
    <link rel="stylesheet" href="../css/style.css?v=20260720d">
    <link rel="stylesheet" href="../css/conversion.css?v=20260720d">
    <link rel="stylesheet" href="../css/news.css?v=20260720d">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="../js/tracking-bootstrap.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4YE334L4TV"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18270406607"></script>
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-MRHPPTJ7');</script>
    <script src="../js/meta-pixel.js" defer></script>
    <link rel="icon" href="/images/favicon.ico" type="image/x-icon">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="article">
</head>
<body class="news-article">
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MRHPPTJ7"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
"""

HEADER = """    <header>
        <div class="container">
            <div class="logo">
                <a href="../index.html"><img src="../images/logo.png" alt="TechLAB Global logo"></a>
            </div>
            <nav>
                <ul>
                    <li><a href="../index.html">Trang chủ</a></li>
                    <li><a href="../index.html#bao-gia">Báo giá</a></li>
                    <li><a href="../ho-so-nang-luc.html">Năng lực</a></li>
                    <li><a href="index.html" class="active">Tin tức</a></li>
                    <li><a href="../index.html#lien-he">Liên hệ</a></li>
                </ul>
            </nav>
            <div class="header-actions">
                <a href="../index.html#bao-gia" class="header-quote-btn">Báo giá ngay</a>
                <a href="tel:0899551228" class="header-call-btn" aria-label="Gọi 0899.551.228"><i class="fas fa-phone"></i></a>
                <button type="button" class="nav-toggle" aria-label="Mở menu" aria-expanded="false"><span></span><span></span><span></span></button>
            </div>
        </div>
    </header>
    <div class="hub-strip" role="navigation" aria-label="Mạng lưới TechLAB Global">
        <div class="container hub-strip-inner">
            <a href="https://techlabglobal.com.vn/">TechLAB Global</a>
            <span class="hub-strip-sep" aria-hidden="true">·</span>
            <a href="index.html">Tin tức kiểm nghiệm</a>
            <span class="hub-strip-sep" aria-hidden="true">·</span>
            <a href="../ho-so-nang-luc.html">Hồ sơ năng lực</a>
            <span class="hub-strip-sep" aria-hidden="true">·</span>
            <a href="../index.html#bao-gia">Báo giá nhanh</a>
        </div>
    </div>
"""

FOOTER = """    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <img src="../images/logo.png" alt="TechLAB Global logo" class="footer-logo-img">
                    <p>Chuyên gia kiểm nghiệm và chứng nhận</p>
                </div>
                <div class="footer-links">
                    <h4>Liên kết nhanh</h4>
                    <ul>
                        <li><a href="../index.html">Trang chủ</a></li>
                        <li><a href="index.html">Tin tức</a></li>
                        <li><a href="../ho-so-nang-luc.html">Hồ sơ năng lực</a></li>
                        <li><a href="../index.html#bao-gia">Báo giá</a></li>
                        <li><a href="../privacy-policy.html">Chính sách bảo mật</a></li>
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>Thông tin liên hệ</h4>
                    <p><i class="fas fa-phone"></i> <a href="tel:0899551228">0899.551.228</a></p>
                    <p><i class="fas fa-phone"></i> HCM: <a href="tel:0907616969">0907.61.69.69</a></p>
                    <p><i class="fas fa-envelope"></i> <a href="mailto:info@techlabglobal.com.vn">info@techlabglobal.com.vn</a></p>
                </div>
            </div>
            <div class="copyright">
                <p>Copyright © 2026 Công ty Cổ phần Khoa học và Công nghệ TechLAB Global</p>
            </div>
        </div>
    </footer>
    <div class="sticky-cta-bar" id="sticky-cta">
        <a href="tel:0899551228" class="sticky-cta-call"><i class="fas fa-phone"></i> Gọi 0899.551.228</a>
        <a href="https://zalo.me/2097486021894945291" class="sticky-cta-zalo" target="_blank" rel="noopener"><i class="fas fa-comment"></i> Chat Zalo</a>
    </div>
    <script src="../js/main.js"></script>
    <script src="../js/conversion.js?v=20260720b"></script>
"""


def related_cards(current_slug: str, limit: int = 3) -> str:
    others = [a for a in DATA["articles"] if a["slug"] != current_slug][:limit]
    cards = []
    for a in others:
        cards.append(
            f"""            <article class="news-card">
                <div class="news-card-meta"><span class="news-card-tag">{a["tag"]}</span><span>{a["date_display"]}</span></div>
                <h2><a href="{a["slug"]}.html">{a["title"]}</a></h2>
                <p>{a["excerpt"]}</p>
                <a class="news-card-link" href="{a["slug"]}.html">Đọc tiếp →</a>
            </article>"""
        )
    return "\n".join(cards)


def render_article(article: dict) -> str:
    slug = article["slug"]
    canonical = f"{BASE}/tin-tuc/{slug}.html"
    cta_links = article.get("cta_links") or [
        {"href": "../index.html#bao-gia", "label": "Gửi yêu cầu báo giá", "class": "btn btn-hero-primary"},
        {"href": "tel:0899551228", "label": "Gọi 0899.551.228", "class": "btn btn-hero-secondary"},
    ]
    cta_html = "".join(
        f'<a href="{c["href"]}" class="{c.get("class", "btn")}">{c["label"]}</a>' for c in cta_links
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta"],
        "datePublished": article["date"],
        "dateModified": article.get("date_modified", article["date"]),
        "author": {"@type": "Organization", "name": "TechLAB Global"},
        "publisher": {
            "@type": "Organization",
            "name": "TechLAB Global",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/images/logo.png"},
        },
        "mainEntityOfPage": canonical,
    }
    return f"""{COMMON_HEAD.format(meta=article["meta"], title=article["title"], canonical=canonical)}
{HEADER}
    <section class="news-article-hero">
        <div class="container">
            <nav class="news-breadcrumb" aria-label="Breadcrumb">
                <a href="../index.html">Trang chủ</a> · <a href="index.html">Tin tức</a> · {article["tag"]}
            </nav>
            <h1>{article["title"]}</h1>
            <div class="news-article-meta">
                <span>{article["date_display"]}</span>
                <span>{article["tag"]}</span>
                <span>TechLAB Global</span>
            </div>
        </div>
    </section>
    <article class="news-article-body">
        <div class="container">
            <p class="news-lead">{article["lead"]}</p>
{article["body"]}
            <div class="news-cta-box">
                <p><strong>Cần báo giá kiểm nghiệm?</strong> TechLAB Global — phòng lab ISO/IEC 17025 (VALAS 217), nhận mẫu HN · CT · HCM.</p>
                <div class="news-cta-actions">{cta_html}</div>
            </div>
        </div>
    </article>
    <section class="news-related">
        <div class="container">
            <h2>Bài viết liên quan</h2>
            <div class="news-grid">
{related_cards(slug)}
            </div>
        </div>
    </section>
{FOOTER}
    <script type="application/ld+json">
    {json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
</body>
</html>
"""


def render_index() -> str:
    articles = DATA["articles"]
    cards = []
    for a in articles:
        cards.append(
            f"""            <article class="news-card">
                <div class="news-card-meta"><span class="news-card-tag">{a["tag"]}</span><span>{a["date_display"]}</span></div>
                <h2><a href="{a["slug"]}.html">{a["title"]}</a></h2>
                <p>{a["excerpt"]}</p>
                <a class="news-card-link" href="{a["slug"]}.html">Đọc tiếp →</a>
            </article>"""
        )
    item_list = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"{BASE}/tin-tuc/{a['slug']}.html",
            "name": a["title"],
        }
        for i, a in enumerate(articles)
    ]
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Tin tức kiểm nghiệm - TechLAB Global",
        "url": f"{BASE}/tin-tuc/",
        "mainEntity": {"@type": "ItemList", "itemListElement": item_list},
    }
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Tin tức & kiến thức kiểm nghiệm thực phẩm, bao bì, dinh dưỡng, ISO 17025 từ phòng thử nghiệm TechLAB Global (VALAS 217).">
    <title>Tin tức kiểm nghiệm | TechLAB Global</title>
    <link rel="canonical" href="{BASE}/tin-tuc/">
    <link rel="stylesheet" href="../css/style.css?v=20260720d">
    <link rel="stylesheet" href="../css/conversion.css?v=20260720d">
    <link rel="stylesheet" href="../css/news.css?v=20260720d">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="../js/tracking-bootstrap.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4YE334L4TV"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-18270406607"></script>
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-MRHPPTJ7');</script>
    <script src="../js/meta-pixel.js" defer></script>
    <link rel="icon" href="/images/favicon.ico" type="image/x-icon">
</head>
<body class="news-list-page">
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MRHPPTJ7"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{HEADER}
    <section class="news-hero">
        <div class="container">
            <h1>Tin tức &amp; kiến thức kiểm nghiệm</h1>
            <p class="news-hero-lead">Cập nhật quy chuẩn, chỉ tiêu và hướng dẫn công bố từ phòng thử nghiệm ISO/IEC 17025 (VALAS 217) — TechLAB Global.</p>
        </div>
    </section>
    <section class="news-list-section">
        <div class="container">
            <div class="news-grid">
{chr(10).join(cards)}
            </div>
        </div>
    </section>
{FOOTER}
    <script type="application/ld+json">
    {json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    for article in DATA["articles"]:
        path = OUT / f"{article['slug']}.html"
        path.write_text(render_article(article), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    print("index → tin-tuc/index.html")


if __name__ == "__main__":
    main()
