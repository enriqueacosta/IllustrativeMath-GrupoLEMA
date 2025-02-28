## Sin traducir, limpiar HTML de launch, activity, synthesis, narrative 

```
Clean up this html by:
*  removing the em tags.
*  in the LI with english and Spanish, just keep the Spanish before the "//"
*  changing quote symbols with <q>....</q>
```

## Traducir una actividad
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
