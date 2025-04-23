"""
OCR Phrase Replacement with Spatial Matching and Baseline Alignment
-------------------------------------------------------------------

This script replaces specific English phrases in transparent PNG images with their Spanish equivalents.
It is designed to preserve layout and typographic alignment, even when OCR splits or distorts the text.

Key Features:
-------------
✓ Uses OCR to extract word positions from an image
✓ Detects multi-word phrases spatially (regardless of reading order)
✓ Replaces phrases with mid-aligned Spanish text (like TikZ `mid`)
✓ Maintains horizontal centering over the full phrase region
✓ Preserves image transparency and style

Example:
  "my group"               → "mi grupo"
  "my partner's group"     → "grupo de mi compañero"

Developed with the assistance of ChatGPT (OpenAI)  
Author: Enrique Acosta, April 2025
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pytesseract
import os
import subprocess
import sys

# ---------------- CONFIGURATION ----------------

# Input and output image filenames
image_filename = "group grid.png"
output_filename = "group grid esp.png"

# Phrase replacements (English → Spanish)
# Keys are clean natural phrases, tokenized internally
replacements_raw = {
    "my group": "mi grupo",
    "my partner's group": "grupo de mi compañero"
}

# Font settings (macOS font path shown)
font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
uniform_font_size = 48

# Scale factor for OCR — improves recognition by doubling resolution
scale_factor = 2

# vertical correction offset for replacement texts (negative raises texts)
vertical_correction_offset = -10 


# ----------- TESSERACT INSTALL CHECK (takes care of the OCR) ----------------
def ensure_tesseract_installed():
    try:
        subprocess.run(["tesseract", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ Tesseract OCR is not installed or not found in system PATH.")
        print("Please install it before running this script.\n")
        print("🔧 Installation instructions:")
        print("  • macOS: brew install tesseract")
        print("  • Ubuntu: sudo apt install tesseract-ocr")
        print("  • Windows: https://github.com/tesseract-ocr/tesseract#windows\n")
        sys.exit(1)

ensure_tesseract_installed()

# ------------------- REPLACEMENT OF TEXTS ---------------------------------

# Step 1: Tokenize phrases and sort by length (longest first)
replacements = sorted(
    [(tuple(k.lower().split()), v) for k, v in replacements_raw.items()],
    key=lambda pair: -len(pair[0])
)

# Step 2: Load original transparent image
image_path = os.path.join(os.path.dirname(__file__), image_filename)
original = Image.open(image_path).convert("RGBA")

# Flatten transparency for OCR while preserving original image
background = Image.new("RGB", original.size, (255, 255, 255))
background.paste(original, mask=original.split()[3])

# Step 3: Improve OCR accuracy with enhanced resolution and contrast
resized = background.resize(
    (original.width * scale_factor, original.height * scale_factor),
    resample=Image.Resampling.LANCZOS
)
gray = resized.convert("L")
enhanced = ImageEnhance.Contrast(gray).enhance(3.0)

# Step 4: Extract OCR data (text + position + size)
ocr_data = pytesseract.image_to_data(enhanced, output_type=pytesseract.Output.DICT)
words = []
for i in range(len(ocr_data["text"])):
    word = ocr_data["text"][i].strip().lower()
    if word:
        words.append({
            "text": word,
            "left": ocr_data["left"][i] // scale_factor,
            "top": ocr_data["top"][i] // scale_factor,
            "width": ocr_data["width"][i] // scale_factor,
            "height": ocr_data["height"][i] // scale_factor
        })

# Step 5: Prepare for drawing on the original image
edited = original.copy()
draw = ImageDraw.Draw(edited)

try:
    default_font = ImageFont.truetype(font_path, uniform_font_size)
except:
    default_font = ImageFont.load_default()

# Utility: Get bounding box of a list of words
def bounding_box(group):
    x0 = min(w["left"] for w in group)
    y0 = min(w["top"] for w in group)
    x1 = max(w["left"] + w["width"] for w in group)
    y1 = max(w["top"] + w["height"] for w in group)
    return (x0, y0, x1, y1)

# Step 6: Match and replace phrases
used = set()  # to avoid double-using words

for phrase_tokens, replacement in replacements:
    token_set = set(phrase_tokens)

    for i, wi in enumerate(words):
        if wi["text"] not in token_set or i in used:
            continue

        found = {wi["text"]: i}

        # Search nearby for other words in the phrase
        for j, wj in enumerate(words):
            if j in used or j == i:
                continue
            if wj["text"] in token_set - found.keys():
                dx = abs(wj["left"] - wi["left"])
                dy = abs(wj["top"] - wi["top"])
                if dx < 500 and dy < 60:
                    found[wj["text"]] = j

        # Replace if full phrase is found
        if len(found) == len(token_set):
            group = [words[k] for k in found.values()]
            x0, y0, x1, y1 = bounding_box(group)

            # --- FINAL ALIGNMENT LOGIC ---
            # Vertical: Use midline of the first word for stable baseline placement
            anchor_word = group[0]
            anchor_cy = anchor_word["top"] + anchor_word["height"] // 2

            # Horizontal: Center across the full phrase width
            box_cx = (x0 + x1) // 2

            # Get text size and font metrics
            text_bbox = draw.textbbox((0, 0), replacement, font=default_font)
            text_width = text_bbox[2] - text_bbox[0]
            ascent, descent = default_font.getmetrics()

            # Mid-aligned baseline coordinates with vertical correction
            text_x = box_cx - text_width // 2
            text_y = anchor_cy - ascent // 2 + vertical_correction_offset

            # --- APPLY REPLACEMENT ---
            draw.rectangle([x0 - 5, y0 - 2, x1 + 5, y1 + 2], fill=(255, 255, 255, 0))  # clear
            draw.text((text_x, text_y), replacement, font=default_font, fill="black")  # draw

            print(f"✅ Replaced: {' '.join(w['text'] for w in group)} → {replacement} at ({x0},{y0})")
            used.update(found.values())

# Step 7: Save output
output_path = os.path.join(os.path.dirname(__file__), output_filename)
edited.save(output_path)
print(f"\n✅ Final image saved as: {output_path}")
