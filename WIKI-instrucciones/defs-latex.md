## Apagar las ligarutas (Roboto le quita el punto a la i en fi)
```latex
\RequirePackage[sfdefault]{roboto}
% to disable ligatures (roboto removes the dot of the i in fi)
\usepackage{microtype}\DisableLigatures{encoding = *, family = *}
```


## Tener control sobre los espacios arriba y abajo de las imagenes
Ajustar las defs de {tcbimage} e {image} así. La clave es el ` before skip=\parskip, after skip=\parskip`. Lo de `\par\vspace{\parskip}%` es para que la imagen siempre empiece con `\par`. Latex se encarga de no agregar dos `\parskip` por la forma en la que combina unidades de glue.
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
  \par\vspace{\parskip}%  % Always end the current paragraph and add one parskip
  \begin{tcbimage}{#1}{#2}{#3}
}{%
  \end{tcbimage}
}
```
