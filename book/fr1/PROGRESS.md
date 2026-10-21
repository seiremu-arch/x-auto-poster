# Édition française, Livre I — État

Traduction du Livre I, `book/vol1/stories/` → `book/fr1/stories/`.

La terminologie est fixée dans [`GLOSSARY.md`](../fr/GLOSSARY.md). Un terme se
décide là avant de servir. Compiler avec `python3 book/tools/build_epub.py fr1`.

**On traduit depuis l'original japonais**, non depuis les éditions anglaise,
allemande ou espagnole.

---

## État

| # | Japonais | Français | Origine | Mots | État |
|---|---|---|---|---|---|
| I | 半色 | Demi-teinte | 4 997 | 2 647 | **fait** |
| II | 忘却の順番待ち | La file d'attente de l'oubli | 4 540 | 2 259 | **fait** |
| III | 夢の遺言 | Le testament | 4 555 | — | en attente |
| IV | 夢の翻訳者 | Le traducteur | 3 915 | — | en attente |
| V | 二人称の夢 | Le rêve à la deuxième personne | 3 454 | — | en attente |
| VI | 夢税 | L'impôt sur les rêves | 3 391 | — | en attente |
| VII | 涙の代筆 | Le deuil par procuration | 4 476 | — | en attente |
| VIII | 夢裁判 | La peine | 4 577 | — | en attente |
| IX | 目覚めない権利 | Le droit de ne pas se réveiller | 4 503 | — | en attente |
| X | 夢の相続 | La succession | 4 587 | — | en attente |
| XI | 幸福指数九八 | Indice de Bonheur 98 | 4 218 | — | en attente |
| XII | 沈黙の被験者 | Le sujet silencieux | 4 508 | — | en attente |

Japonais au total, 51 721 caractères. Les chiffres de ce tableau sont écrits par
`python3 book/tools/sync_tr_counts.py fr1`, non à la main.

---

## Décidé dans la nouvelle I

**Dialogue au tiret cadratin.** Le français admet les guillemets comme le tiret
par réplique ; le tiret est celui de la narrative contemporaine et il garde en
outre un paragraphe pour un paragraphe avec le japonais.

**Narration et dialogue dans le même paragraphe.** Là où le japonais met dans un
seul paragraphe une phrase de narration suivie de 「parole」, le français garde
**un seul paragraphe** et ouvre le tiret sur la même ligne :

> Le chef rit un peu, puis se fit sérieux. Ce que nous faisons ici, au fond,
> c'est aérer.

Couper en deux paragraphes serait tout aussi correct, mais la traduction
cesserait de correspondre paragraphe pour paragraphe à l'original, et
`check_tr_structure.py` ne servirait plus à détecter une omission. Ce contrôle
vaut mieux que la variante typographique.

**Espace insécable avant `:` `;` `?` `!` et dans les guillemets.** C'est une
règle du français, non une préférence : sans elle la ligne se coupe au mauvais
endroit sur une liseuse. On ne la tape pas à la main sur vingt-quatre
nouvelles : on écrit avec des espaces ordinaires et on passe
`python3 book/tools/fix_fr_spacing.py`, puis `check_tr_terms.py` vérifie.

**Virgule décimale, milliers à l'espace insécable.** 0,05 et 0,91 ; 1 027 400 et
non 1.027.400. C'est le point de divergence avec l'espagnol et l'allemand, qui
séparent les milliers par un point.

**Vouvoiement.** Kaji et Saya se vouvoient, même si Saya a treize ans. Le
japonais est en forme polie de bout en bout, et le rapport entre le Bureau et
qui s'y présente est justement le sujet du livre.

**L'intervalle du Correcteur.** « Un intervalle simplement posé à l'endroit où
la phrase se coupe. » Avec mesure : la version japonaise l'a réduit de huit
occurrences à trois, et le français garde ces trois-là.

**半色 → demi-teinte.** C'est le mot le plus heureux des quatre langues. Le
japonais 半色 dit « demi-couleur » ; l'anglais a dû forger *half-shade*,
l'allemand prendre *Halbton*, l'espagnol *media tinta*. Le français avait déjà
le mot d'imprimerie exact, et il porte le demi-pas sans glose.

---

## Contrôles

```bash
python3 book/tools/fix_fr_spacing.py
python3 book/tools/sync_tr_counts.py fr1
python3 book/tools/check_tr_structure.py
python3 book/tools/check_tr_terms.py
python3 book/tools/check_overlap.py
python3 book/tools/build_epub.py fr1
python3 book/tools/build_cover.py fr1
```
