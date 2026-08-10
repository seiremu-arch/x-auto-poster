#!/usr/bin/env python3
"""Obsidian vault(vault/)に案件ノート・ナレッジノートを新規作成する。

使い方:
    python scripts/new_note.py 案件 "新しい案件名"
    python scripts/new_note.py ナレッジ "トピック名" --分野 GitHub

案件は vault/案件/<案件名>/<案件名>.md を、
ナレッジは vault/ナレッジ/<分野>/<トピック名>.md を作り、
どちらも vault/ホーム.md の該当セクションにウィキリンクを追記する。
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
HOME = VAULT / "ホーム.md"

# Obsidianのウィキリンクが壊れる文字
INVALID_CHARS = set('/\\:|#^[]')

案件テンプレート = """---
type: 案件
status: 進行中
created: {today}
updated: {today}
tags:
  - 案件/{title}
---

# {title}

## 概要

## 現状

## 関連ノート

## 使っているナレッジ

## 次にやること

- [ ]

---

親: [[ホーム]] / 書き方: [[運用ルール]]
"""

ナレッジテンプレート = """---
type: ナレッジ
created: {today}
updated: {today}
tags:
  - {分野}
---

# {title}

## 要点

## 詳細

## ハマったこと

## 使っている案件

## 関連

---

親: [[ホーム]] / 書き方: [[運用ルール]]
"""


def validate_title(title):
    title = title.strip()
    if not title:
        sys.exit("エラー: タイトルが空です。")
    bad = sorted(INVALID_CHARS & set(title))
    if bad:
        sys.exit(f"エラー: タイトルに使えない文字が含まれています: {' '.join(bad)}")
    return title


def write_note(path, content):
    if path.exists():
        sys.exit(f"エラー: すでに存在します: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"作成: {path.relative_to(ROOT)}")


def find_heading(lines, heading):
    pattern = re.compile(rf"^#+\s+{re.escape(heading)}\s*$")
    return next((i for i, line in enumerate(lines) if pattern.match(line)), None)


def section_end(lines, start, level):
    """見出し start の節が終わる行番号(同じか上位の見出しが来る位置)を返す。"""
    for i in range(start + 1, len(lines)):
        stripped = lines[i].lstrip("#")
        depth = len(lines[i]) - len(stripped)
        if lines[i].startswith("#") and depth <= level:
            return i
    return len(lines)


def create_subsection(lines, parent, heading):
    """親見出しの節の末尾に `### <heading>` を足し、その行番号を返す。"""
    parent_at = find_heading(lines, parent)
    if parent_at is None:
        return None
    end = section_end(lines, parent_at, 2)
    # 節末尾の空行を食わないように、直前の非空行の後ろへ差し込む
    while end > parent_at + 1 and not lines[end - 1].strip():
        end -= 1
    lines[end:end] = ["", f"### {heading}"]
    return end + 1


def add_home_link(heading, link_line, parent=None):
    """ホーム.md の指定見出しの直後のリスト末尾にリンクを追記する。

    見出しが無く parent が指定されていれば、その配下に見出しごと作る。
    """
    if not HOME.exists():
        print(f"警告: {HOME.relative_to(ROOT)} が無いのでリンクを追記できません。", file=sys.stderr)
        return

    lines = HOME.read_text(encoding="utf-8").splitlines()

    start = find_heading(lines, heading)
    if start is None and parent:
        start = create_subsection(lines, parent, heading)
        if start is not None:
            print(f"ホーム.md に見出しを追加: ### {heading}")
    if start is None:
        print(f"警告: ホーム.md に見出し「{heading}」が無いのでリンクを追記できません。", file=sys.stderr)
        return

    if link_line in lines:
        print(f"ホーム.md にはすでにリンクがあります: {link_line}")
        return

    # 見出しの次の見出しが来る手前までの範囲で、最後のリスト項目の後ろに挿す
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            end = i
            break

    last_item = None
    for i in range(start + 1, end):
        if lines[i].lstrip().startswith("- "):
            last_item = i

    insert_at = last_item + 1 if last_item is not None else start + 1
    if last_item is None:
        # リスト項目がまだ無いセクション: 見出し直後に空行を挟んで置く
        lines.insert(insert_at, "")
        insert_at += 1

    lines.insert(insert_at, link_line)
    HOME.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ホーム.md に追記: {link_line}")


def create_案件(title):
    title = validate_title(title)
    path = VAULT / "案件" / title / f"{title}.md"
    write_note(path, 案件テンプレート.format(title=title, today=date.today().isoformat()))
    add_home_link("案件", f"- [[{title}]]")


def create_ナレッジ(title, 分野):
    title = validate_title(title)
    分野 = validate_title(分野)
    path = VAULT / "ナレッジ" / 分野 / f"{title}.md"
    write_note(
        path,
        ナレッジテンプレート.format(title=title, 分野=分野, today=date.today().isoformat()),
    )
    add_home_link(分野, f"- [[{title}]]", parent="ナレッジ")


def main():
    parser = argparse.ArgumentParser(
        description="vault/ に案件・ナレッジのノートを作る",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("種別", choices=["案件", "ナレッジ"], help="作るノートの種別")
    parser.add_argument("タイトル", help="ノートのタイトル(ファイル名になる)")
    parser.add_argument(
        "--分野",
        help="ナレッジの分野フォルダ名(例: GitHub, RSS, Python)。ナレッジのとき必須",
    )
    args = parser.parse_args()

    if args.種別 == "案件":
        if args.分野:
            print("注意: 案件では --分野 は無視されます。", file=sys.stderr)
        create_案件(args.タイトル)
    else:
        if not args.分野:
            parser.error("ナレッジには --分野 が必要です(例: --分野 GitHub)")
        create_ナレッジ(args.タイトル, args.分野)

    print("\n作成したノートに、関連ノートへのリンクを最低1本張ってください(vault/運用ルール.md)。")


if __name__ == "__main__":
    main()
