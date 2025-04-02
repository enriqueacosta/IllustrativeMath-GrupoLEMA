## para agregar hojas al final para recortar:

Se usa con `\begin{cutoutpage}....\end{cutoutpage}` para cada hoja que se recorta. 

Si se necesitan varias páginas, usar `\cleardoublepage` internamente (eso propduce una hoja en blanco atrás).

```latex
% Define cutoutpage environment with an optional argument for the header or footer
\NewDocumentEnvironment{cutoutpage}{O{}+b} % O{} = optional argument, +b = block
  {
    % Append cutout page content with a header or footer customization command
    \gappto\cutoutpages{%
      \cleardoublepage
      \fancypagestyle{cutoutstyle}{% Define a temporary style
        \fancyhead[C]{\vspace*{1cm}\small #1\hrule} % Use the provided header or footer text
        \fancyfoot[C]{} % Use the provided header or footer text
      }
      \pagestyle{cutoutstyle} % Apply the new header or footer style
      #2\par % Content of the cutout page
    }
    Hojas para recortar al final del libro.
  }
  {}

% Append all stored cutout pages at the end of the document
\AfterEndDocument{%
  \vspace*{8cm}
  {\Huge HOJAS PARA RECORTAR}
  \cleardoublepage
  \cutoutpages
  \cleardoublepage
}
```