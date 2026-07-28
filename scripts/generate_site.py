#!/usr/bin/env python3
"""分岐点ニュース: RSSフィードから記事を集め、事実/意見に分けてdocs/index.htmlを生成する。"""

import html
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

ROOT = Path(__file__).resolve().parent.parent
FEEDS_CONFIG = ROOT / "config" / "feeds.json"
OUTPUT_HTML = ROOT / "docs" / "index.html"

JST = timezone(timedelta(hours=9))
MAX_ARTICLES_PER_CATEGORY = 20
MAX_ARTICLES_PER_FEED = 8
REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; BunkitenNewsBot/1.0; +https://github.com/)"

CATEGORY_LABELS = {"fact": "事実", "opinion": "意見"}


def load_feeds():
    config = json.loads(FEEDS_CONFIG.read_text(encoding="utf-8"))
    return [f for f in config["feeds"] if not f.get("name", "").startswith("_")]


def parse_published(entry):
    for key in ("published_parsed", "updated_parsed"):
        value = entry.get(key)
        if value:
            return datetime(*value[:6], tzinfo=timezone.utc)
    return None


def fetch_feed_articles(feed_config):
    articles = []
    error = None
    try:
        parsed = feedparser.parse(
            feed_config["url"],
            agent=USER_AGENT,
            request_headers={"User-Agent": USER_AGENT},
        )
        if parsed.bozo and not parsed.entries:
            raise parsed.bozo_exception or RuntimeError("failed to parse feed")

        for entry in parsed.entries[:MAX_ARTICLES_PER_FEED]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue
            summary = entry.get("summary", "") or ""
            published = parse_published(entry)
            articles.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                    "source": feed_config["name"],
                }
            )
    except Exception as exc:  # noqa: BLE001 - a broken feed must not stop the whole run
        error = f"{feed_config['name']}: {exc}"

    return articles, error


def collect_articles(feeds):
    by_category = {"fact": [], "opinion": []}
    errors = []

    for feed_config in feeds:
        articles, error = fetch_feed_articles(feed_config)
        if error:
            errors.append(error)
        category = feed_config.get("category")
        if category in by_category:
            by_category[category].extend(articles)

    for category, articles in by_category.items():
        articles.sort(
            key=lambda a: a["published"] or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        by_category[category] = articles[:MAX_ARTICLES_PER_CATEGORY]

    return by_category, errors


def render_article(article):
    title = html.escape(article["title"])
    link = html.escape(article["link"])
    source = html.escape(article["source"])
    if article["published"]:
        published_jst = article["published"].astimezone(JST)
        time_str = published_jst.strftime("%m/%d %H:%M")
    else:
        time_str = ""
    return f"""
      <li class="article">
        <a class="article-title" href="{link}" target="_blank" rel="noopener noreferrer">{title}</a>
        <div class="article-meta">{source}{' ・ ' + time_str if time_str else ''}</div>
      </li>"""


def render_section(category, articles):
    label = CATEGORY_LABELS[category]
    if not articles:
        body = '<li class="empty">現在取得できる記事がありません。</li>'
    else:
        body = "".join(render_article(a) for a in articles)
    return f"""
    <section class="category category-{category}">
      <h2>{label}</h2>
      <ul class="article-list">{body}
      </ul>
    </section>"""


def render_html(by_category, errors):
    now_jst = datetime.now(JST)
    date_str = now_jst.strftime("%Y年%m月%d日 %H:%M JST")
    sections = "".join(
        render_section(category, by_category.get(category, []))
        for category in ("fact", "opinion")
    )
    error_note = ""
    if errors:
        items = "".join(f"<li>{html.escape(e)}</li>" for e in errors)
        error_note = f"""
    <details class="errors">
      <summary>取得できなかったフィード ({len(errors)})</summary>
      <ul>{items}</ul>
    </details>"""

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>分岐点ニュース</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #f8f9fb;
    --fg: #1a1d24;
    --muted: #6b7280;
    --border: #e2e5ea;
    --accent-fact: #1d6fd6;
    --accent-opinion: #b45f18;
    --card-bg: #f1f3f6;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #10121a;
      --fg: #e8eaef;
      --muted: #9096a3;
      --border: #262b36;
      --accent-fact: #6ea8ff;
      --accent-opinion: #f0a35e;
      --card-bg: #181b24;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #10121a;
    --fg: #e8eaef;
    --muted: #9096a3;
    --border: #262b36;
    --accent-fact: #6ea8ff;
    --accent-opinion: #f0a35e;
    --card-bg: #181b24;
  }}
  :root[data-theme="light"] {{
    --bg: #f8f9fb;
    --fg: #1a1d24;
    --muted: #6b7280;
    --border: #e2e5ea;
    --accent-fact: #1d6fd6;
    --accent-opinion: #b45f18;
    --card-bg: #f1f3f6;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 0 1rem 3rem;
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
    line-height: 1.6;
  }}
  header {{
    max-width: 760px;
    margin: 0 auto;
    padding: 2.5rem 0 1rem;
  }}
  h1 {{
    margin: 0 0 0.25rem;
    font-size: 1.75rem;
  }}
  .subtitle {{
    color: var(--muted);
    font-size: 0.9rem;
    margin: 0;
  }}
  main {{
    max-width: 760px;
    margin: 0 auto;
    display: grid;
    gap: 2rem;
  }}
  .category h2 {{
    font-size: 1.1rem;
    border-bottom: 2px solid var(--border);
    padding-bottom: 0.4rem;
    margin-bottom: 0.75rem;
  }}
  .category-fact h2 {{ color: var(--accent-fact); border-color: var(--accent-fact); }}
  .category-opinion h2 {{ color: var(--accent-opinion); border-color: var(--accent-opinion); }}
  .article-list {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.6rem;
  }}
  .article {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
  }}
  .article-title {{
    color: var(--fg);
    text-decoration: none;
    font-weight: 600;
    display: block;
  }}
  .article-title:hover {{ text-decoration: underline; }}
  .article-meta {{
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 0.3rem;
    font-variant-numeric: tabular-nums;
  }}
  .empty {{ color: var(--muted); list-style: none; }}
  .errors {{
    max-width: 760px;
    margin: 2rem auto 0;
    color: var(--muted);
    font-size: 0.8rem;
  }}
  footer {{
    max-width: 760px;
    margin: 2rem auto 0;
    color: var(--muted);
    font-size: 0.75rem;
    text-align: center;
  }}
</style>
</head>
<body>
  <header>
    <h1>分岐点ニュース</h1>
    <p class="subtitle">最終更新: {date_str} ・ 直近ニュースを事実/意見に分けて自動更新</p>
  </header>
  <main>{sections}
  </main>
  {error_note}
  <footer>
    <p>本サイトはRSSフィード由来の情報を自動集約したものです。分類はフィード単位の簡易的な分類であり、完全な事実/意見の判定を保証するものではありません。</p>
  </footer>
</body>
</html>
"""


def main():
    feeds = load_feeds()
    by_category, errors = collect_articles(feeds)
    html_content = render_html(by_category, errors)
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")

    total_articles = sum(len(v) for v in by_category.values())
    print(f"Wrote {OUTPUT_HTML} with {total_articles} articles.")
    if errors:
        print(f"{len(errors)} feed(s) failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
