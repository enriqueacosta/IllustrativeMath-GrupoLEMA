# Nombres de archivos

La idea es siempre es seguir el formato de los nombres de los archivos en los templates. Algunos detalles:


*  `lec-VVVVVVV.ptx`, donde `VVVVVVV` es un nombre descriptivo, usualmente muy parecido al título de la lección, usando [camel case](https://en.wikipedia.org/wiki/Camel_case). Ejemplos:
    * `lec-formasDividirNumerosMasGrandes.ptx`
    *  `lec-multiplicarMultiplos10.ptx`
    *  `lec-relacionarMultiplicacionYDivision.ptx` 

* Actividades: `act-RRRRRR-SSSSSS.ptx` en donde `RRRRRR` es opcional y corresponde a alguna rutina recurrente y `SSSSSS` es un nombre descriptivo usando [camel case](https://en.wikipedia.org/wiki/Camel_case). Ejemplos:
   *  `act-planearLaHuerta.ptx`
   *  `act-queSabesDivision.ptx`
   *  `act-cuantosVes-imagenes.ptx` ( [¿cuántos ves?] es una rutina)
   *  `act-conozcamos-bloquesSolidosGeom-construyeVes.ptx` ( [conozcamos] es una actividad de intro al centro, [bloquesSolidosGeom] es el centro, [construyeVes] es el nombre descriptivo que es el nombre de la etapa).

* Calentamientos: `warm-RRRRRR-SSSSSS.ptx`  en donde `RRRRRR` es opcional y corresponde a alguna rutina recurrente y `SSSSSS` es un nombre descriptivo usando [camel case](https://en.wikipedia.org/wiki/Camel_case). Ejemplos:
    *  `warm-observa-cubosEncajables.ptx`, donde [observa] es la rutina [observa y preguntate]
    *  `warm-verdaderoFalso-multiplicarPor10.ptx`, donde [verdaderoFalso] es la rutina [verdadero o falso]
    *  `warm-converNum-enQueSeParecen.ptx`, donde [converNum] es la rutina [Conversación numérica]
    *  `warm-estimacion-multiplicar.ptx`, donde [estimacion] es la rutina [Estmación numérica]
    *  `warm-cuantosVes-Manzanas.ptx`, donde [cuantosVes] es la rutina [¿Cuántos ves?]
    *  `warm-cualDiferente-rectangulos.ptx`, donde [cualDiferente] es la rutina [¿Cuál es diferente?]
    *   `warm-actuemoslo-laHistoriaCambia.ptx`, donde [actuemoslo] es la rutina correspondiente.

* Cool-downs: `cool-SSSSSS.ptx`  en donde `SSSSSS` es un nombre descriptivo usando [camel case](https://en.wikipedia.org/wiki/Camel_case). Ejemplos:
    *  `cool-manzanasEnLaHuerta.ptx`
    *  `cool-regalitosInvitados.ptx`


Los archivos a nivel de unidad siguen el formato  `graVV-uniXX.ptx`, graVV-uniXX-glosario.ptx`, etc. `graVV-uniXX-secYY` por ser muy fijos.


Note que la única referencia al número de una lección es su título, de modo que agregar una lección implica cambios mínimos. Por ejemplo, el archivo `source/content/lec-problemasMult11a19.ptx` corresponde a la lección 13 de la unidad 3-4 y en su encabezado vemos:
```xml
<subsection xml:id="lec-problemasMult11a19" xmlns:xi="http://www.w3.org/2001/XInclude">

<shorttitle>Lección 13</shorttitle>
<title>Lección 13 -<nbsp/></title>
<title>Resolvamos problemas de grupos iguales</title>
```

#  xml:id para todas las actividades, warm, cool, lecciones y secciones que corresponden a las actividades:

Se debe agregar xml:id (labels) a todas las partes que sirva referenciar, como actividades, secciones que contienen todo lo referente a una actividad, lecciones, etc. Esto sebe ser relativamente evidente pues los TEMPLATES identifican claramente donde deb ir el `xml:id`. Por ejemplo:

Todos estos cambios se reflejan en los TEMPLATES. Por ejemplo, para actividades, ahora aparece el lugar en el que hay que agregar el 

Actividad:
```xml
<activity xml:id="act-RRRRRR-SSSSSS" xmlns:xi="http://www.w3.org/2001/XInclude"> 
<title>[@@@@@@@@@]</title>
<statement>
  <p>[@@@@@@@@@]</p>
</statement>
....
```

Lección (encabezado):
```xml
<!-- ============================================ 
  Actividad 1
=================================================  -->
<subsubsection xml:id="lec-VVVVVV-act1">
  <shorttitle>Actividad 1</shorttitle>
  <title>Actividad 1</title>
  <!-- Tiempo en el título que solo ve el profesor -->
  <title component="profesor"><nbsp/>([@@@@@@@@@] mins)</title>

  <!-- Archivo con el contenido -->
  <xi:include href="./act-RRRRRRRRR.ptx"/> 

  <!-- si hay pregunta reto (Are your ready for more), crear el archivo -reto.ptx (usar el template asociado) -->
  <!-- <xi:include href="./act-RRRRRRRRR-reto.ptx"/>  -->
</subsubsection>
....
```

Lección (parte en la que se incluye una actividad --- note la separación entre `lec-VVVVVV-act1` y `act-RRRRRRRRR`):
```xml
<!-- ============================================ 
  Actividad 1
=================================================  -->
<subsubsection xml:id="lec-VVVVVV-act1">
  <shorttitle>Actividad 1</shorttitle>
  <title>Actividad 1</title>
  <!-- Tiempo en el título que solo ve el profesor -->
  <title component="profesor"><nbsp/>([@@@@@@@@@] mins)</title>

  <!-- Archivo con el contenido -->
  <xi:include href="./act-RRRRRRRRR.ptx"/> 

  <!-- si hay pregunta reto (Are your ready for more), crear el archivo -reto.ptx (usar el template asociado) -->
  <!-- <xi:include href="./act-RRRRRRRRR-reto.ptx"/>  -->
</subsubsection>
....
```

Estos xml:id afectan además los nombres de los archivos html que se crean, entonces sirve que sean relativamente descriptivos.

Nivel lección:
*  Los xml:id de las lecciones ahora son `lec-VVVVVV` y corresponden a nombre del archivo.
*  Los xml:id de las distintas partes de la lección ahora son ``lec-VVVVVV-warm`, `lec-VVVVVV-act1`, `lec-VVVVVV-act2`, `lec-VVVVVV-cool` etc. Ojo que estos no son los xml:id de las actividades mismas! Ahora hay una (buena) separación entre las dos cosas.

Nivel actividad
*   xml:id de actividades es `act-RRRRRR` y corresponden a nombre del archivo.

Nivel calentamiento
*   xml:id de calentamientos es `warm-RRRRRR-SSSSSSS` y corresponden a nombre del archivo.

Nivel cool-down
*   xml:id de cierres son `cool-RRRRRR` y corresponden a nombre del archivo.




# ¿Cómo encontrar el archivo de una actividad particular si los archivos no me dicen la ubicación?

La estrategia más fácil es buscar algún texto que sea único con la herramienta de búsqueda en VSCode. En la gran mayoría de los casos es suficiente usar el título de la actividad o lección. El commando de busqueda en VSCode es `cmd+shift+f` (en Mac) y con el título de una actividad normalmente produce un único resultado. Si eso no funciona, buscar <title> seguido sin espacio del titulo seguro da un sólo resultado.

¡Es más rápido que buscar un archivo con un nombre particular!
