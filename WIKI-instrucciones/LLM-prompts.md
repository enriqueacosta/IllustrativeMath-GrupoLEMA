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
```

Para quitar las líneas con ####:
```
quita las lineas con <p>#############</p>
```

Para una versión más limpia de los textos largos (narative), usar 
```
Haz que el español sea más corto, más fluido, y más fácil de entender.
```

Despues reemplazar el xml de la actividad en VSCode, gaurdar, y mirar el diff de control de cambios para asegurarse que no se cambió nada que no tocaba. Se puede editar sobre el diff mismo.
