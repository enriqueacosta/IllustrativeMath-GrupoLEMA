# Procesos para completar la ingestión de una unidad

Enrique Acosta, 2025

1. Creación de archivos de lección, actividades, warms y cools.
   + se usa el sheets `ingestion IM+LEMA (con xml:id)` y el script de python que se creo para crear los archivos con los templates.
   + el sheets mismo tiene una columna que crea el comando que se debe ejecutar en la terminal.
   + un comando para cada lección
2. Ingestión automatizada de campos simples (launch, synthesis, solutions, narratives)
   + se usan dos scripts que se crearon para esto. Uno que simplifical el HTML original y solo saca esas partes, y uno que pasa esto a los archivos `.ptx` correspondientes que se hicieron en el paso 1.
   + el mismo sheets de ingestión tiene ejemplos de los comandos (son un poco más complejos de generar, sobre todo para grado 0 por lo de K y 0.
   + este proceso también se hace por lección.
   + los campos ingestados quedan en Spanglish, con marca `[+++++++++++++]` para indicar que se ingestaron pero falta traducción. Todos los otros campos no ingestados quedan con `[@@@@@@@@@]` (así vienen los archivos).
3. Finalizacción de ingestión (salvo materiales) y revisión de la ingestión automatizada
   + Los campos que faltan se hacen a mano (todos los `[@@@@@@@@@]`).
   + Hay varios en las lecciones (statements, sobre todo)
   + Tambien PPs y lesson summaries. Para los PPs hay que hacer los archivos a partir de los templates.
   + Por lo general, todos estos involucran imágenes (que hay que guardar en lugares particulares e insertar con los tags de <image> apropiados) y trabajo "de diagramación" con formatos de varias columnas, combinaciones de imágenes y textos, ajustes de imágenes, creaciones de tablas, textos de matemáticas, etc.
   + Se debe revisar todo lo que quedó ingestado automático de las lecciones del paso anterior, y arreglar.
   + Después de este paso, los únicos `[@@@@@@@@@]` que deberían quedar son los de materiales requeridos.
4. Ingestíon de materiales. Para cada lección
   + Creación de archivos `-mat.ptx` y `-matCentros.ptx` para todas las actividades que los necesitan.
   + OJO. El contenido de `mat.ptx` combina los contenidos de `Required Materials` y `Required Preparation`. Ver gra0-uni2 para ver ejemplos. En cada viñeta se lista el material Y la cantidad necesaria para el número de estudiantes especificado.
   + insertar los llamados a estos archivos `-mat` en el archivo `.ptx` de la actividad correspondiente, y en el archivo de resumen de materiales de la lección, en el archivo `lec-*.ptx`
   + Creacion de archivos `blm` para cada blm, con los templates apropiados (hay uno para blm de centros y otro para no centros). Son varios pasos, que involucran:
      -  hacer todas las referencias apropiadas,
      -  guardar los pdf de los blm,
      -  crear thumbnails png con (`magic -density 150 ...`),
      -  etc.
      -  hay que asegurarse que la lista de materiales en la que se usa el blm está actualizada. Una forma rápida de hacer esto "a mano" es b uscar el xml:id del blm, para ver en que archivos `-mat` se menciona. 
   + Creación de archivos `centro` para cada centro que se usa en la unidad con los templates apropiados. Son varios pasos, que involucran:
      -  identificar la etapa que se va ha hacer y crear las líneas correspondientes en el archivo
      -  hacer todas las referencias apropiadas (e todas las direcciones)
      -  buscar en los textos `[++++++++]` las menciones de que los estudiantes van a concocer o retomar un centro y crear referencias apropiadas. Ejemplo ver act-conozcamos-historiasMatematicas-cuantos.ptx
5. Identificar actividades que no funcionan solo web (porque necesitan ser rayables) y crear versiones pdf de las acrivades para que se puedan descargar e imprmir.
   +  Se debe cambiar el componente de la actividad en el archivo lección a `acts-rayable`. Eso hace que aparezca en el output de libro de trabajo.
   +  Se deben ajustar las partes del enunciado que deberían aparecer en las componentes `libroTrabajo` y `no-libroTrabajo` y con un `aside`, se crea un link al pdf que se va a crear (en `assets/act-pdf`).
   +  Se genera el output libro de trabajo de latex y se usa el script que genera el pdf de la actividad `extractActivity-latexStandalone.py`
   +  Se ajusta de ser necesario el pdf de la actividad (con el latex standalone que se creo)
6. Generación de versiones pdf de los cools para la web (para imprimir).
   +  Con el script correspondiente. Se deben guardar en `assets/cool-pdf`

# fase de traducción
7. Traducción de las lecciónes
   +  todos los textos en ENG de los archivos `.ptx` de la lección
   +  Arreglar BLMs que tiene textos en ENG
   +  cración de imagenes en ENG si no están disponibles (por ejemplo, por ser soluciones)
