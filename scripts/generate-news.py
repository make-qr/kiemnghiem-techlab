#!/usr/bin/env python3
"""Sinh trang tin tức + sitemap.xml từ scripts/news-articles.json."""
from __future__ import annotations

import json
import html
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from news_images import (  # noqa: E402
    ensure_article_images,
    figure_html,
    inject_inline_after_first_section,
    verify_unique,
)

DATA = json.loads((ROOT / "scripts" / "news-articles.json").read_text(encoding="utf-8"))
OUT = ROOT / "tin-tuc"
BASE = "https://kiemnghiem.techlabglobal.com.vn"
CSS_V = "20260905b"
IMG_V = "20260905b"

COMMON_HEAD = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta}">
    <title>{title} | TechLAB Global</title>
    <link rel="canonical" href="{canonical}">
    <link rel="stylesheet" href="../css/style.css?v={css_v}">
    <link rel="stylesheet" href="../css/conversion.css?v={css_v}">
    <link rel="stylesheet" href="../css/news.css?v={css_v}">
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
    <meta property="og:type" content="{og_type}">
    <meta property="og:image" content="{og_image}">
</head>
<body class="{body_class}">
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
                        <li><a href="../sitemap.xml">Sitemap</a></li>
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

FILTER_JS = """
    <script>
    (function () {
        var buttons = document.querySelectorAll('.news-filter-btn');
        var cards = document.querySelectorAll('.news-card[data-tag]');
        var empty = document.getElementById('news-empty');
        if (!buttons.length) return;
        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var tag = btn.getAttribute('data-filter');
                buttons.forEach(function (b) { b.classList.toggle('is-active', b === btn); });
                var visible = 0;
                cards.forEach(function (card) {
                    var show = tag === 'all' || card.getAttribute('data-tag') === tag;
                    card.classList.toggle('is-hidden', !show);
                    if (show) visible += 1;
                });
                if (empty) empty.classList.toggle('is-visible', visible === 0);
            });
        });
    })();
    </script>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def card_html(article: dict, featured: bool = False) -> str:
    slug = article["slug"]
    tag = article["tag"]
    title = esc(article["title"])
    excerpt = esc(article["excerpt"])
    date_d = esc(article["date_display"])
    tag_e = esc(tag)
    thumb = f'../images/tin-tuc/{slug}-hero.jpg?v={IMG_V}'
    if featured:
        return f"""            <article class="news-card news-card--featured" data-tag="{tag_e}">
                <a class="news-card-visual" href="{slug}.html">
                    <img class="news-card-thumb" src="{thumb}" alt="{title}" width="640" height="360" loading="eager">
                    <span class="news-featured-label">Bài nổi bật</span>
                    <h2>{title}</h2>
                </a>
                <div class="news-card-inner">
                    <div class="news-card-meta"><span class="news-card-tag">{tag_e}</span></div>
                    <p>{excerpt}</p>
                    <div class="news-card-footer">
                        <a class="news-card-link" href="{slug}.html">Đọc bài viết <i class="fas fa-arrow-right"></i></a>
                        <span class="news-card-date">{date_d}</span>
                    </div>
                </div>
            </article>"""
    return f"""            <article class="news-card" data-tag="{tag_e}">
                <a class="news-card-media" href="{slug}.html">
                    <img class="news-card-thumb" src="{thumb}" alt="{title}" width="640" height="360" loading="lazy">
                </a>
                <div class="news-card-inner">
                    <div class="news-card-meta"><span class="news-card-tag">{tag_e}</span></div>
                    <h2><a href="{slug}.html">{title}</a></h2>
                    <p>{excerpt}</p>
                    <div class="news-card-footer">
                        <a class="news-card-link" href="{slug}.html">Đọc tiếp <i class="fas fa-arrow-right"></i></a>
                        <span class="news-card-date">{date_d}</span>
                    </div>
                </div>
            </article>"""


def related_aside(current_slug: str, limit: int = 5) -> str:
    others = [a for a in DATA["articles"] if a["slug"] != current_slug][:limit]
    items = "\n".join(
        f'                        <li><a href="{a["slug"]}.html">{esc(a["title"])}</a></li>'
        for a in others
    )
    return f"""                <aside class="news-aside" aria-label="Thông tin bổ sung">
                    <div class="news-aside-card">
                        <h3>Bài liên quan</h3>
                        <ul class="news-aside-list">
{items}
                        </ul>
                    </div>
                    <div class="news-aside-card news-aside-cta">
                        <h3>Cần báo giá?</h3>
                        <p>Lab ISO/IEC 17025 (VALAS 217) — nhận mẫu HN · CT · HCM.</p>
                        <a href="../index.html#bao-gia" class="btn btn-hero-primary">Gửi yêu cầu</a>
                    </div>
                </aside>"""


def related_cards(current_slug: str, limit: int = 3) -> str:
    others = [a for a in DATA["articles"] if a["slug"] != current_slug][:limit]
    return "\n".join(card_html(a) for a in others)


def render_article(article: dict) -> str:
    slug = article["slug"]
    ensure_article_images(slug)
    canonical = f"{BASE}/tin-tuc/{slug}.html"
    og_image = f"{BASE}/images/tin-tuc/{slug}-hero.jpg"
    cta_links = article.get("cta_links") or [
        {"href": "../index.html#bao-gia", "label": "Gửi yêu cầu báo giá", "class": "btn btn-hero-primary"},
        {"href": "tel:0899551228", "label": "Gọi 0899.551.228", "class": "btn btn-hero-secondary"},
    ]
    cta_html = "".join(
        f'<a href="{c["href"]}" class="{c.get("class", "btn")}">{c["label"]}</a>' for c in cta_links
    )
    featured = figure_html(slug, "hero", article["title"], IMG_V, loading="eager")
    inline = figure_html(slug, "inline", article["title"], IMG_V, loading="lazy")
    body = inject_inline_after_first_section(article["body"], inline)
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta"],
        "image": [og_image],
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
    head = COMMON_HEAD.format(
        meta=esc(article["meta"]),
        title=esc(article["title"]),
        canonical=canonical,
        css_v=CSS_V,
        og_type="article",
        og_image=og_image,
        body_class="news-article",
    )
    return f"""{head}
{HEADER}
    <section class="news-article-hero">
        <div class="container">
            <div class="news-article-hero-inner">
                <nav class="news-breadcrumb" aria-label="Breadcrumb">
                    <a href="../index.html">Trang chủ</a>
                    <span class="news-breadcrumb-sep">/</span>
                    <a href="index.html">Tin tức</a>
                    <span class="news-breadcrumb-sep">/</span>
                    <span>{esc(article["tag"])}</span>
                </nav>
                <h1>{esc(article["title"])}</h1>
                <div class="news-article-meta">
                    <span class="news-card-tag">{esc(article["tag"])}</span>
                    <span><i class="far fa-calendar-alt"></i> {esc(article["date_display"])}</span>
                    <span>TechLAB Global</span>
                </div>
            </div>
        </div>
    </section>
    <div class="news-layout">
        <article class="news-article-body">
            <div class="container">
{featured}
                <p class="news-lead">{article["lead"]}</p>
{body}
                <div class="news-cta-box">
                    <p><strong>Cần báo giá kiểm nghiệm?</strong> TechLAB Global — phòng lab ISO/IEC 17025 (VALAS 217), nhận mẫu HN · CT · HCM.</p>
                    <div class="news-cta-actions">{cta_html}</div>
                </div>
            </div>
        </article>
{related_aside(slug)}
    </div>
    <section class="news-related">
        <div class="container">
            <h2>Đọc tiếp</h2>
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
    tags = []
    for a in articles:
        if a["tag"] not in tags:
            tags.append(a["tag"])
    filter_btns = ['                <button type="button" class="news-filter-btn is-active" data-filter="all">Tất cả</button>']
    for tag in tags:
        filter_btns.append(
            f'                <button type="button" class="news-filter-btn" data-filter="{esc(tag)}">{esc(tag)}</button>'
        )
    cards = [card_html(articles[0], featured=True)]
    cards.extend(card_html(a) for a in articles[1:])
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
    head = COMMON_HEAD.format(
        meta=esc(
            "Tin tức & kiến thức kiểm nghiệm thực phẩm, bao bì, dinh dưỡng, ISO 17025 từ phòng thử nghiệm TechLAB Global (VALAS 217)."
        ),
        title="Tin tức kiểm nghiệm",
        canonical=f"{BASE}/tin-tuc/",
        css_v=CSS_V,
        og_type="website",
        og_image=f"{BASE}/images/tin-tuc/{articles[0]['slug']}-hero.jpg" if articles else f"{BASE}/images/logo.png",
        body_class="news-list-page",
    )
    return f"""{head}
{HEADER}
    <section class="news-hero">
        <div class="container">
            <p class="news-eyebrow">Kiến thức phòng lab</p>
            <h1>Tin tức &amp; kiến thức kiểm nghiệm</h1>
            <p class="news-hero-lead">Quy chuẩn, chỉ tiêu và hướng dẫn công bố từ phòng thử nghiệm ISO/IEC 17025 (VALAS 217) — viết cho doanh nghiệp cần quyết định nhanh.</p>
            <div class="news-hero-stats">
                <span><strong>{len(articles)}</strong> bài viết</span>
                <span><strong>{len(tags)}</strong> chủ đề</span>
                <span><strong>VALAS 217</strong> · ISO/IEC 17025</span>
            </div>
        </div>
    </section>
    <section class="news-list-section">
        <div class="container">
            <div class="news-toolbar">
                <p class="news-toolbar-label">Lọc theo chủ đề</p>
                <div class="news-filters" role="toolbar" aria-label="Lọc bài viết">
{chr(10).join(filter_btns)}
                </div>
            </div>
            <div class="news-grid" id="news-grid">
{chr(10).join(cards)}
                <p class="news-empty" id="news-empty">Không có bài trong chủ đề này.</p>
            </div>
        </div>
    </section>
{FOOTER}
{FILTER_JS}
    <script type="application/ld+json">
    {json.dumps(ld, ensure_ascii=False, indent=2)}
    </script>
</body>
</html>
"""


def write_sitemap() -> None:
    today = date.today().isoformat()
    urls: list[tuple[str, str, str, str]] = [
        (f"{BASE}/", today, "weekly", "1.0"),
        (f"{BASE}/ho-so-nang-luc.html", today, "monthly", "0.85"),
        (f"{BASE}/tin-tuc/", today, "weekly", "0.9"),
        (f"{BASE}/privacy-policy.html", today, "yearly", "0.3"),
        (f"{BASE}/thank-you.html", today, "yearly", "0.2"),
    ]
    for page in sorted((ROOT / "pages").glob("*.html")):
        urls.append((f"{BASE}/pages/{page.name}", today, "monthly", "0.8"))
    for article in DATA["articles"]:
        urls.append(
            (
                f"{BASE}/tin-tuc/{article['slug']}.html",
                article.get("date", today),
                "monthly",
                "0.7",
            )
        )

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod, freq, pri in urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{escape(loc)}</loc>")
        parts.append(f"    <lastmod>{lastmod}</lastmod>")
        parts.append(f"    <changefreq>{freq}</changefreq>")
        parts.append(f"    <priority>{pri}</priority>")
        parts.append("  </url>")
    parts.append("</urlset>")
    parts.append("")
    (ROOT / "sitemap.xml").write_text("\n".join(parts), encoding="utf-8")
    print(f"sitemap.xml → {len(urls)} URLs")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image_paths: list[Path] = []
    for article in DATA["articles"]:
        hero, inline = ensure_article_images(article["slug"])
        image_paths.extend([hero, inline])
    verify_unique(image_paths)
    print(f"images unique_ok count={len(image_paths)}")

    for old in OUT.glob("*.html"):
        old.unlink()
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    for article in DATA["articles"]:
        path = OUT / f"{article['slug']}.html"
        path.write_text(render_article(article), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    print("index → tin-tuc/index.html")
    write_sitemap()


if __name__ == "__main__":
    main()
