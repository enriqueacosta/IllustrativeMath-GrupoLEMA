#!/usr/bin/env python3
"""
Enrique Acosta, 2025
Convert an act-*.ptx files into a single Pandoc-Markdown* file that renders neatly 
as  Word, but it may also partially work for Reveal.js slides, PDF (Beamer), or PowerPoint.

╭─────────────────────────────  What the script does  ───────────────────────────╮
│ 1. Reads a *.ptx* file that contains one `<activity>` element.                 │
│ 2. Resolves all `<custom ref="…"/>` placeholders using                         │
│       ../meta/customizations/textos-constantes-v1.ptx                          │
│    so, for example, `<custom ref="recommended-time-titulo"/>` becomes          │
│    “Tiempo recomendado”.                                                       │
│ 3. Builds slides in this order (unless flags change it):                       │
│       • Statement  (title “Enunciado”)                                         │
│       • Solution   (title “Solución”)                                          │
│       • All <paragraphs> in <prelude>                                          │
│       • All <paragraphs> in <postlude>                                         │
│ 4. Each `<paragraphs>` block becomes one ## markdown section.                  │
│ 5. Supported inline conversions                                                │
│       <m> … </m>        →  $…$   (inline LaTeX)                                │
│       <me> … </me>      →  $$ … $$ (display math)                              │
│       <image source="foo" width="60%">                                         │
│                         →  `<img src="../assets/foo.png" width="60%">`         │
│       <q> … </q>        →  « … »                                               │
│ 6. `<sidebyside>` is **flattened**: the first “column” is emitted, a blank     │
│    line is inserted, then the second column, etc. `<stack>` wrappers are       │
│    ignored; only their children appear.                                        │
│ 7. Lists keep proper numbering: 1. → a. → 1. for nesting levels 0/1/2+.        │
│ 8. The resulting Markdown is written to the output file.                       │
╰─────────────────────────────────────────────────────────────────────────────────╯

Command-line flags
──────────────────
--prelude-first      Place all <prelude> slides **before** the statement slide
--no-solution        Do not include the <solution> slide
--minimal            Within every <paragraphs> slide:
                       · keep **only** <p> or <li> elements that contain a <q>
                       · drop the entire slide if nothing remains after pruning

Usage
─────
    python createActivitiyPandocMD.py activity.ptx activity.md
    python createActivitiyPandocMD.py activity.ptx activity.md --prelude-first
    python createActivitiyPandocMD.py activity.ptx activity.md --no-solution
    python createActivitiyPandocMD.py activity.ptx activity.md --minimal

Typical Pandoc step afterwards
──────────────────────────────
    pandoc activity.md -o activity.docx                          # Word
    pandoc activity.md -t revealjs -s -o activity.html           # slides
    pandoc activity.md -o activity.pdf --pdf-engine=xelatex      # Beamer PDF
    pandoc activity.md -o activity.pptx                          # PowerPoint

Limitations
───────────
* Images are **not automatically centred** in DOCX/PPTX due to a Pandoc
  limitation; centre manually or via template if needed.
* Column widths and multi-column layouts in DOCX are not preserved; the
  script flattens side-by-side content vertically instead.
* Only the subset of PTX tags listed above is handled. Unknown tags fall
  through as plain text.
"""

from __future__ import annotations
import sys, argparse, textwrap, string, re, copy
from pathlib import Path
from xml.etree import ElementTree as ET

INDENT = "    "


# ───────── helpers (unchanged) ─────────────────────────────────────────
def strip_ns(tag: str) -> str:
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

# ───────── minimal-mode utilities ──────────────────────────────────────
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

# ───────── inline conversion (unchanged) ───────────────────────────────
def inline_md(el: ET.Element, const: dict[str, str]) -> str:
    tag = strip_ns(el.tag)
    if tag == "m":
        return f"${el.text}$"
    if tag == "me":
        return f"\n$${el.text}$$\n"
    if tag == "image":
        src   = el.get("source", "").strip()
        width = (el.get("width") or "").strip()

        # 1 ── normalise: add .png if no ext, prepend ../assets/, URL-encode spaces
        if not src.lower().endswith((".svg", ".png", ".jpg", ".jpeg", ".gif")):
            src += ".png"
        if not src.startswith("../assets/"):
            src = "../assets/" + src
        src = src.replace(" ", "%20")                     # ← NEW (encode spaces)

        # 2 & 3 ── always output Markdown-figure syntax so DOCX keeps the image
        if width:
            if not width.endswith("%"):
                width += "%"
            return f"![]({src}){{width=\"{width}\"}}"     # ← CHANGED
        return f"![]({src})"                              # ← (unchanged path)
    if tag == "custom":
        ref = el.get("ref")
        if ref and ref in const:
            return const[ref]
        return el.text.strip() if el.text else xml_str(el)
    if tag == "q":
        inner = "".join(inline_md(c, const) for c in el)
        return f"«{(el.text or '')}{inner}»"
    parts = [el.text or ""]
    for c in el:
        parts.append(inline_md(c, const))
        if c.tail:
            parts.append(c.tail)
    return "".join(parts)

# ───────── side-by-side flattening (unchanged) ─────────────────────────
def sidebyside_md(node: ET.Element, const: dict[str, str], lvl: int) -> list[str]:
    out, first = [], True
    for col in node:
        if not first:
            out.append("")
        first = False
        if strip_ns(col.tag) == "stack":
            for inner in col:
                out += block_md(inner, const, lvl)
        else:
            out += block_md(col, const, lvl)
    return out

# ───────── block-level conversion (unchanged) ──────────────────────────
def block_md(el: ET.Element, const: dict[str, str], lvl: int = 0) -> list[str]:
    tag = strip_ns(el.tag)
    o: list[str] = []
    if tag == "p":
        o += [inline_md(el, const).strip(), ""]
    elif tag == "line":
        o.append(inline_md(el, const).rstrip())
        if el.tail and el.tail.strip():
            o.append(el.tail.strip())
    elif tag in ("ol", "ul"):
        for i, li in enumerate(el.findall("./li"), start=1):
            o += block_md_li(li, const, lvl, i if tag == "ol" else None)
        o.append("")
    elif tag == "sidebyside":
        o += sidebyside_md(el, const, lvl)
    elif tag == "xi:include":
        o += ["```xml", xml_str(el), "```", ""]
    else:
        o += [inline_md(el, const).strip(), ""]
    return o

def block_md_li(li: ET.Element, const: dict[str, str], lvl: int, num: int | None) -> list[str]:
    bullet = bullet_label(num, lvl) if num is not None else "-"
    prefix = INDENT * lvl + bullet + " "
    out: list[str] = []

    if not (li.text or "").strip() and len(li) and strip_ns(li[0].tag) == "p":
        first = li[0]
        p_lines = block_md(first, const, lvl)
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
            head.append(inline_md(c, const).strip())
            if c.tail and c.tail.strip():
                head.append(c.tail.strip())
        out.append(prefix + (" ".join(head) or " "))
    for c in li:
        t = strip_ns(c.tag)
        if t in ("ol", "ul"):
            out += block_md(c, const, lvl + 1)
        elif t == "p":
            para = textwrap.indent("\n".join(block_md(c, const, lvl + 1)), INDENT * (lvl + 1))
            out.append(para)
    return out

# ───────── slide helper ────────────────────────────────────────────────
def slide(title: str, body: list[str]) -> list[str]:
    return [f"## {title}", ""] + body

# ───────── main ────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Convert PTX to Pandoc Markdown slides.")
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--prelude-first", action="store_true",
                    help="render prelude slides before statement slide")
    ap.add_argument("--no-solution", action="store_true",
                    help="omit the solution slide")
    ap.add_argument("--minimal", action="store_true",
                    help="within <paragraphs> keep only <p>/<li> containing <q>")
    args = ap.parse_args()

    in_f, out_f = Path(args.input), Path(args.output)
    CONST = load_constants(in_f)

    root = ET.parse(in_f).getroot()
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
            heading = inline_md(h_el, CONST) if h_el is not None else "(sin título)"
            body = [ln for ch in work_para if strip_ns(ch.tag) != "title"
                    for ln in block_md(ch, CONST)]
            slides.append(slide(heading, body))
        return slides

    # prelude before?
    if args.prelude_first:
        md += sum(slides_of("prelude"), [])

    # statement slide
    stmt = root.find("./statement")
    if stmt is not None:
        md += slide("Enunciado", [ln for ch in stmt for ln in block_md(ch, CONST)])

    # solution slide (unless suppressed)
    if not args.no_solution:
        sol = root.find("./solution")
        if sol is not None:
            md += slide("Solución", [ln for ch in sol for ln in block_md(ch, CONST)])

    # prelude after, if not first
    if not args.prelude_first:
        md += sum(slides_of("prelude"), [])

    # postlude always
    md += sum(slides_of("postlude"), [])

    Path(out_f).write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_f}")

if __name__ == "__main__":
    main()
