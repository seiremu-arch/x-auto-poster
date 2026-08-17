# x-auto-poster / 分岐点ニュース

RSSフィードから直近のニュースを集め、「事実」と「意見」に分けて毎朝自動更新する静的サイトです。GitHub Actions が毎日決まった時刻にニュースを取得し、`docs/index.html` を再生成して GitHub Pages で公開します。

## 仕組み

1. `.github/workflows/daily-update.yml` が毎日 06:00 JST(21:00 UTC)に実行される
2. `scripts/generate_site.py` が `config/feeds.json` に登録されたRSSフィードを取得
3. フィードごとに設定された `category`(`fact`=事実 / `opinion`=意見)に振り分けて `docs/index.html` を生成
4. 変更があれば自動でコミット・プッシュ
5. GitHub Pages(`main` ブランチの `/docs`)が更新後のページを配信

手動で今すぐ更新したい場合は、GitHub の Actions タブから `Daily News Update` ワークフローを `Run workflow` で実行できます。

## 初回セットアップ(手動で1回だけ必要)

GitHub Pages の公開設定は git push だけでは有効化されないため、リポジトリの管理者が以下を一度だけ行ってください。

1. GitHub のリポジトリ → **Settings** → **Pages**
2. **Source** を `Deploy from a branch` に設定
3. Branch を `main` / フォルダを `/docs` に設定して **Save**

これで `https://<owner>.github.io/x-auto-poster/` でサイトが公開されます。

> 補足: GitHub の `schedule` トリガーは既定ブランチ(通常 `main`)にマージされたワークフローのみ実行されます。このブランチが `main` にマージされるまで、自動実行はされません(`workflow_dispatch` による手動実行は可能)。

## タイムボクシング(ラウンドタイマー)

`docs/timeboxing.html` は同じ GitHub Pages で配信される単独のラウンドタイマーです。公開URLは `https://<owner>.github.io/x-auto-poster/timeboxing.html`(ローカルではファイルを直接ブラウザで開くだけで動きます)。

- プリセット: **入門者** = 3分 × 3ラウンド、**新人** = 3分 × 4ラウンド(いずれもインターバル1分)
- 自由設定: ラウンド数 3/4/6/8/10/12、1ラウンド 3分・2分・1分、インターバル 30秒・1分・1分30秒
- 開始で「カン」とゴング、3分後に再びゴング、インターバルを挟んで次のラウンドへ。最終ラウンド終了時はゴングが3回
- ラウンド残り10秒に拍子木の合図(オン/オフ可)、画面にはボクシングのシルエットと進捗リング
- スペースキーで開始/一時停止、`R` でリセット。計測中は画面のスリープを抑止(Screen Wake Lock 対応ブラウザのみ)

音源ファイルは持たず、ゴングと拍子木は Web Audio API でブラウザ内で合成しています。自動再生制限のため、最初にボタンを押してから音が鳴ります。ニュース生成スクリプトは `docs/index.html` しか書き換えないため、このページは日次更新の影響を受けません。

### Android アプリ(App Bundle / AAB)

`android/` に Android 版のプロジェクトがあります。`docs/timeboxing.html` をそのまま assets に取り込んで WebView で表示する構成なので、**Web版とアプリ版でファイルは1つだけ**です(ビルド時に自動コピー)。ネットワークを使わないため、パーミッションは1つも宣言していません。

| 項目 | 値 |
| --- | --- |
| applicationId | `com.seiremu.timeboxing` |
| 対応OS | Android 8.0 (API 26) 以上 / targetSdk 35 |
| ビルド | AGP 8.7.3 / Gradle 8.11.1 / JDK 17以上 |

#### GitHub Actions でビルドする(Android SDK 不要)

`.github/workflows/android-build.yml` が `android/**` または `docs/timeboxing.html` の変更で自動実行されます(Actions タブから手動実行も可)。完了後、実行ページ下部の Artifacts から取得できます。

- `timeboxing-aab` … `app-release.aab`(Google Play アップロード用)
- `timeboxing-debug-apk` … `app-debug.apk`(端末にそのまま入れて動作確認する用)

#### 手元でビルドする

```bash
cd android
./gradlew bundleRelease   # → app/build/outputs/bundle/release/app-release.aab
./gradlew assembleDebug   # → app/build/outputs/apk/debug/app-debug.apk
```

Android SDK(platform 35 / build-tools 35.0.0)が必要です。Android Studio で `android/` フォルダを開いても構いません。

#### 署名(Play にアップロードする場合)

アップロード鍵を作り、`android/keystore.properties`(`keystore.properties.example` をコピー)に指定するとリリースビルドが署名されます。

```bash
keytool -genkeypair -v -keystore upload-keystore.jks \
        -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

CI で署名する場合は、リポジトリの Secrets に `ANDROID_KEYSTORE_BASE64`(`base64 -w0 upload-keystore.jks` の出力)、`ANDROID_KEYSTORE_PASSWORD`、`ANDROID_KEY_ALIAS`、`ANDROID_KEY_PASSWORD` を登録してください。未設定でもビルドは通りますが、AAB は未署名になります。鍵ファイルと `keystore.properties` は `.gitignore` 済みで、リポジトリには含めません。

## フィードの追加・変更

`config/feeds.json` を編集してください。

```json
{
  "name": "表示名",
  "url": "https://example.com/rss.xml",
  "category": "fact"  // または "opinion"
}
```

- `fact`: 速報・事実報道系のフィード
- `opinion`: コラム・論評・分析系のフィード

分類はフィード単位の簡易的なヒューリスティックであり、記事単位で厳密に事実/意見を判定しているわけではありません。ニュースサイトはRSS配信を予告なく変更・終了することがあるため、フィードが取得できなくなった場合はこのファイルを更新してください(取得に失敗したフィードはページ下部の「取得できなかったフィード」に表示されます)。

## ローカルでの実行

```bash
pip install -r requirements.txt
python scripts/generate_site.py
```

`docs/index.html` が生成されます。
