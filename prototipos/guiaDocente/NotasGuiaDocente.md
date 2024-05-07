Para quitar los errores de \begin{spanish}
==========================================
\newenvironment{spanish}{\relax}{\relax}

Para poder las imagenes con ancho=max width 
===========================================
Por defecto, las imagenes están con \includegraphics[width=\linewidth]
que las hace agrandarse (mal).

Este código arregla esto:
```
\usepackage[export]{adjustbox}% 'export' allows adjustbox keys in \includegraphics
```
seguido de cambiar todos los `[width=\linewidth]` a `[max width=\linewidth]`.


Formato dos columnas
====================
\documentclass[twocolumn]{book}
\setlength{\columnsep}{0.5in}
\usepackage[landscape,hmargin=1cm, vmargin=1in]{geometry}


Arreglo longtable
==================
Es posible que toque redefinir longtable para twocolumn. Así:

```tex
\makeatletter
\let\oldlt\longtable
\let\endoldlt\endlongtable
\def\longtable{\@ifnextchar[\longtable@i \longtable@ii}
\def\longtable@i[#1]{\begin{figure}[t]
\onecolumn
\begin{minipage}{0.5\textwidth}
\oldlt[#1]
}
\def\longtable@ii{\begin{figure}[t]
\onecolumn
\begin{minipage}{0.5\textwidth}
\oldlt
}
\def\endlongtable{\endoldlt
\end{minipage}
\twocolumn
\end{figure}}
\makeatother
```
cortesía de: https://tex.stackexchange.com/questions/161431/how-to-solve-longtable-is-not-in-1-column-mode-error


Formato de notas para el docente
================================
\tcbset{ remarkstyle/.style={blockspacingstyle, breakable, parbox=false, after title={}, boxrule=0mm, leftrule=5pt, bottomrule=2pt, bottomrule at break=0pt, boxsep=0mm, arc=0mm, outer arc=0mm, toptitle=2mm, bottomtitle=1mm, colback=orange!20, colframe=orange!80,} }
\newtcolorbox[use counter from=block]{remark}[2]{title={{\bf Notas para el profesor\notblank{#1}{\space\space#1}{}}}, phantomlabel={#2}, breakable, parbox=false, after={\par}, remarkstyle, }

o este:
\tcbset{ remarkstyle/.style={blockspacingstyle, breakable, parbox=false, after title={}, boxrule=1.5pt, bottomrule=2pt, bottomrule at break=0pt, toprule at break=0pt, boxsep=0mm, arc=0mm, outer arc=0mm, toptitle=2mm, bottomtitle=1mm, colback=orange!20, colframe=orange!80,} }