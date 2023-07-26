# IllustrativeMath-GrupoLEMA

Prototipo del material de [Matemáticas Ilustrativas](https://curriculum.illustrativemathematics.org) en versión [Pretext](https://pretextbook.org).

## Para generar versiones web(html), pdf, latex

Debe tener [Pretext](https://pretextbook.org) instalado. Desde la terminal, en una carpeta de unidad (que contenga un archivo `project.ptx`), ejecutar los siguientes comandos.

Todos los archivos que se generan se guardan en la carpeta `output/`.

### Versiones del estudiante

Para generar la página web:

```bash
pretext build web-est
```

Para ver localmente la página web:

```bash
pretext view web-est
```

Para ver una versión local de la página que se actualiza automáticamente con cambios:

```bash
pretext view -w web-est
```

Para generar el pdf:

```bash
pretext build print-est
```

Para generar el código latex que produce el pdf:

```bash
pretext build print-latex-est
```

### Versiones del profesor

Cambiar `-est` por `-prof` en todos los comandos.

Ambas versiones (estudiante y profesor) se generan a partir de los mismos archivos fuente. Los elementos que contienen `component="profesor"` solo son visibles en la versión del profesor.

## Licencia

Mientras se descifran los detalles de copyright y licencias, este material es ©Enrique Acosta ([enriqueacosta.github.io](https://enriqueacosta.github.io)) y se publica bajo una licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY NC 4.0). En breve e incompleto (los detalles están en las licencias), **tiene toda libertad para adaptar, copiar y distribuir este material siempre y cuando no lo use para fines comerciales y le mantenga la misma licencia y dé la atribución correspondiente (mencione al Grupo LEMA(www.grupolema.org) y a Illustrative Mathematics)** . 

Ver una copia de la licencia en [creativecommons.org](https://creativecommons.org/licenses/by-nc/4.0/"/).

Adaptado de IM K–5 Math v.I, © 2021 Illustrative Mathematics® [illustrativemathematics.org](https://curriculum.illustrativemathematics.org) en su versión en español en [im.kendallhunt.com](https://im.kendallhunt.com/K5_ES/curriculum.html), distribuido con una licencia Creative Commons Attribution 4.0 International License (CC BY 4.0). Ver detalles de esta licencia en https://creativecommons.org/licenses/by/4.0/.

Soluciones en español adaptadas de Open Up Resources © 2022, [openupresources.org](https://access.openupresources.org/curricula/our-k5-math). Publicadas bajo una licencia Creative Commons Attribution-NonCommercial 4.0 International license.

**Nota:** Las traducciones anteriormente mencionadas fueron lideradas y coordinadas por miembros del Grupo LEMA. Ver detalles en: [illustrativemathematics.org](https://curriculum.illustrativemathematics.org/k5/teachers/grade-1/course-guide/contributors.html).

