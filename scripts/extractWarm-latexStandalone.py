"""
Enrique Acosta, 2024
Script para extraer bloque \begin{exploration} de output LaTeX de PreTeXt con xml:id dado. 
También reemplaza todos los \includegraphics[width=\linewidth] por \includegraphics[max width=\linewidth, center] para las imágenes.
Output es 
-  archivo .tex que incuye el calentamiento y preambulo LaTeX para compilar y 
-  archivo .pdf de correr pdflatex dos veces en el archivo .tex (para que queden los encabezados bien) 
El preámbulo con el estilo está aparte, en archivo assets/defs-ptxLEMA-latex-standalone.tex, para que sea más modular el sistema.
Sirve para hacer actividades standalone del tex del libroTrabajo con whitespacing.

Uso: python extractWarm-latexStandalone.py <ruta-archivo> <id-actividad> <tamaño-fuente>
     python extractWarm-latexStandalone.py <ruta-archivo> warm-enganchados 14pt
"""

import sys
import re
import subprocess
import os

def extract_activity(file_path, xml_id, font_size):
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

        # Regular expression to match the \begin{exploration} block with the specific id-string
        pattern = re.compile(
            r"\\begin\{exploration\}\{((?:[^{}]|\\{|\\})*)\}\{((?:[^{}]|\\{|\\})*)\}\{" + re.escape(xml_id) + r"\}(.*?)\\end\{exploration\}",
            re.DOTALL
        )

        match = pattern.search(content)
        if match:
            # store full match (group(0) gives the inner match, without the \begin{exploration}...\end{exploration} lines)
            texto_actividad = match.group(0).strip()
            # Save the output to a file named based on the xml_id
            output_file_name = f"{xml_id}.tex"
            with open(output_file_name, "w") as output_file:
                output_file.write("\\documentclass[" + font_size + "]{extarticle}\n")
                output_file.write("\\input{external/defs-ptxLEMA-latex-standalone.tex}\n")
                output_file.write("\\begin{document}\n")
                output_file.write(texto_actividad)
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
            print(f"No exploration found with id '{xml_id}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always return to the original directory
        os.chdir(orig_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extractWarm-latexStandalone.py <file-path> <id-string> <font-size>")
    else:
        file_path = sys.argv[1]
        xml_id = sys.argv[2]
        font_size = sys.argv[3]
        extract_activity(file_path, xml_id, font_size)