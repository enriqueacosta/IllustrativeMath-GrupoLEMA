## Apagar las ligaduras (Roboto le quita el punto a la i en "fi")
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
Note que parecería por el  `\par\vspace{\parskip}%` es para que {image} siempre empiece con `\par` (un párrafo nuevo) y simepre aregue el espacion (por si no está en vertical mode). Latex se encarga de no agregar dos `\parskip` por la forma en la que combina unidades de glue.
