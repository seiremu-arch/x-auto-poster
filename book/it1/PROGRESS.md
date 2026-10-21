# Edizione italiana, Libro I — Stato

Traduzione del Libro I, `book/vol1/stories/` → `book/it1/stories/`.

La terminologia è fissata in [`GLOSSARY.md`](../it/GLOSSARY.md). Un termine si
decide là prima di essere usato. Compilare con
`python3 book/tools/build_epub.py it1`.

**Si traduce dall'originale giapponese**, non dalle edizioni inglese, tedesca,
spagnola o francese.

---

## Stato

| # | Giapponese | Italiano | Origine | Parole | Stato |
|---|---|---|---|---|---|
| I | 半色 | Mezzatinta | 4.997 | 2.307 | **fatto** |
| II | 忘却の順番待ち | La lista d'attesa dell'oblio | 4.540 | 1.958 | **fatto** |
| III | 夢の遺言 | Il testamento | 4.552 | 1.981 | **fatto** |
| IV | 夢の翻訳者 | Il traduttore | 3.915 | 1.616 | **fatto** |
| V | 二人称の夢 | Il sogno in seconda persona | 3.454 | 1.515 | **fatto** |
| VI | 夢税 | L'imposta sui sogni | 3.391 | 1.478 | **fatto** |
| VII | 涙の代筆 | Il lutto per delega | 4.476 | 1.893 | **fatto** |
| VIII | 夢裁判 | La pena | 4.577 | 1.929 | **fatto** |
| IX | 目覚めない権利 | Il diritto di non svegliarsi | 4.503 | 2.001 | **fatto** |
| X | 夢の相続 | La successione | 4.587 | 1.937 | **fatto** |
| XI | 幸福指数九八 | Indice di Felicità 98 | 4.218 | 1.933 | **fatto** |
| XII | 沈黙の被験者 | Il soggetto silenzioso | 4.508 | 2.118 | **fatto** |

Giapponese in totale, 51.718 caratteri. Le cifre di questa tabella le scrive
`python3 book/tools/sync_tr_counts.py it1`, non la mano.

---

## Deciso nel racconto I

**Dialogo con le caporali.** È la norma della narrativa italiana. Il trattino
per battuta è l'uso spagnolo e francese; in italiano tradirebbe la traduzione.
Le caporali non prendono spazi interni.

**Narrazione e dialogo nello stesso paragrafo.** Dove il giapponese mette in un
solo paragrafo una frase di narrazione seguita da 「battuta」, l'italiano tiene
**un solo paragrafo** e apre le caporali sulla stessa riga:

> Il capo rise un poco, poi si fece serio. «Quello che facciamo qui, in fondo,
> è dare aria.»

Dividerlo in due paragrafi sarebbe altrettanto corretto, ma la traduzione
smetterebbe di corrispondere paragrafo per paragrafo all'originale, e
`check_tr_structure.py` non servirebbe più a rilevare un'omissione. Quel
controllo vale più della variante tipografica.

**Nessuno spazio prima di `:` `;` `?` `!`.** È la regola opposta a quella
francese. Avendo scritto l'edizione francese immediatamente prima, è l'errore
più probabile, perciò sta nel controllo.

**Virgola decimale, migliaia col punto.** 0,05 e 0,91; 114.206 e 1.027.400.
Come lo spagnolo e il tedesco, non come il francese.

**Lei.** Kaji e Saya si danno del Lei, anche se Saya ha tredici anni. Il
giapponese è in forma cortese dall'inizio alla fine, e il rapporto fra
l'Ufficio e chi vi si presenta è proprio il tema del libro.

**L'intervallo del Correttore.** «Un intervallo posato soltanto dove la frase
si interrompe.» Con misura: la versione giapponese l'ha ridotto da otto
occorrenze a tre, e l'italiano tiene quelle tre.

**半色 → mezzatinta.** Come il francese e lo spagnolo, l'italiano aveva già la
parola tipografica esatta. L'inglese ha dovuto coniare *half-shade*.

---

## Controlli

```bash
python3 book/tools/sync_tr_counts.py it1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py it1
python3 book/tools/build_cover.py it1
```
