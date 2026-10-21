# ドイツ語版『Die Angleichung』KDP登録情報

第二巻のドイツ語版です。貼り付ける中身はドイツ語、説明は日本語で書いてあります。

---

## 1. 本の詳細

| 項目 | 内容 |
|---|---|
| Buchtitel | Die Angleichung |
| Untertitel | Das Traumamt, Band Zwei |
| Reihe | Das Traumamt（Band 2） |
| 巻番号 | 2 |
| Verfasser | Kazu A. Suzuki |
| 出版言語 | Deutsch |
| ISBN | 不要（KDPが内部管理番号を自動付与） |

シリーズ名はドイツ語版第一巻と**一字一句同じ**（`Das Traumamt`）にしてください。
違うとシリーズページが別々に作られます。

---

## 2. Beschreibung（そのまま貼り付け可）

Die Angleichung. So heißt ein staatliches Vorhaben, das das Gewicht der Erinnerungen von einer Million Menschen Nacht für Nacht zum Mittelwert hin bewegt.

Während Sie schlafen, macht das Gehirn eine Erinnerung weich, verbindet sie neu und lässt sie wieder setzen. Die Traumbearbeitung greift in diese wenigen Sekunden ein, um das Gewicht zu senken, und in einer Nacht darf höchstens 0,05 bewegt werden. Im Betrieb nennt man das den Halbton.

Wo Band I, Das Traumamt, von einem Techniker und einem Antragsteller handelte, die einander gegenübersaßen, spielen diese zwölf Erzählungen danach: nachdem die Technik erst eine Industrie, dann ein System und schließlich so groß wie ein Land geworden ist.

- Eine Gesellschaft, in der drei Stunden Schlaf genügen, und eine Firma, die in den übrigen vierzig Minuten die Gefühle anderer verkauft — „Die schlaflose Stadt"
- Ein pränataler Eingriff, der Geborgenheit, Vertrauen und Neugier in einem Fötus bildet. Worauf er wirkt, waren nicht die Kinder — „Fundamente"
- Die Trauer, die in einen Täter übertragen wird, ist den Hinterbliebenen im Augenblick der Entnahme bereits genommen — „Die Empathiespritze"
- Automatisierungsgrad 98,4 Prozent, und der letzte Techniker, der die übrigen 1,6 trägt — „Der letzte Handwerker"
- Ein Mann, dem über sieben Nächte ohne seine Einwilligung schwerer gemacht wurde und der sich weigert, zurückgesetzt zu werden — „Körperverletzung"
- Ein Brand mit neunzehn Toten, an den sich niemand erinnert und der nirgends geschrieben steht — „Das Register"

Es gibt keine Bösewichte. Es gibt nur Menschen, die in ihren Abteilungen ihre Arbeit richtig tun. Die Zuteilung ändert etwas wegen der Auslastung, die Störungsanalyse wegen der Behebungskosten, die Technikverwaltung aus Personalmangel. Es gibt keine Spur davon, dass sie miteinander gesprochen hätten.

Was geschah, als die drei Überlegungen in dasselbe Quartal fielen, wird in der letzten Erzählung deutlich, „Der Abschlussbericht".

Jede Erzählung steht für sich. Band I ist nicht erforderlich.

INHALT
I. Die schlaflose Stadt
II. Fundamente
III. Die Empathiespritze
IV. Der letzte Handwerker
V. Träumt die Maschine?
VI. Körperverletzung
VII. Das Register
VIII. Das Meer der Träume
IX. Der Traum von morgen
X. Der letzte Fehler
XI. Residuum
XII. Der Abschlussbericht

Etwa 21.000 Wörter.

---

## 3. Schlüsselwörter（7つ）

1. `literarische Science Fiction`
2. `Dystopie nahe Zukunft`
3. `Erzählungen Zyklus`
4. `Bürokratie Dystopie Roman`
5. `Erinnerung Identität Science Fiction`
6. `leise Science Fiction Kurzgeschichten`
7. `japanische Science Fiction auf Deutsch`

ドイツ語版第一巻とほぼ同じです。5番だけ第二巻の主題（個人ではなく制度の側）に
寄せてあります。

---

## 4. Kategorien（最大3つ）

1. Belletristik → Science-Fiction → Anthologien & Kurzgeschichten
2. Belletristik → Literarische Fiktion
3. Belletristik → Science-Fiction → Dystopie

第一巻と同じにしてあります。シリーズは同じ棚に並んだほうが見つけてもらえます。

---

## 5. 価格とロイヤリティ

| 項目 | 推奨 |
|---|---|
| ロイヤリティ | 70%プラン |
| 価格 | 3,99 €（ドイツ） |
| KDPセレクト | 登録する |

第一巻と同額にしてあります。シリーズで価格が揃っていないと、二冊目で止まる
読者が出ます。付加価値税の扱いは第一巻の登録情報に書いたとおりです。

---

## 6. アップロードするファイル

| 用途 | ファイル |
|---|---|
| 原稿 | `book/dist/Die Angleichung.epub` |
| 表紙 | `book/dist/cover_de2.jpg`（1600×2560px、1.6:1） |

```bash
python3 book/tools/build_epub.py de2
python3 book/tools/build_cover.py de2
```

（検証: 日本語版第二巻の表紙と、字のない下半分を画素比較して差分ゼロを確認済み）

---

## 7. 翻訳について

日本語の原文から訳しています（英語版からの重訳ではありません）。
原文48,719字 → 独文21,103 words（比0.433）。第一巻の0.436とほぼ同じです。

第八話『Das Meer der Träume』は、保管庫に残った記録として、第一巻の第二話・
第四話・第十二話と第二巻第六話の文をそのまま引用します。訳文が一字ずれると
巻をまたいだ繋がりが切れるので、`check_tr_quotes.py` が言語ごとに文字列一致を
機械で確かめています。

---

## 8. 出版前チェックリスト

- [x] 全十二話の翻訳を終えた
- [x] `check_tr_structure.py` が0件で通ることを確認した
- [x] `check_tr_terms.py` が0件で通ることを確認した
- [x] `check_tr_quotes.py` が0件で通ることを確認した
- [x] `check_overlap.py` が0件で通ることを確認した
- [x] 表紙の帯が日本語版第二巻と一致していることを画素比較で確認した
- [ ] Kindle Previewerで表示を三機種確認した（ウムラウトとßの表示を特に）
- [ ] Beschreibung を貼り付けた
- [ ] Schlüsselwörter 7つを入れた
- [ ] Kategorien を3つ選んだ
- [ ] シリーズ名を第一巻と一字一句同じにした
- [ ] 価格を設定し、税抜価格を確認した
- [ ] KDPセレクトの可否を決めた

---

## 9. 六冊の対応

| | 日本語 | English | Deutsch |
|---|---|---|---|
| 第一巻 | 夢編集局 | The Dream Editing Bureau | Das Traumamt |
| 第二巻 | 均し | The Levelling | Die Angleichung |

星新一賞応募作『境界線、未編集』は、この六冊のどれにも入っていません。
`novel/` にあり、未発表のままです。
