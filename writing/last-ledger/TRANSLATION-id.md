# インドネシア語版の方針と対訳表

『最後の帳簿　三つに分けられた遺産』のインドネシア語訳。`manuscript/`（日本語）が原本、
`manuscript-id/` が訳文。**底本は日本語原文。** ほかの版（英・独・仏・西・伊・蘭・葡）は、
固有名詞と言い回しの決め方をそろえるための参照にだけ使う。

## 基本方針

1. **舞台は日本のまま。** 円は *yen*、法制度は日本の法制度。
2. **人名は名→姓**（Shuji Kamiya）。ほかの版と同じ。
3. **敬称。** 姓で呼ぶ相手は *Pak*／*Bu*（*Pak Kamiya*, *Bu Tachibana*, *Bu Sagara*）。
   遠野家は神谷の台詞の中で「-san」を残す（Ryosuke-san, Chizuru-san, Katsumi-san）。
   日本の作品の敬称はインドネシアの読者になじみがある。
   千鶴は兄を *Kak Ryosuke*、亮介は妹を名前で呼ぶ。
4. **Anda／kamu。** 夫婦（aku／kamu）、兄妹、克巳から千鶴、宗一郎から子どもたちはくだけた形。
   それ以外は *Anda* と *saya*。亮介が神谷を「あんた」と呼ぶ場面だけ *kamu* に落として、無礼さを出す。
5. **台詞は “ ”（二重引用符）で括る。** インドネシアの小説で一般的な形。地の文の受けは
   `“Itu saja,” kata Kamiya.` の形。入れ子は ‘ ’。神谷の頭の中で反復される帳簿や手紙の一行は斜体。
   “ ” の対応とほかの版の約物の混入は `check_id.py` で検査する。
6. **法律用語に脚注をつけない。** 台詞の中で一度だけ説明する。
7. **文体。** 短い平叙文。感情の形容詞を使わない。段落は短く。`※` の区切りはそのまま。
8. **数字。** 台詞と地の文の金額は語で書く（*dua puluh delapan juta yen*）。
   帳票は `72.043.518`、`¥1.480`、一覧は `21,4 jt`。日付は `10 Februari 2026`、
   短い日付は日／月（`8/2`）、時刻は `18.40`。
   階数は日本と同じ数え方（地上階が *lantai satu*。日本の2階 = *lantai dua*）。

## 数字の対比（ほかの版と同じ置き換え）

| | 日本語版 | インドネシア語版 |
|---|---|---|
| 歴代の行 | 昭和十六年十二月 | *Showa 16, bulan kedua belas* |
| 〃 | 平成三年 | *Heisei 3* |
| 宗一郎の行 | 2026年2月10日 | **10 Februari 2026** |

## 固有名詞

| 日本語 | Bahasa Indonesia |
|---|---|
| 本家 | rumah induk |
| 遠野精工（株式会社） | (PT) Tono Presisi |
| 遠野建装 | Tono Konstruksi |
| 上州あかぎ銀行 宇賀野支店 | Bank Joshu Akagi cabang Ugano |
| 群馬中央信用金庫 | Koperasi Kredit Gunma Chuo |
| 北関東証券 | Kita-Kanto Securities |
| 白鷺開発 | (PT) Shirasagi Development |
| 梶原FPオフィス | Kantor Perencana Keuangan Kajiwara |
| 前田不動産 | Agen Properti Maeda |
| 宇賀野中央法律事務所 | Kantor Hukum Ugano Chuo |
| 北関東データセンター構想 | proyek pusat data Kanto Utara |
| ホームセンター栄和 | Eiwa Home Center（toko bangunan） |
| リョウ・クリエイト / 〈Arclight Capital〉 / 〈TAKA〉 | PT Ryo Create / Arclight Capital / TAKA |

人名・地名は英語版と同じ（`TRANSLATION.md`）。

## 法律・金融の語

| 日本語 | Bahasa Indonesia |
|---|---|
| 公正証書遺言 | akta wasiat notaris |
| 公証人 / 公証役場 | notaris / kantor notaris |
| 遺言執行者 | pelaksana wasiat |
| 遺留分 | bagian mutlak（インドネシア民法 KUHPerdata にもある概念） |
| 付言事項 | catatan pribadi（「法的効力はない」と第26章で説明される） |
| 遺贈 | hibah wasiat |
| 四十九日 | hari keempat puluh sembilan |
| 月命日 | peringatan bulanan |
| 信託 / 受託者 / 受益権 | trust / bank wali amanat / hak sebagai penerima manfaat |
| 連帯保証（人） | penjaminan tanggung renteng / penjamin tanggung renteng |
| 稟議（書） | usulan kredit |
| 試算表 / 粉飾 | neraca saldo / laporan yang dimanipulasi |
| 固定資産評価証明書 | surat keterangan NJOP（インドネシアの固定資産税評価額の語） |
| 路線価 / 倍率地域 | nilai acuan jalan / zona pengali（橘の台詞で一行説明） |
| 延納 | pembayaran bertahap, cicilan tahunan |
| 実印 / 印鑑証明 | cap terdaftar / sertifikat pendaftaran cap |
| 登記事項証明書 | surat keterangan pendaftaran tanah |
| 任意同行 | datang secara sukarela ke kantor polisi |
| 公訴の取り消し | dakwaan ditarik |
| 鍵の受け渡し簿 | catatan serah terima kunci（表紙は *Kunci*） |

## 繰り返される言い回し

| 日本語 | Bahasa Indonesia |
|---|---|
| すべてを一つに賭けた者には、一円も残すな | **Jangan tinggalkan satu yen pun bagi orang yang mempertaruhkan segalanya pada satu hal.** |
| 毎月、決まった額を、決まった日に／それだけ？／それだけです | **Setiap bulan, jumlah yang sama, di tanggal yang sama.** / *Itu saja?* / *Itu saja.* |
| 私は、何もしていません。／何もしなかっただけです。 | **Saya tidak melakukan apa-apa.** / **Saya hanya membiarkannya terjadi.** |
| 2026年2月10日　三つに分けた　もう一つ　分けられなかったものがある | **10 Februari 2026　kubagi tiga　masih ada satu　yang tak bisa kubagi** |
| 階段から落ちて死んだのなら、それは事故ではありません | **Kalau saya meninggal karena jatuh dari tangga, itu bukan kecelakaan.** |
| 片づける人のやり方です | **Begitulah cara orang yang menyimpan barang.** |
| 金を失ったことのある人間にしか、金の見張りは頼めない | **Hanya kepada orang yang pernah kehilangan uang, kita bisa meminta untuk mengawasi uang.** |
| 金を守れた人間には…／守れなかった人間だけが、どこで手が滑るかを知っている | *Kepada orang yang mampu menjaga uangnya, tidak bisa diminta untuk mengawasi uang.* / *Hanya orang yang tidak mampu menjaganya yang tahu di mana tangan tergelincir.* |
| 間に合わなかったんですか | **Jadi saya terlambat?** |
| いちばん重いものを持とうとする | **ingin memikul beban yang paling berat** |
| もういいんです | **Sudah tidak perlu.** |
| 三つの籠 | tiga keranjang |
| 土地／事業／現金（封筒に書く三つ） | **Tanah / Perusahaan / Uang** |

## 帳簿の七つの記号

漢字を出し、地の文で意味を添える。土 tanah ／ 種 benih ／ 木 pohon ／ 蜜 madu ／ 鍵 kunci ／ 手 tangan ／ 水 air

## タイトル

- シリーズ: **Buku Kas Terakhir**
- 第1巻: **Buku Kas Terakhir: Warisan dalam Tiga Bagian**

## 章題

| 章 | 原題 | インドネシア語 |
| --- | --- | --- |
| 序 | プロローグ | Prolog |
| 1 | 誘導灯 | Tongkat Lampu |
| 2 | 消印 | Cap Pos |
| 3 | 11日 | Tanggal Sebelas |
| 4 | 三つの籠 | Tiga Keranjang |
| 5 | 1996年 | 1996 |
| 6 | 杭 | Patok |
| 7 | 番頭 | Tangan Kanan |
| 8 | 差額 | Selisih |
| 9 | 封をする紙 | Kertas Bersegel |
| 10 | 勝ち組の側 | Di Pihak Pemenang |
| 11 | 三つの値段 | Tiga Harga |
| 12 | 四つの穴 | Empat Lubang |
| 13 | 2月5日 | 5 Februari |
| 14 | 三分の一 | Sepertiga |
| 15 | 相良 | Sagara |
| 16 | 四回目 | Kali Keempat |
| 17 | 任意 | Sukarela |
| 18 | 一回だけ | Hanya Sekali |
| 19 | 名簿 | Daftar Nama |
| 20 | もういいんです | Sudah Tidak Perlu |
| 21 | 立てかけてあった | Bersandar di Dinding |
| 22 | 三つ | Tiga |
| 23 | 何もしなかった | Saya Tidak Melakukan Apa-Apa |
| 24 | 2月10日 | 10 Februari |
| 25 | 連絡先 | Kontak Darurat |
| 26 | 四通目 | Amplop Keempat |
| 27 | 定期 | Deposito Berjangka |
| 終 | エピローグ | Epilog |

章題はインドネシアの書籍の慣例どおり、各語の頭を大文字にした。
第7章「番頭」は、社長の右腕として帳場を預かる人という意味で *Tangan Kanan*。
第23章は千鶴の最後の台詞から *Saya Tidak Melakukan Apa-Apa* とし、続く「何もしなかっただけです」は
*Saya hanya membiarkannya terjadi.*（起きるのに任せただけ）と訳した（伊・蘭・葡語版と同じ判断）。
第27章「定期」は *Deposito Berjangka*（神谷の嘘「定期に入れてある」と同じ語）。

## 翻訳中に見つけて直した原文の傷

| 章 | 直したこと |
|---|---|
| 9 | 兄の亮介が妹の千鶴を「お姉ちゃん」と呼んでいた。「千鶴、それ書いて意味あんの」に直した（英・独・仏・西・伊の各版はもともと名前で訳していた） |
