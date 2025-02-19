# Crear pdfs de una sola actividad o un solo cool para impresión

**Última actualización:** 18 de Febrero 2025

Instrucciones para crear un PDF de una sola actividad o cool listo para impresión
(con comandos de espaciado, encabezado y pie de página con información de licencia)

### 1. Verificar la actividad para impresión
Asegúrese de que la actividad está lista para impresión (incluyendo comandos de espaciado `whitespace`).

### 2. Confirmar que la actividad hace parte de libro de trabajo
Verifique que la actividad forma parte del libro de trabajo (todos los cools en el momento hacen parte del libro de trabajo).

### 3. Generar el código LaTeX del libro de trabajo
Ejecute el siguiente comando en la terminal (ejemplo con gra3-uni4)
```bash
pretext build gra3-uni4-libroTrabajo
```

### 4. Copiar el script adecuado a la carpeta de output
- Ubique la carpeta de output definida en `project.ptx` (ejemplo: `output/print-latex-libroTrabajo/gra3-uni4`).
- Copie uno de estos scripts según corresponda:
  - Para cool: `extractCool-latexStandalone.py`
  - Para actividad: `extractActivity-latexStandalone.py`

### 5. Identificar el `xml:id` de la actividad o cool
Determine el `xml:id` correspondiente. Por ejemplo: `cool-marcaPartesParaEncontrarArea`.

### 6. Ejecutar el script en la terminal
Diríjase a la carpeta de output y ejecute el comando adecuado:

```bash
python extractCool-latexStandalone.py gra3-uni4.tex cool-marcaPartesParaEncontrarArea 14pt
```

Explicacion del comando:
  - `python extractCool-latexStandalone.py`: Ejecuta el script (use `extractAct-latexStandalone.py` para actividades).
  - `gra3-uni4.tex`: Archivo `.tex` de origen.
  - `cool-marcaPartesParaEncontrarArea`: `xml:id` de la actividad o cool.
  - `14pt`: Tamaño de la fuente del pdf que se va a generar (`14pt` es adecuado para grado 3).

### 7. Revisar el PDF generado
- El script creará un archivo `.tex` y ejecutará `pdfLaTeX` para generar el PDF.
- Revise el PDF y determine si necesita ajustes.

### 8. Ajustar si es necesario
Si se requieren ajustes, decida si deben hacerse en:
- **El archivo fuente `.ptx`**: Requiere regenerar el `.tex` y afectan el libro de trabajo (y posiblemente el libro no rayable y todas las páginas web).
- **El archivo `.tex` local**: Se perderán en futuras regeneraciones y en otras versiones. Evitar en lo posible hacer ajustes de este estilo.

### 9. Guardar el PDF final en la carpeta correspondiente
Cuando el PDF esté listo, muévalo a la carpeta adecuada según corresponda:

- Para **cools:** `source/assets/cool-pdf/`
- Para **actividades:** `source/assets/act-pdf/`

**Nota:** No cambie el nombre del archivo. Esto asegura que el enlace al PDF en las páginas web funcione correctamente.

### 10. Crear enlace para impresión en HTML
Si desea ofrecer un enlace para que los profesores o estudiantes puedan imprimir, use el siguiente código dentro de la actividad. El link estará disponible en la siguiente versión que se genere de las páginas web.
```xml
<aside component="web">
    <p>
       Copia para imprimir y rayar en el libro de trabajo, o
       <url href="external/cool-pdf/cool-marcaPartesParaEncontrarArea.pdf">descargar acá</url>.
    </p>
</aside>
```

### 11. Para crear todos los cools de una unidad.
*  Se extraen los xml:id de los cools en el orden que son del export de latex del libro de trabajo (buscar `begin{project}` y copiar lo que está en los últimos {} de la línea). Por ejemplo, para la unidad 3-4 esto produce los xml:id en el orden en el que aparecen en la unidad:
    ```
    cool-cuantasBolsas
    cool-bolsasManzanas
    cool-regalitosInvitados
    cool-losTromposDe
    cool-patasHormigas
    cool-muffinsEnCajas
    cool-rosasParaCompartir
    cool-hechosMultiplicacionDivision
    cool-encuentraProductoDesconocido
    cool-marcaPartesParaEncontrarArea
    cool-expresionesParaRectangulo
    cool-cualEsElValor
    cool-bolsasFrutasGruposIguales
    cool-multiplicaYExplica
    cool-encontrarArea
    cool-mutiplicarNumsMayores20
    cool-globosGruposIguales
    cool-equiposRecreo
    cool-encuentraElValor
    cool-unaDivisionMas
    cool-manzanasEnLaHuerta
    ```

* Con esa lista en orden se crean todos los comandos de ejecución para crear los pdf de los cools. Por ejemplo:
   ```bash
   python extractCool-latexStandalone.py gra3-uni4.tex cool-bolsasManzanas 14pt && \
   python extractCool-latexStandalone.py gra3-uni4.tex cool-regalitosInvitados 14pt && \
   python extractCool-latexStandalone.py gra3-uni4.tex cool-losTromposDe 14pt && \
   python extractCool-latexStandalone.py gra3-uni4.tex cool-patasHormigas 14pt && \
   python extractCool-latexStandalone.py gra3-uni4.tex cool-muffinsEnCajas 14pt && \
   .....
   ```

*  Estos archivos pdf se revisan y se pasan todos a `source/assets/cool-pdf/` como se describe arriba.

### 12. PENDIENTE: Creación de un paquete zip para descargar de todos los cools de la unidad

Está pendiente ajustar el script `extractCool-latexStandalone.py` para poder agregar parametros de entrada en los que se especifica 3-4-lec# como preambulo al nombre del archivo de salida, para poder producir un zip con archivos de la forma

```
3-4-lec1-cool-cuantasBolsas.pdf
3-4-lec2-cool-bolsasManzanas.pdf
3-4-lec3-cool-regalitosInvitados.pdf
3-4-lec4-cool-losTromposDe.pdf
3-4-lec5-cool-patasHormigas.pdf
3-4-lec6-cool-muffinsEnCajas.pdf
3-4-lec7-cool-rosasParaCompartir.pdf
3-4-lec8-cool-hechosMultiplicacionDivision.pdf
3-4-lec9-cool-encuentraProductoDesconocido.pdf
3-4-lec10-cool-marcaPartesParaEncontrarArea.pdf
3-4-lec11-cool-expresionesParaRectangulo.pdf
....
```

Esto probablemente es mejor hacerlo con el script de `extractCool-latexStandalone.py` (agregar parametros de entrada en los que se especifica `3-4-lec#` como preambulo al nombre del archivo de salida)
