# Edisi Indonesia, Buku II — Status

Terjemahan Buku II, `book/vol2/stories/` → `book/id2/stories/`.

Istilah ditetapkan dalam [`GLOSSARY.md`](../id/GLOSSARY.md), dipakai bersama
oleh kedua buku. Kompilasi dengan `python3 book/tools/build_epub.py id2`.

**Diterjemahkan dari teks asli bahasa Jepang.**

---

## Status

| # | Jepang | Indonesia | Asli | Kata | Status |
|---|---|---|---|---|---|
| I | 眠らない都市 | Kota yang Tidak Tidur | 4.336 | 1.858 | **selesai** |
| II | 胎夢 | Fondasi | 4.240 | 1.843 | **selesai** |
| III | 共感注射 | Suntikan Empati | 4.432 | 1.770 | **selesai** |
| IV | 最後の夢職人 | Perajin Terakhir | 4.226 | 1.784 | **selesai** |
| V | ＡＩは夢を見るか | Apakah Mesin Bermimpi? | 3.963 | 1.604 | **selesai** |
| VI | 夢の犯罪 | Penganiayaan | 3.933 | 1.575 | **selesai** |
| VII | 消えた現実 | Buku Induk | 3.982 | 1.759 | **selesai** |
| VIII | 夢の海 | Laut Mimpi | 3.889 | 1.593 | **selesai** |
| IX | 明日の夢 | Mimpi Besok | 3.879 | 1.655 | **selesai** |
| X | 最後のバグ | Bug Terakhir | 3.843 | 1.598 | **selesai** |
| XI | 残差 | Residu | 3.906 | 1.683 | **selesai** |
| XII | 完了報告 | Laporan Penyelesaian | 4.090 | 1.706 | **selesai** |

Bahasa Jepang seluruhnya 48.719 karakter. Angka dalam tabel ini ditulis oleh
`python3 book/tools/sync_tr_counts.py id2`, bukan oleh tangan.

---

## Yang baru dalam buku ini

Rencana Pemerataan bergeser dari latar ke tengah. Buku I menyebutnya; Buku II
bercerita tentang penyelesaiannya.

Bahwa 均し bisa bernama *Pemerataan* dalam bahasa Indonesia adalah keberuntungan
edisi ini. Itu bukan kata teknik yang netral, melainkan kata kebijakan negara,
kata untuk program yang mengecilkan selisih.

Cerita kedelapan mengutip kata demi kata dari Buku I — dari cerita kedua,
keempat, dan kedua belas — dan dari cerita keenam buku ini. Kalau terjemahannya
bergeser satu kata saja, ikatan antara kedua buku itu putus.
`check_tr_quotes.py` memeriksanya dengan mesin, bahasa demi bahasa, dan kelima
kalimat Indonesia itu terdaftar di sana **sebelum** ditulis: tabel itu
spesifikasi, bukan risalah.

---

## Cerita yang diikutkan lomba

Buku II yang paling dekat jalannya dengan『境界線、未編集』, karena keduanya
berbicara tentang Sinkronisasi Kedua. Yang dibagi adalah dunianya — separuh
warna, Rencana Pemerataan, Sinkronisasi Kedua —, bukan satu kalimat, bukan satu
tokoh, bukan satu gambar. Jembatan penyeberangan hijau dari cerita yang
diikutkan lomba tidak muncul di kedua buku dan tidak boleh muncul.

---

## Pemeriksaan

```bash
python3 book/tools/sync_tr_counts.py id2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py id2
python3 book/tools/build_cover.py id2
```
