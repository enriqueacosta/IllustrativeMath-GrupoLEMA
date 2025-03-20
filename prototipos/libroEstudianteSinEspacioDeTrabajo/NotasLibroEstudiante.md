Formato ancho
====================
```
\documentclass{book}
\usepackage[hmargin=3cm, vmargin=1in]{geometry}
```

O, para 2-up:
```
\documentclass[twocolumn]{book}
\setlength{\columnsep}{0.5in}
\usepackage[landscape,hmargin=1cm, vmargin=0.5in]{geometry}
```


Arreglos de imagenes
====================
Por defecto, las imagenes están con \includegraphics[width=\linewidth]
que las hace agrandarse (mal).

Este código arregla esto:
```
\usepackage[export]{adjustbox}% 'export' allows adjustbox keys in \includegraphics
```
seguido de cambiar todos los `[width=\linewidth]` a `[max width=\linewidth]`.


Para kinder con fuente más grande
==================================
\documentclass{book} solo acepta hasta 12pt, entonces usar:
```
\documentclass[14pt]{extbook}
```


Para que los \\ y los \par se comporten distinto en los tcolorbox
===================================================================

```
before upper={%
\setlength{\parskip}{1.1ex}%
\renewcommand{\\}{\par\vspace*{-0.8\parskip}}%
}

```

Para footnotes pequeños
=======================
```
% Make footnotes tiny and reduce spacing
\usepackage{footmisc}  % Package to control footnote formatting
\renewcommand{\footnotemargin}{1em}  % Align footnotes with no extra indentation
\renewcommand{\footnotesize}{\tiny}  % Set all footnotes to tiny font
\setlength{\footnotesep}{0.3\baselineskip}  % Reduce vertical spacing between footnotes
```