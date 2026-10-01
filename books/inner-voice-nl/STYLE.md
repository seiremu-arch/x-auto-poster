# Stijlregels — De zachtste stem

日本語版 `books/inner-voice/STYLE.md` と同じ立場を、オランダ語で守るためのもの。
**読者が自分で確かめられることだけを書く。**

## Toon en positie

- **`je`.** Standaard in het genre; `u` klinkt als een brief van de gemeente
- “Ik” voor alles wat persoonlijk is. “Dit doe ik”, niet “dit moet je doen”
- Nooit een toestand aan de lezer toeschrijven. Niet “als je moe bent” maar “op vermoeide dagen”
- Niet onderwijzen: **ernaast staan.** “Proberen” liever dan “moeten”

### Gebiedende wijs: alleen in stappen en in voorwaardelijke zinnen

1. in de **genummerde stappen** van een oefening
2. in de **voorwaardelijke zin** — “Zet de namen terug, en het wordt weer een gewone vergadering.”

Niet toegestaan: een **kale opdracht** in de lopende tekst en in koppen. De gebiedende wijs is
de stam (“Schrijf”, “Tel”); een stam vooraan in de zin zonder onderwerp erachter is een opdracht.
“Schrijf je het op, dan…” is een voorwaarde (onderwerp `je` erachter) en mag.

## Geen streektaal

Amazon.nl bedient Nederland en Vlaanderen. Woorden die maar aan één kant gangbaar zijn, gaan eruit.

| Niet | Wel |
| --- | --- |
| gsm / mobieltje | telefoon |
| frigo | koelkast (of een ander voorbeeld) |
| pinnen | betalen |
| zetel | bank |
| plezant / goesting | leuk / zin |

## Geen geslacht voor auteur en lezer

Het Nederlands verbuigt bijvoeglijke naamwoorden niet naar het geslacht van een persoon
(`ik ben moe`, `je bent verrast`). Wat overblijft zijn persoonsnamen: de auteur noemt zichzelf
niet “een twijfelaar”, “een beginner” of iets met `-ster`. Personages (de vriendin uit hoofdstuk 1)
hebben wel een geslacht. → Vault `0045c354b1`(読者)/ `dba7c10f3f`(著者)。

Wat er voor de lezer wel overblijft: de algemene `wie …, hij` (“Wie alleen op het lichaam beslist,
ontloopt zijn hele leven…”). Die vorm maakt de lezer stilzwijgend mannelijk. Liever: `wie …` zonder
voornaamwoord erachter, of `je`. `check_style.py` vangt `wie … hij / hem / zijn eigen|hele…`.

## Woorden die er niet in staan

> universum / trilling(en) / manifesteren / wet van aantrekking / hoger zelf / je ware zelf /
> zielsmissie / energie (ook niet als beeld) / spiritueel ontwaken / onderbewustzijn (zonder definitie) /
> ego (zonder definitie) / intuïtie / onderbuikgevoel

Geen absolute beweringen over het effect: **altijd / nooit (over resultaten) / iedereen / gegarandeerd /
verandert je leven / bewezen**. “Wordt nooit luider” in de kernzin gaat over de stem.

Eén uitzondering: de zin in de proloog die zegt dat er in dit boek geen universum en geen trillingen voorkomen.

## Termen

| Begrip | Term | 日本語版 |
| --- | --- | --- |
| de vier stemmen | de angstige stem / de moet-stem / de geleende stem / de zachtste stem | 不安の声 / べき論の声 / 借りものの声 / 内なる声 |
| markering | **A** / **M** / **G** / **?** | |
| criterium 1 | snelheid (de volgorde waarin ze komen) | 速さ |
| criterium 2 | het lichaam — ontspant of spant aan | 体 — ゆるむ / 締まる |
| wat je maakt | ruimte (niet stilte) | 余白 |
| wat je doet | tellen, onderscheiden, terugkomen | 数える / 聞き分ける / 戻る |

De kop van de twijfelsecties is “Waar het vaak vastloopt” (zonder `je`).

## Typografie

Dubbele krulaanhalingstekens “…”. Geen rechte `"` in de tekst. Enkele aanhalingstekens niet gebruiken
(ze botsen met `zo'n`, `auto's`).

## Veiligheid

- Geen lichamelijk symptoom wordt met deze oefeningen geduid
- Niets wat gelezen kan worden als “je hoeft niet naar de dokter”
- Als slaap, eetlust of stemming niet terugkomen, stoppen de oefeningen en komt er iemand met
  kennis van zaken bij (de huisarts als eerste stap). In hoofdstuk 3 **en** in de bijlage

```bash
python books/inner-voice-nl/check_style.py
```
