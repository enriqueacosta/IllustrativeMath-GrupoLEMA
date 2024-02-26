Esta carpeta contiene las imágenes para las que se tiene solo el formato web `svg`. 

Para las versiones pdf de las unidades se necesitan conversiones de estos archivos a formato `pdf`. 

Se creó un script para automatizar esta conversión. Ver

https://github.com/enriqueacosta/IllustrativeMath-GrupoLEMA/blob/main/scripts/convertAllSVGtoPDFinFolder

Este script usa `rsvg-convert` para hacer la conversión de todos los archivos `svg` que no tienen correspondiente `pdf` en la carpeta. Para esto, ejecuta comandos de la forma:
```bash
rsvg-convert --format=pdf --zoom=1 tikz-file-147472.svg > tikz-file-147472.pdf
```
(el `--zoom=1` es para tener la opción de cambiar el tamaño, pero normalmente debe ser 1)

Para instalar `rsvg-convert` en MacOS usar `brew install librsvg` con `homebrew`.

 