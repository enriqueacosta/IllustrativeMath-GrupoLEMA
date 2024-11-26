# Formatos de números

## Números con unidades
Es importante que las unidades abreviadas (como km, g, oz) estén pegadas al número correspondiente para que no se separen con un salto de linea. Para esto, se creó el comando `\unit{}` para usar en modo `<m>...</m>` de LaTeX. 

Entonces, para escribir `La dosis diaria es 1200 mg`, usar:
```xml
La dosis diaria es <m>1200\unit{mg}</m>
```

Correcto:
*  `<m>1200\unit{mg}</m>`
*  `<m>1200 \unit{mg}</m>`
*  `<m>1200    \unit{mg}</m>` (los espacios no importan --- en modo `<m>` se ignoran, y el comando `\unit{}` agrega el espacio apropiado entre en número y la unidad (menos de un espacio completo en su primera implementación)

Incorrecto:
*  `<m>1200</m> \unit{mg}`
*  `<m>1200</m><nbsp/>mg`
*  `1200 mg`
*  `<m>1200</m> mg`

El commando 