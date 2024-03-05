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


Formato de notas para el docente
================================
\tcbset{ remarkstyle/.style={blockspacingstyle, breakable, parbox=false, after title={}, boxrule=0mm, leftrule=5pt, bottomrule=2pt, bottomrule at break=0pt, boxsep=0mm, arc=0mm, outer arc=0mm, toptitle=2mm, bottomtitle=1mm, colback=orange!20, colframe=orange!80,} }
\newtcolorbox[use counter from=block]{remark}[2]{title={{\bf Notas para el profesor\notblank{#1}{\space\space#1}{}}}, phantomlabel={#2}, breakable, parbox=false, after={\par}, remarkstyle, }

o este:
\tcbset{ remarkstyle/.style={blockspacingstyle, breakable, parbox=false, after title={}, boxrule=1.5pt, bottomrule=2pt, bottomrule at break=0pt, toprule at break=0pt, boxsep=0mm, arc=0mm, outer arc=0mm, toptitle=2mm, bottomtitle=1mm, colback=orange!20, colframe=orange!80,} }