#!/usr/bin/env python3
"""Vaultの読み書き。ノートはfrontmatter付きMarkdownで、frontmatterのエッジがグラフになる。

設計は vault/README.md を参照。ここには「追記のみ」「IDは安定」という2つの原則だけを
コードとして固定してある。
"""

import hashlib
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
INBOX = VAULT / "00-inbox"
NOTES = VAULT / "10-notes"
SOURCES = VAULT / "20-sources"
ARTIFACTS = VAULT / "30-artifacts"
RUNS = VAULT / "40-runs"
MEMORY = VAULT / "MEMORY.md"

NOTE_DIRS = (INBOX, NOTES, SOURCES, ARTIFACTS, RUNS)

JST = timezone(timedelta(hours=9))

# frontmatterに書いたIDがそのままグラフの辺になる。derived_fromは出自(claim <- capture)。
EDGE_KEYS = ("supports", "contradicts", "supersedes", "derived_from")
REQUIRED_KEYS = ("id", "type", "title", "status")
NOTE_TYPES = ("capture", "claim", "entity", "source", "artifact", "run")
NOTE_STATUSES = ("inbox", "promoted", "active", "archived")

# frontmatterに書く順番。読みやすさのためだけの並びで、意味はない。
KEY_ORDER = (
    "id",
    "type",
    "title",
    "status",
    "source",
    "category",
    "url",
    "published",
    "captured_at",
    "promoted_at",
    "tags",
    *EDGE_KEYS,
)

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)


def now_jst():
    return datetime.now(JST).replace(microsecond=0)


def iso(dt):
    """frontmatterに入れる文字列表現。Noneはそのまま返す。"""
    if dt is None:
        return None
    if isinstance(dt, str):
        return dt
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(JST).replace(microsecond=0).isoformat()


def make_id(*parts):
    """安定ID。同じ入力からは常に同じIDが出るので、これが重複検知の鍵になる。"""
    raw = "\x00".join(p for p in parts if p)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def parse_note(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        frontmatter = {}
    return frontmatter, match.group(2)


def read_note(path):
    return parse_note(Path(path).read_text(encoding="utf-8"))


def dump_note(frontmatter, body):
    ordered = {}
    for key in KEY_ORDER:
        if key in frontmatter and frontmatter[key] not in (None, ""):
            ordered[key] = frontmatter[key]
    for key, value in frontmatter.items():  # KEY_ORDERに無いキーも落とさない
        if key not in ordered and value not in (None, ""):
            ordered[key] = value
    header = yaml.safe_dump(ordered, allow_unicode=True, sort_keys=False, width=10**6)
    body = body.strip("\n")
    return f"---\n{header}---\n\n{body}\n"


def write_note(path, frontmatter, body):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_note(frontmatter, body), encoding="utf-8")
    return path


def append_to_note(path, text):
    """本文への追記。書き換えないというルールを守るための唯一の更新手段。"""
    path = Path(path)
    frontmatter, body = read_note(path)
    body = body.rstrip("\n") + "\n\n" + text.strip("\n")
    return write_note(path, frontmatter, body)


def note_paths(*dirs):
    for directory in dirs or NOTE_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            yield path


def iter_notes(*dirs):
    for path in note_paths(*dirs):
        frontmatter, body = read_note(path)
        yield path, frontmatter, body


def index_by_id(*dirs):
    """id -> [path, ...]。重複IDもreviewで検知したいのでリストで持つ。"""
    index = {}
    for path, frontmatter, _ in iter_notes(*dirs):
        note_id = frontmatter.get("id")
        if note_id:
            index.setdefault(str(note_id), []).append(path)
    return index


def known_ids():
    return set(index_by_id().keys())


def edges(frontmatter, key):
    value = frontmatter.get(key) or []
    if isinstance(value, str):
        value = [value]
    return [str(v) for v in value if v]


def tags(frontmatter):
    return edges(frontmatter, "tags")


def note_filename(note_id, when=None, prefix=""):
    when = when or now_jst()
    stem = f"{when.strftime('%Y-%m-%d')}-{prefix}{note_id}"
    return f"{stem}.md"


def update_memory_last_run(text):
    """MEMORY.mdの `<!-- loop:last-run -->` ブロックだけを差し替える。

    本文の他の部分には触らない(触ると「書き換えない」というルールが崩れる)。
    """
    if not MEMORY.exists():
        return None
    content = MEMORY.read_text(encoding="utf-8")
    block = f"<!-- loop:last-run -->\n{text.strip()}\n<!-- /loop:last-run -->"
    pattern = re.compile(
        r"<!-- loop:last-run -->.*?<!-- /loop:last-run -->", re.DOTALL
    )
    if not pattern.search(content):
        content = content.rstrip("\n") + "\n\n## 直近のラン\n\n" + block + "\n"
    else:
        content = pattern.sub(lambda _: block, content, count=1)
    MEMORY.write_text(content, encoding="utf-8")
    return MEMORY
