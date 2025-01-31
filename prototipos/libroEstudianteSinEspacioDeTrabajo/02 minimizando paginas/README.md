En esta versión se logra un ahorro significativo de páginas.

Diferencias grandes con el prototipo anterior
==============================================

*  Ya no se usan \subsection con los títulos [Calentamiento], [Actividad #], etc encima de las cajas. Ahora esos títulos están dentro del título de la caja, al extremo la derecha.

*  El parskip de enumitem está ahora en 0.9ex (y no en 1ex)

*  Le agregué comandos de espacioado flexible (del estilo [minus 0.5ex]) entre las cajas, para que latex solo tratara de hacer caber más cajas por página reduciendo automáticamente espacio entre las cajas.

*  Uso de \begin{multicosl}{2}....\end{multicols} para ahorrar espacio
   -  Adentro de las cajas, para ahorras espacio (por ejemplo, en muchos calentamientos)
   -  entre cajas, para poner una caja al lado de la otra.

*  Minimizar hasta el nivel de no ser usables las cosas que no se deben rallar (como tablas para rellenar, cuadrículas para colorear) para:
   -  Ahorrar espacio
   -  Indicar de una forma que no esconde el contenido que se debe usar una hoja rallable en otro lado (comparar con el libro del est combo-libroTrabajoYlibroMinimal en el que solo se ponía [Ver libro de trabajo])