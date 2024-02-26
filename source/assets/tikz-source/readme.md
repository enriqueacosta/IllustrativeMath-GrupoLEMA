Esta carpeta contiene las imágenes que se crearon en Tikz (LaTeX). El código fuente de cada imagen está en los archivos `.tex`. 

Por ejemplo, el contenido de `tikz-file-149311.tex` es:
```Tex
\documentclass[grado3]{LEMA-Tikz-IM}
\begin{document}
\begin{tikzpicture}


\newcommand{\hSep}{3.3*\midDotSize}
\newcommand{\vSep}{2*\midDotSize}
\midDotGroup{2}{1}
\midDotGroup[shift={(1*\hSep,0)}]{2}{1}
\midDotGroup[shift={(2*\hSep,0)}]{2}{1}
\midDotGroup[shift={(0,1*\vSep)}]{2}{1}
\midDotGroup[shift={(1*\hSep,1*\vSep)}]{2}{1}
\midDotGroup[shift={(2*\hSep,1*\vSep)}]{2}{1}

\end{tikzpicture}
\end{document}
```
Esté código produce la imagen:


![](tikz-file-149311.svg)


Se creó un estilo propio de Tikz para este proyecto. Está compuesto por los archivos

*  LEMA-Tikz-IM.cls
*  LEMA-Tikz-IM.sty

Estos dos archivos contienen las definiciones del documentclass `LEMA-Tikz-IM` y todos los comandos especiales. Por ejemplo tienen la definición del comando `\midDotGroup{#}{#}` que hace un grupo de puntos con un rectángulo alrededor de ellos.


Con el código `.tex`, al correr `pdflatex` se produce el archivo pdf de la imagen que se va a usar en el pdf. Así:
```bash
pdflatex tikz-file-149311.tex
```
Este comando produce el archivo
*  tikz-file-149311.pdf


## Generar los archivos svg para la web
Para las páginas web de los libros se necesitan conversiones de estos archivos a formato `svg`. Se creó un script para automatizar esta conversión. Ver el script [convertAllPDFtoSVGinFolder](https://github.com/enriqueacosta/IllustrativeMath-GrupoLEMA/blob/main/scripts/convertAllPDFtoSVGinFolder)

Este script usa `pdf2svg` para hacer la conversión de todos los archivos `pdf` que no tienen correspondiente `svg` en la carpeta. Para esto, ejecuta comandos de la forma:
```bash
pdf2svg tikz-file-147472.pdf
```
Los svg que produce pdf2svg se ven muy chiquitos en la web cuando se ponen en su tamaño natural (al cambiar `width : 100%` a `max-width : 100%` en el CSS. 

Para agrandarlos el script usa comandos del estilo:
```bash
rsvg-convert --zoom 1.25 --format svg --output tikz-file-149311.svg tikz-file-149311.svg
```

Para instalar `pdf2svg` en MacOS usar `brew install pdf2svg` con `homebrew`.

Para instalar `rsvg-convert` en MacOS usar `brew install librsvg` con `homebrew`.

Para correr el script hay que ejecutarlo en la forma 
```bash
./convertAllPDFtoSVGinFolder
```
Es posible que toque hacer una copia del script en la carpeta `assets/tikz-source` para poder ejecutarlo.
