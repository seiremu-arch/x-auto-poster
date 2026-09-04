#!/usr/bin/env python3
"""Loop Engineering のCLI: capture → context → agent/draft → review → commit。

状態はチャットではなくVault(`vault/`)にある。このスクリプトは、そのVaultに
「落とす」「集める」「昇格させる」「検証する」の4つだけを提供する。
考えるのはClaudeの仕事なので、ここには判断ロジックを置かない。

    python scripts/loop.py capture              # RSSから00-inboxへ
    python scripts/loop.py capture --note "..."  # 思いつきを00-inboxへ
    python scripts/loop.py context <id>          # 文脈バンドルを出力
    python scripts/loop.py promote <id>          # 10-notesに原子ノートを作る
    python scripts/loop.py archive               # 滞留したinboxノートを畳む
    python scripts/loop.py canvas                # エッジから vault/graph.canvas を作る
    python scripts/loop.py review                # スキーマとエッジを検証
    python scripts/loop.py status                # Vaultの現在地
"""

import argparse
import html as html_lib
import json
import os
import re
import sys
import uuid
from collections import Counter
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import vault  # noqa: E402  (パス調整のあとに読む)

STALE_INBOX_DAYS = 30
CONTEXT_MAX_CHARS = 8000
SUMMARY_MAX_CHARS = 600

# JSON Canvas (https://jsoncanvas.org/spec/1.0/) の出力設定。
# Obsidianで `vault/` を開いたときに、frontmatterのエッジをそのまま図として見るためのもの。
CANVAS_PATH = vault.VAULT / "graph.canvas"
CANVAS_COLUMN_ORDER = ("source", "capture", "claim", "entity", "artifact", "run")
CANVAS_COLORS = {  # Obsidianのプリセット色(1=赤 2=橙 3=黄 4=緑 5=水 6=紫)
    "source": "5",
    "capture": "2",
    "claim": "4",
    "entity": "6",
    "artifact": "3",
    "run": "1",
}
CANVAS_NODE_WIDTH = 380
CANVAS_NODE_HEIGHT = 120
CANVAS_COLUMN_GAP = 280
CANVAS_ROW_GAP = 60
CANVAS_GROUP_PADDING = 40

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t　]+")


# --------------------------------------------------------------------------- 共通

def plain_text(raw, limit=SUMMARY_MAX_CHARS):
    text = html_lib.unescape(TAG_RE.sub(" ", raw or ""))
    text = WS_RE.sub(" ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def dedupe(items):
    seen, out = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def parse_dt(value):
    if not value:
        return None
    if not isinstance(value, str):
        return value
    try:
        return vault.datetime.fromisoformat(value)
    except ValueError:
        return None


def resolve(ref):
    """IDでもファイルパスでも受け取れるようにする。曖昧なら候補を出して止める。"""
    index = vault.index_by_id()
    if ref in index:
        paths = index[ref]
        if len(paths) > 1:
            raise SystemExit(f"IDが重複しています: {ref}\n" + "\n".join(str(p) for p in paths))
        return paths[0]

    candidate = Path(ref)
    if candidate.exists():
        return candidate

    matches = [p for p in vault.note_paths() if ref in p.name]
    matches += [paths[0] for note_id, paths in index.items() if ref in note_id and paths[0] not in matches]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(f"ノートが見つかりません: {ref}")
    raise SystemExit("候補が複数あります:\n" + "\n".join(str(p) for p in matches))


def rel(path):
    path = Path(path)
    try:
        return path.relative_to(vault.ROOT).as_posix()
    except ValueError:  # リポジトリの外を指しているとき(canvas --output など)
        return path.as_posix()


# --------------------------------------------------------------------------- capture

def source_note(feed):
    """フィード1本につき1ノート。同じURLなら常に同じIDになる。"""
    source_id = vault.make_id(feed["url"])
    path = vault.SOURCES / f"{source_id}.md"
    if not path.exists():
        vault.write_note(
            path,
            {
                "id": source_id,
                "type": "source",
                "title": feed["name"],
                "status": "active",
                "url": feed["url"],
                "category": feed.get("category"),
                "captured_at": vault.iso(vault.now_jst()),
                "tags": [],
            },
            f"`config/feeds.json` に登録された情報源。分類は `{feed.get('category')}`。",
        )
    return source_id


def capture_article(article, feed, source_id, now):
    note_id = vault.make_id(article["link"])
    path = vault.INBOX / vault.note_filename(note_id, now)
    frontmatter = {
        "id": note_id,
        "type": "capture",
        "title": article["title"],
        "status": "inbox",
        "source": article["source"],
        "category": feed.get("category"),
        "url": article["link"],
        "published": vault.iso(article.get("published")),
        "captured_at": vault.iso(now),
        "tags": [],
        "derived_from": [source_id],
    }
    summary = plain_text(article.get("summary"))
    body = summary or "(要約なし)"
    body += "\n\n## メモ\n\n<!-- ここに判断を書く。書いたら `loop.py promote` で10-notesへ。 -->"
    vault.write_note(path, frontmatter, body)
    return path


def capture_feeds(limit_per_feed, dry_run):
    from generate_site import fetch_feed_articles, load_feeds  # 遅延import(reviewはfeedparser不要)

    now = vault.now_jst()
    seen = vault.known_ids()
    created, skipped, errors = [], 0, []

    for feed in load_feeds():
        articles, error = fetch_feed_articles(feed)
        if error:
            errors.append(error)
            continue
        source_id = None if dry_run else source_note(feed)
        for article in articles[:limit_per_feed]:
            note_id = vault.make_id(article["link"])
            if note_id in seen:
                skipped += 1
                continue
            seen.add(note_id)
            if dry_run:
                created.append(Path(f"(dry-run) {article['title']}"))
                continue
            created.append(capture_article(article, feed, source_id, now))

    return created, skipped, errors


def capture_thought(text, tags, dry_run):
    now = vault.now_jst()
    note_id = vault.make_id(text, now.isoformat())
    path = vault.INBOX / vault.note_filename(note_id, now, prefix="note-")
    if dry_run:
        return path
    vault.write_note(
        path,
        {
            "id": note_id,
            "type": "capture",
            "title": plain_text(text, 60),
            "status": "inbox",
            "source": "manual",
            "captured_at": vault.iso(now),
            "tags": tags,
        },
        text.strip(),
    )
    return path


def write_run_note(kind, created, skipped, errors, dry_run):
    now = vault.now_jst()
    # ランは同一秒に複数回走りうるので、IDは内容ではなく一意性で決める
    run_id = vault.make_id("run", now.isoformat(), uuid.uuid4().hex)
    lines = [
        f"- 種別: {kind}",
        f"- 新規キャプチャ: {len(created)}件",
        f"- 重複スキップ: {skipped}件",
        f"- 失敗した情報源: {len(errors)}件",
    ]
    if created:
        lines.append("")
        lines.append("## 新規ノート")
        lines.append("")
        lines += [f"- `{rel(p)}`" for p in created]
    if errors:
        lines.append("")
        lines.append("## 取得できなかった情報源")
        lines.append("")
        lines += [f"- {e}" for e in errors]

    body = "\n".join(lines)
    if dry_run:
        return None
    path = vault.RUNS / vault.note_filename(run_id, now, prefix="run-")
    vault.write_note(
        path,
        {
            "id": run_id,
            "type": "run",
            "title": f"{kind} {now.strftime('%Y-%m-%d %H:%M')}",
            "status": "archived",
            "captured_at": vault.iso(now),
            "tags": [],
        },
        body,
    )
    vault.update_memory_last_run(
        f"- {now.strftime('%Y-%m-%d %H:%M')} `{kind}` — 新規 {len(created)} / "
        f"重複 {skipped} / 失敗 {len(errors)} (`{rel(path)}`)"
    )
    return path


def cmd_capture(args):
    if args.note:
        path = capture_thought(args.note, args.tag, args.dry_run)
        print(f"captured: {rel(path) if not args.dry_run else path}")
        write_run_note("capture(manual)", [path], 0, [], args.dry_run)
        return 0

    created, skipped, errors = capture_feeds(args.limit, args.dry_run)
    run_path = write_run_note("capture(feeds)", created, skipped, errors, args.dry_run)
    for path in created:
        print(f"captured: {path if args.dry_run else rel(path)}")
    print(f"新規 {len(created)} / 重複スキップ {skipped} / 失敗 {len(errors)}")
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    if run_path:
        print(f"run note: {rel(run_path)}")
    return 0


# --------------------------------------------------------------------------- context

def incoming_edges(target_id):
    found = []
    for path, frontmatter, _ in vault.iter_notes():
        for key in vault.EDGE_KEYS:
            if target_id in vault.edges(frontmatter, key):
                found.append((key, path, frontmatter))
    return found


def render_note_line(path, frontmatter):
    return (
        f"- `{frontmatter.get('id')}` [{frontmatter.get('type')}/{frontmatter.get('status')}] "
        f"{frontmatter.get('title')} — `{rel(path)}`"
    )


def cmd_context(args):
    path = resolve(args.ref)
    frontmatter, body = vault.read_note(path)
    note_id = str(frontmatter.get("id", ""))
    index = vault.index_by_id()

    out = [f"# 文脈バンドル: {frontmatter.get('title')}", "", f"対象: `{rel(path)}`", ""]

    out.append("## このノート")
    out.append("")
    out.append(vault.dump_note(frontmatter, body).rstrip())
    out.append("")

    out.append("## 出ていくエッジ")
    out.append("")
    outgoing = False
    for key in vault.EDGE_KEYS:
        for edge_id in vault.edges(frontmatter, key):
            outgoing = True
            paths = index.get(edge_id)
            if not paths:
                out.append(f"- {key} → `{edge_id}` (**リンク切れ**)")
                continue
            target_fm, _ = vault.read_note(paths[0])
            out.append(f"- {key} → {render_note_line(paths[0], target_fm)[2:]}")
    if not outgoing:
        out.append("(なし)")
    out.append("")

    out.append("## 入ってくるエッジ")
    out.append("")
    incoming = incoming_edges(note_id) if note_id else []
    if incoming:
        for key, other_path, other_fm in incoming:
            out.append(f"- {key} ← {render_note_line(other_path, other_fm)[2:]}")
    else:
        out.append("(なし)")
    out.append("")

    note_tags = set(vault.tags(frontmatter))
    source = frontmatter.get("source")
    neighbours = []
    for other_path, other_fm, _ in vault.iter_notes(vault.INBOX, vault.NOTES):
        if other_path == path:
            continue
        shared = note_tags & set(vault.tags(other_fm))
        same_source = source and other_fm.get("source") == source
        if shared or same_source:
            reason = "tag:" + ",".join(sorted(shared)) if shared else "same-source"
            neighbours.append((reason, other_path, other_fm))

    out.append(f"## 近いノート ({len(neighbours)}件)")
    out.append("")
    if neighbours:
        for reason, other_path, other_fm in neighbours[: args.max_neighbours]:
            out.append(f"{render_note_line(other_path, other_fm)} ({reason})")
        if len(neighbours) > args.max_neighbours:
            out.append(f"- …ほか {len(neighbours) - args.max_neighbours}件(省略)")
    else:
        out.append("(なし)")
    out.append("")

    if vault.MEMORY.exists():
        out.append("## MEMORY.md")
        out.append("")
        out.append(vault.MEMORY.read_text(encoding="utf-8").strip())
        out.append("")

    text = "\n".join(out)
    if len(text) > args.max_chars:
        text = text[: args.max_chars] + (
            f"\n\n<!-- {args.max_chars}文字で打ち切り。長すぎる場合はノートを分割する(ルール3) -->\n"
        )
    print(text)
    print(f"\n<!-- 約{len(text)}文字 -->", file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- promote

def cmd_promote(args):
    path = resolve(args.ref)
    frontmatter, _ = vault.read_note(path)
    capture_id = str(frontmatter.get("id", ""))
    now = vault.now_jst()

    title = args.title or frontmatter.get("title") or "(無題)"
    claim_id = vault.make_id("claim", capture_id, title)
    if claim_id in vault.known_ids():
        raise SystemExit(f"同じ主張のノートが既にあります: {claim_id}")

    claim_path = vault.NOTES / vault.note_filename(claim_id, now, prefix="claim-")
    vault.write_note(
        claim_path,
        {
            "id": claim_id,
            "type": args.type,
            "title": title,
            "status": "active",
            "source": frontmatter.get("source"),
            "url": frontmatter.get("url"),
            "promoted_at": vault.iso(now),
            "tags": dedupe(vault.tags(frontmatter) + args.tag),
            "supports": [],
            "contradicts": [],
            "supersedes": [],
            "derived_from": [capture_id] if capture_id else [],
        },
        "## 主張\n\n"
        "<!-- 1文で書く。1ノート=1主張。 -->\n\n"
        "## 根拠\n\n"
        f"- 出典: `{rel(path)}`\n\n"
        "## 反証されうる点\n\n"
        "<!-- 何が観測されたらこの主張を撤回するか。 -->",
    )

    # 元のキャプチャは書き換えない。状態遷移だけ更新して、本文には追記する。
    frontmatter["status"] = "promoted"
    frontmatter["promoted_at"] = vault.iso(now)
    _, body = vault.read_note(path)
    vault.write_note(path, frontmatter, body)
    vault.append_to_note(
        path,
        f"## 昇格 {now.strftime('%Y-%m-%d')}\n\n- → `{claim_id}` `{rel(claim_path)}`",
    )

    print(f"promoted: {rel(path)} → {rel(claim_path)}")
    print(f"次: {claim_path.name} の「主張」を1文で書き、`loop.py review` で検証する")
    return 0


# --------------------------------------------------------------------------- archive

def cmd_archive(args):
    """滞留したinboxノートを畳む。本文は消さず、status を archived にして追記するだけ。"""
    now = vault.now_jst()
    cutoff = timedelta(days=args.days)
    archived = []

    for path, frontmatter, body in vault.iter_notes(vault.INBOX):
        if frontmatter.get("status") != "inbox":
            continue
        captured = parse_dt(frontmatter.get("captured_at"))
        if not captured or now - captured <= cutoff:
            continue
        if args.dry_run:
            archived.append(path)
            continue
        frontmatter["status"] = "archived"
        vault.write_note(path, frontmatter, body)
        vault.append_to_note(
            path,
            f"## 保留 {now.strftime('%Y-%m-%d')}\n\n"
            f"- {args.days}日間昇格されなかったため archived。"
            "扱う気になったら status を inbox に戻す。",
        )
        archived.append(path)

    for path in archived:
        print(f"archived: {rel(path)}")
    print(f"{len(archived)}件を archived にしました({args.days}日超)")
    return 0


# --------------------------------------------------------------------------- canvas

def canvas_selection(include_inbox=False, include_runs=False):
    """キャンバスに載せるノートを選ぶ。

    既定は知識グラフだけ: `10-notes` / `20-sources` / `30-artifacts` と、そこから
    参照されているキャプチャ。`00-inbox` は毎朝増えるので、昇格して誰かに参照された
    ものしか載らない(全部載せると図が読めなくなり、差分も毎日荒れる)。
    """
    notes = {}
    for path, frontmatter, _ in vault.iter_notes():
        note_id = str(frontmatter.get("id", ""))
        if note_id:
            notes.setdefault(note_id, (path, frontmatter))

    selected = {}
    for note_id, (path, frontmatter) in notes.items():
        wanted = (
            path.parent in (vault.NOTES, vault.SOURCES, vault.ARTIFACTS)
            or (include_inbox and path.parent == vault.INBOX)
            or (include_runs and path.parent == vault.RUNS)
        )
        if wanted:
            selected[note_id] = (path, frontmatter)

    # 主張や成果物が指している先は、inboxにあっても載せる(出自が見えないと図にならない)
    for _, (_, frontmatter) in list(selected.items()):
        for key in vault.EDGE_KEYS:
            for edge_id in vault.edges(frontmatter, key):
                if edge_id in notes and edge_id not in selected:
                    selected[edge_id] = notes[edge_id]
    return selected


def canvas_node_id(note_id):
    return vault.make_id("canvas-node", note_id, length=16)


def compact(obj):
    """値がNoneのキーを落とす。JSON Canvasの任意フィールドを空で書かないため。"""
    return {key: value for key, value in obj.items() if value is not None}


def build_canvas(selected):
    """frontmatterのエッジをそのままJSON Canvasにする。type別に列を作って並べるだけ。"""
    columns = {}
    for note_id, (path, frontmatter) in selected.items():
        columns.setdefault(frontmatter.get("type") or "capture", []).append((path, note_id))

    ordered_types = [t for t in CANVAS_COLUMN_ORDER if t in columns]
    ordered_types += sorted(t for t in columns if t not in CANVAS_COLUMN_ORDER)

    groups, nodes = [], []
    for column, note_type in enumerate(ordered_types):
        entries = sorted(columns[note_type], key=lambda entry: entry[0].name)
        x = column * (CANVAS_NODE_WIDTH + CANVAS_COLUMN_GAP)
        height = len(entries) * (CANVAS_NODE_HEIGHT + CANVAS_ROW_GAP) - CANVAS_ROW_GAP
        color = CANVAS_COLORS.get(note_type)
        groups.append(compact({
            "id": vault.make_id("canvas-group", note_type, length=16),
            "type": "group",
            "x": x - CANVAS_GROUP_PADDING,
            "y": -CANVAS_GROUP_PADDING,
            "width": CANVAS_NODE_WIDTH + CANVAS_GROUP_PADDING * 2,
            "height": height + CANVAS_GROUP_PADDING * 2,
            "label": f"{note_type} ({len(entries)})",
            "color": color,
        }))
        for row, (path, note_id) in enumerate(entries):
            nodes.append(compact({
                "id": canvas_node_id(note_id),
                "type": "file",
                "file": path.relative_to(vault.VAULT).as_posix(),
                "x": x,
                "y": row * (CANVAS_NODE_HEIGHT + CANVAS_ROW_GAP),
                "width": CANVAS_NODE_WIDTH,
                "height": CANVAS_NODE_HEIGHT,
                "color": color,
            }))

    edges = []
    for note_id, (_, frontmatter) in sorted(selected.items()):
        for key in vault.EDGE_KEYS:
            for edge_id in vault.edges(frontmatter, key):
                if edge_id not in selected:
                    continue  # 載せていないノートへのエッジは描かない(リンク切れは review が見る)
                edges.append({
                    "id": vault.make_id("canvas-edge", note_id, key, edge_id, length=16),
                    "fromNode": canvas_node_id(note_id),
                    "toNode": canvas_node_id(edge_id),
                    "toEnd": "arrow",
                    "label": key,
                })

    # グループを先に置く(配列の順序がそのままz-index。先頭が一番下)
    return {"nodes": groups + nodes, "edges": edges}


def render_canvas(canvas):
    return json.dumps(canvas, ensure_ascii=False, indent=2) + "\n"


def cmd_canvas(args):
    wider = args.include_inbox or args.all
    if wider and not args.output:
        # `vault/graph.canvas` は既定の選び方で固定する。ここが可変だと `--check` と
        # `review` の陳腐化チェックが「どの選び方と比べるか」を決められなくなる。
        raise SystemExit(
            "--include-inbox / --all は使い捨ての図なので `--output` が要ります\n"
            "例: python scripts/loop.py canvas --all --output /tmp/all.canvas"
        )

    selected = canvas_selection(include_inbox=wider, include_runs=args.all)
    canvas = build_canvas(selected)
    text = render_canvas(canvas)
    path = Path(args.output) if args.output else CANVAS_PATH

    if args.check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == text:
            print(f"最新です: {rel(path)}")
            return 0
        print(
            f"{rel(path)} がノートと食い違っています。"
            "`python scripts/loop.py canvas` で作り直してください",
            file=sys.stderr,
        )
        return 1

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    files = sum(1 for node in canvas["nodes"] if node.get("type") == "file")
    print(f"canvas: {rel(path)} — ノート {files}件 / エッジ {len(canvas['edges'])}件")
    return 0


# --------------------------------------------------------------------------- review

def review_canvases(errors):
    """`.canvas` もグラフなので、frontmatterのエッジと同じ強さで検証する。"""
    for path in sorted(vault.VAULT.rglob("*.canvas")):
        where = rel(path)
        try:
            canvas = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{where}: JSONとして読めない ({exc})")
            continue

        node_ids = set()
        for node in canvas.get("nodes") or []:
            node_id = node.get("id")
            if not node_id:
                errors.append(f"{where}: `id` のないノードがある")
                continue
            if node_id in node_ids:
                errors.append(f"{where}: ノードIDが重複: {node_id}")
            node_ids.add(node_id)
            if node.get("type") == "file" and not (vault.VAULT / node.get("file", "")).exists():
                errors.append(f"{where}: 存在しないファイルを指すノード → {node.get('file')}")

        for edge in canvas.get("edges") or []:
            for key in ("fromNode", "toNode"):
                if edge.get(key) not in node_ids:
                    errors.append(f"{where}: エッジの `{key}` が解決できない → {edge.get(key)}")


def review_bases(errors):
    """`.base` はVaultの見え方を決めるので、YAMLとして壊れていたらエラーにする。"""
    for path in sorted(vault.VAULT.rglob("*.base")):
        try:
            vault.yaml.safe_load(path.read_text(encoding="utf-8"))
        except vault.yaml.YAMLError as exc:
            errors.append(f"{rel(path)}: YAMLとして読めない ({exc})")


def cmd_review(args):
    errors, warnings = [], []
    index = vault.index_by_id()

    for note_id, paths in sorted(index.items()):
        if len(paths) > 1:
            joined = ", ".join(rel(p) for p in paths)
            errors.append(f"IDが重複: {note_id} ({joined})")

    now = vault.now_jst()
    for path, frontmatter, body in vault.iter_notes():
        where = rel(path)
        for key in vault.REQUIRED_KEYS:
            if not frontmatter.get(key):
                errors.append(f"{where}: frontmatterに `{key}` がない")

        note_type = frontmatter.get("type")
        if note_type and note_type not in vault.NOTE_TYPES:
            errors.append(f"{where}: 未知の type `{note_type}`")

        status = frontmatter.get("status")
        if status and status not in vault.NOTE_STATUSES:
            errors.append(f"{where}: 未知の status `{status}`")

        note_id = str(frontmatter.get("id", ""))
        if note_id and note_id not in path.stem:
            errors.append(f"{where}: ファイル名にID `{note_id}` が含まれていない")

        for key in vault.EDGE_KEYS:
            for edge_id in vault.edges(frontmatter, key):
                if edge_id == note_id:
                    errors.append(f"{where}: `{key}` が自分自身を指している")
                elif edge_id not in index:
                    errors.append(f"{where}: `{key}` のリンク切れ → {edge_id}")

        if not body.strip():
            warnings.append(f"{where}: 本文が空")

        if path.parent == vault.INBOX and status == "inbox":
            captured = parse_dt(frontmatter.get("captured_at"))
            if captured and now - captured > timedelta(days=STALE_INBOX_DAYS):
                age = (now - captured).days
                warnings.append(
                    f"{where}: inboxに{age}日滞留。昇格するか status を archived にする"
                )

    if not vault.MEMORY.exists():
        errors.append("vault/MEMORY.md がない")

    review_canvases(errors)
    review_bases(errors)

    if CANVAS_PATH.exists():
        expected = render_canvas(build_canvas(canvas_selection()))
        if CANVAS_PATH.read_text(encoding="utf-8") != expected:
            warnings.append(
                f"{rel(CANVAS_PATH)}: ノートと食い違っている。"
                "`python scripts/loop.py canvas` で作り直す"
            )

    for line in errors:
        print(f"ERROR {line}")
    for line in warnings:
        print(f"WARN  {line}")
    print(f"\nノート {sum(len(p) for p in index.values())}件 / "
          f"エラー {len(errors)}件 / 警告 {len(warnings)}件")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


# --------------------------------------------------------------------------- status

def cmd_status(args):
    counts, statuses, tag_counter = Counter(), Counter(), Counter()
    stale = 0
    now = vault.now_jst()

    for path, frontmatter, _ in vault.iter_notes():
        counts[path.parent.name] += 1
        statuses[frontmatter.get("status", "?")] += 1
        tag_counter.update(vault.tags(frontmatter))
        if path.parent == vault.INBOX and frontmatter.get("status") == "inbox":
            captured = parse_dt(frontmatter.get("captured_at"))
            if captured and now - captured > timedelta(days=STALE_INBOX_DAYS):
                stale += 1

    print("# Vault status\n")
    print("## ディレクトリ別")
    for name in ("00-inbox", "10-notes", "20-sources", "30-artifacts", "40-runs"):
        print(f"- {name}: {counts.get(name, 0)}")
    print("\n## status別")
    for name, count in sorted(statuses.items()):
        print(f"- {name}: {count}")
    if tag_counter:
        print("\n## よく出るタグ")
        for tag, count in tag_counter.most_common(10):
            print(f"- {tag}: {count}")
    if stale:
        print(f"\n滞留中のinboxノート: {stale}件 ({STALE_INBOX_DAYS}日超)")

    runs = sorted(vault.note_paths(vault.RUNS))
    if runs:
        print(f"\n直近のラン: `{rel(runs[-1])}`")
    return 0


# --------------------------------------------------------------------------- CLI

def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_capture = sub.add_parser("capture", help="00-inboxに落とす")
    p_capture.add_argument("--note", help="RSSではなく、手で書いた思いつきを落とす")
    p_capture.add_argument("--tag", action="append", default=[], help="タグ(複数可)")
    p_capture.add_argument("--limit", type=int, default=8, help="フィード1本あたりの最大取り込み件数")
    p_capture.add_argument("--dry-run", action="store_true", help="書き込まずに結果だけ出す")
    p_capture.set_defaults(func=cmd_capture)

    p_context = sub.add_parser("context", help="ノート1件の文脈バンドルを出力する")
    p_context.add_argument("ref", help="IDまたはファイルパス")
    p_context.add_argument("--max-neighbours", type=int, default=15)
    p_context.add_argument("--max-chars", type=int, default=CONTEXT_MAX_CHARS)
    p_context.set_defaults(func=cmd_context)

    p_promote = sub.add_parser("promote", help="キャプチャを10-notesの原子ノートに昇格する")
    p_promote.add_argument("ref", help="IDまたはファイルパス")
    p_promote.add_argument("--title", help="主張のタイトル(省略時は元ノートのタイトル)")
    p_promote.add_argument("--type", default="claim", choices=vault.NOTE_TYPES)
    p_promote.add_argument("--tag", action="append", default=[])
    p_promote.set_defaults(func=cmd_promote)

    p_archive = sub.add_parser("archive", help="滞留したinboxノートをarchivedにする")
    p_archive.add_argument("--days", type=int, default=STALE_INBOX_DAYS)
    p_archive.add_argument("--dry-run", action="store_true")
    p_archive.set_defaults(func=cmd_archive)

    p_canvas = sub.add_parser("canvas", help="エッジから vault/graph.canvas を生成する")
    p_canvas.add_argument("--include-inbox", action="store_true",
                          help="00-inboxのノートも全部載せる(--output が要る)")
    p_canvas.add_argument("--all", action="store_true",
                          help="ランも含めて全ノートを載せる(--output が要る)")
    p_canvas.add_argument("--output", help="出力先(既定は vault/graph.canvas)")
    p_canvas.add_argument("--check", action="store_true", help="書き込まず、最新かどうかだけ確認する")
    p_canvas.set_defaults(func=cmd_canvas)

    p_review = sub.add_parser("review", help="スキーマとエッジを機械的に検証する")
    p_review.add_argument("--strict", action="store_true", help="警告もエラー扱いにする")
    p_review.set_defaults(func=cmd_review)

    p_status = sub.add_parser("status", help="Vaultの現在地")
    p_status.set_defaults(func=cmd_status)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except BrokenPipeError:  # `| head` などで打ち切られたとき
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


if __name__ == "__main__":
    sys.exit(main())
