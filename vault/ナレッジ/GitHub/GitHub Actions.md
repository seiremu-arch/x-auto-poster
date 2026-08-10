---
type: ナレッジ
created: 2026-08-10
updated: 2026-08-10
tags:
  - GitHub
---

# GitHub Actions

## 要点

定期実行してリポジトリに自動コミットさせる用途のメモ。ハマりどころは **cronはUTC**、**scheduleは既定ブランチのみ**、**書き込みには権限指定が要る** の3つ。

## 詳細

### cronはUTC

タイムゾーン指定は無い。日本時間に直すには9時間引く。

```yaml
on:
  schedule:
    - cron: "0 21 * * *"   # 21:00 UTC = 翌日 06:00 JST
  workflow_dispatch: {}
```

`workflow_dispatch: {}` を併記しておくと、Actionsタブから手動実行できる。定期実行の動作確認はこれでやる。

### scheduleは既定ブランチのワークフローしか動かない

feature ブランチに置いた `schedule` は**永遠に発火しない**。`main` にマージされて初めて動く。ブランチ上で確認したいときは `workflow_dispatch` を使う。

なお、リポジトリが60日間活動していないと schedule は自動で止まる。

### 書き込み権限

`GITHUB_TOKEN` は既定では読み取りのみ。プッシュするなら明示する。

```yaml
permissions:
  contents: write
```

### 差分があるときだけコミット

生成物を毎日コミットする系では、無変更でも空コミットが積まれないようにする。

```bash
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add docs/index.html
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "chore: update daily news ($(date -u +%Y-%m-%d))"
  git push
fi
```

`git diff --cached --quiet` はステージ済みの差分が無いとき終了コード0。

### 同時実行の抑制

手動実行と定期実行がぶつかるとプッシュが競合する。

```yaml
concurrency:
  group: daily-news-update
  cancel-in-progress: false
```

`cancel-in-progress: false` にすると、走っているジョブは殺さず後続を待たせる。生成物をコミットする処理は途中で殺したくないのでこちら。

## ハマったこと

- 自動コミットのプッシュは、他のワークフローを連鎖起動しない(`GITHUB_TOKEN` によるpushは `on: push` を発火させない)。無限ループ防止の仕様。
- ブランチ保護をかけていると bot のプッシュも弾かれる。

## 使っている案件

- [[分岐点ニュース]] — [[構成とデータフロー]] に実際のジョブ構成

## 関連

- [[GitHub Pages]]

---

親: [[ホーム]] / 書き方: [[運用ルール]]
