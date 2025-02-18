# Crear pdfs de una sola actividad o un solo cool para impresión

Última actualización: 18 de Febrero 2025

Instrucciones para crear in pdf de una sola actividad listo para impresión (con todos los comandos de espaciado de impresión, con encabezado y pie de página con info de licencia)

1. Asegurarse que la actividad está lista para impresión (inlcuyendo los comandos de espaciado whitespace)

2. Asegurarse que la actividad haga parte del libro de trabajo (todos los cools en el momento hacen parte del libro de trabajo).

3. Generar el código latex del libro de trabajo. Por ejemplo:
   ```terminal
   pretext build gra3-uni4-libroTrabajo
   ```
4. Copiar el script `extractCool-latexStandalone.py` o `extractActivity-latexStandalone.py` a la carpeta del output definida para este build en `project.ptx` (por ejemplo, en este momento `output/print-latex-libroTrabajo/gra3-uni4`) 

5. Identificar el `xml:id` de la actividad o cool que se quiere general. Par este ejemplo, va a ser el cooldown `cool-marcaPartesParaEncontrarArea`.

6. Abrir una terminal en la carpeta del output definida para este build en `project.ptx` (por ejemplo, en este momento `output/print-latex-libroTrabajo/gra3-uni4`) y ejecutar el script así (en este ejemplo, para extraer un cool):
   ```terminal
   python extractCool-latexStandalone.py gra3-uni4.tex cool-marcaPartesParaEncontrarArea 14pt
   ```
   Acá:
   *   `python extractCool-latexStandalone.py` ejecuta el script. Cambiar a `python extractAct-latexStandalone.py` si es una actividad.
   *   `gra3-uni4.tex` es el archivo tex del cual se va a extraer la actividad o cool.
   *   `cool-marcaPartesParaEncontrarArea` es el `xml:id` de la actividad o cool.
   *   `14pt` es el tamaño de la fuente (que debe ser distinto de acuerdo al grado. `14pt` es el tamaño correcto para grado 3 en este momento.


7. El script genera un archivo `.tex` y corre pdfLaTeX solo para generar el pdf correspondiente. Revisar el pdf y decidir si necesita ajustes. 

8. De requerir ajustes decidir si esos ajustes debe ser del source `.ptx` (en cuyo caso hay que hacerlos y regenerar el `.tex` del libro de trabajo) o si deben ser ajustes locales al `.tex` que se van a perder a futuro.

9. Mover cuando esté bien, mover el pdf (sin cambiarle el nombre) a la carpeta `source/assets/cool-pdf/` o `source/assets/act-pdf/` dependiendo de si es un cool o una actividad. Si es in cool, esto se asegura de que funcione bien que el link en el HTML del cool para impirmir.

10. Si se quiere dar el link a profesores o estudiantes para que puedan imprimir (por ejemplo, su hay un diagrama para rayar), usar un codigo del estilo:
   ```xml
   <aside component="web">
       <p>
          Copia para imprimir y rayar en el libro de trabajo, o <url href="external/cool-pdf/cool-marcaPartesParaEncontrarArea.pdf">descargar acá</url>.
       </p>
    </aside>
   ```