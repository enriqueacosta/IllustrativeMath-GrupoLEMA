import numpy as np
import svgwrite
from PIL import Image
import os

# Load the image
image_path = "barra-colorGrupoLEMA-OLD.png"  # Replace with your image file path
image = Image.open(image_path)

# Target number of bars
num_bars = 500

# Dimensions of the original image
width, height = image.size

# Calculate bar width and adjust slightly to avoid gaps
bar_width = width / num_bars
adjusted_bar_width = bar_width * 1.01  # Increase width slightly to eliminate gaps

# Sample colors evenly from the original image
pixels = np.array(image)
sampled_colors = pixels[:, ::pixels.shape[1] // num_bars][:, :num_bars]

# Create an SVG drawing
svg_output_path = "barra-colorGrupoLEMA.svg"  # Output file name
dwg = svgwrite.Drawing(svg_output_path, size=(width, height))

# Add vertical bars to the SVG
for i in range(num_bars):
    # Sample a representative color for each bar
    bar_color = sampled_colors[0, i]  # Use the first row for simplicity
    color_hex = f'#{bar_color[0]:02x}{bar_color[1]:02x}{bar_color[2]:02x}'

    # Calculate bar position and add it to the SVG
    x_start = i * bar_width  # Original position remains
    dwg.add(dwg.rect(insert=(x_start, 0),
                     size=(adjusted_bar_width, height),
                     fill=color_hex))

# Save the SVG file
dwg.save()

print(f"SVG file saved to: {svg_output_path}")

# Convert the SVG to PDF using rsvg-convert
pdf_output_path = "barra-colorGrupoLEMA.pdf"
os.system(f"rsvg-convert --format=pdf {svg_output_path} > {pdf_output_path}")

print(f"PDF file saved to: {pdf_output_path}")
