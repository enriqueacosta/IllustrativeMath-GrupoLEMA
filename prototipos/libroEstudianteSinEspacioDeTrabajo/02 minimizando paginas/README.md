En esta versión se logra un ahorro significativo de páginas.

Diferencias grandes con el prototipo anterior
==============================================

*  Ya no se usan \subsection con los títulos [Calentamiento], [Actividad #], etc encima de las cajas. Ahora esos títulos están dentro del título de la caja, al extremo la derecha.

*  El parskip de enumitem está ahora en 0.9ex (y no en 1ex)

*  Le agregué comandos de espaciado flexible (del estilo [minus 0.5ex]) entre las cajas, para que latex por sí solo intentara hacer caber más cajas por página reduciendo de ser necesario el espacio entre las cajas.

*  Uso de \begin{multicosl}{2}....\end{multicols} para ahorrar espacio
   -  Adentro de las cajas, para ahorras espacio (por ejemplo, en muchos calentamientos)
   -  entre cajas, para poner una caja al lado de la otra.

*  Minimizar hasta el nivel de no ser utilizables las cosas que no se deben rallar (como tablas para rellenar, cuadrículas para colorear) para:
   -  Ahorrar espacio
   -  Indicar de una forma que no esconde el contenido que se debe usar una hoja rayable en otro lado (comparar con el libro del est combo-libroTrabajoYlibroMinimal en el que solo se ponía [Ver libro de trabajo])


Libro BLM minimal
==================
La carpeta [LibroBLM-minimal] tiene prototipos del libro mínimo del BLM (actividades que hay que rayar y BLMs que hay que recortar o rayar.
*  `gra3-uni4-libroTrabajoMinimal` tiene todo en orden, parecido al combo `combo-libroTrabajoYlibroMinimal`
*  `gra3-uni4-libroTrabajoMinimal-BLMAlFinal` tiene comandos de latex especiales que permiten enviar páginas para rectorar al final del documento sin tener que pasar su código al final.

Estos dos archivos se crearon muy "a mano", borrando partes del output del libroDeTrabajo actual hasta que quedara unicamente lo que era imprescindible imprimir.