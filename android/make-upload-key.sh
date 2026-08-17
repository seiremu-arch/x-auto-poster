#!/usr/bin/env bash
# タイムボクシングのアップロード鍵(署名鍵)を作るスクリプト。
#
#   cd android && ./make-upload-key.sh
#
# 生成した upload-keystore.jks と keystore.properties は .gitignore 済みで、
# リポジトリには入りません。**鍵とパスワードは必ず自分で控えて保管してください。**
# Play Console にアップロードした後にこの鍵を失うと、同じアプリの更新を
# 出せなくなります(Play アプリ署名の鍵リセット申請が必要になります)。
set -euo pipefail

cd "$(dirname "$0")"

KEYSTORE=upload-keystore.jks
ALIAS=upload

if [ -e "$KEYSTORE" ]; then
  echo "既に $KEYSTORE があります。作り直す場合は先に退避してください。" >&2
  exit 1
fi

if ! command -v keytool > /dev/null 2>&1; then
  echo "keytool が見つかりません。JDK(17以上)をインストールしてください。" >&2
  echo "  macOS: brew install temurin   /   Android Studio 同梱の JDK でも可" >&2
  exit 1
fi

read -r -s -p "キーストアのパスワード(6文字以上): " STORE_PASS; echo
read -r -s -p "もう一度入力: " STORE_PASS2; echo
if [ "$STORE_PASS" != "$STORE_PASS2" ]; then
  echo "パスワードが一致しません。" >&2
  exit 1
fi
if [ ${#STORE_PASS} -lt 6 ]; then
  echo "パスワードは6文字以上にしてください。" >&2
  exit 1
fi

keytool -genkeypair -v \
  -keystore "$KEYSTORE" \
  -alias "$ALIAS" \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass "$STORE_PASS" -keypass "$STORE_PASS" \
  -dname "CN=TimeBoxing, OU=, O=, L=, ST=, C=JP"

cat > keystore.properties <<EOF
storeFile=$KEYSTORE
storePassword=$STORE_PASS
keyAlias=$ALIAS
keyPassword=$STORE_PASS
EOF
chmod 600 keystore.properties "$KEYSTORE"

echo
echo "--------------------------------------------------------------"
echo "作成しました: android/$KEYSTORE と android/keystore.properties"
echo
echo "【手元でビルドする場合】これだけで署名されます:"
echo "    ./gradlew bundleRelease"
echo
echo "【GitHub Actions で署名する場合】リポジトリの"
echo "  Settings → Secrets and variables → Actions → New repository secret"
echo "に次の4つを登録してください:"
echo
echo "  ANDROID_KEYSTORE_BASE64    ← 下のコマンドの出力("
echo "                                base64 -w0 $KEYSTORE  ※macOSは base64 -i $KEYSTORE )"
echo "  ANDROID_KEYSTORE_PASSWORD  ← 入力したパスワード"
echo "  ANDROID_KEY_ALIAS          ← $ALIAS"
echo "  ANDROID_KEY_PASSWORD       ← 入力したパスワード"
echo
echo "鍵ファイルは安全な場所にバックアップしてください(紛失すると更新が出せません)。"
echo "--------------------------------------------------------------"
