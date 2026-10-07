# Ficha KDP — *El último libro de cuentas: Una herencia en tres partes*（スペイン語版）

スペイン語版は、ほかの版とは別の KDP タイトル（別ASIN）として登録する。
以下はそのまま KDP の入力欄に貼れる。**残るのは表紙と価格の2つ。**

---

## 1. 入稿ファイル

| ファイル | 用途 |
| --- | --- |
| `El_ultimo_libro_de_cuentas_1_Una_herencia_en_tres_partes.epub` | **KDPにアップロードするのはこれ**（横書き・左開き） |
| `El_ultimo_libro_de_cuentas_1_Una_herencia_en_tres_partes.md` | 統合原稿（読み返し用） |

EPUB3・リフロー、`dc:language` は `es`、`page-progression-direction="ltr"`。
本文は `../manuscript-es/*.md`、方針と対訳表は `../TRANSLATION-es.md`。
本文を直したら、`../check_es.py` で « » と ¿ ¡ の漏れを確かめてから組む。

```bash
python3 writing/last-ledger/check_es.py
python3 writing/last-ledger/build_epub.py --spanish
```

---

## 2. Detalles del libro

**Idioma**

```
Español
```

**Título / Subtítulo**

```
El último libro de cuentas
Una herencia en tres partes
```

**Serie / Número**

```
El último libro de cuentas / 1
```

**Autor**

```
Nombre: Kazu A.
Apellido: Suzuki
```

**Descripción**（約240語。KDPの上限は4,000字）

```
Dejó trescientos millones de yenes. Cada heredero solo podrá quedarse con un tercio.

Durante treinta años, Shuji Kamiya examinó expedientes de crédito en un banco japonés,
y durante un año le ocultó a su mujer que había perdido la mayor parte de su
indemnización en una estafa de inversión extranjera. Entonces llega por correo un
viejo libro de cuentas. Lo envía un hombre al que solo vio una vez, hace treinta años:
Soichiro Tono, cuya empresa dejó caer el banco de Kamiya en 1996.

La carta que lo acompaña dice: «Si he muerto al caer por la escalera, no fue un
accidente».

Fue enviada el día antes de que Soichiro cayera por la escalera de la casa familiar,
vacía.

Su testamento divide la herencia en inmuebles, empresa y efectivo, y obliga a tres
herederos a elegir cada uno una parte en un sobre cerrado. Si dos eligen la misma, va
a una fundación. Como nota personal dejó una sola línea: «A quien lo haya apostado
todo a una sola cosa, que no le quede ni un yen».

Nombrado albacea, Kamiya empieza a contar. De la noche a la mañana, el terreno cae de
cien a veinte millones. Hay dinero que ha desaparecido en el extranjero. Y en la pared
de la escalera quedan cuatro agujeros de tornillo, donde antes había una barandilla.

Una novela negra financiera, sobria y precisa, sobre la herencia, la estafa y un
crimen que consiste en no hacer nada. Libro 1 de la serie «El último libro de cuentas».
```

**Palabras clave**（7つまで）

```
novela negra japonesa
thriller financiero
misterio herencia testamento
secretos de familia japón
estafa inversión novela
traducida del japonés
novela policiaca literaria
```

**Categorías**（KDPで3つまで。表示名はストアで変わるので、ピッカーで最も近いものを選ぶ）

```
Tienda Kindle › eBooks Kindle › Policíaca, negra y suspense › Policíaca › Internacional
Tienda Kindle › eBooks Kindle › Policíaca, negra y suspense › Thriller › Financiero
Tienda Kindle › eBooks Kindle › Literatura y ficción › Literatura extranjera › Asia › Japón
```

**Contenido para adultos** No
**Territorios** Todos

---

## 3. ★ AI開示（必須）

KDP は、本文・画像・**翻訳**にAIを使ったかを申告させる。このスペイン語版は
**AIの支援で翻訳した**ので、*Traducciones*（Translations）は **Sí／Yes** と答える。
誤って申告すると販売停止になることがある。

---

## 4. ★ 表紙（未着手）

- 1600 × 2560 px、JPEG または TIFF、RGB、72dpi以上、50MB未満
- 文字：**EL ÚLTIMO LIBRO DE CUENTAS** ／ *Una herencia en tres partes* ／ **Kazu A. Suzuki**
- ほかの版と同じ絵に文字だけ載せ替えると、シリーズとしてそろう

---

## 5. 価格

- 約36,000語。紙換算でおよそ160〜180ページ
- 主な市場は Amazon.es（スペイン）と Amazon.com.mx（メキシコ）。米国のスペイン語読者は Amazon.com
- 70%ロイヤリティの価格帯は Amazon.es で 2,99〜9,99 €（**税込で設定する**。スペインの電子書籍はIVA 4%）。
  メキシコは MXN で別に設定する
- 新人作家の第1巻なら **2,99〜3,99 €** が置きやすい
- スペインには書籍の定価制度（Ley del libro、電子書籍も対象）があり、メキシコにも同様の
  「precio único」がある。KDPセレクトに入れず他のストアでも売る場合は、国内のどのストアでも
  同じ価格にする必要がある

---

## 6. 出版前チェックリスト

- [x] 著者名 `Kazu A. Suzuki`（`dc:creator`、扉、Créditos）
- [x] EPUB の XML 検証済み、`mimetype` 非圧縮で先頭
- [x] « » と ¿ ¡ の対応（`check_es.py`）
- [ ] 表紙画像（1600 × 2560 px）
- [ ] KDP プレビューアで確認：左開き、段落の字下げ、`※` の区切り
- [ ] 目次（Índice）から全章に飛べるか
- [ ] 帳簿の最新の一行が *10 de febrero de 2026…* になっているか（和暦の中で唯一の西暦）
- [ ] AI開示（3.）
- [ ] 内容紹介の末尾に第2巻の予告を入れるか
