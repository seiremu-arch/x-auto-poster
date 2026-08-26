#!/usr/bin/env python3
"""Claude Codeのセッションログ(JSONL)から、userとassistantの本文だけをMarkdownに変換する。

元のJSONLは読み取り専用で開き、変更・削除は一切行わない。
"""

import argparse
import json
import sys
from pathlib import Path

SESSION_LOG_DIR = Path("/root/.claude/projects/-home-user-x-auto-poster")
OUTPUT_DIR = Path("/home/user/knowledge-base/raw")
DEFAULT_TARGETS = ["facee82f-8ce4-5217-ad97-223580286bab.jsonl"]

ROLE_LABELS = {"user": "User", "assistant": "Assistant"}


def extract_text(content):
    """message.content から本文テキストだけを取り出す。

    content が文字列ならそれ自体が本文。配列の場合は type=="text" のブロックのみを
    採用し、thinking / tool_use / tool_result は本文ではないので捨てる。
    """
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    texts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text", "").strip()
            if text:
                texts.append(text)
    return "\n\n".join(texts)


def parse_session(jsonl_path):
    """JSONLを1行ずつ読み、(role, timestamp, text) のリストを返す。"""
    turns = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  警告: {jsonl_path.name}:{line_no} を読み飛ばしました ({e})",
                      file=sys.stderr)
                continue

            role = record.get("type")
            if role not in ROLE_LABELS:
                continue

            message = record.get("message")
            if not isinstance(message, dict):
                continue

            text = extract_text(message.get("content"))
            if not text:
                continue

            turns.append((role, record.get("timestamp", ""), text))
    return turns


def render_markdown(session_id, turns):
    lines = [f"# Session {session_id}", ""]
    for role, timestamp, text in turns:
        heading = f"## {ROLE_LABELS[role]}"
        if timestamp:
            heading += f" ({timestamp})"
        lines.extend([heading, "", text, ""])
    return "\n".join(lines).rstrip() + "\n"


def convert(jsonl_path, output_dir):
    turns = parse_session(jsonl_path)
    session_id = jsonl_path.stem
    output_path = output_dir / f"{session_id}.md"
    output_path.write_text(render_markdown(session_id, turns), encoding="utf-8")
    return output_path, len(turns)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", default=None,
                        help="変換するJSONLファイル名またはパス(省略時は既定の1件のみ)")
    parser.add_argument("--source-dir", type=Path, default=SESSION_LOG_DIR,
                        help=f"セッションログのディレクトリ (既定: {SESSION_LOG_DIR})")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR,
                        help=f"Markdownの出力先 (既定: {OUTPUT_DIR})")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    names = args.targets or DEFAULT_TARGETS
    exit_code = 0
    for name in names:
        jsonl_path = Path(name)
        if not jsonl_path.is_absolute():
            jsonl_path = args.source_dir / name
        if not jsonl_path.is_file():
            print(f"エラー: 見つかりません: {jsonl_path}", file=sys.stderr)
            exit_code = 1
            continue
        output_path, count = convert(jsonl_path, args.output_dir)
        print(f"{jsonl_path.name} -> {output_path} ({count} メッセージ)")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
