import re
import sys

# Scale factor for resizing SVG dimensions
SCALE_FACTOR = 1.6

def scale_svg(input_file):
    """
    Scales the width and height of an SVG file by SCALE_FACTOR (1.6).
    Author: Enrique Acosta, November 2024
    
    - Adds ".svg" extension if missing.
    - Saves output as "<filename>-scale13.svg".
    - Handles cases where one or both of `width` and `height` are present:
      - If both are present, both are scaled.
      - If only `width` or only `height` is present, only that attribute is scaled.
      - If neither is present, the SVG is left unchanged.
    """
    # Ensure .svg extension
    if not input_file.endswith(".svg"):
        input_file += ".svg"
    output_file = input_file.replace(".svg", "-scale16.svg")

    # Read the SVG file
    with open(input_file, "r", encoding="utf-8") as file:
        svg_content = file.read()

    # Function to scale the dimension, preserving any units
    def scale_dimension(match):
        value = float(match.group(1))
        unit = match.group(2) or ""
        return f"{value * SCALE_FACTOR}{unit}"

    # Substitute scaled values for width and height, if present
    svg_content = re.sub(
        r'width=["\']([0-9.]+)([a-z%]*)["\']', 
        lambda m: f'width="{scale_dimension(m)}"', 
        svg_content
    )
    svg_content = re.sub(
        r'height=["\']([0-9.]+)([a-z%]*)["\']', 
        lambda m: f'height="{scale_dimension(m)}"', 
        svg_content
    )

    # Write the modified SVG to output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(svg_content)
    print(f"Resized SVG saved as {output_file}")

# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scaleSVGFactor16.py <input-file.svg or input-file>")
    else:
        scale_svg(sys.argv[1])
