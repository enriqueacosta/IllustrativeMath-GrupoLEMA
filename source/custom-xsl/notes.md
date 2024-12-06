pretext-common-refsActConLecYAct.xsl
====================================
Para identificar los ajustes, hacer un diff pretext-common.xml

Lo que hace:

*  Crea la funcionalidad: <xref ref="..." title="activity-titles"> usa como texto del link [$grandparent-shorttitle  - $parent-shorttitle] donde: 
    - $parent-shorttitle es el `<shortitle>` de la sección que corresponde a la actividad (entoces el [Actividad #]) y 
    - $grandparent-shorttitle  es el `<shortitle>` de la sección que corresponde a la lección en la que está la actividas (entoces es [Leccion #]).

*  El resultado es un link con un texto como [Lección 9 - Actividad 2]



pretext-common-refsActConLecYAct.xsl
====================================
Es un xsl que funciona ENCIMA de pretext-latex.xsl y que se invoca solo con xsltproc (no con pretext) para generat un archivo .tex standalone de los cools. 

Detalles en el encabezado del archivo mismo.

El script `createStandaloneCools` usa este archivo para generar los .tex y correr pdflatex en cada uno para generar los pdf mismos.