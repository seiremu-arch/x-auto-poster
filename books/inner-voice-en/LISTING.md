# KDP registration sheet — Your Quietest Voice (English edition)

Amazon.com向け。**そのまま貼る**ためのもので、ここに「なぜこうしたか」は書かない
(書き直しの方針は Vault `fcfb3b0ebf`、分量は `bdb7a50e65`、表紙の意匠は `0adde001a2` の追記)。

日本語版とは**別のタイトルとして登録する**(同じ本の別版ではない)。著者名は
`Kazu A. Suzuki` で完全に一致させる。一致していないと著者ページが二つに割れる。

項目名や選べる数はKDP側で変わる。**合わなかったら画面のほうに合わせる。**
判断が要る項目には「→ 要判断」と書いてある。

---

## 1. Kindle eBook Details

### Language

English

### Book Title

```
Your Quietest Voice
```

### Subtitle

```
Seven practices for telling your own voice from the noise in your head
```

### Series / Edition Number

なし(両方空欄)

### Author

- First name: `Kazu A.`
- Last name: `Suzuki`

### Description

貼るのはこれ(プレーン版)。**最初の2〜3行だけで読者が自分ごとにできる**組みにしている。

```
After the light goes off, your head starts talking. Tomorrow's reply. The way you said that thing. Something that ended years ago and cannot be changed now. You put the phone down and it keeps going.

This book sorts that talking into four voices. The anxious voice (fast, repeats, speaks in the future tense). The should voice ("normally," "properly," "at your age"). The borrowed voice (somebody else's phrasing, still intact — it has an accent). And the quietest voice: slow, short, and it says things once.

There are only two criteria for telling them apart. Speed — the order they arrive in. And the body — whether it loosens or tightens. Nothing in here asks you to believe anything you can't check for yourself.

Each chapter ends with one practice you can do with paper and a pen. Seven in total: the twenty-four hour rule, seven minutes of doing nothing, the three-part question, the smallest possible step, three lines to come back. Five to fifteen minutes each. You do not have to do all of them. One full chapter is given to the weeks when you hear nothing at all, because those weeks are coming.

There is no universe in here, and no vibrations. Nothing is promised. What's offered is this: a few more nights when you can tell how many voices are talking.

CONTENTS
Prologue: The loudest voice is not always right
1. How many voices are talking (Practice 1: Write the voices down)
2. Telling them apart by speed (Practice 2: The twenty-four hour rule)
3. Telling them apart in the body (Practice 3: Try both options in your body)
4. Making room (Practice 4: Seven minutes of doing nothing)
5. Writing to listen (Practice 5: The three-part question)
6. Deciding small (Practice 6: The smallest possible step)
7. The days you hear nothing (Practice 7: Three lines to come back)
Closing: Quiet is not a destination
Back matter: the seven practices, the four voices

This book is not a substitute for medical or psychological care. If sleep, appetite or mood do not come back, please talk to a professional.
```

太字と改行を効かせたい場合のHTML版。

```html
<p>After the light goes off, your head starts talking. Tomorrow's reply. The way you said that thing. Something that ended years ago and cannot be changed now. You put the phone down and it keeps going.</p>
<p>This book sorts that talking into four voices. <b>The anxious voice</b> (fast, repeats, speaks in the future tense). <b>The <i>should</i> voice</b> ("normally," "properly," "at your age"). <b>The borrowed voice</b> (somebody else's phrasing, still intact — it has an accent). And <b>the quietest voice</b>: slow, short, and it says things once.</p>
<p>There are only two criteria for telling them apart. <b>Speed</b> — the order they arrive in. And <b>the body</b> — whether it loosens or tightens. Nothing in here asks you to believe anything you can't check for yourself.</p>
<p>Each chapter ends with one practice you can do with paper and a pen. Seven in total: the twenty-four hour rule, seven minutes of doing nothing, the three-part question, the smallest possible step, three lines to come back. Five to fifteen minutes each. <b>You do not have to do all of them.</b> One full chapter is given to the weeks when you hear nothing at all, because those weeks are coming.</p>
<p>There is no universe in here, and no vibrations. Nothing is promised. What's offered is this: a few more nights when you can tell how many voices are talking.</p>
<p><b>CONTENTS</b><br>
Prologue: The loudest voice is not always right<br>
1. How many voices are talking (Practice 1: Write the voices down)<br>
2. Telling them apart by speed (Practice 2: The twenty-four hour rule)<br>
3. Telling them apart in the body (Practice 3: Try both options in your body)<br>
4. Making room (Practice 4: Seven minutes of doing nothing)<br>
5. Writing to listen (Practice 5: The three-part question)<br>
6. Deciding small (Practice 6: The smallest possible step)<br>
7. The days you hear nothing (Practice 7: Three lines to come back)<br>
Closing: Quiet is not a destination<br>
Back matter: the seven practices, the four voices</p>
<p><i>This book is not a substitute for medical or psychological care. If sleep, appetite or mood do not come back, please talk to a professional.</i></p>
```

弾かれたらプレーン版に戻す。**貼ったあとにプレビューで改行を見る。**

### Publishing Rights

"I own the copyright and I hold the necessary publishing rights."
本文はすべて書き下ろしで、引用は入っていない。

### Primary Audience

- Sexually explicit images or title: **No**
- Reading age / grade: 空欄(一般向け)

### Keywords (7)

```
overthinking
racing thoughts
inner critic
self-trust
journaling
decision making
mindfulness
```

**タイトルとサブタイトルに入っている語(voice / noise / practices / head / quietest)は
入れていない。** そこはもう検索に効いているので、重複で1枠を潰さない。
`manifestation` `law of attraction` のような、内容と合わない強い語も使わない。

### Categories (up to 3)

画面のブラウズから近いものを選ぶ。候補は上から順に。

1. Self-Help > Personal Transformation
2. Self-Help > Journal Writing
3. Health, Fitness & Dieting > Mental Health > Emotional Mental Health

カテゴリの階層はAmazon側で変わる。**画面に出てきた名前で近いものを選ぶ**のが正で、
このメモに合わせにいかない。

---

## 2. Kindle eBook Content

### Manuscript

```bash
python scripts/build_book.py inner-voice-en --epub
# → books/inner-voice-en/build/inner-voice-en.epub
```

リフロー型。表は巻末の1つだけ(the four voices)。

### Cover

```bash
python scripts/build_cover.py inner-voice-en
# → books/inner-voice-en/build/inner-voice-en-cover.jpg(幅1600 × 高さ2560、JPEG)
```


日本語版と同じ仕様で、文字だけ英語にする(幅1600 × 高さ2560 px(縦長)、RGB、要素3つ、
余白を大きく、細いセリフ体、光の粒子や後光は使わない)。
**日本語版と別のデザインにしない。** 同じ著者の同じ本だと分かる形にする。

### ISBN

不要。空欄のまま。

### DRM

→ **要判断。** 公開後に変更できない。迷うなら Enable。

### Kindle Previewer

アップロード後に必ず一度通す。見るのはこの3つ。

- 巻末の表(the four voices)が崩れていないか
- 目次から各章に飛べるか
- Practice の番号リストが途中で切れていないか

---

## 3. Pricing

### KDP Select

→ **要判断。** 90日間Amazon独占の代わりに Kindle Unlimited の対象になる。
英語圏の self-help は KU で読まれる比率が高いので、初回は登録をすすめる。

### Territories

All territories (worldwide rights)

### Royalty and Price

- Royalty plan: **70%**
- Price (Amazon.com): **$4.99**

70%の範囲は $2.99〜$9.99。$4.99 はその中。他国は米ドルからの自動換算でよい。
**まず $4.99 で出して、レビューが5件つくまで動かさない。**

### Book Lending

Enabled(70%プランでは既定で有効)

---

## 出す前の確認

```bash
python scripts/build_book.py inner-voice-en --check   # 語数と芯の一文の一致
grep -niE "the universe|vibration|manifest|law of attraction|higher self|your true self|soul's purpose|awakening|guaranteed|will change your life|proven|intuition|your gut" \
  books/inner-voice-en/manuscript/*.md               # 序章の宣言1件だけがヒットする状態が正
```

- [ ] **タイトルの重複。** Amazon.com で "Your Quietest Voice" を検索し、同名・近似の本が
      上位にいないか見る。いたら副題で差をつけるか、タイトルを変える(ここが最優先)
  - **2026-10-06 のウェブ検索で同名の本が見つかった。** J.L. Neal『The Quietest Voice: Whispers From the Mind of a Murderer』(The Quietest Voice Series 第1巻、Kindle、2025年5月刊、心理スリラー)。登録は拒まれないが、検索で並ぶ → **題名を変えるかは要判断**(Vault `15227c1bed`)
  - 2026-10-06 に題を **Your Quietest Voice** に変えた(著者の判断)。新しい題と完全に一致する本はウェブ検索では無かった。
    ただし「quietest voice」で検索すると、上のスリラー(Kindle と紙)は近くに並び続ける。登録前に画面で新しい題を検索する
- [ ] 著者名が日本語版と完全に一致しているか(`Kazu A. Suzuki`)
- [ ] Description をプレビューで見て、改行が意図どおりか
- [ ] 表紙のサムネイル(縦200px)でタイトルが読めるか
- [ ] DRM と KDP Select を決めたか(あとから変えにくい2項目)
