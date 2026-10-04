#!/usr/bin/env bash
# Playwright MCP の起動ラッパー(.mcp.json から呼ぶ想定)。
# - Claude Code のクラウドセッション: 同梱の Chromium を使い、headless / no-sandbox で起動する
#   (@playwright/mcp が期待するブラウザ版とは違うので、パスを明示しないと起動しない)
# - ローカル: 画面があれば普通にブラウザ窓が開く
set -euo pipefail

args=()
if [[ -x /opt/pw-browsers/chromium ]]; then
  args+=(--executable-path /opt/pw-browsers/chromium --no-sandbox)
fi
if [[ "${CLAUDE_CODE_REMOTE:-}" == "true" || ( -z "${DISPLAY:-}" && "$(uname)" == "Linux" ) ]]; then
  args+=(--headless)
fi

exec npx -y @playwright/mcp@latest "${args[@]}" "$@"
