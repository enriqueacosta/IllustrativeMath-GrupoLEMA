"""
Enrique Acosta, 2024
Script para extraer bloque \begin{activity} de output LaTeX de PreTeXt con xml:id dado. 
También reemplaza todos los \includegraphics[width=\linewidth] por \includegraphics[max width=\linewidth, center] para las imágenes.
Output es 
-  archivo .tex que incuye actividad y preambulo LaTeX para compilar y 
-  archivo .pdf de correr pdflatex dos veces en el archivo .tex (para que queden los encabezados bien) 
El preámbulo con el estilo está aparte, en archivo assets/defs-ptxLEMA-latex-standalone.tex, para que sea más modular el sistema.
Sirve para hacer actividades standalone del tex del libroTrabajo con whitespacing.

Uso: python extractActivity-latexStandalone.py <ruta-archivo> <id-actividad> <tamaño-fuente>
"""

import sys
import re
import subprocess

def extract_activity(file_path, activity_id, font_size):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Regular expression to match the \begin{activity} block with the specific id-string
        pattern = re.compile(
            r"\\begin\{activity\}\{[^\}]*\}\{[^\}]*\}\{" + re.escape(activity_id) + r"\}(.*?)\\end\{activity\}",
            re.DOTALL
        )

        match = pattern.search(content)
        if match:
            # store full match (group(1) gives the inner match, without the \begin{activity}...\end{activity} lines)
            texto_actividad = match.group(0).strip()
            # Save the output to a file named based on the activity_id
            output_file_name = f"{activity_id}.tex"
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
            
            print(f"Output saved to '{output_file_name}'")
        else:
            print(f"No activity found with id '{activity_id}'")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python crearActividad.py <file-path> <id-string> <font-size>")
    else:
        file_path = sys.argv[1]
        activity_id = sys.argv[2]
        font_size = sys.argv[3]
        extract_activity(file_path, activity_id, font_size)
