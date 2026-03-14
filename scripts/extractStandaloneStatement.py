"""
Enrique Acosta, 2024

Script para extraer un bloque de enunciado del output LaTeX de PreTeXt con xml:id dado.
Sirve para hacer los pdf de act- y cool- a partir del tex del libroTrabajo con whitespacing.

El tipo de bloque se detecta automáticamente del prefijo del xml:id:
- act-  → bloque begin{activity}
- cool- → bloque begin{project}

Input es:
- <ruta-archivo>: la ruta al archivo .tex del libroTrabajo de una unidad,
    que se genera, por ejemplo con `pretext build gra3-uni2-libroTrabajo`.

Output es:
-  archivo .tex que incluye solo el enunciado del act- o cool- y preámbulo LaTeX para compilar y
-  archivo .pdf de correr pdflatex dos veces en el archivo .tex (para que queden los encabezados bien)

El preámbulo con el estilo para el latex se carga de un archivo aparte: assets/preamble-latex-standalone.tex,
Esto permite que sea más modular el sistema.

Nota: el script reemplaza todos los includegraphics[width=linewidth] por
includegraphics[max width=\\linewidth, center] para corregir el tamaño de las imágenes y centrarlas.


Uso: python extractStandaloneStatement.py <ruta-archivo> <xml:id> <tamaño-fuente>
     python extractStandaloneStatement.py <ruta-archivo> act-contarImagenes 14pt
     python extractStandaloneStatement.py <ruta-archivo> cool-pesoCirculo 14pt
"""

import sys
import re
import subprocess
import os

def extract_statement(file_path, xml_id, font_size):
    # Detect block type from xml:id prefix
    if xml_id.startswith("act-"):
        block_type = "activity"
    elif xml_id.startswith("cool-"):
        block_type = "project"
    else:
        print(f"Error: xml:id '{xml_id}' debe empezar con 'act-' o 'cool-'")
        sys.exit(1)

    preamble_file = "external/preamble-latex-standalone.tex"

    # Get the absolute path to the input file and its containing folder
    abs_file_path = os.path.abspath(file_path)
    work_dir = os.path.dirname(abs_file_path)
    file_name = os.path.basename(abs_file_path)

    # Save the current working directory
    orig_dir = os.getcwd()

    try:
        # Change to the directory with the LaTeX file
        os.chdir(work_dir)

        # Read the content of the LaTeX input file
        with open(file_name, 'r') as file:
            content = file.read()

        # Regular expression to match the block with the specific id-string
        pattern = re.compile(
            r"\\begin\{" + block_type + r"\}\{((?:[^{}]|\\{|\\})*)\}\{((?:[^{}]|\\{|\\})*)\}\{" + re.escape(xml_id) + r"\}(.*?)\\end\{" + block_type + r"\}",
            re.DOTALL
        )

        match = pattern.search(content)
        if match:
            # store full match
            texto = match.group(0).strip()
            # Save the output to a file named based on the xml_id
            output_file_name = f"{xml_id}.tex"
            with open(output_file_name, "w") as output_file:
                output_file.write("\\documentclass[" + font_size + "]{extarticle}\n")
                output_file.write("\\input{" + preamble_file + "}\n")
                output_file.write("\\begin{document}\n")
                output_file.write(texto)
                output_file.write("\n\\end{document}")

            # Post-processing:
            # Replace \includegraphics[width=\linewidth] with \includegraphics[max width=\linewidth, center]
            with open(output_file_name, "r") as output_file:
                file_content = output_file.read()
            modified_content = re.sub(
                r"\\includegraphics\[width=\\linewidth\]",
                r"\\includegraphics[max width=\\linewidth, center]",
                file_content
            )
            # Write the modified content back to the file
            with open(output_file_name, "w") as output_file:
                output_file.write(modified_content)

            # Run pdflatex twice on the file
            try:
                subprocess.run(["pdflatex", output_file_name], check=True)
                subprocess.run(["pdflatex", output_file_name], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running pdflatex: {e}")
                return

            print(f"Output saved to '{os.path.abspath(output_file_name)}'")
        else:
            print(f"No se encontró '{block_type}' con id '{xml_id}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always return to the original directory
        os.chdir(orig_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extractStandaloneStatement.py <file-path> <xml:id> <font-size>")
        print("       xml:id must start with 'act-' or 'cool-'")
    else:
        file_path = sys.argv[1]
        xml_id = sys.argv[2]
        font_size = sys.argv[3]
        extract_statement(file_path, xml_id, font_size)
