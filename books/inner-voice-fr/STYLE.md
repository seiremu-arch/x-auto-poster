# Règles de style — La voix la plus basse

日本語版 `books/inner-voice/STYLE.md` と同じ立場を、フランス語で守るためのもの。
**読者が自分で確かめられることだけを書く。**

## Adresse et posture

- **`vous`.** Pas `tu`(理由は Vault `e778004e3b`)。例外は登場人物どうしの会話だけ
  (第1章の友人の台詞「Démissionne, tout simplement.」など)
- « Je » pour tout ce qui est personnel. « Voici ce que je fais », pas « Voici ce qu'il faut faire »
- Ne jamais attribuer un état au lecteur. Pas « vous êtes épuisé », mais « quand on est épuisé »
- Ne pas enseigner : **se tenir à côté.** « Essayer » plutôt que « il faut »
- Quand je parle d'expérience, les fois où ça n'a pas marché en font partie

### Impératif : seulement dans les étapes et dans les phrases conditionnelles

Comme `du` en allemand, `vous` peut glisser vers la consigne. L'impératif est permis à deux endroits :

1. dans les **étapes numérotées** d'un exercice
2. dans la **phrase conditionnelle** — « Remettez les noms, et cela redevient une réunion normale. »
   Ce n'est pas une consigne, c'est l'explication d'une conséquence

Interdit : la **consigne nue** dans le texte courant et dans les titres.
Pas « Utilisez le corps seulement pour… », mais « Le corps ne sert qu'à… ».
Pas « ## Coupez la question en trois », mais « ## La question, coupée en trois ».

L'allemand a appris la leçon à ses dépens (14 cas trouvés après coup, → Vault `7586251f89`).
Ici, on vérifie **dès le premier chapitre**.

## Mots absents

Tout ce qui ne peut pas être vérifié. Ni dans le texte, ni sur la couverture, ni dans la description.

> l'univers / vibration(s) / manifester / loi de l'attraction / moi supérieur / votre vrai moi /
> mission d'âme / énergie (même en image) / éveil / subconscient (sans définition) /
> ego (sans définition) / intuition / « votre instinct »

Pas d'affirmations absolues sur l'effet : **toujours / jamais (à propos des résultats) /
tout le monde / garanti / changera votre vie / prouvé**. Le `grep` sur ces mots demande
un œil humain : « pas toujours », « jamais plus fort » (dans la phrase centrale) sont en règle.

Une exception, comme dans les autres éditions : la phrase de l'avant-propos qui dit qu'il
n'y a ni univers ni vibrations dans ce livre.

## Termes (identiques d'un chapitre à l'autre)

| Concept | Terme | 日本語版 |
| --- | --- | --- |
| les quatre voix | la voix anxieuse / la voix du « il faut » / la voix empruntée / la voix la plus basse | 不安の声 / べき論の声 / 借りものの声 / 内なる声 |
| critère 1 | la vitesse (l'ordre dans lequel elles arrivent) | 速さ |
| critère 2 | le corps — ça se relâche ou ça se serre | 体 — ゆるむ / 締まる |
| ce qu'on crée | de la place (pas le silence) | 余白 |
| ce qu'on fait | compter, distinguer, revenir | 数える / 聞き分ける / 戻る |

## Typographie

Espace insécable avant `; : ! ?` et à l'intérieur des guillemets `« … »`.
Dans les fichiers on tape une espace normale ; `check_style.py --fix` la remplace
par une espace insécable (U+00A0), pour que la liseuse ne coupe jamais la ligne
juste avant un point d'interrogation.

## Phrases

- Une idée par phrase
- Trois ou quatre phrases par paragraphe. L'idée principale dans la première
- Les scènes commencent par un moment concret, pas par une abstraction
- Deux images par chapitre, au plus

## Sécurité

- Aucun symptôme physique n'est interprété à travers ces exercices
- Rien qui puisse se lire comme « pas besoin de voir un médecin »
- Dire clairement : si le sommeil, l'appétit ou l'humeur ne reviennent pas, les exercices
  s'arrêtent et quelqu'un de formé prend le relais. Au chapitre 3 **et** en annexe

```bash
python books/inner-voice-fr/check_style.py         # impératif, mots absents, typographie
python books/inner-voice-fr/check_style.py --fix   # espaces insécables
```
