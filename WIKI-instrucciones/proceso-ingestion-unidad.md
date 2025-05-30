# Procesos para completar la ingestión de una unidad

1. Creación de archivos de lección, actividades, warms y cools.
   + se usa el sheets `ingestion IM+LEMA (con xml:id)` y el script de python que se creo para crear los archivos con los templates.
   + el sheets mismo tiene una columna que crea el comando que se debe ejecutar en la terminal.
   + un comando para cada lección
2. Ingestión automatizada de cajas simples (launch, synthesis, solutions, narratives)
   + se usan dos scripts que se crearon para esto. Uno que simplifical el HTML original y solo saca esas partes, y uno que pasa esto a los archivos `.ptx` correspondientes que se hicieron en el paso 1.
   + el mismo sheets de ingestión tiene ejemplos de los comandos (son un poco más complejos de generar, sobre todo para grado 0 por lo de K y 0.
   + este proceso también se hace por lección.
3. 
