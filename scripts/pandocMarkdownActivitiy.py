#!/usr/bin/env python3
"""
Enrique Acosta, 2025  
Convert an act-*.ptx, warm-*.ptx, cool-*.ptx, files into a single Pandoc-Markdown  
file that renders neatly as docx Word, but it may also partially work for Reveal.js  
slides, PDF (Beamer), or PowerPoint.

╭─────────────────────────────  What the script does  ───────────────────────────╮
│ 1. Reads a *.ptx* file that contains one `<activity>` element (or corresponding│
│    warm and cool tags).                                                        │
│ 2. Resolves all `<custom ref="…"/>` placeholders using                         │
│       ../meta/customizations/textos-constantes-v1.ptx                          │
│    so, for example, `<custom ref="recommended-time-titulo"/>` becomes          │
│    “Tiempo recomendado”.                                                       │
│ 3. Resolves all `<xi:include href="…"/>` directives using XInclude.            │
│    The script uses `lxml.etree` to expand includes before processing content.  │
│ 4. Builds slides in this order (unless flags change it):                       │
│       • Statement  (title “Enunciado”)                                         │
│       • Solution   (title “Solución”)                                          │
│       • All <paragraphs> in <prelude>                                          │
│       • All <paragraphs> in <postlude>                                         │
│ 5. Each `<paragraphs>` block becomes one ## markdown section.                  │
│ 6. Supported inline conversions:                                               │
│       <m> … </m>        →  $…$   (inline LaTeX)                                │
│       <me> … </me>      →  $$ … $$ (display math)                              │
│       <image>           →  `![](../assets/foo.png){width=…}`                   │
│                          Width is taken from @width (e.g., "45%") on the image,│
│                          or inherited from an enclosing <sidebyside>. It is    │
│                          converted to inches unless --keep-percentage-widths   │
│                          is used.                                              │
│       <q> … </q>        →  « … »                                               │
│ 7. `<sidebyside>` is **flattened**: the first “column” is emitted, a blank     │
│    line is inserted, then the second column, etc. `<stack>` wrappers are       │
│    ignored; only their children appear.                                        │
│ 8. Lists keep proper numbering: 1. → a. → 1. for nesting levels 0/1/2+.        │
│ 9. The resulting Markdown is written to the output file.                       │
╰────────────────────────────────────────────────────────────────────────────────╯

Command-line flags
──────────────────
--prelude-first      Place all <prelude> slides **before** the statement slide  
--no-solution        Do not include the <solution> slide  
--minimal            Within every <paragraphs> slide:  
                       · keep **only** <p> or <li> elements that contain a <q>  
                       · drop the entire slide if nothing remains after pruning  
--keep-percentage-widths  Keep image widths as percentages (e.g., 45%) instead of
                          converting them to absolute inches.
--convert-svg        Convert extensionless <image> sources from their .pdf version to
                     a high-res .png. Width is calculated from the .svg version.
                     Requires ImageMagick to be installed.

Usage
─────
  python pandocMarkdownActivitiy.py <path to activity.ptx>  
  python pandocMarkdownActivitiy.py <path to activity.ptx> --prelude-first  
  python pandocMarkdownActivitiy.py <path to activity.ptx> --no-solution  
  python pandocMarkdownActivitiy.py <path to activity.ptx> --minimal  

Typical Pandoc step afterwards
──────────────────────────────
  pandoc activity.md -o activity.docx                                 # Word  
  pandoc activity.md -t revealjs -s -o activity.html                  # slides  
  pandoc activity.md -o activity.pdf --pdf-engine=xelatex             # Beamer PDF  
  pandoc activity.md -o activity.pptx --reference-doc template5.pptx  # PowerPoint  

Limitations
───────────
* Images are **not automatically centred** in DOCX/PPTX due to a Pandoc  
  limitation; centre manually or via template if needed.  
* Column widths and multi-column layouts in DOCX are not preserved; the  
  script flattens side-by-side content vertically instead.  
* Image width is inherited from the enclosing <sidebyside> widths attribute  
  if not explicitly set, but layout remains vertical.  
* Only the subset of PTX tags listed above is handled. Unknown tags fall  
  through as plain text.
"""

from __future__ import annotations
import sys, argparse, textwrap, string, re, copy
from pathlib import Path
import subprocess # Needed for running external commands

# Use lxml.etree instead of xml.etree for XInclude support
from lxml import etree as ET

INDENT = "    "
# Assumed text width for a standard document (e.g., 8.5" paper with 1" margins)
DEFAULT_DOC_WIDTH_INCHES = 6.5
# DPI for SVG to PNG conversion
SVG_CONVERSION_DPI = 300


# ───────── SVG/PDF Conversion Helpers ────────────────────────────────
def get_svg_pixel_width(svg_path: Path) -> float:
    """Parses an SVG file to find its intrinsic pixel width."""
    try:
        svg_tree = ET.parse(str(svg_path))
        svg_root = svg_tree.getroot()
        width_str = svg_root.get("width", "")
        if width_str:
            return float(re.sub(r"[a-zA-Z%]+", "", width_str))
        viewBox = svg_root.get("viewBox")
        if viewBox:
            return float(viewBox.split()[2])
    except Exception as e:
        print(f"Warning: Could not parse SVG dimensions from {svg_path.name}: {e}", file=sys.stderr)
    return 0.0

def run_pdf_to_png_conversion(pdf_path: Path, png_path: Path):
    """If the target PNG doesn't exist, converts the PDF using ImageMagick."""
    if not pdf_path.exists():
        print(f"Warning: PDF source file not found at {pdf_path}", file=sys.stderr)
        return

    if not png_path.exists():
        print(f"Converting PDF: {pdf_path.name} -> {png_path.name}")
        command = [
            "magick", "convert",
            "-density", str(SVG_CONVERSION_DPI),
            "-background", "none",
            str(pdf_path),
            str(png_path)
        ]
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            print("FATAL ERROR: `magick` command not found. Please install ImageMagick and ensure it is in your PATH.", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"FATAL ERROR: ImageMagick failed to convert {pdf_path.name}.", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
            sys.exit(1)


# ───────── helpers ─────────────────────────────────────────
def strip_ns(tag) -> str:
    if not isinstance(tag, str): return ""
    return tag.split("}", 1)[-1]

def xml_str(el: ET.Element) -> str:
    return ET.tostring(el, encoding="unicode").strip()

def bullet_label(num: int, lvl: int) -> str:
    if lvl == 0: return f"{num}."
    if lvl == 1:
        i, j = divmod(num - 1, 26)
        return (string.ascii_lowercase[i - 1] if i else "") + string.ascii_lowercase[j] + "."
    return f"{num}."

def load_constants(base: Path) -> dict[str, str]:
    p = (base.parent / "../meta/customizations/textos-constantes-v1.ptx").resolve()
    d: dict[str, str] = {}
    try:
        root = ET.parse(p).getroot()
        for c in root.findall(".//custom"):
            if c.get("name") and c.text: d[c.get("name")] = c.text.strip()
    except FileNotFoundError: pass
    return d

# ───────── minimal-mode utilities ──────────────────────────
def has_q(elem: ET.Element) -> bool:
    if strip_ns(elem.tag) == "q": return True
    return any(has_q(child) for child in elem)

def prune_for_minimal(paragraphs: ET.Element) -> ET.Element | None:
    new_para = copy.copy(paragraphs); new_para.clear()
    for child in paragraphs:
        tag = strip_ns(child.tag)
        if tag == "title": new_para.append(child); continue
        if tag == "p" and has_q(child): new_para.append(child)
        elif tag in ("ol", "ul"):
            new_list = copy.copy(child); new_list.clear()
            for li in child.findall("./li"):
                if has_q(li): new_list.append(li)
            if len(new_list): new_para.append(new_list)
    keep = any(strip_ns(c.tag) != "title" for c in new_para)
    return new_para if keep else None


# ───────── inline conversion ──────────────────────────────
def inline_md(el: ET.Element, const: dict[str, str], keep_percentage_widths: bool, convert_svg: bool, input_dir: Path) -> str:
    tag = strip_ns(el.tag)
    if tag == "m": return f"${el.text}$"
    if tag == "me": return f"\n$${el.text}$$\n"
    if tag == "image":
        src = el.get("source", "").strip()
        width = el.get("width", "").strip()

        # 1 ── Inherit width if not explicitly set on the tag
        if not width:
            parent = el.getparent()
            while parent is not None:
                if strip_ns(parent.tag) == "sidebyside":
                    widths_attr = parent.get("widths")
                    if not widths_attr:
                        container = parent.getparent()
                        if container is not None: widths_attr = container.get("widths")
                    if widths_attr:
                        widths = widths_attr.split()
                        column_el = el
                        while column_el.getparent() is not None and column_el.getparent() != parent:
                            column_el = column_el.getparent()
                        siblings = [s for s in parent if isinstance(s.tag, str)]
                        try:
                            idx = siblings.index(column_el)
                            if idx < len(widths): width = widths[idx].strip()
                        except ValueError: pass
                    break
                parent = parent.getparent()
        
        # 2 ── Normalize path (with integrated conversion logic)
        is_conversion_case = convert_svg and not Path(src).suffix
        
        # Start with the original path normalization logic.
        if not src.startswith("../assets/"):
            src = "../assets/" + src
        
        # After normalization, handle the PDF-to-PNG conversion case.
        if is_conversion_case:
            # The SVG path is needed for width calculation.
            svg_abs_path = (input_dir / src).with_suffix('.svg').resolve()
            # The PDF path is the source for the conversion command.
            pdf_abs_path = svg_abs_path.with_suffix('.pdf')
            # The final output is a PNG.
            png_abs_path = svg_abs_path.with_suffix('.png')
            
            run_pdf_to_png_conversion(pdf_abs_path, png_abs_path)
            
            # The final source path in the markdown points to the new PNG.
            src += '.png'
            
            # If no width was found from attributes/inheritance, calculate it from the SVG.
            if not width:
                pixel_width = get_svg_pixel_width(svg_abs_path)
                if pixel_width > 0:
                    physical_width_in = pixel_width / SVG_CONVERSION_DPI
                    percentage = (physical_width_in / DEFAULT_DOC_WIDTH_INCHES) * 100
                    width = f"{percentage:.0f}%"
                else:
                    width = "4in" # Fallback
        else:
            # For non-conversion cases, just ensure it has a .png if it had no extension.
            if not Path(src).suffix:
                 src += ".png"
        
        src = src.replace(" ", "%20")

        # 3 ── Process the final width string
        final_width_str = ""
        if not width:
            final_width_str = "4in"
        elif keep_percentage_widths:
            final_width_str = width
        else: # Convert percentage string to inches.
            try:
                percentage_val = float(width.strip('%'))
                final_width_str = f"{(percentage_val / 100.0) * DEFAULT_DOC_WIDTH_INCHES:.2f}in"
            except (ValueError, TypeError):
                final_width_str = "4in"

        return f"![]({src}){{width=\"{final_width_str}\"}}"

    if tag == "custom":
        ref = el.get("ref"); return const[ref] if ref and ref in const else (el.text.strip() if el.text else xml_str(el))
    if tag == "q":
        inner = "".join(inline_md(c, const, keep_percentage_widths, convert_svg, input_dir) for c in el)
        return f"«{(el.text or '')}{inner}»"

    parts = [el.text or ""]
    for c in el:
        child_tag = strip_ns(c.tag)
        if child_tag in ("sidebyside", "ol", "ul"):
            parts.append("\n\n" + "\n".join(block_md(c, const, keep_percentage_widths, convert_svg, input_dir, lvl=0)).strip() + "\n\n")
        else:
            parts.append(inline_md(c, const, keep_percentage_widths, convert_svg, input_dir))
        if c.tail: parts.append(c.tail)
    return "".join(parts)

# --- Block processing functions now pass `input_dir` down ---
def sidebyside_md(node: ET.Element, const: dict[str, str], keep_percentage_widths: bool, convert_svg: bool, input_dir: Path, lvl: int) -> list[str]:
    out, first = [], True
    for col in node:
        if not first: out.append("")
        first = False
        if strip_ns(col.tag) in ("stack", "div", "col"):
            for inner in col: out += block_md(inner, const, keep_percentage_widths, convert_svg, input_dir, lvl)
        else:
            out += block_md(col, const, keep_percentage_widths, convert_svg, input_dir, lvl)
    return out

def block_md(el: ET.Element, const: dict[str, str], keep_percentage_widths: bool, convert_svg: bool, input_dir: Path, lvl: int = 0) -> list[str]:
    tag = strip_ns(el.tag)
    o: list[str] = []
    if tag == "p":
        content = inline_md(el, const, keep_percentage_widths, convert_svg, input_dir).strip()
        if content: o.extend(content.splitlines()); o.append("")
    elif tag == "line":
        o.append(inline_md(el, const, keep_percentage_widths, convert_svg, input_dir).rstrip())
        if el.tail and el.tail.strip(): o.append(el.tail.strip())
    elif tag in ("ol", "ul"):
        for i, li in enumerate(el.findall("./li"), start=1):
            o += block_md_li(li, const, keep_percentage_widths, convert_svg, input_dir, lvl, i if tag == "ol" else None)
        o.append("")
    elif tag == "sidebyside":
        o += sidebyside_md(el, const, keep_percentage_widths, convert_svg, input_dir, lvl)
    elif tag == "xi:include":
        o += ["```xml", xml_str(el), "```", ""]
    else:
        content = inline_md(el, const, keep_percentage_widths, convert_svg, input_dir).strip()
        if content: o += [content, ""]
    return o

def block_md_li(li: ET.Element, const: dict[str, str], keep_percentage_widths: bool, convert_svg: bool, input_dir: Path, lvl: int, num: int | None) -> list[str]:
    bullet = bullet_label(num, lvl) if num is not None else "*"
    prefix = INDENT * lvl + bullet + " "
    content = inline_md(li, const, keep_percentage_widths, convert_svg, input_dir).strip()
    lines = content.split('\n')
    if not lines or not lines[0].strip(): return []
    out = [prefix + lines[0].lstrip()]
    indent_prefix = ' ' * len(prefix)
    for line in lines[1:]:
        if line.strip(): out.append(indent_prefix + line)
        else: out.append("")
    return out

def slide(title: str, body: list[str]) -> list[str]: return [f"## {title}", ""] + body

# ───────── main ─────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Convert PTX to Pandoc Markdown slides.", formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("input", help="input .ptx file")
    ap.add_argument("--prelude-first", action="store_true", help="render prelude slides before statement slide")
    ap.add_argument("--no-solution", action="store_true", help="omit the solution slide")
    ap.add_argument("--minimal", action="store_true", help="within <paragraphs> keep only <p>/<li> containing <q>")
    ap.add_argument("--keep-percentage-widths", action="store_true", help="keep image widths as percentages instead of converting to inches")
    ap.add_argument("--convert-svg", action="store_true", help="Convert extensionless <image> sources from their .pdf version to a high-res .png")
    args = ap.parse_args()

    in_f = Path(args.input)
    out_f = in_f.with_suffix(".md")
    # The directory of the main input file is the root for resolving all relative asset paths.
    input_dir = in_f.parent

    CONST = load_constants(in_f)
    
    parser = ET.XMLParser(load_dtd=True, recover=True)
    tree = ET.parse(str(in_f), parser)
    tree.xinclude()
    root = tree.getroot()

    title = root.findtext("./title", "(sin título)").replace('"', r"\"")
    md = ["---", 'title: "IM+LEMA: Actividad editable"', "slideLevel: 2", "---", "", f"# {title}", ""]

    def slides_of(section: str) -> list[list[str]]:
        slides = []
        for para in root.findall(f".//{section}//paragraphs"):
            work_para = para
            if args.minimal:
                pruned = prune_for_minimal(para)
                if pruned is None: continue
                work_para = pruned
            h_el = work_para.find("./title")
            heading = inline_md(h_el, CONST, args.keep_percentage_widths, args.convert_svg, input_dir) if h_el is not None else "(sin título)"
            body = [ln for ch in work_para if hasattr(ch, "tag") and strip_ns(ch.tag) != "title" for ln in block_md(ch, CONST, args.keep_percentage_widths, args.convert_svg, input_dir)]
            slides.append(slide(heading, body))
        return slides

    if args.prelude_first: md += sum(slides_of("prelude"), [])
    stmt = root.find("./statement")
    if stmt is not None: md += slide("Enunciado", [ln for ch in stmt for ln in block_md(ch, CONST, args.keep_percentage_widths, args.convert_svg, input_dir)])
    if not args.no_solution:
        sol = root.find("./solution")
        if sol is not None: md += slide("Solución", [ln for ch in sol for ln in block_md(ch, CONST, args.keep_percentage_widths, args.convert_svg, input_dir)])
    if not args.prelude_first: md += sum(slides_of("prelude"), [])
    md += sum(slides_of("postlude"), [])

    Path(out_f).write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_f}")

if __name__ == "__main__":
    main()