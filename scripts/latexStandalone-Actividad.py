"""
Enrique Acosta, 2024
Script para extraer un bloque \begin{activity} específico de un archivo LaTeX basado en un id único y generar un archivo .tex independiente con el contenido de la actividad. 
Sirve para hacer actividades standalone del tex del libroTrabajo con whitespacing.
Uso: python crearActividad.py <ruta-archivo> <id-actividad> <tamaño-fuente>

Pendiente: posiblemente cambiar los "includegraphics[width=\line width]" a  "includegraphics[max width=\line width, center]", porque en este momento toca ajustar esto a mano.
"""

import sys
import re

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
            texto_actividad = match.group(0).strip()
            # Save the output to a file named based on the activity_id
            output_file_name = f"{activity_id}.tex"
            with open(output_file_name, "w") as output_file:
                output_file.write("\\documentclass[" + font_size + "]{extarticle}\n")
                output_file.write("\\input{external/defs-ptxLEMA-latex-standalone.tex}\n")
                output_file.write("\\begin{document}\n")
                output_file.write(texto_actividad)
                output_file.write("\n\\end{document}")
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
