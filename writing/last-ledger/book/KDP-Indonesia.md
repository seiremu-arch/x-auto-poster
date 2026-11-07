# Data KDP — *Buku Kas Terakhir: Warisan dalam Tiga Bagian*（インドネシア語版）

インドネシア語版は、ほかの版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。ただしその前に、0. を必ず確かめる。**

---

## 0. ★ 出版前にまず確かめること：KDPがインドネシア語を受け付けるか

KDPの「Supported languages（対応言語）」のページに、電子書籍の言語として
**Indonesian（Bahasa Indonesia）** が載っているかを確かめる。
この版を作った時点では、作業環境からKDPのヘルプページを開けず、**確認できていない**。

- 載っていれば、このシートのとおりに登録する
- 載っていなければ、KDPでは出せない。インドネシア語の電子書籍を扱うほかの配信先
  （たとえば Google Play ブックスのパートナー登録）で受け付けるかを調べる。
  EPUB はそのまま使える

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `Buku_Kas_Terakhir_1_Warisan_dalam_Tiga_Bagian.epub` | **入稿するのはこれ**（横書き・左開き） |
| `Buku_Kas_Terakhir_1_Warisan_dalam_Tiga_Bagian.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `id`、`page-progression-direction="ltr"`。
本文は `../manuscript-id/*.md`、方針と対訳表は `../TRANSLATION-id.md`。
本文を直したら、`../check_id.py` で “ ” の対応を確かめてから組む。

```bash
python3 writing/last-ledger/check_id.py
python3 writing/last-ledger/build_epub.py --indonesian
```

---

## 2. Detail buku

**Bahasa**

```
Bahasa Indonesia
```

**Judul / Subjudul**

```
Buku Kas Terakhir
Warisan dalam Tiga Bagian
```

**Seri / Nomor**

```
Buku Kas Terakhir / 1
```

**Pengarang**

```
Nama depan: Kazu A.
Nama belakang: Suzuki
```

**Deskripsi**（約240語。KDPの上限は4,000字）

```
Ia meninggalkan tiga ratus juta yen. Setiap ahli waris hanya boleh mengambil sepertiganya.

Tiga puluh tahun Shuji Kamiya menilai usulan kredit di sebuah bank Jepang, dan sudah
setahun ia menyembunyikan dari istrinya bahwa sebagian besar uang pesangonnya habis
dalam penipuan investasi luar negeri. Lalu datang lewat pos sebuah buku kas tua.
Pengirimnya lelaki yang hanya sekali ia temui, tiga puluh tahun lalu: Soichiro Tono,
yang perusahaannya dilepas oleh bank tempat Kamiya bekerja pada tahun 1996.

Surat yang menyertainya berbunyi: “Kalau saya meninggal karena jatuh dari tangga, itu
bukan kecelakaan.”

Surat itu diposkan sehari sebelum Soichiro jatuh dari tangga di rumah induk keluarga
yang kosong.

Wasiatnya membagi harta menjadi tanah, perusahaan, dan uang, dan memaksa tiga ahli
waris memilih masing-masing satu bagian dalam amplop tersegel. Kalau dua orang memilih
yang sama, bagian itu jatuh ke yayasan. Sebagai catatan pribadi, ia hanya meninggalkan
satu baris: “Jangan tinggalkan satu yen pun bagi orang yang mempertaruhkan segalanya
pada satu hal.”

Ditunjuk sebagai pelaksana wasiat, Kamiya mulai menghitung. Dalam semalam, nilai tanah
jatuh dari seratus juta menjadi dua puluh juta. Ada uang yang lenyap ke luar negeri.
Dan di dinding tangga tersisa empat lubang sekrup, tempat dulu ada pegangan.

Novel misteri keuangan yang tenang dan cermat, tentang warisan, penipuan, dan kejahatan
yang berupa tidak melakukan apa-apa. Buku 1 seri “Buku Kas Terakhir”.
```

**Kata kunci**（7つまで）

```
novel misteri jepang
thriller keuangan
misteri warisan wasiat
rahasia keluarga jepang
novel penipuan investasi
terjemahan dari bahasa jepang
novel detektif
```

**Kategori**（KDPで3つまで。表示名はストアで変わるので、ピッカーで最も近いものを選ぶ）

```
Kindle Store › Kindle eBooks › Mystery, Thriller & Suspense › Mystery › International Mystery & Crime
Kindle Store › Kindle eBooks › Mystery, Thriller & Suspense › Thrillers & Suspense › Financial
Kindle Store › Kindle eBooks › Literature & Fiction › World Literature › Asian › Japanese
```

**Konten dewasa** Tidak
**Wilayah** Semua

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このインドネシア語版は
**AIの支援で翻訳した**ので、*Translations* は **Yes** と答える。
誤って申告すると販売停止になることがある。ほかの配信先でも、同様の申告欄があれば同じく答える。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**BUKU KAS TERAKHIR** ／ *Warisan dalam Tiga Bagian* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約31,000語。紙換算でおよそ150〜170ページ
- Amazon にはインドネシア向けのストアがなく、インドネシアの読者は主に Amazon.com から買う。
  価格は USD で設定する。インドネシアの電子書籍の相場はほかの版の市場より低いので、
  英語版と同じ値段にせず、低めに置くことを検討する
- 70%ロイヤリティを選べる価格帯と条件は、KDPの価格欄とロイヤリティの説明で確かめる

---

## 6. 出版前チェックリスト

- [ ] **KDPの対応言語にインドネシア語があるか（0.）**
- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Hak Cipta）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] “ ” の対応とほかの版の約物の混入（`check_id.py`）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り
- [ ] 目次（Daftar Isi）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 Februari 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
