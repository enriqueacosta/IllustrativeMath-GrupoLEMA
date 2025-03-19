## Sin traducir, limpiar HTML de launch, activity, synthesis, narrative 

```
Clean up this html by:
*  removing the em tags.
*  in the LI with english and Spanish, just keep the Spanish before the "//"
*  changing quote symbols with <q>....</q>
```

## Poner los decimales en \num{....}
```
Please warp all  numbers that have decimal periods with \num{} in all the .ptx files in this folder. Do not make any other changes. 

Examples:
*  <m> 3x + 14.56 +10 = 13.45 </m> --- > <m> 3x + \num{14.56} +10 = \num{13.45} </m>
*  <m>1200.532 \unit{mg}</m> ---> <m>\num{1200.532} \unit{mg}</m>
*  x+ \frac{45.321}{0.1}  ---> x+ \frac{\num{45.321}}{\num{0.1}}
```

## Ingestar launch, activity instructions, activity synthesis, lesson purpose, reflection questions con python

Gererar el HTML "limpio" con esa info del lesson.html usando el script `extract_HTML_launch_synthesis_instructions.py` con commando:
```
python extract_HTML_lesson_and_preparation.py <path a lesson.html y preparation.html> --no-raw-html --strip-qtags
```

Después, usar el script `ingest_simple_lesson_content.py` para ingerir todo. Este script lo generó cursor y es posible que a veces no funciona 100 bien. Si no funciona, ver siguoente sección.




## Ingestar launch, activity instructions, activity synthesis con cursor
(probado con Claude Sonnet 3.7 en Marzo 2025)

Gererar el HTML "limpio" con esa info del lesson.html usando el script `extract_HTML_launch_synthesis_instructions.py` con commando:
```
python extract_HTML_launch_synthesis_instructions.py lesson.html --no-raw-html --strip-qtags
```

Después, usar el script `ingest_launch_synthesis_instructions_content.py` para ingerir todo. Este script lo generó cursor y es posible que a veces no funciona 100 bien. Si no funciona, usar el chat de cursor como describo abajo.

Después, en Cursor, en el chat en modo `edit` poner la `lec-*.ptx` en el contexto y decir esto:

```
This xml lesson plan file has several xi:include for each activity or warm-up. Please paste the following content in the right places in each of the files. There are placeholders @@@@@ in the places where it must go. 

Note that the <h3> headings give the "ref=" which indicates the right place in each activity file, so it should replace those @@@@@. 

General instructions:
* Do not change the xml you are pasting in.
* Do not change the xml if the files in which you pasting in except for replacing the @@@@@@@@ by the corresponding content.
*  Do not change any <p>[@@@@@@@@]</p> that you don't replace to <p></p>
*  Do not invent content for the "materiales" section.
*  Please indent appropriately the code you pasted

Here is the content:

<<pegar el código HTML directamente>>

```


## Traducir una actividad (GPT)
Instrucciones iniciales en en chat:
```
You are an XML and language processing assistant specializing in <activity> files. Your primary tasks are to activities to Spanish.

Input Structure:
You will receive XML <activity> files as input. These files contain structured text within tags such as <statement>, <solution>, <prelude>, and <postlude>. Some tags may contain additional attributes or nested tags.

Tasks:
Maintain structural integrity of the XML.
Use formal Spanish ("usted") for teacher-facing content.
Use informal Spanish ("tú") for student-facing content.
Comment out the English that got translated. The original English must not be lost.
Do not add comments for parts that are already in Spanish.
```

Para ajustar traduciones de terminos (se ajustan los textos en toda la actividad) :
```
Ajusta estas estas traducciones:
quiet think time --> tiempo para pensar en silencio
geoblock --> bloque sólido geométrico
partner discussion --> discusión en pareja
independent work time --> tiempo de trabajo individual
```
(ver mini GLO abajo)

Para quitar las líneas con ####:
```
quita las lineas con <p>#############</p>
```

Para una versión más limpia de los textos largos (narative), usar 
```
Haz que el español sea más corto, más fluido, y más fácil de entender.
```

Despues reemplazar el xml de la actividad en VSCode, gaurdar, y mirar el diff de control de cambios para asegurarse que no se cambió nada que no tocaba. Se puede editar sobre el diff mismo.

## Traducir toda una lección (cursor chat mode agent)
Abrir el archivo de la lección y empezar el chat en modo `agent` (no `edit` ni `ask`) con
```
You are an XML and language processing assistant specializing in translating xml files to Spanish.

Input Structure:
You will receive XML files as input with xi:include files that must also be processesed. These files contain structured text within tags such as <statement>, <solution>, <prelude>, and <postlude>. Some tags may contain additional attributes or nested tags.

Tasks:
Maintain structural integrity of the XML.
Use formal Spanish ("usted") for teacher-facing content.
Use informal Spanish ("tú") for student-facing content.
Comment out the English that got translated. The original English must not be lost.
Do not add comments for parts that are already in Spanish.
```
si no traduce las actividades, insistir:
```
you did not follow the xi:inlcude files to make edits there
```

Despues, ajustar la traducción en toda la lección:
```
Ajusta estas estas traducciones en todos los archivos que estas editando:
Sample responses > Ejemplos de respuestas
.
.
.
```

## mini-GLO de launch, Activity instructions, synthesis

Instrucciones de da el profesor:
```
consider > considere
quiet think time > tiempo para pensar en silencio
independent > individual
shape > figura
monitor for students > identifique a los estudiantes
were introduced > se le presentó
encourage > motívelos
flash > muestre rápidamente
display > muestre
solved > resolvieron
share > repartir
did you say > dijo
elicit > generar
tell students > diga a los estudiantes
teacher > profesor
invite students > invite a los estudiantes
sentence frame > esquema de oración
partner discussion > discusión en pareja
classroom > salón de clase
revisit > retome
```

Objetos:
```
blackline master > hoja reproducible
poster > póster
connecting cube > cubo encajable
array > arreglo
equal size > igual tamaño
counter > ficha
visual display > presentación visual
pattern block > ficha geométrica
5-frame > tablero de 5
number mat > tablero de números
geoblock > bloque sólido geométrico
number cube > dado numérico
```

Rutinas:
```
gallery walk > Recorrido por el salón
what is the same and what is different > en qué se parecen y en qué son diferentes
Which One Doesn’t Belong > ¿Cuál es diferente?
```

Otros:
```
warm-up > actividad de calentamiento
cool-down > actividad de cierre
Checkpoint > Punto de chequeo
Sample responses > Ejemplos de respuestas
matches > corresponde a
match > emparejan
perpendicular bisector > mediatriz
move between centers > pasar de un centro a otro
classroom > salón de clase
```

A veces:
```
introduced > que se presentaron
monitor for > identifique a
move between centers > pasar de un centro a otro
```

## Arreglar todos decimales para que queden adentro de \num{} para una unidad.

En cursor, poner la carpeta de la unidad en el contexto del chat, y en modo agente:
```
Please warp all  numbers that have decimal periods with \num{} in all the .ptx files in this folder. Do not make any other changes. 

Examples:
*  <m> 3x + 14.56 +10 = 13.45 </m> --- > <m> 3x + \num{14.56} +10 = \num{13.45} </m>
*   <m>1200.532 \unit{mg}</m> ---> <m>\num{1200.532} \unit{mg}</m>
*  x+ \frac{45.321}{0.1}  ---> x+ \frac{\num{45.321}}{\num{0.1}}
```
