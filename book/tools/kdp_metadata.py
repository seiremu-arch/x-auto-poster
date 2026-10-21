#!/usr/bin/env python3
"""14冊のKDP登録情報を1枚にまとめ、同時に食い違いを検査する。

使い方:
    python3 book/tools/kdp_metadata.py          # 検査して一覧を書き出す
    python3 book/tools/kdp_metadata.py --check  # 検査だけ（書き出さない）

各巻の `KDP登録情報.md` が正本で、この道具はそこから読む。一覧を手で
書くと、価格を一冊だけ直したときに古い数字が残る。原文の字数で実際に
それが起きたので、同じ失敗を繰り返さないために道具にしてある。

出力は `book/KDP-メタデータ一覧.md`。登録画面を14回うめるとき、
14ファイルを開き直さずに済むようにするためのもの。
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_tr_counts import chars, words           # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = ROOT / "KDP-メタデータ一覧.md"

# 登録の順番。第一巻を先に出してシリーズ名を確定させる
ORDER = ["vol1", "vol2", "en1", "en2", "de1", "de2",
         "es1", "es2", "fr1", "fr2", "it1", "it2", "nl1", "nl2"]

LANG_OF = {"vol": "ja", "en": "en", "de": "de",
           "es": "es", "fr": "fr", "it": "it", "nl": "nl"}

# 言語ごとの市場と電子書籍の軽減税率。税率はロイヤリティの計算に効く
MARKETS = {
    "ja": ("amazon.co.jp", "10%（軽減税率の対象外）"),
    "en": ("amazon.com / .co.uk / .ca / .au", "米国なし・英国0%・加5%ほか"),
    "de": ("amazon.de / .at", "7%"),
    "es": ("amazon.es", "4%"),
    "fr": ("amazon.fr / .ca / .be", "5,5%"),
    "it": ("amazon.it", "4%"),
    "nl": ("amazon.nl / .com.be", "9%（白6%）"),
}


def sections(text: str) -> dict:
    """「## N. 見出し」で本文を切り分ける。見出し語は言語ごとに違うので番号で取る。"""
    out, num = {}, None
    for line in text.split("\n"):
        m = re.match(r"^## (\d+)\.", line)
        if m:
            num = int(m.group(1))
            out[num] = []
        elif num is not None:
            out[num].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table_rows(block: str) -> list:
    """表の行を [左, 右] の並びで返す。見出し行と罫線は落とす。"""
    rows = []
    for line in block.split("\n"):
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == 2 and cells[0] not in ("項目",):
            rows.append(cells)
    return rows


def numbered(block: str) -> list:
    """「1. 中身」の並びを返す。バックティックは外す。"""
    out = []
    for line in block.split("\n"):
        m = re.match(r"^\d+\.\s+(.*?)\s*$", line)
        if m:
            out.append(m.group(1).strip("`"))
    return out


def read_book(vol: str) -> dict:
    path = ROOT / vol / "KDP登録情報.md"
    sec = sections(path.read_text(encoding="utf-8"))
    detail = table_rows(sec.get(1, ""))
    price = table_rows(sec.get(5, ""))
    files = table_rows(sec.get(6, ""))
    lang = LANG_OF[re.sub(r"\d+$", "", vol)]
    ja_vol = vol if vol.startswith("vol") else "vol" + vol[-1]

    story_dir = ROOT / vol / "stories"
    stories = sorted(story_dir.glob("[0-9][0-9]_*.txt"))
    ja_stories = sorted((ROOT / ja_vol / "stories").glob("[0-9][0-9]_*.txt"))

    return {
        "vol": vol,
        "lang": lang,
        "detail": detail,
        "price": {k: v for k, v in price},
        "files": {k: v for k, v in files},
        "description": sec.get(2, "").strip(),
        "keywords": numbered(sec.get(3, "")),
        "categories": numbered(sec.get(4, "")),
        "stories": len(stories),
        "ja_chars": sum(chars(p) for p in ja_stories),
        "words": None if lang == "ja" else sum(words(p) for p in stories),
    }


def field(book: dict, i: int) -> str:
    """詳細表のi行目の右側。行の並びは全14冊で同じ（題・副題・シリーズ・巻・著者・言語・ISBN）。"""
    rows = book["detail"]
    return rows[i][1] if i < len(rows) else ""


def strip_code(s: str) -> str:
    """ファイル名のバックティックと注記を外す。"""
    m = re.search(r"`([^`]+)`", s)
    return m.group(1) if m else s


def check(books: list) -> int:
    """食い違いを報告する。戻り値は要対応の件数。"""
    bad = 0
    print("【検査】")

    for b in books:
        v = b["vol"]
        if len(b["detail"]) < 7:
            print(f"  × {v}: 詳細表の行が足りない（{len(b['detail'])}行、7行必要）")
            bad += 1
        if len(b["keywords"]) != 7:
            print(f"  × {v}: キーワードが{len(b['keywords'])}個（7個必要）")
            bad += 1
        if not 1 <= len(b["categories"]) <= 3:
            print(f"  × {v}: カテゴリーが{len(b['categories'])}個（3個まで）")
            bad += 1
        if b["stories"] != 12:
            print(f"  × {v}: 収録話数が{b['stories']}（12必要）")
            bad += 1
        for label, cell in b["files"].items():
            name = strip_code(cell)
            if not name or label == "用途":
                continue
            if not (DIST / Path(name).name).exists():
                print(f"  × {v}: {label} のファイルがない（{name}）")
                bad += 1

    # シリーズ名は、同じ言語の二巻で巻番号の部分以外が一致していなければならない。
    # ここが一字違うと、Amazonはシリーズページを二つ作る。
    for lang in ("ja", "en", "de", "es", "fr", "it", "nl"):
        pair = [b for b in books if b["lang"] == lang]
        if len(pair) != 2:
            continue
        names = [re.sub(r"[（(].*", "", field(b, 2)).strip() for b in pair]
        if names[0] != names[1]:
            print(f"  × {lang}: シリーズ名が二巻で違う（{names[0]!r} / {names[1]!r}）")
            bad += 1

    # 第7節の「原文N字 → 訳文M words（比R）」は手で書いた一文で、
    # sync_tr_counts.py が同期する表の外にある。訳文を一語直すとここだけ
    # 古くなる。実際に西語版第二巻で、前置詞を一つ直したあと22,735のまま
    # 残っていた。行をまたいで書かれている版もあるので、改行は潰して探す。
    WORDS = re.compile(
        r"原文[\d.,\u00a0]+字\s*→\s*[^\d]*?([\d.,\u00a0]+)\s*words"
        r"（比([\d.]+)）")
    for b in books:
        if b["words"] is None:
            continue
        text = (ROOT / b["vol"] / "KDP登録情報.md").read_text(encoding="utf-8")
        m = WORDS.search(re.sub(r"\s*\n\s*", "", text))
        if not m:
            print(f"  × {b['vol']}: 第7節に語数の一文が見つからない")
            bad += 1
            continue
        written = int(re.sub(r"[.,\u00a0]", "", m.group(1)))
        ratio = f"{b['words'] / b['ja_chars']:.3f}"
        if written != b["words"]:
            print(f"  × {b['vol']}: 第7節の語数が古い"
                  f"（{written:,} と書いてあるが {b['words']:,}）")
            bad += 1
        elif m.group(2) != ratio:
            print(f"  × {b['vol']}: 第7節の比が合わない"
                  f"（{m.group(2)} と書いてあるが {ratio}）")
            bad += 1

    authors = {field(b, 4) for b in books}
    if len(authors) != 1:
        print(f"  × 著者名が揃っていない: {sorted(authors)}")
        bad += 1

    if not bad:
        print("  ○ 食い違いなし（詳細表・キーワード・カテゴリー・"
              "シリーズ名・著者名・ファイルの実在・第7節の語数）")
    return bad


def write(books: list) -> None:
    L = []
    a = L.append

    a("# KDPメタデータ一覧（14冊）")
    a("")
    a("**この表は手で書かない。** 各巻の `KDP登録情報.md` が正本で、")
    a("`python3 book/tools/kdp_metadata.py` が読み直して書き出す。")
    a("価格やキーワードを直すときは各巻のファイルを直して、この道具を走らせる。")
    a("")
    a("登録画面をうめる順に並べてある。各言語とも**第一巻を先に登録**して、")
    a("シリーズ名を確定させてから第二巻を出す。")
    a("")
    a("---")
    a("")
    a("## 1. 一覧")
    a("")
    a("| # | 記号 | 題 | 副題 | シリーズ | 巻 | 言語 | 価格 |")
    a("|---|---|---|---|---|---|---|---|")
    for i, b in enumerate(books, start=1):
        a(f"| {i} | `{b['vol']}` | {field(b, 0)} | {field(b, 1)} | "
          f"{field(b, 2)} | {field(b, 3)} | {field(b, 5)} | "
          f"{b['price'].get('価格', '')} |")
    a("")
    a("## 2. 分量と原稿")
    a("")
    a("| 記号 | 話数 | 原文 | 訳文 | 比 | 原稿 | 表紙 |")
    a("|---|---|---|---|---|---|---|")
    for b in books:
        w = f"{b['words']:,} words" if b["words"] else "—"
        r = f"{b['words'] / b['ja_chars']:.3f}" if b["words"] else "—"
        epub = next((strip_code(v) for k, v in b["files"].items()
                     if "epub" in strip_code(v).lower()), "")
        cover = next((strip_code(v) for k, v in b["files"].items()
                      if "cover" in strip_code(v).lower()
                      or "jpg" in strip_code(v).lower()), "")
        a(f"| `{b['vol']}` | {b['stories']} | {b['ja_chars']:,}字 | {w} | {r} | "
          f"`{Path(epub).name}` | `{Path(cover).name}` |")
    a("")
    a("原文の字数は日本語版の原稿から数えた値で、同じ巻の七言語で同じになる。")
    a("訳文の語数は空白区切りの語数。比は words/字。")
    a("")
    a("## 3. 市場と税率")
    a("")
    a("| 言語 | 主な市場 | 電子書籍の付加価値税 |")
    a("|---|---|---|")
    for lang in ("ja", "en", "de", "es", "fr", "it", "nl"):
        m, vat = MARKETS[lang]
        a(f"| {lang} | {m} | {vat} |")
    a("")
    a("ロイヤリティは**税抜額**に対してかかる。同じ 3,99 € でも、")
    a("西・伊（4%）と蘭（9%）では手取りが違う。登録画面で自動換算させたあと、")
    a("税抜額のほうを確認する。")
    a("")
    a("**KDPセレクト。** 90日間の独占は**言語版ごと**に数える。")
    a("一つの言語版をセレクトに入れても、他の言語版の扱いには影響しない。")
    a("")
    a("---")
    a("")
    a("## 4. 貼り付ける中身")
    a("")
    a("内容紹介もそのまま入れてある。この節だけで登録画面はうまる。")
    a("貼る前に、内容紹介に応募作の文が紛れていないかを `check_overlap.py` が")
    a("見ている（七言語・各巻の第2節を対象にしている）。")
    a("")
    for i, b in enumerate(books, start=1):
        a(f"### {i}. `{b['vol']}` — {field(b, 0)}")
        a("")
        a(f"- **題** {field(b, 0)}")
        a(f"- **副題** {field(b, 1)}")
        a(f"- **シリーズ** {field(b, 2)}")
        a(f"- **言語** {field(b, 5)}　**価格** {b['price'].get('価格', '')}"
          f"　**ロイヤリティ** {b['price'].get('ロイヤリティ', '')}"
          f"　**KDPセレクト** {b['price'].get('KDPセレクト', '')}")
        a("")
        a("<details><summary>内容紹介（そのまま貼り付け可）</summary>")
        a("")
        a(b["description"])
        a("")
        a("</details>")
        a("")
        a("キーワード（7つ、この順）")
        a("")
        for n, k in enumerate(b["keywords"], start=1):
            a(f"{n}. `{k}`")
        a("")
        a("カテゴリー（最大3つ、この順）")
        a("")
        for n, c in enumerate(b["categories"], start=1):
            a(f"{n}. {c}")
        a("")
    a("---")
    a("")
    a("## 5. つまずきやすいところ")
    a("")
    a("1. **シリーズ名は一字一句同じに。** 同じ言語の二巻でシリーズ名が")
    a("   一字でも違うと、Amazonはシリーズページを二つ作る。アポストロフィの")
    a("   形（`'` と `’`）も違いとして数えられる。この道具が検査している。")
    a("2. **ISBNは不要。** KDPが内部管理番号を自動で付ける。自分で買う必要はない。")
    a("3. **著者名は全14冊で同じ綴り。** `Kazu A. Suzuki`。")
    a("   表記が揺れると著者ページが分かれる。")
    a("4. **出版言語は原稿の言語に合わせる。** ここを間違えると、")
    a("   その言語の読者に推薦されない。")
    a("5. **価格は税抜額を確認。** 70%プランが使えるのは")
    a("   2,99 €〜9,99 €（日本は250円〜1,250円）の範囲。")
    a("6. **応募作は一冊も含まない。** 『境界線、未編集』は未発表のままで、")
    a("   14冊のどこにも入っていない。`check_overlap.py` が七言語で")
    a("   機械的に確認している。内容紹介に紛れ込ませないこと。")
    a("")
    a("---")
    a("")
    a("## 6. 出す前に通す検査")
    a("")
    a("```bash")
    a("python3 book/tools/sync_tr_counts.py       # 分量の表を更新")
    a("python3 book/tools/check_tr_structure.py   # 段落の対応")
    a("python3 book/tools/check_tr_terms.py       # 用語と表記")
    a("python3 book/tools/check_tr_quotes.py      # 巻をまたぐ引用")
    a("python3 book/tools/check_overlap.py        # 応募作との重複")
    a("python3 book/tools/kdp_metadata.py         # この一覧を作り直す")
    a("```")
    a("")
    a("Kindle Previewerでの表示確認だけは手元でしかできない。")
    a("引用符とアクセント記号の出かたを、三機種で見ること。")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n書き出した: {OUT.relative_to(ROOT.parent)}（{len(L)}行）")


def main() -> int:
    books = [read_book(v) for v in ORDER]
    bad = check(books)
    if "--check" not in sys.argv:
        write(books)
    if bad:
        print(f"\n要対応 {bad} 件")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
