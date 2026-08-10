#!/usr/bin/env python3
"""vault/ 内のウィキリンクが壊れていないか、孤立ノートが無いかを検査する。

使い方:
    python scripts/check_vault_links.py

未解決リンクがあれば終了コード1で終わる。孤立ノート(どこからもリンクされて
いないノート)は警告のみで、終了コードには影響しない。
コードブロック・インラインコード内の [[...]] は、Obsidianがリンクとして
扱わないため検査対象から除外する。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"

WIKILINK = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]+)?\]\]")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
PLACEHOLDER = re.compile(r"\{\{|<[^>]+>|\.\.\.")


def strip_code(text):
    """コードブロックとインラインコードを取り除く。"""
    out = []
    in_fence = False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(INLINE_CODE.sub("", line))
    return "\n".join(out)


def main():
    if not VAULT.exists():
        sys.exit(f"エラー: {VAULT} がありません。")

    notes = {p.stem: p for p in VAULT.rglob("*.md")}
    broken = []
    linked_to = set()

    for path in sorted(VAULT.rglob("*.md")):
        text = strip_code(path.read_text(encoding="utf-8"))
        for match in WIKILINK.finditer(text):
            target = match.group(1).strip()
            if not target or PLACEHOLDER.search(target):
                continue  # テンプレートの雛形表記は無視
            if target in notes:
                linked_to.add(target)
            else:
                broken.append((path.relative_to(VAULT), target))

    print(f"ノート: {len(notes)} 件")

    if broken:
        print(f"\n未解決リンク: {len(broken)} 件")
        for src, target in broken:
            print(f"  {src} -> [[{target}]]")
    else:
        print("未解決リンク: なし")

    orphans = sorted(n for n in notes if n not in linked_to and n != "ホーム")
    if orphans:
        print(f"\n警告: どこからもリンクされていないノート {len(orphans)} 件")
        for name in orphans:
            print(f"  {name}")
        print("  → 上位ノート(案件ハブ / ホーム)からリンクを張ってください。")
    else:
        print("孤立ノート: なし")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
