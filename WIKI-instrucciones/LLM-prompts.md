## Sin traducir, limpiar HTML de launch, activity, synthesis, narrative 

```
Clean up this html by:
*  removing the em tags.
*  in the LI with english and Spanish, just keep the Spanish before the "//"
*  changing quote symbols with <q>....</q>
```

## Ingestar launch, activity instructions, lesson synthesis con cursor
(probado con Claude Sonnet 3.7 en Marzo 2025)

Gererar el HTML "limpio" con esa info del lesson.html usando el script `extract_HTML_launch_synthesis_instructions.py` con commando:
```
python extract_HTML_launch_synthesis_instructions.py lesson.html --no-raw-html --strip-qtags
```

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

## Traducir toda una lección (cursor agent)
Abrir el archivo de la lección y empezar el chat (agent) con
```
You are an XML and language processing assistant specializing in trasnlating to Spanish xml files. 

Input Structure:
You will receive XML files  as input with xi:include files that must also be processes. These files contain structured text within tags such as <statement>, <solution>, <prelude>, and <postlude>. Some tags may contain additional attributes or nested tags.

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
