# Crear acchivos de una lección

Se deben usar los templates que están en la carpeta `source/TEMPLATES`:
*  `lec-VVVVVV.ptx` --> para las leciones
*  `warm-RRRRRR-SSSSSS.ptx` --> para los calentamientos
*  `act-RRRRRR-SSSSSS.ptx` --> para las actividades
*  `cool-RRRRRR.ptx` --> para los cooldowns (problemas de cierre)

Se deben ajustar todos los xml:id en estos archivos para que correspondan (por ejemplo, cambiar todas las apariciones de `lec-VVVVVV en el archivo `lec-VVVVVV.ptx` por lo que sea que va a ser el xml-id de la lección (hay muchos xml:id compuestos, que empiezan con el xml:id de la lección).

Hay un script que automatiza gran parte de esto. Ver `scripts/create_lesson_files.py`. Este script usa la más reciente versión de los templates para crear los archivos. Ver documentacion adentro del archivo `.py`.