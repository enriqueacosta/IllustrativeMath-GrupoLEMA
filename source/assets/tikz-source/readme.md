Esta carpeta contiene las imágenes que se crearon en Tikz (LaTeX). El código fuente de cada imagen está en los archivos `.tex`. Ejemplo: `tikz-file-149311.tex`

El contenido de `tikz-file-149311.tex` es por ejemplo
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
[]!(tikz-file-149311.svg)


Se creó un estilo propio de Tikz para este proyecto. Está compuesto por los archivos

*  LEMA-Tikz-IM.cls
*  LEMA-Tikz-IM.sty

Estos dos archivos contienen las definiciones del documentclass `LEMA-Tikz-IM` y todos los comandos especiales. Por ejemplo tienen la definición del comando `\midDotGroup{#}{#}` que hace un grupo de puntos con un rectángulo alrededor de ellos.


Con el código `tex`, al correr `pdflatex` se produce el archivo pdf de la imagen que se va a usar en el pdf. Así:
```bash
pdflatex tikz-file-149311.tex
```
Este comando produce el archivo
*  tikz-file-149311.pdf

Para producir el archivo svg para la web, se puede usar pdf2svg:
```bash
pdf2svg tikz-file-149311.pdf
```

Alternativamente, se pueden crear los archivos pdf y svg al tiempo usando la opción de `--shell-escape` de LaTeX:
```bash
pdflatex -shell-escape tikz-file-149311.tex
```
Produce los archivos `tikz-file-149311.pdf` y `tikz-file-149311.svg`.

Esto funciona así porque el `documentclass{LEMA-Tikz-IM}` está definido en `LEMA-Tikz-IM.cls` así:
```TeX
\LoadClass[border=5pt, 12pt, tikz, convert={pdf2svg,outfile=\jobname.svg}]{standalone}
```

## Agrandar los svg
Los svg que produce pdf2svg se ven muy chiquitos en la web cuando se ponen en su tamaño natural (al cambiar `width : 100%` a `max-width : 100%` en el CSS. 

Para agrandarlos se puede usar un comando como:
```bash
rsvg-convert --zoom 1.25 --format svg --output tikz-file-149311.svg tikz-file-149311.svg
```