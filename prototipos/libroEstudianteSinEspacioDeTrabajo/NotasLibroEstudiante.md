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