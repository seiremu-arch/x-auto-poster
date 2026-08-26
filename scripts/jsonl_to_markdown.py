#!/usr/bin/env python3
"""Claude Codeのセッションログ(JSONL)から、userとassistantの本文だけをMarkdownに変換する。

手動実行と、Stop hookからの自動実行の両方に対応する。
Stop hookから呼ばれた場合は、stdinで渡されるJSONの transcript_path を変換対象にする。

Stop hook全体を巻き込んで失敗させないため、どんなエラーでも終了コードは常に0。
元のJSONLは読み取り専用で開き、変更・削除は一切行わない。
"""

import argparse
import json
import os
import select
import sys
import tempfile
from pathlib import Path

SESSION_LOG_DIR = Path("/root/.claude/projects/-home-user-x-auto-poster")
OUTPUT_DIR = Path("/home/user/knowledge-base/raw")
DEFAULT_TARGETS = ["facee82f-8ce4-5217-ad97-223580286bab.jsonl"]

ROLE_LABELS = {"user": "User", "assistant": "Assistant"}

# stdinにhookのJSONが来ているかを待つ上限。手動実行時に固まらないための保険。
STDIN_WAIT_SECONDS = 0.5


def warn(message):
    """失敗を1行だけstderrに出す。hookのログを汚さないようトレースバックは出さない。"""
    print(f"jsonl_to_markdown: {message}", file=sys.stderr)


def read_hook_payload():
    """Stop hookがstdinで渡すJSONを読む。hook起動でなければ None を返す。

    端末からの手動実行(stdinがTTY)や、stdinに何も来ない場合はブロックせず
    None を返すので、従来どおりの手動実行を妨げない。
    """
    try:
        if sys.stdin is None or sys.stdin.closed or sys.stdin.isatty():
            return None
        if not select.select([sys.stdin], [], [], STDIN_WAIT_SECONDS)[0]:
            return None
        raw = sys.stdin.read()
    except Exception:
        return None

    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


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
    """JSONLを読み取り専用で開き、(turns, 壊れた行数) を返す。

    turns は (role, timestamp, text) のリスト。書き込み途中の行が混じっていても
    落ちないよう、壊れた行は数えて読み飛ばす。
    """
    turns = []
    skipped = 0
    with jsonl_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if not isinstance(record, dict):
                skipped += 1
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
    return turns, skipped


def render_markdown(session_id, turns):
    lines = [f"# Session {session_id}", ""]
    for role, timestamp, text in turns:
        heading = f"## {ROLE_LABELS[role]}"
        if timestamp:
            heading += f" ({timestamp})"
        lines.extend([heading, "", text, ""])
    return "\n".join(lines).rstrip() + "\n"


def write_atomic(path, text):
    """同じディレクトリの一時ファイルに書いてから置き換える。

    途中で失敗しても、中途半端な内容のMarkdownが残らないようにする。
    """
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent),
                                    prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        # mkstempは0600で作るので、通常のファイル作成と同じくumask基準に直す。
        umask = os.umask(0)
        os.umask(umask)
        os.chmod(tmp_name, 0o666 & ~umask)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def convert(jsonl_path, output_dir):
    """1件のJSONLをMarkdownに変換する。出力名は元ファイルのstem + '.md'。"""
    turns, skipped = parse_session(jsonl_path)
    session_id = jsonl_path.stem
    output_path = output_dir / f"{session_id}.md"
    write_atomic(output_path, render_markdown(session_id, turns))
    return output_path, len(turns), skipped


def resolve_targets(targets, source_dir):
    """相対指定はセッションログのディレクトリ基準、絶対指定はそのまま使う。"""
    resolved = []
    for name in targets:
        path = Path(name)
        resolved.append(path if path.is_absolute() else source_dir / name)
    return resolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*",
                        help="変換するJSONLファイル名またはパス"
                             "(省略時はstdinのtranscript_path、それも無ければ既定の1件)")
    parser.add_argument("--source-dir", type=Path, default=SESSION_LOG_DIR,
                        help=f"セッションログのディレクトリ (既定: {SESSION_LOG_DIR})")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR,
                        help=f"Markdownの出力先 (既定: {OUTPUT_DIR})")
    parser.add_argument("--quiet", action="store_true",
                        help="成功時の標準出力を抑制する")
    args = parser.parse_args()

    # 引数が明示されていればstdinは読まない(手動実行がstdin待ちで固まらないように)。
    payload = read_hook_payload() if not args.targets else None
    hook_mode = payload is not None
    quiet = args.quiet or hook_mode

    if args.targets:
        targets = resolve_targets(args.targets, args.source_dir)
    else:
        transcript_path = payload.get("transcript_path") if payload else None
        if isinstance(transcript_path, str) and transcript_path.strip():
            targets = [Path(transcript_path.strip())]
        else:
            targets = resolve_targets(DEFAULT_TARGETS, args.source_dir)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        warn(f"出力先を作成できません: {args.output_dir} ({e})")
        return 0

    for jsonl_path in targets:
        try:
            if not jsonl_path.is_file():
                warn(f"見つかりません: {jsonl_path}")
                continue
            output_path, count, skipped = convert(jsonl_path, args.output_dir)
        except Exception as e:
            warn(f"変換に失敗しました: {jsonl_path} ({type(e).__name__}: {e})")
            continue

        # hook実行時は末尾1行が書き込み途中のことがあるため、1行だけの欠けは黙認する。
        if skipped and (not quiet or skipped > 1):
            warn(f"{jsonl_path.name}: 壊れた行を {skipped} 行スキップしました")
        if not quiet:
            print(f"{jsonl_path.name} -> {output_path} ({count} メッセージ)")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        # Stop hookを巻き込まないよう、想定外の例外でも0で終える。
        warn(f"予期しないエラー: {type(e).__name__}: {e}")
        sys.exit(0)
