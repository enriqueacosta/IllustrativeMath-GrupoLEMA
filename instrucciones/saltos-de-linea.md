# Saltos de línea

PreTeXt, siguiendo su filosofía que el markup XML debe especificar estructura del contenido y no forma, no permite el uso de tags `<br/>` para saltar linea.

Hay dos cosas para tener en cuenta si quiere un salto de linea:

1. Pregúntese: ¿de verdad quiero un salto de línea? ¿o en realidad es un párrafo nuevo y no estaba bien no agregar la separación? Si es párrafo nuevo, use ¡`<p>....</p>`!
2. En PreTeXt se puede separar un párrafo en líneas específicando lo que va en cada linea (piense, en un poema). El formato es así:
    ```xml
    <p>
      <line> contenido de la 1ra línea </line>
      <line> 2da línea </line>
      <line> 3ra línea </line>
    </p>
    ```
