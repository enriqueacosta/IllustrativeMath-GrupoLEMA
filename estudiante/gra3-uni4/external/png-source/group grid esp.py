"""
Image Text Replacement Script for Transparent PNGs
---------------------------------------------------

This script replaces specific English text in a transparent PNG image 
with Spanish equivalents while preserving transparency and layout.

Original Texts:
  - "my group"               → "mi grupo"
  - "my partner's group"     → "grupo de mi compañero"

The script works by overlaying semi-transparent rectangles to remove 
the old text, then writing new text in appropriate positions.

Developed with the assistance of ChatGPT (OpenAI)

Enrique Acosta, April 2025
"""

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Load image from same folder as this script
image_path = os.path.join(os.path.dirname(__file__), "group grid.png")
image = Image.open(image_path).convert("RGBA")

# Create editable copy
edited_image = image.copy()
draw = ImageDraw.Draw(edited_image)

# Add transparency rectangles to cover original text (slightly adjusted height)
draw.rectangle((120, 20, 600, 80), fill=(255, 255, 255, 0))    # Cover "my group"
draw.rectangle((960, 20, 1800, 80), fill=(255, 255, 255, 0))   # Cover "my partner's group"

# Try to load a macOS system font
font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"  # Or Helvetica.ttc, or another font
if Path(font_path).exists():
    font = ImageFont.truetype(font_path, 47)
else:
    font = ImageFont.load_default()

# Draw the new Spanish text
draw.text((180, 20), "mi grupo", font=font, fill="black")
draw.text((1020, 20), "grupo de mi compañero", font=font, fill="black")

# Save result in same folder
output_filename = os.path.join(os.path.dirname(__file__), "group grid esp.png")
edited_image.save(output_filename)
print(f"Modified image saved as: {output_filename}")

# Optionally show it (comment out if not using GUI environment)
# plt.imshow(edited_image)
# plt.axis("off")
# plt.title("Modified Image")
# plt.show()
