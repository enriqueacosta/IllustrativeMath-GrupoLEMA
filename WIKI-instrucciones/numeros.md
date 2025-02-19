# Formatos de números

## Regla: números siempre en `<m>...</m>`
Siempre que aparezca un número, ponerlo en modo LaTeX con `<m>...</m>`. Esto garantiza uniformidad de cómo se ven los números en todo el grado (tamaño, fuente, color).


## Números con unidades
Es importante que las unidades abreviadas (como km, g, oz) estén pegadas al número correspondiente para que no se separen con un salto de linea. Para esto, se creó el comando `\unit{}` para usar en modo `<m>...</m>` de LaTeX. 

Entonces, para escribir `La dosis diaria es 1200 mg`, usar:
```xml
La dosis diaria es <m>1200\unit{mg}</m>
```

Correcto:
*  `<m>1200\unit{mg}</m>`
*  `<m>1200 \unit{mg}</m>`
*  `<m>1200    \unit{mg}</m>` (los espacios no importan --- en modo `<m>` se ignoran, y el comando `\unit{}` agrega el espacio apropiado entre en número y la unidad).

Incorrecto:
*  `<m>1200</m> \unit{mg}`
*  `<m>1200</m><nbsp/>mg`
*  `1200 mg`
*  `<m>1200</m> mg`

Ver def del marco `\unit{}` en `<macros>` en meta_docinfo.ptx.


## Números con decimales y separadores de miles
Todo número que tenga un separador decimal se debe escribir con el formato `\num{1234.56}`. 

Ejemplos:

*  `<m> 3x + \num{14.56} +10 = \num{13.45} </m>`
*  `<m>\num{1200.532} \unit{mg}</m>`
*  `x+ \frac{\num{45.321}}{\num{0.1}}`

Solo los números con separador decimal necesitan `\num`, pero no pasa nada si se lo ponen a un entero, como `\num{10}`.

**Qué se logra con esto:** en HTML y LaTeX se puede definir `\num` para que haga cosas como:
*  Cambiar el separador decimal de `.` a `,`
*  Agregar separadores de miles para números mayores que 9999.

Ver https://github.com/enriqueacosta/IllustrativeMath-GrupoLEMA/issues/113 sobre lo que se debe hacer.

## Números mixtos
Para números mixtos (como 3⅘) usar siempre el código LaTeX `n\trac{p}{q}` (con `\tfrac`, no con `\frac`). 

**¿por qué usar `\tfrac`?**: La fracción en el número mixto 3⅘ debe aparecer pequeña. Si uno está en `<m>` y no en `<me>` o `<md>`, el código `<m>3\frac{4}{5}</m>` va a funcionar perfecto *excepto* si el `<m>` es el único contenido de un item de una lista (un `<li>`). En ese caso PreTeXt agrega un \displaystyle sin que se le solicite y esto causa que `\frac{4}{5}` se muestre grande (incorrecto). La solución en los casos de `<me>`, `<md>` o [`<m>` solo adentro de un `<li>`] es usar el comando especial `\tfrac{4}{5}`. Este commando le indica a LaTeX o a MathJaX que esta es una fracción que no se debe agrandar. Como el comando `\tfrac{4}{5}` también funciona and `<m>` es mejor unificar todos los casos y que el código latex no dependa del lugar en el que está.

*Nota*: Se podría desabilitar el comportaminto de PreTexT de agregar el `\displaystyle` en las listas, pero es mejor hacer que el LaTeX contenga el significado semantico. En todo caso, el código de PreTeXt que hace esto está en el archivo `pretext-common.xsl`. Buscar `<xsl:template match="m" mode="display-style-prefix">`.  

