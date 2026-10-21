# KDPメタデータ一覧（14冊）

**この表は手で書かない。** 各巻の `KDP登録情報.md` が正本で、
`python3 book/tools/kdp_metadata.py` が読み直して書き出す。
価格やキーワードを直すときは各巻のファイルを直して、この道具を走らせる。

登録画面をうめる順に並べてある。各言語とも**第一巻を先に登録**して、
シリーズ名を確定させてから第二巻を出す。

---

## 1. 一覧

| # | 記号 | 題 | 副題 | シリーズ | 巻 | 言語 | 価格 |
|---|---|---|---|---|---|---|---|
| 1 | `vol1` | 夢編集局 | 十二の夜 | 夢編集局（第1巻） | 1 | 日本語 | 500円 |
| 2 | `vol2` | 均し | 夢編集局 第二集 | 夢編集局（第2巻） | 2 | 日本語 | 500円 |
| 3 | `en1` | The Dream Editing Bureau | Twelve Nights | The Dream Editing Bureau（Book 1） | 1 | English | $3.99（米国） |
| 4 | `en2` | The Levelling | The Dream Editing Bureau, Book Two | The Dream Editing Bureau（Book 2） | 2 | English | $3.99（米国） |
| 5 | `de1` | Das Traumamt | Zwölf Nächte | Das Traumamt（Band 1） | 1 | Deutsch | 3,99 €（ドイツ） |
| 6 | `de2` | Die Angleichung | Das Traumamt, Band Zwei | Das Traumamt（Band 2） | 2 | Deutsch | 3,99 €（ドイツ） |
| 7 | `es1` | La Oficina de Sueños | Doce noches | La Oficina de Sueños（Libro 1） | 1 | Español | 3,99 €（スペイン） |
| 8 | `es2` | La Nivelación | La Oficina de Sueños, Libro Dos | La Oficina de Sueños（Libro 2） | 2 | Español | 3,99 €（スペイン） |
| 9 | `fr1` | Le Bureau des Rêves | Douze nuits | Le Bureau des Rêves（Livre 1） | 1 | Français | 3,99 €（フランス） |
| 10 | `fr2` | Le Nivellement | Le Bureau des Rêves, Livre Deux | Le Bureau des Rêves（Livre 2） | 2 | Français | 3,99 €（フランス） |
| 11 | `it1` | L'Ufficio dei Sogni | Dodici notti | L'Ufficio dei Sogni（Libro 1） | 1 | Italiano | 3,99 €（イタリア） |
| 12 | `it2` | Il Livellamento | L'Ufficio dei Sogni, Libro Due | L'Ufficio dei Sogni（Libro 2） | 2 | Italiano | 3,99 €（イタリア） |
| 13 | `nl1` | Het Droombureau | Twaalf nachten | Het Droombureau（Deel 1） | 1 | Nederlands | 3,99 €（オランダ） |
| 14 | `nl2` | De Nivellering | Het Droombureau, Deel Twee | Het Droombureau（Deel 2） | 2 | Nederlands | 3,99 €（オランダ） |

## 2. 分量と原稿

| 記号 | 話数 | 原文 | 訳文 | 比 | 原稿 | 表紙 |
|---|---|---|---|---|---|---|
| `vol1` | 12 | 51,718字 | — | — | `夢編集局.epub` | `cover_vol1.jpg` |
| `vol2` | 12 | 48,719字 | — | — | `均し.epub` | `cover_vol2.jpg` |
| `en1` | 12 | 51,718字 | 23,924 words | 0.463 | `The Dream Editing Bureau.epub` | `cover_en1.jpg` |
| `en2` | 12 | 48,719字 | 22,452 words | 0.461 | `The Levelling.epub` | `cover_en2.jpg` |
| `de1` | 12 | 51,718字 | 22,569 words | 0.436 | `Das Traumamt.epub` | `cover_de1.jpg` |
| `de2` | 12 | 48,719字 | 21,103 words | 0.433 | `Die Angleichung.epub` | `cover_de2.jpg` |
| `es1` | 12 | 51,718字 | 23,429 words | 0.453 | `La Oficina de Sueños.epub` | `cover_es1.jpg` |
| `es2` | 12 | 48,719字 | 22,734 words | 0.467 | `La Nivelación.epub` | `cover_es2.jpg` |
| `fr1` | 12 | 51,718字 | 25,600 words | 0.495 | `Le Bureau des Rêves.epub` | `cover_fr1.jpg` |
| `fr2` | 12 | 48,719字 | 24,709 words | 0.507 | `Le Nivellement.epub` | `cover_fr2.jpg` |
| `it1` | 12 | 51,718字 | 22,670 words | 0.438 | `L'Ufficio dei Sogni.epub` | `cover_it1.jpg` |
| `it2` | 12 | 48,719字 | 21,853 words | 0.449 | `Il Livellamento.epub` | `cover_it2.jpg` |
| `nl1` | 12 | 51,718字 | 25,487 words | 0.493 | `Het Droombureau.epub` | `cover_nl1.jpg` |
| `nl2` | 12 | 48,719字 | 24,065 words | 0.494 | `De Nivellering.epub` | `cover_nl2.jpg` |

原文の字数は日本語版の原稿から数えた値で、同じ巻の七言語で同じになる。
訳文の語数は空白区切りの語数。比は words/字。

## 3. 市場と税率

| 言語 | 主な市場 | 電子書籍の付加価値税 |
|---|---|---|
| ja | amazon.co.jp | 10%（軽減税率の対象外） |
| en | amazon.com / .co.uk / .ca / .au | 米国なし・英国0%・加5%ほか |
| de | amazon.de / .at | 7% |
| es | amazon.es | 4% |
| fr | amazon.fr / .ca / .be | 5,5% |
| it | amazon.it | 4% |
| nl | amazon.nl / .com.be | 9%（白6%） |

ロイヤリティは**税抜額**に対してかかる。同じ 3,99 € でも、
西・伊（4%）と蘭（9%）では手取りが違う。登録画面で自動換算させたあと、
税抜額のほうを確認する。

**KDPセレクト。** 90日間の独占は**言語版ごと**に数える。
一つの言語版をセレクトに入れても、他の言語版の扱いには影響しない。

---

## 4. 貼り付ける中身

内容紹介もそのまま入れてある。この節だけで登録画面はうまる。
貼る前に、内容紹介に応募作の文が紛れていないかを `check_overlap.py` が
見ている（七言語・各巻の第2節を対象にしている）。

### 1. `vol1` — 夢編集局

- **題** 夢編集局
- **副題** 十二の夜
- **シリーズ** 夢編集局（第1巻）
- **言語** 日本語　**価格** 500円　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

夢は、消せない。軽くできるだけだ。

眠っているあいだ、人の脳は記憶をいったん柔らかくして、繋ぎ直し、また固める。その数秒に立ち会って、繋ぎ直しの手つきを少しだけ変える。それが夢編集という仕事である。

できるのは、記憶の重さを下げることだけ。一晩に動かせる上限は〇・〇五。現場ではこれを「半色」と呼ぶ。

上限がある理由は、技術の限界ではない。一気に薄くすると、書き換えられた痕跡ごと消えてしまうからだ。痕跡が残っているかぎり、人は「これは編集された夢だ」と自分に言える。上限が守っているのは、眠っている人の夢ではなく、目が覚めたあとで自分の記憶を疑ってみることのできる余地のほうだった。

本書は、その技術が社会の隅々にまで行き渡った国を舞台にした、十二話の連作短編集です。

・悪夢を消さないでほしいと言う、十三歳の少女――「半色」
・四年七か月待たされた末に、順番が来たところで処置を辞退した女性――「忘却の順番待ち」
・亡き夫の「言えなかった謝罪」を合成して届けられた妻と、それを偽物だと言う娘――「夢の遺言」
・言葉を持たない我が子の夢を、毎月わかりやすい物語に翻訳して聞かされる母――「夢の翻訳者」
・加害者の悔恨を、十五晩かけて〇・〇七から〇・八一まで引き上げる技師――「夢裁判」
・悲嘆処理が四十八時間以内に義務づけられた職場で、一人だけ処置を拒む男――「涙の代筆」

どの話にも、悪人は出てきません。出てくるのは、規定に従って正しく仕事をする人たちと、その規定に用意されていなかった一つの欄だけです。

一話ずつ独立して読めますが、読み進めるほど、この国が何を「幸福」と呼んできたのかが見えてきます。

【収録作】
一　半色
二　忘却の順番待ち
三　夢の遺言
四　夢の翻訳者
五　二人称の夢
六　夢税
七　涙の代筆
八　夢裁判
九　目覚めない権利
十　夢の相続
十一　幸福指数九八
十二　沈黙の被験者

約五万二千字／縦書き

---

</details>

キーワード（7つ、この順）

1. `SF 短編集`
2. `近未来 ディストピア`
3. `AI 人工知能 小説`
4. `連作短編集`
5. `記憶 夢 SF`
6. `社会派 SF 日本`
7. `静かな余韻 考えさせられる小説`

カテゴリー（最大3つ、この順）

1. 文学・評論 → SF・ホラー・ファンタジー → SF
2. 文学・評論 → 文学 → 日本文学
3. 文学・評論 → 小説・文芸

### 2. `vol2` — 均し

- **題** 均し
- **副題** 夢編集局 第二集
- **シリーズ** 夢編集局（第2巻）
- **言語** 日本語　**価格** 500円　**ロイヤリティ** 70%プラン　**KDPセレクト** 第一巻と揃える

<details><summary>内容紹介（そのまま貼り付け可）</summary>

均し（ならし）。百万人の記憶の重さを、夜ごとに平均へ寄せる国家事業の名である。

眠っているあいだ、人の脳は記憶をいったん柔らかくして、繋ぎ直し、また固める。その数秒に介入して重さを下げるのが夢編集で、一晩に動かせる上限は〇・〇五。現場ではこれを「半色」と呼ぶ。

第一巻『夢編集局』が、技師と客が一対一で向き合う現場の話だったのに対し、本書はその技術が産業になり、制度になり、国の規模に達したあとの十二話です。

・睡眠が三時間で足りる身体になった社会で、空いた四十分に他人の情動を売る会社――「眠らない都市」
・胎児に安心・信頼・好奇の三つを形成する出生前施術。効いているのは子どもにではなかった――「胎夢」
・加害者に移入する被害者遺族の悲しみは、採取した時点で遺族の側から減っている――「共感注射」
・自動処理率九八・四パーセント。残り一・六パーセントを担う最後の技師――「最後の夢職人」
・七晩かけて無断で重くされた男が、元に戻る処置を拒む――「夢の犯罪」
・十九人が死んだ火災を、誰も覚えておらず、どこにも書かれていない――「消えた現実」

どの話にも悪人は出てきません。出てくるのは、それぞれの部署で正しく仕事をする人たちです。配分課は稼働率のために、解析課は代償の大きさのために、技術管理部は人手不足のために、それぞれ別の理由で別の改定をします。連絡を取り合った形跡はありません。

三本の筋が同じ四半期に揃ったとき、何が起きたのかは最終話「完了報告」で明らかになります。

各話は独立して読めます。第一巻を読んでいなくても差し支えありません。

【収録作】
一　眠らない都市
二　胎夢
三　共感注射
四　最後の夢職人
五　ＡＩは夢を見るか
六　夢の犯罪
七　消えた現実
八　夢の海
九　明日の夢
十　最後のバグ
十一　残差
十二　完了報告

約四万九千字／縦書き

---

</details>

キーワード（7つ、この順）

1. `SF 短編集`
2. `近未来 ディストピア`
3. `AI 官僚制 SF`
4. `連作短編集 第2巻`
5. `記憶 統計 監視社会`
6. `社会派 SF 日本`
7. `静かな余韻 考えさせられる小説`

カテゴリー（最大3つ、この順）

1. 文学・評論 → SF・ホラー・ファンタジー → SF
2. 文学・評論 → 文学 → 日本文学
3. 文学・評論 → 小説・文芸

### 3. `en1` — The Dream Editing Bureau

- **題** The Dream Editing Bureau
- **副題** Twelve Nights
- **シリーズ** The Dream Editing Bureau（Book 1）
- **言語** English　**価格** $3.99（米国）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Dreams cannot be erased. They can only be made lighter.

While you sleep, the brain softens a memory, re-joins it, and sets it again. Dream editing is the work of attending those few seconds and altering the hand that does the re-joining, very slightly.

All it can do is lower the weight of a memory. The most that may be moved in one night is 0.05. In the field they call it the half-shade.

The ceiling is not there because of a limit in the technique. Thin a memory too fast and the trace of the rewriting goes with it. While the trace remains, a person can still tell themselves: this is an edited dream. What the ceiling protects is not the dream of the sleeping person. It is the room left afterwards, on waking, to doubt one's own memory.

Twelve linked stories, set in a country where that technique has reached into every corner of ordinary life.

- A girl of thirteen who asks for her nightmare to be left alone — "Half-Shade"
- A woman who waits four years and seven months, and declines the procedure on the day her turn comes — "The Waiting List for Forgetting"
- A widow given the apology her husband never managed to say, synthesised from his diaries, and a daughter who calls it a forgery — "The Bequest"
- A mother who is read a clear, comforting story each month, translated from the dreams of a son who has no language — "The Translator"
- A technician who raises an offender's remorse from 0.07 to 0.81 over fifteen nights — "The Sentence"
- A workplace where grief processing is compulsory within forty-eight hours, and one man who will not take it — "Grief by Proxy"

There are no villains. There are only people doing their work correctly, according to the rules, and one field the rules never provided.

Each story stands alone. Read on, and what this country has been calling happiness comes gradually into view.

CONTENTS
I. Half-Shade
II. The Waiting List for Forgetting
III. The Bequest
IV. The Translator
V. The Second-Person Dream
VI. Dream Tax
VII. Grief by Proxy
VIII. The Sentence
IX. The Right Not to Wake
X. Inheritance
XI. Happiness Index 98
XII. The Silent Subject

Approximately 24,000 words.

---

</details>

キーワード（7つ、この順）

1. `literary science fiction`
2. `near future dystopia`
3. `linked short stories`
4. `memory and identity`
5. `quiet speculative fiction short story collection`
6. `bureaucracy dystopian fiction`
7. `japanese science fiction in english`

カテゴリー（最大3つ、この順）

1. Fiction → Science Fiction → Short Stories
2. Fiction → Literary
3. Fiction → Science Fiction → Dystopian

### 4. `en2` — The Levelling

- **題** The Levelling
- **副題** The Dream Editing Bureau, Book Two
- **シリーズ** The Dream Editing Bureau（Book 2）
- **言語** English　**価格** $3.99（米国）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

The Levelling. The name of a state programme that brings the weight of a million people's memories towards the mean, night by night.

While you sleep, the brain softens a memory, re-joins it, and sets it again. Dream editing intervenes in those few seconds to lower the weight, and the most that may be moved in one night is 0.05. In the field they call it the half-shade.

Where Volume I, The Dream Editing Bureau, was about a technician and a client facing each other one to one, these twelve stories come after the technique has become an industry, then a scheme, and then the size of a country.

- A society where three hours of sleep is enough, and a company that sells other people's feelings in the forty minutes left over — "The Sleepless City"
- A prenatal procedure forming security, trust and curiosity in a foetus. What it works on was not the children — "Foundations"
- The grief transferred into an offender has already been taken off the bereaved at the moment it was harvested — "The Empathy Injection"
- Automation rate 98.4 per cent, and the last technician carrying the remaining 1.6 — "The Last Craftsman"
- A man made heavier over seven nights without his consent, who refuses to be put back — "Bodily Harm"
- A fire in which nineteen people died, which nobody remembers and which is written down nowhere — "The Register"

There are no villains. There are only people doing their work correctly in their own departments. Allocation revises for utilisation, Fault Analysis for the cost of correcting, Technical Management for want of staff. There is no trace of their having been in touch.

What happened when the three reasonings fell into the same quarter becomes clear in the final story, "The Completion Report".

Each story stands alone. Volume I is not required.

CONTENTS
I. The Sleepless City
II. Foundations
III. The Empathy Injection
IV. The Last Craftsman
V. Does the Machine Dream?
VI. Bodily Harm
VII. The Register
VIII. The Sea of Dreams
IX. Tomorrow's Dream
X. The Last Bug
XI. Residual
XII. The Completion Report

Approximately 22,500 words.

---

</details>

キーワード（7つ、この順）

1. `literary science fiction`
2. `near future dystopia`
3. `linked short stories`
4. `bureaucracy dystopian fiction`
5. `memory and identity speculative fiction`
6. `quiet science fiction short story collection`
7. `japanese science fiction in english`

カテゴリー（最大3つ、この順）

1. Fiction → Science Fiction → Short Stories
2. Fiction → Literary
3. Fiction → Science Fiction → Dystopian

### 5. `de1` — Das Traumamt

- **題** Das Traumamt
- **副題** Zwölf Nächte
- **シリーズ** Das Traumamt（Band 1）
- **言語** Deutsch　**価格** 3,99 €（ドイツ）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

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

</details>

キーワード（7つ、この順）

1. `literarische Science Fiction`
2. `Dystopie nahe Zukunft`
3. `Erzählungen Zyklus`
4. `Erinnerung Identität`
5. `leise Science Fiction Kurzgeschichten`
6. `Bürokratie Dystopie Roman`
7. `japanische Science Fiction auf Deutsch`

カテゴリー（最大3つ、この順）

1. Belletristik → Science-Fiction → Anthologien & Kurzgeschichten
2. Belletristik → Literarische Fiktion
3. Belletristik → Science-Fiction → Dystopie

### 6. `de2` — Die Angleichung

- **題** Die Angleichung
- **副題** Das Traumamt, Band Zwei
- **シリーズ** Das Traumamt（Band 2）
- **言語** Deutsch　**価格** 3,99 €（ドイツ）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

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

</details>

キーワード（7つ、この順）

1. `literarische Science Fiction`
2. `Dystopie nahe Zukunft`
3. `Erzählungen Zyklus`
4. `Bürokratie Dystopie Roman`
5. `Erinnerung Identität Science Fiction`
6. `leise Science Fiction Kurzgeschichten`
7. `japanische Science Fiction auf Deutsch`

カテゴリー（最大3つ、この順）

1. Belletristik → Science-Fiction → Anthologien & Kurzgeschichten
2. Belletristik → Literarische Fiktion
3. Belletristik → Science-Fiction → Dystopie

### 7. `es1` — La Oficina de Sueños

- **題** La Oficina de Sueños
- **副題** Doce noches
- **シリーズ** La Oficina de Sueños（Libro 1）
- **言語** Español　**価格** 3,99 €（スペイン）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Los sueños no pueden borrarse. Solo pueden aligerarse.

Mientras usted duerme, el cerebro ablanda un recuerdo, vuelve a unirlo y lo deja asentarse de nuevo. La edición de sueños es el oficio de asistir a esos pocos segundos y alterar, muy poco, la mano que vuelve a unir.

No puede hacerse más que bajar el peso de un recuerdo. En una noche solo pueden moverse 0,05 como máximo. En el oficio lo llaman la media tinta.

El límite no existe por una limitación de la técnica. Si se adelgaza un recuerdo demasiado deprisa, el rastro de la reescritura se va con él. Mientras el rastro permanece, una persona puede decirse: esto es un sueño editado. Lo que el límite protege no es el sueño de quien duerme. Es el margen que queda después, al despertar, para dudar de la propia memoria.

Doce relatos enlazados, situados en un país donde esa técnica ha llegado hasta el último rincón de la vida corriente.

- Una muchacha de trece años que pide que dejen en paz su pesadilla — «Media tinta»
- Una mujer que espera cuatro años y siete meses y se retira el día que le toca — «La lista de espera del olvido»
- Una viuda a quien entregan la disculpa que su marido nunca consiguió decir, sintetizada a partir de sus diarios, y una hija que la llama falsificación — «El legado»
- Una madre a la que cada mes le leen una historia clara y consoladora, traducida de los sueños de un hijo sin lenguaje — «El traductor»
- Un técnico que eleva el remordimiento de un agresor de 0,07 a 0,81 a lo largo de quince noches — «La condena»
- Un centro de trabajo donde la tramitación del duelo es obligatoria en cuarenta y ocho horas, y un hombre que no la acepta — «Duelo por delegación»

No hay villanos. Solo hay personas que hacen su trabajo correctamente, conforme a la norma, y un campo que la norma nunca previó.

Cada relato se sostiene solo. Cuanto más se avanza, más claro queda qué ha venido llamando felicidad este país.

ÍNDICE
I. Media tinta
II. La lista de espera del olvido
III. El legado
IV. El traductor
V. El sueño en segunda persona
VI. Impuesto sobre el sueño
VII. Duelo por delegación
VIII. La condena
IX. El derecho a no despertar
X. La herencia
XI. Índice de Felicidad 98
XII. El sujeto silencioso

Unas 23.000 palabras.

---

</details>

キーワード（7つ、この順）

1. `ciencia ficción literaria`
2. `distopía futuro cercano`
3. `relatos enlazados`
4. `memoria e identidad`
5. `ciencia ficción contemplativa cuentos`
6. `distopía burocrática novela`
7. `ciencia ficción japonesa en español`

カテゴリー（最大3つ、この順）

1. Ficción → Ciencia ficción → Antologías y relatos
2. Ficción → Literatura y ficción general
3. Ficción → Ciencia ficción → Distopías

### 8. `es2` — La Nivelación

- **題** La Nivelación
- **副題** La Oficina de Sueños, Libro Dos
- **シリーズ** La Oficina de Sueños（Libro 2）
- **言語** Español　**価格** 3,99 €（スペイン）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

La Nivelación. Así se llama un proyecto estatal que acerca a la media, noche tras noche, el peso de los recuerdos de un millón de personas.

Mientras usted duerme, el cerebro ablanda un recuerdo, vuelve a unirlo y lo deja asentarse de nuevo. La edición de sueños interviene en esos pocos segundos para bajar el peso, y en una noche solo pueden moverse 0,05 como máximo. En el oficio lo llaman la media tinta.

Si el Libro I, La Oficina de Sueños, trataba de un técnico y un solicitante sentados frente a frente, estos doce relatos ocurren después: cuando la técnica se ha hecho primero una industria, después un sistema y por fin algo del tamaño de un país.

- Una sociedad en que bastan tres horas de sueño, y una empresa que en los cuarenta minutos restantes vende los sentimientos de otros — «La ciudad que no duerme»
- Una intervención prenatal que forma amparo, confianza y curiosidad en un feto. Aquello sobre lo que actuaba no eran los niños — «Cimientos»
- La pena que se transfiere a un agresor ya les ha sido quitada a los deudos en el instante de la extracción — «La inyección de empatía»
- Grado de automatización, 98,4 por ciento, y el último artesano que carga con el 1,6 restante — «El último artesano»
- Un hombre a quien durante siete noches se le hizo más pesado sin su consentimiento y que se niega a que lo devuelvan — «Lesiones»
- Un incendio con diecinueve muertos que nadie recuerda y que no está escrito en ninguna parte — «El registro»

No hay villanos. Solo hay personas que, en sus departamentos, hacen su trabajo correctamente. Distribución cambia algo por la tasa de utilización; Análisis de Incidencias, por el coste de corregir; Gestión Técnica, por falta de plantilla. No hay indicio alguno de que hablaran entre sí.

Qué ocurrió cuando los tres razonamientos cayeron en el mismo trimestre se aclara en el último relato, «El informe de cierre».

Cada relato se sostiene solo. No hace falta el Libro I.

ÍNDICE
I. La ciudad que no duerme
II. Cimientos
III. La inyección de empatía
IV. El último artesano
V. ¿Sueña la máquina?
VI. Lesiones
VII. El registro
VIII. El mar de los sueños
IX. El sueño de mañana
X. El último fallo
XI. Residuo
XII. El informe de cierre

Unas 22.700 palabras.

---

</details>

キーワード（7つ、この順）

1. `ciencia ficción literaria`
2. `distopía futuro cercano`
3. `relatos enlazados`
4. `distopía burocrática novela`
5. `memoria e identidad`
6. `ciencia ficción contemplativa cuentos`
7. `ciencia ficción japonesa en español`

カテゴリー（最大3つ、この順）

1. Ficción → Ciencia ficción → Antologías y relatos
2. Ficción → Ciencia ficción → Distopías
3. Ficción → Literatura y ficción general

### 9. `fr1` — Le Bureau des Rêves

- **題** Le Bureau des Rêves
- **副題** Douze nuits
- **シリーズ** Le Bureau des Rêves（Livre 1）
- **言語** Français　**価格** 3,99 €（フランス）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Les rêves ne s'effacent pas. Ils ne peuvent qu'être allégés.

Pendant que vous dormez, le cerveau ramollit un souvenir, le relie à nouveau et le laisse se fixer de nouveau. L'édition des rêves est le métier qui assiste à ces quelques secondes et modifie, très peu, la main qui relie.

On ne peut rien faire d'autre que baisser le poids d'un souvenir. En une nuit, 0,05 au maximum. Dans le métier, on appelle cela la demi-teinte.

La limite n'existe pas par insuffisance de la technique. Si l'on amincit un souvenir trop vite, la trace de la réécriture s'en va avec lui. Tant que la trace demeure, on peut se dire : ceci est un rêve édité. Ce que la limite protège, ce n'est pas le rêve de qui dort. C'est la marge qui reste ensuite, au réveil, pour douter de sa propre mémoire.

Douze nouvelles liées, dans un pays où cette technique est entrée jusqu'au dernier recoin de la vie ordinaire.

- Une jeune fille de treize ans qui demande qu'on laisse son cauchemar tranquille — « Demi-teinte »
- Une femme qui attend quatre ans et sept mois et renonce le jour de son tour — « La file d'attente de l'oubli »
- Une veuve à qui l'on remet les excuses que son mari n'a jamais su dire, synthétisées d'après ses journaux, et une fille qui appelle cela une contrefaçon — « Le testament »
- Une mère à qui l'on lit chaque mois une histoire claire et consolante, traduite des rêves d'un fils sans langage — « Le traducteur »
- Un technicien qui élève le remords d'un meurtrier de 0,07 à 0,81 au long de quinze nuits — « La peine »
- Un lieu de travail où la tramitation du deuil est obligatoire en quarante-huit heures, et un homme qui ne l'accepte pas — « Le deuil par procuration »

Il n'y a pas de méchants. Il n'y a que des gens qui font leur travail correctement, conformément à la norme, et un champ que la norme n'a jamais prévu.

Chaque nouvelle se tient seule. Plus on avance, plus il devient clair ce que ce pays appelle depuis toujours le bonheur.

SOMMAIRE
I. Demi-teinte
II. La file d'attente de l'oubli
III. Le testament
IV. Le traducteur
V. Le rêve à la deuxième personne
VI. L'impôt sur les rêves
VII. Le deuil par procuration
VIII. La peine
IX. Le droit de ne pas se réveiller
X. La succession
XI. Indice de Bonheur 98
XII. Le sujet silencieux

Environ 25 600 mots.

---

</details>

キーワード（7つ、この順）

1. `science-fiction littéraire`
2. `dystopie futur proche`
3. `nouvelles liées`
4. `mémoire et identité`
5. `science-fiction contemplative nouvelles`
6. `dystopie bureaucratique roman`
7. `science-fiction japonaise en français`

カテゴリー（最大3つ、この順）

1. Romans et littérature → Science-fiction → Anthologies et nouvelles
2. Romans et littérature → Littérature générale
3. Romans et littérature → Science-fiction → Dystopies

### 10. `fr2` — Le Nivellement

- **題** Le Nivellement
- **副題** Le Bureau des Rêves, Livre Deux
- **シリーズ** Le Bureau des Rêves（Livre 2）
- **言語** Français　**価格** 3,99 €（フランス）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Le Nivellement. C'est le nom d'un projet d'État qui rapproche de la moyenne, nuit après nuit, le poids des souvenirs d'un million de personnes.

Pendant que vous dormez, le cerveau ramollit un souvenir, le relie à nouveau et le laisse se fixer de nouveau. L'édition des rêves intervient dans ces quelques secondes pour baisser le poids, et en une nuit 0,05 au maximum peuvent être déplacés. Dans le métier, on appelle cela la demi-teinte.

Si le Livre I, Le Bureau des Rêves, traitait d'un technicien et d'un demandeur assis face à face, ces douze nouvelles se passent après : quand la technique est devenue d'abord une industrie, puis un système, et enfin quelque chose de la taille d'un pays.

- Une société où trois heures de sommeil suffisent, et une entreprise qui vend, dans les quarante minutes restantes, les sentiments des autres — « La ville qui ne dort pas »
- Une intervention prénatale qui forme sécurité, confiance et curiosité chez un fœtus. Ce sur quoi elle agissait, ce n'était pas les enfants — « Fondations »
- Le chagrin transféré à un auteur a déjà été retiré aux proches à l'instant du prélèvement — « L'injection d'empathie »
- Taux d'automatisation, 98,4 pour cent, et le dernier artisan qui porte les 1,6 restants — « Le dernier artisan »
- Un homme à qui l'on a rendu les choses plus lourdes pendant sept nuits sans son consentement, et qui refuse qu'on les lui remette — « Violences »
- Un incendie avec dix-neuf morts dont personne ne se souvient et qui n'est écrit nulle part — « Le registre »

Il n'y a pas de méchants. Il n'y a que des gens qui, dans leurs services, font leur travail correctement. La Répartition change quelque chose pour le taux d'utilisation ; l'Analyse des anomalies, pour le coût de la correction ; la Gestion technique, par manque d'effectifs. Il n'y a aucun indice qu'ils se soient parlé.

Ce qui s'est produit quand les trois raisonnements sont tombés dans le même trimestre s'éclaire dans la dernière nouvelle, « Le rapport de clôture ».

Chaque nouvelle se tient seule. Le Livre I n'est pas nécessaire.

SOMMAIRE
I. La ville qui ne dort pas
II. Fondations
III. L'injection d'empathie
IV. Le dernier artisan
V. La machine rêve-t-elle ?
VI. Violences
VII. Le registre
VIII. La mer des rêves
IX. Le rêve de demain
X. Le dernier bug
XI. Résidu
XII. Le rapport de clôture

Environ 24 700 mots.

---

</details>

キーワード（7つ、この順）

1. `science-fiction littéraire`
2. `dystopie futur proche`
3. `nouvelles liées`
4. `dystopie bureaucratique roman`
5. `mémoire et identité`
6. `science-fiction contemplative nouvelles`
7. `science-fiction japonaise en français`

カテゴリー（最大3つ、この順）

1. Romans et littérature → Science-fiction → Anthologies et nouvelles
2. Romans et littérature → Science-fiction → Dystopies
3. Romans et littérature → Littérature générale

### 11. `it1` — L'Ufficio dei Sogni

- **題** L'Ufficio dei Sogni
- **副題** Dodici notti
- **シリーズ** L'Ufficio dei Sogni（Libro 1）
- **言語** Italiano　**価格** 3,99 €（イタリア）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

I sogni non si cancellano. Si possono soltanto alleggerire.

Mentre dormite, il cervello ammorbidisce un ricordo, lo rilega e lo lascia fissarsi di nuovo. L'edizione dei sogni è il mestiere che assiste a quei pochi secondi e modifica, di molto poco, la mano che rilega.

Non si può fare altro che abbassare il peso di un ricordo. In una notte, 0,05 al massimo. Nel mestiere lo chiamano la mezzatinta.

Il limite non esiste per insufficienza della tecnica. Se si assottiglia un ricordo troppo in fretta, la traccia della riscrittura se ne va con lui. Finché la traccia resta, si può dire a sé stessi: questo è un sogno montato. Ciò che il limite protegge non è il sogno di chi dorme. È il margine che resta dopo, al risveglio, per dubitare della propria memoria.

Dodici racconti collegati, in un paese dove quella tecnica è entrata fino all'ultimo angolo della vita ordinaria.

- Una ragazza di tredici anni che chiede di lasciare in pace il proprio incubo — «Mezzatinta»
- Una donna che attende quattro anni e sette mesi e rinuncia il giorno del suo turno — «La lista d'attesa dell'oblio»
- Una vedova a cui consegnano le scuse che il marito non ha mai saputo dire, sintetizzate dai suoi diari, e una figlia che chiama quella cosa una contraffazione — «Il testamento»
- Una madre a cui leggono ogni mese una storia chiara e consolante, tradotta dai sogni di un figlio senza linguaggio — «Il traduttore»
- Un tecnico che eleva il rimorso di un omicida da 0,07 a 0,81 nel corso di quindici notti — «La pena»
- Un luogo di lavoro dove il trattamento del dolore è obbligatorio entro quarantotto ore, e un uomo che non lo accetta — «Il lutto per delega»

Non ci sono cattivi. Ci sono soltanto persone che fanno il loro lavoro correttamente, conformemente alla norma, e un campo che la norma non ha mai previsto.

Ogni racconto sta da sé. Più si avanza, più diventa chiaro che cosa questo paese chiami da sempre felicità.

INDICE
I. Mezzatinta
II. La lista d'attesa dell'oblio
III. Il testamento
IV. Il traduttore
V. Il sogno in seconda persona
VI. L'imposta sui sogni
VII. Il lutto per delega
VIII. La pena
IX. Il diritto di non svegliarsi
X. La successione
XI. Indice di Felicità 98
XII. Il soggetto silenzioso

Circa 22.700 parole.

---

</details>

キーワード（7つ、この順）

1. `fantascienza letteraria`
2. `distopia futuro prossimo`
3. `racconti collegati`
4. `memoria e identità`
5. `fantascienza contemplativa racconti`
6. `distopia burocratica romanzo`
7. `fantascienza giapponese in italiano`

カテゴリー（最大3つ、この順）

1. Narrativa → Fantascienza → Antologie e racconti
2. Narrativa → Narrativa letteraria
3. Narrativa → Fantascienza → Distopie

### 12. `it2` — Il Livellamento

- **題** Il Livellamento
- **副題** L'Ufficio dei Sogni, Libro Due
- **シリーズ** L'Ufficio dei Sogni（Libro 2）
- **言語** Italiano　**価格** 3,99 €（イタリア）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Il Livellamento. È il nome di un piano statale che avvicina alla media, notte dopo notte, il peso dei ricordi di un milione di persone.

Mentre dormite, il cervello ammorbidisce un ricordo, lo rilega e lo lascia fissarsi di nuovo. L'edizione dei sogni interviene in quei pochi secondi e abbassa il peso: in una notte si possono spostare 0,05 al massimo. Nel mestiere lo chiamano la mezzatinta.

Se il Libro I, L'Ufficio dei Sogni, trattava di un tecnico e di un richiedente seduti uno di fronte all'altro, questi dodici racconti vengono dopo: quando la tecnica è diventata prima un'industria, poi un sistema, e infine una cosa della taglia di un paese.

- Una società in cui bastano tre ore di sonno, e un'azienda che nei quaranta minuti rimasti vende i sentimenti degli altri — «La città che non dorme»
- Un intervento prenatale che forma sicurezza, fiducia e curiosità in un feto. Ciò su cui agiva non erano i bambini — «Fondazioni»
- Il dolore trasferito a uno scrittore è già stato tolto ai familiari nell'istante del prelievo — «L'iniezione di empatia»
- Tasso di automazione 98,4 per cento, e l'ultimo artigiano che porta l'1,6 restante — «L'ultimo artigiano»
- Un uomo a cui per sette notti hanno reso le cose più pesanti senza il suo consenso, e che rifiuta che gliele si rimettano a posto — «Lesioni»
- Un incendio con diciannove morti di cui nessuno si ricorda e che non è scritto in nessun luogo — «Il registro»

Non ci sono cattivi. Ci sono soltanto persone che, nei loro servizi, fanno il loro lavoro correttamente. La Ripartizione cambia qualcosa per il tasso di utilizzo; l'Analisi anomalie, per l'entità del costo della correzione; la Gestione tecnica, per mancanza di personale. Non c'è traccia che si siano parlati.

Che cosa si sia prodotto quando i tre ragionamenti sono caduti nello stesso trimestre si chiarisce nell'ultimo racconto, «La relazione di chiusura».

Ogni racconto sta da sé. Il Libro I non è necessario.

INDICE
I. La città che non dorme
II. Fondazioni
III. L'iniezione di empatia
IV. L'ultimo artigiano
V. La macchina sogna?
VI. Lesioni
VII. Il registro
VIII. Il mare dei sogni
IX. Il sogno di domani
X. L'ultimo bug
XI. Residuo
XII. La relazione di chiusura

Circa 21.800 parole.

---

</details>

キーワード（7つ、この順）

1. `fantascienza letteraria`
2. `distopia futuro prossimo`
3. `racconti collegati`
4. `distopia burocratica romanzo`
5. `memoria e identità`
6. `fantascienza contemplativa racconti`
7. `fantascienza giapponese in italiano`

カテゴリー（最大3つ、この順）

1. Narrativa → Fantascienza → Antologie e racconti
2. Narrativa → Fantascienza → Distopie
3. Narrativa → Narrativa letteraria

### 13. `nl1` — Het Droombureau

- **題** Het Droombureau
- **副題** Twaalf nachten
- **シリーズ** Het Droombureau（Deel 1）
- **言語** Nederlands　**価格** 3,99 €（オランダ）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

Dromen laten zich niet wissen. Zij laten zich alleen lichter maken.

Terwijl u slaapt, maakt het brein een herinnering zacht, bindt haar opnieuw en laat haar zich weer vastzetten. De droomredactie is het vak dat bij die paar seconden aanwezig is en de hand die bindt een heel klein beetje verzet.

Er is niets anders te doen dan het gewicht van een herinnering verlagen. In één nacht ten hoogste 0,05. In het vak heet dat de halftint.

De grens bestaat niet omdat de techniek tekortschiet. Maak je een herinnering te snel dunner, dan gaat het spoor van de herschrijving met haar mee. Zolang het spoor er is, kan iemand tegen zichzelf zeggen: dit is een geredigeerde droom. Wat de grens beschermt is niet de droom van wie slaapt. Het is de ruimte die daarna, bij het ontwaken, overblijft om aan je eigen geheugen te twijfelen.

Twaalf verbonden verhalen, in een land waar die techniek tot in de laatste hoek van het gewone leven is doorgedrongen.

- Een meisje van dertien dat vraagt haar eigen nachtmerrie te laten staan — Halftint
- Een vrouw die vier jaar en zeven maanden wacht en op de dag van haar beurt afziet — De wachtlijst van de vergetelheid
- Een weduwe die de verontschuldiging in handen krijgt die haar man nooit heeft kunnen uitspreken, gesynthetiseerd uit zijn dagboeken, en een dochter die dat namaak noemt — Het testament
- Een moeder aan wie elke maand een helder, troostend verhaal wordt voorgelezen, vertaald uit de dromen van een zoon zonder taal — De vertaler
- Een technicus die de wroeging van een doodslager in vijftien nachten van 0,07 naar 0,81 brengt — De boete
- Een werkplek waar de behandeling van verdriet binnen achtenveertig uur verplicht is, en een man die zich er niet bij neerlegt — Rouw bij volmacht

Er zijn geen slechteriken. Er zijn alleen mensen die hun werk correct doen, volgens de regeling, en een veld dat de regeling nooit heeft voorzien.

Elk verhaal staat op zichzelf. Hoe verder u komt, hoe duidelijker wordt wat dit land al die tijd geluk heeft genoemd.

INHOUD
I. Halftint
II. De wachtlijst van de vergetelheid
III. Het testament
IV. De vertaler
V. De droom in de tweede persoon
VI. Droombelasting
VII. Rouw bij volmacht
VIII. De boete
IX. Het recht niet te ontwaken
X. De erfopvolging
XI. Geluksindex 98
XII. De zwijgende proefpersoon

Ongeveer 25.500 woorden.

---

</details>

キーワード（7つ、この順）

1. `literaire sciencefiction`
2. `dystopie nabije toekomst`
3. `samenhangende verhalenbundel`
4. `geheugen en identiteit`
5. `beschouwende sciencefiction verhalen`
6. `bureaucratische dystopie roman`
7. `japanse sciencefiction in het nederlands`

カテゴリー（最大3つ、この順）

1. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Anthologieën en korte verhalen
2. Literatuur en fictie → Literaire fictie
3. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Dystopisch

### 14. `nl2` — De Nivellering

- **題** De Nivellering
- **副題** Het Droombureau, Deel Twee
- **シリーズ** Het Droombureau（Deel 2）
- **言語** Nederlands　**価格** 3,99 €（オランダ）　**ロイヤリティ** 70%プラン　**KDPセレクト** 登録する

<details><summary>内容紹介（そのまま貼り付け可）</summary>

De Nivellering. Zo heet een staatsplan dat het gewicht van de herinneringen van een miljoen mensen, nacht na nacht, naar het gemiddelde brengt.

Terwijl u slaapt, maakt het brein een herinnering zacht, bindt haar opnieuw en laat haar zich weer vastzetten. De droomredactie grijpt in die paar seconden in en verlaagt het gewicht; in één nacht kan er ten hoogste 0,05 worden verplaatst. In het vak heet dat de halftint.

Ging Deel I, Het Droombureau, over een technicus en een aanvrager die tegenover elkaar zitten, dan komen deze twaalf verhalen daarna: wanneer de techniek eerst een bedrijfstak is geworden, toen een stelsel, en ten slotte iets van de omvang van een land.

- Een samenleving waarin drie uur slaap genoeg is, en een bedrijf dat in de veertig minuten die overblijven de gevoelens van anderen verkoopt — De stad die niet slaapt
- Een ingreep voor de geboorte die bij een ongeboren kind geborgenheid, vertrouwen en nieuwsgierigheid vormt. Waar zij op werkte, waren niet de kinderen — Fundamenten
- Het verdriet dat naar een dader wordt overgebracht, is de nabestaanden op het ogenblik van de afname al afgenomen — De empathie-injectie
- Percentage automatische verwerking 98,4, en de laatste ambachtsman die de resterende 1,6 draagt — De laatste ambachtsman
- Een man bij wie zeven nachten zonder zijn instemming de dingen zwaarder zijn gemaakt, en die weigert ze te laten terugzetten — Mishandeling
- Een brand met negentien doden die niemand zich herinnert en die nergens is opgeschreven — Het register

Er zijn geen slechteriken. Er zijn alleen mensen die op hun afdeling hun werk correct doen. De Verdeling verandert iets om het bezettingspercentage; de Storingsanalyse om de omvang van de correctiekosten; Technisch Beheer uit tekort aan personeel. Er is geen spoor dat zij met elkaar hebben gesproken.

Wat zich voordeed toen de drie redeneringen in hetzelfde kwartaal bij elkaar kwamen, komt in het laatste verhaal aan het licht, Het eindrapport.

Elk verhaal staat op zichzelf. Deel I is niet nodig.

INHOUD
I. De stad die niet slaapt
II. Fundamenten
III. De empathie-injectie
IV. De laatste ambachtsman
V. Droomt de machine?
VI. Mishandeling
VII. Het register
VIII. De zee van dromen
IX. De droom van morgen
X. De laatste bug
XI. Residu
XII. Het eindrapport

Ongeveer 24.000 woorden.

---

</details>

キーワード（7つ、この順）

1. `literaire sciencefiction`
2. `dystopie nabije toekomst`
3. `samenhangende verhalenbundel`
4. `bureaucratische dystopie roman`
5. `geheugen en identiteit`
6. `beschouwende sciencefiction verhalen`
7. `japanse sciencefiction in het nederlands`

カテゴリー（最大3つ、この順）

1. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Anthologieën en korte verhalen
2. Literatuur en fictie → Sciencefiction en fantasy → Sciencefiction → Dystopisch
3. Literatuur en fictie → Literaire fictie

---

## 5. つまずきやすいところ

1. **シリーズ名は一字一句同じに。** 同じ言語の二巻でシリーズ名が
   一字でも違うと、Amazonはシリーズページを二つ作る。アポストロフィの
   形（`'` と `’`）も違いとして数えられる。この道具が検査している。
2. **ISBNは不要。** KDPが内部管理番号を自動で付ける。自分で買う必要はない。
3. **著者名は全14冊で同じ綴り。** `Kazu A. Suzuki`。
   表記が揺れると著者ページが分かれる。
4. **出版言語は原稿の言語に合わせる。** ここを間違えると、
   その言語の読者に推薦されない。
5. **価格は税抜額を確認。** 70%プランが使えるのは
   2,99 €〜9,99 €（日本は250円〜1,250円）の範囲。
6. **応募作は一冊も含まない。** 『境界線、未編集』は未発表のままで、
   14冊のどこにも入っていない。`check_overlap.py` が七言語で
   機械的に確認している。内容紹介に紛れ込ませないこと。

---

## 6. 出す前に通す検査

```bash
python3 book/tools/sync_tr_counts.py       # 分量の表を更新
python3 book/tools/check_tr_structure.py   # 段落の対応
python3 book/tools/check_tr_terms.py       # 用語と表記
python3 book/tools/check_tr_quotes.py      # 巻をまたぐ引用
python3 book/tools/check_overlap.py        # 応募作との重複
python3 book/tools/kdp_metadata.py         # この一覧を作り直す
```

Kindle Previewerでの表示確認だけは手元でしかできない。
引用符とアクセント記号の出かたを、三機種で見ること。
