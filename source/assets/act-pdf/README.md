# Generación de PDFs de Actividades

Este proceso permite generar archivos PDF para actividades específicas a partir de los archivos fuente `act-*.ptx`, eliminando textos duplicados y asegurando consistencia.

## Pasos para generar un PDF de una actividad:

### 1. Generar el archivo LaTeX del libro de trabajo de la unidad correspondiente.
Usar el comando siguiente, reemplazando `gra3-uni4-libroTrabajo` con el nombre del libro de trabajo que se va a generar:

```bash
pretext build gra3-uni4-libroTrabajo
```

Esto genera un archivo lates que incluye comandos de whitespace y posibles comentarios para el diagramador.

### 2. Extraer la actividad con el script de Python.
Ejecutar el script `extractActivity-latexStandalone.py` en la carpeta donde se generaron los archivos LaTeX (normalmente ubicada en `output/libroTrabajo/<unidad>`). Por ejemplo:

```bash
python extractActivity-latexStandalone.py gra3-uni4.tex act-siSeQueEntoncesSeQue 14pt
```

**Parámetros del comando:**
- `gra3-uni4.tex`: Nombre del archivo LaTeX del libro de trabajo correspondiente.
- `act-siSeQueEntoncesSeQue`: El `xml:id` de la actividad que deseas extraer. **Nota:** Esto no es el nombre del archivo, aunque a veces pueden coincidir.
- `14pt`: Tamaño de la fuente para el PDF generado. Esto depende del grado escolar.

### 3. Ubicación del script
El script `extractActivity-latexStandalone.py` está en la carpeta `SCRIPTS`. En algunos casos, es posible que toque copiarlo a la carpeta de salida (`output`) antes de ejecutarlo.
