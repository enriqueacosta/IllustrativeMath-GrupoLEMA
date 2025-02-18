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
