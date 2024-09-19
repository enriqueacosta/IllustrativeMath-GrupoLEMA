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
\newcommand{\scalefactor}{1}

% Declare options for each grade level, adjusting the scale factor
\DeclareOption{grado0}{\renewcommand{\scalefactor}{2.0}}  % 200% scale
\DeclareOption{grado1}{\renewcommand{\scalefactor}{1.7}}  % 170% scale
\DeclareOption{grado2}{\renewcommand{\scalefactor}{1.5}}  % 150% scale
\DeclareOption{grado3}{\renewcommand{\scalefactor}{1.3}}  % 130% scale
\DeclareOption{grado4}{\renewcommand{\scalefactor}{1.1}}  % 110% scale
\DeclareOption{grado5}{\renewcommand{\scalefactor}{1.0}}  % 100% scale


\DeclareOption*{\PassOptionsToClass{\CurrentOption}{standalone}}
\ProcessOptions\relax


% Separate scaling for each font size category
\newcommand{\setscaledfonts}{
  \pgfmathparse{10 * \scalefactor}\let\normalsizevalue\pgfmathresult
  \pgfmathparse{12 * \scalefactor}\let\normalsizebaselineskip\pgfmathresult

  \pgfmathparse{12 * \scalefactor}\let\largevalue\pgfmathresult
  \pgfmathparse{14 * \scalefactor}\let\largebaselineskip\pgfmathresult

  \pgfmathparse{14 * \scalefactor}\let\Largevalue\pgfmathresult
  \pgfmathparse{18 * \scalefactor}\let\Largebaselineskip\pgfmathresult

  \pgfmathparse{18 * \scalefactor}\let\LARGEvalue\pgfmathresult
  \pgfmathparse{22 * \scalefactor}\let\LARGEbaselineskip\pgfmathresult

  \pgfmathparse{24 * \scalefactor}\let\Hugevalue\pgfmathresult
  \pgfmathparse{30 * \scalefactor}\let\Hugebaselineskip\pgfmathresult

  \pgfmathparse{9 * \scalefactor}\let\smallvalue\pgfmathresult
  \pgfmathparse{11 * \scalefactor}\let\smallbaselineskip\pgfmathresult

  \pgfmathparse{8 * \scalefactor}\let\footnotesizevalue\pgfmathresult
  \pgfmathparse{9 * \scalefactor}\let\footnotesizebaselineskip\pgfmathresult

  \pgfmathparse{7 * \scalefactor}\let\scriptsizevalue\pgfmathresult
  \pgfmathparse{8 * \scalefactor}\let\scriptsizebaselineskip\pgfmathresult

  \pgfmathparse{5 * \scalefactor}\let\tinyvalue\pgfmathresult
  \pgfmathparse{6 * \scalefactor}\let\tinybaselineskip\pgfmathresult

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

