import re
import sys

FRAME_WIDTH = 1  # pt

def add_frame(input_file, padding=0):
    """
    Adds a 1pt frame around the content of a dvisvgm-generated SVG file.
    Author: Enrique Acosta, April 2026

    - Adds ".svg" extension if missing.
    - Saves output as "<filename>-framed.svg".
    - Optional padding adds space between content and frame.
    - Expands viewBox to accommodate padding + half stroke-width on each side.
    - Inserts a <rect> element to draw the frame.

    NOTE: Padding is in pt. This works correctly for dvisvgm-generated SVGs
    because dvisvgm sets width/height in pt and the viewBox dimensions match,
    so 1 viewBox unit = 1pt. Do not use this script on SVGs where the viewBox
    units differ from pt.
    """
    if not input_file.endswith(".svg"):
        input_file += ".svg"
    output_file = input_file.replace(".svg", "-framed.svg")

    with open(input_file, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Parse viewBox: "x y w h"
    vb_match = re.search(r'viewBox=["\']([^"\']+)["\']', svg_content)
    if not vb_match:
        print("Error: no viewBox attribute found.")
        sys.exit(1)

    vb_values = vb_match.group(1).split()
    if len(vb_values) != 4:
        print("Error: unexpected viewBox format.")
        sys.exit(1)

    vb_x, vb_y, vb_w, vb_h = [float(v) for v in vb_values]

    # The rect sits padding pt outside the original content bounds
    rect_x = vb_x - padding
    rect_y = vb_y - padding
    rect_w = vb_w + 2 * padding
    rect_h = vb_h + 2 * padding

    # The viewBox must also accommodate the outer half of the stroke
    half = FRAME_WIDTH / 2
    expand = padding + half
    new_vb_x = vb_x - expand
    new_vb_y = vb_y - expand
    new_vb_w = vb_w + 2 * expand
    new_vb_h = vb_h + 2 * expand

    # Format helper: strip unnecessary trailing zeros
    def fmt(v):
        return f"{v:g}"

    new_viewbox = f"{fmt(new_vb_x)} {fmt(new_vb_y)} {fmt(new_vb_w)} {fmt(new_vb_h)}"

    # Update viewBox
    svg_content = re.sub(r'viewBox=["\'][^"\']+["\']', f'viewBox="{new_viewbox}"', svg_content)

    # Update width and height attributes on the <svg> tag
    svg_content = re.sub(
        r'width=["\']([0-9.]+)([a-z%]*)["\']',
        lambda m: f'width="{fmt(float(m.group(1)) + 2 * expand)}{m.group(2)}"',
        svg_content
    )
    svg_content = re.sub(
        r'height=["\']([0-9.]+)([a-z%]*)["\']',
        lambda m: f'height="{fmt(float(m.group(1)) + 2 * expand)}{m.group(2)}"',
        svg_content
    )

    # Build the frame rect
    rect = (f'<rect x="{fmt(rect_x)}" y="{fmt(rect_y)}" '
            f'width="{fmt(rect_w)}" height="{fmt(rect_h)}" '
            f'fill="none" stroke="black" stroke-width="{FRAME_WIDTH}"/>')

    # Insert rect after <defs>...</defs> block if present, else after opening <svg> tag
    if '</defs>' in svg_content:
        svg_content = svg_content.replace('</defs>', f'</defs>\n{rect}', 1)
    else:
        svg_content = re.sub(r'(<svg\b[^>]*>)', r'\1\n' + rect, svg_content, count=1)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Framed SVG saved as {output_file}")

def parse_padding(value):
    m = re.fullmatch(r'([0-9.]+)pt', value.strip())
    if not m:
        print(f"Error: unrecognized padding '{value}'. Use e.g. '10pt'.")
        sys.exit(1)
    return float(m.group(1))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add_svg_frame.py <input-file.svg> [padding]")
        print("  padding  optional space between content and frame, e.g. 10pt (default: 0pt)")
        print("           Units must be pt. Only valid for dvisvgm-generated SVGs, where")
        print("           width/height are in pt and viewBox units match (1 viewBox unit = 1pt).")
    else:
        padding = parse_padding(sys.argv[2]) if len(sys.argv) >= 3 else 0
        add_frame(sys.argv[1], padding=padding)
