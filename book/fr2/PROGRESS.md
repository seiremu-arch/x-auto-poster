# Édition française, Livre II — État

Traduction du Livre II, `book/vol2/stories/` → `book/fr2/stories/`.

La terminologie est fixée dans [`GLOSSARY.md`](../fr/GLOSSARY.md), partagé avec
le Livre I. Compiler avec `python3 book/tools/build_epub.py fr2`.

**On traduit depuis l'original japonais.**

---

## État

| # | Japonais | Français | Origine | Mots | État |
|---|---|---|---|---|---|
| I | 眠らない都市 | La ville qui ne dort pas | 4 336 | 2 179 | **fait** |
| II | 胎夢 | Fondations | 4 240 | 2 045 | **fait** |
| III | 共感注射 | L'injection d'empathie | 4 432 | 2 124 | **fait** |
| IV | 最後の夢職人 | Le dernier artisan | 4 226 | 2 070 | **fait** |
| V | ＡＩは夢を見るか | La machine rêve-t-elle ? | 3 963 | — | en attente |
| VI | 夢の犯罪 | Violences | 3 933 | — | en attente |
| VII | 消えた現実 | Le registre | 3 982 | — | en attente |
| VIII | 夢の海 | La mer des rêves | 3 889 | — | en attente |
| IX | 明日の夢 | Le rêve de demain | 3 879 | — | en attente |
| X | 最後のバグ | Le dernier bug | 3 843 | — | en attente |
| XI | 残差 | Résidu | 3 906 | — | en attente |
| XII | 完了報告 | Le rapport de clôture | 4 090 | — | en attente |

Japonais au total, 48 719 caractères. Les chiffres de ce tableau sont écrits par
`python3 book/tools/sync_tr_counts.py fr2`, non à la main.

---

## Ce qui est nouveau dans ce livre

Le Plan de Nivellement passe du fond au centre. Le Livre I le mentionne ; le
Livre II traite de sa clôture.

La huitième nouvelle cite littéralement du Livre I — des nouvelles deuxième,
quatrième et douzième — et de la sixième de ce livre. Si la traduction s'écarte
ne fût-ce que d'un mot, le lien entre les livres se rompt.
`check_tr_quotes.py` le vérifie mécaniquement, par langue, et les cinq phrases
françaises y sont enregistrées **avant** d'être écrites : la table est la
spécification, non le relevé.

---

## La nouvelle présentée au prix

Le Livre II est celui qui court le plus près de『境界線、未編集』, parce que les
deux traitent de la Deuxième Synchronisation. On partage le monde — la
demi-teinte, le Plan de Nivellement, la Deuxième Synchronisation —, non une
phrase, ni un personnage, ni une image. La passerelle piétonne verte de la
nouvelle présentée ne figure dans aucun des deux livres et ne doit pas y
figurer.

---

## Contrôles

```bash
python3 book/tools/fix_fr_spacing.py
python3 book/tools/sync_tr_counts.py fr2
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_tr_quotes.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py fr2
python3 book/tools/build_cover.py fr2
```
