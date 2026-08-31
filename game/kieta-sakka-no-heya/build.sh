#!/bin/sh
# itch.io の HTML5 枠にそのまま上げられる ZIP を作る（index.html がZIP直下に来る形）
set -e
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/kieta-sakka-no-heya.zip
zip -q -X dist/kieta-sakka-no-heya.zip index.html
echo "dist/kieta-sakka-no-heya.zip"
unzip -l dist/kieta-sakka-no-heya.zip
