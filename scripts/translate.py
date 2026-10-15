#!/usr/bin/env python3
"""英語フィードの見出しとRSS要約を、Claude APIで日本語に訳す。

訳すのはRSSに載っている見出しと短い要約(リード文)だけで、記事本文は取りに行かない。
ANTHROPIC_API_KEY が無い・APIが失敗した、といった場合は原文のまま返す
(翻訳が落ちてもサイト生成は止めない)。
"""

import html
import os
import re
import sys

MODEL = "claude-opus-5-5"
MAX_SUMMARY_CHARS = 600

SYSTEM_PROMPT = """あなたは経済・国際ニュースの翻訳者です。
英語のニュース見出しと要約を、日本の新聞の見出し・リード文として自然な日本語に訳してください。
- 意訳はしても、原文にない情報・評価は足さない
- 固有名詞は日本の主要メディアで定着している表記を使う(例: Federal Reserve → 米連邦準備理事会(FRB))
- 見出しは簡潔に、要約は「です・ます」ではなく「だ・である」調で
- 要約が空の記事は summary_ja も空文字にする
- 入力と同じ index を付けて、すべての記事を返す"""

TAG_RE = re.compile(r"<[^>]+>")


def plain_text(value):
    """RSSの要約に混ざるHTMLタグと実体参照を落とす。"""
    return " ".join(html.unescape(TAG_RE.sub(" ", value or "")).split())


def translate_articles(articles):
    """articles の各要素に title_ja / summary_ja を足す(その場で更新し、エラー文字列を返す)。"""
    if not articles:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return "翻訳をスキップしました(ANTHROPIC_API_KEY が設定されていません)"

    try:
        import anthropic
        from pydantic import BaseModel
    except ImportError as exc:
        return f"翻訳をスキップしました(ライブラリがありません: {exc.name})"

    class Translation(BaseModel):
        index: int
        title_ja: str
        summary_ja: str

    class TranslationBatch(BaseModel):
        items: list[Translation]

    lines = []
    for i, article in enumerate(articles):
        summary = plain_text(article.get("summary"))[:MAX_SUMMARY_CHARS]
        lines.append(f"[{i}]\nTitle: {article['title']}\nSummary: {summary}")

    try:
        client = anthropic.Anthropic()
        response = client.messages.parse(
            model=MODEL,
            max_tokens=16000,
            output_config={"effort": "low"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": "\n\n".join(lines)}],
            output_format=TranslationBatch,
        )
    except anthropic.AuthenticationError:
        return "翻訳をスキップしました(ANTHROPIC_API_KEY が無効です)"
    except anthropic.APIConnectionError:
        return "翻訳をスキップしました(Claude APIに接続できません)"
    except anthropic.APIStatusError as exc:
        return f"翻訳をスキップしました(Claude API: {exc.status_code} {exc.message})"

    if response.stop_reason != "end_turn" or response.parsed_output is None:
        return f"翻訳をスキップしました(stop_reason={response.stop_reason})"

    for item in response.parsed_output.items:
        if 0 <= item.index < len(articles):
            articles[item.index]["title_ja"] = item.title_ja.strip()
            articles[item.index]["summary_ja"] = item.summary_ja.strip()
    return None


if __name__ == "__main__":
    # 手元での確認用: python scripts/translate.py "Headline" ["Summary"]
    sample = [{"title": sys.argv[1], "summary": " ".join(sys.argv[2:])}]
    err = translate_articles(sample)
    print(err or f"{sample[0].get('title_ja')}\n{sample[0].get('summary_ja')}")
