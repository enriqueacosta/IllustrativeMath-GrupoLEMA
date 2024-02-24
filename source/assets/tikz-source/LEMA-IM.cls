\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{LEMA-IM}

\newcommand{\gradeFontSize}{\large}
\DeclareOption{grado0}{\renewcommand{\gradeFontSize}{\huge}}
\DeclareOption{grado1}{\renewcommand{\gradeFontSize}{\LARGE}}
\DeclareOption{grado2}{\renewcommand{\gradeFontSize}{\Large}}
% \DeclareOption{grado3}{\tikzset{every node/.append style={font=\large\sansmath\sffamily}}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{standalone}}
\ProcessOptions\relax

\LoadClass[border=5pt, 12pt, tikz, convert={pdf2svg,outfile=\jobname.svg}]{standalone}
\RequirePackage{LEMA-IM}