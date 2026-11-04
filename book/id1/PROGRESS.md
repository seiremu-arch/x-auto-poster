# Edisi Indonesia, Buku I — Status

Terjemahan Buku I, `book/vol1/stories/` → `book/id1/stories/`.

Istilah ditetapkan dalam [`GLOSSARY.md`](../id/GLOSSARY.md), dipakai bersama
oleh kedua buku. Kompilasi dengan `python3 book/tools/build_epub.py id1`.

**Diterjemahkan dari teks asli bahasa Jepang.**

---

## Status

| # | Jepang | Indonesia | Asli | Kata | Status |
|---|---|---|---|---|---|
| I | 半色 | Separuh Warna | 4.997 | 1.993 | **selesai** |
| II | 忘却の順番待ち | Daftar Tunggu Pelupaan | 4.540 | 1.753 | **selesai** |
| III | 夢の遺言 | Wasiat | 4.552 | 1.835 | **selesai** |
| IV | 夢の翻訳者 | Penerjemah | — | — | menunggu |
| V | 二人称の夢 | Mimpi Orang Kedua | — | — | menunggu |
| VI | 夢税 | Pajak Mimpi | — | — | menunggu |
| VII | 涙の代筆 | Duka yang Diwakilkan | — | — | menunggu |
| VIII | 夢裁判 | Hukuman | — | — | menunggu |
| IX | 目覚めない権利 | Hak untuk Tidak Terbangun | — | — | menunggu |
| X | 夢の相続 | Warisan | — | — | menunggu |
| XI | 幸福指数九八 | Indeks Kebahagiaan 98 | — | — | menunggu |
| XII | 沈黙の被験者 | Subjek yang Membisu | — | — | menunggu |

Bahasa Jepang seluruhnya 51.718 karakter. Angka dalam tabel ini ditulis oleh
`python3 book/tools/sync_tr_counts.py id1`, bukan oleh tangan.

---

## Yang khas pada edisi ini

**Ejaan yang berlaku sekarang.** Bukan `tjara`, `djalan`, `oentoek`. Ada
pemeriksaan untuk ejaan sebelum 1972.

**Bahasa Melayu dekat.** Sebuah `isteri` atau `kerana` yang tertinggal tidak
menonjol saat dibaca dalam teks Indonesia, tidak seperti kata Inggris atau
Jerman. Karena itu ada pemeriksaan tersendiri untuk ejaan yang berbeda di antara
kedua bahasa.

**di- dan di.** Awalan pasif dirangkai dan kata depan tempat dipisah. Keduanya
salah dalam arah yang berlawanan, dan keduanya diperiksa mesin: ini kesalahan
yang paling sering terjadi dalam bahasa Indonesia dan paling mudah lewat saat
dibaca.

---

## Pemeriksaan

```bash
python3 book/tools/sync_tr_counts.py id1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py id1
python3 book/tools/build_cover.py id1
```
