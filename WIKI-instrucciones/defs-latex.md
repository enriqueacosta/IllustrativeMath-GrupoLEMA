## Apagar las ligaduras (la fuente Roboto le quita el punto a la i en "fi")
```latex
\RequirePackage[sfdefault]{roboto}
% to disable ligatures (roboto removes the dot of the i in fi)
\usepackage{microtype}\DisableLigatures{encoding = *, family = *}
```


## Tener control sobre los espacios arriba y abajo de las imagenes
Ajustar las defs de {tcbimage} e {image} así. La clave es el ` before skip=\parskip, after skip=\parskip`.
```latex
\tcbset{ imagestyle/.style={enhanced, blanker} }
\NewTColorBox{tcbimage}{mmm}{
  imagestyle,
  left=0pt, right=0pt, top=0ex, bottom=0ex,
  width=#2\linewidth,
  boxsep=0pt,
  before skip=\parskip, after skip=\parskip
}
\NewDocumentEnvironment{image}{mmmm}{%
  \notblank{#4}{\leavevmode\nopagebreak\vspace{#4}}{~%
  \par\vspace{\parskip}}%  % Always end the current paragraph and add one parskip
  \begin{tcbimage}{#1}{#2}{#3}
}{%
  \end{tcbimage}
}
```
Note que parecería por el  `\par\vspace{\parskip}%` es para que {image} siempre empiece con `\par` (un párrafo nuevo) y simepre aregue el espacio (por si no está en vertical mode). Latex se encarga de no agregar dos `\parskip` por la forma en la que combina unidades de glue.


## footer con fancyheader con distintos tamaños de fuente sin que se cree un caos en el tamaño del salto de línea
El paquete fancyheader no se comporta muy bien con los ajustes de tamaño de fuente. El \baselineskip no se actualiza bien.

Arreglo, usar un \parbox:

```latex
\fancyfoot[L]{%
  \parbox{1.05\textwidth}{%
    \fontsize{9pt}{11pt}\selectfont
    Grupo LEMA (www.grupolema.org), \the\year{}. Licencia de uso CC-BY-NC Internacional 4.0.\\
    \fontsize{7pt}{8.4pt}\selectfont
    Adaptado de IM K--5 Math v.I, © 2021 Illustrative Mathematics ® illustrativemathematics.org en su versión en español en im.kendallhunt.com y de Open Up Resources © 2022, openupresources.org, publicadas bajo una licencia Creative Commons CC BY 4.0. \\Detalles: https://creativecommons.org/licenses/by/4.0/deed.es
  }
}
```
