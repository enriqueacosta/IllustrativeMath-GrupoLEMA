# Problemas de práctica

## Template
Todos los problemas de práctica usan el template `PP-HHHHHHHHHHHHHHHH.ptx`.

El HHHHHHHHHHHHHHHH es un UUIID que se genera automáticamente al crear el archivo `.ptx` y que no se puede cambiar (para evitar conflictos). Para generar un UUID usar el script `generate_pp_code.py` en la carpeta `SCRIPTS`


## Alineación de los PPs

Los PPs puede estar alineados con una lección, o con una sección. Después, pueden aparecer en su lección, en otra lección distinta, o en un conglomerado de sección (como en K-5). Ejemplo:

<img width="600" alt="Screenshot 2024-11-26 at 10 50 40 AM" src="https://github.com/user-attachments/assets/e63ac338-2c8e-4c4c-a8e2-484b8846b313">

Al crea los `.ptx` se debe tener en cuenta esta alineación y marcarla claramente en el tag `<title component="metadata>`. Ver el template `PP-HHHHHHHHHHHHHHHH.ptx`.
   
## Como incluir los PPs

Los PPs aparecen a nivel de sección para K-5, y a nivel de lección para 6-8.

### Para K-5:
*  Todos los PPs se cargan en un archivo `.ptx` a nivel de sección. El template es `graVV-uniXX-secYY-ProblemasPractica.ptx`


### Para 6-8:
*  Los PPs aparecen a nivel de lección y se incluyen directamente en el `.ptx` de la lección. Pueden estar alineados con esa lección, o con otra. 


