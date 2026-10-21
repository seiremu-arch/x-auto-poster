# ドイツ語版『Das Traumamt』KDP登録情報

第一巻のドイツ語版です。KDPの登録画面にそのままコピーして貼れる形でまとめてあります。
貼り付ける中身はドイツ語、説明は日本語で書いてあります。

日本語版とも英語版とも**別の本**として登録します。主戦場は amazon.de です。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Buchtitel | Das Traumamt |
| Untertitel | Zwölf Nächte |
| Reihe | Das Traumamt（Band 1） |
| 巻番号 | 1 |
| Verfasser | Kazu A. Suzuki |
| 出版言語 | Deutsch |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

英語版とはシリーズ名が違います（`Das Traumamt` と `The Dream Editing Bureau`）。
言語ごとに別のシリーズになるので、これで正しい動きです。

---

## 2. Beschreibung（そのまま貼り付け可）

Träume lassen sich nicht löschen. Sie lassen sich nur leichter machen.

Während Sie schlafen, macht das Gehirn eine Erinnerung weich, verbindet sie neu und lässt sie wieder setzen. Traumbearbeitung ist die Arbeit, bei diesen wenigen Sekunden dabei zu sein und die Hand, die neu verbindet, ein ganz klein wenig zu verändern.

Mehr als das Gewicht einer Erinnerung zu senken, ist nicht möglich. In einer Nacht darf höchstens 0,05 bewegt werden. Im Betrieb nennt man das den Halbton.

Die Obergrenze gibt es nicht wegen einer Grenze der Technik. Verdünnt man eine Erinnerung zu schnell, geht die Spur der Umschreibung mit ihr. Solange die Spur bleibt, kann ein Mensch zu sich sagen: Das ist ein bearbeiteter Traum. Was die Obergrenze schützt, ist nicht der Traum des Schlafenden. Es ist der Spielraum, der danach bleibt, beim Erwachen, um am eigenen Gedächtnis zu zweifeln.

Zwölf verbundene Erzählungen aus einem Land, in dem diese Technik bis in den letzten Winkel des Alltags gelangt ist.

- Ein Mädchen von dreizehn, das darum bittet, ihren Albtraum in Ruhe zu lassen — „Halbton"
- Eine Frau, die vier Jahre und sieben Monate wartet und am Tag ihres Termins zurücktritt — „Die Warteliste für das Vergessen"
- Eine Witwe, der man die Entschuldigung überreicht, die ihr Mann nie herausbrachte, synthetisiert aus seinen Tagebüchern, und eine Tochter, die das eine Fälschung nennt — „Das Vermächtnis"
- Eine Mutter, der man jeden Monat eine klare, tröstliche Geschichte vorliest, übersetzt aus den Träumen eines Sohnes ohne Sprache — „Der Übersetzer"
- Ein Techniker, der die Reue eines Täters über fünfzehn Nächte von 0,07 auf 0,81 hebt — „Das Strafmaß"
- Ein Betrieb, in dem Trauerbearbeitung innerhalb von achtundvierzig Stunden Pflicht ist, und ein Mann, der sie nicht annimmt — „Trauer in Vertretung"

Es gibt keine Bösewichte. Es gibt nur Menschen, die ihre Arbeit nach Vorschrift richtig tun, und ein Feld, das die Vorschrift nie vorgesehen hat.

Jede Erzählung steht für sich. Je weiter man liest, desto deutlicher wird, was dieses Land Glück genannt hat.

INHALT
I. Halbton
II. Die Warteliste für das Vergessen
III. Das Vermächtnis
IV. Der Übersetzer
V. Der Traum in der zweiten Person
VI. Traumsteuer
VII. Trauer in Vertretung
VIII. Das Strafmaß
IX. Das Recht, nicht zu erwachen
X. Der Nachlass
XI. Glücksindex 98
XII. Der schweigende Proband

Etwa 22.500 Wörter.

---

## 3. Schlüsselwörter（7つ）

1. `literarische Science Fiction`
2. `Dystopie nahe Zukunft`
3. `Erzählungen Zyklus`
4. `Erinnerung Identität`
5. `leise Science Fiction Kurzgeschichten`
6. `Bürokratie Dystopie Roman`
7. `japanische Science Fiction auf Deutsch`

**入れてはいけないもの**：他の作家名や既存作品名。Amazonの規約で禁じられています。
日本語版・英語版と同じ注意です。

---

## 4. Kategorien（最大3つ）

1. Belletristik → Science-Fiction → Anthologien & Kurzgeschichten
2. Belletristik → Literarische Fiktion
3. Belletristik → Science-Fiction → Dystopie

日本語版・英語版と同じ配分です。一つ目を主戦場に置き、残りで文芸の読者にも
届くようにしています。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（ドイツ） |
| KDPセレクト | 登録する |

70%プランが使えるのは **2,99 €〜9,99 €** の範囲です。英語版の $3.99 と
揃えてあります。

**付加価値税に注意してください。** ドイツの電子書籍は軽減税率（7%）の対象です。
KDPでは税込価格と税抜価格の両方が表示されます。ロイヤリティは**税抜**価格に
対して計算されるので、3,99 € と入れたときの手取りは単純な七割ではありません。
登録画面に出る税抜額を確認してください。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Das Traumamt.epub` |
| 表紙 | `book/dist/cover_de1.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py de1
python3 book/tools/build_cover.py de1
```

表紙は四言語六冊すべて同じ乱数の種で帯を描いています。字だけが変わります。
（検証: 日本語版第一巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み）

ウムラウト（Zwölf Nächte）は DejaVu Serif で正しく出ています。

---

## 7. 翻訳について

**英語版からの重訳ではなく、日本語の原文から訳しています。** 重訳すると
英語で選んだ解釈がそのまま固定され、原文からのずれが二重になるためです。
英語版と訳が食い違う箇所があっても、どちらも原文に当たっているかぎり誤りでは
ありません。

原文51,718字 → 独文22,569 words（比0.436）。英語版の0.463より低いのは、
ドイツ語の複合語が英語の数語を一語にまとめるためで、訳し落としではありません。
落ちていないかどうかは `check_tr_structure.py`（節ごとの段落数の照合）が
見ています。

用語は `book/de/GLOSSARY.md` で固定しました。主な判断:

| 日本語 | Deutsch | 理由 |
|---|---|---|
| 夢編集局 | das Traumamt | 「Amt für Traumbearbeitung」は題として重い。短く、独語では即座に役所と読める |
| 半色 | der Halbton | 「Halbfarbe」は独語に無い。印刷の網点と音楽の半音の両方を持ち、固定した半歩（0,05）に合う |
| 校正官 | der Korrektor | 原文の編集／校正という出版の比喩をそのまま残す |
| 素片 | das Fragment | |
| 情動荷重 | die affektive Last | |
| 残差 | das Residuum | 独語の統計用語 |
| 照合機 | der Komparator | |
| 夢裁判 | Das Strafmaß | 「Traumprozess」はカフカを連想させ、ここでは誤導 |

組み方は、**小数点が読点**（0,05）、**引用符が „ … "**、新正書法（dass）、
ドイツ式の ß です。小数点は特に重要で、点のままだとドイツ語読者には
桁区切りに見えます。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `python3 book/tools/check_tr_structure.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_tr_terms.py` が0件で通ることを確認した
- [x] `python3 book/tools/check_overlap.py` が0件で通ることを確認した
- [x] 表紙の帯が日本語版第一巻と一致していることを画素比較で確認した
- [ ] Kindle Previewerで表示を三機種確認した（ウムラウトの表示を特に）
- [ ] Beschreibung を貼り付けた
- [ ] Schlüsselwörter 7つを入れた
- [ ] Kategorien を3つ選んだ
- [ ] 価格を設定し、**税抜価格**を確認した
- [ ] KDPセレクトの可否を決めた
