# Reglas de estilo — La voz más baja

日本語版 `books/inner-voice/STYLE.md` と同じ立場を、スペイン語で守るためのもの。
**読者が自分で確かめられることだけを書く。**

## Trato y postura

- **`tú`.** Ni `usted` (distante en este género), ni `vosotros` (solo España),
  ni `vos` (solo algunas regiones). → Vault `cb294d65c0`
- «Yo» para todo lo propio. «Esto es lo que hago», no «esto es lo que hay que hacer»
- Nunca atribuir un estado al lector. No «estás agotado», sino «en los días de cansancio»
- No enseñar: **estar al lado.** «Probar» antes que «hay que»
- Cuando hablo de experiencia, las veces que no funcionó también cuentan

### Imperativo: solo en los pasos y en las frases condicionales

1. en los **pasos numerados** de un ejercicio
2. en la **frase condicional** — «Vuelve a poner los nombres, y se convierte en una reunión normal.»
   No es una orden: explica una consecuencia

Prohibido: la **orden desnuda** en el texto corrido y en los títulos.
No «Usa el cuerpo solo para…», sino «El cuerpo solo sirve para…».

## Sin género gramatical para el autor ni para el lector

→ Vault `c36e89b074`. Ni el autor ni el lector tienen un género fijado por la gramática.

| En lugar de | Escribir |
| --- | --- |
| me quedé sorprendido | me sorprendió |
| estaba solo | estaba a solas |
| estoy seguro de que | tengo la certeza de que / seguramente |
| cuando estás cansado | en los días de cansancio / cuando el cansancio aprieta |
| si te quedas dormido | si el sueño gana |
| no estás obligado | nada te obliga |
| me sentí pesado | todo se volvió pesado |

`check_style.py` busca `estoy / estaba / me sentí / estás / te sientes …` seguidos de
un adjetivo o participio con género. Los personajes (la amiga del capítulo 1) sí tienen género.

## Vocabulario neutral

| Evitar (regional) | Usar |
| --- | --- |
| móvil / celular | teléfono |
| piso (vivienda) / departamento | apartamento |
| coche / carro | auto |
| ordenador / computadora | (evitar; «pantalla» si hace falta) |
| vale / ahorita / guay / chévere / chido | (evitar) |
| coger | tomar / agarrar |
| zumo / jugo, conducir / manejar | (evitar) |
| aparcar / estacionar | (evitar) |
| alquiler | alquiler (se entiende en todas partes; «renta» significa también ingreso) |

Formas de `vosotros` (`sabéis`, `tenéis`) y de `vos` (`sabés`, `tenés`) cuentan como errores.

## Palabras ausentes

> el universo / vibración(es) / manifestar / ley de la atracción / yo superior /
> tu verdadero yo / misión del alma / energía (ni como imagen) / despertar espiritual /
> subconsciente (sin definir) / ego (sin definir) / intuición / «tu instinto»

Sin afirmaciones absolutas sobre el efecto: **siempre / nunca (sobre resultados) / todo el mundo /
garantizado / cambiará tu vida / comprobado**. «Nunca hablará más fuerte» en la frase central
es sobre la voz, no sobre un resultado.

Una excepción: la frase del prólogo que dice que en este libro no hay universo ni vibraciones.

## Términos

| Concepto | Término | 日本語版 |
| --- | --- | --- |
| las cuatro voces | la voz ansiosa / la voz del «debería» / la voz prestada / la voz más baja | 不安の声 / べき論の声 / 借りものの声 / 内なる声 |
| criterio 1 | la velocidad (el orden en que llegan) | 速さ |
| criterio 2 | el cuerpo — se afloja o se tensa | 体 — ゆるむ / 締まる |
| lo que se crea | espacio (no silencio) | 余白 |
| lo que se hace | contar, distinguir, volver | 数える / 聞き分ける / 戻る |

## Tipografía

- Signos de apertura obligatorios: `¿…?` y `¡…!`. `check_style.py` comprueba que cada
  línea tenga tantos `¿` como `?` y tantos `¡` como `!`
- Comillas latinas `«…»` sin espacios interiores

## Seguridad

- Ningún síntoma físico se interpreta a través de estos ejercicios
- Nada que pueda leerse como «no hace falta ir al médico»
- Si el sueño, el apetito o el ánimo no vuelven, los ejercicios se detienen y entra alguien
  con formación. En el capítulo 3 **y** en el apéndice

```bash
python books/inner-voice-es/check_style.py
```
