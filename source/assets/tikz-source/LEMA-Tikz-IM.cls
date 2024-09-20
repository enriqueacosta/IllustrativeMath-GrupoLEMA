\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{LEMA-Tikz-IM}

\LoadClass[border=5pt, tikz]{standalone}
\RequirePackage{LEMA-Tikz-IM}

\RequirePackage{pgf}       % for floating pint arithmetic arithmetic
\RequirePackage{fix-cm}    % allow for arbitrary font sizes using fix-cm



% Opciones dependiendo del grado (por ejemplo, tamaño de la fuente)
% Ejemplo: \documentclass[grado3]{LEMA-IM}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Código para ajustar la fuente dependiento del grado
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% \newcommand{\gradeFontSize}{\normalsize}
% \DeclareOption{grado0}{\renewcommand{\gradeFontSize}{\huge}}
% \DeclareOption{grado1}{\renewcommand{\gradeFontSize}{\LARGE}}
% \DeclareOption{grado2}{\renewcommand{\gradeFontSize}{\Large}}

% Default scaling factor
\newcommand{\myscalefactor}{1}

% Declare options for each grade level, adjusting the scale factor
\DeclareOption{grado0}{\renewcommand{\myscalefactor}{2.0}}  % 200% scale
\DeclareOption{grado1}{\renewcommand{\myscalefactor}{1.7}}  % 170% scale
\DeclareOption{grado2}{\renewcommand{\myscalefactor}{1.5}}  % 150% scale
\DeclareOption{grado3}{\renewcommand{\myscalefactor}{1.3}}  % 130% scale
\DeclareOption{grado4}{\renewcommand{\myscalefactor}{1.1}}  % 110% scale
\DeclareOption{grado5}{\renewcommand{\myscalefactor}{1.0}}  % 100% scale


\DeclareOption*{\PassOptionsToClass{\CurrentOption}{standalone}}
\ProcessOptions\relax


% Separate scaling for each font size category
\newcommand{\setscaledfonts}{
  \pgfmathparse{10 * \myscalefactor}\let\normalsizevalue\pgfmathresult
  \pgfmathparse{12 * \myscalefactor}\let\normalsizebaselineskip\pgfmathresult

  \pgfmathparse{12 * \myscalefactor}\let\largevalue\pgfmathresult
  \pgfmathparse{14 * \myscalefactor}\let\largebaselineskip\pgfmathresult

  \pgfmathparse{14 * \myscalefactor}\let\Largevalue\pgfmathresult
  \pgfmathparse{18 * \myscalefactor}\let\Largebaselineskip\pgfmathresult

  \pgfmathparse{18 * \myscalefactor}\let\LARGEvalue\pgfmathresult
  \pgfmathparse{22 * \myscalefactor}\let\LARGEbaselineskip\pgfmathresult

  \pgfmathparse{24 * \myscalefactor}\let\Hugevalue\pgfmathresult
  \pgfmathparse{30 * \myscalefactor}\let\Hugebaselineskip\pgfmathresult

  \pgfmathparse{9 * \myscalefactor}\let\smallvalue\pgfmathresult
  \pgfmathparse{11 * \myscalefactor}\let\smallbaselineskip\pgfmathresult

  \pgfmathparse{8 * \myscalefactor}\let\footnotesizevalue\pgfmathresult
  \pgfmathparse{9 * \myscalefactor}\let\footnotesizebaselineskip\pgfmathresult

  \pgfmathparse{7 * \myscalefactor}\let\scriptsizevalue\pgfmathresult
  \pgfmathparse{8 * \myscalefactor}\let\scriptsizebaselineskip\pgfmathresult

  \pgfmathparse{5 * \myscalefactor}\let\tinyvalue\pgfmathresult
  \pgfmathparse{6 * \myscalefactor}\let\tinybaselineskip\pgfmathresult

  % Apply the computed sizes
  \renewcommand\normalsize{\fontsize{\normalsizevalue pt}{\normalsizebaselineskip pt}\selectfont}
  \renewcommand\large{\fontsize{\largevalue pt}{\largebaselineskip pt}\selectfont}
  \renewcommand\Large{\fontsize{\Largevalue pt}{\Largebaselineskip pt}\selectfont}
  \renewcommand\LARGE{\fontsize{\LARGEvalue pt}{\LARGEbaselineskip pt}\selectfont}
  \renewcommand\Huge{\fontsize{\Hugevalue pt}{\Hugebaselineskip pt}\selectfont}
  \renewcommand\small{\fontsize{\smallvalue pt}{\smallbaselineskip pt}\selectfont}
  \renewcommand\footnotesize{\fontsize{\footnotesizevalue pt}{\footnotesizebaselineskip pt}\selectfont}
  \renewcommand\scriptsize{\fontsize{\scriptsizevalue pt}{\scriptsizebaselineskip pt}\selectfont}
  \renewcommand\tiny{\fontsize{\tinyvalue pt}{\tinybaselineskip pt}\selectfont}

  % Ensure \normalsize is applied
  \normalsize
}


\AtBeginDocument{%
    \setscaledfonts % Apply the custom font size at the start of the document
}

