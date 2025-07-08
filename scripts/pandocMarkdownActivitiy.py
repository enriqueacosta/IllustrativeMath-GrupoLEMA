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

# Use lxml.etree instead of xml.etree for XInclude support
from lxml import etree as ET

INDENT = "    "
# Assumed text width for a standard document (e.g., 8.5" paper with 1" margins)
DEFAULT_DOC_WIDTH_INCHES = 6.5


# ───────── helpers (unchanged) ─────────────────────────────────────────
def strip_ns(tag) -> str:
    if not isinstance(tag, str):
        return ""
    return tag.split("}", 1)[-1]

def xml_str(el: ET.Element) -> str:
    return ET.tostring(el, encoding="unicode").strip()

def bullet_label(num: int, lvl: int) -> str:
    if lvl == 0:
        return f"{num}."
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
            if c.get("name") and c.text:
                d[c.get("name")] = c.text.strip()
    except FileNotFoundError:
        pass
    return d

# ───────── minimal-mode utilities (unchanged) ──────────────────────────
def has_q(elem: ET.Element) -> bool:
    """Return True if element has any <q> descendant."""
    if strip_ns(elem.tag) == "q":
        return True
    return any(has_q(child) for child in elem)

def prune_for_minimal(paragraphs: ET.Element) -> ET.Element | None:
    """
    Return a pruned shallow copy of <paragraphs> keeping only:
      • <p> that contain <q>
      • lists (<ol>/<ul>) where each <li> is kept only if it contains <q>
    If nothing remains, return None.
    """
    new_para = copy.copy(paragraphs)           # shallow copy (keeps attribs)
    new_para.clear()                           # we'll append filtered kids

    for child in paragraphs:
        tag = strip_ns(child.tag)
        if tag == "title":                     # keep title unchanged
            new_para.append(child)
            continue
        if tag == "p" and has_q(child):
            new_para.append(child)
        elif tag in ("ol", "ul"):
            new_list = copy.copy(child); new_list.clear()
            for li in child.findall("./li"):
                if has_q(li):
                    new_list.append(li)
            if len(new_list):                  # keep list only if something left
                new_para.append(new_list)

    # after filtering, are there non-title children?
    keep = any(strip_ns(c.tag) != "title" for c in new_para)
    return new_para if keep else None

# ───────── inline conversion (SIMPLIFIED) ──────────────────────────────
def inline_md(el: ET.Element, const: dict[str, str], keep_percentage_widths: bool) -> str:
    tag = strip_ns(el.tag)
    if tag == "m":
        return f"${el.text}$"
    if tag == "me":
        return f"\n$${el.text}$$\n"
    if tag == "image":
        src = el.get("source", "").strip()
        width = el.get("width", "").strip()

        # 1 ── Normalize path
        if not src.lower().endswith((".svg", ".png", ".jpg", ".jpeg", ".gif")):
            src += ".png"
        if not src.startswith("../assets/"):
            src = "../assets/" + src
        src = src.replace(" ", "%20")

        # 2 ── If width is not set, try to inherit from <sidebyside> or its container
        if not width:
            parent = el.getparent()
            while parent is not None:
                if strip_ns(parent.tag) == "sidebyside":
                    widths_attr = parent.get("widths")
                    if not widths_attr:
                        container = parent.getparent()
                        if container is not None:
                            widths_attr = container.get("widths")

                    if widths_attr:
                        widths = widths_attr.split()
                        column_el = el
                        while column_el.getparent() is not None and column_el.getparent() != parent:
                            column_el = column_el.getparent()
                        siblings = [s for s in parent if isinstance(s.tag, str)]
                        try:
                            idx = siblings.index(column_el)
                            if idx < len(widths):
                                width = widths[idx].strip()
                        except ValueError:
                            pass
                    break
                parent = parent.getparent()

        # 3 ── Process width, knowing it's always a percentage string like "45%"
        final_width = ""
        if not width:
            final_width = "4in"  # Fallback for no width
        elif keep_percentage_widths:
            final_width = width  # Use the "45%" string directly
        else:
            # Convert percentage to absolute inches
            try:
                percentage_val = float(width.strip('%'))
                absolute_width = (percentage_val / 100.0) * DEFAULT_DOC_WIDTH_INCHES
                final_width = f"{absolute_width:.2f}in"
            except (ValueError, TypeError):
                final_width = "4in" # Fallback on conversion error

        return f"![]({src}){{width=\"{final_width}\"}}"
    if tag == "custom":
        ref = el.get("ref")
        if ref and ref in const:
            return const[ref]
        return el.text.strip() if el.text else xml_str(el)
    if tag == "q":
        inner = "".join(inline_md(c, const, keep_percentage_widths) for c in el)
        return f"«{(el.text or '')}{inner}»"
    parts = [el.text or ""]
    for c in el:
        parts.append(inline_md(c, const, keep_percentage_widths))
        if c.tail:
            parts.append(c.tail)
    return "".join(parts)

# ───────── side-by-side flattening (MODIFIED) ──────────────────────────
def sidebyside_md(node: ET.Element, const: dict[str, str], keep_percentage_widths: bool, lvl: int) -> list[str]:
    out, first = [], True
    for col in node:
        if not first:
            out.append("")
        first = False
        if strip_ns(col.tag) == "stack":
            for inner in col:
                out += block_md(inner, const, keep_percentage_widths, lvl)
        else:
            out += block_md(col, const, keep_percentage_widths, lvl)
    return out

# ───────── block-level conversion (MODIFIED) ───────────────────────────
def block_md(el: ET.Element, const: dict[str, str], keep_percentage_widths: bool, lvl: int = 0) -> list[str]:
    tag = strip_ns(el.tag)
    o: list[str] = []
    if tag == "p":
        o += [inline_md(el, const, keep_percentage_widths).strip(), ""]
    elif tag == "line":
        o.append(inline_md(el, const, keep_percentage_widths).rstrip())
        if el.tail and el.tail.strip():
            o.append(el.tail.strip())
    elif tag in ("ol", "ul"):
        for i, li in enumerate(el.findall("./li"), start=1):
            o += block_md_li(li, const, keep_percentage_widths, lvl, i if tag == "ol" else None)
        o.append("")
    elif tag == "sidebyside":
        o += sidebyside_md(el, const, keep_percentage_widths, lvl)
    elif tag == "xi:include":
        o += ["```xml", xml_str(el), "```", ""]
    else:
        o += [inline_md(el, const, keep_percentage_widths).strip(), ""]
    return o

def block_md_li(li: ET.Element, const: dict[str, str], keep_percentage_widths: bool, lvl: int, num: int | None) -> list[str]:
    bullet = bullet_label(num, lvl) if num is not None else "-"
    prefix = INDENT * lvl + bullet + " "
    out: list[str] = []

    if not (li.text or "").strip() and len(li) and strip_ns(li[0].tag) == "p":
        first = li[0]
        p_lines = block_md(first, const, keep_percentage_widths, lvl)
        out.append(prefix + p_lines.pop(0).strip())
        for ln in p_lines:
            out.append(textwrap.indent(ln, INDENT * (lvl + 1)))
        li.remove(first)
    else:
        head = []
        if li.text and li.text.strip():
            head.append(li.text.strip())
        inline_k, block_k = [], []
        for c in li:
            (inline_k if strip_ns(c.tag) not in ("ol", "ul", "p") else block_k).append(c)
        for c in inline_k:
            head.append(inline_md(c, const, keep_percentage_widths).strip())
            if c.tail and c.tail.strip():
                head.append(c.tail.strip())
        out.append(prefix + (" ".join(head) or " "))
    for c in li:
        t = strip_ns(c.tag)
        if t in ("ol", "ul"):
            out += block_md(c, const, keep_percentage_widths, lvl + 1)
        elif t == "p":
            para = textwrap.indent("\n".join(block_md(c, const, keep_percentage_widths, lvl + 1)), INDENT * (lvl + 1))
            out.append(para)
    return out

# ───────── slide helper (unchanged) ────────────────────────────────────
def slide(title: str, body: list[str]) -> list[str]:
    return [f"## {title}", ""] + body

# ───────── main (MODIFIED) ─────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Convert PTX to Pandoc Markdown slides.")
    ap.add_argument("input", help="input .ptx file")
    ap.add_argument("--prelude-first", action="store_true",
                    help="render prelude slides before statement slide")
    ap.add_argument("--no-solution", action="store_true",
                    help="omit the solution slide")
    ap.add_argument("--minimal", action="store_true",
                    help="within <paragraphs> keep only <p>/<li> containing <q>")
    ap.add_argument("--keep-percentage-widths", action="store_true",
                    help="keep image widths as percentages instead of converting to inches")
    args = ap.parse_args()

    in_f = Path(args.input)
    out_f = in_f.with_suffix(".md")

    CONST = load_constants(in_f)

    # Parse the XML and expand any <xi:include href="..."/> directives
    parser = ET.XMLParser(load_dtd=True, recover=True)  # Allow recovery and DTD loading
    tree = ET.parse(str(in_f), parser)
    tree.xinclude()
    root = tree.getroot()

    title = root.findtext("./title", "(sin título)").replace('"', r"\"")

    md = [
        "---",
        'title: "IM+LEMA: Actividad editable"',
        "slideLevel: 2",
        "---",
        "",
        f"# {title}",
        "",
    ]

    # ----- helper to build slides from <paragraphs> -----
    def slides_of(section: str) -> list[list[str]]:
        slides = []
        for para in root.findall(f".//{section}//paragraphs"):
            work_para = para
            if args.minimal:  # prune content
                pruned = prune_for_minimal(para)
                if pruned is None:
                    continue           # skip empty slide
                work_para = pruned

            h_el = work_para.find("./title")
            heading = inline_md(h_el, CONST, args.keep_percentage_widths) if h_el is not None else "(sin título)"
            body = [ln for ch in work_para if hasattr(ch, "tag") and strip_ns(ch.tag) != "title"
                    for ln in block_md(ch, CONST, args.keep_percentage_widths)]
            slides.append(slide(heading, body))
        return slides

    # prelude before?
    if args.prelude_first:
        md += sum(slides_of("prelude"), [])

    # statement slide
    stmt = root.find("./statement")
    if stmt is not None:
        md += slide("Enunciado", [ln for ch in stmt for ln in block_md(ch, CONST, args.keep_percentage_widths)])

    # solution slide (unless suppressed)
    if not args.no_solution:
        sol = root.find("./solution")
        if sol is not None:
            md += slide("Solución", [ln for ch in sol for ln in block_md(ch, CONST, args.keep_percentage_widths)])

    # prelude after, if not first
    if not args.prelude_first:
        md += sum(slides_of("prelude"), [])

    # postlude always
    md += sum(slides_of("postlude"), [])

    Path(out_f).write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_f}")

if __name__ == "__main__":
    main()